#!/usr/bin/env python3
"""Optional Windows-side worker to complete music on existing Instagram carousel.

Run on Android-connected PC using Task Scheduler. Disabled unless explicitly
enabled with INSTAGRAM_ANDROID_MUSIC_ENABLED=true. Never creates Instagram posts.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from instagram_mobile_music import Android, QueueError, select_pending
from instagram_queue import read_document, validate_manifest, validate_state

ROOT=Path(__file__).resolve().parent.parent
CLAIM_DIR=Path.home()/".instagram-tue-android-music"

def pending_tasks(manifest: dict, state: dict) -> list[dict]:
    validate_state(state)
    tasks=[]
    for post in validate_manifest(manifest):
        if not (post["kind"]=="carousel" and post.get("approved") is True
                and post.get("distribution_mode")=="api_carousel_then_native_music"
                and post.get("owner_authorized_two_step_music") is True):
            continue
        try:
            candidate=select_pending(manifest,state,post["id"])
        except QueueError:
            continue
        if candidate["track"] and candidate["artist"]:
            tasks.append(candidate)
    return tasks

def update_checkout() -> None:
    def git(*args):
        return subprocess.run(["git",*args],cwd=ROOT,capture_output=True,
                              text=True,check=True,timeout=60).stdout
    try:
        if git("status","--porcelain").strip():
            raise QueueError("Há alterações locais; não atualizar o checkout.")
        git("pull","--ff-only","origin","main")
    except (OSError,subprocess.SubprocessError):
        raise QueueError("Falha no git pull seguro; nenhuma edição do Instagram.") from None

def reserve_once(identifier: str, media_id: str) -> bool:
    if (not identifier.replace("_","").replace("-","").isalnum()
            or not media_id.isdigit()):
        raise QueueError("ID inválido para reserva.")
    CLAIM_DIR.mkdir(parents=True,exist_ok=True)
    path=CLAIM_DIR/(identifier+"-"+media_id+".claim")
    try:
        with path.open("x",encoding="utf-8") as f:
            json.dump({"id":identifier,"media_id":media_id,
                       "policy":"one UI attempt, no automatic retry"},f)
    except FileExistsError:
        return False
    return True

def run_once(*, execute: bool, refresh: bool) -> dict[str,Any]:
    if refresh:
        update_checkout()
    manifest=read_document(ROOT/"content/schedule.json")
    state=read_document(ROOT/"content/publication-state.json")
    tasks=pending_tasks(manifest,state)
    if not execute or os.environ.get("INSTAGRAM_ANDROID_MUSIC_ENABLED")!="true":
        return {"ok":True,"mode":"dry_run","approved_music_tasks":len(tasks),
                "mobile_write_enabled":False}
    if len(tasks)!=1:
        return {"ok":True,"mode":"blocked","approved_music_tasks":len(tasks),
                "reason":"Exactly one approved music task is required"}
    task=tasks[0]
    Android().preflight()
    if not reserve_once(task["id"],str(task["media_id"])):
        return {"ok":True,"mode":"already_attempted","id":task["id"]}
    proc=subprocess.run([sys.executable,str(ROOT/"scripts/instagram_mobile_music.py"),
                         "--id",task["id"],"--execute"],
                        cwd=ROOT,capture_output=True,text=True,timeout=240)
    if proc.returncode!=0:
        return {"ok":False,"mode":"needs_manual_review","id":task["id"],
                "reason":"Android UI result unverified; one-shot claim retained"}
    return {"ok":True,"mode":"music_verified","id":task["id"]}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--skip-pull",action="store_true",
                        help="Read-only offline diagnostics only")
    args=parser.parse_args(argv)
    try:
        result=run_once(execute=args.execute,refresh=not args.skip_pull)
        print(json.dumps(result,ensure_ascii=False))
        return 0 if result["ok"] else 1
    except (QueueError,OSError,ValueError) as exc:
        print(json.dumps({"ok":False,"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())

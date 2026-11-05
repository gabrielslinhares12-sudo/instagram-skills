#!/usr/bin/env python3
"""Safely resume the exact owner-approved 05NOV Lúmino carousel after a *pre-claim* failure.

This program never creates a new queue item, never regenerates media, and
never retries a previously claimed Instagram post. It reconciles remote Git
ledger and recent Meta feed before the first mutation. Publishes only the
six immutable, exact-match original JPGs pinned in GitHub.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from facebook_poster import FacebookConfig, FacebookPoster
from instagram_preflight import check as check_preflight
from instagram_queue import (
    GitLedger, QueueError, read_document, validate_manifest,
    validate_state, run_queue, plan,
)

TARGET_ID = "tue-2026-11-05-lumino-historia-final-aprovada"
TARGET = "https://www.instagram.com/temumaexplicacao/"
REPO = "gabrielslinhares12-sudo/instagram-skills"
PINNED = "ce0b441ac5303fd1eb477eeab148b48da6058639"
MEDIA_DIR = Path("content/media/instagram/2026-11-05/LUMINO-HISTORIA-FINAL-APROVADO")
QUEUE_PATH = Path("content/schedule.json")
STATE_PATH = Path("content/publication-state.json")
HASHES = (
    "7d5b4ce12a307cb1a4a58de95c379646210134f5f286f296965fe3cfbf67ec88",
    "8f009dcc82e9341d74c0e4fa899a1070b10b2422a381225adbc2dda3f124ca35",
    "e242d3fd3b0a3fd5e8296ec8330b5d5aeace6dc198c0a7169b7a42bf003ce490",
    "eaf58274cdc0f9edda32995d62ef8fdb6de3e91f36dafcdf303a5d2bb848c78a",
    "3dad49f3b20b489209e1d4c2602b8c2e81c38e449b7d8499853dfaee21c1fb62",
    "03375b61b262214559892a41258a9f40cda1f57031717acd92f4b6f97a127952",
)
MEDIA_URLS = [
    f"https://raw.githubusercontent.com/{REPO}/{PINNED}/{MEDIA_DIR.as_posix()}/LUMINO-HISTORIA-FINAL-{i:02}.jpg"
    for i in range(1, 7)
]
MARKER = "#HistoriaDoLumino"

class Blocked(Exception):
    pass

def safe_git(*args: str) -> str:
    try:
        p = subprocess.run(["git", *args], text=True, capture_output=True,
                           check=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise Blocked("git_sync_failed") from exc
    return p.stdout.strip()

def local_manifest() -> dict:
    all_posts = validate_manifest(read_document(QUEUE_PATH))
    matching = [p for p in all_posts if p["id"] == TARGET_ID]
    if len(matching) != 1:
        raise Blocked("expected_single_approved_item_not_found")
    post = matching[0]
    if not (
        post.get("username") == "temumaexplicacao"
        and post.get("target_url") == TARGET
        and post.get("approved") is True
        and post.get("kind") == "carousel"
        and post.get("media_sha256") == list(HASHES)
        and post.get("media_urls") == MEDIA_URLS
        and post.get("distribution_mode") == "api_carousel_without_native_music"
        and post.get("owner_authorized_without_music") is True
        and post.get("ai_origin") == "synthetic"
        and post.get("content_style") == "clearly_illustrated"
        and MARKER in post.get("caption","")
    ):
        raise Blocked("queue_media_identity_or_approval_changed")
    return post

def qc():
    from PIL import Image
    for i, sha in enumerate(HASHES, 1):
        local = MEDIA_DIR/f"LUMINO-HISTORIA-FINAL-{i:02}.jpg"
        if not local.is_file() or hashlib.sha256(local.read_bytes()).hexdigest() != sha:
            raise Blocked(f"original_jpeg_integrity_failed_{i}")
        with Image.open(local) as im:
            if im.format != "JPEG" or im.size != (1080, 1350):
                raise Blocked(f"approved_image_dimensions_failed_{i}")
        req=Request(MEDIA_URLS[i-1],headers={"User-Agent":"TUE-Instagram-QC/1.0"})
        try:
            with urlopen(req,timeout=40) as response:
                data=response.read(4*1024*1024+1)
        except (HTTPError,URLError,OSError):
            raise Blocked(f"public_jpeg_access_failed_{i}") from None
        if hashlib.sha256(data).hexdigest()!=sha:
            raise Blocked(f"public_jpeg_integrity_failed_{i}")
        print(f"APPROVED_PUBLIC_ORIGINAL_{i}_VERIFIED=true",flush=True)

def check_duplicate(poster):
    data=poster._request("GET",poster.config.user_id+"/media",
        params={"fields":"id,media_type,caption,permalink","limit":100},
        timeout=35)
    if not isinstance(data.get("data"),list):
        raise Blocked("cannot_read_instagram_feed_to_check_duplicate")
    for item in data["data"]:
        if (isinstance(item,dict) and item.get("media_type") == "CAROUSEL_ALBUM"
            and MARKER in (item.get("caption") or "")):
            print("EXISTING_CAROUSEL="+json.dumps({
                "media_id":item.get("id"),"permalink":item.get("permalink"),
                "status":"already_published_no_retry",
            },ensure_ascii=False),flush=True)
            return True
    return False

def main() -> int:
    if os.getenv("GITHUB_REF") != "refs/heads/main":
        raise Blocked("not_main_branch")
    # Refresh every relevant file; never trust the workflow triggering SHA as the latest.
    safe_git("pull","--ff-only","origin","main")
    state=validate_state(read_document(STATE_PATH,missing={"version":1,"items":{}}))
    recorded=state["items"].get(TARGET_ID)
    if recorded is not None:
        print("ALREADY_CLAIMED_NO_RETRY="+json.dumps(
            {k: recorded.get(k) for k in ("status","media_id","claimed_at","published_at")},
            ensure_ascii=False),flush=True)
        return 0
    post=local_manifest()
    qc()
    poster=FacebookPoster(FacebookConfig.from_env())
    pre=check_preflight(poster)
    if pre.get("ok") is not True or pre.get("username") != "temumaexplicacao":
        raise Blocked("preflight_account_or_permissions_not_verified")
    if check_duplicate(poster):
        return 0
    state=validate_state(read_document(STATE_PATH,missing={"version":1,"items":{}}))
    if state["items"].get(TARGET_ID) is not None:
        raise Blocked("another_worker_claimed_post")
    now=datetime.now(timezone.utc)
    timing=plan([post],state,now)[0]["status"]
    print("SINGLE_POST_PLAN="+timing,flush=True)
    if timing != "due":
        raise Blocked("post_outside_approved_due_window")
    safe_git("config","user.name","github-actions[bot]")
    safe_git("config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
    result=run_queue([post],state,now,execute=True,enabled=True,
                     persist=GitLedger(STATE_PATH),poster_factory=lambda:poster)
    print("META_PUBLICATION_RESULT="+json.dumps(result,ensure_ascii=False),flush=True)
    if not result.get("ok") or result.get("status") != "published":
        raise Blocked("meta_not_confirmed_do_not_retry_automatically")
    try:
        detail=poster._request("GET",str(result["media_id"]),
            params={"fields":"id,permalink,media_type"},timeout=30)
        print("META_PERMALINK="+json.dumps(detail,ensure_ascii=False),flush=True)
    except Exception:
        print("META_PUBLICATION_CONFIRMED_BUT_LINK_LOOKUP_UNAVAILABLE",flush=True)
    return 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except (Blocked,QueueError) as exc:
        print("SAFE_RESUME_BLOCKED="+str(exc),file=sys.stderr,flush=True)
        sys.exit(1)
    except Exception as exc:
        print("SAFE_RESUME_EXCEPTION="+type(exc).__name__,file=sys.stderr,flush=True)
        sys.exit(1)

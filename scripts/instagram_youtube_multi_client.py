#!/usr/bin/env python3
"""Download a selected TUE-owned Short using several official yt-dlp clients.

Runs inside GitHub Actions; stores MP4 only as private artifact. Never publishes.
Each attempt remains serial and bounded. No cookies, proxy, credential or paid API.
"""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re
import sys
import time
from zoneinfo import ZoneInfo

import yt_dlp
from instagram_download_approved_tue_short import verify_mp4, DownloadError

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "content/editorial/REELS-E-STORIES-2026-11-02-a-08.json"
OUT = ROOT / "output/youtube-reel-import"
CHANNEL_ID = "UCeVMYZs1z9HecuK0cPKnHgQ"
CLIENTS = ("tv", "web_safari", "android_vr")


def get_entry(day):
    doc = json.loads(PLAN.read_text(encoding="utf-8"))
    posts = [x for x in doc["reels"] if x.get("day") == day and x.get("slot") == "18:00"]
    if len(posts) != 1:
        raise DownloadError("No unique Reel slot for specified day")
    post = posts[0]
    vid = post.get("source_video_id")
    if (not isinstance(vid, str) or not re.fullmatch("[A-Za-z0-9_-]{11}", vid)
            or post.get("source_channel") != "Tem Uma Explicação YouTube PT"
            or post.get("source_video_url") != "https://www.youtube.com/shorts/" + vid
            or post.get("reel_published") or post.get("approved")):
        raise DownloadError("Reel not verified as selected and awaiting download")
    return vid, post


def cleanup(vid):
    for p in OUT.glob(vid + ".*"):
        if p.is_file():
            p.unlink()


def attempt_download(vid, client):
    url = "https://www.youtube.com/shorts/" + vid
    options = {
        "quiet": True, "no_warnings": False, "noplaylist": True,
        "outtmpl": str(OUT / (vid + ".%(ext)s")),
        "format": "bv*[height<=1920][ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
        "merge_output_format": "mp4", "max_filesize": 200 * 1024 * 1024,
        "socket_timeout": 15, "retries": 1, "fragment_retries": 1,
        "extractor_retries": 0, "concurrent_fragment_downloads": 1,
        "extractor_args": {"youtube": {"player_client": [client]}},
    }
    with yt_dlp.YoutubeDL(options) as dl:
        info = dl.extract_info(url, download=True)
    if not isinstance(info, dict) or info.get("channel_id") != CHANNEL_ID:
        raise DownloadError("Downloaded metadata channel_id did not match owner channel")
    files = list(OUT.glob(vid + ".mp4"))
    if len(files) != 1:
        raise DownloadError("Downloaded media not MP4")
    qc = verify_mp4(files[0])
    return files[0], info, qc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", default=datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat())
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    state = {
        "day": args.day, "slot": "18:00 America/Sao_Paulo",
        "channel_id": CHANNEL_ID, "method": "yt-dlp with Deno EJS, sequential client profiles",
        "drive_folder_id": "1R4t22XHMEIfbZJjvttOWekXMyfJuKDAK",
        "published": False, "approval": False, "origin_review": "pending",
        "attempts": [], "status": "blocked"}
    try:
        vid, post = get_entry(args.day)
        state["id"] = vid
        state["url"] = post["source_video_url"]
        for client in CLIENTS:
            cleanup(vid)
            print("TRY_CLIENT=" + client, flush=True)
            try:
                f, info, qc = attempt_download(vid, client)
                state["attempts"].append({"client": client, "result": "success"})
                state["status"] = "downloaded_for_review"
                state["file"] = {"name": f.name, **qc}
                state["video_title"] = info.get("title")
                print("VERIFIED_MP4=" + f.name, flush=True)
                break
            except (yt_dlp.utils.DownloadError, DownloadError, OSError) as exc:
                msg = str(exc)
                safe = ("youtube_login_required" if "Sign in to confirm" in msg or "not a bot" in msg
                        else "download_or_QC_failure")
                state["attempts"].append({"client": client, "result": safe,
                                          "exception_type": type(exc).__name__})
                print("CLIENT_RESULT=" + client + " " + safe, flush=True)
                cleanup(vid)
                time.sleep(2)
        if state["status"] != "downloaded_for_review":
            state["reason"] = "All supported clients failed; authenticated original required"
    except (DownloadError, OSError, KeyError, ValueError) as exc:
        state["reason"] = str(exc)[:150]
    (OUT / "multi-client-report.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("IMPORT_FINAL_STATUS=" + state["status"], flush=True)
    return 0 if state["status"] == "downloaded_for_review" else 1


if __name__ == "__main__":
    sys.exit(main())

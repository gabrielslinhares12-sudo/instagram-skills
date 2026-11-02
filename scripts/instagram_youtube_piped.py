#!/usr/bin/env python3
"""One-shot Piped proxy retrieval for the selected owner-channel YouTube Short.

No scraping credentials and no upload to Instagram. Streams must come from
published Piped instances, pass identity and MP4/audio QC before any Drive upload.
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, build_opener
from urllib.error import URLError, HTTPError

from instagram_download_approved_tue_short import (
    HttpsOnly, DownloadError, verify_mp4, safe_https, CHUNK, MAX_BYTES
)

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "content/editorial/REELS-E-STORIES-2026-11-02-a-08.json"
OUT = ROOT / "output/youtube-reel-import"
CHANNEL = "UCeVMYZs1z9HecuK0cPKnHgQ"
API_HOSTS = (
    "https://pipedapi.kavin.rocks",
    "https://pipedapi.adminforge.de",
    "https://piped-api.privacy.com.de",
)
ALLOWED_STREAM_SUFFIX = (
    ".kavin.rocks", ".adminforge.de", ".privacy.com.de", ".piped.yt",
)


def select():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    matches = [x for x in plan["reels"] if x.get("day") == "2026-11-02"]
    if len(matches) != 1:
        raise DownloadError("Missing selected video for target day")
    entry = matches[0]
    vid = entry.get("source_video_id")
    if (not isinstance(vid, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{11}", vid)
            or entry.get("source_video_url") != "https://www.youtube.com/shorts/" + vid
            or entry.get("approved") or entry.get("reel_published")):
        raise DownloadError("Selected owner Short missing or already published")
    return vid


def stream_valid(url):
    if not isinstance(url, str) or not safe_https(url):
        return False
    host = (urlsplit(url).hostname or "").lower()
    return any(host.endswith(s) for s in ALLOWED_STREAM_SUFFIX)


def download(url, path):
    if not stream_valid(url):
        raise DownloadError("Untrusted proxy stream")
    opener = build_opener(HttpsOnly())
    with opener.open(Request(url, headers={"Accept": "video/mp4,audio/mp4,application/octet-stream"}),
                     timeout=55) as response:
        if response.status != 200:
            raise DownloadError("Streaming status not 200")
        typ = response.headers.get("Content-Type", "").split(";")[0].lower()
        if typ not in ("video/mp4", "audio/mp4", "application/octet-stream"):
            raise DownloadError("Streaming MIME is not MP4 audio/video")
        total = 0
        with path.open("wb") as f:
            while True:
                b = response.read(CHUNK)
                if not b:
                    break
                total += len(b)
                if total > MAX_BYTES:
                    raise DownloadError("Stream exceeds size limit")
                f.write(b)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    state = {"source": "Piped public API", "status": "blocked",
             "published": False, "attempts": [],
             "drive_folder": "1R4t22XHMEIfbZJjvttOWekXMyfJuKDAK"}
    tmp_files = []
    try:
        vid = select()
        state["video_id"] = vid
        output = OUT / (vid + ".mp4")
        opener = build_opener(HttpsOnly())
        for host in API_HOSTS:
            attempt = {"api": host, "result": "unavailable"}
            state["attempts"].append(attempt)
            print("PIPED_TEST=" + host, flush=True)
            try:
                api = host + "/streams/" + vid
                with opener.open(Request(api, headers={"Accept": "application/json"}),
                                 timeout=20) as response:
                    raw = response.read(240000)
                metadata = json.loads(raw.decode("utf-8"))
                if metadata.get("uploaderUrl") != "/channel/" + CHANNEL:
                    raise DownloadError("Piped uploader channel ID mismatch")
                if metadata.get("livestream") is True:
                    raise DownloadError("Live media not eligible")
                seconds = metadata.get("duration")
                if not isinstance(seconds, (int,float)) or not 5 <= seconds <= 180:
                    raise DownloadError("Duration missing/outside Short limit")
                streamlist = [s for s in metadata.get("videoStreams", [])
                              if isinstance(s,dict) and s.get("mimeType") == "video/mp4"
                              and stream_valid(s.get("url"))]
                streamlist.sort(key=lambda x: x.get("height") or 0, reverse=True)
                audio = [s for s in metadata.get("audioStreams", [])
                         if isinstance(s,dict) and s.get("mimeType") == "audio/mp4"
                         and stream_valid(s.get("url"))]
                audio.sort(key=lambda x: x.get("bitrate") or 0, reverse=True)
                if not streamlist:
                    raise DownloadError("No MP4 video stream")
                for video in streamlist[:1]:
                    vpath = OUT / (vid + ".video.partial")
                    apath = OUT / (vid + ".audio.partial")
                    tmp_files.extend([vpath, apath])
                    download(video["url"], vpath)
                    if video.get("videoOnly") is True:
                        if not audio:
                            raise DownloadError("No M4A audio stream")
                        download(audio[0]["url"], apath)
                        subprocess.run(["ffmpeg","-y","-v","error",
                                        "-i",str(vpath),"-i",str(apath),
                                        "-map","0:v:0","-map","1:a:0",
                                        "-c","copy",str(output)],
                                       check=True, timeout=65, capture_output=True)
                    else:
                        vpath.replace(output)
                    qc = verify_mp4(output)
                    state["status"] = "downloaded_for_review"
                    state["file"] = {"name": output.name, **qc}
                    attempt["result"] = "downloaded_verified"
                    print("VERIFIED_MP4=" + output.name, flush=True)
                    break
                if state["status"] == "downloaded_for_review":
                    break
            except (DownloadError, URLError, HTTPError, TimeoutError, OSError,
                    ValueError, subprocess.SubprocessError) as exc:
                attempt["error_type"] = type(exc).__name__
                attempt["result"] = "api_http_" + str(exc.code) if isinstance(exc,HTTPError) else "failed"
                output.unlink(missing_ok=True)
                for f in tmp_files:
                    f.unlink(missing_ok=True)
        if state["status"] != "downloaded_for_review":
            state["reason"] = "No Piped instance returned valid owner MP4"
    except (OSError, DownloadError, ValueError) as exc:
        state["reason"] = str(exc)[:160]
    finally:
        for f in tmp_files:
            f.unlink(missing_ok=True)
    (OUT / "piped-report.json").write_text(
        json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("PIPED_FINAL=" + state["status"], flush=True)
    return 0 if state["status"] == "downloaded_for_review" else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Download one owner-channel YouTube Short by its URL through a documented public service.

No Instagram publication, no authentication bypass, no credentials; fail closed on
untrusted/missing media. Derived files are kept only in a GitHub Actions artifact.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "content/editorial/REELS-E-STORIES-2026-11-02-a-08.json"
OUT = ROOT / "output/youtube-reel-import"
REPORT = OUT / "download-report.json"
YT_CHANNEL = "UCeVMYZs1z9HecuK0cPKnHgQ"
API = "https://save.brianrianrehan.com/api/v1/download?wait=true&download=true"
MAX_BYTES = 200 * 1024 * 1024
CHUNK = 256 * 1024


class DownloadError(Exception):
    pass


def safe_https(url: str) -> bool:
    try:
        u = urlsplit(url)
        if (u.scheme != "https" or not u.hostname or u.username or
                u.password or u.port not in (None, 443)):
            return False
        host = u.hostname.lower().rstrip(".")
        if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
            return False
        try:
            ipaddress.ip_address(host)
            return False
        except ValueError:
            return "." in host
    except ValueError:
        return False


class HttpsOnly(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not safe_https(newurl):
            raise DownloadError("Redirect outside public HTTPS host")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def selected_entry() -> dict:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    entries = [x for x in plan.get("reels", [])
               if x.get("day") == "2026-11-02" and x.get("slot") == "18:00"]
    if len(entries) != 1:
        raise DownloadError("Expected exactly one selected Reel for today")
    item = entries[0]
    vid = item.get("source_video_id")
    import re
    if (not isinstance(vid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid)
            or item.get("source_channel") != "Tem Uma Explicação YouTube PT"
            or item.get("approved") is True or item.get("reel_published") is True):
        raise DownloadError("Reel must be selected and unpublished")
    expected = "https://www.youtube.com/shorts/" + vid
    if item.get("source_video_url") != expected:
        raise DownloadError("Video link does not match selected ID")
    return {"id": vid, "url": expected, "title": item.get("source_video_title"),
            "views_approx": item.get("youtube_public_views_approx")}


def verify_mp4(path: Path) -> dict:
    size = path.stat().st_size
    if not 1024 * 128 <= size <= MAX_BYTES:
        raise DownloadError("MP4 size is missing or outside limits")
    with path.open("rb") as f:
        header = f.read(16)
    if len(header) < 12 or header[4:8] != b"ftyp":
        raise DownloadError("Media is not a valid MP4 container header")
    try:
        proc = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                               "-show_format", "-of", "json", str(path)],
                              capture_output=True, text=True, timeout=30, check=True)
        data = json.loads(proc.stdout)
    except (FileNotFoundError, ValueError, subprocess.SubprocessError) as exc:
        raise DownloadError("ffprobe failed to validate the MP4") from exc
    streams = data.get("streams") or []
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    if len(video) != 1 or not audio:
        raise DownloadError("MP4 requires a video stream and audio")
    w, h = int(video[0].get("width", 0)), int(video[0].get("height", 0))
    seconds = float(data.get("format", {}).get("duration", 0))
    if not (w >= 360 and h >= 640 and h > w and 5 <= seconds <= 180):
        raise DownloadError("MP4 needs vertical orientation and a Short duration")
    return {"width": w, "height": h, "duration_seconds": round(seconds, 2),
            "video_codec": video[0].get("codec_name"),
            "audio_codec": audio[0].get("codec_name"),
            "bytes": size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def download_via_site(url: str, path: Path) -> dict:
    if not safe_https(url) or not url.startswith("https://www.youtube.com/shorts/"):
        raise DownloadError("Only the owner's selected public Short URL is accepted")
    if not safe_https(API):
        raise DownloadError("Downloader API URL must use public HTTPS")
    payload = json.dumps({"url": url, "format": "video",
                          "quality": "best", "outputFormat": "mp4"}).encode("utf-8")
    req = Request(API, data=payload,
                  headers={"Content-Type": "application/json", "Accept": "video/mp4,application/octet-stream"},
                  method="POST")
    opener = build_opener(HttpsOnly())
    try:
        with opener.open(req, timeout=110) as response:
            if response.status != 200:
                raise DownloadError("Downloader did not return a completed MP4")
            mime = response.headers.get("Content-Type", "").split(";")[0].lower().strip()
            if mime not in ("video/mp4", "application/octet-stream", "application/mp4",
                            "video/quicktime", "binary/octet-stream"):
                raise DownloadError("Service returned non-video content")
            total = 0
            with path.open("wb") as dst:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_BYTES:
                        raise DownloadError("MP4 exceeds limit")
                    dst.write(chunk)
    except HTTPError as exc:
        status = exc.code
        # 425 is a queued/unready job. Do not launch another download.
        if status in (425, 429, 413):
            raise DownloadError(f"Public download service status {status}; no unsafe retry") from exc
        raise DownloadError(f"Public download service HTTP {status}") from exc
    except (URLError, TimeoutError) as exc:
        raise DownloadError("Public download service unavailable") from exc
    return verify_mp4(path)


def download_via_freeapi(url: str, path: Path) -> dict:
    """Fallback to a documented free URL-to-MP4 API. Never trust returned metadata."""
    if not safe_https(url) or not url.startswith("https://www.youtube.com/shorts/"):
        raise DownloadError("Only selected channel URLs may be downloaded")
    endpoint = "https://freeapi.pro/api/alldl?" + urlencode({"url": url})
    req = Request(endpoint, headers={"Accept": "application/json"}, method="GET")
    opener = build_opener(HttpsOnly())
    try:
        with opener.open(req, timeout=30) as response:
            if response.status != 200:
                raise DownloadError("Fallback downloader returned non-200")
            raw = response.read(64 * 1024 + 1)
        if len(raw) > 64 * 1024:
            raise DownloadError("Fallback metadata response exceeds limit")
        info = json.loads(raw.decode("utf-8"))
        if info.get("success") is not True or not isinstance(info.get("mediaInfo"), dict):
            raise DownloadError("Fallback downloader did not resolve video")
        media = info["mediaInfo"]
        direct = media.get("videoUrl")
        if not isinstance(direct, str) or not safe_https(direct):
            raise DownloadError("Fallback did not return a public HTTPS MP4 URL")
        if urlsplit(direct).hostname in ("www.youtube.com", "youtube.com", "youtu.be"):
            raise DownloadError("Fallback returned the watch page instead of video")
        req = Request(direct, headers={"Accept": "video/mp4,application/octet-stream"})
        with opener.open(req, timeout=100) as response:
            if response.status != 200:
                raise DownloadError("Fallback media download was not successful")
            mimetype = response.headers.get("Content-Type", "").split(";")[0].lower().strip()
            if mimetype not in ("video/mp4", "application/octet-stream", "application/mp4",
                                "binary/octet-stream", "video/quicktime"):
                raise DownloadError("Fallback returned non-video MIME type")
            total = 0
            with path.open("wb") as dst:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_BYTES:
                        raise DownloadError("Fallback media exceeds allowed size")
                    dst.write(chunk)
    except HTTPError as exc:
        raise DownloadError(f"Fallback service HTTP {exc.code}") from exc
    except (URLError, TimeoutError, ValueError, UnicodeError) as exc:
        raise DownloadError("Fallback service could not provide a valid MP4") from exc
    return verify_mp4(path)


def download_via_gendownload(url: str, path: Path) -> dict:
    """Resolve owner's selected Short with GenDownload's documented public API."""
    if not safe_https(url) or not url.startswith("https://www.youtube.com/shorts/"):
        raise DownloadError("Invalid selected channel Short")
    body = json.dumps({"url": url}).encode("utf-8")
    opener = build_opener(HttpsOnly())
    try:
        req = Request("https://gendownload.com/api/extract",
                      data=body,
                      headers={"Content-Type": "application/json", "Accept": "application/json"},
                      method="POST")
        with opener.open(req, timeout=40) as response:
            if response.status != 200:
                raise DownloadError("GenDownload extraction did not return 200")
            payload = response.read(64 * 1024 + 1)
        if len(payload) > 64 * 1024:
            raise DownloadError("GenDownload metadata is oversized")
        info = json.loads(payload.decode("utf-8"))
        formats = info.get("formats")
        if not isinstance(formats, list):
            raise DownloadError("GenDownload did not return media formats")
        viable = [f for f in formats
                  if isinstance(f, dict) and f.get("type") == "video"
                  and f.get("ext") == "mp4"
                  and isinstance(f.get("url"), str)
                  and safe_https(f["url"])]
        if not viable:
            raise DownloadError("GenDownload returned no MP4 format")
        # Up to 2 format variants, avoiding bulk requests and excessive storage.
        for chosen in viable[:2]:
            target = chosen["url"]
            req = Request(target, headers={"Accept": "video/mp4,application/octet-stream"},
                          method="GET")
            try:
                with opener.open(req, timeout=100) as response:
                    if response.status != 200:
                        continue
                    mime = response.headers.get("Content-Type", "").split(";")[0].lower().strip()
                    if mime not in ("video/mp4", "application/octet-stream", "application/mp4",
                                    "binary/octet-stream", "video/quicktime"):
                        continue
                    total = 0
                    with path.open("wb") as dst:
                        while True:
                            chunk = response.read(CHUNK)
                            if not chunk:
                                break
                            total += len(chunk)
                            if total > MAX_BYTES:
                                raise DownloadError("GenDownload MP4 exceeds allowed size")
                            dst.write(chunk)
                try:
                    return verify_mp4(path)
                except DownloadError:
                    path.unlink(missing_ok=True)
                    continue
            except (HTTPError, URLError, TimeoutError):
                path.unlink(missing_ok=True)
                continue
        raise DownloadError("GenDownload could not supply a valid vertical MP4 with audio")
    except HTTPError as exc:
        raise DownloadError(f"GenDownload extraction HTTP {exc.code}") from exc
    except (URLError, TimeoutError, ValueError, UnicodeError) as exc:
        raise DownloadError("GenDownload extraction unavailable") from exc


def download_with_fallback(url: str, path: Path) -> tuple[dict, str]:
    errors = []
    for label, handler in (("WebDownloader", download_via_site),
                           ("FreeAPI", download_via_freeapi),
                           ("GenDownload", download_via_gendownload)):
        path.unlink(missing_ok=True)
        try:
            return handler(url, path), label
        except DownloadError as exc:
            errors.append(label + ": " + str(exc))
    path.unlink(missing_ok=True)
    raise DownloadError("; ".join(errors))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    state = {"source_channel_id": YT_CHANNEL, "operation": "download_only",
             "target_day": "2026-11-02", "target_slot_local": "18:00",
             "downloader": "WebDownloader public API v1, URL only",
             "published": False, "approved": False,
             "original_rights_review": "pending",
             "ai_origin_review": "pending"}
    try:
        chosen = selected_entry()
        state["selected"] = chosen
        file = OUT / (chosen["id"] + ".mp4")
        qc, provider = download_with_fallback(chosen["url"], file)
        state["download_provider"] = provider
        state.update({"status": "downloaded_pending_editorial_qc",
                      "file": {"name": file.name, **qc}})
        print("MP4_VERIFIED=" + str(file.name), flush=True)
    except DownloadError as exc:
        state.update({"status": "blocked_no_publish", "reason": str(exc)})
        for file in OUT.glob("*.mp4"):
            file.unlink(missing_ok=True)
        print("DOWNLOAD_BLOCKED=" + str(exc), file=sys.stderr, flush=True)
    REPORT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if state["status"] == "downloaded_pending_editorial_qc" else 1


if __name__ == "__main__":
    raise SystemExit(main())

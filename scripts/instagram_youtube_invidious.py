#!/usr/bin/env python3
"""Invidious API read-only source verification + owner-video media download.
Only documented public instances. No publication or authentication tokens.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from zoneinfo import ZoneInfo

from instagram_download_approved_tue_short import (
    HttpsOnly, safe_https, DownloadError, verify_mp4, MAX_BYTES, CHUNK
)
from instagram_youtube_multi_client import get_entry, OUT, CHANNEL_ID

INSTANCES = (
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://invidious.tiekoetter.com",
)
ACCEPT = ("video/mp4", "application/octet-stream", "binary/octet-stream")


def request_json(url):
    if not safe_https(url):
        raise DownloadError("Non-HTTPS instance URL")
    opener = build_opener(HttpsOnly())
    with opener.open(Request(url, headers={"Accept": "application/json",
                                         "User-Agent": "TUE-Instagram-import/1.0"}),
                     timeout=18) as response:
        data = response.read(200 * 1024 + 1)
        if len(data) > 200 * 1024:
            raise DownloadError("Oversized response from public Invidious")
        return json.loads(data.decode("utf-8"))


def download_stream(url, path):
    if not safe_https(url):
        raise DownloadError("Insecure stream URL")
    opener = build_opener(HttpsOnly())
    with opener.open(Request(url, headers={"Accept": "video/mp4"}), timeout=65) as resp:
        if resp.status != 200:
            raise DownloadError("Stream HTTP non-200")
        ct = resp.headers.get("Content-Type", "").split(";")[0].lower().strip()
        if ct not in ACCEPT:
            raise DownloadError("Invidious response not MP4")
        length = 0
        with path.open("wb") as file:
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                length += len(chunk)
                if length > MAX_BYTES:
                    raise DownloadError("MP4 exceeds size limit")
                file.write(chunk)
    return verify_mp4(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", default=datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat())
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"source": "public Invidious API", "day": args.day, "published": False,
              "drive_folder": "1R4t22XHMEIfbZJjvttOWekXMyfJuKDAK",
              "attempts": [], "status": "blocked"}
    try:
        video_id, entry = get_entry(args.day)
        report["video_id"] = video_id
        target = OUT / (video_id + ".mp4")
        for host in INSTANCES:
            target.unlink(missing_ok=True)
            attempt = {"instance": host, "result": "failed"}
            report["attempts"].append(attempt)
            print("TEST_INSTANCE=" + host, flush=True)
            try:
                meta = request_json(host + "/api/v1/videos/" + video_id)
                if meta.get("videoId") != video_id or meta.get("authorId") != CHANNEL_ID:
                    raise DownloadError("Author/channel ID not verified")
                streams = meta.get("formatStreams") or []
                mp4 = [x for x in streams if isinstance(x, dict)
                       and (x.get("type") or "").startswith("video/mp4")
                       and str(x.get("itag", "")).isdigit()]
                mp4.sort(key=lambda x: int(str(x.get("qualityLabel", "0p")).replace("p","")
                                                .split("x")[0]) if str(x.get("qualityLabel", "")).endswith("p") else 0,
                         reverse=True)
                if not mp4:
                    raise DownloadError("No progressive MP4 with audio listed")
                # Invidious documents the local proxied latest_version endpoint.
                for s in mp4[:2]:
                    itag = str(s["itag"])
                    proxy = host + "/latest_version?" + urlencode({
                        "id": video_id, "itag": itag, "local": "true"})
                    try:
                        qc = download_stream(proxy, target)
                        report["status"] = "downloaded_for_review"
                        report["file"] = {"name": target.name, **qc}
                        report["instance"] = host
                        attempt["result"] = "success"
                        print("VALIDATED_ORIGINAL=" + target.name, flush=True)
                        break
                    except (DownloadError, HTTPError, URLError, TimeoutError, OSError):
                        target.unlink(missing_ok=True)
                if report["status"] == "downloaded_for_review":
                    break
                raise DownloadError("No valid progressive stream was delivered")
            except (HTTPError, URLError, TimeoutError, OSError, ValueError, DownloadError) as exc:
                attempt["type"] = type(exc).__name__
                attempt["result"] = ("instance_http_" + str(exc.code)) if isinstance(exc, HTTPError) else "unavailable_or_failed_qc"
                target.unlink(missing_ok=True)
        if report["status"] != "downloaded_for_review":
            report["reason"] = "Public instances did not deliver source MP4"
    except (DownloadError, OSError, ValueError, KeyError) as exc:
        report["reason"] = str(exc)[:140]
    (OUT / "invidious-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("STATUS=" + report["status"], flush=True)
    return 0 if report["status"] == "downloaded_for_review" else 1


if __name__ == "__main__":
    sys.exit(main())

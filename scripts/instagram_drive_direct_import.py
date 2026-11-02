#!/usr/bin/env python3
"""Import the one owner-approved Reel from Google Drive directly in GitHub Actions.

Use Drive's public media endpoint only when anonymously accessible, otherwise
the owner's separate Drive OAuth refresh-token secrets. No credentials or
private download URLs are recorded. Never regard a Drive preview HTML page
as MP4. The original must match the archive SHA-256 before public staging.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

FILE_ID = "16o_d6_R-bDXQSpC0Mu-KP-UOoHjL5hEQ"
SOURCE_URL = "https://drive.google.com/file/d/" + FILE_ID + "/view"
API_URL = "https://www.googleapis.com/drive/v3/files/" + FILE_ID + "?alt=media"
PUBLIC_URL = "https://drive.google.com/uc?export=download&id=" + FILE_ID
EXPECTED_SHA256 = "ae4892d2c9c3b7215bb621d1c4d79e5a2669938428c97345effbf6a113d96fba"
EXPECTED_BYTES = 41994355
OUTPUT = Path("output/instagram-drive-reel") / "H9WGKaO5XQ4.mp4"
REPORT = Path("output/instagram-drive-reel") / "import-report.json"


class ImportErrorSafe(Exception):
    pass


def summary(status: str, **items):
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    result = {"status": status, "source": "google_drive", "file_id": FILE_ID,
              "expected_sha256": EXPECTED_SHA256, "publishing_attempted": False,
              "target": "@temumaexplicacao", **items}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("TUE_DRIVE_IMPORT=" + status, flush=True)


class NoAuthRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        if request.get_header("Authorization"):
            raise ImportErrorSafe("oauth_media_redirect_refused")
        parsed = urllib.parse.urlsplit(newurl)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or not (host == "drive.google.com"
            or host == "drive.usercontent.google.com"
            or host.endswith(".googleusercontent.com")):
            raise ImportErrorSafe("unexpected_public_drive_redirect")
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def get_oauth_token():
    names = ("GDRIVE_OAUTH_CLIENT_ID", "GDRIVE_OAUTH_CLIENT_SECRET", "GDRIVE_OAUTH_REFRESH_TOKEN")
    values = [os.environ.get(x, "").strip() for x in names]
    if not all(values):
        return None
    body = urllib.parse.urlencode({
        "client_id": values[0], "client_secret": values[1],
        "refresh_token": values[2], "grant_type": "refresh_token"
    }).encode("utf-8")
    request = urllib.request.Request("https://oauth2.googleapis.com/token",
                                     data=body, method="POST",
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            info = json.load(response)
    except (OSError, urllib.error.HTTPError, ValueError) as exc:
        raise ImportErrorSafe("drive_oauth_token_refresh_rejected") from exc
    token = info.get("access_token")
    if not isinstance(token, str) or len(token) < 20:
        raise ImportErrorSafe("drive_oauth_token_unavailable")
    return token


def stream_mp4(request, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(NoAuthRedirect())
    try:
        with opener.open(request, timeout=120) as response:
            if response.status != 200:
                raise ImportErrorSafe("drive_download_not_http_200")
            mimetype = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if mimetype not in ("video/mp4", "application/octet-stream", "binary/octet-stream"):
                raise ImportErrorSafe("drive_sent_preview_instead_of_mp4")
            digest = hashlib.sha256()
            length = 0
            with output.open("wb") as dest:
                while True:
                    part = response.read(1024 * 1024)
                    if not part:
                        break
                    length += len(part)
                    if length > EXPECTED_BYTES:
                        raise ImportErrorSafe("drive_file_larger_than_original")
                    digest.update(part)
                    dest.write(part)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise ImportErrorSafe("drive_download_unavailable") from exc
    if length != EXPECTED_BYTES:
        raise ImportErrorSafe("drive_file_byte_count_mismatch")
    if digest.hexdigest() != EXPECTED_SHA256:
        raise ImportErrorSafe("drive_mp4_sha256_mismatch")
    with output.open("rb") as f:
        header = f.read(16)
    if len(header) < 12 or header[4:8] != b"ftyp":
        raise ImportErrorSafe("drive_file_not_mp4")
    return {"bytes": length, "sha256": digest.hexdigest()}


def validate_media(path: Path):
    try:
        check = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                                "-show_format", "-of", "json", str(path)],
                               capture_output=True, text=True, timeout=30, check=True)
        details = json.loads(check.stdout)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise ImportErrorSafe("ffprobe_validation_failed") from exc
    streams = details.get("streams") or []
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    secs = float(details.get("format", {}).get("duration") or 0)
    if not v or not a or int(v.get("width") or 0) != 1080 or int(v.get("height") or 0) != 1920:
        raise ImportErrorSafe("unexpected_video_or_missing_audio")
    if not 44 <= secs <= 49:
        raise ImportErrorSafe("unexpected_duration")
    return {"width": 1080, "height": 1920, "duration": round(secs, 2), "has_audio": True}


def main():
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    token_present = all(os.environ.get(k) for k in (
        "GDRIVE_OAUTH_CLIENT_ID", "GDRIVE_OAUTH_CLIENT_SECRET", "GDRIVE_OAUTH_REFRESH_TOKEN"))
    print("GDRIVE_OAUTH_SECRETS_COMPLETE=" + str(token_present).lower(), flush=True)
    try:
        try:
            print("TEST_GDRIVE_ANONYMOUS_MEDIA", flush=True)
            qc = stream_mp4(urllib.request.Request(PUBLIC_URL,
                            headers={"User-Agent": "TUE/1.0"}, method="GET"), OUTPUT)
            mode = "anonymous_public_drive"
        except ImportErrorSafe as exc:
            OUTPUT.unlink(missing_ok=True)
            print("ANONYMOUS_DRIVE_RESULT=" + str(exc), flush=True)
            token = get_oauth_token()
            if token is None:
                raise ImportErrorSafe("drive_private_oauth_secrets_missing")
            print("TEST_GDRIVE_OAUTH_API", flush=True)
            qc = stream_mp4(urllib.request.Request(API_URL, headers={
                "Authorization": "Bearer " + token,
                "Accept": "application/octet-stream"
            }, method="GET"), OUTPUT)
            mode = "owner_drive_oauth"
        extra = validate_media(OUTPUT)
        summary("verified", access_mode=mode, filename=OUTPUT.name, **qc, **extra)
        return 0
    except ImportErrorSafe as exc:
        OUTPUT.unlink(missing_ok=True)
        summary("blocked", blocker=str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())

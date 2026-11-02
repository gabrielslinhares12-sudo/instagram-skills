#!/usr/bin/env python3
"""Upload a QC-passed MP4 to the owner's private Google Drive folder.

One-time OAuth application credentials must be configured as GitHub Secrets.
Missing credentials never turn a failed download into a fake Drive receipt.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import sys

from instagram_download_approved_tue_short import verify_mp4

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output/youtube-reel-import"
FOLDER = "1R4t22XHMEIfbZJjvttOWekXMyfJuKDAK"
GOOGLE_SCOPE = "https://www.googleapis.com/auth/drive"
CHANNEL_ID = "UCeVMYZs1z9HecuK0cPKnHgQ"


def upload():
    reports = list(OUTPUT.glob("multi-client-report.json")) + list(
        OUTPUT.glob("invidious-report.json"))
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in reports]
    success = [d for d in docs if d.get("status") in
               ("downloaded_for_review", "downloaded_pending_editorial_qc")]
    if not success:
        print("DRIVE_UPLOAD_SKIPPED=no_successful_video_download")
        return 0
    doc = success[0]
    vid = doc.get("id") or doc.get("video_id")
    if not isinstance(vid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
        raise RuntimeError("Video ID is invalid")
    file = OUTPUT / (vid + ".mp4")
    if not file.exists():
        raise RuntimeError("MP4 is absent")
    qc = verify_mp4(file)
    if doc.get("file", {}).get("sha256") != qc["sha256"]:
        raise RuntimeError("MP4 hash differs from QC report")
    client_id = os.environ.get("GDRIVE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GDRIVE_OAUTH_CLIENT_SECRET")
    refresh_token = os.environ.get("GDRIVE_OAUTH_REFRESH_TOKEN")
    if not all((client_id, client_secret, refresh_token)):
        print("DRIVE_UPLOAD_SKIPPED=one_time_drive_oauth_setup_required")
        return 0
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = Credentials(token=None, refresh_token=refresh_token,
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=client_id, client_secret=client_secret,
                        scopes=[GOOGLE_SCOPE])
    creds.refresh(Request())
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    name = "TUE-YouTube-" + vid + ".mp4"
    safe_name = name.replace("'", "\\'")
    q = "name = '" + safe_name + "' and '" + FOLDER + "' in parents and trashed = false"
    listed = service.files().list(q=q, fields="files(id,name,size,md5Checksum,webViewLink,description)",
                                  page_size=20).execute()
    checksum = qc["sha256"]
    for existing in listed.get("files", []):
        if "SHA256=" + checksum in (existing.get("description") or ""):
            receipt = {"id": existing["id"], "name": name, "sha256": checksum,
                       "url": existing.get("webViewLink"), "already_exists": True}
            (OUTPUT / "drive-upload-receipt.json").write_text(
                json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
            print("DRIVE_MP4_ALREADY_EXISTS=" + existing["id"])
            return 0
        raise RuntimeError("Drive has same-named file with differing checksum; review before upload")
    metadata = {
        "name": name, "parents": [FOLDER], "mimeType": "video/mp4",
        "description": "Canal TUE " + CHANNEL_ID + ". SHA256=" + checksum +
                       ". Importado para revisao, nao publicado no Instagram."
    }
    media = MediaFileUpload(str(file), mimetype="video/mp4", chunksize=5*1024*1024,
                            resumable=True)
    req = service.files().create(body=metadata, media_body=media,
                                 fields="id,name,size,webViewLink,md5Checksum,parents")
    response = None
    while response is None:
        _, response = req.next_chunk(num_retries=2)
    if FOLDER not in response.get("parents", []):
        raise RuntimeError("Google Drive receipt not in target folder")
    if int(response.get("size", -1)) != file.stat().st_size:
        raise RuntimeError("Google Drive file size verification failed")
    receipt = {"id": response["id"], "name": response["name"],
               "sha256": checksum, "size": response.get("size"),
               "url": response.get("webViewLink")}
    (OUTPUT / "drive-upload-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DRIVE_MP4_UPLOADED=" + response["id"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(upload())
    except Exception as exc:
        print("DRIVE_UPLOAD_FAILED=" + type(exc).__name__)
        sys.exit(1)

#!/usr/bin/env python3
"""Download user's original Odisseia V9 WAV to GitHub Actions, READ-ONLY.

Does not generate TTS, does not alter Drive sharing or publish a video.
Requires Google OAuth secrets configured in the repo and authorized to this Drive file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import wave

DRIVE_ID = "1ei0GDUAAPNdkQtDuYSiumq4R4d4-U58k"
SHA256 = "9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667"
EXPECTED_BYTES = 10586924
EXPECTED_SECONDS = 220.56

def credentials_present() -> bool:
    return all(os.environ.get(k, "").strip() for k in
        ("GDRIVE_OAUTH_CLIENT_ID", "GDRIVE_OAUTH_CLIENT_SECRET", "GDRIVE_OAUTH_REFRESH_TOKEN"))

def download(out: Path) -> None:
    if not credentials_present():
        raise RuntimeError("GDRIVE_OAUTH_SECRETS_MISSING: no file was downloaded")
    args = urllib.parse.urlencode({
        "client_id": os.environ["GDRIVE_OAUTH_CLIENT_ID"],
        "client_secret": os.environ["GDRIVE_OAUTH_CLIENT_SECRET"],
        "refresh_token": os.environ["GDRIVE_OAUTH_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    token_req = urllib.request.Request("https://oauth2.googleapis.com/token",
        data=args, method="POST", headers={"Content-Type":"application/x-www-form-urlencoded"})
    with urllib.request.urlopen(token_req, timeout=30) as response:
        token = json.load(response)["access_token"]
    url = f"https://www.googleapis.com/drive/v3/files/{DRIVE_ID}?alt=media"
    get = urllib.request.Request(url, headers={"Authorization":"Bearer " + token})
    with urllib.request.urlopen(get, timeout=120) as response:
        content = response.read(EXPECTED_BYTES+1)
    # Fail if anything differs from the original user-supplied WAV.
    if len(content) != EXPECTED_BYTES or hashlib.sha256(content).hexdigest() != SHA256:
        raise RuntimeError("VOICE_SOURCE_SIZE_OR_SHA_MISMATCH")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("xb") as f:
        f.write(content)
    try:
        with wave.open(str(out), "rb") as w:
            seconds = w.getnframes()/w.getframerate()
            assert w.getnchannels() == 1
            assert w.getframerate() == 24000
            assert w.getsampwidth() == 2
            assert abs(seconds - EXPECTED_SECONDS) < .01
    except Exception:
        out.unlink(missing_ok=True)
        raise
    report = out.with_suffix(".qc.json")
    report.write_text(json.dumps({
        "origin":"Original user audio / Google Drive private file",
        "source_id":DRIVE_ID,"sha256":SHA256,
        "duration_seconds":seconds,"sample_rate":24000,
        "name":out.name,"voice":"Rasalgethi — declaration from user",
        "published":False,"remixed":False,"generated_api_calls":0
    },indent=2),encoding="utf-8")
    print("ODISSEIA_ORIGINAL_WAV_VERIFIED_SHA256", SHA256)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--out",type=Path,
      default=Path("odyssey_185/out/voice/ODISSEIA_V9_RASALGETHI_220s.wav"))
    a=p.parse_args()
    if a.check:
        print("ODISSEIA_DRIVE_AUDIO_PRECHECK", "secrets_available=" + str(credentials_present()).lower())
        print("NO_TTS_OR_UPLOAD_OR_PUBLISH")
    else:
        download(a.out)

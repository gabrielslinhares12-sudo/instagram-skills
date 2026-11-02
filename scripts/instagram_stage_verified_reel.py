#!/usr/bin/env python3
"""Stage only the verified Drive-fetched MP4 on a public, isolated media branch.

Never publishes a Reel. Original SHA-256 must be exact. A previous branch is
never overwritten; remote bytes are reverified before any Meta publishing.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import Request, urlopen

FILE = Path("output/instagram-drive-reel/H9WGKaO5XQ4.mp4")
EXPECTED_BYTES = 41994355
EXPECTED_SHA = "ae4892d2c9c3b7215bb621d1c4d79e5a2669938428c97345effbf6a113d96fba"
BRANCH = "instagram-reel-media-2026-11-02"
FILE_AT_REPO = "instagram-reel-media/H9WGKaO5XQ4.mp4"
MEDIA_URL = (
    "https://raw.githubusercontent.com/gabrielslinhares12-sudo/"
    "instagram-skills/" + BRANCH + "/" + FILE_AT_REPO
)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          timeout=95, check=True).stdout.strip()


def sha256(file):
    digest = hashlib.sha256()
    with open(file, "rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def assert_original():
    if not FILE.is_file() or FILE.stat().st_size != EXPECTED_BYTES:
        raise RuntimeError("staging_mp4_missing_or_wrong_size")
    if sha256(FILE) != EXPECTED_SHA:
        raise RuntimeError("staging_mp4_digest_mismatch")
    with FILE.open("rb") as stream:
        if stream.read(12)[4:8] != b"ftyp":
            raise RuntimeError("staging_invalid_mp4_header")


def verify_public_media():
    for attempt in range(4):
        try:
            with urlopen(Request(MEDIA_URL, headers={
                "User-Agent": "TUE-Reel-Source-Verification/1.0"
            }), timeout=40) as resp:
                if resp.status != 200:
                    raise RuntimeError("public_media_not_200")
                digest = hashlib.sha256()
                bytes_read = 0
                while chunk := resp.read(1024 * 1024):
                    bytes_read += len(chunk)
                    if bytes_read > EXPECTED_BYTES:
                        raise RuntimeError("public_media_oversize")
                    digest.update(chunk)
                if bytes_read == EXPECTED_BYTES and digest.hexdigest() == EXPECTED_SHA:
                    print("PUBLIC_MEDIA_SHA256_VERIFIED=true", flush=True)
                    return
        except (OSError, TimeoutError, RuntimeError):
            pass
        if attempt < 3:
            time.sleep(5)
    raise RuntimeError("public_mp4_not_verified_unchanged")


def main():
    assert_original()
    target = Path(FILE_AT_REPO)
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("staging_only_from_main")
    if git("branch", "--show-current") != "main":
        raise RuntimeError("git_checkout_not_main")
    remote = subprocess.run(["git", "ls-remote", "--heads", "origin", BRANCH],
                            capture_output=True, text=True, timeout=35, check=True)
    if remote.stdout.strip():
        print("PUBLIC_MEDIA_BRANCH_ALREADY_EXISTS=true", flush=True)
    else:
        git("config", "user.name", "github-actions[bot]")
        git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        try:
            git("switch", "-c", BRANCH)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(FILE.read_bytes())
            git("add", "-f", "--", FILE_AT_REPO)
            git("commit", "-m", "media(instagram): host verified dog-vision reel for Meta")
            git("push", "origin", "HEAD:refs/heads/" + BRANCH)
            print("PUBLIC_MEDIA_BRANCH_CREATED=true", flush=True)
        finally:
            git("switch", "main")
    verify_public_media()
    print("TUE_MEDIA_READY_FOR_META=true", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("TUE_MEDIA_STAGING_BLOCKED=" + type(exc).__name__, file=sys.stderr)
        sys.exit(1)

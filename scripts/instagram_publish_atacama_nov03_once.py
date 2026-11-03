#!/usr/bin/env python3
"""Publish only the exact 2026-11-03 15:00 Atacama carousel without music.

One-shot owner authorization; never changes the 11h tirinha or another post.
Uses the same Git-backed durable ledger as the regular Instagram scheduler.
At other times, or with any asset/permission/identity mismatch, fails closed.
"""
from __future__ import annotations

from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler

from facebook_poster import FacebookConfig, FacebookPoster
from instagram_queue import (
    ACCOUNT, GitLedger, QueueError, read_document, validate_manifest,
    validate_state, run_queue, plan, utc_time
)
from instagram_preflight import check as check_preflight

ID = "tue-2026-11-03-15-atacama-florido"
TARGET_DATE = "2026-11-03"
TARGET_DUE = "2026-11-03T18:00:00Z"
MEDIA_DIR = Path("content/media/instagram/2026-11-03/final")
LEDGER = Path("content/publication-state.json")
EXPECTED = [
    "08ca2c522f0768b8f3acd5307127e913eccfad0c23df5066ec5f07be6c1f2e5f",
    "b35b9e0af99f008b95a89f3f04652470a3d53717cf937c6dec589da3ecb60203",
    "e717e1338a5d4a68ef87a4b05fa0458a15d51a5f4d61f61659c0d0cc1c86fbff",
    "4df804be6371acbe6658e5f9b5592996aca73c90d8c0ca8d4cf98d1dd21a8988",
    "a3d750b169b5dea568f0271e10b449a2de1ae444e4ff6266b0df9c9977e9acc8",
]
NAMES = [f"{index + 1:02d}_03NOV_15H_ATACAMA_{index:02d}.jpg" for index in range(1, 6)]
PINNED = "007a7fefb47b303316170c972e0ffdff7d8475dc"
PREFIX = ("https://raw.githubusercontent.com/"
          "gabrielslinhares12-sudo/instagram-skills/" + PINNED +
          "/content/media/instagram/2026-11-03/final/")
MAX_MEDIA = 3 * 1024 * 1024


class Blocked(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def get_post() -> dict:
    posts = validate_manifest(read_document(Path("content/schedule.json")))
    selected = [p for p in posts if p["id"] == ID]
    if len(selected) != 1:
        raise Blocked("atacama_queue_entry_missing_or_duplicated")
    p = selected[0]
    expected_urls = [PREFIX + name for name in NAMES]
    if not (p["username"] == ACCOUNT
            and p["target_url"] == "https://www.instagram.com/temumaexplicacao/"
            and p["due_at"] == TARGET_DUE
            and p["kind"] == "carousel" and p["approved"] is True
            and p["media_sha256"] == EXPECTED
            and p["media_urls"] == expected_urls
            and p["distribution_mode"] == "api_carousel_without_native_music"
            and p.get("owner_authorized_without_music") is True
            and p.get("ai_origin") == "synthetic"
            and p.get("content_style") == "clearly_illustrated"):
        raise Blocked("atacama_media_or_music_authorization_mismatch")
    return p


def validate_assets_remote(post: dict) -> None:
    from PIL import Image
    from io import BytesIO
    opener = build_opener(NoRedirect())
    for name, url, want in zip(NAMES, post["media_urls"], EXPECTED):
        file = MEDIA_DIR / name
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != want:
            raise Blocked("atacama_local_jpeg_sha256_mismatch")
        try:
            with Image.open(file) as im:
                if im.format != "JPEG" or im.size != (1080, 1350):
                    raise Blocked("atacama_jpeg_dimensions_wrong")
            with opener.open(Request(url, headers={"User-Agent": "TUE-Instagram-Meta-Preflight/1.0"}), timeout=30) as resp:
                if resp.status != 200:
                    raise Blocked("atacama_public_url_wrong_http_status")
                data = resp.read(MAX_MEDIA + 1)
            if len(data) > MAX_MEDIA or hashlib.sha256(data).hexdigest() != want:
                raise Blocked("atacama_public_jpeg_digest_mismatch")
        except (HTTPError, URLError, TimeoutError, OSError):
            raise Blocked("atacama_public_media_fetch_failed") from None
    print("ATACAMA_FIVE_JPEG_SHA256_VERIFIED=true", flush=True)


def existing_duplicate(poster, post: dict) -> str | None:
    identity = poster.check_identity()
    if (identity.get("username") != ACCOUNT or
            identity.get("instagram_user_id") != "17841433004716815"):
        raise Blocked("wrong_instagram_identity")
    response = poster._request(
        "GET", "17841433004716815/media",
        params={"fields": "id,caption,media_type,children{id},permalink", "limit": 50},
        timeout=25,
    )
    items = response.get("data")
    if not isinstance(items, list):
        raise Blocked("instagram_media_history_unavailable")
    for item in items:
        if not isinstance(item, dict):
            continue
        caption = item.get("caption") or ""
        if item.get("media_type") == "CAROUSEL_ALBUM" and (
            caption == post["caption"] or (
                "O deserto virou um jardim?" in caption and
                "#DesertoFlorido" in caption
            )
        ):
            return str(item.get("id", "unknown"))
    return None


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)

    post = get_post()
    state = validate_state(read_document(LEDGER, missing={"version": 1, "items": {}}))
    now = datetime.now(timezone.utc)
    if ID in state["items"]:
        result = {"ok": True, "mode": "already_claimed_no_retry",
                  "status": state["items"][ID]["status"],
                  "media_id": state["items"][ID].get("media_id")}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    if not args.execute:
        result = {"ok": True, "mode": "dry_run", "post_id": ID,
                  "schedule_utc": TARGET_DUE, "music_required": False,
                  "media_count": len(post["media_urls"]),
                  "time_status": plan([post], state, now)[0]["status"],
                  "publication_attempted": False}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise Blocked("not_main")
    if now.date().isoformat() != TARGET_DATE:
        raise Blocked("outside_approved_day")
    if plan([post], state, now)[0]["status"] != "due":
        raise Blocked("outside_approved_15h_window")
    validate_assets_remote(post)
    poster = FacebookPoster(FacebookConfig.from_env())
    perm = check_preflight(poster)
    if not perm.get("ok") or perm.get("username") != ACCOUNT:
        raise Blocked("publishing_grants_not_verified")
    prior_id = existing_duplicate(poster, post)
    if prior_id is not None:
        print(json.dumps({"ok": False, "status": "duplicate_on_instagram",
                          "existing_media_id": prior_id,
                          "publication_attempted": False}))
        return 0

    result = run_queue(
        [post], state, now, execute=True, enabled=True,
        persist=GitLedger(LEDGER),
        poster_factory=lambda: poster
    )
    print(json.dumps(result, ensure_ascii=False))
    if not result.get("ok"):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Blocked, QueueError) as exc:
        print(json.dumps({"ok": False, "status": "blocked",
                          "reason": str(exc), "automatic_retry": False},
                         ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "blocked_unexpected",
                          "failure_type": type(exc).__name__,
                          "check_ledger_and_instagram_before_retry": True},
                         ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)

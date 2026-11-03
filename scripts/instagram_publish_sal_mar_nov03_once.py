#!/usr/bin/env python3
"""One-shot Instagram Reel for an explicitly requested owner-created video.

Strictly: @temumaexplicacao, OlUMyBWiZDQ, no other uploads or scheduler changes.
The Git ledger is durably claimed before any POST; an uncertain result is never
retried. A private Drive URL must not be submitted to the public Meta API.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from facebook_poster import FacebookConfig, FacebookPoster
from instagram_queue import GitLedger, validate_state
from meta_poster import MetaError

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "content/publication-state.json"
EXPECTED = "temumaexplicacao"
IG_ID = "17841433004716815"
CHANNEL_VIDEO_ID = "OlUMyBWiZDQ"
POST_ID = "tue-2026-11-03-18-reel-sal-mar-original"
TARGET = "https://www.instagram.com/" + EXPECTED + "/"
MEDIA = ("https://raw.githubusercontent.com/"
         "gabrielslinhares12-sudo/instagram-skills/"
         "instagram-reel-media-sal-mar-2026-11-03/"
         "instagram-reel-media/OlUMyBWiZDQ.mp4")
SHA256 = "20fae81be736cf10c27ef4576ef389825ca57e7cf0d3bd9bf4e3a839c43a8241"
CAPTION = (
    "🌊 O mar sempre foi salgado? De onde vem tanto sal?\n\n"
    "Uma pista está nas rochas e na água dos rios, que carregam substâncias "
    "dissolvidas ao longo do tempo. E o oceano tem mais histórias para contar.\n\n"
    "Você já tinha pensado nisso? Siga @temumaexplicacao para descobrir outras "
    "curiosidades reais.\n\n"
    "#TemUmaExplicacao #Curiosidades #Oceanos #Ciencia #Natureza"
)
FINGERPRINT = hashlib.sha256(json.dumps(
    {"post_id": POST_ID, "account": EXPECTED, "youtube_id": CHANNEL_VIDEO_ID,
     "source_sha256": SHA256, "caption": CAPTION, "media": MEDIA},
    ensure_ascii=False, sort_keys=True, separators=(",", ":")
).encode("utf-8")).hexdigest()


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold())
                   if not unicodedata.combining(c))


def read_ledger() -> dict:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    return validate_state(data)


def public_media_ready():
    if not MEDIA.startswith("https://raw.githubusercontent.com/"):
        raise RuntimeError("Media host not authorized")
    request = Request(MEDIA, headers={"Range": "bytes=0-31", "User-Agent": "TUE-Instagram-Reel/1.0"})
    try:
        with urlopen(request, timeout=25) as resp:
            content_type = resp.headers.get("Content-Type", "").lower()
            length = resp.headers.get("Content-Length")
            body = resp.read(32)
            if resp.status not in (200, 206):
                raise RuntimeError("Public MP4 returned invalid HTTP status")
            if len(body) < 12 or body[4:8] != b"ftyp":
                raise RuntimeError("Public MP4 header invalid")
            if "text/html" in content_type or "json" in content_type:
                raise RuntimeError("Public media URL is not downloadable video")
        return {"media_host_ready": True, "first_chunk_valid": True}
    except HTTPError as error:
        raise RuntimeError(f"Public media HTTP {error.code}") from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError("Public media host not reachable by anonymous reader") from error


def read_recent_media(poster):
    result = poster._request("GET", IG_ID + "/media",
                             params={"fields": "id,caption,permalink,media_type,timestamp",
                                     "limit": 50}, timeout=25)
    records = result.get("data")
    if not isinstance(records, list):
        raise RuntimeError("Could not verify recent Instagram media for duplicates")
    return records


def matching_existing(records):
    # Stop when a Reel with this subject already appears in the owner's recent feed.
    for entry in records:
        if not isinstance(entry, dict):
            continue
        text = normalize(str(entry.get("caption") or ""))
        if ("sal do mar" in text
                or ("de onde vem" in text and "tanto sal" in text)
                or ("mar sempre foi salgado" in text)):
            return entry
    return None


def claim(state, writer):
    if POST_ID in state["items"]:
        raise RuntimeError("One-shot Reel was already attempted; no retry permitted")
    state["items"][POST_ID] = {
        "status": "claimed", "fingerprint": FINGERPRINT,
        "due_at": "2026-11-03T21:00:00Z", "claimed_at": stamp(),
        "source_video_id": CHANNEL_VIDEO_ID,
        "source_sha256": SHA256,
    }
    writer(state, "ops(instagram): reservar envio unico do Reel original do sal do mar antes de falar com Meta")


def record_result(state, writer, status, **fields):
    state["items"][POST_ID].update({"status": status, **fields})
    writer(state, "ops(instagram): registrar recibo do Reel ou necessidade de revisao")


def main():
    if os.environ.get("GITHUB_REF") not in ("refs/heads/main", None):
        raise RuntimeError("Only main checkout may publish")
    now = datetime.now(timezone.utc)
    due = datetime(2026, 11, 3, 21, 0, tzinfo=timezone.utc)
    cutoff = datetime(2026, 11, 3, 23, 0, tzinfo=timezone.utc)
    if now < due or now >= cutoff:
        print(json.dumps({"ok": True, "status": "not_in_18h_publishing_window",
                          "publication_attempted": False,
                          "scheduled_at": due.isoformat()}))
        return 0
    current = read_ledger()
    if POST_ID in current["items"]:
        print(json.dumps({"ok": False, "status": "already_attempted",
                          "publication_retried": False}))
        return 0
    public_media_ready()
    from instagram_stage_sal_mar_nov03 import verify_public_media
    verify_public_media()
    poster = FacebookPoster(FacebookConfig.from_env())
    identity = poster.check_identity()
    if (identity.get("username") != EXPECTED or
            identity.get("instagram_user_id") != IG_ID):
        raise RuntimeError("Wrong Instagram account; no upload attempted")
    records = read_recent_media(poster)
    duplicate = matching_existing(records)
    if duplicate:
        print(json.dumps({"ok": False, "status": "existing_reel_possible_duplicate",
                          "existing_media_id": duplicate.get("id"),
                          "existing_permalink": duplicate.get("permalink"),
                          "publication_retried": False}, ensure_ascii=False))
        return 0

    writer = GitLedger(LEDGER)
    claim(current, writer)  # Durable remote commit BEFORE the Meta write.
    try:
        result = poster.publish("reel", TARGET, {
            "kind": "reel", "target_url": TARGET,
            "approved": True, "draft_text": CAPTION, "media_urls": [MEDIA],
            "is_ai_generated": True  # Narracao original sintetizada; declarar proveniencia real.
        })
        if not result.get("ok") or not str(result.get("media_id", "")).isdigit():
            raise RuntimeError("Meta returned no valid media receipt")
    except (MetaError, RuntimeError) as exc:
        info = exc.public() if isinstance(exc, MetaError) else {"error": "invalid_receipt"}
        record_result(current, writer, "needs_review",
                      error_kind=str(info.get("error", "unknown"))[:160],
                      http_status=info.get("http_status"),
                      creation_id=info.get("creation_id"),
                      publishing_retry_allowed=False)
        print(json.dumps({"ok": False, "status": "needs_review",
                          "reason": info.get("error", "Invalid response"),
                          "http_status": info.get("http_status"),
                          "code": info.get("code"),
                          "creation_id": info.get("creation_id"),
                          "publish_retry_allowed": False}, ensure_ascii=False))
        return 1

    # Meta media_publish ID is a real receipt. A failed permalink read does not
    # undo a confirmed publish and must never cause an upload retry.
    media_id = result["media_id"]
    receipt = None
    try:
        details = poster._request(
            "GET", media_id,
            params={"fields": "id,username,media_type,permalink,timestamp"}, timeout=25)
        if (details.get("id") == media_id
                and str(details.get("username", "")).lower() == EXPECTED
                and str(details.get("permalink", "")).startswith("https://www.instagram.com/")):
            receipt = details["permalink"]
    except MetaError:
        pass
    record_result(current, writer, "published",
                  media_id=media_id,
                  creation_id=result.get("creation_id"),
                  instagram_user_id=IG_ID,
                  page_id=identity["page_id"],
                  published_at=stamp(),
                  source_video_id=CHANNEL_VIDEO_ID,
                  source_sha256=SHA256,
                  **({"permalink": receipt} if receipt else {}))
    print(json.dumps({"ok": True, "status": "published", "media_id": media_id,
                      "permalink": receipt, "account": EXPECTED,
                      "video_id": CHANNEL_VIDEO_ID, "hashtag_count": 5},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        # Don't include remote error messages or credentials in logs.
        print(json.dumps({"ok": False, "status": "blocked_before_publish_or_ledger_failure",
                          "error_type": type(error).__name__,
                          "safe_failure_reason": str(error)[:160] if isinstance(error, RuntimeError) else "unexpected_error",
                          "publication_confirmed": False,
                          "check_ledger_before_retry": True}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(1)

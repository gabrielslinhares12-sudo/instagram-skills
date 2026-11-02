#!/usr/bin/env python3
"""Safely reconcile verified posts with pending NATIVE Instagram Story reshares.

This performs READ-ONLY Meta requests for the original post permalink. It never
publishes a Story, never creates standalone Story media, and never claims a
text overlay or native reshare without an authenticated receipt.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "content/publication-state.json"
STORIES = ROOT / "content/editorial/STORIES-VINCULADOS-2026-11-02-a-08.json"
ACCOUNT = "temumaexplicacao"
# Editorial planning ID was frozen before the urgent post was published.
# An explicit alias preserves weekly schedule integrity without fabricating
# another post or rewriting the actual, immutable publication receipt.
ALIASES = {"tue-2026-11-02-18-senha-impossivel":
           "tue-2026-11-02-15-senha-impossivel"}
CTA = "Gostou dessa? Então vai lá, curte o post e segue o Tem Uma Explicação para não perder as próximas!"


def approved_permalink(url: object) -> bool:
    if not isinstance(url, str) or len(url) > 500:
        return False
    try:
        u = urlsplit(url)
        return (u.scheme == "https" and u.hostname == "www.instagram.com"
                and u.username is None and u.password is None
                and u.query == "" and u.fragment == ""
                and u.path.startswith(("/p/", "/reel/", "/tv/"))
                and len(u.path.split("/")[2]) >= 5)
    except (ValueError, IndexError):
        return False


def reconcile(ledger: dict, stories: dict, lookup=None) -> tuple[dict, list[dict]]:
    """Only a verified permalink enables the published-parent Story state."""
    if (stories.get("native_share_required") is not True
            or stories.get("text_cta") != CTA
            or stories.get("text_cta_required") is not True
            or stories.get("no_external_link_or_link_sticker") is not True):
        raise ValueError("Native Story contract is missing.")
    result = json.loads(json.dumps(stories))
    notes = []
    for entry in result.get("entries", []):
        actual_id = ALIASES.get(entry["parent_id"], entry["parent_id"])
        claim = ledger.get("items", {}).get(actual_id, {})
        if (claim.get("status") not in {"published", "awaiting_native_music"}
                or not str(claim.get("media_id", "")).isdigit()
                or not claim.get("published_at")
                or (claim.get("instagram_user_id") and
                    claim["instagram_user_id"] != "17841433004716815")):
            continue
        entry["actual_published_parent_id"] = actual_id
        entry["parent_receipt_media_id"] = claim["media_id"]
        if entry.get("story_published") is True:
            # Never overwrite or recreate completed Stories.
            notes.append({"parent_id": actual_id, "status": "story_already_recorded"})
            continue
        permalink = claim.get("permalink")
        if not approved_permalink(permalink) and lookup is not None:
            try:
                permalink = lookup(claim["media_id"])
            except Exception:
                permalink = None  # no token, URL, or server details in logs
        if not approved_permalink(permalink):
            entry["status"] = "pending_verified_permalink_before_native_share"
            notes.append({"parent_id": actual_id, "status": entry["status"],
                          "media_id": claim["media_id"]})
            continue
        entry.update({
            "parent_published": True,
            "parent_media_id": claim["media_id"],
            "parent_permalink": permalink,
            "source_verified_by_official_receipt": True,
            "status": "awaiting_native_app_share_with_text_cta",
        })
        notes.append({"parent_id": actual_id, "status": entry["status"],
                      "media_id": claim["media_id"], "parent_permalink": permalink})
    return result, notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true", help="Update Story planning JSON; never posts Stories.")
    args = ap.parse_args()
    ledger = json.loads(STATE.read_text(encoding="utf-8"))
    story = json.loads(STORIES.read_text(encoding="utf-8"))
    lookup = None
    if args.execute and os.environ.get("FACEBOOK_USER_ACCESS_TOKEN"):
        try:
            from facebook_poster import FacebookConfig, FacebookPoster
            p = FacebookPoster(FacebookConfig.from_env())
            identity = p.check_identity()
            if identity.get("username") != ACCOUNT:
                raise ValueError("Configured Instagram identity does not match.")
            def get_permalink(media_id):
                response = p._request("GET", str(media_id),
                                      params={"fields": "id,username,permalink"})
                if (response.get("id") != str(media_id)
                        or response.get("username", "").lower() != ACCOUNT):
                    return None
                return response.get("permalink")
            lookup = get_permalink
        except Exception:
            lookup = None
    updated, notes = reconcile(ledger, story, lookup)
    if args.execute and updated != story:
        STORIES.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"ok": True, "operation": "reconcile_only",
                      "native_story_publish_attempted": False,
                      "updated": bool(args.execute and updated != story),
                      "pending": notes}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

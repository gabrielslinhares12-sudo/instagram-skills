#!/usr/bin/env python3
"""Read-only live audit: compare approved Halloween carousel with account media.

Never prints tokens, captions or full API responses. Never creates media.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
from facebook_poster import FacebookConfig, FacebookPoster
from instagram_queue import read_document, validate_manifest
from meta_poster import MetaError

MAX_PAGES = 3
MAX_MEDIA = 75
PAGE_SIZE = 25
POST_ID = "halloween-2026-10-31-historia-8-laminas"

def duplicate(item: dict, record: dict) -> bool:
    if record.get("media_type") != "CAROUSEL_ALBUM":
        return False
    if record.get("caption") != item["caption"]:
        return False
    children = record.get("children")
    return isinstance(children,dict) and isinstance(children.get("data"),list) and len(children["data"])==8

def main():
    manifest = validate_manifest(read_document(Path("content/schedule.json")))
    post = next(p for p in manifest if p["id"] == POST_ID)
    poster = FacebookPoster(FacebookConfig.from_env())
    identity=poster.check_identity()
    if identity.get("username") != "temumaexplicacao":
        raise RuntimeError("Account identity did not match")
    ig_id=identity["instagram_user_id"]
    cursor=None
    inspected=[]
    matches=[]
    for _ in range(MAX_PAGES):
        params={"fields":"id,caption,media_type,children{id},permalink",
                "limit":PAGE_SIZE}
        if cursor:
            params["after"]=cursor
        response=poster._request("GET", f"{ig_id}/media", params=params)
        batch=response.get("data")
        if not isinstance(batch,list):
            raise ValueError("Graph media response invalid")
        for media in batch:
            if not isinstance(media,dict):
                continue
            inspected.append(media)
            if duplicate(post,media):
                matches.append(media.get("id"))
        paging=response.get("paging") or {}
        cursors=paging.get("cursors") if isinstance(paging,dict) else None
        next_cursor=cursors.get("after") if isinstance(cursors,dict) else None
        if not paging.get("next") or not next_cursor or next_cursor==cursor or len(inspected)>=MAX_MEDIA:
            break
        cursor=next_cursor
    result={
        "ok":True,
        "read_only":True,
        "account_verified":True,
        "media_inspected":len(inspected),
        "exact_halloween_duplicate":bool(matches),
        "possible_match_count":len(matches),
        "publishing_attempted":False,
        "scope_limit":"last 75 published items at most; cannot prove global absence",
    }
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        # Generic errors only; never expose Meta response containing token.
        print(json.dumps({"ok":False,"read_only":True,
                          "failure_type":type(error).__name__,
                          "publishing_attempted":False}),file=sys.stderr)
        raise SystemExit(1)

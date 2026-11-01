#!/usr/bin/env python3
"""Read-only inspection of the quarantined Halloween creation ID and Instagram feed."""
import json
from difflib import SequenceMatcher
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from facebook_poster import FacebookConfig, FacebookPoster
from instagram_queue import validate_state, validate_manifest, read_document

ID = "halloween-2026-10-31-historia-8-laminas"

def main():
    ledger = validate_state(read_document(Path("content/publication-state.json")))
    entry = ledger["items"].get(ID)
    if not entry or entry.get("status") not in ("needs_review", "awaiting_native_music", "published"):
        raise SystemExit("Expected quarantined or published entry not found")
    creation = entry.get("creation_id")
    if not creation or not str(creation).isdigit():
        raise SystemExit("Missing valid Meta creation ID; stop")
    manifest = validate_manifest(read_document(Path("content/schedule.json")))
    post = next(p for p in manifest if p["id"] == ID)
    client = FacebookPoster(FacebookConfig.from_env())
    identity = client.check_identity()
    if identity.get("username") != "temumaexplicacao":
        raise SystemExit("Account mismatch")
    result = client._request("GET", creation, params={"fields":"id,status_code"})
    status = result.get("status_code")
    if status not in ("ERROR","EXPIRED","FINISHED","PUBLISHED","IN_PROGRESS"):
        status = "UNKNOWN"
    recent = client._request("GET", identity["instagram_user_id"] + "/media",
                             params={"fields":"id,caption,media_type,permalink,timestamp","limit":100})
    rows = recent.get("data")
    if not isinstance(rows, list):
        raise SystemExit("Media list unavailable")
    same = [m for m in rows
            if m.get("caption") == post["caption"] and m.get("media_type") == "CAROUSEL_ALBUM"]
    print(json.dumps({
        "check":"read_only", "account":"temumaexplicacao",
        "creation_id":creation, "creation_status":status,
        "same_carousel_found":bool(same), "matches":len(same),
        "matching_media_ids":[x["id"] for x in same if isinstance(x.get("id"),str)],
        "matching_permalinks":[x["permalink"] for x in same if isinstance(x.get("permalink"),str)],
        "recent_media": [
            {
              "id":m.get("id"),
              "type":m.get("media_type"),
              "permalink":m.get("permalink"),
              "timestamp":m.get("timestamp"),
              "caption_similarity":round(SequenceMatcher(
                  None,str(m.get("caption") or ""),post["caption"]).ratio(),3),
              "caption_prefix":str(m.get("caption") or "")[:70],
            }
            for m in rows[:20] if isinstance(m,dict)
        ],
        "current_ledger_status":entry["status"], "mutation":False,
    },ensure_ascii=False))
if __name__=="__main__":
    main()

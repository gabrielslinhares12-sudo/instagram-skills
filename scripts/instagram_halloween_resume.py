#!/usr/bin/env python3
"""One authorized finalization attempt of the existing FINISHED Halloween container.

Never creates new image/carousel containers. Fail-closed preflight checks and
durable Git claim precede the sole media_publish request.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from instagram_queue import (GitLedger, QueueError, read_document,
                             validate_manifest, validate_state, fingerprint, timestamp)
from facebook_poster import FacebookPoster, FacebookConfig
from meta_poster import MetaError, NUMERIC_ID

ID="halloween-2026-10-31-historia-8-laminas"

def main():
    posts=validate_manifest(read_document(Path("content/schedule.json")))
    post=next(p for p in posts if p["id"]==ID)
    state=validate_state(read_document(Path("content/publication-state.json")))
    entry=state["items"].get(ID)
    if (post.get("kind")!="carousel" or post.get("approved") is not True
        or post.get("distribution_mode")!="api_carousel_then_native_music"
        or post.get("owner_authorized_two_step_music") is not True
        or not isinstance(entry,dict)
        or entry.get("status")!="needs_review"
        or entry.get("fingerprint")!=fingerprint(post)
        or entry.get("resume_attempted_at")
        or entry.get("creation_id")!="18102064946100158"):
        raise QueueError("The one-time Halloween recovery is not eligible; stop.")
    client=FacebookPoster(FacebookConfig.from_env())
    identity=client.check_identity()
    if identity.get("username")!="temumaexplicacao":
        raise QueueError("Instagram identity mismatch.")
    creation=entry["creation_id"]
    status=client._request("GET", creation, params={"fields":"id,status_code"}).get("status_code")
    if status!="FINISHED":
        raise QueueError("Media container is not FINISHED. Do not retry.")
    feed=client._request("GET",identity["instagram_user_id"]+"/media",
                        params={"fields":"id,caption,media_type","limit":100})
    items=feed.get("data")
    if not isinstance(items,list):
        raise QueueError("Could not check Instagram feed.")
    if any(x.get("caption")==post["caption"] and x.get("media_type")=="CAROUSEL_ALBUM"
           for x in items):
        raise QueueError("An identical carousel is already published; stop.")
    persist=GitLedger(Path("content/publication-state.json"))
    entry["status"]="claimed"
    entry["resume_attempted_at"]=timestamp(datetime.now(timezone.utc))
    entry["resume_container_id"]=creation
    persist(state, "Claim single final publish of existing Halloween Meta container")
    try:
        response=client._request("POST",identity["instagram_user_id"]+"/media_publish",
                                 data={"creation_id":creation})
        media_id=str(response.get("id",""))
        if not NUMERIC_ID.fullmatch(media_id):
            raise QueueError("Meta did not confirm a media ID.")
        media=client._request("GET",media_id,params={"fields":"id,caption,media_type,permalink"})
        if (media.get("id")!=media_id
            or media.get("media_type")!="CAROUSEL_ALBUM"
            or media.get("caption")!=post["caption"]):
            raise QueueError("Live carousel verification failed.")
        entry.update(status="awaiting_native_music", media_id=media_id,
                     published_at=timestamp(datetime.now(timezone.utc)),
                     music_status="pending_add_in_instagram_app",
                     permalink=media.get("permalink") if isinstance(media.get("permalink"),str) else None)
        persist(state,"Record Halloween photo carousel published; native music pending")
        print(json.dumps({"ok":True,"status":"awaiting_native_music",
                          "media_id":media_id,"permalink":entry.get("permalink"),
                          "post_kind":"carousel","music_added":False},ensure_ascii=False))
    except Exception:
        entry.update(status="needs_review",error_type="resume_outcome_uncertain")
        persist(state,"Quarantine uncertain Halloween container finalization")
        raise QueueError("Publishing or verification was not confirmed. Do not retry this container.") from None

if __name__=="__main__":
    try: main()
    except (QueueError,MetaError) as error:
        print(json.dumps({"ok":False,"error":str(error)},ensure_ascii=False),file=sys.stderr)
        sys.exit(1)

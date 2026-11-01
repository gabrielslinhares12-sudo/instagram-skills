#!/usr/bin/env python3
"""One-shot owner-authorized Halloween recovery, with a different media host.

Uses original approved JPEG bytes (SHA256 checked), but CDN URL for delivery.
Every Meta write is guarded by a durable Git claim. Never automatically retry
an ambiguous publish response, and never claim music was added by Graph API.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from facebook_poster import FacebookPoster, FacebookConfig
from instagram_queue import (GitLedger, QueueError, read_document, validate_manifest,
                             validate_state, fingerprint, timestamp)
from instagram_halloween_cdn_preflight import verify as verify_cdn, BASE
from meta_poster import MetaError, NUMERIC_ID

ID="halloween-2026-10-31-historia-8-laminas"
OLD_CONTAINER="18102064946100158"

def ensure_no_duplicate(client, identity, caption):
    feed=client._request("GET", identity["instagram_user_id"]+"/media",
                         params={"fields":"id,caption,media_type,permalink","limit":100})
    items=feed.get("data")
    if not isinstance(items,list):
        raise QueueError("Instagram feed read failed; no publication.")
    found=[p for p in items if isinstance(p,dict)
           and p.get("media_type")=="CAROUSEL_ALBUM"
           and (str(p.get("caption") or "")==caption
                or str(p.get("caption") or "").startswith(caption[:100]))]
    if found:
        raise QueueError("An identical carousel already exists; do not duplicate.")
    return len(items)

def run():
    posts=validate_manifest(read_document(Path("content/schedule.json")))
    post=next(x for x in posts if x["id"]==ID)
    state=validate_state(read_document(Path("content/publication-state.json")))
    original=state["items"].get(ID)
    if (post.get("approved") is not True or post.get("kind")!="carousel"
        or len(post["media_urls"])!=8
        or post.get("distribution_mode")!="api_carousel_then_native_music"
        or post.get("owner_authorized_two_step_music") is not True
        or not isinstance(original,dict)
        or original.get("status")!="needs_review"
        or original.get("fingerprint")!=fingerprint(post)
        or original.get("creation_id")!=OLD_CONTAINER
        or not original.get("resume_attempted_at")
        or original.get("cdn_recovery_claimed_at")):
        raise QueueError("Halloween recovery is not eligible or already attempted.")
    assets=verify_cdn()
    if assets.get("bytes_verified")!=8:
        raise QueueError("Alternative CDN image bytes could not be verified.")
    client=FacebookPoster(FacebookConfig.from_env())
    identity=client.check_identity()
    if identity.get("username")!="temumaexplicacao":
        raise QueueError("Wrong Instagram destination.")
    count=ensure_no_duplicate(client,identity,post["caption"])
    print(json.dumps({"preflight":"passed","original_jpegs_verified":8,
                      "recent_account_posts_checked":count,
                      "duplicate_found":False}),flush=True)
    persist=GitLedger(Path("content/publication-state.json"))
    original["cdn_recovery_claimed_at"]=timestamp(datetime.now(timezone.utc))
    original["status"]="claimed"
    original["cdn_origin"]="pinned_jsdelivr"
    original["cdn_attempt_max"]=1
    persist(state,"Claim ONE alternate-CDN Instagram Halloween recovery before any Meta write")
    created_children=[]
    parent=None
    last_stage="create_carousel_children"
    try:
        for i in range(1,9):
            image_url=BASE+f"{i:02d}-historia-halloween.jpg"
            child=client._create_container({"image_url":image_url,
                                            "is_carousel_item":"true"})
            if not isinstance(child,str) or not NUMERIC_ID.fullmatch(child):
                raise QueueError("Instagram did not confirm a child container.")
            created_children.append(child)
            print(json.dumps({"step":"child_ready","page":i,"total_pages":8}),flush=True)
        last_stage="create_carousel"
        opts={"media_type":"CAROUSEL","children":",".join(created_children),
              "caption":post["caption"],"is_ai_generated":"true"}
        parent=client._create_container(opts)
        original["cdn_carousel_creation_id"]=parent
        original["cdn_child_container_count"]=8
        persist(state,"Record exact new Halloween album container, before final publish")
        last_stage="finalize_carousel"
        response=client._request("POST",identity["instagram_user_id"]+"/media_publish",
                                 data={"creation_id":parent})
        media_id=str(response.get("id",""))
        if not NUMERIC_ID.fullmatch(media_id):
            raise QueueError("Instagram did not return the published media ID.")
        original["cdn_published_media_id"]=media_id
        persist(state,"Record Meta media ID before verifying published Halloween carousel")
        last_stage="verify_post"
        published=client._request("GET",media_id,params={"fields":"id,caption,media_type,permalink"})
        if (published.get("id")!=media_id
            or published.get("media_type")!="CAROUSEL_ALBUM"
            or str(published.get("caption") or "")!=post["caption"]):
            raise QueueError("Instagram post metadata does not confirm the approved carousel.")
        original.update(status="awaiting_native_music",media_id=media_id,
                        published_at=timestamp(datetime.now(timezone.utc)),
                        music_status="pending_instagram_app",
                        permalink=published.get("permalink"))
        persist(state,"Confirm Halloween original photo carousel, native music pending")
        print(json.dumps({"ok":True,"status":"awaiting_native_music",
                          "media_id":media_id, "permalink":published.get("permalink"),
                          "music_added":False},ensure_ascii=False),flush=True)
        return
    except Exception as exc:
        # Never retry uncertain POST. Store container IDs to enable read-only reconciliation.
        original.update(status="needs_review",error_type="cdn_recovery_not_confirmed",
                        cdn_failure_stage=last_stage,cdn_created_children=created_children,
                        cdn_parent_container=parent)
        if isinstance(exc,MetaError):
            for field in ("http_status","code","subcode"):
                number=getattr(exc,field,None)
                if type(number) is int:original["cdn_"+field]=number
        persist(state,"Quarantine one-shot alternate-CDN Halloween publication")
        raise QueueError("Alternate CDN Instagram publish not confirmed: "+last_stage+
                         ". No automatic second attempt.") from None

if __name__=="__main__":
    try:run()
    except (QueueError,MetaError) as error:
        print(json.dumps({"ok":False,"error":str(error)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(1)

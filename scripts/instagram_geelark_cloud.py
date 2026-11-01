#!/usr/bin/env python3
"""Schedule approved photo+native-music carousels via GeeLark's cloud Android RPA.

Uses GeeLark's DOCUMENTED instagramPubReelsImages endpoint with publishPost=true
and sameStyleUrl for music. No PC, no private Instagram API, no login retry.
The API returns a TASK ID, never proof of a successful Instagram post.

Modes:
  check      - local validation, no vendor requests or git writes
  submit     - requires explicit account/cost/music approval and one-shot Git ledger
  reconcile  - read task status, NEVER retry an ambiguous vendor action

Important: use the vendor's official documentation. A template update, unavailable
track or account restriction may break publication; verify Instagram separately.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

from instagram_queue import validate_manifest, validate_state, fingerprint, read_document

OWNER = "gabrielslinhares12-sudo/instagram-skills"
ACCOUNT = "temumaexplicacao"
API_ROOT = "https://openapi.geelark.com"
LEDGER = Path("content/geelark-task-state.json")
MANIFEST = Path("content/schedule.json")
PUB_STATE = Path("content/publication-state.json")
TASK_CREATE = "/open/v1/rpa/task/instagramPubReelsImages"
TASK_QUERY = "/open/v1/task/query"
TEMP_UPLOAD = "/open/v1/upload/getUrl"
NUMERIC_ID = re.compile(r"[0-9]{3,35}\Z")
POST_SLUG = re.compile(r"[a-z0-9-]{4,140}\Z")
SHORTCODE = re.compile(r"[A-Za-z0-9_-]{5,60}\Z")
FIELDS = frozenset({"version", "items"})
ITEM_STATES = frozenset({"claimed", "scheduled", "vendor_completed_unverified", "needs_review"})
MAX_JPEG = 8 * 1024 * 1024

class Blocked(RuntimeError):
    """Fail closed, without sensitive data."""

def iso_time(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise Blocked("Scheduled time must be UTC ISO, YYYY-MM-DDTHH:MM:SSZ.")
    try:
        when = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Blocked("Invalid UTC scheduled time.") from exc
    if when.utcoffset() != timedelta(0):
        raise Blocked("Only UTC scheduled time is allowed.")
    return when

def source_url(url: str) -> str:
    """GeeLark 'sameStyleUrl' must reference approved Instagram audio."""
    if not isinstance(url, str):
        raise Blocked("Instagram audio-source URL is missing.")
    value = url.strip()
    try:
        p = urlsplit(value)
        parts = p.path.strip("/").split("/")
        ok = (p.scheme == "https" and p.hostname in ("instagram.com", "www.instagram.com")
              and p.username is None and p.password is None and not p.query and not p.fragment
              and len(parts) == 2 and parts[0] in ("reel", "p")
              and SHORTCODE.fullmatch(parts[1]) is not None)
    except ValueError:
        ok = False
    if not ok:
        raise Blocked("Use a canonical public Instagram Reel/Post URL with approved native audio.")
    return "https://www.instagram.com/" + "/".join(parts) + "/"

def load_post(post_id: str) -> dict:
    if not POST_SLUG.fullmatch(post_id):
        raise Blocked("Invalid post identifier.")
    data = validate_manifest(read_document(MANIFEST))
    matches = [p for p in data if p["id"] == post_id]
    if len(matches) != 1:
        raise Blocked("No unique queue item with that post ID.")
    post = matches[0]
    if post.get("kind") != "carousel" or post.get("approved") is not True:
        raise Blocked("Only already-approved photo carousels can be scheduled.")
    if post.get("distribution_mode", "native_music_carousel") != "native_music_carousel":
        raise Blocked("This content is not approved as a native-music carousel.")
    if post.get("username") != ACCOUNT or len(post.get("media_urls", [])) != 8:
        raise Blocked("Unexpected account or photo count. Require 8 approved images.")
    if len(post.get("media_sha256", [])) != 8:
        raise Blocked("Missing original photo hashes.")
    return post

def validate_state_doc(document: Any) -> dict:
    if not isinstance(document, dict) or document.get("version") != 1 or set(document) != FIELDS:
        raise Blocked("Invalid GeeLark task ledger.")
    items = document.get("items")
    if not isinstance(items, dict):
        raise Blocked("Invalid GeeLark task ledger items.")
    for k, v in items.items():
        if not isinstance(k, str) or not POST_SLUG.fullmatch(k) or not isinstance(v, dict):
            raise Blocked("Invalid task ledger item.")
        if v.get("status") not in ITEM_STATES:
            raise Blocked("Unknown task ledger status.")
    return document

def git_save(state: dict, message: str) -> None:
    """Write/push atomic claim BEFORE any non-idempotent vendor mutation."""
    validate_state_doc(state)
    if not LEDGER.is_file() or LEDGER.is_symlink():
        raise Blocked("Task ledger must already be tracked in the repository.")
    def git(*args: str) -> str:
        try:
            p = subprocess.run(["git", *args], check=True, text=True,
                               capture_output=True, timeout=60)
            return p.stdout
        except Exception as exc:
            raise Blocked("Could not durably commit the task claim; stopped before vendor upload.") from exc
    if git("status", "--porcelain", "--untracked-files=no").strip():
        raise Blocked("Git checkout has unstaged changes. Refusing task claim.")
    original = LEDGER.read_text("utf-8")
    try:
        with tempfile.NamedTemporaryFile("w", dir=LEDGER.parent, delete=False, encoding="utf-8") as fh:
            json.dump(state, fh, sort_keys=True, indent=2, ensure_ascii=False)
            fh.write("\n")
            tempname = fh.name
        os.replace(tempname, LEDGER)
        git("add", "--", str(LEDGER))
        git("commit", "-m", message, "--", str(LEDGER))
        git("push", "origin", "HEAD:main")
    except Exception:
        # Do NOT roll back after a possibly successful push. Require human reconciliation.
        raise

def verify_files(post: dict, directory: Path) -> list[Path]:
    from PIL import Image
    import io
    downloaded = []
    for i, (url, checksum) in enumerate(zip(post["media_urls"], post["media_sha256"]), 1):
        p = urlsplit(url)
        if (p.scheme != "https" or p.hostname != "raw.githubusercontent.com"
                or not p.path.startswith("/" + OWNER + "/") or not p.path.endswith(".jpg")
                or p.query or p.fragment):
            raise Blocked("Non-approved media source.")
        try:
            with urlopen(Request(url, headers={"User-Agent":"TUE-GeeLark-Cloud/1"}), timeout=30) as response:
                raw=response.read(MAX_JPEG+1)
        except Exception as exc:
            raise Blocked("Could not fetch one of the approved images.") from exc
        if len(raw)>MAX_JPEG or hashlib.sha256(raw).hexdigest()!=checksum:
            raise Blocked("One approved image is missing or altered.")
        try:
            with Image.open(io.BytesIO(raw)) as img:
                if img.format!="JPEG" or img.size!=(1080,1350):
                    raise Blocked("Photo is not original 1080x1350 JPEG.")
        except OSError as exc:
            raise Blocked("Invalid JPEG payload.") from exc
        dest=directory/f"{i:02d}.jpg"
        dest.write_bytes(raw)
        downloaded.append(dest)
    return downloaded

class GeeLark:
    def __init__(self, token: str) -> None:
        if not token or any(c.isspace() for c in token):
            raise Blocked("GeeLark API token missing or malformed.")
        self.__token=token

    def post(self, endpoint: str, body: dict) -> dict:
        if endpoint not in (TASK_CREATE, TASK_QUERY, TEMP_UPLOAD):
            raise Blocked("Vendor endpoint is not allowlisted.")
        payload=json.dumps(body).encode("utf-8")
        req=Request(API_ROOT+endpoint, data=payload, headers={
            "Authorization": "Bearer " + self.__token,
            "Content-Type": "application/json",
            "traceId": str(uuid4()).upper(),
            "User-Agent": "TUE-GeeLark-Cloud/1",
        }, method="POST")
        try:
            with urlopen(req, timeout=30) as response:
                raw=response.read(250000)
        except (HTTPError, URLError, OSError) as exc:
            # Even a timeout can represent successful vendor task creation.
            raise Blocked("Vendor request failed or timed out; inspect ledger before retry.") from exc
        try:
            data=json.loads(raw)
        except ValueError as exc:
            raise Blocked("Vendor response was not valid JSON.") from exc
        if not isinstance(data, dict) or data.get("code") != 0 or not isinstance(data.get("data"), dict):
            raise Blocked("GeeLark did not acknowledge the task or upload request.")
        return data["data"]

    def upload_jpg(self, path: Path) -> str:
        cfg=self.post(TEMP_UPLOAD, {"fileType":"jpg"})
        target=cfg.get("uploadUrl")
        resource=cfg.get("resourceUrl")
        if not isinstance(target,str) or not isinstance(resource,str):
            raise Blocked("Vendor temporary upload URLs missing.")
        up=urlsplit(target)
        res=urlsplit(resource)
        if (up.scheme != "https" or not up.hostname or
            res.scheme != "https" or res.hostname not in
            {"material.geelark.com", "material-prod.geelark.cn", "material.geelark.cn"}):
            raise Blocked("Upload URL did not meet TLS or GeeLark host validation.")
        # Never log the signed target URL or its query parameters.
        req=Request(target,data=path.read_bytes(),headers={"Content-Type":"image/jpeg"},
                    method="PUT")
        try:
            with urlopen(req,timeout=35) as resp:
                if resp.status not in (200,201,204):
                    raise Blocked("Vendor media storage rejected image bytes.")
        except (HTTPError, URLError, OSError) as exc:
            raise Blocked("Could not upload approved JPEG to vendor storage.") from exc
        return resource

    def submit(self, *, phone_id: str, images: list[str],
               caption: str, when: datetime, music: str, post_id: str) -> str:
        if not NUMERIC_ID.fullmatch(phone_id) or len(images)!=8:
            raise Blocked("Invalid cloud phone identifier or photo count.")
        result=self.post(TASK_CREATE,{
            "name": "Instagram TUE - " + post_id[:100],
            "remark": "Approved 8-photo carousel with Instagram native music",
            "scheduleAt": int(when.timestamp()),
            "id": phone_id,
            "description": caption,
            "image": images,
            "sameStyleUrl": music,
            "aiTag": False,
            "publishPost": True,
            "needShareLink": True,
        })
        task=result.get("taskId")
        if not isinstance(task,str) or not NUMERIC_ID.fullmatch(task):
            raise Blocked("Vendor did not return a valid task ID.")
        return task

    def task_status(self, task_id: str) -> dict:
        if not isinstance(task_id,str) or not NUMERIC_ID.fullmatch(task_id):
            raise Blocked("Invalid vendor task ID.")
        result=self.post(TASK_QUERY,{"ids":[task_id]})
        items=result.get("items",[])
        if not isinstance(items,list):
            raise Blocked("Vendor task query response malformed.")
        matching=[x for x in items if isinstance(x,dict) and x.get("id")==task_id]
        if len(matching)!=1:
            raise Blocked("Vendor task record not returned.")
        data=matching[0]
        return {"status":data.get("status"),"share_link_present":bool(data.get("shareLink")),
                "task_id":task_id}

def check_inputs(args: argparse.Namespace) -> tuple[dict,dict,datetime,str,dict]:
    post=load_post(args.post_id)
    public_ledger=validate_state(read_document(PUB_STATE,missing={"version":1,"items":{}}))
    if post["id"] in public_ledger["items"]:
        raise Blocked("Post already claimed or published in the official ledger.")
    ledger=validate_state_doc(read_document(LEDGER))
    if post["id"] in ledger["items"]:
        raise Blocked("Post already claimed by cloud phone; no automatic retry.")
    when=iso_time(args.schedule_at)
    now=datetime.now(timezone.utc)
    if when < now+timedelta(minutes=10) or when > now+timedelta(days=75):
        raise Blocked("Schedule must be at least 10 minutes ahead and within 75 days.")
    music=source_url(args.music_url)
    flags={
        "api_token_present":bool(os.getenv("GEELARK_TOKEN")),
        "phone_id_present":bool(os.getenv("GEELARK_PHONE_ID")),
        "publisher_enabled":os.getenv("GEELARK_PUBLISH_ENABLED")=="true",
        "account_confirmed":os.getenv("GEELARK_ACCOUNT_CONFIRMED")=="true",
        "vendor_cost_approved":os.getenv("GEELARK_COST_APPROVED")=="true",
    }
    return post,ledger,when,music,flags

def check(args: argparse.Namespace) -> int:
    post=load_post(args.post_id)
    public_ledger=validate_state(read_document(PUB_STATE,missing={"version":1,"items":{}}))
    ledger=validate_state_doc(read_document(LEDGER))
    flags={
        "api_token_present":bool(os.getenv("GEELARK_TOKEN")),
        "phone_id_present":bool(os.getenv("GEELARK_PHONE_ID")),
        "publisher_enabled":os.getenv("GEELARK_PUBLISH_ENABLED")=="true",
        "account_confirmed":os.getenv("GEELARK_ACCOUNT_CONFIRMED")=="true",
        "vendor_cost_approved":os.getenv("GEELARK_COST_APPROVED")=="true",
    }
    has_date=bool(args.schedule_at)
    has_music=bool(args.music_url)
    if has_date:
        when=iso_time(args.schedule_at)
        now=datetime.now(timezone.utc)
        if when < now+timedelta(minutes=10) or when > now+timedelta(days=75):
            raise Blocked("Schedule must be at least 10 minutes ahead and within 75 days.")
    if has_music:
        source_url(args.music_url)
    already_claimed=(post["id"] in public_ledger["items"] or post["id"] in ledger["items"])
    ready=(all(flags.values()) and has_date and has_music and not already_claimed)
    print(json.dumps({
        "ok":True,"mode":"check","post_id":post["id"],
        "account":ACCOUNT,"images":len(post["media_urls"]),
        "native_music_url_supplied":has_music,
        "schedule_utc":args.schedule_at if has_date else None,
        "vendor":"GeeLark documented Instagram RPA template",
        "task_exists":already_claimed,"conditions":flags,"ready_to_attempt":ready,
        "publication_attempted":False,
    },ensure_ascii=False))
    return 0

def submit(args: argparse.Namespace) -> int:
    post,ledger,when,music,flags=check_inputs(args)
    if not all(flags.values()):
        raise Blocked("Cloud service is not configured, approved and signed in. No task submitted.")
    phone_id=os.environ["GEELARK_PHONE_ID"]
    if not NUMERIC_ID.fullmatch(phone_id):
        raise Blocked("Invalid GeeLark cloud-phone ID.")
    from tempfile import TemporaryDirectory
    with TemporaryDirectory(prefix="instagram-geelark-") as tempdir:
        files=verify_files(post,Path(tempdir))
        # The durable claim precedes all vendor mutations and stops duplicate scheduling.
        ledger["items"][post["id"]]={
            "status":"claimed","fingerprint":fingerprint(post),
            "scheduled_at":args.schedule_at,"claimed_at":datetime.now(timezone.utc).isoformat(),
            "music_source_url":music,
        }
        git_save(ledger,"Claim GeeLark native-music carousel "+post["id"])
        client=GeeLark(os.environ["GEELARK_TOKEN"])
        try:
            media=[client.upload_jpg(p) for p in files]
            task_id=client.submit(phone_id=phone_id,images=media,
                                  caption=post["caption"],when=when,music=music,
                                  post_id=post["id"])
            ledger["items"][post["id"]].update(
                status="scheduled",vendor_task_id=task_id)
            git_save(ledger,"Record GeeLark task ID "+post["id"])
        except Exception:
            ledger["items"][post["id"]]["status"]="needs_review"
            git_save(ledger,"Quarantine uncertain GeeLark task "+post["id"])
            raise Blocked("Vendor task was not confirmed. Check service and Instagram; do not retry.") from None
    print(json.dumps({"ok":True,"mode":"scheduled","post_id":post["id"],
                      "vendor_task_id":task_id,"task_confirmed_by_vendor":True,
                      "instagram_publication_confirmed":False},ensure_ascii=False))
    return 0

def reconcile(args: argparse.Namespace) -> int:
    ledger=validate_state_doc(read_document(LEDGER))
    to_check={k:v for k,v in ledger["items"].items()
              if v["status"]=="scheduled" and v.get("vendor_task_id")}
    if not to_check:
        print('{"ok":true,"mode":"reconcile","tasks_checked":0}')
        return 0
    token=os.environ.get("GEELARK_TOKEN","")
    if not token:
        raise Blocked("Cannot reconcile tasks without configured GeeLark API token.")
    client=GeeLark(token)
    results=[]
    for post_id,entry in list(to_check.items())[:10]:
        status=client.task_status(entry["vendor_task_id"])
        v=status["status"]
        if v==3:  # Vendor task completed, not independently verified on Instagram.
            entry["status"]="vendor_completed_unverified"
        elif v in (4,7): # Failed/cancelled: may still have side effects.
            entry["status"]="needs_review"
        elif v not in (1,2):
            entry["status"]="needs_review"
        results.append({"post_id":post_id,"vendor_status":v,
                        "share_link_present":status["share_link_present"],
                        "instagram_music_verified":False})
    if any(ledger["items"][r["post_id"]]["status"]!="scheduled" for r in results):
        git_save(ledger,"Reconcile GeeLark task status (unverified music)")
    print(json.dumps({"ok":True,"mode":"reconcile","tasks_checked":len(results),
                      "items":results},ensure_ascii=False))
    return 0

def auto() -> int:
    """One approved music carousel per invocation, never more than one."""
    document=read_document(Path("content/geelark-music-plan.json"))
    if (not isinstance(document,dict) or set(document)!={"version","account","items"}
        or document.get("version")!=1 or document.get("account")!=ACCOUNT
        or not isinstance(document.get("items"),list)
        or len(document["items"])>100):
        raise Blocked("Invalid approved GeeLark music queue.")
    posts={p["id"]:p for p in validate_manifest(read_document(MANIFEST))}
    ledger=validate_state_doc(read_document(LEDGER))
    used=set()
    eligible=[]
    for item in document["items"]:
        if not isinstance(item,dict) or set(item)!={"id","schedule_utc","music_source_url","approved"}:
            raise Blocked("Invalid music assignment shape.")
        pid=item.get("id")
        if not isinstance(pid,str) or not POST_SLUG.fullmatch(pid) or pid in used:
            raise Blocked("Duplicate or invalid approved music assignment ID.")
        used.add(pid)
        if item.get("approved") is not True:
            continue
        post=posts.get(pid)
        if post is None or post.get("approved") is not True or post.get("kind")!="carousel":
            raise Blocked("Approved music assignment references unapproved content.")
        if post.get("due_at")!=item.get("schedule_utc"):
            raise Blocked("Music schedule must exactly match the approved editorial due time.")
        when=iso_time(item["schedule_utc"])
        music=source_url(item["music_source_url"])
        if pid in ledger["items"]:
            continue
        # Past or already published assignments stay unmodified, not auto-rescheduled.
        now=datetime.now(timezone.utc)
        if when < now+timedelta(minutes=10) or when > now+timedelta(days=75):
            continue
        eligible.append((when,pid,music))
    if not eligible:
        print('{"ok":true,"mode":"auto","tasks_scheduled":0,"reason":"no_due_approved_music_assignments"}')
        return 0
    eligible.sort()
    when,pid,music=eligible[0]
    if not all((
       bool(os.getenv("GEELARK_TOKEN")),bool(os.getenv("GEELARK_PHONE_ID")),
       os.getenv("GEELARK_PUBLISH_ENABLED")=="true",
       os.getenv("GEELARK_ACCOUNT_CONFIRMED")=="true",
       os.getenv("GEELARK_COST_APPROVED")=="true",
    )):
        print('{"ok":true,"mode":"auto","tasks_scheduled":0,"reason":"cloud_phone_not_authorized"}')
        return 0
    params=argparse.Namespace(post_id=pid,
        schedule_at=when.replace(microsecond=0).isoformat().replace("+00:00","Z"),
        music_url=music)
    return submit(params)

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=("check","submit","reconcile","auto"))
    p.add_argument("--post-id",default="")
    p.add_argument("--schedule-at",default="")
    p.add_argument("--music-url",default="")
    args=p.parse_args()
    try:
        if args.mode=="check":return check(args)
        if args.mode=="submit":return submit(args)
        if args.mode=="auto":return auto()
        return reconcile(args)
    except Exception as error:
        # Whitelist types only. No vendor messages, tokens or signed URLs in logs.
        print(json.dumps({"ok":False,"mode":args.mode,"error_type":type(error).__name__,
                          "message":str(error) if isinstance(error,Blocked)
                                    else "Validation or vendor check failed."}),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""One-shot import and real Meta publication for the SIX user-approved Lúmino slides.

No re-rendering or substitution of art. The owner explicitly approved exactly the
six new differentiated-pose images on 2026-11-05. Fail closed on any SHA, Drive,
Meta identity, publishing permissions, duplicate, or ledger uncertainty.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

import requests
from PIL import Image
from facebook_poster import FacebookConfig, FacebookPoster
from instagram_queue import (
    GitLedger, read_document, validate_manifest, validate_state, run_queue, plan,
)
from instagram_preflight import check as check_preflight

REPO = "gabrielslinhares12-sudo/instagram-skills"
ID = "tue-2026-11-05-lumino-historia-final-aprovada"
PREFIX = Path("content/media/instagram/2026-11-05/LUMINO-HISTORIA-FINAL-APROVADO")
STATE = Path("content/publication-state.json")
QUEUE = Path("content/schedule.json")
TARGET = "https://www.instagram.com/temumaexplicacao/"
FILES = [
  ("1tDx5lTLIYDsDs41gUjSnpK9UT-cfhagH", "7d5b4ce12a307cb1a4a58de95c379646210134f5f286f296965fe3cfbf67ec88"),
  ("1oi1YHhBPzVcc4pe6ON09wwq5TBrgOApy", "8f009dcc82e9341d74c0e4fa899a1070b10b2422a381225adbc2dda3f124ca35"),
  ("1G7pK5w6gFoJ2Bp9XGRRRFlW_GjUYv5vw", "e242d3fd3b0a3fd5e8296ec8330b5d5aeace6dc198c0a7169b7a42bf003ce490"),
  ("1Ngrw1Tn8rjWPV8R-5pvck-6rlED7cyo1", "eaf58274cdc0f9edda32995d62ef8fdb6de3e91f36dafcdf303a5d2bb848c78a"),
  ("1uVhOTpl4itiRTy5N7rdprUydcyp1xIkv", "3dad49f3b20b489209e1d4c2602b8c2e81c38e449b7d8499853dfaee21c1fb62"),
  ("1LYdcl5k05_vpjocS_dhUDCJhdY3BQQ9F", "03375b61b262214559892a41258a9f40cda1f57031717acd92f4b6f97a127952"),
]
CAPTION = """💡🔎 QUEM É O LÚMINO?

Toda grande explicação começa com uma pergunta. Conheça a história do nosso detetive da curiosidade: uma lanterna que ilumina ideias e investiga os mistérios do mundo, do oceano às estrelas.

Ele segue três passos: observa, busca pistas e confere as explicações. Agora, a próxima pergunta é sua!

Qual mistério devemos investigar juntos?

#TemUmaExplicacao #Lumino #Curiosidades #Ciencia #HistoriaDoLumino"""
CLAIM_FINGERPRINT = "#HistoriaDoLumino"

class SafeBlock(Exception):
    pass

def cmd(*args):
    try:
        r = subprocess.run(list(args), check=True, capture_output=True, text=True, timeout=75)
        return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        raise SafeBlock("git_operation_failed") from None

def oauth():
    keys=("GDRIVE_OAUTH_CLIENT_ID","GDRIVE_OAUTH_CLIENT_SECRET","GDRIVE_OAUTH_REFRESH_TOKEN")
    vals=[os.environ.get(k,"").strip() for k in keys]
    print("GOOGLE_DRIVE_OAUTH_CONFIGURED=" + str(all(vals)).lower(), flush=True)
    if not all(vals):
        return None
    response=requests.post(
        "https://oauth2.googleapis.com/token",
        data=dict(client_id=vals[0],client_secret=vals[1],refresh_token=vals[2],grant_type="refresh_token"),
        timeout=25,
    )
    if response.status_code!=200:
        raise SafeBlock("drive_oauth_refresh_rejected")
    token=response.json().get("access_token")
    if not isinstance(token,str) or len(token)<20:
        raise SafeBlock("drive_oauth_response_no_token")
    return token

def get_jpeg(fid, token):
    if token:
        response=requests.get(
            f"https://www.googleapis.com/drive/v3/files/{fid}",
            params={"alt":"media"},
            headers={"Authorization": "Bearer "+token},
            timeout=80,
        )
        if response.status_code == 200:
            return response.content
        print("DRIVE_OAUTH_READ_RESULT_"+str(response.status_code), flush=True)
    response=requests.get(
        f"https://drive.google.com/uc?export=download&id={fid}", timeout=80
    )
    if response.status_code != 200:
        raise SafeBlock("drive_media_unavailable_http_"+str(response.status_code))
    return response.content

def verify_and_store():
    """Use the six approved original JPEGs already committed in GitHub, not private Drive."""
    if not PREFIX.is_dir():
        raise SafeBlock("approved_github_image_directory_not_found")
    for i,(_,sha) in enumerate(FILES,1):
        file=PREFIX/f"LUMINO-HISTORIA-FINAL-{i:02d}.jpg"
        if not file.is_file():
            raise SafeBlock(f"github_image_missing_{i}")
        data=file.read_bytes()
        if hashlib.sha256(data).hexdigest()!=sha:
            raise SafeBlock(f"github_image_sha256_mismatch_{i}")
        if len(data)>4*1024*1024:
            raise SafeBlock(f"github_image_too_large_{i}")
        try:
            with Image.open(BytesIO(data)) as im:
                if im.format!="JPEG" or im.size!=(1080,1350):
                    raise SafeBlock(f"github_image_invalid_format_or_resolution_{i}")
        except OSError:
            raise SafeBlock(f"github_image_invalid_{i}")
        print(f"APPROVED_MEDIA_{i}_SHA256_VERIFIED=true SIZE={len(data)}",flush=True)

def stage_queue():
    current=read_document(QUEUE)
    if any(p.get("id")==ID for p in current["posts"]):
        raise SafeBlock("one_shot_post_already_in_queue_no_auto_retry")
    now=datetime.now(timezone.utc)
    due=(now-timedelta(seconds=35)).isoformat(timespec="seconds").replace("+00:00","Z")
    # Original bytes are already committed and identified by immutable commit SHA.
    cmd("git","config","user.name","github-actions[bot]")
    cmd("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
    pinned="ce0b441ac5303fd1eb477eeab148b48da6058639"
    urls=[f"https://raw.githubusercontent.com/{REPO}/{pinned}/{PREFIX.as_posix()}/LUMINO-HISTORIA-FINAL-{i:02d}.jpg" for i in range(1,7)]
    for i,(url,(_,sha)) in enumerate(zip(urls,FILES),1):
        # Meta needs to reach these URLs without GitHub credentials.
        readable=False
        for attempt in range(3):
            r=requests.get(url,timeout=30)
            if r.status_code==200 and hashlib.sha256(r.content).hexdigest()==sha:
                readable=True
                break
            time.sleep(3)
        if not readable:
            raise SafeBlock(f"github_public_url_not_readable_or_sha_mismatch_{i}")
    post={
        "id": ID,
        "due_at":due,
        "username":"temumaexplicacao",
        "kind":"carousel",
        "target_url":TARGET,
        "title":"Quem é o Lúmino? A história do nosso detetive da curiosidade",
        "caption":CAPTION,
        "media_urls":urls,
        "media_sha256":[sha for _,sha in FILES],
        "approved":True,
        "ai_origin":"synthetic",
        "content_style":"clearly_illustrated",
        "ai_disclosure_review":"no_mandatory_self_disclosure_for_stylized_still",
        "distribution_mode":"api_carousel_without_native_music",
        "owner_authorized_without_music":True,
        "sources":[],
        "approval_note":"Usuario aprovou expressamente a postagem imediata das seis artes diferenciadas no chat em 2026-11-05; sem musica e sem story."
    }
    current["posts"].append(post)
    validate_manifest(current)
    QUEUE.write_text(json.dumps(current,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    cmd("git","add","--",str(QUEUE))
    cmd("git","commit","-m","ops(instagram): approve one-shot Lúmino six-image carousel after owner approval")
    cmd("git","push","origin","HEAD:main")
    print("STAGED_POST_ID="+ID,flush=True)
    return post

def check_duplicate(poster):
    identity=poster.check_identity()
    if identity.get("username")!="temumaexplicacao":
        raise SafeBlock("instagram_identity_mismatch")
    r=poster._request("GET",poster.config.user_id+"/media",params={"fields":"id,media_type,caption,permalink","limit":100},timeout=30)
    if not isinstance(r.get("data"),list):
        raise SafeBlock("instagram_recent_media_unavailable")
    for item in r["data"]:
        if not isinstance(item,dict):
            continue
        if item.get("media_type")=="CAROUSEL_ALBUM" and CLAIM_FINGERPRINT in (item.get("caption") or ""):
            print("DUPLICATE_FOUND_MEDIA_ID="+str(item.get("id","unknown")),flush=True)
            return item.get("id")
    return None

def main():
    if os.getenv("GITHUB_REF")!="refs/heads/main":
        raise SafeBlock("not_main_branch")
    existing=validate_state(read_document(STATE,missing={"version":1,"items":{}}))
    if ID in existing["items"]:
        raise SafeBlock("already_claimed_no_retry")
    if any(p.get("id")==ID for p in read_document(QUEUE)["posts"]):
        raise SafeBlock("already_in_queue_needs_manual_reconciliation")

    verify_and_store()
    # Check the target identity and existing Instagram posts BEFORE queue registration.
    poster=FacebookPoster(FacebookConfig.from_env())
    preflight=check_preflight(poster)
    if not preflight.get("ok") or preflight.get("username")!="temumaexplicacao":
        raise SafeBlock("meta_preflight_failed_not_published")
    if check_duplicate(poster):
        print(json.dumps({"status":"duplicate_confirmed","publication_attempted":False,"post_id":ID}),flush=True)
        return 0
    # Do not mutate Instagram until public GitHub URL hashes and the queue are verified.
    post=stage_queue()
    now=datetime.now(timezone.utc)
    state=validate_state(read_document(STATE,missing={"version":1,"items":{}}))
    if plan([post],state,now)[0]["status"]!="due":
        raise SafeBlock("post_not_due_after_staging")
    result=run_queue([post],state,now,execute=True,enabled=True,
        persist=GitLedger(STATE),poster_factory=lambda:poster)
    print("CAROUSEL_PUBLICATION_RESULT="+json.dumps(result,ensure_ascii=False),flush=True)
    if not result.get("ok") or result.get("status")!="published":
        raise SafeBlock("meta_publication_not_confirmed_no_automatic_retry")
    try:
        details=poster._request("GET",str(result["media_id"]),params={"fields":"id,permalink,media_type"},timeout=25)
        print("META_CONFIRMED_POST="+json.dumps(details,ensure_ascii=False),flush=True)
    except Exception:
        print("META_MEDIA_ID_CONFIRMED_PERMALINK_LOOKUP_UNAVAILABLE",flush=True)
    return 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except SafeBlock as exc:
        print("TUE_LUMINO_ONE_SHOT_BLOCKED="+str(exc),file=sys.stderr,flush=True)
        sys.exit(1)
    except Exception as exc:
        print("TUE_LUMINO_ONE_SHOT_UNEXPECTED="+type(exc).__name__,file=sys.stderr,flush=True)
        sys.exit(1)

#!/usr/bin/env python3
"""Owner-approved Lúmino origin carousel, 05 Nov 2026: private Drive -> public JPGs -> Meta.

One-shot, no paid API, no browser, no Stories, no music.
Never post before all six image digests, public media URLs, account, permissions
and Instagram recent history have been verified. A durable Git claim precedes POST.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from io import BytesIO
import hashlib, json, os, subprocess, sys, time, urllib.parse

from PIL import Image

from facebook_poster import FacebookPoster, FacebookConfig
from instagram_preflight import check as preflight
from instagram_queue import GitLedger, read_document, validate_state, validate_manifest, run_queue

REPO="gabrielslinhares12-sudo/instagram-skills"
PREFIX="content/media/instagram/2026-11-05/LUMINO-ORIGEM-APROVADO"
POST_ID="tue-2026-11-05-lumino-origem-aprovado"
EXPECTED_IG="17841433004716815"
SOURCE=[
  ("1PYvzRe6jGclZlN6SfGSUIa-zLRrQ-HZv","01-quem-e-o-lumino.jpg","c22c9e54894fa6106a5b0c7d16952e0379370b9749092492e11ad4362005cbf0"),
  ("1O6KRH4XR87mKsXnBfKcL6edM6INlf04g","02-onde-tudo-comecou.jpg","7bdb8186a1db25cbfd27ada9206c9b05fbcf9495e46525534fb8fb1f5bf3a82e"),
  ("1TsrYO77czm4F_d-ZYaV7WT01bTRQTfLb","03-nao-e-magia.jpg","88b38679513c3519b10a53e6d9e54a21e2777a607e1a5b99f928bb6a0f15bdb0"),
  ("1f1JUrrx1idCCLc4pAuYi9pgR5tbXA3AS","04-do-oceano-as-estrelas.jpg","bf613e7be6cb85079fed6c502183dfff6fd21b481f77f0d9de1a27a911934a1c"),
  ("1QO4jaQO1Ovw_7P1GflOv9WrzBBCY_Yp8","05-ele-investiga-com-metodo.jpg","0c1f9b8e724fffceca2c50ddfe0a62fd661739d632a1a54e83e6cccda93a88c7"),
  ("1OpDCSUKStD6W8OsXEYagTcwrRvHJ9JCG","06-a-proxima-pergunta-e-sua.jpg","3d8ffd50746aa271f51cd55fe11a56fd4e5ecf6b0d3eee6227786cd65883016e")
]
CAPTION=("A HISTÓRIA DO LÚMINO 💡🔎\n\n"
"De onde veio essa luz que nunca para de fazer perguntas? Conheça o Lúmino, o nosso detetive da curiosidade: observa o mundo, segue pistas e transforma dúvidas em descobertas.\n\n"
"Da natureza às estrelas, sua missão é mostrar que grandes explicações começam com boas perguntas. E agora ele quer ouvir a sua: qual mistério você gostaria de investigar?\n\n"
"#TemUmaExplicacao #Lumino #Curiosidades #Ciencia #Descobertas")
STATE=Path("content/publication-state.json")

def git(*args):
    return subprocess.run(["git",*args],check=True,text=True,capture_output=True,timeout=90).stdout.strip()

def sha(data): return hashlib.sha256(data).hexdigest()

def oauth_token():
    keys=("GDRIVE_OAUTH_CLIENT_ID","GDRIVE_OAUTH_CLIENT_SECRET","GDRIVE_OAUTH_REFRESH_TOKEN")
    env=[os.environ.get(k,"").strip() for k in keys]
    print("GOOGLE_DRIVE_OAUTH_CONFIGURED="+str(all(env)).lower(),flush=True)
    if not all(env): return None
    body=urllib.parse.urlencode(dict(client_id=env[0],client_secret=env[1],
                                     refresh_token=env[2],grant_type="refresh_token")).encode()
    try:
        with urlopen(Request("https://oauth2.googleapis.com/token",data=body,
                  headers={"Content-Type":"application/x-www-form-urlencoded"}),timeout=30) as resp:
            value=json.load(resp).get("access_token")
    except (URLError,HTTPError,ValueError,TimeoutError) as e:
        raise RuntimeError("drive_oauth_refresh_failed") from None
    if not isinstance(value,str) or len(value)<20: raise RuntimeError("drive_oauth_token_unavailable")
    return value

def download_png(fid,expected,token):
    endpoints=[]
    if token: endpoints.append((f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media",{"Authorization":"Bearer "+token}))
    endpoints.append((f"https://drive.google.com/uc?export=download&id={fid}",{}))
    problems=[]
    for url,headers in endpoints:
        try:
            with urlopen(Request(url,headers=headers),timeout=60) as resp:
                if resp.status!=200: raise RuntimeError("not_http_200")
                b=resp.read(4_200_000)
                if len(b)>4_000_000: raise RuntimeError("image_too_large")
            if sha(b)!=expected: raise RuntimeError("unexpected_image_sha256")
            if b[:8]!=b'\x89PNG\r\n\x1a\n':raise RuntimeError("not_png")
            with Image.open(BytesIO(b)) as im:
                im.load()
                if im.size!=(1122,1402) or im.format!="PNG": raise RuntimeError("wrong_dimensions")
            return b
        except (URLError,HTTPError,TimeoutError,RuntimeError,OSError) as e:
            problems.append(type(e).__name__)
    raise RuntimeError("drive_source_unavailable_or_wrong_bytes:"+str(problems))

def stage_images():
    if POST_ID in validate_state(read_document(STATE,missing={"version":1,"items":{}}))["items"]:
        print("EXISTING_DURABLE_CLAIM_NO_RETRY",flush=True)
        return None
    token=oauth_token()
    os.makedirs(PREFIX,exist_ok=True)
    entries=[]
    for i,(fid,name,digest) in enumerate(SOURCE,1):
        b=download_png(fid,digest,token)
        with Image.open(BytesIO(b)) as im:
            final=im.convert("RGB").resize((1080,1350),Image.Resampling.LANCZOS)
        path=Path(PREFIX)/name
        final.save(path,"JPEG",quality=92,subsampling=0,optimize=True)
        with Image.open(path) as check:
            if check.format!="JPEG" or check.size!=(1080,1350):raise RuntimeError("JPEG_QC_FAILED")
        j=path.read_bytes()
        entries.append({"file":name,"sha256":sha(j),"bytes":len(j),"source_sha256":digest})
        print(f"ASSET_{i}=verified={len(j)}_bytes",flush=True)
    (Path(PREFIX)/"MANIFEST.json").write_text(json.dumps({
        "origin":"six_owner_approved_images_from_chat_2026-11-05",
        "visual_standard":"TUE-MESTRE-01",
        "status":"approved_for_immediate_post_by_owner",
        "ai_origin":"synthetic",
        "count":6,"files":entries},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (Path(PREFIX)/"LEGENDA.txt").write_text(CAPTION,encoding="utf-8")
    git("config","user.name","github-actions[bot]")
    git("config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
    git("add","--",PREFIX)
    git("commit","-m","media(lumino): stage six owner-approved generated slides for immediate Instagram")
    git("push","origin","HEAD:main")
    pinned=git("rev-parse","HEAD")
    print("APPROVED_SLIDES_STAGED="+pinned,flush=True)
    urls=[f"https://raw.githubusercontent.com/{REPO}/{pinned}/{PREFIX}/{row['file']}" for row in entries]
    for i,(url,row) in enumerate(zip(urls,entries),1):
        # Read-only retry after push for GitHub CDN propagation.
        for retry in range(7):
            try:
                with urlopen(Request(url,headers={"User-Agent":"TUE-Instagram-Meta-Preflight/1.0"}),timeout=25) as res:
                    b=res.read(2_500_000)
                    if res.status==200 and sha(b)==row["sha256"]:break
            except (HTTPError,URLError,TimeoutError):pass
            if retry==6:raise RuntimeError(f"public_jpeg_{i}_not_verified")
            time.sleep(6)
        else:raise RuntimeError("unreachable")
    print("ALL_SIX_PUBLIC_MEDIA_URLS_VERIFIED",flush=True)
    return urls,[row["sha256"] for row in entries]

def duplicate_check(poster):
    identity=poster.check_identity()
    if (identity.get("username")!="temumaexplicacao" or identity.get("instagram_user_id")!=EXPECTED_IG):
        raise RuntimeError("wrong_instagram_identity")
    # Bounded recent media check, fail closed if unable to inspect.
    response=poster._request("GET",EXPECTED_IG+"/media",
       params={"fields":"id,caption,media_type,permalink","limit":100},timeout=35)
    records=response.get("data")
    if not isinstance(records,list):raise RuntimeError("recent_instagram_media_unavailable")
    for item in records:
        caption=(item.get("caption") or "").lower()
        if item.get("media_type")=="CAROUSEL_ALBUM" and (
           caption==CAPTION.lower() or ("a história do lúmino" in caption and "#lumino" in caption)):
            print("ALREADY_PUBLISHED_MEDIA_ID="+str(item.get("id")),flush=True)
            print("ALREADY_PUBLISHED_PERMALINK="+str(item.get("permalink")),flush=True)
            return True
    return False

def publish(urls,digests):
    state=validate_state(read_document(STATE,missing={"version":1,"items":{}}))
    if POST_ID in state["items"]:
        print("EXISTING_CLAIM_NO_AUTOMATIC_REPOST",flush=True)
        return 0
    now=datetime.now(timezone.utc)
    if now.date().isoformat()!="2026-11-05":raise RuntimeError("outside_owner_approved_day")
    post={
       "id":POST_ID,
       "due_at":(now-timedelta(seconds=45)).isoformat(timespec="seconds").replace("+00:00","Z"),
       "username":"temumaexplicacao",
       "kind":"carousel",
       "target_url":"https://www.instagram.com/temumaexplicacao/",
       "title":"Quem é o Lúmino? A história do nosso detetive",
       "caption":CAPTION,
       "media_urls":urls,
       "media_sha256":digests,
       "approved":True,
       "ai_origin":"synthetic",
       "content_style":"clearly_illustrated",
       "ai_disclosure_review":"no_mandatory_self_disclosure_for_stylized_still",
       "sources":[],
       "approval_note":"Proprietário aprovou expressamente em 05/11/2026 as seis artes e pediu: Poste isso imediatamente no nosso Instagram.",
       "distribution_mode":"api_carousel_without_native_music",
       "owner_authorized_without_music":True
    }
    validated=validate_manifest({"version":1,"posts":[post]})
    poster=FacebookPoster(FacebookConfig.from_env())
    permissions=preflight(poster)
    print("META_PREFLIGHT_OK="+str(permissions.get("ok") is True).lower(),flush=True)
    if not permissions.get("ok"):raise RuntimeError("meta_publishing_permissions_not_verified")
    if duplicate_check(poster):return 0
    # Claim and push BEFORE any Meta write; uncertain responses are quarantined.
    result=run_queue(validated,state,now,execute=True,enabled=True,
        persist=GitLedger(STATE),poster_factory=lambda:poster)
    print("INSTAGRAM_PUBLISH_RESULT="+json.dumps(result,ensure_ascii=False),flush=True)
    media_id=result.get("media_id")
    if result.get("status")!="published" or not isinstance(media_id,str):
        return 1
    try:
        details=poster._request("GET",media_id,params={"fields":"id,permalink,media_type,caption"},timeout=30)
        if details.get("id")==media_id and details.get("permalink"):
            print("INSTAGRAM_VERIFIED_PERMALINK="+details["permalink"],flush=True)
    except Exception as e:
        print("PERMALINK_READBACK_UNAVAILABLE="+type(e).__name__,flush=True)
    return 0

def main():
    if os.environ.get("GITHUB_REF")!="refs/heads/main":raise RuntimeError("not_main")
    stage=stage_images()
    if stage is None:return 0
    return publish(*stage)

if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:
        print("ONE_SHOT_BLOCKED="+type(e).__name__+":"+str(e),file=sys.stderr,flush=True)
        sys.exit(1)

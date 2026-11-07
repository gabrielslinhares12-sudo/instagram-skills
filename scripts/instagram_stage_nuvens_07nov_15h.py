#!/usr/bin/env python3
"""Stage five exact user-approved lenticular-cloud images for 15h Brazil, 07NOV.

GitHub-hosted only. Never publish in this staging step. Pins immutable JPEGs,
checks hashes and Meta identity/duplicates before queueing. No draft substitution.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from PIL import Image
import hashlib
import json
import os
import subprocess
import sys
import time

from instagram_queue import read_document, validate_manifest, validate_state
from facebook_poster import FacebookPoster, FacebookConfig
from instagram_visual_standard import audit_queue

REPO = "gabrielslinhares12-sudo/instagram-skills"
POST_ID = "tue-2026-11-07-15-nuvens-lenticulares-5-artes"
DUE = "2026-11-07T18:00:00Z"
SOURCE_COMMIT = "497c17aefb193b374729d186ebcaab0aa134edc2"
ROOT = Path("content/media/instagram/2026-11-07/nuvens-lenticulares-15h")
SOURCE_SHA = [
    "51cf2742520b076eed2ab3941b8fc827457a06ed392e8f37ba2bcf12449f538c",
    "0b9b5a38e2786c9c547020a6875de303b3b30606730804dba9a39c4badfea3bb",
    "ca5769b9443146a3d12c2fd750919c8f17be48568e83e1c506b021ed7c8caab3",
    "ba53d169ee9aecc7c69291e596a8b897261bcc8427373265b13c3c672e3ccf58",
    "6c0f858edb15c840493cb18d627ff550b48e802c1e92ced00ff669182c17c126",
]
JPG_SHA = [
    "f4241da6d12dda32c554f7319c11d934323755ed673f814b3680223638f28930",
    "567f0068b05a66c0c052a69b7dde07faf2474f68db347268105d498d0074863e",
    "483808cf9ce29bd54f16c4958ab8838c86684d38ca0d00e216ef4a5719989ae9",
    "aba33b558250363b5fc2cf73f6ee019c1133d2f82344c2dbfb079e15843b602b",
    "dbd3c308f1996b2989d7053d82d50a0b37c5fdc910bfdce9b55944faa517bbe3",
]
CAPTION = (
    "☁️ ESSAS NUVENS PARECEM OVNIs? O céu às vezes cria formas que "
    "parecem discos voadores — mas isso tem uma explicação!\n\n"
    "As nuvens lenticulares surgem quando o ar úmido atravessa regiões "
    "montanhosas e forma ondas atmosféricas. Quando a umidade condensa "
    "nessas ondas, aparecem camadas com formato de lente. Mesmo com "
    "vento, elas podem parecer paradas porque se formam continuamente "
    "na mesma região.\n\n"
    "Você já viu uma nuvem assim? ☁️\n\n"
    "#TemUmaExplicacao #Lumino #NuvensLenticulares "
    "#Meteorologia #Ciencia #Curiosidades"
)

def run_git(*args):
    result = subprocess.run(["git",*args],check=True,capture_output=True,text=True,timeout=90)
    return result.stdout.strip()

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check_time():
    now = datetime.now(timezone.utc)
    due = datetime.fromisoformat(DUE.replace("Z","+00:00"))
    if now >= due:
        raise RuntimeError("15h_deadline_passed: do_not_backdate")

def preexisting_queue_and_ledger():
    schedule = validate_manifest(read_document(Path("content/schedule.json")))
    ledger = validate_state(read_document(Path("content/publication-state.json")))
    if POST_ID in ledger["items"]:
        raise RuntimeError("post_has_claim_or_receipt_prevent_duplicate")
    if any(p["id"] == POST_ID for p in schedule):
        print("ALREADY_QUEUED_NO_REPOST",flush=True)
        return False
    if any(p["due_at"] == DUE and p["approved"] for p in schedule):
        raise RuntimeError("15h_slot_already_reserved")
    return True

def verify_meta_destination_and_duplicates():
    poster=FacebookPoster(FacebookConfig.from_env())
    identity=poster.check_identity()
    if identity.get("username") != "temumaexplicacao" or identity.get("instagram_user_id") != "17841433004716815":
        raise RuntimeError("wrong_meta_account")
    response=poster._request("GET","17841433004716815/media",
        params={"fields":"id,caption,permalink,timestamp,media_type","limit":100},timeout=40)
    rows=response.get("data")
    if not isinstance(rows,list):
        raise RuntimeError("unable_to_verify_meta_duplicates")
    for row in rows:
        caption=str(row.get("caption") or "").casefold()
        if ("nuvens lenticulares" in caption or
            ("essas nuvens" in caption and "ovnis" in caption)):
            print("POSSIBLE_DUPLICATE_ID="+str(row.get("id")),flush=True)
            raise RuntimeError("similar_carousel_already_on_instagram_manual_reconcile")
    print("META_ACCOUNT_VERIFIED_AND_NO_SIMILAR_POST",flush=True)

def convert_approved_media():
    (ROOT/"final").mkdir(parents=True,exist_ok=True)
    for i,(source_sha,jpg_sha) in enumerate(zip(SOURCE_SHA,JPG_SHA),1):
        source=ROOT/"aprovados-originais"/f"{i:02d}.png"
        dest=ROOT/"final"/f"{i:02d}-nuvens-lenticulares.jpg"
        if not source.is_file() or digest(source)!=source_sha:
            raise RuntimeError(f"approved_original_{i}_not_identical")
        with Image.open(source) as im:
            if im.format != "PNG" or im.size != (1122,1402):
                raise RuntimeError(f"approved_original_{i}_invalid_format")
            jpg=im.convert("RGB").resize((1080,1350),Image.Resampling.LANCZOS)
        jpg.save(dest,"JPEG",quality=95,optimize=True,subsampling=0,progressive=False)
        if digest(dest) != jpg_sha:
            raise RuntimeError(f"jpg_conversion_{i}_not_identical_to_reviewed_export")
        with Image.open(dest) as im:
            im.verify()
        print(f"APPROVED_JPG_VERIFIED_{i}="+jpg_sha,flush=True)

def commit_media():
    run_git("add","--",str(ROOT/"final"))
    run_git("commit","-m","media(instagram): exportar 5 artes aprovadas 15h sem alteracao criativa")
    run_git("push","origin","HEAD:main")
    return run_git("rev-parse","HEAD")

def verify_public_immutable_urls(release_sha):
    urls=[]
    for i,expected in enumerate(JPG_SHA,1):
        url=(f"https://raw.githubusercontent.com/{REPO}/{release_sha}/"
             f"{ROOT.as_posix()}/final/{i:02d}-nuvens-lenticulares.jpg")
        for attempt in range(8):
            try:
                with urlopen(Request(url,headers={"User-Agent":"InstagramTUE-ApprovedArtwork/1.0"}),timeout=20) as response:
                    raw=response.read(2_000_000)
                if hashlib.sha256(raw).hexdigest()==expected:
                    break
            except (HTTPError,URLError,TimeoutError):
                pass
            if attempt==7:
                raise RuntimeError(f"immutable_jpg_{i}_not_publicly_available")
            time.sleep(5)
        print(f"PINNED_MEDIA_PUBLIC_{i}=true",flush=True)
        urls.append(url)
    return urls

def save_approval_and_schedule(release_sha,urls):
    run_git("pull","--ff-only","origin","main")
    if not preexisting_queue_and_ledger():
        return
    approval={
        "id":POST_ID,"preset_id":"TUE-MESTRE-01","approved":True,
        "owner_authorized":True,"visual_reviewed":True,
        "original_mascot_pixel_match_verified":False,
        "source_commit":SOURCE_COMMIT,"release_commit":release_sha,
        "source_png_sha256":SOURCE_SHA,
        "approved_media_sha256":JPG_SHA,"release_media_urls":urls,
        "post_due_at":DUE,"distribution_mode":"api_carousel_without_native_music",
        "owner_authorized_without_music":True,
        "approval_note":("Proprietário visualmente aprovou o carrossel final de cinco imagens de "
                         "nuvens lenticulares em 07/11/2026 e solicitou agendamento às 15h. "
                         "Exceção vinculada aos PNGs exatos; nenhum pixel-match do Lúmino "
                         "canônico é afirmado."),
    }
    post={
        "id":POST_ID,"due_at":DUE,"username":"temumaexplicacao",
        "kind":"carousel","target_url":"https://www.instagram.com/temumaexplicacao/",
        "title":"Essas nuvens parecem OVNIs? — Nuvens lenticulares",
        "caption":CAPTION,"media_urls":urls,"media_sha256":JPG_SHA,
        "approved":True,"ai_origin":"synthetic","content_style":"clearly_illustrated",
        "ai_disclosure_review":"no_mandatory_self_disclosure_for_stylized_still",
        "distribution_mode":"api_carousel_without_native_music",
        "owner_authorized_without_music":True,
        "approval_note":"Aprovadas exatamente as cinco artes finais em conversa de 07/11/2026; postar às 15h.",
    }
    path=Path("content/approved")/POST_ID/"approval.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(approval,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest=read_document(Path("content/schedule.json"))
    manifest["posts"].append(post)
    validate_manifest(manifest)
    manifest["posts"].sort(key=lambda x:(x["due_at"],x["id"]))
    Path("content/schedule.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    check=audit_queue(only_ids={POST_ID})
    if POST_ID not in check["approved_new_carousels_checked"]:
        raise RuntimeError("specific_approved_media_quality_gate_not_passed")
    run_git("add","--",str(path),"content/schedule.json")
    run_git("commit","-m","schedule(instagram): nuvens lenticulares 07nov 15h 5 artes exatas")
    run_git("push","origin","HEAD:main")
    print("GITHUB_15H_QUEUE_VERIFIED="+POST_ID,flush=True)
    print("SCHEDULED_UTC="+DUE,flush=True)
    print("SCHEDULED_BRT=2026-11-07T15:00:00-03:00",flush=True)
    print("IMMUTABLE_MEDIA_COMMIT="+release_sha,flush=True)

def main():
    if os.getenv("GITHUB_REF")!="refs/heads/main":
        raise RuntimeError("only_main_branch_authorized")
    check_time()
    run_git("config","user.name","github-actions[bot]")
    run_git("config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
    run_git("pull","--ff-only","origin","main")
    if not preexisting_queue_and_ledger():
        return 0
    verify_meta_destination_and_duplicates()
    convert_approved_media()
    release_sha=commit_media()
    urls=verify_public_immutable_urls(release_sha)
    save_approval_and_schedule(release_sha,urls)
    return 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print("15H_SCHEDULE_FAILED="+type(error).__name__+":"+str(error),file=sys.stderr,flush=True)
        sys.exit(1)

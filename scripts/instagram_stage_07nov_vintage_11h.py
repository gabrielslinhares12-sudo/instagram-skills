#!/usr/bin/env python3
"""Stage ONLY the owner-approved 07NOV vintage strip, then schedule for 11:00 BRT.

Source ZIP is an immutable archive stored on the owner's Google Drive.
Never use older draft images. No publishing is attempted by this script.
The existing Instagram scheduler is responsible for one-shot Meta publishing.
"""
from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import zipfile

from PIL import Image
from instagram_queue import read_document, validate_manifest, validate_state
from facebook_poster import FacebookPoster, FacebookConfig

REPO = "gabrielslinhares12-sudo/instagram-skills"
SOURCE_DRIVE_FILE = "1V45K8RswS7TtvQCpY7ai6xVo7jiTQg1H"
SOURCE_ZIP_SHA = "11593b93accea3e03f06fc4d9e94bd6c31ab12f0eacc973e6740f3d656ba62fe"
POST_ID = "tue-2026-11-07-11-rh-do-caos-cadeira-vintage-5-artes"
DEST = Path("content/media/instagram/2026-11-07/RH-DO-CAOS-VINTAGE")
QUEUE = Path("content/schedule.json")
LEDGER = Path("content/publication-state.json")
DUE_AT = "2026-11-07T14:00:00Z"
EXPECTED_IG_ID = "17841433004716815"
CAPTION = (
    "🪑 A CADEIRA PEDIU DEMISSÃO! No RH do Lúmino, uma cadeira descobriu que "
    "foi contratada para sentar gente, mas acabou trabalhando como guarda-roupa. "
    "Sem aumento, com acúmulo de função e até aviso prévio das roupas! 😂\n\n"
    "Na sua casa também existe uma cadeira promovida a armário? Conta aqui!\n\n"
    "#TemUmaExplicacao #Lumino #RHdoCaos #Tirinhas #Humor"
)
EXPECTED = {
    f"TIRINHA_{i:02d}_INSTAGRAM_1080x1350.jpg": digest
    for i, digest in enumerate([
        "e6445f43d5c7599125987c527fc05781357d6e2d7040df0041929947e45ba28a",
        "4f9a088ed9f126ec474aa5140954368e86061aa4d7cb8aca5ce9bab04b33d62f",
        "86088e45b4f7c0b887378d9f8aa3e1bab5613f378ebc3b61058d063b9a7dacea",
        "f76f84d1b93b906561b78b675b27018c19fc4183441d384d17c152d8c8998211",
        "ce54e848696fa8aa3874246ddc0935f584c686c7660da205aa540021d433ab41"
    ], 1)
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.run(["git", *args], check=True, text=True,
                          capture_output=True, timeout=90).stdout.strip()

def fetch_access_token():
    names = ("GDRIVE_OAUTH_CLIENT_ID", "GDRIVE_OAUTH_CLIENT_SECRET", "GDRIVE_OAUTH_REFRESH_TOKEN")
    values = [os.getenv(x, "").strip() for x in names]
    if not all(values):
        raise RuntimeError("missing_private_drive_oauth_credentials")
    payload = urlencode({
        "client_id": values[0], "client_secret": values[1],
        "refresh_token": values[2], "grant_type": "refresh_token"
    }).encode()
    with urlopen(Request("https://oauth2.googleapis.com/token", data=payload,
                         headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=35) as r:
        token = json.load(r).get("access_token")
    if not isinstance(token, str) or len(token) < 20:
        raise RuntimeError("drive_oauth_token_missing")
    return token

def download_exact_zip(token):
    url = f"https://www.googleapis.com/drive/v3/files/{SOURCE_DRIVE_FILE}?alt=media"
    with urlopen(Request(url, headers={"Authorization": "Bearer " + token}), timeout=90) as r:
        data = r.read(32_000_001)
    if len(data) > 32_000_000 or sha(data) != SOURCE_ZIP_SHA:
        raise RuntimeError("downloaded_package_not_exact_approved_zip")
    return data

def verified_jpegs(package):
    items = []
    with zipfile.ZipFile(BytesIO(package)) as zf:
        for index, (old_name, digest) in enumerate(EXPECTED.items(), 1):
            if old_name not in zf.namelist():
                raise RuntimeError("approved_jpeg_missing: " + old_name)
            data = zf.read(old_name)
            if sha(data) != digest:
                raise RuntimeError("approved_jpeg_checksum_mismatch: " + old_name)
            with Image.open(BytesIO(data)) as im:
                im.verify()
            with Image.open(BytesIO(data)) as im:
                if im.size != (1080, 1350) or im.format != "JPEG":
                    raise RuntimeError("approved_jpeg_invalid_dimensions")
            items.append((f"{index:02d}-tirinha-vintage.jpg", data, digest))
    return items

def verify_meta_destination():
    poster = FacebookPoster(FacebookConfig.from_env())
    identity = poster.check_identity()
    if identity.get("username") != "temumaexplicacao" or identity.get("instagram_user_id") != EXPECTED_IG_ID:
        raise RuntimeError("meta_wrong_target_account")
    result = poster._request("GET", EXPECTED_IG_ID + "/media",
        params={"fields":"id,media_type,caption,permalink,timestamp", "limit":100}, timeout=35)
    feed = result.get("data")
    if not isinstance(feed, list):
        raise RuntimeError("meta_recent_feed_check_unavailable")
    for item in feed:
        caption = (item.get("caption") or "").casefold()
        if "a cadeira pediu demissão" in caption and ("#rhdocaos" in caption or "guarda-roupa" in caption):
            print("POSSIBLE_EXISTING_POST=" + str(item.get("permalink")), flush=True)
            raise RuntimeError("already_published_or_possible_duplicate")
    print("META_ACCOUNT_VERIFIED_NO_MATCHING_DUPLICATE", flush=True)

def create_schedule(images):
    state = validate_state(read_document(LEDGER))
    if POST_ID in state["items"]:
        raise RuntimeError("post_already_claimed_no_duplicate")
    manifest = read_document(QUEUE)
    if any(x["id"] == POST_ID for x in manifest["posts"]):
        print("ALREADY_QUEUED_NO_MUTATION", flush=True)
        return False
    if any(x.get("due_at") == DUE_AT and x.get("approved") is True for x in manifest["posts"]):
        raise RuntimeError("first_slot_already_booked")
    pinned_commit = git("rev-parse", "HEAD")
    # Images will be committed first, then the queue is pinned to that image commit.
    urls = [f"https://raw.githubusercontent.com/{REPO}/{pinned_commit}/{DEST.as_posix()}/{filename}"
            for filename, _, _ in images]
    item = {
        "id": POST_ID, "due_at": DUE_AT,
        "username": "temumaexplicacao", "kind": "carousel",
        "target_url": "https://www.instagram.com/temumaexplicacao/",
        "title": "A cadeira pediu demissão — RH do Caos",
        "caption": CAPTION,
        "media_urls": urls,
        "media_sha256": [digest for _, _, digest in images],
        "approved": True,
        "ai_origin": "synthetic",
        "content_style": "clearly_illustrated",
        "ai_disclosure_review": "no_mandatory_self_disclosure_for_stylized_still",
        "distribution_mode": "api_carousel_without_native_music",
        "owner_authorized_without_music": True,
        "approval_note": ("Proprietário solicitou em 07/11/2026 agendar esta tirinha vintage"
                          " corrigida como primeira publicação do dia, preservando as cinco artes."),
    }
    manifest["posts"].append(item)
    manifest["posts"] = sorted(validate_manifest(manifest), key=lambda x: (x["due_at"], x["id"]))
    QUEUE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    git("add", "--", str(QUEUE))
    git("commit", "-m", "schedule(instagram): 07nov 11h tirinha vintage aprovada sem duplicatas")
    git("push", "origin", "HEAD:main")
    print("SCHEDULED_IN_GITHUB_QUEUE=2026-11-07T11:00:00-03:00", flush=True)
    print("QUEUE_ITEM_ID=" + POST_ID, flush=True)
    return True

def main():
    if os.getenv("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("stage_requires_main_branch")
    now = datetime.now(timezone.utc)
    if now >= datetime(2026, 11, 7, 14, 0, tzinfo=timezone.utc):
        raise RuntimeError("11h_slot_already_passed_do_not_backdate")
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("pull", "--ff-only", "origin", "main")
    queue = read_document(QUEUE)
    if any(x["id"] == POST_ID for x in queue["posts"]):
        print("ALREADY_QUEUED_NO_RETRY", flush=True)
        return 0
    if POST_ID in validate_state(read_document(LEDGER))["items"]:
        raise RuntimeError("existing_publishing_claim")
    verify_meta_destination()
    package = download_exact_zip(fetch_access_token())
    images = verified_jpegs(package)
    DEST.mkdir(parents=True, exist_ok=True)
    for filename, data, _ in images:
        (DEST / filename).write_bytes(data)
    (DEST / "SOURCE.json").write_text(json.dumps({
        "drive_zip_id": SOURCE_DRIVE_FILE,
        "source_zip_sha256": SOURCE_ZIP_SHA,
        "schedule_time": DUE_AT,
        "status": "media_staged_not_published",
        "media": [{"file": name, "sha256": digest} for name, _, digest in images]
    }, indent=2)+"\n", encoding="utf-8")
    git("add", "--", str(DEST))
    git("commit", "-m", "media(instagram): stage 5 exact owner-approved 07nov vintage panels")
    git("push", "origin", "HEAD:main")
    pinned = git("rev-parse", "HEAD")
    for filename, data, digest in images:
        url = f"https://raw.githubusercontent.com/{REPO}/{pinned}/{DEST.as_posix()}/{filename}"
        for attempt in range(8):
            try:
                with urlopen(Request(url, headers={"User-Agent": "TUE-Meta-Preflight/1.0"}), timeout=20) as response:
                    actual = response.read(2_000_000)
                if sha(actual) == digest:
                    break
            except (HTTPError, URLError, TimeoutError):
                pass
            if attempt == 7:
                raise RuntimeError("public_media_not_verified:" + filename)
            time.sleep(5)
        print("PUBLIC_MEDIA_VERIFIED=" + filename, flush=True)
    # Stage commit hash may become outdated if other pushes run: use exact pinned one.
    # The workflow itself has just staged images: git pull again before queue mutation;
    # keep pinned URLs to the staged commit.
    git("pull", "--ff-only", "origin", "main")
    manifest = read_document(QUEUE)
    if any(x["id"] == POST_ID for x in manifest["posts"]):
        print("ALREADY_QUEUED", flush=True)
        return 0
    if any(x.get("due_at")==DUE_AT and x.get("approved") for x in manifest["posts"]):
        raise RuntimeError("first_slot_booked_after_staging")
    item = {
        "id": POST_ID, "due_at": DUE_AT, "username":"temumaexplicacao",
        "kind":"carousel", "target_url":"https://www.instagram.com/temumaexplicacao/",
        "title":"A cadeira pediu demissão — RH do Caos", "caption":CAPTION,
        "media_urls":[f"https://raw.githubusercontent.com/{REPO}/{pinned}/{DEST.as_posix()}/{name}" for name, _, _ in images],
        "media_sha256":[digest for _, _, digest in images],
        "approved":True, "ai_origin":"synthetic",
        "content_style":"clearly_illustrated",
        "ai_disclosure_review":"no_mandatory_self_disclosure_for_stylized_still",
        "distribution_mode":"api_carousel_without_native_music",
        "owner_authorized_without_music":True,
        "approval_note":"Proprietário aprovou em 07/11/2026 as cinco artes corrigidas e mandou agendar como primeiro post do dia."
    }
    manifest["posts"].append(item)
    manifest["posts"] = validate_manifest(manifest)
    QUEUE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    git("add","--",str(QUEUE))
    git("commit","-m","schedule(instagram): tirinha vintage 07nov 11h via Meta")
    git("push","origin","HEAD:main")
    print("GITHUB_QUEUE_CONFIRMED=2026-11-07T11:00:00-03:00", flush=True)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("07NOV_STAGE_BLOCKED="+type(e).__name__+":"+str(e), file=sys.stderr, flush=True)
        sys.exit(1)

#!/usr/bin/env python3
"""Audit the GitHub-only ability to edit native audio on an EXISTING carousel.

Does NOT log into Instagram, publish, edit, invoke mobile private APIs, or
modify the ledger. Read-only proof of the exact existing post and selected
soundtrack, with a clearly-blocked implementation status.

Only a documented, tested platform edit endpoint could unblock this contract.
Do not infer that an in-app Edit button means Graph API edit support.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from instagram_mobile_music import load_music_assignments, select_pending
from instagram_queue import QueueError, read_document, validate_manifest, validate_state

ID = "halloween-2026-10-31-historia-8-laminas"
MEDIA_ID = "18107496023215107"
PERMALINK = "https://www.instagram.com/p/DfNVlLDmC8P/"
TRACK = "Thriller"
ARTIST = "Michael Jackson"

def audit() -> dict:
    manifest = read_document(ROOT / "content/schedule.json")
    ledger = read_document(ROOT / "content/publication-state.json")
    albums = validate_manifest(manifest)
    state = validate_state(ledger)
    assignment = load_music_assignments().get(ID)
    if not isinstance(assignment, dict):
        raise QueueError("A atribuição musical de Halloween não foi localizada.")
    post = next((p for p in albums if p["id"] == ID), None)
    if not post or not post["approved"] or post["kind"] != "carousel":
        raise QueueError("O carrossel aprovado de Halloween não está íntegro.")
    if len(post["media_urls"]) != 8:
        raise QueueError("A quantidade de artes aprovadas mudou inesperadamente.")
    receipt = state["items"].get(ID)
    if not isinstance(receipt, dict):
        raise QueueError("Recibo de publicação ausente. Nenhuma republicação será feita.")
    if (receipt.get("media_id") != MEDIA_ID or receipt.get("permalink") != PERMALINK
            or assignment.get("track") != TRACK or assignment.get("artist") != ARTIST
            or assignment.get("media_id") != MEDIA_ID or assignment.get("permalink") != PERMALINK
            or assignment.get("approved_by_owner") is not True):
        raise QueueError("O recibo e a música aprovada não correspondem ao mesmo post.")
    status = receipt["status"]
    if status == "awaiting_native_music":
        pending = select_pending(manifest, ledger, ID)
        if pending["track"] != TRACK or pending["artist"] != ARTIST:
            raise QueueError("Fila e aprovação musical divergem.")
    elif status != "published":
        raise QueueError("Estado inesperado para carrossel existente.")
    # As of this implementation, documented official Graph endpoints provide
    # creation-time media/audio operations but no native sound update for an
    # already-published carousel. Instagrapi's documented media_edit edits
    # caption/location/tags, not native audio. A runner is not an Android app.
    return {
        "ok": True,
        "mode": "github_only_read_only",
        "post_id": ID,
        "media_id": MEDIA_ID,
        "permalink": PERMALINK,
        "images_preserved": 8,
        "approved_track": TRACK,
        "approved_artist": ARTIST,
        "ledger_status": status,
        "official_graph_native_audio_edit_supported": False,
        "documented_instagrapi_existing_carousel_audio_edit_supported": False,
        "mobile_instagram_authenticated_in_this_runner": False,
        "cloud_audio_edit_attempted": False,
        "new_post_created": False,
        "result": "blocked_no_documented_existing_post_audio_edit_endpoint",
        "note": "Do not mark music applied based on a successful CI run.",
    }

def main() -> int:
    try:
        result = audit()
    except (QueueError, ValueError, KeyError) as exc:
        print(json.dumps({"ok": False, "mode": "read_only", "error": str(exc)},
                         ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    summary = __import__("os").environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Música no Halloween — checagem sem publicação\n\n")
            f.write("- Post preservado: "+PERMALINK+"\n")
            f.write("- Música aprovada: **Thriller — Michael Jackson**\n")
            f.write("- Recibo: `"+status_mark(result["ledger_status"])+"`\n")
            f.write("- **Edição de áudio pelo GitHub: BLOQUEADA**, sem endpoint documentado\n")
            f.write("- Nenhuma publicação nova e nenhuma edição efetuada\n")
    return 0

def status_mark(value: str) -> str:
    return value if value in ("published","awaiting_native_music") else "unknown"

if __name__ == "__main__":
    raise SystemExit(main())

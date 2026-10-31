#!/usr/bin/env python3
"""Validate and install the immutable 31 Oct–6 Nov 2026 Instagram media package.

This module NEVER approves, schedules automatically, or publishes Instagram items.
Called by the one-shot GitHub Actions import workflow, in two phases.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "content/uploads/instagram-tue-semana-2026-10-31-06nov.zip"
MEDIA_DIR = ROOT / "content/media/semana-2026-10-31-final"
SCHEDULE = ROOT / "content/schedule.json"
LEDGER = ROOT / "content/publication-state.json"
REPO = "gabrielslinhares12-sudo/instagram-skills"
NAMES = {
    "halloween": "lumino-halloween-2026",
    "votos": "lumino-votos-2026",
    "dolar": "lumino-dolar-2026",
    "oncas": "lumino-oncas-2026",
    "enem": "lumino-enem-2026",
    "foguete": "lumino-foguete-2026",
    "lua": "lumino-lua-2026",
}
EXPECTED_COUNTS = {
    "halloween": 1, "votos": 8, "dolar": 8,
    "oncas": 7, "enem": 1, "foguete": 1, "lua": 1,
}


def verify_zip():
    if not PACKAGE.is_file() or PACKAGE.stat().st_size > 25_000_000:
        raise ValueError("Missing package or unexpectedly large archive")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger.get("items"):
        raise ValueError("Publication ledger is not empty; refuse to overwrite claimed/published media")
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    posts = {p["id"]: p for p in schedule["posts"]}
    if set(posts) != set(NAMES.values()) or any(p["approved"] for p in posts.values()):
        raise ValueError("Unexpected scheduled posts or existing approvals")
    result = {}
    with zipfile.ZipFile(PACKAGE) as z:
        manifest = json.loads(z.read("manifesto-arquivos.json"))
        if manifest.get("version") != 1 or len(manifest.get("items", [])) != 7:
            raise ValueError("Unexpected package manifest")
        if set(p["id"] for p in manifest["items"]) != set(NAMES):
            raise ValueError("Missing, duplicate or unknown package item")
        for item in manifest["items"]:
            slug = item["id"]
            files = item["files"]
            if len(files) != EXPECTED_COUNTS[slug]:
                raise ValueError("Wrong media count for " + slug)
            encoded = []
            folder = None
            for asset in files:
                source = asset["file"]
                if (source.startswith("/") or ".." in Path(source).parts
                        or Path(source).suffix.lower() not in {".jpg", ".mp4"}):
                    raise ValueError("Invalid archive media path")
                source_folder = source.split("/", 1)[0]
                if folder is None:
                    folder = source_folder
                elif folder != source_folder:
                    raise ValueError("Mixed folders in one item")
                raw = z.read(source)
                if (len(raw) != asset["bytes"] or
                        hashlib.sha256(raw).hexdigest() != asset["sha256"]):
                    raise ValueError("Checksum/size mismatch for " + source)
                suffix = Path(source).suffix.lower()
                if suffix == ".jpg" and not raw.startswith(b"\xff\xd8\xff"):
                    raise ValueError("Invalid JPEG header")
                if suffix == ".mp4" and raw[4:8] != b"ftyp":
                    raise ValueError("Invalid MP4 header")
                relative = f"{slug}/{Path(source).name}"
                encoded.append((relative, raw, asset["sha256"]))
            caption_name = f"{folder}/legenda.txt"
            caption = z.read(caption_name).decode("utf-8").strip()
            if not (1 <= len(caption) <= 2200):
                raise ValueError("Missing/invalid caption for " + slug)
            result[slug] = (encoded, caption)
    assert sum(len(v[0]) for v in result.values()) == 27
    return result, schedule


def extract():
    result, _ = verify_zip()
    for assets, _caption in result.values():
        for relative, raw, _sha in assets:
            output = MEDIA_DIR / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists() and output.read_bytes() != raw:
                raise ValueError("Conflicting existing media: " + str(output))
            output.write_bytes(raw)
    print("Validated and extracted", sum(len(a) for a, _ in result.values()), "media files")


def finalize(media_commit):
    if not re.fullmatch(r"[0-9a-f]{40}", media_commit):
        raise ValueError("Media commit SHA missing or invalid")
    result, schedule = verify_zip()
    for post in schedule["posts"]:
        slug = post["id"][len("lumino-"):-len("-2026")]
        assets, caption = result[slug]
        for relative, _raw, expected_sha in assets:
            on_disk = MEDIA_DIR / relative
            if not on_disk.is_file() or hashlib.sha256(on_disk.read_bytes()).hexdigest() != expected_sha:
                raise ValueError("Committed media missing or modified: " + relative)
        post["caption"] = caption
        post["media_urls"] = [
            "https://raw.githubusercontent.com/" + REPO + "/" + media_commit
            + "/content/media/semana-2026-10-31-final/" + relative
            for relative, _, _ in assets
        ]
        post["media_sha256"] = [sha for _, _, sha in assets]
        post["approved"] = False
        post["approval_note"] = (
            "27 mídias finais importadas e verificadas por SHA256. "
            "Publicação e agendamento NÃO ativados; aguarda revisão e acionamento manual. "
            "Mídia fixa no commit " + media_commit
        )
    schedule["approval_note"] = (
        "Pacote da semana importado para GitHub. URLs finais com SHA imutável, "
        "todos approved=false. Nenhum workflow de verificação recorrente habilitado."
    )
    SCHEDULE.write_text(
        json.dumps(schedule, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Prepared immutable URLs for 27 files; approved stays false")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("extract", "finalize"))
    parser.add_argument("--media-commit", default="")
    a = parser.parse_args()
    try:
        if a.phase == "extract":
            extract()
        else:
            finalize(a.media_commit)
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as e:
        print("IMPORT FAILED:", e, file=sys.stderr)
        sys.exit(1)

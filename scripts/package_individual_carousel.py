#!/usr/bin/env python3
"""Package EIGHT already art-directed JPGs without repainting or changing their content.

The approved reference is a creative guide, not something a generic compositor
can reproduce. This script accepts finished artwork only. The contact sheet is
ALWAYS derived from the exact eight deliverable files.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image

from instagram_visual_standard import (
    ROOT, SAFE_ID, VisualError, safe_file, sha256, validate_package, verify_brand
)

MODE = "individually_art_directed_v1"
THUMB = (216, 270)


def build_preview(folder: Path, pages: list[dict]) -> Image.Image:
    """Deterministic 4x2 contact sheet using final JPEG pixels only."""
    image = Image.new("RGB", (4 * THUMB[0], 2 * THUMB[1]))
    for idx, page in enumerate(pages):
        file = safe_file(folder, page["file"])
        with Image.open(file) as original:
            tile = original.convert("RGB").resize(THUMB, Image.Resampling.LANCZOS)
        image.paste(tile, ((idx % 4) * THUMB[0], (idx // 4) * THUMB[1]))
    return image


def dhash(image: Image.Image) -> int:
    """A low-cost near-duplicate warning, not a substitute for visual review."""
    gray = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    px = list(gray.getdata())
    value = 0
    for row in range(8):
        for col in range(8):
            value = (value << 1) | int(px[row * 9 + col] > px[row * 9 + col + 1])
    return value


def package(spec_path: Path, out: Path) -> dict:
    brand = verify_brand()
    spec_path = spec_path.resolve()
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    post_id = data.get("post_id")
    if not isinstance(post_id, str) or not SAFE_ID.fullmatch(post_id):
        raise VisualError("ID de carrossel inválido.")
    source = spec_path.parent
    out = out.resolve()
    if out == source or out.is_relative_to(source):
        raise VisualError("A saída deve ficar fora da pasta de artes de entrada.")
    items = data.get("slides")
    if not isinstance(items, list) or len(items) != 8:
        raise VisualError("São obrigatórias oito artes finais individuais.")
    if out.exists() and list(out.iterdir()):
        raise VisualError("Saída deve estar vazia para não reaproveitar rascunhos.")
    out.mkdir(parents=True, exist_ok=True)

    pages: list[dict] = []
    fingerprints: list[int] = []
    for number, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise VisualError("Arte deve ser especificada por objeto.")
        required = ("file", "headline", "mascot_box", "credit", "layout")
        if any(not item.get(field) for field in required):
            raise VisualError(f"Página {number}: dados de arte incompletos.")
        src = safe_file(source, item["file"])
        if src.suffix.lower() not in {".jpg", ".jpeg"} or not src.is_file():
            raise VisualError(f"Página {number}: somente JPG individual pronto.")
        with Image.open(src) as original:
            if original.format != "JPEG" or original.size != (1080, 1350):
                raise VisualError(f"Página {number}: JPG deve ser exatamente 1080x1350.")
            fingerprint = dhash(original)
        if any((fingerprint ^ seen).bit_count() <= 3 for seen in fingerprints):
            raise VisualError(f"Página {number}: arte duplicada ou quase idêntica.")
        fingerprints.append(fingerprint)
        dest = out / f"{number:02d}.jpg"
        shutil.copyfile(src, dest)  # bytes are preserved; absolutely NO re-render
        original_sha = sha256(src)
        if sha256(dest) != original_sha:
            raise VisualError(f"Página {number}: montagem alterou a arte.")
        pages.append({
            "number": number, "file": dest.name, "sha256": original_sha,
            "source_sha256": original_sha,
            "headline": item["headline"], "layout": item["layout"],
            "mascot_box": item["mascot_box"],
            "background_credit": item["credit"],
            "background_type": item.get("background_type", "illustration"),
            "visual_notes": item.get("visual_notes", ""),
        })

    preview_name = "PREVIA-8-ARTES.png"
    preview_file = out / preview_name
    build_preview(out, pages).save(preview_file, format="PNG")
    manifest = {
        "version": 1,
        "production_mode": MODE,
        "standard_id": brand["id"],
        "reference_sha256": brand["reference"]["sha256"],
        "lumino_sha256": brand["lumino"]["sha256"],
        "post_id": post_id,
        "approved": False,
        "visual_reviewed": False,
        "owner_authorized": False,
        "preview_file": preview_name,
        "preview_sha256": sha256(preview_file),
        "pages": pages,
    }
    manifest_path = out / "visual-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return validate_package(manifest_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.spec, args.out), ensure_ascii=False))
        return 0
    except (VisualError, OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

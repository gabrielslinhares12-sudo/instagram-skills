#!/usr/bin/env python3
"""TUE-MESTRE-01: reject final exports that silently redesign approved artwork.

Compare the full approved raster with the Instagram export after scaling the
export back to approved size. Resize/color conversion passes; substantial
layout reconstruction fails. This is a guard, NOT proof of artistic quality.
Run on actual image files *before* any publishing authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageStat


class VisualFidelityError(ValueError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_final(approved_path: Path, final_path: Path, expected_sha: str,
                 max_changed_fraction: float = 0.12,
                 pixel_threshold: int = 35) -> dict:
    if not expected_sha or len(expected_sha) != 64 or sha256(approved_path) != expected_sha.lower():
        raise VisualFidelityError("SHA-256 da arte mestre aprovada ausente ou diferente.")
    if not (0 <= max_changed_fraction <= 0.12):
        raise VisualFidelityError("Não é permitido aumentar o limite padrão de alteração silenciosa.")
    if pixel_threshold != 35:
        raise VisualFidelityError("Limiar de comparação imutável: 35.")
    with Image.open(approved_path) as im:
        reference = im.convert("RGB")
    with Image.open(final_path) as im:
        delivered = im.convert("RGB")
    ra = reference.width / reference.height
    rb = delivered.width / delivered.height
    if abs(ra - rb) > 0.005:
        raise VisualFidelityError("A arte final foi cortada ou mudou de proporção.")
    delivered = delivered.resize(reference.size, Image.Resampling.LANCZOS)
    delta = ImageChops.difference(reference, delivered)
    channels = delta.split()
    peak = ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]), channels[2])
    changed = peak.point(lambda px: 255 if px > pixel_threshold else 0)
    changed_fraction = ImageStat.Stat(changed).mean[0] / 255.0
    avg_absolute_difference = sum(ImageStat.Stat(delta).mean) / 3.0
    report = {
        "preset": "TUE-MESTRE-01",
        "approved_sha256": expected_sha.lower(),
        "approved_resolution": list(reference.size),
        "final_resolution": list(delivered.size),
        "fraction_visibly_changed": round(changed_fraction, 5),
        "mean_absolute_channel_change": round(avg_absolute_difference, 3),
        "max_allowed_fraction": max_changed_fraction,
        "human_visual_approval_still_required": True,
    }
    if changed_fraction > max_changed_fraction:
        raise VisualFidelityError(
            "FINAL REPROVADO: {:.1%} dos pixels mudaram visualmente contra o mestre aprovado. "
            "É proibido reconstruir a composição por crops, tarjas e fundos chapados; "
            "entregue o master preservado ou obtenha aprovação explícita de uma nova imagem."
            .format(changed_fraction)
        )
    report["ok"] = True
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--approved", required=True, type=Path,
                   help="Imagem INTEIRA que foi aprovada, não um layout de referência")
    p.add_argument("--final", required=True, type=Path,
                   help="Arquivo efetivamente entregue ao Instagram")
    p.add_argument("--expected-sha", required=True,
                   help="SHA-256 imutável da arte inteira aprovada")
    args = p.parse_args()
    try:
        print(json.dumps(verify_final(args.approved, args.final, args.expected_sha), ensure_ascii=False))
        return 0
    except (VisualFidelityError, OSError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

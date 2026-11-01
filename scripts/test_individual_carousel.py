#!/usr/bin/env python3
"""Regression tests for the eight-independent-pages pipeline (no network)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from instagram_visual_standard import VisualError, sha256, verify_preview
from package_individual_carousel import build_preview, package


class IndividualCarouselTests(unittest.TestCase):
    def test_preview_contains_pixels_from_final_art_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            pages = []
            for i in range(1, 9):
                name = f"{i:02d}.jpg"
                Image.new("RGB", (1080, 1350), (i * 20, 50, 100)).save(folder / name)
                pages.append({"file": name, "number": i})
            img = build_preview(folder, pages)
            self.assertEqual(img.size, (864, 540))
            preview = folder / "PREVIA-8-ARTES.png"
            img.save(preview)
            data = {"preview_file": preview.name, "preview_sha256": sha256(preview), "pages": pages}
            verify_preview(folder, data)
            with Image.open(preview) as opened:
                edited = opened.convert("RGB")
            edited.putpixel((4, 4), (250, 250, 250))
            edited.save(preview)
            data["preview_sha256"] = sha256(preview)
            with self.assertRaisesRegex(VisualError, "não corresponde"):
                verify_preview(folder, data)

    def test_rejects_collage_instead_of_eight_individual_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            spec = base / "input" / "brief.json"
            spec.parent.mkdir()
            spec.write_text(json.dumps({"post_id": "teste", "slides": [{"file": "sheet.jpg"}]}),
                            encoding="utf-8")
            with patch("package_individual_carousel.verify_brand", return_value={"id": "test"}):
                with self.assertRaisesRegex(VisualError, "oito artes"):
                    package(spec, base / "output")

    def test_outdated_template_is_not_an_independent_authoring_method(self):
        from render_instagram_carrossel import ROOT
        source = (ROOT / "scripts/render_instagram_carrossel.py").read_text(encoding="utf-8")
        self.assertIn('"production_mode":"generic_template_draft_only"', source)
        from instagram_visual_standard import INDIVIDUAL_MODE, LEGACY_MODE
        self.assertNotEqual(INDIVIDUAL_MODE, LEGACY_MODE)

    def test_duplicate_previews_dont_count_as_eight_variations(self):
        from package_individual_carousel import dhash
        sample = Image.new("RGB", (1080, 1350), "white")
        self.assertEqual(dhash(sample), dhash(sample.copy()))


if __name__ == "__main__":
    unittest.main()

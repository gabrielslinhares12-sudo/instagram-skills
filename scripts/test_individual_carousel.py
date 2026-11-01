#!/usr/bin/env python3
"""Regression tests for variable-length independent carousel art."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from instagram_visual_standard import VisualError, preview_geometry, sha256, verify_preview
from package_individual_carousel import build_preview, package, dhash


class IndividualCarouselTests(unittest.TestCase):
    def test_variable_length_preview_only_uses_final_jpg_pixels(self):
        for count in (2, 3, 5, 8, 10, 12, 16, 20):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp)
                pages = []
                for i in range(1, count+1):
                    name = f"{i:02d}.jpg"
                    Image.new("RGB", (1080, 1350), (i * 10, 40, 90)).save(folder / name)
                    pages.append({"file": name, "number": i})
                cols, rows, width, height = preview_geometry(count)
                self.assertEqual((width, height), (cols * 216, rows * 270))
                img = build_preview(folder, pages)
                self.assertEqual(img.size, (width, height))
                path = folder / f"PREVIA-{count:02d}-ARTES.png"
                img.save(path)
                data = {"preview_file": path.name, "preview_sha256": sha256(path), "pages": pages}
                verify_preview(folder, data)
                altered = img.copy()
                altered.putpixel((4, 4), (250, 250, 250))
                altered.save(path)
                data["preview_sha256"] = sha256(path)
                with self.assertRaisesRegex(VisualError, "não corresponde"):
                    verify_preview(folder, data)

    def test_rejects_one_image_or_more_than_twenty(self):
        for count in (1, 21):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                spec = base / "input" / "brief.json"
                spec.parent.mkdir()
                spec.write_text(json.dumps({
                    "post_id":"test", "slides":[{"file":"missing.jpg"}]*count
                }), encoding="utf-8")
                brand={"id":"test","output":{"min_pages":2,"max_pages":20}}
                with patch("package_individual_carousel.verify_brand", return_value=brand):
                    with self.assertRaisesRegex(VisualError, "2 e 20"):
                        package(spec, base / "output")

    def test_music_carousel_cannot_be_silently_posted_by_api(self):
        from instagram_visual_standard import verify_publication_route
        with self.assertRaisesRegex(VisualError, "aplicativo Instagram"):
            verify_publication_route({"distribution_mode": "native_music_carousel"})
        with self.assertRaisesRegex(VisualError, "autorização expressa"):
            verify_publication_route({"distribution_mode": "api_carousel_without_native_music"})
        verify_publication_route({
            "distribution_mode": "api_carousel_without_native_music",
            "owner_authorized_without_music": True,
        })
        with self.assertRaisesRegex(VisualError, "não reconhecido"):
            verify_publication_route({"distribution_mode": "invalid_mode"})

    def test_outdated_template_cannot_publish(self):
        from render_instagram_carrossel import ROOT
        source = (ROOT / "scripts/render_instagram_carrossel.py").read_text(encoding="utf-8")
        self.assertIn('"production_mode":"generic_template_draft_only"', source)
        from instagram_visual_standard import INDIVIDUAL_MODE, LEGACY_MODE
        self.assertNotEqual(INDIVIDUAL_MODE, LEGACY_MODE)

    def test_duplicate_images_rejected_by_fingerprint(self):
        sample = Image.new("RGB", (1080, 1350), "white")
        self.assertEqual(dhash(sample), dhash(sample.copy()))


if __name__ == "__main__":
    unittest.main()

"""TUE-MESTRE-01 tests: export must preserve the actual approved visual."""
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageDraw
from instagram_preserve_approved_art import verify_final, VisualFidelityError


class ApprovedArtPreservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.approved = self.root / "approved.png"
        self.final = self.root / "final.jpg"
        source = Image.new("RGB", (400, 500), "#f8ecd8")
        draw = ImageDraw.Draw(source)
        draw.rectangle((10, 60, 390, 175), fill="#ffd600")
        draw.rectangle((12, 200, 388, 455), fill="#15223b")
        draw.ellipse((55, 235, 245, 430), fill="#e0a525")
        draw.ellipse((290, 240, 360, 305), fill="#00d8ff")
        source.save(self.approved)
        self.sha = hashlib.sha256(self.approved.read_bytes()).hexdigest()

    def test_proportional_resize_keeps_approved_art(self):
        with Image.open(self.approved) as im:
            im.resize((1200,1500), Image.Resampling.LANCZOS).save(self.final, quality=96)
        report = verify_final(self.approved, self.final, self.sha)
        self.assertTrue(report["ok"])
        self.assertLess(report["fraction_visibly_changed"], 0.12)

    def test_flat_recreation_rejected_even_at_4k(self):
        substitute = Image.new("RGB",(1600,2000),"#f8ecd8")
        d=ImageDraw.Draw(substitute)
        d.rectangle((60,80,1540,450),fill="#ffd600")
        d.rectangle((60,500,1540,1000),fill="#18213a")
        d.rectangle((60,1020,1540,1900),fill="#60354b")
        substitute.save(self.final)
        with self.assertRaisesRegex(VisualFidelityError,"REPROVADO"):
            verify_final(self.approved,self.final,self.sha)

    def test_approved_master_sha_cannot_be_changed(self):
        with Image.open(self.approved) as im:
            im.save(self.final)
        with self.assertRaisesRegex(VisualFidelityError,"SHA-256"):
            verify_final(self.approved,self.final,"0"*64)

    def test_different_crop_aspect_is_rejected(self):
        with Image.open(self.approved) as im:
            im.resize((1200,1200)).save(self.final)
        with self.assertRaisesRegex(VisualFidelityError,"proporção"):
            verify_final(self.approved,self.final,self.sha)

    def test_cannot_relax_limit_to_approve_rebuild(self):
        with Image.open(self.approved) as im:
            im.save(self.final)
        with self.assertRaisesRegex(VisualFidelityError,"aumentar"):
            verify_final(self.approved,self.final,self.sha,max_changed_fraction=0.8)


if __name__=="__main__":
    unittest.main()

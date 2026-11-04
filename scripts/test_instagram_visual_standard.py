#!/usr/bin/env python3
"""Testes offline: o template bloqueia alteracoes de marca e mascote."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw
from instagram_visual_standard import ROOT, VisualError, verify_brand, validate_package, audit_queue, verify_reel_release, verify_visible_progress_dots, sha256
from render_instagram_carrossel import render

class ReelReleaseTests(unittest.TestCase):
    def test_original_reel_requires_immutable_source_qc_and_ai_info(self):
        slug = "tue-2026-11-04-18-defesa-civil-alerta"
        receipt = json.loads(
            (ROOT / "content/approved" / slug / "approval.json").read_text(encoding="utf-8"))
        post = {"id": slug, "kind": "reel", "media_urls": [receipt["release_url"]],
                "media_sha256": list(receipt["media_sha256"]), "cover_url": receipt["cover_url"],
                "ai_origin": "synthetic", "is_ai_generated": True,
                "ai_disclosure_review": "mandatory_realistic_synthetic_audio"}
        self.assertEqual(verify_reel_release(ROOT, post), slug)
        for changes in (
            {"media_sha256": ["0" * 64]},
            {"media_urls": [receipt["release_url"].replace(
                receipt["technical_provenance"]["media_immutable_commit"],
                "instagram-reel-defesa-civil-04nov-2026")]},
            {"ai_origin": "verified_non_synthetic"},
            {"is_ai_generated": False},
            {"ai_disclosure_review": "optional"},
            {"cover_url": receipt["cover_url"].replace(".jpg", ".png")},
        ):
            with self.subTest(changes=changes), self.assertRaises(VisualError):
                verify_reel_release(ROOT, {**post, **changes})


class ProgressDotsTests(unittest.TestCase):
    @staticmethod
    def draw_footer(count, active, missing=None):
        im=Image.new("RGB",(1080,1350),(247,243,235))
        draw=ImageDraw.Draw(im)
        for j in range(1,count+1):
            if j==missing:
                continue
            x=round(534+(j-1-(count-1)/2)*31)
            rgb=(255,214,0) if j==active else (192,194,195)
            draw.ellipse((x-8,1267,x+8,1283),fill=rgb)
        return im

    def test_correct_progress_for_any_allowed_carousel_length(self):
        for length in (2,3,4,5,8,10,20):
            for current in range(1,length+1):
                with self.subTest(length=length,active=current):
                    verify_visible_progress_dots(
                        self.draw_footer(length,current),current,length)

    def test_catches_wrong_active_dot_and_missing_dot(self):
        with self.assertRaisesRegex(VisualError,"ponto 1"):
            verify_visible_progress_dots(self.draw_footer(5,3),1,5)
        with self.assertRaisesRegex(VisualError,"ausente"):
            verify_visible_progress_dots(self.draw_footer(5,2,missing=4),2,5)

    def test_catches_extra_yellow_on_inactive_dot(self):
        im=self.draw_footer(5,1)
        d=ImageDraw.Draw(im)
        x=round(534+(2-(5-1)/2)*31)
        d.ellipse((x-8,1267,x+8,1283),fill=(255,214,0))
        with self.assertRaisesRegex(VisualError,"cor incorreta"):
            verify_visible_progress_dots(im,1,5)


class BrandTests(unittest.TestCase):
    def test_canonical_assets_unchanged(self):
        cfg=verify_brand()
        self.assertEqual(cfg["lumino"]["sha256"],
                         "f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b")
        self.assertEqual(cfg["editorial_standard"]["id"], "TUE-MESTRE-01")
        self.assertNotIn("reference", cfg)
        master = cfg["visual_master"]
        self.assertEqual(master["path"], "content/brand/REFERENCIA-VISUAL-OFICIAL-TUE-MESTRE-01-02NOV2026.jpg")
        self.assertEqual(master["sha256"], "571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9")
        self.assertEqual(cfg["design"]["swipe_cue_display_text"], "ARRASTE PARA O LADO →")
        self.assertTrue(cfg["design"]["footer_dots"])

    def test_existing_queue_cannot_autoapprove(self):
        result=audit_queue()
        self.assertTrue(result["ok"])

    def test_new_approval_without_owner_record_is_blocked(self):
        # A mere approved=true in schedule may not bypass the user's sign-off.
        from unittest.mock import patch
        import instagram_visual_standard as standard
        original_read=standard.read_json
        schedule=original_read(standard.ROOT/"content/schedule.json")
        fake=json.loads(json.dumps(schedule))
        fake["posts"].append({
            "id":"qa-approved-without-review",
            "due_at":"2026-11-05T21:00:00Z",
            "kind":"carousel",
            "approved":True,
            "media_urls":[],
            "media_sha256":[]
        })
        def fake_read(path):
            if Path(path)==standard.ROOT/"content/schedule.json":
                return fake
            return original_read(path)
        with patch.object(standard,"read_json",side_effect=fake_read):
            with self.assertRaisesRegex(VisualError,"sem verificacao"):
                audit_queue()

    def test_renderer_cannot_grant_approval(self):
        # Every newly rendered package starts as a draft.
        import render_instagram_carrossel as generator
        self.assertIn('"approved":False', Path(generator.__file__).read_text(encoding="utf-8").replace(" ", ""))

    def test_legacy_generic_renderer_is_rejected_by_current_master(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)
            slides=[]
            for i in range(8):
                for suff in ("a","b"):
                    im=Image.new("RGB",(900,800),(70+i*8+(20 if suff=="b" else 0),110+i*9,125+i*5))
                    draw=ImageDraw.Draw(im)
                    draw.ellipse((40+i*5,40,750,750),fill=(125+i*6,140+i*7,90+i*3))
                    im.save(path/f"{i}-{suff}.jpg")
                slides.append({"headline":f"PÁGINA {i+1} EXPLICAÇÃO",
                               "body":"Uma informacao confirmada de cada vez. A imagem ilustra o conceito sem alterar o mascote.",
                               "callout":"LEIA E COMPARTILHE",
                               "photo":f"{i}-a.jpg","photo_secondary":f"{i}-b.jpg",
                               "credit":"Ilustracao local de teste",
                               "layout":["hero","split","diagram"][i%3]})
            spec=path/"input.json"
            spec.write_text(json.dumps({"post_id":"qa-teste","slides":slides},ensure_ascii=False),encoding="utf-8")
            out=path/"produced"
            # The former 8-panel generic renderer is prohibited by the
            # current master art. It must FAIL, never become a publishable
            # package merely because its mascot checksum is correct.
            with self.assertRaisesRegex(VisualError, "falta faixa amarela"):
                render(spec,out)

if __name__=="__main__":unittest.main()

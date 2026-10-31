#!/usr/bin/env python3
"""Testes offline: o template bloqueia alteracoes de marca e mascote."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw
from instagram_visual_standard import ROOT, VisualError, verify_brand, validate_package, audit_queue, sha256
from render_instagram_carrossel import render

class BrandTests(unittest.TestCase):
    def test_canonical_assets_unchanged(self):
        cfg=verify_brand()
        self.assertEqual(cfg["lumino"]["sha256"],
                         "f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b")
        self.assertEqual(cfg["reference"]["sha256"],
                         "6d3dcdebcea7006b4f1934e74c19618951453b000aea9deb6968add55d5f0e63")

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

    def test_rendered_page_passes_and_replacement_fails(self):
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
            result=render(spec,out)
            self.assertTrue(result["ok"])
            manifest=out/"visual-manifest.json"
            page=out/"01.jpg"
            # Alterar o personagem e tentar forjar um novo SHA nao passa na analise visual.
            with Image.open(page) as im:
                im=im.convert("RGB")
                ImageDraw.Draw(im).rectangle((18,973,290,1257),fill=(20,20,20))
                im.save(page,format="JPEG",quality=96)
            data=json.loads(manifest.read_text(encoding="utf-8"))
            data["pages"][0]["sha256"]=sha256(page)
            manifest.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaisesRegex(VisualError,"Lumino"):
                validate_package(manifest)

if __name__=="__main__":unittest.main()

#!/usr/bin/env python3
"""Prepare actual JPEG media hosted at public raw.githubusercontent.com for Meta API.

Only renders from the existing complete approved art; does not rebuild the
artwork, add labels, create a queue entry or publish.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageCms

ROOT=Path(__file__).resolve().parent.parent
DIR=ROOT/"content/media/instagram/2026-11-02"
SOURCES=[
    "TUE-02NOV-MAR-CRUZADO-01.png",
    "TUE-02NOV-MAR-CRUZADO-02.png",
    "TUE-02NOV-MAR-CRUZADO-03.png",
    "TUE-02NOV-MAR-CRUZADO-04.png",
    "TUE-02NOV-MAR-CRUZADO-05.png",
    "TUE-02NOV-15H-SAC-SENHA-IMPOSSIVEL.png",
]
BASE="https://raw.githubusercontent.com/gabrielslinhares12-sudo/instagram-skills/main/content/media/instagram/2026-11-02/"
MAX_BYTES=8_000_000

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare()->dict:
    result=[]
    for name in SOURCES:
        src=DIR/name
        if not src.is_file():
            raise RuntimeError("Missing required approved source: "+name)
        target=src.with_suffix(".jpg")
        with Image.open(src) as base:
            base.load()
            if base.format!="PNG":
                raise RuntimeError("Expected original PNG: "+name)
            if base.width < 1080 or base.height < 1350:
                raise RuntimeError("Original image resolution too small: "+name)
            ratio=base.width/base.height
            if abs(ratio-4/5)>0.004:
                raise RuntimeError("Unexpected crop/aspect ratio for "+name)
            if "icc_profile" in base.info:
                try:
                    rgb=ImageCms.profileToProfile(base, ImageCms.ImageCmsProfile(
                        __import__("io").BytesIO(base.info["icc_profile"])),
                        ImageCms.createProfile("sRGB"), outputMode="RGB")
                except (ValueError, OSError):
                    raise RuntimeError("Cannot safely convert ICC profile for "+name) from None
            elif base.mode=="RGBA":
                rgb=Image.new("RGB",base.size,(255,255,255))
                rgb.paste(base,mask=base.getchannel("A"))
            else:
                rgb=base.convert("RGB")
            # Negligible 0.03% geometric adjustment; no recropping, new text or scene.
            rgb=rgb.resize((1080,1350),resample=Image.Resampling.LANCZOS)
            rgb.save(target,"JPEG",quality=95,subsampling=0,optimize=True)
        with Image.open(target) as jpg:
            if jpg.format!="JPEG" or jpg.size!=(1080,1350):
                raise RuntimeError("JPEG inspection failed for "+name)
        if target.stat().st_size>MAX_BYTES:
            raise RuntimeError("JPEG exceeds Instagram image limit "+name)
        result.append({
            "source_png":name,"source_sha256":sha(src),
            "jpeg_name":target.name,"jpeg_sha256":sha(target),
            "bytes":target.stat().st_size,"width":1080,"height":1350,
            "public_jpeg_url":BASE+target.name
        })
    manifest={
        "kind":"meta_public_media_assets","version":1,
        "date":"2026-11-02","format":"JPEG","source_count":6,
        "publication_status":"NOT_SCHEDULED_NOT_PUBLISHED",
        "review":"Media-hosting only. Artwork, copyright, AI-origin disclosure, account credentials and publishing approval remain separate gates.",
        "files":result,
    }
    (DIR/"meta-media-manifest.json").write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

if __name__=="__main__":
    result=prepare()
    print(json.dumps({"status":"JPEG_ready_for_public_hosting",
                      "count":len(result["files"]),
                      "size":sum(f["bytes"] for f in result["files"])},ensure_ascii=False))

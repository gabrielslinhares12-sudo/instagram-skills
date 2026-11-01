#!/usr/bin/env python3
"""Read-only public-image origin preflight for original Halloween JPEGs.

No Instagram write, login, or publication. Verify bytes, content type, and
original SHA256; this does not prove Meta's own CDN downloader can reach them.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

BASE="https://cdn.jsdelivr.net/gh/gabrielslinhares12-sudo/instagram-skills@f32ed0dae986e38ff058d3ba84f02b6a5c4b94fb/content/media/halloween-2026-10-31/"
POST="halloween-2026-10-31-historia-8-laminas"

def verify():
    queue=json.loads(Path("content/schedule.json").read_text(encoding="utf-8"))
    posts=[p for p in queue.get("posts",[]) if p.get("id")==POST]
    if len(posts)!=1 or posts[0].get("kind")!="carousel" or posts[0].get("approved") is not True:
        raise ValueError("Original Halloween carousel unavailable or unapproved")
    media=posts[0]
    urls,hashes=media["media_urls"],media["media_sha256"]
    if len(urls)!=8 or len(hashes)!=8:
        raise ValueError("Wrong Halloween image count")
    response=[]
    for i in range(1,9):
        url=BASE+f"{i:02d}-historia-halloween.jpg"
        with urlopen(Request(url,headers={"User-Agent":"TUE-ImageOriginCheck/1"}),timeout=20) as r:
            resolved=r.geturl()
            image=r.read(8*1024*1024+1)
            mime=r.headers.get("Content-Type","")
        if (urlsplit(resolved).hostname not in ("cdn.jsdelivr.net","fastly.jsdelivr.net")
            or not mime.lower().startswith("image/jpeg")
            or len(image)>8*1024*1024
            or hashlib.sha256(image).hexdigest()!=hashes[i-1]):
            raise ValueError("CDN source fails exact byte verification")
        response.append({"index":i,"ok":True,"bytes":len(image)})
    return {"ok":True,"mode":"read_only",
            "source":"jsdelivr_version_pinned", "bytes_verified":len(response),
            "files":response,"ready_to_upload":False,
            "verified_to_work_at_Meta":False}

if __name__=="__main__":
    try:print(json.dumps(verify(),ensure_ascii=False))
    except Exception:
        print(json.dumps({"ok":False,"reason":"Alternative host failed public read or byte comparison",
                          "ready_to_upload":False}),file=sys.stderr)
        sys.exit(1)

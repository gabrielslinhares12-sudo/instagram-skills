#!/usr/bin/env python3
"""Odyssey V17: fetch real photogrammetry rock/cliff mesh & PBR materials,
not giant procedural icospheres. Poly Haven public CC0 assets and API.

Asset credit while using the live API: Powered by Poly Haven.
API documentation: https://api.polyhaven.com
CC0 license: https://polyhaven.com/license
This downloads assets, never publishes any animation or uploads private WAV.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, urllib.request, urllib.parse
from urllib.error import HTTPError
ASSETS=("coastal_cliff_01","namaqualand_boulder_03")
ROOT=pathlib.Path("odyssey_185/out/cc0_rocks")
USER_AGENT="TUE-Studio-Odyssey/17 (Powered by Poly Haven; CC0; no paid API)"
def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=40) as response:
        return json.load(response)
def choose_gltf(files,res="1k"):
    gltf=files.get("gltf",{})
    if not gltf:
        raise ValueError("POLYHAVEN_MODEL_MISSING_GLTF")
    for key in (res,"2k","4k","8k"):
        item=gltf.get(key)
        if not item:continue
        if "gltf" in item and "url" in item["gltf"]:return key,item["gltf"]
        if "url" in item:return key,item
    raise ValueError("POLYHAVEN_NO_GLTF_SIZE_AVAILABLE")
def valid_url(url):
    uri=urllib.parse.urlsplit(url)
    if uri.scheme!="https" or not uri.hostname:
        raise ValueError("POLYHAVEN_ASSET_URL_NOT_HTTPS")
    if not (uri.hostname.endswith(".polyhaven.com") or
            uri.hostname in ("polyhaven.com","cdn.polyhaven.com","dl.polyhaven.org","dl.polyhaven.com")):
        raise ValueError("POLYHAVEN_ASSET_DOWNLOAD_UNTRUSTED_HOST")
def fetch_file(fileinfo,path):
    u=fileinfo.get("url")
    if not u:raise ValueError("POLYHAVEN_MISSING_DOWNLOAD_URL")
    valid_url(u)
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise FileExistsError(path)
    request=urllib.request.Request(u,headers={"User-Agent":USER_AGENT})
    hasher=hashlib.md5()
    written=0
    with urllib.request.urlopen(request,timeout=120) as response, path.open("xb") as stream:
        while True:
            chunk=response.read(512*1024)
            if not chunk:break
            written+=len(chunk)
            if written>250*1024*1024:raise RuntimeError("ASSET_TOO_LARGE_ABORT")
            stream.write(chunk);hasher.update(chunk)
    if fileinfo.get("size") and written!=int(fileinfo["size"]):
        path.unlink(missing_ok=True);raise ValueError("ASSET_SIZE_MISMATCH")
    if fileinfo.get("md5") and hasher.hexdigest().lower()!=fileinfo["md5"].lower():
        path.unlink(missing_ok=True);raise ValueError("ASSET_MD5_MISMATCH")
    return {"bytes":written,"md5":hasher.hexdigest(),"path":str(path)}
def download(asset,out,metadata_only=False):
    info=get_json("https://api.polyhaven.com/info/"+asset)
    if info.get("type")!=2:raise RuntimeError("NOT_A_POLYHAVEN_3D_MODEL")
    # The public license page declares Poly Haven assets CC0.
    meta=get_json("https://api.polyhaven.com/files/"+asset)
    size,primary=choose_gltf(meta)
    root=out/asset
    deps=primary.get("include",{})
    if metadata_only:
        print("CC0_ASSET_AVAILABLE",asset,size,primary.get("size"),"dependencies",len(deps))
        return {"asset":asset,"resolution":size,"dependencies":list(deps)}
    name=pathlib.PurePosixPath(urllib.parse.urlsplit(primary["url"]).path).name
    if not name.endswith(".gltf"):raise ValueError("UNEXPECTED_PRIMARY_EXT")
    downloads=[fetch_file(primary,root/name)]
    for relative,entry in deps.items():
        safe=pathlib.PurePosixPath(relative)
        if ".." in safe.parts or safe.is_absolute():raise RuntimeError("UNSAFE_GLTF_DEPENDENCY_PATH")
        downloads.append(fetch_file(entry,root/pathlib.Path(*safe.parts)))
    manifest={"source":"Poly Haven official API","license":"CC0 1.0", "api_credit":"Powered by Poly Haven",
              "asset_id":asset,"asset_page":"https://polyhaven.com/a/"+asset,
              "resolution":size,"model":name,
              "files":downloads}
    (root/"receipt.json").write_text(json.dumps(manifest,indent=2),encoding="utf8")
    print("ODISSEIA_V17_POLYHAVEN_CC0_MODEL_IMPORTED",asset,size,sum(v["bytes"] for v in downloads),flush=True)
    return manifest

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--metadata-only",action="store_true")
    p.add_argument("--out",type=pathlib.Path,default=ROOT)
    args=p.parse_args()
    for name in ASSETS:download(name,args.out,args.metadata_only)

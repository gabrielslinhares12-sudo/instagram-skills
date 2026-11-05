#!/usr/bin/env python3
"""Publish the six original owner-approved Lúmino images already staged in GitHub.

No browser, Drive tokens, paid API, Stories or music. 
Fail closed unless all six HTTPS images match SHA-256 and the official Meta account.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
import subprocess,sys,time
from instagram_lumino_nov05_publish_once import publish,POST_ID,STATE,PREFIX,REPO
from instagram_queue import read_document,validate_state
EXPECTED=[
 ("01-quem-e-o-lumino.jpg","2b2fcc4478b952ff14a4675d1d296a4115ab500555caa7c33e17e9a24da2e2e2"),
 ("02-onde-tudo-comecou.jpg","0dfe3f51e75040b92b65ef47e65412aa8b1e67f3bf9c476c0e0894ab015f2cf3"),
 ("03-nao-e-magia.jpg","5ef0e6d6483d6977279ed0808511073cf1e5303bc3cd6c54c1fc685d283fe19b"),
 ("04-do-oceano-as-estrelas.jpg","faee5d2a43c763f29b007a212e6da8405e0950a6fca295d2ddd7c91fdb240871"),
 ("05-ele-investiga-com-metodo.jpg","a39e46e0f15f53848cc6386f567bfb6857906281b16a87953115798d724dfb7c"),
 ("06-a-proxima-pergunta-e-sua.jpg","3b451390fb3d1725dbbee22ec71355cff9608eb869debbbf9568ce3e6833ed52")
]
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
    state=validate_state(read_document(STATE,missing={"version":1,"items":{}}))
    if POST_ID in state["items"]:
        item=state["items"][POST_ID]
        print("EXISTING_PUBLICATION_STATE_NO_RETRY="+str(item.get("status")),flush=True)
        print("EXISTING_MEDIA_ID="+str(item.get("media_id") or ""),flush=True)
        return 0
    pin=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    urls=[]
    for i,(name,expected_sha) in enumerate(EXPECTED,1):
        path=Path(PREFIX)/name
        data=path.read_bytes()
        if digest(data)!=expected_sha or data[:3]!=b'\xff\xd8\xff':
            raise RuntimeError(f"slide_{i}_not_exact_owner_approved_jpeg")
        url=f"https://raw.githubusercontent.com/{REPO}/{pin}/{PREFIX}/{name}"
        for attempt in range(7):
            try:
                with urlopen(Request(url,headers={"User-Agent":"TUE-Meta-Image-Preflight/1.0"}),timeout=30) as res:
                    remote=res.read(1_900_000)
                    if res.status==200 and digest(remote)==expected_sha:break
            except (HTTPError,URLError,TimeoutError):pass
            if attempt==6:raise RuntimeError(f"public_https_slide_{i}_unverified")
            time.sleep(4)
        urls.append(url)
        print(f"SLIDE_{i}_PUBLIC_SHA256_VERIFIED",flush=True)
    print("ALL_SIX_IDENTICAL_APPROVED_ARTS_VERIFIED",flush=True)
    return publish(urls,[item[1] for item in EXPECTED])
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:
        print("META_LUMINO_ONE_SHOT_BLOCKED="+type(e).__name__+":"+str(e),file=sys.stderr,flush=True)
        sys.exit(1)

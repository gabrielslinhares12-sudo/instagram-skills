#!/usr/bin/env python3
"""Readiness of the official Instagram app on an ephemeral GitHub Android emulator.
No accounts, credentials, paid services, private APKs, posts, or edits.
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import time
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

PACKAGE="com.instagram.android"
STORE="com.android.vending"
OUT=Path("cloud-probe/official-instagram-preflight")

def adb(*args, timeout=70, check=True):
    return subprocess.run(["adb",*args],capture_output=True,text=True,timeout=timeout,check=check)

def norm(value):
    return "".join(c for c in unicodedata.normalize("NFKD",str(value or ""))
                   if not unicodedata.combining(c)).lower().strip()

def parse_nodes(xml):
    nodes=[]
    for element in ET.fromstring(xml).iter("node"):
        a=element.attrib
        m=re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",a.get("bounds",""))
        if m:
            nodes.append({"text":a.get("text",""),"desc":a.get("content-desc",""),
                          "pkg":a.get("package",""),"enabled":a.get("enabled")=="true",
                          "bounds":[int(v) for v in m.groups()]})
    return nodes

def classify(nodes,installed=False):
    if installed:return "instagram_installed"
    labels=[norm(n["text"]+" "+n["desc"]) for n in nodes]
    if not labels:return "ui_unavailable"
    for text in labels:
        if any(word in text for word in ("sign in","fazer login","iniciar sessao",
              "log in","use your google account","iniciar sesion")):
            return "google_sign_in_required"
    if any("instagram" in t for t in labels) and any(
            norm(n["text"]) in ("install","instalar") and n["pkg"]==STORE
            and n["enabled"] for n in nodes):
        return "install_available"
    return "official_install_unavailable"

def installed(package):
    return f"package:{package}" in adb("shell","pm","list","packages",package).stdout.splitlines()

def ui():
    r=adb("shell","uiautomator","dump","/sdcard/tue-store.xml",check=False)
    if r.returncode:return []
    xml=adb("exec-out","cat","/sdcard/tue-store.xml",check=False).stdout
    try:return parse_nodes(xml)
    except ET.ParseError:return []

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    adb("wait-for-device",timeout=100)
    report={"android":adb("shell","getprop","ro.build.version.release").stdout.strip(),
            "play_store_installed":installed(STORE),
            "instagram_before":installed(PACKAGE),
            "instagram_after":False,
            "install_clicked":False,"credentials_used":False,
            "new_posts":0,"published_posts_edited":0,"music_applied":False}
    if not report["play_store_installed"]:
        report["state"]="official_store_missing"
    elif report["instagram_before"]:
        report["state"]="instagram_installed"
    else:
        adb("shell","am","start","-a","android.intent.action.VIEW",
            "-d",f"market://details?id={PACKAGE}",check=False)
        time.sleep(12)
        nodes=ui()
        state=classify(nodes)
        report["initial_state"]=state
        if state=="install_available":
            choices=[n for n in nodes if norm(n["text"]) in ("install","instalar")
                     and n["pkg"]==STORE and n["enabled"]]
            if len(choices)==1:
                a,b,c,d=choices[0]["bounds"]
                if c>a and d>b:
                    adb("shell","input","tap",str((a+c)//2),str((b+d)//2))
                    report["install_clicked"]=True
                    for _ in range(10):
                        time.sleep(5)
                        if installed(PACKAGE):break
                    state=classify(ui(),installed(PACKAGE))
        report["state"]=state
    report["instagram_after"]=installed(PACKAGE)
    if report["instagram_after"]:
        adb("shell","monkey","-p",PACKAGE,"-c","android.intent.category.LAUNCHER",
            "1",check=False)
        report["next_blocker"]="instagram_login_required_for_real_audio_editor"
    elif report["state"]=="google_sign_in_required":
        report["next_blocker"]="google_play_login_required_for_official_instagram_install"
    else:
        report["next_blocker"]="no_verified_install_without_google_login"
    (OUT/"result.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("ANDROID_OFFICIAL_INSTAGRAM="+json.dumps(report,ensure_ascii=False),flush=True)
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as f:
            f.write("## Instagram oficial no Android cloud\n")
            for key in ("android","play_store_installed","instagram_after","state","next_blocker"):
                f.write(f"- {key}: {report.get(key)}\n")
            f.write("- Nenhum login, publicacao ou edicao foi tentado.\n")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

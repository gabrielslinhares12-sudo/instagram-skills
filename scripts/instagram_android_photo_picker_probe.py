#!/usr/bin/env python3
"""Instrument Android's native multi-image picker without Instagram credentials."""
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

OUT=Path("cloud-probe/photo-picker")
OUT.mkdir(parents=True,exist_ok=True)
NAMES=[f"{n:02d}-historia-halloween.jpg" for n in range(1,9)]

def adb(*args, timeout=40):
    p=subprocess.run(["adb",*args],text=True,capture_output=True,timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"ADB failed for {args[0]}: exit {p.returncode}; {p.stderr[-250:]}")
    return p.stdout

def nodes():
    adb("shell","uiautomator","dump","/sdcard/window.xml",timeout=55)
    root=ET.fromstring(adb("exec-out","cat","/sdcard/window.xml"))
    result=[]
    for x in root.iter("node"):
        a=x.attrib
        m=re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",a.get("bounds",""))
        if m:
            result.append({"label":a.get("text","")+" "+a.get("content-desc",""),
                "box":list(map(int,m.groups()))})
    return result

def labels(seq):
    return list(dict.fromkeys(x["label"].strip() for x in seq if x["label"].strip()))[:60]

def find(seq,key):
    return next((x for x in seq if key.lower() in x["label"].lower() and
                x["box"][2]>x["box"][0]),None)

def click(item,hold=False):
    a,b,c,d=item["box"]
    x,y=str((a+c)//2),str((b+d)//2)
    if hold:
        adb("shell","input","swipe",x,y,x,y,"1100")
    else:
        adb("shell","input","tap",x,y)
    time.sleep(1.1)

def shot(name):
    with (OUT/(name+".png")).open("wb") as f:
        subprocess.run(["adb","exec-out","screencap","-p"],stdout=f,check=True)

def view(stage,seq):
    print(stage+"="+json.dumps(labels(seq),ensure_ascii=False),flush=True)
    shot(stage)

def main():
    dev=adb("shell","ls","/sdcard/Pictures/InstagramTUEProbe").splitlines()
    assert len([x for x in dev if x.endswith(".jpg")])==8
    print("DEVICE_PHOTOS_PRESENT=8",flush=True)
    q=adb("shell","content","query","--uri","content://media/external/images/media",
          "--projection","_display_name")
    print("MEDIA_STORE_INDEXED="+str(sum(n in q for n in NAMES))+"/8",flush=True)
    adb("shell","input","keyevent","KEYCODE_BACK")
    uri="content://com.android.externalstorage.documents/document/primary%3APictures%2FInstagramTUEProbe"
    adb("shell","am","start","-a","android.intent.action.OPEN_DOCUMENT",
        "-c","android.intent.category.OPENABLE","-t","image/jpeg",
        "--ez","android.intent.extra.ALLOW_MULTIPLE","true",
        "--eu","android.provider.extra.INITIAL_URI",uri)
    time.sleep(5)
    seq=nodes()
    view("01-initial",seq)
    if len([f for f in NAMES if find(seq,f)])!=8:
        menu=find(seq,"Show roots") or find(seq,"Navigate up")
        if menu:
            click(menu)
            seq=nodes()
            view("02-roots",seq)
            local=(find(seq,"sdk_gphone") or find(seq,"Internal storage") or
                   find(seq,"Android SDK built for") or find(seq,"pixel"))
            if local:
                click(local)
                seq=nodes()
                view("03-local",seq)
                for folder in ("Pictures","InstagramTUEProbe"):
                    item=find(seq,folder)
                    if not item:
                        break
                    click(item)
                    seq=nodes()
                    print("NAVIGATED_FOLDER="+folder,flush=True)
    view("04-target-folder",seq)
    visible=[f for f in NAMES if find(seq,f)]
    print("PICKER_VISIBLE_UNIQUE_FILES="+str(len(visible))+"/8",flush=True)
    if len(visible)!=8:
        raise RuntimeError("Android picker failed to display 8 original images")
    # Files displays image-grid preview icons; switch to list rows for reliable ADB clicks.
    toggle=find(seq,"List view")
    if toggle:
        click(toggle)
        seq=nodes()
        view("05-list-view",seq)
    first=find(seq,NAMES[0])
    if not first:
        raise RuntimeError("First image row missing after switching to list view")
    click(first,hold=True)
    seq=nodes()
    view("06-first-hold",seq)
    first_selected=(find(seq,"1 selected") or find(seq,"1 item selected") or
                    find(seq,"Select 1") or find(seq,"1 file selected"))
    print("FIRST_LONG_PRESS_SELECTED="+str(bool(first_selected)).lower(),flush=True)
    if not first_selected:
        # Do not try blind publication; record evidence for deterministic follow-up.
        raise RuntimeError("Long-press did not enter file selection mode")
    for n in NAMES[1:]:
        x=find(seq,n)
        if not x:
            raise RuntimeError("Picker cannot select all; missing "+n)
        click(x)
        seq=nodes()
    view("07-eight-selected",seq)
    count=(find(seq,"8 selected") or find(seq,"Selected 8") or
           find(seq,"8 items selected") or find(seq,"8 files selected"))
    print("PICKER_EIGHT_SELECTED_VERIFIED="+str(bool(count)).lower(),flush=True)
    if not count:
        raise RuntimeError("No Android UI confirmation of selecting eight files")
    (OUT/"proof.json").write_text(json.dumps({"original_jpegs":8,
        "picker_visible":8,"picker_selected":8,
        "instagram_install_attempted":False,"published":False},indent=2)+"\n")
    print("INSTAGRAM_PUBLISHED=false",flush=True)

if __name__=="__main__":
    main()

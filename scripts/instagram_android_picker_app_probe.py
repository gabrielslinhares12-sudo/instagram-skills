#!/usr/bin/env python3
"""End-to-end Android picker test with our original offline requestor app."""
import json
import time
from pathlib import Path
import instagram_android_photo_picker_probe as util

NAMES=util.NAMES
OUT=util.OUT

def ui(stage):
    seq=util.nodes()
    util.view(stage,seq)
    return seq

def main():
    util.adb("logcat","-c")
    util.adb("shell","am","start","-n","com.temumaexplicacao.pickerprobe/.MainActivity")
    time.sleep(6)
    seq=ui("10-real-app-picker")
    names=[n for n in NAMES if util.find(seq,n)]
    print("REAL_CALLER_VISIBLE_FILES="+str(len(names))+"/8",flush=True)
    if len(names)!=8:
        raise RuntimeError("Real app picker cannot see the eight photos")
    toggle=util.find(seq,"List view")
    if toggle:
        util.click(toggle)
        seq=ui("11-real-app-list")
    def select_status(items):
        return (util.find(items,"1 selected") or util.find(items,"1 item selected") or
                util.find(items,"1 file selected"))
    def exact_file(items,name):
        matching=[v for v in items if v["label"].strip()==name]
        return matching[0] if matching else util.find(items,name)
    first=exact_file(seq,NAMES[0])
    print("FIRST_EXACT_FILENAME_NODE="+json.dumps(first),flush=True)
    util.click(first,hold=True)
    seq=ui("12-real-app-first-hold")
    selected=select_status(seq)
    if not selected:
        # Files UI exposes a separate preview icon and the file thumbnail: test thumbnail.
        rect=first["box"]
        y=(rect[1]+rect[3])//2
        util.adb("shell","input","swipe","75",str(y),"75",str(y),"1200")
        time.sleep(1.2)
        seq=ui("13-real-app-thumbnail-hold")
        selected=select_status(seq)
    if not selected:
        rect=first["box"]
        y=(rect[1]+rect[3])//2
        util.adb("shell","input","tap","75",str(y))
        time.sleep(1.1)
        seq=ui("14-real-app-thumbnail-tap")
        selected=select_status(seq)
    print("REAL_APP_FIRST_SELECTED="+str(bool(selected)).lower(),flush=True)
    if not selected:
        log=util.adb("logcat","-d","-s","TUEPickerProbe:I","*:S")
        print("APP_RETURNED_AFTER_TAP="+str("PICKER_RESULT_COUNT=" in log).lower(),flush=True)
        raise RuntimeError("Actual Android caller did not enter multi-select after text and thumbnail interactions")
    # Click the remaining rows, checking selection after each action.
    for index,name in enumerate(NAMES[1:],2):
        item=util.find(seq,name)
        if not item:
            raise RuntimeError("Missing image row on multi-select: "+name)
        util.click(item)
        seq=util.nodes()
        print("REAL_CALLER_SELECTION_STEP="+str(index),flush=True)
    util.view("14-real-app-eight-selected",seq)
    selected8=(util.find(seq,"8 selected") or util.find(seq,"8 items selected") or
               util.find(seq,"8 files selected"))
    print("REAL_APP_EIGHT_SELECTED="+str(bool(selected8)).lower(),flush=True)
    if not selected8:
        raise RuntimeError("No verified eight-photo selection in Android UI")
    button=util.find(seq,"Open") or util.find(seq,"Select") or util.find(seq,"Done")
    if not button:
        raise RuntimeError("Native picker has no confirm-selection control")
    util.click(button)
    time.sleep(3)
    ui("15-real-app-result")
    log=util.adb("logcat","-d","-s","TUEPickerProbe:I","*:S")
    observed="PICKER_RESULT_COUNT=8 RESULT_OK=true" in log
    print("PICKER_RESULT_COUNT_8="+str(observed).lower(),flush=True)
    if not observed:
        raise RuntimeError("Real test app did not receive eight Android image URIs")
    (OUT/"picker-app-proof.json").write_text(json.dumps({"original_photos":8,
       "caller":"locally-built signed test APK","received_uris":8,
       "instagram_installed":False,"instagram_login":False,"published":False},indent=2)+"\n",encoding="utf-8")
    print("INSTAGRAM_PUBLISHED=false",flush=True)

if __name__=="__main__":
    main()

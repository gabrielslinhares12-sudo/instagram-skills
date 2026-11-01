#!/usr/bin/env python3
"""Offline Android picker input diagnostic; no Instagram, login or publishing."""
import json
import subprocess
import time
from pathlib import Path
import xml.etree.ElementTree as ET

OUT=Path("cloud-probe/input-diagnostic")
OUT.mkdir(parents=True,exist_ok=True)
def adb(*args,timeout=50):
    r=subprocess.run(["adb",*args],capture_output=True,text=True,timeout=timeout)
    if r.returncode:
        print("ADB_COMMAND_FAILED",args[0],r.stderr.strip()[-240:],flush=True)
    return r.stdout.strip(),r.returncode
def capture(label):
    r=subprocess.run(["adb","exec-out","screencap","-p"],capture_output=True,timeout=25)
    if r.returncode==0:
        (OUT/(label+".png")).write_bytes(r.stdout)
    adb("shell","uiautomator","dump","/sdcard/picker-dump.xml",timeout=55)
    xml,rc=adb("exec-out","cat","/sdcard/picker-dump.xml")
    if rc: return []
    (OUT/(label+".xml")).write_text(xml)
    root=ET.fromstring(xml)
    nodes=[]
    for el in root.iter("node"):
        a=el.attrib
        name=a.get("text") or a.get("content-desc") or ""
        if name:
            nodes.append({k:a.get(k) for k in ["text","content-desc","bounds","selected","checked","enabled","clickable","long-clickable"]})
    print("UI_STATE",label,json.dumps(nodes[:32],ensure_ascii=False),flush=True)
    return nodes
def current_activity():
    out,_=adb("shell","dumpsys","window","windows")
    relevant=[ln.strip() for ln in out.splitlines() if "mCurrentFocus" in ln or "mFocusedApp" in ln]
    print("FOCUSED_WINDOW",json.dumps(relevant),flush=True)
def launch(label):
    adb("shell","am","force-stop","com.temumaexplicacao.pickerprobe")
    adb("shell","am","start","-n","com.temumaexplicacao.pickerprobe/.MainActivity")
    time.sleep(4)
    current_activity()
    capture(label+"-before")
def poke(cmd,label):
    out,rc=adb("shell","input",*cmd)
    print("INPUT_COMMAND",label,"rc",rc,out[-150:],flush=True)
    time.sleep(2)
    current_activity()
    capture(label+"-after")
    out,_=adb("logcat","-d","-s","TUEPickerProbe:I","*:S")
    print("APP_CALLBACK",label,[x.strip()[-200:] for x in out.splitlines() if "PICKER_RESULT_COUNT" in x][-5:],flush=True)
def main():
    # Coordinates correspond to native 1080x2280 screen, first row image y~760.
    # Each input variation starts with fresh caller and Android DocumentsUI selection.
    # XML confirms first item grid cell [66,699][367,1001], preview button [235,699][367,831].
    # Earlier tests tapped filename/preview overlays rather than a file's center.
    scenarios=[
      ("tap-cell-center",["tap","152","870"]),
      ("longpress-cell-center",["swipe","152","870","152","870","1700"]),
      ("tap-cell-edge",["tap","210","944"]),
      ("longpress-cell-edge",["swipe","210","944","210","944","1700"]),
      ("tap-preview-exact",["tap","301","765"]),
      ("touchscreen-center",["touchscreen","tap","152","870"]),
      ("tap-second-cell-center",["tap","505","870"]),
    ]
    for label,cmd in scenarios:
        print("SCENARIO_START",label,flush=True)
        launch(label)
        poke(cmd,label)
    print("DIAGNOSTIC_COMPLETED_NO_INSTAGRAM_OR_POST=true",flush=True)
if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Only read DuoPlus cloud-phone status. Never write/launch/login/publish."""
import json, os, re, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

URL = "https://openapi.duoplus.net/api/v1/cloudPhone/list"
PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,100}$")

def check(payload, wanted):
    if not isinstance(payload, dict) or payload.get("code") != 200:
        return {"state":"api_denied","ready":False}
    data = payload.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("list"),list):
        return {"state":"invalid_schema","ready":False}
    matches = [p for p in data["list"] if isinstance(p,dict) and p.get("id")==wanted]
    if len(matches)!=1:
        return {"state":"device_missing_or_ambiguous","ready":False}
    p=matches[0]
    if p.get("status")!=1:state="not_running"
    elif str(p.get("http_status"))!="1":state="http_disabled"
    else:state="ready"
    return {"state":state,"ready":state=="ready",
            "android_version":str(p.get("os") or "unknown")[:32]}
    # NO raw JSON! May contain phone IP, ADB password, account identifiers.

def request_status(token,phone):
    r=Request(URL,data=json.dumps({"image_id":[phone],"page":1,"pagesize":100}).encode(),
              method="POST",headers={"DuoPlus-API-Key":token,"Content-Type":"application/json",
                "Lang":"en","Accept":"application/json"})
    try:
        with urlopen(r,timeout=18) as resp:
            body=resp.read(500001)
            if len(body)>500000:return {"state":"response_too_large","ready":False}
            return check(json.loads(body),phone)
    except HTTPError as ex:
        return {"state":"auth_required" if ex.code in (401,403) else "http_error","ready":False}
    except (ValueError,URLError,OSError,TimeoutError):
        return {"state":"network_or_response_error","ready":False}

def main():
    key=os.getenv("DUOPLUS_API_KEY","").strip()
    phone=os.getenv("DUOPLUS_PHONE_ID","").strip()
    if not key:result={"state":"api_key_not_connected","ready":False}
    elif not phone:result={"state":"phone_id_not_set","ready":False}
    elif not PATTERN.fullmatch(phone):result={"state":"invalid_phone_id","ready":False}
    else:result=request_status(key,phone)
    result.update(provider="DuoPlus",mode="read_only",posted=False,
                  music_confirmed=False,charges_authorized=False)
    print("DUOPLUS_STATUS="+json.dumps(result,ensure_ascii=False,sort_keys=True))
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as f:
            f.write("## TUE cloud phone - somente leitura\n\n")
            f.write("Estado: "+result["state"]+"\n\n")
            f.write("Nenhuma conta, post ou cobranca foi modificada.\n")
    return 0 if result["state"] in {"api_key_not_connected","phone_id_not_set",
        "invalid_phone_id","device_missing_or_ambiguous","not_running","http_disabled","ready"
    } else 1

if __name__=="__main__":sys.exit(main())

#!/usr/bin/env python3
"""Publora TUE: verify connected Instagram account with GET only.

No drafting, uploading, scheduling, posting, login automation, or API mutation.
Prints no API keys, bearer tokens, usernames other than the expected public
account, or raw provider response.
"""
from __future__ import annotations

import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

EXPECTED_USERNAME = "temumaexplicacao"
URL = "https://api.publora.com/api/v1/platform-connections"
PLATFORM_ID = re.compile(r"instagram-[a-zA-Z0-9_-]{3,80}\Z")


def evaluate(key: str | None, target: str | None, transport=urlopen) -> dict:
    key, target = (key or "").strip(), (target or "").strip()
    if not key and not target:
        return {"ok": False, "mode": "not_configured", "publora_connected": False,
                "music_via_publora_api": False, "mutations": False}
    if not key or not PLATFORM_ID.fullmatch(target):
        return {"ok": False, "mode": "incomplete_credentials_or_platform_id",
                "publora_connected": False, "music_via_publora_api": False, "mutations": False}
    if len(key) > 512 or not key.startswith("sk_"):
        return {"ok": False, "mode": "invalid_api_key_format",
                "publora_connected": False, "music_via_publora_api": False, "mutations": False}
    request = Request(URL, method="GET", headers={
        "x-publora-key": key, "Accept": "application/json",
        "User-Agent": "TUE-Publora-ReadOnly-Preflight/1",
    })
    try:
        with transport(request, timeout=15) as response:
            document = json.loads(response.read(256 * 1024).decode("utf-8"))
    except (HTTPError, URLError, OSError, UnicodeError, ValueError, TimeoutError):
        return {"ok": False, "mode": "connection_unverified",
                "publora_connected": False, "music_via_publora_api": False, "mutations": False}
    if not isinstance(document, dict) or document.get("success") is not True:
        return {"ok": False, "mode": "unexpected_response", "publora_connected": False,
                "music_via_publora_api": False, "mutations": False}
    connections = document.get("connections")
    if not isinstance(connections, list):
        return {"ok": False, "mode": "unexpected_response", "publora_connected": False,
                "music_via_publora_api": False, "mutations": False}
    matches = [connection for connection in connections
               if isinstance(connection, dict) and connection.get("platformId") == target]
    if len(matches) != 1:
        return {"ok": False, "mode": "platform_id_not_found", "publora_connected": False,
                "music_via_publora_api": False, "mutations": False}
    item = matches[0]
    username = str(item.get("username") or "").lstrip("@").lower()
    active = item.get("connectionStatus") == "active"
    valid = item.get("tokenStatus") in ("valid", "expiring_soon")
    correct = username == EXPECTED_USERNAME
    return {
        "ok": correct and active and valid,
        "mode": "verified" if correct and active and valid else "account_or_token_not_ready",
        "publora_connected": correct and active and valid,
        "target_username": EXPECTED_USERNAME,
        "account_matches": correct,
        "token_ready": valid,
        "connection_active": active,
        "music_via_publora_api": False,
        "mutations": False,
    }


def main() -> int:
    result = evaluate(os.getenv("PUBLORA_API_KEY"), os.getenv("INSTAGRAM_PLATFORM_ID"))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    # Missing configuration is not a CI failure. Genuine wrong-account or
    # network errors after attempted configuration are a failure.
    return 0 if result["mode"] in ("not_configured", "verified") else 1


if __name__ == "__main__":
    sys.exit(main())

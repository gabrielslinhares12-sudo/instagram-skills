#!/usr/bin/env python3
"""Read-only readiness proof for Instagram carousel+native-music via unofficial mobile API.

No Instagram login, cookies, API writes or publication. This is NOT a claim
that Instagram will permit a real upload or that a selected song exists.
"""
from __future__ import annotations
import inspect
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from instagram_private_music import fetch_verified_jpegs
from instagram_queue import validate_manifest

def main() -> int:
    import instagrapi
    from instagrapi import Client
    filename = Path("content/schedule.json")
    manifest = validate_manifest(json.loads(filename.read_text(encoding="utf-8")))
    method = getattr(Client, "album_upload_with_music", None)
    finder = getattr(Client, "search_music", None)
    read_identity = getattr(Client, "account_info", None)
    signature_ok = False
    if callable(method):
        signature = inspect.signature(method)
        signature_ok = {"paths", "caption", "track"}.issubset(signature.parameters)
    library_ok = bool(signature_ok and callable(finder) and callable(read_identity))
    if not library_ok:
        raise RuntimeError("Installed mobile library does not have required album/music methods")

    native = [p for p in manifest if p["kind"] == "carousel" and
              p.get("distribution_mode", "native_music_carousel") == "native_music_carousel"]
    verified = []
    for p in native:
        if p["id"] == "halloween-2026-10-31-historia-8-laminas":
            with TemporaryDirectory() as d:
                paths = fetch_verified_jpegs(p, Path(d))
                if len(paths) != 8:
                    raise RuntimeError("Eight approved Halloween images were not verified")
                verified.append(p["id"])
    expected = "halloween-2026-10-31-historia-8-laminas"
    if expected not in verified:
        raise RuntimeError("Approved Halloween post is absent from validated cloud queue")

    session_exists = bool(os.getenv("INSTAGRAM_PRIVATE_SESSION_B64", "").strip())
    publisher_enabled = os.getenv("INSTAGRAM_PRIVATE_PUBLISH_ENABLED") == "true"
    risk_accepted = os.getenv("INSTAGRAM_PRIVATE_RISK_ACCEPTED") == "true"
    authorized = [p["id"] for p in native if p.get("private_api_authorized") is True and
                  p.get("music_track") and p.get("music_artist")]
    state = json.loads(Path("content/publication-state.json").read_text(encoding="utf-8"))
    unpublished = [p["id"] for p in native if p["id"] not in state.get("items", {})]
    # Deliberately never decode the session, print account details or call Instagram.
    result = {
        "check": "read_only",
        "cloud_runner": True,
        "library_version": getattr(instagrapi, "__version__", "unknown"),
        "native_carousel_upload_method": library_ok,
        "approved_halloween_images_sha256_verified": len(verified) == 1,
        "verified_halloween_image_count": 8,
        "native_music_carousels": len(native),
        "explicitly_authorized_for_unofficial_api": len(authorized),
        "unpublished_native_carousels": len(unpublished),
        "session_secret_configured": session_exists,
        "enable_flag": publisher_enabled,
        "risk_acceptance_flag": risk_accepted,
        "can_attempt_unofficial_publication": bool(session_exists and publisher_enabled and
             risk_accepted and authorized),
        "post_attempted": False,
        "audio_library_queried": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    summary=os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary,"a",encoding="utf-8") as out:
            out.write("### Instagram cloud: native music readiness (no publication)\n")
            for key in ("native_carousel_upload_method","approved_halloween_images_sha256_verified",
                        "session_secret_configured","enable_flag","risk_acceptance_flag",
                        "can_attempt_unofficial_publication"):
                out.write(f"- `{key}`: `{result[key]}`\n")
            out.write("- WARNING: this method is **unofficial** and may cause login challenges/account restrictions.\n")
            out.write("- Passing library checks does not prove Instagram accepted a music carousel.\n")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"ok": False, "diagnostic":"nonpublishing_library_or_asset_check_failed",
                          "exception_type":type(exc).__name__}),file=sys.stderr)
        raise SystemExit(1)

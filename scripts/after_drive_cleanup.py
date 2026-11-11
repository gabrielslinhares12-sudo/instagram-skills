#!/usr/bin/env python3
"""Delete a GitHub Actions artifact ONLY after an exact matching Google Drive backup.

- Read a versioned, explicit allowlist in the same GitHub repo.
- Independently stream and hash the raw GitHub artifact ZIP and the Drive ZIP.
- Compare against the receipt SHA256, expected sizes, IDs, names and run IDs.
- Delete only the exact verified Actions artifact, never a workflow run/release/Drive file.
- Missing credentials, failed reads or mismatched data fail closed.

Designed for use with short-lived GitHub Actions credentials and Drive OAuth.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = "gabrielslinhares12-sudo/instagram-skills"
API = f"https://api.github.com/repos/{REPO}/actions/artifacts/"
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "content/artifact-cleanup/drive_verified.json"
REQUIRED = {"artifact_id", "run_id", "artifact_name", "size_bytes", "drive_file_id", "drive_name", "drive_parent_id", "sha256"}
USER_AGENT = "TUE-verified-drive-artifact-cleanup/1.0"

# Eight initial files: GitHub archive and owner Drive bytes were independently
# matched via SHA256 in the audited conversation on 2026-11-11.
# This is a one-time allowlist, never inferred for later artifacts.
INITIAL_DRIVE_HASH_PROOF = {
    13766758374: ("1VVBxIPXhWYQCXoQwr47d0lMj2wgz0QlP", "c77a20960dedb8e4e7fd7bd66015e74d7bf218a4ca434ca744bb7fc29377d7b3", 26978689, 42822095152),
    13762140586: ("1hmglWzT346tnSJeJYvAOzRRBzE7Bke4E", "9368977491998b7e74721640a3c988c913a247df730f324d680909659cac5038", 17714302, 42808350863),
    13761625774: ("1Adys3EYZUbkBkWhQTRW7ESpLH-dqew26", "2b408b5cb5abc1e9279baa606fb0f52e17bd3d293b7780eb4a2ed95df4f40ac4", 21979562, 42808350863),
    13760476858: ("1C9Nn_RXTuJvOuyrC6jOLbnIngusOt5MW", "c2d80f71d2abbd044754f43e56ea9825a300825e2b45dfcc34de2bf285f135ad", 18926361, 42808350863),
    13767511517: ("1ft4of8dyqZ4hJjKFmGRuslYnGiz4dY4E", "4e5b28fc05dfdbcaefd9ccb9f4c8adea287d8741a45e1309b957ec64d404a6f7", 42823749, 42821244925),
    13766234421: ("1vJAK5zg-nLQeoOAggQIaDvRambfrd5H3", "c81d7fab060bf05051806ec1a265ae6c3d7312df811a751469d4fabef7d49df7", 33200305, 42821244925),
    13767361897: ("1RtcmWqGQKZ9D83F-6QvDmLaaqi1zstAQ", "e521d3c29b2a9e165d143a3a308ec37ea644a74bcb56009ca6f8d2e419c6943e", 42390652, 42821244925),
    13767297700: ("1PH7GDSMda705hm3-3ACSp4DMdBMPD0rC", "ef910d7e84e1b7cb7f364bc30b0a5d7f4941d242d7f62d6fb8ecfa6686f46c8e", 31474746, 42821919215),
}
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
DRIVE_ID = re.compile(r"^[A-Za-z0-9_-]{10,150}$")


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Never forward GH authorization to the archive CDN on redirects."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        u = urllib.parse.urlsplit(newurl)
        h = (u.hostname or "").lower()
        if u.scheme != "https" or not (
            h == "github.com"
            or h == "objects.githubusercontent.com"
            or h.endswith(".githubusercontent.com")
            or h.endswith(".blob.core.windows.net")
            or h.endswith(".github.com")
        ):
            raise RuntimeError("Artifact redirected to untrusted host: " + h)
        return urllib.request.Request(newurl, headers={"User-Agent": USER_AGENT}, method="GET")


def read_json(url: str, headers: dict[str, str], data: bytes | None = None) -> dict:
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=60) as r:
        return json.load(r)


def sha256_stream(request: urllib.request.Request, *, safe_redirect=False) -> tuple[str, int]:
    opener = urllib.request.build_opener(SafeRedirect()) if safe_redirect else urllib.request.build_opener()
    h = hashlib.sha256()
    size = 0
    with opener.open(request, timeout=150) as response:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def validate_row(row: dict) -> None:
    if not isinstance(row, dict) or not REQUIRED.issubset(row):
        raise ValueError("Incomplete receipt")
    if type(row["artifact_id"]) is not int or row["artifact_id"] < 1:
        raise ValueError("Invalid artifact ID")
    if type(row["run_id"]) is not int or row["run_id"] < 1:
        raise ValueError("Invalid run ID")
    if type(row["size_bytes"]) is not int or row["size_bytes"] < 1:
        raise ValueError("Invalid size")
    if not HEX_64.fullmatch(row["sha256"]):
        raise ValueError("Invalid sha256")
    if not all(isinstance(row[n], str) and row[n].strip() for n in ("artifact_name", "drive_name")):
        raise ValueError("Missing archive name")
    if not DRIVE_ID.fullmatch(row["drive_file_id"]) or not DRIVE_ID.fullmatch(row["drive_parent_id"]):
        raise ValueError("Invalid Drive file/parent ID")


def load_rows() -> list[dict]:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1 or document.get("repository") != REPO:
        raise ValueError("Unexpected receipt schema/repository")
    rows = document.get("verified_copies")
    if not isinstance(rows, list):
        raise ValueError("Malformed receipts list")
    seen: set[int] = set()
    for row in rows:
        validate_row(row)
        if row["artifact_id"] in seen:
            raise ValueError("Duplicate artifact ID in receipts")
        seen.add(row["artifact_id"])
    return rows


def github_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }


def get_artifact(token: str, artifact_id: int) -> dict | None:
    try:
        return read_json(API + str(artifact_id), github_headers(token))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def validate_artifact_metadata(actual: dict, receipt: dict) -> None:
    if actual.get("id") != receipt["artifact_id"]:
        raise RuntimeError("GitHub artifact ID mismatch")
    if actual.get("name") != receipt["artifact_name"]:
        raise RuntimeError("GitHub artifact name mismatch")
    if actual.get("size_in_bytes") != receipt["size_bytes"]:
        raise RuntimeError("GitHub artifact size mismatch")
    if actual.get("expired") is not False:
        raise RuntimeError("GitHub artifact expired")
    if (actual.get("workflow_run") or {}).get("id") != receipt["run_id"]:
        raise RuntimeError("GitHub workflow run mismatch")


def get_drive_access_token() -> str:
    keys = ("GDRIVE_OAUTH_CLIENT_ID", "GDRIVE_OAUTH_CLIENT_SECRET", "GDRIVE_OAUTH_REFRESH_TOKEN")
    vals = [os.getenv(x, "").strip() for x in keys]
    if not all(vals):
        raise RuntimeError("Drive OAuth secrets not configured; deletion refused")
    body = urllib.parse.urlencode({"client_id": vals[0], "client_secret": vals[1],
                                   "refresh_token": vals[2], "grant_type": "refresh_token"}).encode()
    info = read_json("https://oauth2.googleapis.com/token", {"Content-Type": "application/x-www-form-urlencoded",
                                                               "User-Agent": USER_AGENT}, data=body)
    token = info.get("access_token")
    if not isinstance(token, str) or len(token) < 20:
        raise RuntimeError("Drive OAuth token missing")
    return token


def verify_drive(receipt: dict, drive_token: str) -> None:
    fid = receipt["drive_file_id"]
    root = "https://www.googleapis.com/drive/v3/files/" + urllib.parse.quote(fid)
    h = {"Authorization": "Bearer " + drive_token, "User-Agent": USER_AGENT}
    q = urllib.parse.urlencode({"fields": "id,name,mimeType,size,parents,trashed", "supportsAllDrives": "true"})
    metadata = read_json(root + "?" + q, h)
    if (metadata.get("id") != fid or metadata.get("name") != receipt["drive_name"]
            or metadata.get("mimeType") not in ("application/zip", "application/x-zip-compressed")
            or int(metadata.get("size", -1)) != receipt["size_bytes"]
            or metadata.get("trashed") is not False
            or receipt["drive_parent_id"] not in metadata.get("parents", [])):
        raise RuntimeError("Drive file identity, parent, or size mismatch")
    media_url = root + "?" + urllib.parse.urlencode({"alt": "media", "supportsAllDrives": "true"})
    sha, length = sha256_stream(urllib.request.Request(media_url, headers=h))
    if length != receipt["size_bytes"] or sha != receipt["sha256"]:
        raise RuntimeError("Drive content SHA256/bytes mismatch")


def verify_github_content(receipt: dict, gh_token: str) -> None:
    url = API + str(receipt["artifact_id"]) + "/zip"
    sha, length = sha256_stream(urllib.request.Request(url, headers=github_headers(gh_token)), safe_redirect=True)
    if length != receipt["size_bytes"] or sha != receipt["sha256"]:
        raise RuntimeError("GitHub artifact ZIP SHA256/bytes mismatch")


def delete_artifact(receipt: dict, gh_token: str) -> None:
    req = urllib.request.Request(API + str(receipt["artifact_id"]),
                                 headers=github_headers(gh_token), method="DELETE")
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 204:
            raise RuntimeError("GitHub did not confirm artifact deletion")
    if get_artifact(gh_token, receipt["artifact_id"]) is not None:
        raise RuntimeError("Artifact still present after deletion")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true", help="Delete ONLY after both remote hashes verify")
    p.add_argument("--max-artifacts", type=int, default=20)
    a = p.parse_args()
    if os.getenv("GITHUB_REPOSITORY") != REPO or os.getenv("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("Restricted to approved repository's main branch")
    token = os.getenv("GH_TOKEN", "")
    if not token:
        raise RuntimeError("GitHub Actions token missing")
    rows = load_rows()
    if a.max_artifacts < 1 or a.max_artifacts > 100:
        raise ValueError("Invalid max artifacts")
    try:
        drive_token = get_drive_access_token()
    except RuntimeError:
        drive_token = None
        print("DRIVE_OAUTH_MISSING: only exact eight previously SHA256-verified receipts eligible", flush=True)
    deleted = verified = missing = blocked = 0
    bytes_deleted = 0
    for entry in rows[:a.max_artifacts]:
        aid = entry["artifact_id"]
        try:
            actual = get_artifact(token, aid)
            if actual is None:
                print(f"ALREADY_ABSENT {aid}", flush=True)
                missing += 1
                continue
            validate_artifact_metadata(actual, entry)
            if drive_token:
                verify_drive(entry, drive_token)
            else:
                expected_proof = INITIAL_DRIVE_HASH_PROOF.get(aid)
                actual_proof = (entry["drive_file_id"], entry["sha256"], entry["size_bytes"], entry["run_id"])
                if expected_proof != actual_proof:
                    raise RuntimeError("Drive OAuth unavailable and no exact initial verified backup proof")
                print(f"INITIAL_DRIVE_PROOF_PREVIOUSLY_CHECKED {aid}", flush=True)
            verify_github_content(entry, token)
            verified += 1
            if a.apply:
                delete_artifact(entry, token)
                deleted += 1
                bytes_deleted += entry["size_bytes"]
                print(f"DELETED_AFTER_SHA256_MATCH {aid} {entry['size_bytes']}", flush=True)
            else:
                print(f"DRY_RUN_VERIFIED_NOT_DELETED {aid} {entry['size_bytes']}", flush=True)
        except Exception as exc:
            blocked += 1
            # Do not print access tokens, response URLs, or raw HTML error bodies.
            print(f"BLOCKED_NO_DELETE {aid} {type(exc).__name__}: {str(exc)[:160]}", flush=True)
    print(f"RESULT verified={verified} deleted={deleted} already_absent={missing} "
          f"blocked={blocked} deleted_bytes={bytes_deleted}", flush=True)
    return 1 if blocked else 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("CLEANUP_FAIL_CLOSED " + type(exc).__name__ + ": " + str(exc)[:160], flush=True)
        sys.exit(1)
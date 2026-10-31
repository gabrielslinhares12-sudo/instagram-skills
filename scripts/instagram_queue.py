#!/usr/bin/env python3
"""Publish due, approved Instagram items with a durable, no-retry Git ledger.

Dry-run is the default and needs no Meta credentials. Execution requires
INSTAGRAM_SCHEDULER_ENABLED=true, and commits a claim to the remote repository
before calling FacebookPoster.publish. A claim or uncertain outcome is never
retried automatically. GitHub Actions supplies the clock; scheduling is not
delegated to Instagram's media endpoint.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Callable
from urllib.parse import urlsplit

from facebook_poster import FacebookConfig, FacebookPoster
from meta_poster import MetaError, NUMERIC_ID, profile_username


ACCOUNT = "temumaexplicacao"
ITEM_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,79}\Z")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
MAX_DOCUMENT_BYTES = 4 * 1024 * 1024
MAX_POSTS = 366
MAX_LATENESS = timedelta(hours=2)
ITEM_FIELDS = frozenset({
    "id", "due_at", "username", "kind", "target_url", "caption", "media_urls", "approved",
    "is_ai_generated", "cover_url", "media_sha256", "title", "sources", "approval_note",
})
PAYLOAD_OPTIONS = ("is_ai_generated", "cover_url")
FINAL_STATES = frozenset({"claimed", "published", "needs_review"})


class QueueError(Exception):
    """A fixed, non-secret message suitable for Actions logs."""


def utc_time(value: Any) -> datetime:
    if not isinstance(value, str) or len(value) > 40:
        raise QueueError("Queue dates must be explicit UTC ISO 8601 strings.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise QueueError("Queue dates must be explicit UTC ISO 8601 strings.") from None
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise QueueError("Queue dates must include the UTC timezone.")
    return parsed.astimezone(timezone.utc)


def timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def public_media_url(value: Any) -> None:
    if not isinstance(value, str) or len(value) > 2048:
        raise QueueError("Queue media must have bounded public HTTPS URLs.")
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme == "https" and bool(parsed.hostname)
                 and parsed.username is None and parsed.password is None
                 and not parsed.query and not parsed.fragment and parsed.port in (None, 443))
    except ValueError:
        valid = False
    if not valid:
        raise QueueError("Queue media URLs must use HTTPS without credentials, queries or fragments.")


def read_document(path: Path, *, missing: Any = None) -> Any:
    try:
        with path.open("rb") as stream:
            raw = stream.read(MAX_DOCUMENT_BYTES + 1)
    except FileNotFoundError:
        if missing is not None:
            return missing
        raise QueueError("The requested queue document does not exist.") from None
    except OSError:
        raise QueueError("The requested queue document could not be read.") from None
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise QueueError("The queue document exceeds the size limit.")
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError):
        raise QueueError("The queue document must be valid UTF-8 JSON.") from None


def validate_manifest(document: Any) -> list[dict[str, Any]]:
    if (not isinstance(document, dict) or document.get("version") != 1
            or set(document) - {"version", "posts", "approval_note", "created_at", "timezone"}
            or not isinstance(document.get("posts"), list)
            or len(document["posts"]) > MAX_POSTS):
        raise QueueError("The queue manifest must have version 1 and a bounded posts list.")
    seen: set[str] = set()
    approved_slots: set[str] = set()
    posts = []
    for raw in document["posts"]:
        if not isinstance(raw, dict) or set(raw) - ITEM_FIELDS:
            raise QueueError("A queue item has an invalid shape or unsupported fields.")
        item = dict(raw)
        identifier = item.get("id")
        if not isinstance(identifier, str) or not ITEM_ID.fullmatch(identifier) or identifier in seen:
            raise QueueError("Queue item identifiers must be unique, bounded lowercase slugs.")
        seen.add(identifier)
        due = utc_time(item.get("due_at"))
        if item.get("username") != ACCOUNT or profile_username(item.get("target_url")) != ACCOUNT:
            raise QueueError("Every queue item must target the configured Instagram account.")
        kind, urls = item.get("kind"), item.get("media_urls")
        if kind not in {"post", "carousel", "reel"} or not isinstance(urls, list):
            raise QueueError("Queue items must use a supported kind and media_urls list.")
        if (kind == "carousel" and not 2 <= len(urls) <= 10
                or kind != "carousel" and len(urls) != 1):
            raise QueueError("Post and Reel need one URL; carousel needs two to ten images.")
        for url in urls:
            public_media_url(url)
        caption = item.get("caption")
        if not isinstance(caption, str) or not 1 <= len(caption) <= 2200:
            raise QueueError("Queue captions must contain one to 2200 characters.")
        if type(item.get("approved")) is not bool:
            raise QueueError("Every queue item must declare an explicit boolean approval.")
        if "is_ai_generated" in item and type(item["is_ai_generated"]) is not bool:
            raise QueueError("is_ai_generated must be boolean when supplied.")
        if "cover_url" in item:
            if kind != "reel":
                raise QueueError("cover_url is supported only for Reels.")
            public_media_url(item["cover_url"])
        hashes = item.get("media_sha256")
        if hashes is not None and (not isinstance(hashes, list) or len(hashes) != len(urls)
                                   or any(not isinstance(value, str) or not SHA256.fullmatch(value)
                                          for value in hashes)):
            raise QueueError("Optional media hashes must match the media URL count.")
        if item["approved"]:
            slot = timestamp(due)
            if slot in approved_slots:
                raise QueueError("Only one approved queue item is allowed per exact UTC time slot.")
            approved_slots.add(slot)
        posts.append(item)
    return sorted(posts, key=lambda item: (utc_time(item["due_at"]), item["id"]))


def validate_state(document: Any) -> dict[str, Any]:
    if (not isinstance(document, dict) or document.get("version") != 1
            or set(document) - {"version", "items"} or not isinstance(document.get("items"), dict)):
        raise QueueError("The publication ledger must have version 1 and an items object.")
    for identifier, entry in document["items"].items():
        if (not isinstance(identifier, str) or not ITEM_ID.fullmatch(identifier)
                or not isinstance(entry, dict) or entry.get("status") not in FINAL_STATES
                or not isinstance(entry.get("fingerprint"), str)
                or not SHA256.fullmatch(entry["fingerprint"])):
            raise QueueError("The publication ledger contains an invalid item.")
    return document


def payload_for(item: dict[str, Any]) -> dict[str, Any]:
    result = {"kind": item["kind"], "target_url": item["target_url"], "approved": item["approved"],
              "draft_text": item["caption"], "media_urls": list(item["media_urls"])}
    result.update({name: item[name] for name in PAYLOAD_OPTIONS if name in item})
    return result


def fingerprint(item: dict[str, Any]) -> str:
    # Bind the durable claim to final content, destination, schedule and byte hashes.
    content = {"id": item["id"], "due_at": item["due_at"], "username": item["username"],
               "payload": payload_for(item), "media_sha256": item.get("media_sha256")}
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def plan(posts: list[dict[str, Any]], state: dict[str, Any], now: datetime) -> list[dict[str, Any]]:
    if now.tzinfo is None or now.utcoffset() != timedelta(0):
        raise QueueError("The scheduler clock must use UTC.")
    items = []
    for post in posts:
        due = utc_time(post["due_at"])
        prior = state["items"].get(post["id"])
        if prior is not None:
            status = prior["status"] if prior["fingerprint"] == fingerprint(post) else "changed_after_claim"
        elif post["approved"] is not True:
            status = "not_approved"
        elif due > now:
            status = "future"
        elif now - due > MAX_LATENESS:
            status = "missed_window"
        else:
            status = "due"
        items.append({"id": post["id"], "due_at": post["due_at"], "kind": post["kind"], "status": status})
    return items


class GitLedger:
    """Persist only the ledger file, and require a successful push before proceeding."""

    def __init__(self, path: Path, branch: str = "main") -> None:
        self.path = path.resolve()
        self.branch = branch
        if branch != "main" or path.is_symlink():
            raise QueueError("The production ledger must use main and a regular file.")
        try:
            completed = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True,
                                       capture_output=True, text=True, timeout=20)
            self.root = Path(completed.stdout.strip()).resolve()
            self.relative = self.path.relative_to(self.root).as_posix()
        except (OSError, ValueError, subprocess.SubprocessError):
            raise QueueError("A writable Git checkout is required for the publication ledger.") from None
        if self.relative != "content/publication-state.json":
            raise QueueError("The production ledger must be content/publication-state.json.")

    def _git(self, *arguments: str) -> str:
        try:
            completed = subprocess.run(["git", *arguments], cwd=self.root, check=True,
                                       capture_output=True, text=True, timeout=60)
            return completed.stdout
        except (OSError, subprocess.SubprocessError):
            raise QueueError("The publication ledger could not be committed or pushed; check GitHub Actions.") from None

    def __call__(self, state: dict[str, Any], message: str) -> None:
        # Refuse unrelated staged files instead of accidentally committing them.
        staged = self._git("diff", "--cached", "--name-only").splitlines()
        if staged:
            raise QueueError("The publication ledger requires an initially clean Git index.")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary: str | None = None
        try:
            with tempfile.NamedTemporaryFile("w", dir=self.path.parent, encoding="utf-8", delete=False) as stream:
                temporary = stream.name
                json.dump(state, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        except OSError:
            raise QueueError("The publication ledger could not be written.") from None
        finally:
            if temporary is not None:
                Path(temporary).unlink(missing_ok=True)
        self._git("add", "--", self.relative)
        self._git("commit", "-m", message, "--", self.relative)
        self._git("push", "--porcelain", "origin", "HEAD:" + self.branch)


def safe_publication_result(result: Any) -> dict[str, Any]:
    if (not isinstance(result, dict) or result.get("ok") is not True
            or result.get("mode") != "published" or result.get("username") != ACCOUNT
            or not isinstance(result.get("media_id"), str) or not NUMERIC_ID.fullmatch(result["media_id"])):
        raise QueueError("The publisher did not return a confirmed publication result.")
    public = {"media_id": result["media_id"]}
    for name in ("creation_id", "instagram_user_id", "page_id"):
        value = result.get(name)
        if isinstance(value, str) and NUMERIC_ID.fullmatch(value):
            public[name] = value
    return public


def run_queue(posts: list[dict[str, Any]], state: dict[str, Any], now: datetime, *, execute: bool,
              enabled: bool, persist: Callable[[dict[str, Any], str], None] | None = None,
              poster_factory: Callable[[], Any] | None = None) -> dict[str, Any]:
    items = plan(posts, state, now)
    base = {"ok": True, "mode": "dry_run" if not execute else "disabled", "username": ACCOUNT,
            "checked_at": timestamp(now), "items": items}
    if not execute or not enabled:
        return base
    base["mode"] = "execute"
    selected = next((entry for entry in items if entry["status"] == "due"), None)
    if selected is None:
        return base
    if persist is None or poster_factory is None:
        raise QueueError("Execution requires a durable ledger and the configured publisher.")
    post = next(item for item in posts if item["id"] == selected["id"])
    # Constructing the official publisher validates configuration but makes no network request.
    poster = poster_factory()
    identifier = post["id"]
    entry = {"status": "claimed", "fingerprint": fingerprint(post), "due_at": post["due_at"],
             "claimed_at": timestamp(now)}
    state["items"][identifier] = entry
    persist(state, "Claim Instagram queue item " + identifier)
    # If durable persistence failed, execution never reaches this Meta mutation.
    try:
        result = poster.publish(post["kind"], post["target_url"], payload_for(post))
        entry.update(safe_publication_result(result), status="published",
                     published_at=timestamp(datetime.now(timezone.utc)))
    except Exception as error:
        # Retain the claim even for a failure apparently preceding publication. Never
        # infer a safe automatic retry from transport errors or a missing response.
        entry.update(status="needs_review", error_type="publication_not_confirmed")
        if isinstance(error, MetaError):
            for name in ("http_status", "code", "subcode"):
                value = getattr(error, name, None)
                if type(value) is int and 0 <= value < 10**12:
                    entry[name] = value
            creation = error.creation_id
            if isinstance(creation, str) and NUMERIC_ID.fullmatch(creation):
                entry["creation_id"] = creation
        persist(state, "Quarantine Instagram queue item " + identifier)
        base.update(ok=False, item_id=identifier, status="needs_review",
                    error="Publication was not confirmed. Inspect the account and ledger before manual recovery.")
        base["items"] = plan(posts, state, now)
        return base
    persist(state, "Record Instagram publication " + identifier)
    base.update(item_id=identifier, status="published", media_id=entry["media_id"])
    base["items"] = plan(posts, state, now)
    return base


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("content/schedule.json"))
    parser.add_argument("--state", type=Path, default=Path("content/publication-state.json"))
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="Inspect the queue without any Meta calls (default).")
    modes.add_argument("--execute", action="store_true", help="Publish due items only if the scheduler is enabled.")
    parser.add_argument("--now", help="UTC clock override, allowed only for dry-run validation.")
    args = parser.parse_args(argv)
    try:
        if args.now is not None and args.execute:
            raise QueueError("A clock override cannot be used for execution.")
        now = utc_time(args.now) if args.now is not None else datetime.now(timezone.utc)
        posts = validate_manifest(read_document(args.manifest))
        state = validate_state(read_document(args.state, missing={"version": 1, "items": {}}))
        enabled = os.environ.get("INSTAGRAM_SCHEDULER_ENABLED") == "true"
        account = os.environ.get("INSTAGRAM_USERNAME", ACCOUNT)
        if account != ACCOUNT:
            raise QueueError("The launch account does not match this queue's fixed Instagram account.")
        ledger = GitLedger(args.state) if args.execute and enabled else None
        result = run_queue(posts, state, now, execute=args.execute, enabled=enabled, persist=ledger,
                           poster_factory=lambda: FacebookPoster(FacebookConfig.from_env()))
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["ok"] else 1
    except (QueueError, MetaError) as error:
        # Exception messages defined here and in MetaError never echo input data.
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

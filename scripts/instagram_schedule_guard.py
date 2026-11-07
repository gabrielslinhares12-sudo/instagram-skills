#!/usr/bin/env python3
"""Read-only publication-slot watchdog for Instagram TUE.

This does not post or modify schedule/ledger. It fails visibly when an expected
slot is missing, late, or has an unconfirmed claim. Uses Sao Paulo civil time
and the canonical GitHub publication ledger; no local PC or paid APIs.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from instagram_queue import read_document, validate_manifest, validate_state, utc_time, ACCOUNT

TZ = ZoneInfo("America/Sao_Paulo")
SLOTS = (11, 15, 18)
MINUTES_BEFORE = 35
MINUTES_AFTER = 12


def inspect(posts, ledger, now, day=None):
    if now.tzinfo is None:
        raise ValueError("Watchdog requires timezone-aware datetime.")
    local = now.astimezone(TZ)
    day = day or local.date()
    if isinstance(day, str):
        day = date.fromisoformat(day)
    if not isinstance(day, date):
        raise ValueError("Invalid day.")
    expected = []
    for hour in SLOTS:
        due_local = datetime.combine(day, time(hour, 0), tzinfo=TZ)
        due = due_local.astimezone(timezone.utc)
        matching = [post for post in posts if utc_time(post["due_at"]) == due and post["username"] == ACCOUNT]
        item = matching[0] if matching else None
        claimed = ledger["items"].get(item["id"]) if item else None
        if len(matching) > 1:
            status = "duplicate_slot"
        elif item is None:
            status = "missing"
        elif not item["approved"]:
            status = "not_approved"
        elif claimed is None:
            status = "queued_unconfirmed" if now >= due else "queued"
        elif claimed["status"] == "published":
            status = "published"
        elif claimed["status"] in {"needs_review", "claimed", "awaiting_native_music"}:
            status = claimed["status"]
        else:
            status = "unconfirmed"
        report = {
            "slot": f"{hour:02d}:00", "due_at": due.isoformat(),
            "id": item["id"] if item else None, "status": status,
            "minutes_to_due": round((due-now).total_seconds()/60),
            "media_id": claimed.get("media_id") if claimed else None,
        }
        expected.append(report)
    return {"date": day.isoformat(), "timezone": "America/Sao_Paulo",
            "checked_at": now.isoformat(), "slots": expected}


def gate(result, mode):
    bad = []
    for slot in result["slots"]:
        minutes = slot["minutes_to_due"]
        status = slot["status"]
        if mode == "preflight":
            # Preflight only looks at the imminent slot. A missing post tomorrow
            # cannot stop today's valid publication.
            if -2 <= minutes <= MINUTES_BEFORE and status not in ("queued", "published"):
                bad.append(slot)
        elif mode == "postflight":
            if -120 <= minutes <= -MINUTES_AFTER and status != "published":
                bad.append(slot)
        elif mode == "report":
            pass
        else:
            raise ValueError("Unsupported watchdog mode")
    return bad


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("preflight", "postflight", "report"), default="report")
    parser.add_argument("--schedule", type=Path, default=Path("content/schedule.json"))
    parser.add_argument("--ledger", type=Path, default=Path("content/publication-state.json"))
    parser.add_argument("--now", help="Only for read-only test/replay; ISO8601 UTC offset required")
    parser.add_argument("--date", help="Inspect a specific local calendar date")
    args = parser.parse_args(argv)
    now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(timezone.utc)
    if now.tzinfo is None:
        parser.error("--now must include UTC offset.")
    posts = validate_manifest(read_document(args.schedule))
    ledger = validate_state(read_document(args.ledger))
    result = inspect(posts, ledger, now, args.date)
    problems = gate(result, args.mode)
    result.update(mode=args.mode, ok=not problems, problems=problems)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    for slot in problems:
        print(f"::error title=Instagram {slot['slot']} sem comprovante::"
              f"Falha de publicacao {result['date']} {slot['slot']}, status={slot['status']}, "
              f"post={slot['id'] or 'NAO_PREPARADO'}. Nao reenviar se a Meta ja tem o post.",
              flush=True)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())

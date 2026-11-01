#!/usr/bin/env python3
"""Safely summarize cloud queue state; no credentials or Meta writes."""
from __future__ import annotations
from collections import Counter
import json
import os
from pathlib import Path
import sys


ALLOWED_STATUSES = frozenset({
    "future", "not_approved", "published", "claimed", "needs_review",
    "changed_after_claim", "missed_window", "due", "requires_native_music",
})


def summary(plan: dict) -> tuple[dict[str, int], str]:
    items = plan.get("items")
    if plan.get("ok") is not True or not isinstance(items, list):
        raise ValueError("Invalid plan document.")
    count = Counter()
    for item in items:
        status = item.get("status") if isinstance(item, dict) else None
        if status not in ALLOWED_STATUSES:
            raise ValueError("Unrecognized plan status.")
        count[status] += 1
    lines = [
        "### Instagram cloud — fila segura",
        "- Runner: GitHub-hosted ubuntu-latest, sem PC ou telefone",
        "- Frequência: cron de 10 minutos, sujeito a atrasos do GitHub",
        "- Itens: " + ", ".join(f"`{k}`: {v}" for k, v in sorted(count.items())),
        "- `requires_native_music`: bloqueio intencional; API não adiciona música a carrosséis.",
        "- `missed_window`: nenhuma publicação tardia não autorizada.",
    ]
    return dict(count), "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: instagram_cloud_report.py plan.json", file=sys.stderr)
        return 2
    try:
        plan = json.loads(Path(args[0]).read_text(encoding="utf-8"))
        counts, body = summary(plan)
        target = os.environ.get("GITHUB_STEP_SUMMARY")
        if target:
            with open(target, "a", encoding="utf-8") as file:
                file.write(body)
        print(json.dumps({"ok": True, "counts": counts}, ensure_ascii=False))
        return 0
    except (ValueError, OSError):
        print('{"ok":false,"error":"Cannot summarize validated queue plan."}', file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

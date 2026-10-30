#!/usr/bin/env python3
"""Verify current publishing grants and account identity using GET requests only."""
from __future__ import annotations

import json
import sys
from typing import Any

from facebook_poster import FacebookConfig, FacebookPoster
from meta_poster import MetaError

REQUIRED = frozenset({'instagram_basic', 'instagram_content_publish',
                      'pages_show_list', 'pages_read_engagement'})


def check(poster: Any) -> dict[str, Any]:
    # The object initially holds the user token; discovery later selects a Page token.
    response = poster._request('GET', 'me/permissions')
    records = response.get('data')
    if not isinstance(records, list):
        raise MetaError('Meta returned invalid permission metadata.')
    granted = {item.get('permission') for item in records
               if isinstance(item, dict) and item.get('status') == 'granted'
               and isinstance(item.get('permission'), str)}
    missing = sorted(REQUIRED - granted)
    if missing:
        return {'ok': False, 'mode': 'preflight', 'missing_permissions': missing}
    identity = poster.check_identity()
    return {**identity, 'mode': 'preflight', 'required_permissions_granted': sorted(REQUIRED),
            'publishing_exercised': False}


def main() -> int:
    try:
        result = check(FacebookPoster(FacebookConfig.from_env()))
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result['ok'] else 1
    except MetaError as error:
        print(json.dumps(error.public(), ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

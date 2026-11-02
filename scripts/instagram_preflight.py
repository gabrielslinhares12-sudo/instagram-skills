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
    try:
        response = poster._request('GET', 'me/permissions')
    except MetaError as error:
        # Graph's /me/permissions can deny inspection (code 200) even
        # while Page/Instagram identity reads remain authorized. A denied
        # permissions inspection does NOT prove publishing permission.
        # Verify the exact account through the independent Page relationship
        # and let Meta's actual publish endpoint enforce publishing rights.
        # Preserve explicit uncertainty rather than claiming scopes granted.
        if error.code != 200:
            error.preflight_stage = 'read_permissions'
            raise
        try:
            identity = poster.check_identity()
        except MetaError as identity_error:
            identity_error.preflight_stage = 'verify_account_identity'
            raise
        if identity.get('ok') is not True or identity.get('username') != 'temumaexplicacao':
            mismatch = MetaError('The Instagram account identity does not match the approved destination.')
            mismatch.preflight_stage = 'verify_account_identity'
            raise mismatch
        return {**identity, 'mode': 'preflight', 'permission_inspection': 'denied_code_200',
                'permissions_verified': False, 'required_permissions_granted': [],
                'publishing_exercised': False}
    records = response.get('data')
    if not isinstance(records, list):
        raise MetaError('Meta returned invalid permission metadata.')
    granted = {item.get('permission') for item in records
               if isinstance(item, dict) and item.get('status') == 'granted'
               and isinstance(item.get('permission'), str)}
    missing = sorted(REQUIRED - granted)
    if missing:
        return {'ok': False, 'mode': 'preflight', 'missing_permissions': missing}
    try:
        identity = poster.check_identity()
    except MetaError as error:
        error.preflight_stage = 'verify_account_identity'
        raise
    return {**identity, 'mode': 'preflight', 'required_permissions_granted': sorted(REQUIRED),
            'publishing_exercised': False}


def main() -> int:
    try:
        result = check(FacebookPoster(FacebookConfig.from_env()))
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result['ok'] else 1
    except MetaError as error:
        diagnostic = error.public()
        diagnostic['preflight_stage'] = getattr(error, 'preflight_stage', 'initialize_connection')
        diagnostic['publishing_exercised'] = False
        if error.code == 200:
            diagnostic['next_action'] = (
                'Review the Facebook/Instagram connection and publishing grants; '
                'reauthorize Meta permissions and retest before any retry.'
            )
        print(json.dumps(diagnostic, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

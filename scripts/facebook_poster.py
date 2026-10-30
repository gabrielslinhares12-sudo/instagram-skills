#!/usr/bin/env python3
"""Use official Facebook Login to publish one approved Instagram image.

The Facebook user token discovers authorized Pages and the linked Instagram
account. A Page token is retained in memory only and revalidates that link.
Run --check for read-only discovery and validation. The publication contract
matches meta_poster.py: KIND TARGET_URL argv and approved JSON on stdin.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
import os
import sys
from typing import Any, Mapping

from meta_poster import API_VERSION, NUMERIC_ID, USERNAME, Config, MetaError, MetaPoster


FACEBOOK_API_HOST = "https://graph.facebook.com"
MAX_PAGE_BATCHES = 20
PAGE_BATCH_SIZE = 100
PAGE_FIELDS = "id,name,access_token,instagram_business_account{id,username}"
RELATIONSHIP_FIELDS = "id,instagram_business_account{id,username}"
CHECK_STAGES = frozenset({"configuration", "discovery_user_token", "relationship_page_token"})


def credential_summary(value: str) -> dict[str, Any]:
    """Describe common copy errors without returning any credential characters.

    Prefix families are diagnostic hints only: access tokens are opaque, so
    these heuristics never decide whether a credential may be used.
    """
    token = value.strip()
    if not token:
        shape = "empty"
    elif token.isascii() and token.isdigit():
        shape = "digits_only"
    elif token.startswith("EAA"):
        shape = "facebook_like"
    elif token.startswith("IG"):
        shape = "instagram_like"
    else:
        shape = "other"
    return {"characters": len(token), "shape": shape,
            "has_outer_whitespace": value != token,
            "has_internal_whitespace": any(character.isspace() for character in token),
            "wrapped_in_quotes": len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'"}


@dataclass(frozen=True)
class FacebookConfig:
    user_access_token: str = field(repr=False)
    version: str
    username: str
    page_id: str | None = None
    instagram_user_id: str | None = None

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "FacebookConfig":
        source = os.environ if environ is None else environ
        token = source.get("FACEBOOK_USER_ACCESS_TOKEN", "").strip()
        version = source.get("INSTAGRAM_API_VERSION", "").strip()
        username = source.get("INSTAGRAM_USERNAME", "temumaexplicacao").strip()
        if not token or any(character.isspace() for character in token):
            raise MetaError("Set FACEBOOK_USER_ACCESS_TOKEN for Facebook Login in the launch environment.")
        if not API_VERSION.fullmatch(version):
            raise MetaError("Set INSTAGRAM_API_VERSION in vN.N format.")
        if not USERNAME.fullmatch(username):
            raise MetaError("Set INSTAGRAM_USERNAME to the expected account username.")
        filters = []
        for variable in ("FACEBOOK_PAGE_ID", "FACEBOOK_INSTAGRAM_USER_ID"):
            value = source.get(variable, "").strip()
            if value and not NUMERIC_ID.fullmatch(value):
                raise MetaError("Optional Facebook Page and Instagram ID filters must be numeric.")
            filters.append(value or None)
        return cls(token, version, username.lower(), *filters)


@dataclass(frozen=True)
class PageAccount:
    page_id: str
    instagram_user_id: str
    username: str
    access_token: str = field(repr=False)


class FacebookPoster(MetaPoster):
    """A fixed Facebook Graph host; Instagram Login tokens are never read."""

    api_host = FACEBOOK_API_HOST

    def __init__(self, facebook_config: FacebookConfig, session: Any = None) -> None:
        self.facebook_config = facebook_config
        self.page_id: str | None = None
        self.check_stage = "configuration"
        super().__init__(self._user_config(), session)

    def _user_config(self) -> Config:
        configured = self.facebook_config
        # No Instagram ID is trusted until Page discovery and validation finish.
        return Config(configured.user_access_token, configured.instagram_user_id or "0",
                      configured.version, configured.username)

    def _candidate(self, item: Any) -> PageAccount | None:
        if not isinstance(item, dict):
            raise MetaError("Facebook returned an invalid authorized Page record.")
        account = item.get("instagram_business_account")
        if not isinstance(account, dict):
            return None
        username = account.get("username")
        if not isinstance(username, str) or username.lower() != self.facebook_config.username:
            return None
        page_id, instagram_id = item.get("id"), account.get("id")
        if (not isinstance(page_id, str) or not NUMERIC_ID.fullmatch(page_id)
                or not isinstance(instagram_id, str) or not NUMERIC_ID.fullmatch(instagram_id)):
            raise MetaError("Facebook returned an invalid Page or Instagram identifier.")
        expected = self.facebook_config
        if expected.page_id is not None and page_id != expected.page_id:
            return None
        if expected.instagram_user_id is not None and instagram_id != expected.instagram_user_id:
            return None
        token = item.get("access_token")
        if not isinstance(token, str) or not token or any(character.isspace() for character in token):
            raise MetaError("The matching Page has no usable Page access token.")
        return PageAccount(page_id, instagram_id, username.lower(), token)

    def _discover(self) -> PageAccount:
        candidates: dict[tuple[str, str], PageAccount] = {}
        cursor: str | None = None
        cursors_seen: set[str] = set()
        for _ in range(MAX_PAGE_BATCHES):
            params: dict[str, Any] = {"fields": PAGE_FIELDS, "limit": PAGE_BATCH_SIZE}
            if cursor is not None:
                params["after"] = cursor
            batch = self._request("GET", "me/accounts", params=params)
            records = batch.get("data")
            if not isinstance(records, list):
                raise MetaError("Facebook returned an invalid authorized Pages list.")
            for record in records:
                candidate = self._candidate(record)
                if candidate is not None:
                    candidates[(candidate.page_id, candidate.instagram_user_id)] = candidate
            paging = batch.get("paging", {})
            if not isinstance(paging, dict):
                raise MetaError("Facebook returned invalid Page pagination metadata.")
            if not paging.get("next"):
                break
            # Never follow paging.next: it may contain credentials or another host.
            cursors = paging.get("cursors")
            cursor = cursors.get("after") if isinstance(cursors, dict) else None
            if (not isinstance(cursor, str) or not cursor or len(cursor) > 4096
                    or cursor in cursors_seen):
                raise MetaError("Facebook Page pagination is missing a usable continuation cursor.")
            cursors_seen.add(cursor)
        else:
            raise MetaError("Facebook Page discovery exceeded its bounded pagination limit.")
        if not candidates:
            raise MetaError("No authorized Page matches the expected linked Instagram account and ID filters.")
        if len(candidates) != 1:
            raise MetaError("Multiple Pages match. Set FACEBOOK_PAGE_ID to select the authorized Page.")
        return next(iter(candidates.values()))

    def check_identity(self) -> dict[str, Any]:
        self.page_id = None
        # Always discover with the user token, including when an object is reused.
        self.config = self._user_config()
        self.check_stage = "discovery_user_token"
        selected = self._discover()
        self.config = Config(selected.access_token, selected.instagram_user_id,
                             self.facebook_config.version, selected.username)
        self.check_stage = "relationship_page_token"
        relationship = self._request("GET", selected.page_id,
                                     params={"fields": RELATIONSHIP_FIELDS})
        account = relationship.get("instagram_business_account")
        if (relationship.get("id") != selected.page_id or not isinstance(account, dict)
                or account.get("id") != selected.instagram_user_id
                or not isinstance(account.get("username"), str)
                or account["username"].lower() != selected.username):
            raise MetaError("The Page-to-Instagram relationship changed or does not match the expected account.")
        self.page_id = selected.page_id
        return {"ok": True, "mode": "check", "login": "facebook", "page_id": selected.page_id,
                "instagram_user_id": selected.instagram_user_id, "username": selected.username}

    def publish(self, kind: str, target_url: str, payload: Any) -> dict[str, Any]:
        result = super().publish(kind, target_url, payload)
        result.update({"login": "facebook", "page_id": self.page_id,
                       "instagram_user_id": self.config.user_id})
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Discover and validate accounts without publishing.")
    parser.add_argument("kind", nargs="?")
    parser.add_argument("target_url", nargs="?")
    args = parser.parse_args(argv)
    poster: FacebookPoster | None = None
    try:
        poster = FacebookPoster(FacebookConfig.from_env())
        if args.check:
            if args.kind is not None or args.target_url is not None:
                raise MetaError("Use --check without publication arguments.")
            result = poster.check_identity()
        else:
            if args.kind is None or args.target_url is None:
                raise MetaError("Supply kind and target_url, or use --check.")
            try:
                payload = json.load(sys.stdin)
            except (ValueError, UnicodeError):
                raise MetaError("The stdin payload must be valid JSON.") from None
            result = poster.publish(args.kind, args.target_url, payload)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except MetaError as error:
        public = error.public()
        if args.check:
            stage = poster.check_stage if poster is not None else "configuration"
            public["diagnostics"] = {
                "stage": stage if stage in CHECK_STAGES else "unknown",
                "user_token": credential_summary(os.environ.get("FACEBOOK_USER_ACCESS_TOKEN", "")),
            }
        print(json.dumps(public, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Publish one approved image through Instagram Login's official Meta API.

The custom-poster contract is: KIND TARGET_URL argv and a JSON object on stdin.
Run --check to validate credentials and account identity without creating media.
Credentials and the custom-poster command belong in the launch environment.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from http.client import HTTPException
import json
import os
import re
import sys
import time
from typing import Any, Mapping
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


API_HOST = "https://graph.instagram.com"
USERNAME = re.compile(r"[A-Za-z0-9._]{1,30}\Z")
NUMERIC_ID = re.compile(r"[0-9]{1,40}\Z")
API_VERSION = re.compile(r"v[0-9]+\.[0-9]+\Z")
POLL_SECONDS = 120.0
POLL_INTERVAL = 2.0


class MetaError(Exception):
    """An error whose public fields never contain API messages or credentials."""

    def __init__(self, message: str, *, http_status: int | None = None,
                 code: int | None = None, subcode: int | None = None) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.code = code
        self.subcode = subcode
        self.creation_id: str | None = None
        self.write_attempted = False

    def public(self) -> dict[str, Any]:
        result: dict[str, Any] = {"ok": False, "error": str(self)}
        for name in ("http_status", "code", "subcode", "creation_id"):
            value = getattr(self, name)
            if value is not None:
                result[name] = value
        if self.write_attempted or self.creation_id:
            result["retry_notice"] = (
                "Do not retry automatically. Check the container and account "
                "before another publication attempt."
            )
        return result


@dataclass(frozen=True)
class Config:
    access_token: str
    user_id: str
    version: str
    username: str

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Config":
        source = os.environ if environ is None else environ
        token = source.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
        user_id = source.get("INSTAGRAM_USER_ID", "").strip()
        version = source.get("INSTAGRAM_API_VERSION", "").strip()
        username = source.get("INSTAGRAM_USERNAME", "temumaexplicacao").strip()
        if not token or any(c.isspace() for c in token):
            raise MetaError("Set INSTAGRAM_ACCESS_TOKEN in the launch environment.")
        if not NUMERIC_ID.fullmatch(user_id):
            raise MetaError("Set a numeric INSTAGRAM_USER_ID.")
        if not API_VERSION.fullmatch(version):
            raise MetaError("Set INSTAGRAM_API_VERSION in vN.N format.")
        if not USERNAME.fullmatch(username):
            raise MetaError("Set INSTAGRAM_USERNAME to the expected account username.")
        return cls(token, user_id, version, username.lower())


def profile_username(target_url: str) -> str:
    """Accept only a specific Instagram profile, never a composer or post URL."""
    try:
        parsed = urlsplit(target_url)
        username = parsed.path.strip("/")
        valid = (
            parsed.scheme == "https"
            and parsed.netloc.lower() in {"instagram.com", "www.instagram.com"}
            and not parsed.query and not parsed.fragment
            and parsed.path in {f"/{username}", f"/{username}/"}
            and USERNAME.fullmatch(username)
        )
    except (ValueError, TypeError):
        valid = False
    if not valid:
        raise MetaError("The target must be an HTTPS Instagram profile URL.")
    return username.lower()


def validate_payload(kind: str, target_url: str, payload: Any,
                     config: Config) -> tuple[str, str]:
    """Reject unsupported requests before even checking the remote account."""
    if not isinstance(payload, dict):
        raise MetaError("The stdin payload must be a JSON object.")
    if payload.get("kind") != kind or payload.get("target_url") != target_url:
        raise MetaError("The argv kind and target must match the stdin payload.")
    if kind != "post":
        raise MetaError("Only a single-image post is supported; no Reels, carousels or Stories.")
    if payload.get("scheduled_time") is not None:
        raise MetaError("Scheduling is unsupported. Do not send scheduled_time.")
    if payload.get("media"):
        raise MetaError("Local media is unsupported. Supply one hosted HTTPS media_urls item.")
    if profile_username(target_url) != config.username:
        raise MetaError("The target profile does not match INSTAGRAM_USERNAME.")
    if payload.get("approved") is not True:
        raise MetaError("Explicit approved=true is required after reviewing the final image and caption.")
    caption = payload.get("draft_text")
    if not isinstance(caption, str) or len(caption) > 2200:
        raise MetaError("draft_text must be a string of at most 2200 characters.")
    urls = payload.get("media_urls")
    if not isinstance(urls, list) or len(urls) != 1 or not isinstance(urls[0], str):
        raise MetaError("Supply exactly one hosted HTTPS image in media_urls.")
    try:
        parsed = urlsplit(urls[0])
        valid_url = (parsed.scheme == "https" and bool(parsed.hostname)
                     and parsed.username is None and parsed.password is None
                     and not parsed.fragment)
        parsed.port  # Reject malformed port syntax without printing the URL.
    except ValueError:
        valid_url = False
    if not valid_url:
        raise MetaError("The image URL must use HTTPS without credentials or a fragment.")
    allowed = {"kind", "target_url", "draft_text", "approved", "media_urls", "media", "scheduled_time"}
    if set(payload) - allowed:
        raise MetaError("The payload contains unsupported options.")
    return caption, urls[0]


def _numeric_code(value: Any) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool) and 0 <= value < 10**12:
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]{1,12}", value):
        return int(value)
    return None


def _response_id(data: dict[str, Any]) -> str:
    value = data.get("id")
    if not isinstance(value, str) or not NUMERIC_ID.fullmatch(value):
        raise MetaError("Meta returned an invalid or missing media identifier.")
    return value


class NoRedirect(HTTPRedirectHandler):
    """Never forward an authenticated request to a redirect destination."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class Response:
    status_code: int
    body: bytes

    def json(self) -> Any:
        return json.loads(self.body.decode("utf-8"))


class UrllibTransport:
    """Small standard-library transport with no retries and no redirects."""

    def __init__(self) -> None:
        self.opener = build_opener(NoRedirect())

    def request(self, method: str, url: str, *, headers: dict[str, str],
                params: dict[str, Any] | None, data: dict[str, Any] | None,
                timeout: float, allow_redirects: bool) -> Response:
        if allow_redirects:
            raise MetaError("Authenticated redirects must remain disabled.")
        if params:
            url += "?" + urlencode(params)
        encoded = None if data is None else urlencode(data).encode("utf-8")
        request = Request(url, data=encoded, headers=headers, method=method)
        try:
            response = self.opener.open(request, timeout=timeout)
        except HTTPError as error:
            response = error
        with response:
            # Limit untrusted response data retained in memory, including errors.
            return Response(response.code, response.read(1024 * 1024))


class MetaPoster:
    api_host = API_HOST

    def __init__(self, config: Config, session: Any = None) -> None:
        self.config = config
        self.session = UrllibTransport() if session is None else session
        self.creation_id: str | None = None
        self.write_attempted = False

    def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None,
                 data: dict[str, Any] | None = None,
                 timeout: float = 20) -> dict[str, Any]:
        if method == "POST":
            self.write_attempted = True
        try:
            response = self.session.request(
                method, f"{self.api_host}/{self.config.version}/{path}",
                headers={"Authorization": f"Bearer {self.config.access_token}"},
                params=params, data=data, timeout=timeout, allow_redirects=False,
            )
        except (OSError, HTTPException):
            raise MetaError("The Meta request failed or timed out; no raw transport details are shown.") from None
        if 300 <= response.status_code < 400:
            raise MetaError("Meta returned a redirect, which was refused.", http_status=response.status_code)
        try:
            body = response.json()
        except (ValueError, TypeError, UnicodeError):
            raise MetaError("Meta returned an invalid JSON response.", http_status=response.status_code) from None
        if not isinstance(body, dict):
            raise MetaError("Meta returned an unexpected response shape.", http_status=response.status_code)
        if not 200 <= response.status_code < 300 or "error" in body:
            error = body.get("error")
            details = error if isinstance(error, dict) else {}
            raise MetaError("Meta rejected the request.", http_status=response.status_code,
                            code=_numeric_code(details.get("code")),
                            subcode=_numeric_code(details.get("error_subcode")))
        return body

    def check_identity(self) -> dict[str, Any]:
        identity = self._request("GET", "me", params={"fields": "user_id,username"})
        user_id, username = identity.get("user_id"), identity.get("username")
        if (str(user_id) != self.config.user_id or not isinstance(username, str)
                or username.lower() != self.config.username):
            raise MetaError("The connected Instagram identity does not match the configured ID and username.")
        return {"ok": True, "mode": "check", "user_id": self.config.user_id,
                "username": self.config.username}

    def _wait_until_finished(self) -> None:
        deadline = time.monotonic() + POLL_SECONDS
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise MetaError("Media processing did not finish within 120 seconds.")
            status = self._request(
                "GET", str(self.creation_id), params={"fields": "status_code"},
                timeout=min(20, remaining),
            ).get("status_code")
            if time.monotonic() >= deadline:
                raise MetaError("Media processing did not finish within 120 seconds.")
            if status == "FINISHED":
                return
            if status != "IN_PROGRESS":
                raise MetaError("Media processing failed or returned an unsupported state.")
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(POLL_INTERVAL, remaining))

    def publish(self, kind: str, target_url: str, payload: Any) -> dict[str, Any]:
        self.creation_id = None
        self.write_attempted = False
        caption, image_url = validate_payload(kind, target_url, payload, self.config)
        self.check_identity()
        try:
            created = self._request("POST", f"{self.config.user_id}/media",
                                    data={"image_url": image_url, "caption": caption})
            self.creation_id = _response_id(created)
            self._wait_until_finished()
            published = self._request("POST", f"{self.config.user_id}/media_publish",
                                      data={"creation_id": self.creation_id})
            return {"ok": True, "mode": "published", "creation_id": self.creation_id,
                    "media_id": _response_id(published), "username": self.config.username}
        except MetaError as error:
            error.creation_id = self.creation_id
            error.write_attempted = self.write_attempted
            raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate identity without publishing.")
    parser.add_argument("kind", nargs="?")
    parser.add_argument("target_url", nargs="?")
    args = parser.parse_args(argv)
    try:
        poster = MetaPoster(Config.from_env())
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
        print(json.dumps(error.public(), ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

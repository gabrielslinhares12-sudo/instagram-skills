#!/usr/bin/env python3
"""Opt-in cloud experiment: unofficial Instagram mobile carousel with native music.

NOT an official Meta Graph API. Requires an explicitly approved music/title
and a pre-existing authenticated instagrapi session in an Actions secret.
Never prints cookies, tokens, session data, tracks or private API messages.
The durable Git ledger protects against duplicate/ambiguous publication.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

from instagram_queue import (
    ACCOUNT, GitLedger, QueueError, read_document, run_queue,
    validate_manifest, validate_state, utc_time, timestamp
)

BASE = "raw.githubusercontent.com"
OWNER_REPO = "/gabrielslinhares12-sudo/instagram-skills/"
MAX_JPEG = 8 * 1024 * 1024
ID = re.compile(r"[0-9]{3,30}\Z")
SHORTCODE = re.compile(r"[a-zA-Z0-9_-]{5,40}\Z")


class PrivateMusicError(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def normalize(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value)
    return " ".join("".join(c for c in folded if not unicodedata.combining(c)).casefold().split())


def fetch_verified_jpegs(post: dict, folder: Path) -> list[Path]:
    urls, hashes = post["media_urls"], post.get("media_sha256")
    if not isinstance(hashes, list) or len(hashes) != len(urls) or not 2 <= len(urls) <= 10:
        raise PrivateMusicError("As artes precisam ter SHA256 e quantidade válida.")
    from PIL import Image
    opener = build_opener(NoRedirect())
    paths = []
    for i, (url, expected_hash) in enumerate(zip(urls, hashes), 1):
        u = urlsplit(url)
        if (u.scheme != "https" or u.hostname != BASE or
            not u.path.startswith(OWNER_REPO) or not u.path.endswith(".jpg") or
            u.query or u.fragment or u.username or u.password):
            raise PrivateMusicError("Fonte de arte fora do GitHub aprovado.")
        try:
            with opener.open(Request(url, headers={"User-Agent": "TUE-InstagramCloud/1"}), timeout=30) as response:
                content = response.read(MAX_JPEG + 1)
        except Exception:
            raise PrivateMusicError("Não foi possível obter imagem original aprovada.") from None
        if len(content) > MAX_JPEG or hashlib.sha256(content).hexdigest() != expected_hash:
            raise PrivateMusicError("JPG original ausente ou com hash divergente.")
        try:
            with Image.open(io.BytesIO(content)) as image:
                if image.format != "JPEG" or image.size != (1080, 1350):
                    raise PrivateMusicError("JPG inválido ou não 1080x1350.")
        except (OSError, ValueError):
            raise PrivateMusicError("A arte aprovada está inválida.") from None
        path = folder / f"{i:02d}.jpg"
        path.write_bytes(content)
        paths.append(path)
    return paths


def choose_approved_track(client, post: dict):
    title, artist = post.get("music_track", ""), post.get("music_artist", "")
    if not title or not artist or len(title) > 120 or len(artist) > 120:
        raise PrivateMusicError("Título e artista do instrumental devem ser aprovados.")
    # Search through Instagram's music surface. Never pick an unrelated
    # 'trending' track when the approved instrumental is unavailable.
    tracks = client.search_music(title)
    matches = []
    for track in tracks:
        actual_title = str(getattr(track, "title", "") or "")
        actual_artist = str(getattr(track, "subtitle", "") or getattr(track, "artist", "") or "")
        if normalize(title) in normalize(actual_title) and normalize(artist) in normalize(actual_artist):
            matches.append(track)
    if len(matches) != 1:
        raise PrivateMusicError("Faixa instrumental não encontrada de modo inequívoco na biblioteca.")
    return matches[0]


def decode_session() -> dict:
    encoded = os.environ.get("INSTAGRAM_PRIVATE_SESSION_B64", "").strip()
    if not encoded or len(encoded) > 100_000:
        raise PrivateMusicError("Sessão móvel não oficial não configurada no GitHub Secret.")
    try:
        data = json.loads(base64.b64decode(encoded, validate=True))
    except (ValueError, TypeError):
        raise PrivateMusicError("Sessão móvel inválida.") from None
    if not isinstance(data, dict) or not data:
        raise PrivateMusicError("Sessão móvel vazia ou inválida.")
    return data


class InstagramPrivateMusicPoster:
    def __init__(self, post: dict) -> None:
        # The queue constructs the poster BEFORE creating the durable claim.
        # Preflight failures do not consume the one-shot publication slot.
        self.post = post
        self.temp = tempfile.TemporaryDirectory()
        try:
            self.paths = fetch_verified_jpegs(post, Path(self.temp.name))
            from instagrapi import Client
            self.client = Client()
            self.client.set_settings(decode_session())
            identity = self.client.account_info()
            username = str(getattr(identity, "username", "")).lower()
            if username != ACCOUNT:
                raise PrivateMusicError("Sessão móvel não pertence a @temumaexplicacao.")
            self.track = choose_approved_track(self.client, post)
            # Verify no matching publication was already made outside Git ledger.
            user_pk = str(getattr(identity, "pk", ""))
            if not user_pk:
                raise PrivateMusicError("Identidade da conta não pôde ser confirmada.")
            existing = self.client.user_medias(user_pk, amount=20)
            self.duplicate = None
            for media in existing:
                caption = str(getattr(media, "caption_text", "") or "")
                pages = getattr(media, "resources", None) or []
                if caption == post["caption"] and len(pages) == len(self.paths):
                    pk = str(getattr(media, "pk", "") or "")
                    if ID.fullmatch(pk):
                        detail = self.client.media_info_v1(pk)
                        if not getattr(detail, "music_metadata", None):
                            raise PrivateMusicError(
                                "Publicação igual já existe, mas sem música confirmada."
                            )
                        self.duplicate = pk
                        break
        except Exception:
            self.temp.cleanup()
            raise PrivateMusicError("Não foi possível validar sessão, música ou artes. Verificar a conta.") from None

    def publish(self, kind: str, target_url: str, payload: dict) -> dict:
        try:
            if (kind != "carousel" or target_url != self.post["target_url"] or
                payload.get("draft_text") != self.post["caption"] or
                payload.get("media_urls") != self.post["media_urls"]):
                raise PrivateMusicError("Dados diferentes do carrossel aprovado.")
            if self.duplicate:
                return {"ok": True, "mode": "published", "username": ACCOUNT,
                        "media_id": self.duplicate}
            # One write attempt only. Instagram may accept it even on timeout.
            media = self.client.album_upload_with_music(
                paths=self.paths, caption=self.post["caption"], track=self.track
            )
            pk = str(getattr(media, "pk", "") or "")
            if not ID.fullmatch(pk):
                raise PrivateMusicError("Instagram não confirmou o identificador da publicação.")
            # Check the posted carousel still has music. Lack of proof quarantines
            # it as uncertain; a retry must never silently duplicate the post.
            verified = self.client.media_info_v1(pk)
            metadata = getattr(verified, "music_metadata", None)
            if not metadata:
                raise PrivateMusicError("Carrossel enviado, mas música não pôde ser confirmada.")
            return {"ok": True, "mode": "published", "username": ACCOUNT, "media_id": pk}
        finally:
            self.temp.cleanup()


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    execute = argv == ["--execute"]
    if argv not in (["--execute"], ["--dry-run"]):
        print('{"ok":false,"error":"Usar --dry-run ou --execute."}')
        return 2
    try:
        posts = validate_manifest(read_document(Path("content/schedule.json")))
        state = validate_state(read_document(Path("content/publication-state.json")))
        now = datetime.now(timezone.utc)
        candidates = [p for p in posts if p["kind"] == "carousel" and
                      p.get("distribution_mode", "native_music_carousel") == "native_music_carousel"]
        enabled = (os.environ.get("INSTAGRAM_PRIVATE_PUBLISH_ENABLED") == "true" and
                   os.environ.get("INSTAGRAM_PRIVATE_RISK_ACCEPTED") == "true")
        if execute and not enabled:
            raise PrivateMusicError("O método não oficial exige habilitação explícita e aceite de risco.")
        # Keep only the native-music carousels; official queue manages other types.
        selected = [p for p in candidates if p["approved"] and
                    p.get("private_api_authorized") is True and
                    p.get("music_track") and p.get("music_artist")]
        if not execute:
            print(json.dumps({"ok": True, "mode": "dry_run_private",
                              "pending_native_carousels": len(candidates),
                              "explicitly_authorized": len(selected),
                              "cloud_runner": True}, ensure_ascii=False))
            return 0
        from instagram_queue import plan, MAX_LATENESS
        due = [p for p in selected if (p["id"] not in state["items"] and
                 utc_time(p["due_at"]) <= now <= utc_time(p["due_at"]) + MAX_LATENESS)]
        if not due:
            print('{"ok":true,"mode":"private_no_due_post"}')
            return 0
        due = sorted(due, key=lambda p: utc_time(p["due_at"]))[:1]
        ledger = GitLedger(Path("content/publication-state.json"))
        result = run_queue(due, state, now, execute=True, enabled=True, private_music=True,
                           persist=ledger,
                           poster_factory=lambda: InstagramPrivateMusicPoster(due[0]))
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("ok") else 1
    except (PrivateMusicError, QueueError) as error:
        # Error types and messages are fixed, never contain auth details.
        print(json.dumps({"ok":False,"error":str(error)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

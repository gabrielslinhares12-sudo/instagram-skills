#!/usr/bin/env python3
"""Instagram TUE: optional Android UI bridge for music on an EXISTING carousel.

Requires an authenticated official Instagram Android app and an ADB-authorized
device. The Meta Graph API and instagrapi cannot add music to an existing post.
Does NOT manage credentials, create media, or modify captions.

Fail-closed: exact account, post permalink, track+artist and screen controls
must be observed before each action. UI changes are NOT claimed as success
until the same original post displays the requested track after reopening.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET

from instagram_queue import GitLedger, QueueError, fingerprint, read_document, validate_manifest, validate_state

ACCOUNT = "temumaexplicacao"
PACKAGE = "com.instagram.android"
POST_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,79}\Z")
LINK = re.compile(r"https://www\.instagram\.com/p/[A-Za-z0-9_-]{5,40}/\Z")
TITLE_INPUT = re.compile(r"[a-zA-Z0-9 ]{3,80}\Z")
ASSIGNMENTS_PATH = Path(__file__).resolve().parent.parent / "content/music-assignments.json"


def normalized(s: str) -> str:
    folded = unicodedata.normalize("NFKD", s).casefold()
    return " ".join("".join(c for c in folded if not unicodedata.combining(c)).split())


def load_music_assignments() -> dict:
    """Approved song intent is kept separate from the immutable published fingerprint."""
    doc = read_document(ASSIGNMENTS_PATH, missing={"version": 1, "assignments": {}})
    if not (isinstance(doc, dict) and doc.get("version") == 1
            and isinstance(doc.get("assignments"), dict)
            and set(doc) == {"version", "assignments"}):
        raise QueueError("O catálogo de músicas aprovadas é inválido.")
    return doc["assignments"]


def approved_music(post: dict, entry: dict, assignments: dict) -> tuple[str | None, str | None]:
    assignment = assignments.get(post["id"])
    current = (post.get("music_track"), post.get("music_artist"))
    if assignment is None:
        return current
    if not (isinstance(assignment, dict)
            and assignment.get("approved_by_owner") is True
            and assignment.get("media_id") == entry.get("media_id")
            and assignment.get("permalink") == entry.get("permalink")
            and isinstance(assignment.get("track"), str)
            and isinstance(assignment.get("artist"), str)
            and 3 <= len(assignment["track"]) <= 120
            and 3 <= len(assignment["artist"]) <= 120):
        raise QueueError("Música aprovada não corresponde exatamente ao post e recibo.")
    selected = (assignment["track"], assignment["artist"])
    if any(current) and current != selected:
        raise QueueError("O manifesto e a aprovação musical divergem; não selecionar faixa.")
    return selected


def select_pending(manifest: dict, ledger: dict, item_id: str | None,
                   assignments: dict | None = None) -> dict:
    posts = validate_manifest(manifest)
    state = validate_state(ledger)
    if assignments is None:
        assignments = load_music_assignments()
    matches = []
    for p in posts:
        entry = state["items"].get(p["id"])
        if not (p["kind"] == "carousel" and p.get("distribution_mode") == "api_carousel_then_native_music"
                and p.get("owner_authorized_two_step_music") is True
                and p.get("approved") is True and isinstance(entry, dict)
                and entry.get("status") == "awaiting_native_music"
                and entry.get("fingerprint") == fingerprint(p)
                and entry.get("media_id") and LINK.fullmatch(str(entry.get("permalink", "")))):
            continue
        music_title, music_artist = approved_music(p, entry, assignments)
        matches.append({"id": p["id"], "permalink": entry["permalink"],
                        "media_id": entry["media_id"],
                        "track": music_title, "artist": music_artist})
    if item_id is None:
        if len(matches) != 1:
            raise QueueError("Escolha o ID; existem zero ou vários carrosséis aguardando música.")
        return matches[0]
    selected = [p for p in matches if p["id"] == item_id]
    if len(selected) != 1:
        raise QueueError("O ID solicitado não tem carrossel elegível aguardando música.")
    return selected[0]


def parse_nodes(xml_text: str) -> list[dict]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        raise QueueError("Android não retornou árvore de acessibilidade válida.") from None
    nodes = []
    for node in root.iter("node"):
        label = (node.attrib.get("text") or "").strip()
        desc = (node.attrib.get("content-desc") or "").strip()
        m = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",
                         node.attrib.get("bounds", ""))
        if m is None:
            continue
        x0, y0, x1, y1 = (int(x) for x in m.groups())
        if x1 <= x0 or y1 <= y0:
            continue
        nodes.append({"label": label, "desc": desc, "rid": node.attrib.get("resource-id", ""),
                      "clickable": node.attrib.get("clickable") == "true",
                      "center": ((x0 + x1) // 2, (y0 + y1) // 2),
                      "bounds": (x0, y0, x1, y1)})
    return nodes


def matches(nodes: list[dict], terms: tuple[str, ...], *, exact: bool = True) -> list[dict]:
    requested = {normalized(t) for t in terms}
    found = []
    used = set()
    for node in nodes:
        values = (normalized(node["label"]), normalized(node["desc"]))
        good = any((v in requested if exact else any(k in v for k in requested)) for v in values if v)
        if good and node["bounds"] not in used:
            found.append(node)
            used.add(node["bounds"])
    return found


class Android:
    def __init__(self, adb: str = "adb") -> None:
        self.adb = adb

    def run(self, *args: str, timeout: int = 25) -> str:
        try:
            p = subprocess.run([self.adb, *args], check=True,
                               capture_output=True, text=True, timeout=timeout)
        except (OSError, subprocess.SubprocessError):
            raise QueueError("ADB indisponível; verifique celular autorizado e depuração USB.") from None
        return p.stdout

    def preflight(self) -> None:
        devices = [line for line in self.run("devices").splitlines()[1:]
                   if line.strip() and line.rstrip().endswith("\tdevice")]
        if len(devices) != 1:
            raise QueueError("É necessário exatamente um Android com ADB autorizado.")
        packages = self.run("shell", "pm", "list", "packages", PACKAGE)
        if f"package:{PACKAGE}" not in packages.splitlines():
            raise QueueError("O Instagram oficial não está instalado no dispositivo.")
        display = self.run("shell", "dumpsys", "window")
        if "mDreamingLockscreen=true" in display or "mShowingLockscreen=true" in display:
            raise QueueError("Desbloqueie o celular para editar música.")

    def nodes(self) -> list[dict]:
        self.run("shell", "uiautomator", "dump", "/sdcard/window.xml", timeout=35)
        raw = self.run("exec-out", "cat", "/sdcard/window.xml")
        return parse_nodes(raw)

    def open(self, permalink: str) -> None:
        self.run("shell", "am", "start", "-W", "-a", "android.intent.action.VIEW",
                 "-d", permalink, "-p", PACKAGE)

    def tap(self, node: dict) -> None:
        x, y = node["center"]
        self.run("shell", "input", "tap", str(x), str(y))

    def click(self, terms: tuple[str, ...], *, timeout: int = 18) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            found = matches(self.nodes(), terms)
            if len(found) == 1:
                self.tap(found[0])
                time.sleep(1)
                return
            if len(found) > 1:
                raise QueueError("Controles duplicados no Instagram; nenhuma ação efetuada.")
            time.sleep(1.2)
        raise QueueError("Controle do Instagram não encontrado; interface pode ter mudado.")

    def wait_for(self, terms: tuple[str, ...], *, timeout: int = 20) -> list[dict]:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            snapshot = self.nodes()
            if matches(snapshot, terms):
                return snapshot
            time.sleep(1.2)
        raise QueueError("Não foi possível confirmar o controle na interface do aplicativo.")

    def search(self, title: str) -> None:
        if not TITLE_INPUT.fullmatch(title):
            raise QueueError("A busca automática ADB exige título ASCII simples; usar o app manualmente.")
        self.click(("Pesquisar", "Pesquisar música", "Buscar", "Search", "Search music"))
        self.run("shell", "input", "text", title.replace(" ", "%s"))

    def choose_exact(self, title: str, artist: str) -> None:
        wanted = normalized(title)
        singer = normalized(artist)
        nodes = self.nodes()
        candidates = matches(nodes, (title,))
        artists = matches(nodes, (artist,))
        # Exact, same visual result band. Do not guess among similar tracks.
        pairs = [(a, b) for a in candidates for b in artists
                 if abs(a["center"][1]-b["center"][1]) <= 150]
        if len(pairs) != 1 or normalized(pairs[0][0]["label"] or pairs[0][0]["desc"]) != wanted or \
                normalized(pairs[0][1]["label"] or pairs[0][1]["desc"]) != singer:
            raise QueueError("Faixa e artista não encontrados juntos, de forma única, na biblioteca.")
        self.tap(pairs[0][0])

    def ensure_account(self) -> None:
        nodes = self.nodes()
        if not matches(nodes, (ACCOUNT,)):
            raise QueueError("Não foi possível confirmar @temumaexplicacao no post exibido.")

    def edit_track(self, permalink: str, track: str, artist: str) -> None:
        self.open(permalink)
        self.wait_for((ACCOUNT,), timeout=35)
        self.ensure_account()
        self.click(("Mais opções", "More options", "Opções", "More"))
        self.click(("Editar", "Edit"))
        self.click(("Adicionar música", "Add music"))
        self.search(track)
        self.choose_exact(track, artist)
        self.click(("Concluir", "Done", "Avançar", "Next"))
        # Save must be a named accessible control, NEVER a blind top-right tap.
        self.click(("Salvar", "Save", "Concluir", "Done"))
        self.open(permalink)
        self.wait_for((ACCOUNT,), timeout=30)
        snapshot = self.nodes()
        if not matches(snapshot, (track,)) or not matches(snapshot, (artist,)):
            raise QueueError("Salvar foi tentado, mas faixa e artista não aparecem no mesmo post.")

    def verify_current(self, permalink: str, track: str, artist: str) -> bool:
        self.open(permalink)
        self.wait_for((ACCOUNT,), timeout=35)
        nodes = self.nodes()
        return bool(matches(nodes, (track,)) and matches(nodes, (artist,)))


def save_verified_receipt(post: dict, track: str, artist: str, state_path: Path) -> None:
    manifest = read_document(Path("content/schedule.json"))
    state = validate_state(read_document(state_path))
    current = select_pending(manifest, state, post["id"])
    if current["media_id"] != post["media_id"] or current["permalink"] != post["permalink"]:
        raise QueueError("O ID ou o link da publicação mudou; não atualizar o recibo.")
    record = state["items"][post["id"]]
    record["status"] = "published"
    record["music_status"] = "verified_on_official_android_app"
    record["music_track"] = track
    record["music_artist"] = artist
    record["music_verified_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    GitLedger(state_path)(state, "Verify native Instagram music on existing carousel " + post["id"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", help="ID do carrossel no manifesto")
    parser.add_argument("--track", help="Nome EXATO da música escolhida")
    parser.add_argument("--artist", help="Artista EXATO da música escolhida")
    parser.add_argument("--execute", action="store_true", help="Editar a publicação no aplicativo Android")
    parser.add_argument("--verify-only", action="store_true", help="Verificar música já salva no post")
    parser.add_argument("--adb", default="adb", help="Executável do Android Debug Bridge")
    args = parser.parse_args(argv)
    try:
        manifest = read_document(Path("content/schedule.json"))
        state_path = Path("content/publication-state.json")
        state = read_document(state_path)
        post = select_pending(manifest, state, args.id)
        track = args.track or post.get("track")
        artist = args.artist or post.get("artist")
        overview = {"ok": True, "id": post["id"], "permalink": post["permalink"],
                    "status": "awaiting_native_music", "mobile_required": True,
                    "exact_song_configured": bool(track and artist),
                    "adb_required_for_unattended_completion": True}
        if not args.execute and not args.verify_only:
            print(json.dumps(overview, ensure_ascii=False))
            return 0
        if not track or not artist:
            raise QueueError("Antes de automatizar, escolha o título e artista exatos da música.")
        if args.track and post.get("track") and normalized(args.track) != normalized(post["track"]):
            raise QueueError("A faixa fornecida não coincide com a aprovada no manifesto.")
        if args.artist and post.get("artist") and normalized(args.artist) != normalized(post["artist"]):
            raise QueueError("O artista fornecido não coincide com a aprovação editorial.")
        device = Android(args.adb)
        device.preflight()
        if args.execute:
            device.edit_track(post["permalink"], track, artist)
        if not device.verify_current(post["permalink"], track, artist):
            raise QueueError("A música não pôde ser confirmada na publicação existente.")
        save_verified_receipt(post, track, artist, state_path)
        print(json.dumps({"ok": True, "status": "published",
                          "music_status": "verified_on_official_android_app",
                          "id":post["id"], "permalink": post["permalink"]}, ensure_ascii=False))
        return 0
    except QueueError as error:
        # Never disclose UI dumps, account tokens or Android screen contents.
        print(json.dumps({"ok": False, "error": str(error), "music_verified": False},
                         ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

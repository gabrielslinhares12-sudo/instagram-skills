"""Safety tests for opt-in unofficial mobile music; no credentials or network."""
from __future__ import annotations

from datetime import datetime, timezone
import unittest
from unittest.mock import Mock, patch

from instagram_private_music import normalize, choose_approved_track, PrivateMusicError
from instagram_queue import run_queue, validate_manifest

NOW = datetime(2026, 10, 31, 22, 0, tzinfo=timezone.utc)
URL = "https://raw.githubusercontent.com/gabrielslinhares12-sudo/instagram-skills/main/01.jpg"


def post(**extra):
    p = {
        "id": "carousel-canonical", "due_at": "2026-10-31T22:00:00Z",
        "username": "temumaexplicacao",
        "target_url": "https://www.instagram.com/temumaexplicacao/",
        "caption": "Uma narrativa aprovada.", "kind": "carousel",
        "media_urls": [URL, URL.replace("01.jpg", "02.jpg")], "approved": True
    }
    p.update(extra)
    return p


class PrivateMusicSafetyTests(unittest.TestCase):
    def test_track_name_normalization_is_accent_independent(self):
        self.assertEqual(normalize("Prelúdio  N.º 4"), normalize("PRELUDIO n.º 4"))

    def test_track_selection_requires_one_matching_exact_instrumental(self):
        track = Mock(title="Bachianas Brasileiras 4 Prelúdio",
                     subtitle="Heitor Villa-Lobos")
        client = Mock(search_music=Mock(return_value=[track]))
        self.assertIs(choose_approved_track(client, {
            "music_track": "Bachianas Brasileiras 4 Prelúdio",
            "music_artist": "Heitor Villa-Lobos",
        }), track)
        with self.assertRaises(PrivateMusicError):
            choose_approved_track(client, {
                "music_track": "Música desconhecida", "music_artist": "Cantor desconhecido"
            })
        with self.assertRaises(PrivateMusicError):
            choose_approved_track(Mock(search_music=Mock(return_value=[track, track])), {
                "music_track": "Bachianas Brasileiras 4 Prelúdio",
                "music_artist": "Heitor Villa-Lobos",
            })

    def test_native_music_does_not_publish_without_explicit_private_opt_in(self):
        state = {"version":1,"items":{}}
        posts = validate_manifest({"version":1,"posts":[post()]})
        poster, persist = Mock(), Mock()
        result = run_queue(posts,state,NOW,execute=True,enabled=True,private_music=True,
                           poster_factory=lambda:poster,persist=persist)
        self.assertEqual(result["items"][0]["status"], "private_music_not_authorized")
        poster.publish.assert_not_called()
        persist.assert_not_called()

    def test_authorized_music_uses_existing_durable_claim(self):
        state = {"version":1,"items":{}}
        posts = validate_manifest({"version":1,"posts":[post(
            private_api_authorized=True,
            music_track="Bachianas Brasileiras 4 Prelúdio",
            music_artist="Heitor Villa-Lobos"
        )]})
        events = []
        publisher = Mock()
        publisher.publish.side_effect = lambda *args: (
            events.append("write") or {
                "ok":True,"mode":"published","username":"temumaexplicacao",
                "media_id":"123456789"
            }
        )
        def persist(document,message):
            events.append("claim" if len(events)==0 else "receipt")
        result=run_queue(posts,state,NOW,execute=True,enabled=True,private_music=True,
                         persist=persist,poster_factory=lambda:publisher)
        self.assertEqual(events,["claim","write","receipt"])
        self.assertEqual(result["status"],"published")

    def test_private_cron_disabled_by_default_and_cloud_only(self):
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent
        workflow = (root/".github/workflows/instagram-private-music.yml").read_text(encoding="utf-8")
        self.assertIn("runs-on: ubuntu-latest",workflow)
        self.assertIn("INSTAGRAM_PRIVATE_PUBLISH_ENABLED",workflow)
        self.assertIn("INSTAGRAM_PRIVATE_RISK_ACCEPTED",workflow)
        self.assertIn("secrets.INSTAGRAM_PRIVATE_SESSION_B64",workflow)
        self.assertNotIn("runs-on: [self-hosted",workflow)


if __name__ == "__main__":
    unittest.main()

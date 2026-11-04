"""Offline regression: the 03NOV 18:00 original salt-of-sea Reel is isolated."""
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"scripts"))
import instagram_publish_sal_mar_nov03_once as sal


class TimedReelTest(unittest.TestCase):
    def fixed_datetime(self, date):
        class MockDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                return date
        return MockDateTime

    def test_original_media_matches_weekly_plan(self):
        p=json.loads((BASE/"content/editorial/REELS-E-STORIES-2026-11-02-a-08.json").read_text(encoding="utf-8"))
        reel=next(p for p in p["reels"] if p["day"]=="2026-11-03")
        self.assertTrue(reel["approved"])
        self.assertFalse(reel["reel_published"])
        self.assertEqual(reel["slot"],"18:00")
        self.assertEqual(reel["source_video_id"],sal.CHANNEL_VIDEO_ID)
        self.assertEqual(reel["source_mp4"],sal.MEDIA)
        self.assertEqual(reel["caption_draft"],sal.CAPTION)
        self.assertEqual(reel["original_media_record"]["sha256"],sal.SHA256)
        self.assertEqual(reel["scheduled_for"],"2026-11-03T18:00:00-03:00")
        self.assertEqual(reel["expected_destination"],"temumaexplicacao")

    def test_cannot_publish_one_second_before_18h(self):
        instant=datetime(2026,11,3,20,59,59,tzinfo=timezone.utc)
        with patch.object(sal,"datetime",self.fixed_datetime(instant)), \
             patch.object(sal,"read_ledger",side_effect=AssertionError("ledger must not be touched")), \
             patch.object(sal,"public_media_ready",side_effect=AssertionError("no network before 18h")):
            self.assertEqual(sal.main(),0)

    def test_never_publishes_after_two_hour_cutoff(self):
        instant=datetime(2026,11,3,23,0,0,tzinfo=timezone.utc)
        with patch.object(sal,"datetime",self.fixed_datetime(instant)), \
             patch.object(sal,"read_ledger",side_effect=AssertionError("ledger must not be touched")):
            self.assertEqual(sal.main(),0)

    def test_existing_claim_prevents_duplicate(self):
        instant=datetime(2026,11,3,21,15,tzinfo=timezone.utc)
        with patch.object(sal,"datetime",self.fixed_datetime(instant)), \
             patch.object(sal,"read_ledger",return_value={"version":1,"items":{sal.POST_ID:{"status":"claimed"}}}), \
             patch.object(sal,"public_media_ready",side_effect=AssertionError("no media read after claim")):
            self.assertEqual(sal.main(),0)


if __name__=="__main__":
    unittest.main()

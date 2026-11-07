#!/usr/bin/env python3
import unittest
from datetime import datetime, timezone
from instagram_schedule_guard import inspect, gate

TODAY="2026-11-08"
def sample_posts():
    return [
        {"id":"tue-11","username":"temumaexplicacao","due_at":"2026-11-08T14:00:00Z","approved":True},
        {"id":"tue-15","username":"temumaexplicacao","due_at":"2026-11-08T18:00:00Z","approved":True},
        {"id":"tue-18","username":"temumaexplicacao","due_at":"2026-11-08T21:00:00Z","approved":True}
    ]
def clock(hour,minute=0):
    return datetime(2026,11,8,hour,minute,tzinfo=timezone.utc)
def ledger(items=None):
    return {"version":1,"items":items or {}}
class TestInstagramScheduleGuard(unittest.TestCase):
    def test_future_preflight_does_not_block_unrelated_missing_slots(self):
        posts=sample_posts()[:1]
        report=inspect(posts,ledger(),clock(13,30))
        self.assertEqual(report["slots"][0]["status"],"queued")
        self.assertEqual(gate(report,"preflight"),[])
    def test_missing_imminent_slot_detected(self):
        report=inspect([],ledger(),clock(13,31))
        self.assertEqual([(x["slot"],x["status"]) for x in gate(report,"preflight")],
                         [("11:00","missing")])
    def test_unapproved_slot_blocks_before_due(self):
        posts=sample_posts()
        posts[0]["approved"]=False
        report=inspect(posts,ledger(),clock(13,35))
        self.assertEqual(gate(report,"preflight")[0]["status"],"not_approved")
    def test_scheduled_but_not_published_12_minutes_late(self):
        report=inspect(sample_posts(),ledger(),clock(14,12))
        self.assertEqual(gate(report,"postflight")[0]["status"],"queued_unconfirmed")
    def test_publication_receipt_satisfies_postflight(self):
        data={"tue-11":{"status":"published","media_id":"12345"}}
        report=inspect(sample_posts(),ledger(data),clock(14,20))
        self.assertEqual(gate(report,"postflight"),[])
    def test_claim_in_progress_sends_alert(self):
        data={"tue-11":{"status":"claimed"}}
        report=inspect(sample_posts(),ledger(data),clock(14,13))
        self.assertEqual(gate(report,"postflight")[0]["status"],"claimed")
    def test_other_slot_in_same_day_is_not_flagged_early(self):
        report=inspect(sample_posts(),ledger(),clock(14,12))
        self.assertEqual(len(gate(report,"postflight")),1)
        self.assertEqual(gate(report,"postflight")[0]["slot"],"11:00")
    def test_timezone_local_brt(self):
        report=inspect(sample_posts(),ledger(),clock(14,0))
        self.assertEqual(report["slots"][0]["minutes_to_due"],0)
        self.assertEqual(report["slots"][1]["minutes_to_due"],240)
    def test_previous_day_not_reexamined(self):
        report=inspect(sample_posts(),ledger(),clock(18,20))
        self.assertEqual(gate(report,"postflight")[0]["slot"],"15:00")
if __name__=="__main__":
    unittest.main()

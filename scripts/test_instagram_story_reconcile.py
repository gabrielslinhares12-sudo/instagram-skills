#!/usr/bin/env python3
"""Regression: native Story linkages never fabricate posting or a text overlay."""
from __future__ import annotations
import copy
import unittest
from instagram_story_reconcile import CTA, ALIASES, approved_permalink, reconcile


class StoryReconcileTests(unittest.TestCase):
    def setUp(self):
        self.actual_id = "tue-2026-11-02-15-senha-impossivel"
        self.entry = {
            "parent_id": "tue-2026-11-02-18-senha-impossivel",
            "parent_published": False,
            "parent_media_id": None,
            "parent_permalink": None,
            "source_verified_by_official_receipt": False,
            "story_created": False,
            "story_published": False,
            "story_media_id": None,
            "text_cta_visible_verified": False,
            "no_external_link_sticker": True,
            "status": "awaiting_parent_publication",
        }
        self.doc = {"native_share_required": True, "text_cta": CTA,
                    "text_cta_required": True, "no_external_link_or_link_sticker": True,
                    "entries": [self.entry]}
        self.ledger = {"items": {self.actual_id: {
            "status": "published", "media_id": "18131786309499353",
            "published_at": "2026-11-02T16:51:58Z",
            "instagram_user_id": "17841433004716815"}}}
        self.url = "https://www.instagram.com/p/D123ABCxyz/"

    def test_linked_post_keeps_story_unpublished_until_native_receipt(self):
        out, notes = reconcile(self.ledger, self.doc, lambda media_id: self.url)
        e = out["entries"][0]
        self.assertEqual(e["actual_published_parent_id"], self.actual_id)
        self.assertTrue(e["parent_published"])
        self.assertEqual(e["parent_permalink"], self.url)
        self.assertFalse(e["story_created"])
        self.assertFalse(e["story_published"])
        self.assertIsNone(e["story_media_id"])
        self.assertEqual(e["status"], "awaiting_native_app_share_with_text_cta")
        self.assertFalse(self.entry["parent_published"])

    def test_without_verified_permalink_no_false_native_story_state(self):
        out, _ = reconcile(self.ledger, self.doc, lambda m: None)
        e = out["entries"][0]
        self.assertFalse(e["parent_published"])
        self.assertIsNone(e["parent_permalink"])
        self.assertEqual(e["status"], "pending_verified_permalink_before_native_share")

    def test_unknown_or_unpublished_source_ignored(self):
        for claims in ({}, {"status": "claimed", "media_id": "123", "published_at": "2026-11-02T00:00:00Z"},
                       {"status": "published", "media_id": "123"}):
            with self.subTest(claims=claims):
                out, notes = reconcile({"items": {self.actual_id: claims}}, self.doc, lambda m: self.url)
                self.assertEqual(out, self.doc)
                self.assertEqual(notes, [])

    def test_wrong_instagram_account_ignored(self):
        bad = copy.deepcopy(self.ledger)
        bad["items"][self.actual_id]["instagram_user_id"] = "000111222"
        out, _ = reconcile(bad, self.doc, lambda m: self.url)
        self.assertEqual(out, self.doc)

    def test_already_completed_story_is_never_modified_or_republished(self):
        doc = copy.deepcopy(self.doc)
        doc["entries"][0]["story_published"] = True
        doc["entries"][0]["story_media_id"] = "188877766655"
        out, _ = reconcile(self.ledger, doc, lambda m: self.url)
        self.assertTrue(out["entries"][0]["story_published"])
        self.assertEqual(out["entries"][0]["story_media_id"], "188877766655")

    def test_reject_bad_unsafe_permalink(self):
        for value in (None, "https://evil.example/p/post123/", "http://www.instagram.com/p/post123/",
                      "https://www.instagram.com/otheruser/", "https://www.instagram.com/p/",
                      "https://www.instagram.com/p/123456/?token=secret"):
            with self.subTest(url=value):
                self.assertFalse(approved_permalink(value))
        self.assertTrue(approved_permalink(self.url))


if __name__ == "__main__":
    unittest.main()

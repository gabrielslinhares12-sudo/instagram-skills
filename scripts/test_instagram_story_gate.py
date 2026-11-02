"""Unit tests (offline) for linked native Instagram Story lifecycle."""
import copy
import json
from pathlib import Path
import unittest

from instagram_story_gate import verify_linked_stories, StoryGateError

ROOT = Path(__file__).resolve().parent.parent / "content/editorial"


class LinkedNativeStoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feed = json.loads((ROOT / "semana-independente-2026-11-02-a-08/grade.json").read_text(encoding="utf-8"))
        cls.reels = json.loads((ROOT / "REELS-E-STORIES-2026-11-02-a-08.json").read_text(encoding="utf-8"))
        cls.stories = json.loads((ROOT / "STORIES-VINCULADOS-2026-11-02-a-08.json").read_text(encoding="utf-8"))

    def test_21_posts_have_21_uncreated_stories(self):
        summary = verify_linked_stories(self.feed, self.reels, self.stories)
        self.assertEqual(summary["linked_stories_planned"],21)
        self.assertEqual(summary["stories_published"],0)

    def test_never_create_a_story_before_post_receipt(self):
        broken=copy.deepcopy(self.stories)
        # First two posts and 02/11 Reel now have verified parent receipts;
        # use the next-day draft to prove Stories cannot precede publication.
        pending=next(i for i, entry in enumerate(broken["entries"])
                     if entry.get("parent_published") is not True)
        broken["entries"][pending]["story_created"]=True
        with self.assertRaisesRegex(StoryGateError, "depois do post"):
            verify_linked_stories(self.feed,self.reels,broken)

    def test_never_replace_native_reshare_with_new_media(self):
        broken=copy.deepcopy(self.stories)
        broken["entries"][0]["independent_story_asset"]="https://example.com/standalone.jpg"
        with self.assertRaisesRegex(StoryGateError, "independente"):
            verify_linked_stories(self.feed,self.reels,broken)

    def test_story_receipt_needs_native_share_and_text_cta(self):
        broken=copy.deepcopy(self.stories)
        entry=broken["entries"][0]
        entry.update(parent_published=True, source_verified_by_official_receipt=True,
                     parent_media_id="18114706189871027",
                     parent_permalink="https://www.instagram.com/p/EXAMPLE/",
                     story_created=True,story_published=True,
                     story_media_id="1234567")
        with self.assertRaisesRegex(StoryGateError, "falta republicação"):
            verify_linked_stories(self.feed,self.reels,broken)
        entry.update(text_cta_visible_verified=True,
                     native_original_post_tappable_verified=True)
        self.assertEqual(verify_linked_stories(self.feed,self.reels,broken)["stories_published"],1)

    def test_visible_text_is_required_no_voice(self):
        broken=copy.deepcopy(self.stories)
        entry=broken["entries"][0]
        entry.update(parent_published=True, source_verified_by_official_receipt=True,
                     parent_media_id="18114706189871027",
                     parent_permalink="https://www.instagram.com/p/EXAMPLE/",
                     story_created=True,story_published=True,
                     native_original_post_tappable_verified=True,
                     story_media_id="1234567",
                     text_cta_visible_verified=False)
        with self.assertRaisesRegex(StoryGateError, "texto"):
            verify_linked_stories(self.feed,self.reels,broken)
        entry["text_cta_visible_verified"]=True
        self.assertEqual(verify_linked_stories(self.feed,self.reels,broken)["stories_published"],1)

    def test_external_link_sticker_is_forbidden(self):
        broken=copy.deepcopy(self.stories)
        broken["entries"][1]["external_link_sticker"]="https://example.org/"
        with self.assertRaisesRegex(StoryGateError, "independente"):
            verify_linked_stories(self.feed,self.reels,broken)

    def test_voiceover_is_forbidden(self):
        broken=copy.deepcopy(self.stories)
        broken["entries"][1]["voiceover_created"]=True
        with self.assertRaisesRegex(StoryGateError, "narração"):
            verify_linked_stories(self.feed,self.reels,broken)

    def test_wrong_parent_and_duplicate_are_blocked(self):
        broken=copy.deepcopy(self.stories)
        broken["entries"][1]["parent_id"]=broken["entries"][0]["parent_id"]
        with self.assertRaisesRegex(StoryGateError, "repetido"):
            verify_linked_stories(self.feed,self.reels,broken)


if __name__=="__main__":
    unittest.main()

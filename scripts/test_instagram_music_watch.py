"""Offline tests for optional Android music worker. No phone required."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from instagram_music_watch import pending_tasks, reserve_once, run_once
from instagram_queue import fingerprint


def make(song=True):
    p={"id":"halloween","kind":"carousel","approved":True,
       "username":"temumaexplicacao",
       "target_url":"https://www.instagram.com/temumaexplicacao/",
       "caption":"Approved","due_at":"2026-11-01T18:00:00Z",
       "media_urls":["https://example.com/a.jpg","https://example.com/b.jpg"],
       "distribution_mode":"api_carousel_then_native_music",
       "owner_authorized_two_step_music":True}
    if song:
        p.update(music_track="Approved Track",music_artist="Approved Artist")
    s={"version":1,"items":{"halloween":{"status":"awaiting_native_music",
       "fingerprint":fingerprint(p),"media_id":"18107496023215107",
       "permalink":"https://www.instagram.com/p/DfNVlLDmC8P/"}}}
    return {"version":1,"posts":[p]},s


class WorkerTests(unittest.TestCase):
    def test_only_preapproved_track_and_pending_eligible(self):
        manifest,state=make()
        self.assertEqual(len(pending_tasks(manifest,state)),1)
        a,b=make(False)
        self.assertEqual(pending_tasks(a,b),[])
        state["items"]["halloween"]["status"]="published"
        self.assertEqual(pending_tasks(manifest,state),[])

    def test_attempt_reserved_at_most_once(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch("instagram_music_watch.CLAIM_DIR",Path(folder)):
                self.assertTrue(reserve_once("halloween","18107496023215107"))
                self.assertFalse(reserve_once("halloween","18107496023215107"))

    def test_dry_run_never_accesses_adb(self):
        manifest,state=make()
        with patch("instagram_music_watch.update_checkout"), \
             patch("instagram_music_watch.read_document",side_effect=[manifest,state]), \
             patch("instagram_music_watch.Android") as android:
            result=run_once(execute=False,refresh=True)
        self.assertEqual(result["mode"],"dry_run")
        self.assertEqual(result["approved_music_tasks"],1)
        android.assert_not_called()

    def test_environment_default_disables_mobile_writes(self):
        manifest,state=make()
        with patch("instagram_music_watch.read_document",side_effect=[manifest,state]), \
             patch("instagram_music_watch.Android") as android, \
             patch.dict("os.environ",{"INSTAGRAM_ANDROID_MUSIC_ENABLED":"false"}):
            result=run_once(execute=True,refresh=False)
        self.assertEqual(result["mode"],"dry_run")
        android.assert_not_called()


if __name__=="__main__":
    unittest.main()

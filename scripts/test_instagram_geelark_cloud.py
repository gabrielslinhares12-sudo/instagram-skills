"""Offline contract tests for GeeLark cloud carousel + native music.

No accounts, secrets, vendor calls or Instagram posts.
"""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
import os
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import instagram_geelark_cloud as g

def args(**kw):
    d={"post_id":"halloween-2026-10-31-historia-8-laminas",
       "schedule_at":(datetime.now(timezone.utc)+timedelta(hours=2))
                      .replace(microsecond=0).isoformat().replace("+00:00","Z"),
       "music_url":"https://www.instagram.com/reel/CaPtuRe123/"}
    d.update(kw)
    return SimpleNamespace(**d)

class GeeLarkGuardrailTests(unittest.TestCase):
    def test_audio_url_must_be_instagram_reel_or_post(self):
        self.assertEqual(g.source_url("https://instagram.com/reel/CaPtuRe123/"),
                         "https://www.instagram.com/reel/CaPtuRe123/")
        for url in ("https://instagram.com.evil.com/reel/CaPtuRe123/",
                    "https://www.instagram.com/reel/a/?music=1",
                    "http://www.instagram.com/reel/CaPtuRe123/",
                    "https://www.instagram.com/stories/CaPtuRe123/",
                    "https://www.instagram.com/reel/CaPtuRe123/?__a=1",
                    "https://www.instagram.com/reel/",
                    ""):
            with self.subTest(url=url), self.assertRaises(g.Blocked):
                g.source_url(url)

    def test_claims_are_unique_and_valid(self):
        self.assertEqual(g.validate_state_doc({"version":1,"items":{}}),
                         {"version":1,"items":{}})
        with self.assertRaises(g.Blocked):
            g.validate_state_doc({"version":1,"items":{"halloween-2026-10-31-historia-8-laminas":{"status":"published"}}})

    def test_original_halloween_is_approved_photo_carousel(self):
        post=g.load_post("halloween-2026-10-31-historia-8-laminas")
        self.assertEqual(post["username"],"temumaexplicacao")
        self.assertEqual(post["kind"],"carousel")
        self.assertEqual(len(post["media_urls"]),8)
        self.assertTrue(post["approved"])

    def test_unapproved_posts_never_reach_vendor(self):
        with self.assertRaises(g.Blocked):
            g.load_post("votos-validos-2026-11-01-v2-revisao")

    def test_readiness_does_not_contact_vendor_or_publish(self):
        with patch.dict(os.environ,{},clear=True),patch.object(g.GeeLark,"post") as request:
            output=io.StringIO()
            with redirect_stdout(output):
                g.check(args())
            result=json.loads(output.getvalue())
            self.assertTrue(result["ok"])
            self.assertEqual(result["images"],8)
            self.assertFalse(result["conditions"]["api_token_present"])
            self.assertFalse(result["ready_to_attempt"])
            self.assertFalse(result["publication_attempted"])
            request.assert_not_called()

    def test_publish_disabled_means_no_vendor_request_or_ledger(self):
        with patch.dict(os.environ,{},clear=True),patch.object(g.GeeLark,"post") as request,patch.object(g,"git_save") as save:
            with self.assertRaises(g.Blocked):
                g.submit(args())
            request.assert_not_called()
            save.assert_not_called()

    def test_vendor_task_request_keeps_carousel_and_music(self):
        client=g.GeeLark("unit-test-token")
        with patch.object(client,"post",return_value={"taskId":"123456789"}) as request:
            when=datetime.now(timezone.utc)+timedelta(hours=2)
            task=client.submit(phone_id="12345678",
                 images=["https://material.geelark.com/test"+str(i)+".jpg" for i in range(8)],
                 caption="Aprovado com música",when=when,
                 music="https://www.instagram.com/reel/CaPtuRe123/",
                 post_id="halloween-2026-10-31-historia-8-laminas")
            self.assertEqual(task,"123456789")
            endpoint,body=request.call_args.args
            self.assertEqual(endpoint,g.TASK_CREATE)
            self.assertEqual(body["id"],"12345678")
            self.assertEqual(len(body["image"]),8)
            self.assertEqual(body["description"],"Aprovado com música")
            self.assertTrue(body["publishPost"])
            self.assertTrue(body["needShareLink"])
            self.assertEqual(body["sameStyleUrl"],"https://www.instagram.com/reel/CaPtuRe123/")
            self.assertFalse(body["aiTag"])

    def test_vendor_task_status_never_implies_verified_music(self):
        client=g.GeeLark("unit-test-token")
        with patch.object(client,"post",return_value={
             "items":[{"id":"12345678","status":3,
                       "shareLink":"https://www.instagram.com/p/Example/"}]}):
            result=client.task_status("12345678")
            self.assertEqual(result["status"],3)
            self.assertTrue(result["share_link_present"])
            self.assertNotIn("native_music_verified",result)

    def test_past_due_and_excessively_late_schedules_rejected(self):
        for when in (datetime.now(timezone.utc)-timedelta(minutes=1),
                     datetime.now(timezone.utc)+timedelta(days=76)):
            with self.subTest(when=when),self.assertRaises(g.Blocked):
                g.check_inputs(args(schedule_at=when.replace(microsecond=0).isoformat().replace("+00:00","Z")))

if __name__ == "__main__":
    unittest.main()

"""Offline contract tests for the unofficial native-music carousel poster.

NEVER logs into or uploads to Instagram. All requests are mocked.
"""
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from instagram_private_music import InstagramPrivateMusicPoster, PrivateMusicError

ACCOUNT="temumaexplicacao"
def approved_post():
    return {"id":"halloween-2026-10-31-historia-8-laminas",
            "caption":"Legenda aprovada, fotos íntegras.",
            "kind":"carousel",
            "target_url":"https://www.instagram.com/temumaexplicacao/",
            "media_urls":[f"https://example.invalid/{i:02d}.jpg" for i in range(1,9)]}

class NativeMusicPosterTests(unittest.TestCase):
    def make_client(self, username=ACCOUNT, existing=None, confirmed_music=None):
        client=Mock()
        client.account_info.return_value=SimpleNamespace(username=username, pk=123456)
        client.user_medias.return_value=existing or []
        client.album_upload_with_music.return_value=SimpleNamespace(pk=12345678999)
        client.media_info_v1.return_value=SimpleNamespace(
            music_metadata={"music_track_id":"example"} if confirmed_music is None else confirmed_music)
        return client

    def make_poster(self, client, post=None):
        from instagrapi import Client
        files=[Path(f"/tmp/approved-{i:02d}.jpg") for i in range(1,9)]
        post=post or approved_post()
        with patch("instagram_private_music.fetch_verified_jpegs",return_value=files), \
             patch("instagram_private_music.decode_session",return_value={"settings":"opaque"}), \
             patch("instagram_private_music.choose_approved_track",return_value=SimpleNamespace(title="Approved Instrumental")), \
             patch.object(Client, "__new__",return_value=client):
            return InstagramPrivateMusicPoster(post)

    def test_authenticated_correct_account_publishes_once_with_music(self):
        client=self.make_client()
        poster=self.make_poster(client)
        post=approved_post()
        result=poster.publish("carousel",post["target_url"],{
            "draft_text":post["caption"],"media_urls":post["media_urls"]})
        self.assertEqual(result["media_id"],"12345678999")
        client.album_upload_with_music.assert_called_once()
        kwargs=client.album_upload_with_music.call_args.kwargs
        self.assertEqual(len(kwargs["paths"]),8)
        self.assertEqual(kwargs["caption"],post["caption"])
        self.assertEqual(kwargs["track"].title,"Approved Instrumental")
        client.media_info_v1.assert_called_once_with("12345678999")

    def test_wrong_instagram_account_rejected_before_upload(self):
        client=self.make_client(username="someone_else")
        with self.assertRaises(PrivateMusicError):
            self.make_poster(client)
        client.album_upload_with_music.assert_not_called()

    def test_duplicate_with_confirmed_music_does_not_upload_twice(self):
        post=approved_post()
        prior=SimpleNamespace(pk=8888888,caption_text=post["caption"],
                              resources=[object() for _ in range(8)])
        client=self.make_client(existing=[prior])
        poster=self.make_poster(client,post)
        result=poster.publish("carousel",post["target_url"],{
            "draft_text":post["caption"],"media_urls":post["media_urls"]})
        self.assertEqual(result["media_id"],"8888888")
        client.album_upload_with_music.assert_not_called()

    def test_missing_music_confirmation_blocks_success(self):
        client=self.make_client(confirmed_music={})
        poster=self.make_poster(client)
        post=approved_post()
        with self.assertRaises(PrivateMusicError):
            poster.publish("carousel",post["target_url"],{
                "draft_text":post["caption"],"media_urls":post["media_urls"]})
        client.album_upload_with_music.assert_called_once()

if __name__=="__main__":
    unittest.main()

#!/usr/bin/env python3
"""Offline unit tests for URL-based downloads (no network and no publishing)."""
import json
from pathlib import Path
import tempfile
from unittest import TestCase, main
from unittest.mock import Mock, patch

import instagram_download_approved_tue_short as d


class YoutubeReelDownloadTests(TestCase):
    def test_only_public_https_urls(self):
        self.assertTrue(d.safe_https("https://www.youtube.com/shorts/H9WGKaO5XQ4"))
        for url in ("http://example.com/file", "https://localhost/file",
                    "https://127.0.0.1/file", "https://a.local/file",
                    "https://user:secret@example.com/a", "file:///etc/passwd"):
            with self.subTest(url=url):
                self.assertFalse(d.safe_https(url))

    def test_selected_reel_from_official_plan_not_approved(self):
        chosen = d.selected_entry()
        self.assertEqual(chosen["id"], "H9WGKaO5XQ4")
        self.assertEqual(chosen["url"], "https://www.youtube.com/shorts/H9WGKaO5XQ4")
        self.assertEqual(chosen["views_approx"], 5700)

    def test_fake_mp4_rejected_before_ffprobe(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.mp4"
            path.write_bytes(b"<html>bad</html>" * 10000)
            with self.assertRaisesRegex(d.DownloadError, "MP4 container"):
                d.verify_mp4(path)

    def test_mp4_requires_sound_and_vertical_orientation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "video.mp4"
            path.write_bytes(b"\x00\x00\x00\x20ftypisom" + b"\x00" * 150000)
            result = Mock(stdout=json.dumps({
                "streams": [
                    {"codec_type": "video", "width": 1080, "height": 1920, "codec_name": "h264"},
                    {"codec_type": "audio", "codec_name": "aac"}],
                "format": {"duration": "45.0"}}))
            with patch.object(d.subprocess, "run", return_value=result):
                check = d.verify_mp4(path)
            self.assertEqual(check["height"], 1920)
            self.assertEqual(check["audio_codec"], "aac")

    def test_no_arbitrary_url_to_downloader(self):
        with self.assertRaises(d.DownloadError):
            d.download_via_site("https://example.com/video", Path("/tmp/not-created.mp4"))


if __name__ == "__main__":
    main()

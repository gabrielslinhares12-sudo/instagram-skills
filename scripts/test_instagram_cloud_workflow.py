"""Static cloud-runner safety checks; no Meta, GitHub or Instagram credentials."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CloudRunnerTests(unittest.TestCase):
    def test_only_central_scheduler_has_automatic_cron(self):
        cloud = (ROOT / ".github/workflows/instagram-scheduler.yml").read_text(encoding="utf-8")
        legacy = (ROOT / ".github/workflows/halloween-31out-2026.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '*/10 * * * *'", cloud)
        self.assertIn("runs-on: ubuntu-latest", cloud)
        self.assertNotIn("runs-on: [self-hosted", cloud.split("jobs:", 1)[1])
        self.assertIn("cancel-in-progress: false", cloud)
        self.assertIn("python3 scripts/instagram_queue.py --dry-run", cloud)
        self.assertIn("python3 scripts/instagram_preflight.py", cloud)
        self.assertIn("python3 scripts/instagram_queue.py --execute", cloud)
        self.assertIn("contents: write", cloud)
        self.assertNotIn("schedule:", legacy)
        self.assertNotIn("python3 scripts/instagram_queue.py --execute", legacy)
        self.assertNotIn("secrets.FACEBOOK_USER_ACCESS_TOKEN", legacy)

    def test_report_only_counts_safe_statuses(self):
        from instagram_cloud_report import summary
        counts, body = summary({"ok": True, "items": [
            {"status": "requires_native_music"},
            {"status": "missed_window"},
            {"status": "published"},
        ]})
        self.assertEqual(counts["requires_native_music"], 1)
        self.assertIn("sem PC", body)
        self.assertNotIn("secret", body)
        with self.assertRaises(ValueError):
            summary({"ok": True, "items": [{"status": "arbitrary"}]})

    def test_music_carousels_require_explicit_opt_out_before_meta(self):
        source = (ROOT / "scripts/instagram_queue.py").read_text(encoding="utf-8")
        self.assertIn('status = "requires_native_music"', source)
        self.assertIn('owner_authorized_without_music") is not True', source)
        self.assertIn('status"] == "due"', (ROOT / ".github/workflows/instagram-scheduler.yml").read_text(encoding="utf-8"))
        self.assertIn("needs_review", source)
        self.assertIn('MAX_LATENESS = timedelta(hours=2)', source)


if __name__ == "__main__":
    unittest.main()

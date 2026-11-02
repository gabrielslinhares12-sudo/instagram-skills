"""Offline queue tests, including durable claims against a local bare Git remote."""
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import io
import json
import os
from pathlib import Path
from secrets import token_urlsafe
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from instagram_queue import (GitLedger, QueueError, fingerprint, main, payload_for, plan,
                             run_queue, validate_manifest, validate_state)
from meta_poster import MetaError


NOW = datetime(2026, 10, 31, 22, 0, tzinfo=timezone.utc)
TARGET = "https://www.instagram.com/temumaexplicacao/"
URL = "https://raw.githubusercontent.com/gabrielslinhares12-sudo/instagram-skills/main/content/image.jpg"


def item(**overrides):
    value = {"id": "2026-10-31-halloween", "due_at": "2026-10-31T22:00:00Z",
             "username": "temumaexplicacao", "kind": "post", "target_url": TARGET,
             "caption": "Uma legenda final.", "media_urls": [URL], "approved": True}
    value.update(overrides)
    return value


def manifest(*posts):
    return {"version": 1, "posts": list(posts)}


def empty_state():
    return {"version": 1, "items": {}}


def published():
    return {"ok": True, "mode": "published", "username": "temumaexplicacao", "media_id": "222",
            "creation_id": "111", "page_id": "123", "instagram_user_id": "456"}


@contextmanager
def working_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class QueueTests(unittest.TestCase):
    def test_default_dry_run_does_not_construct_publisher_or_persist(self):
        factory, persist = Mock(), Mock()
        result = run_queue(validate_manifest(manifest(item())), empty_state(), NOW,
                           execute=False, enabled=True, poster_factory=factory, persist=persist)
        self.assertEqual(result["mode"], "dry_run")
        self.assertEqual(result["items"][0]["status"], "due")
        factory.assert_not_called()
        persist.assert_not_called()

    def test_disabled_execute_makes_no_api_calls_and_does_not_claim(self):
        state, factory, persist = empty_state(), Mock(), Mock()
        result = run_queue(validate_manifest(manifest(item())), state, NOW,
                           execute=True, enabled=False, poster_factory=factory, persist=persist)
        self.assertEqual(result["mode"], "disabled")
        self.assertEqual(state, empty_state())
        factory.assert_not_called()
        persist.assert_not_called()

    def test_clock_window_future_boundary_and_missed_items(self):
        posts = validate_manifest(manifest(item()))
        self.assertEqual(plan(posts, empty_state(), NOW - timedelta(seconds=1))[0]["status"], "future")
        self.assertEqual(plan(posts, empty_state(), NOW)[0]["status"], "due")
        self.assertEqual(plan(posts, empty_state(), NOW + timedelta(hours=2))[0]["status"], "due")
        self.assertEqual(plan(posts, empty_state(), NOW + timedelta(hours=2, seconds=1))[0]["status"],
                         "missed_window")

    def test_unapproved_and_future_items_are_not_published(self):
        for post in (item(approved=False), item(due_at="2026-11-01T22:00:00Z")):
            with self.subTest(post=post["approved"]):
                factory, persist = Mock(), Mock()
                run_queue(validate_manifest(manifest(post)), empty_state(), NOW,
                          execute=True, enabled=True, poster_factory=factory, persist=persist)
                factory.assert_not_called()
                persist.assert_not_called()

    def test_success_requires_claim_persistence_before_publication(self):
        state, events = empty_state(), []
        poster = Mock()
        def persist(document, message):
            events.append(("persist", deepcopy(document)))
        def publish(kind, target, payload):
            self.assertEqual(events[0][1]["items"][item()["id"]]["status"], "claimed")
            self.assertEqual(target, TARGET)
            self.assertTrue(payload["approved"])
            self.assertNotIn("due_at", payload)
            events.append(("publish", payload))
            return published()
        poster.publish.side_effect = publish
        result = run_queue(validate_manifest(manifest(item())), state, NOW, execute=True, enabled=True,
                           persist=persist, poster_factory=lambda: poster)
        self.assertEqual([event[0] for event in events], ["persist", "publish", "persist"])
        self.assertEqual(result["status"], "published")
        self.assertEqual(state["items"][item()["id"]]["media_id"], "222")

    def test_failed_claim_persistence_prevents_any_meta_publication(self):
        poster = Mock()
        persist = Mock(side_effect=QueueError("Unable to save the claim."))
        with self.assertRaises(QueueError):
            run_queue(validate_manifest(manifest(item())), empty_state(), NOW, execute=True,
                      enabled=True, persist=persist, poster_factory=lambda: poster)
        poster.publish.assert_not_called()

    def test_uncertain_error_is_quarantined_without_sensitive_text_or_retry(self):
        secret = token_urlsafe(24)
        error = MetaError(secret, http_status=401, code=190, subcode=463)
        error.creation_id = "111"
        error.write_attempted = True
        poster, state, persist = Mock(), empty_state(), Mock()
        poster.publish.side_effect = error
        posts = validate_manifest(manifest(item()))
        result = run_queue(posts, state, NOW, execute=True, enabled=True,
                           persist=persist, poster_factory=lambda: poster)
        self.assertFalse(result["ok"])
        self.assertEqual(state["items"][item()["id"]]["status"], "needs_review")
        self.assertEqual(state["items"][item()["id"]]["creation_id"], "111")
        self.assertEqual(state["items"][item()["id"]]["code"], 190)
        self.assertNotIn(secret, json.dumps(state) + json.dumps(result))
        run_queue(posts, state, NOW + timedelta(minutes=15), execute=True, enabled=True,
                  persist=persist, poster_factory=lambda: poster)
        self.assertEqual(poster.publish.call_count, 1)
        self.assertEqual(persist.call_count, 2)

    def test_unexpected_publisher_exception_also_never_leaks_or_retries(self):
        secret = token_urlsafe(24)
        poster, state = Mock(), empty_state()
        poster.publish.side_effect = RuntimeError(secret)
        result = run_queue(validate_manifest(manifest(item())), state, NOW, execute=True, enabled=True,
                           persist=Mock(), poster_factory=lambda: poster)
        self.assertFalse(result["ok"])
        self.assertEqual(state["items"][item()["id"]]["status"], "needs_review")
        self.assertNotIn(secret, json.dumps(result) + json.dumps(state))

    def test_invalid_or_wrong_account_publication_result_requires_manual_review(self):
        for result in ({"ok": False}, dict(published(), username="different"),
                       dict(published(), media_id="not-an-id")):
            with self.subTest(result=result):
                state, poster = empty_state(), Mock()
                poster.publish.return_value = result
                checked = run_queue(validate_manifest(manifest(item())), state, NOW, execute=True,
                                    enabled=True, persist=Mock(), poster_factory=lambda: poster)
                self.assertFalse(checked["ok"])
                self.assertEqual(state["items"][item()["id"]]["status"], "needs_review")

    def test_changed_content_or_existing_claim_blocks_republication(self):
        original = item()
        for status in ("claimed", "published", "needs_review", "awaiting_native_music"):
            state = {"version": 1, "items": {original["id"]:
                     {"status": status, "fingerprint": fingerprint(original)}}}
            factory = Mock()
            same = plan(validate_manifest(manifest(original)), state, NOW)[0]
            self.assertEqual(same["status"], status)
            changed = validate_manifest(manifest(item(caption="A different final caption.")))
            self.assertEqual(plan(changed, state, NOW)[0]["status"], "changed_after_claim")
            run_queue(changed, state, NOW, execute=True, enabled=True,
                      persist=Mock(), poster_factory=factory)
            factory.assert_not_called()

    def test_manifest_rejects_wrong_account_unsafe_urls_and_implicit_approval(self):
        invalid = [item(username="different"), item(target_url="https://www.instagram.com/different/"),
                   item(target_url="https://www.instagram.com/temumaexplicacao/?bad=true"),
                   item(media_urls=["http://example.test/media.jpg"]),
                   item(media_urls=["https://secret@example.test/media.jpg"]),
                   item(media_urls=["https://example.test/media.jpg?access_token=hidden"]),
                   item(approved="true"), item(caption="x" * 2201),
                   item(due_at="2026-10-31T22:00:00"), item(due_at="2026-10-31T19:00:00-03:00"),
                   item(kind="story"), item(media_urls=[]), item(extra_option="untrusted")]
        for post in invalid:
            with self.subTest(post=post):
                with self.assertRaises((QueueError, MetaError)):
                    validate_manifest(manifest(post))

    def test_duplicate_ids_and_duplicate_approved_time_slots_are_rejected(self):
        for document in (manifest(item(), item()),
                         manifest(item(), item(id="same-slot"))):
            with self.assertRaises(QueueError):
                validate_manifest(document)

    def test_two_approved_posts_same_day_with_different_times_are_valid(self):
        posts = validate_manifest(manifest(item(), item(id="evening-carousel", due_at="2026-10-31T21:00:00Z")))
        self.assertEqual(len(posts), 2)
        self.assertNotEqual(posts[0]["due_at"], posts[1]["due_at"])

    def test_carousel_reel_optional_ai_label_and_cover_are_mapped_without_schedule(self):
        for post in (item(kind="carousel", media_urls=[URL, URL + "-two"]),
                     item(kind="reel", is_ai_generated=True, cover_url=URL)):
            checked = validate_manifest(manifest(post))[0]
            payload = payload_for(checked)
            self.assertEqual(payload["draft_text"], post["caption"])
            self.assertEqual(payload["media_urls"], post["media_urls"])
            self.assertNotIn("scheduled_time", payload)
            self.assertNotIn("due_at", payload)
        for invalid in (item(kind="carousel"), item(kind="reel", media_urls=[URL, URL]),
                        item(cover_url=URL), item(is_ai_generated="true")):
            with self.assertRaises(QueueError):
                validate_manifest(manifest(invalid))

    def test_ai_provenance_prevents_false_labels_and_under_disclosure(self):
        self.assertNotIn("is_ai_generated", payload_for(validate_manifest(manifest(
            item(kind="reel", ai_origin="verified_non_synthetic")))[0]))
        self.assertEqual(payload_for(validate_manifest(manifest(
            item(kind="reel", ai_origin="synthetic", is_ai_generated=True)))[0])["is_ai_generated"],True)
        for bad in (item(kind="reel", ai_origin="unverified"),
                    item(kind="reel", ai_origin="synthetic"),
                    item(kind="reel", ai_origin="verified_non_synthetic", is_ai_generated=True),
                    item(kind="reel", is_ai_generated=False)):
            with self.subTest(bad=bad):
                with self.assertRaises(QueueError):
                    validate_manifest(manifest(bad))

    def test_new_clearly_illustrated_stills_preserve_truthful_origin(self):
        cutoff = "2026-11-02T18:00:00Z"
        for kind in ("post", "carousel"):
            urls = [URL, URL + "-two"] if kind == "carousel" else [URL]
            post = item(kind=kind, due_at=cutoff, media_urls=urls,
                        ai_origin="synthetic", content_style="clearly_illustrated",
                        ai_disclosure_review="no_mandatory_self_disclosure_for_stylized_still")
            posts=validate_manifest(manifest(post))
            self.assertNotIn("is_ai_generated", payload_for(posts[0]))
        with self.assertRaises(QueueError):
            validate_manifest(manifest(item(kind="post", due_at=cutoff,
                ai_origin="synthetic", content_style="clearly_illustrated")))
        with self.assertRaises(QueueError):
            validate_manifest(manifest(item(kind="reel", due_at=cutoff,
                ai_origin="synthetic", content_style="clearly_illustrated",
                ai_disclosure_review="no_mandatory_self_disclosure_for_stylized_still")))

    def test_new_posts_never_add_optional_ai_label(self):
        cutoff = "2026-11-03T21:00:00Z"
        good = item(kind="reel", due_at=cutoff,
                    ai_origin="verified_non_synthetic")
        self.assertNotIn("is_ai_generated",
                         payload_for(validate_manifest(manifest(good))[0]))
        blocked = (
            item(kind="reel", due_at=cutoff),
            item(kind="reel", due_at=cutoff, ai_origin="unverified"),
            item(kind="reel", due_at=cutoff, ai_origin="synthetic",
                 is_ai_generated=True),
            item(kind="reel", due_at=cutoff, ai_origin="verified_non_synthetic",
                 is_ai_generated=False),
            item(kind="reel", due_at=cutoff, ai_origin="verified_non_synthetic",
                 caption="Este conteúdo foi feito por IA. Confira."),
        )
        for post in blocked:
            with self.subTest(post=post):
                with self.assertRaises(QueueError):
                    validate_manifest(manifest(post))

    def test_cloud_carousel_with_native_music_never_posts_silently(self):
        # Applies to legacy approved carousels as well as new ones.
        carousel = item(kind="carousel", media_urls=[URL, URL + "-two"])
        posts = validate_manifest(manifest(carousel))
        self.assertEqual(plan(posts, empty_state(), NOW)[0]["status"], "requires_native_music")
        poster, persist = Mock(), Mock()
        run_queue(posts, empty_state(), NOW, execute=True, enabled=True,
                  persist=persist, poster_factory=lambda: poster)
        poster.publish.assert_not_called()
        persist.assert_not_called()

    def test_cloud_carousel_without_music_requires_specific_opt_out(self):
        carousel = item(kind="carousel", media_urls=[URL, URL + "-two"],
                        distribution_mode="api_carousel_without_native_music")
        with self.assertRaisesRegex(QueueError, "specific owner authorization"):
            validate_manifest(manifest(carousel))
        carousel["owner_authorized_without_music"] = True
        checked = validate_manifest(manifest(carousel))
        self.assertEqual(plan(checked, empty_state(), NOW)[0]["status"], "due")
        for bad in ("reel_with_audio", "music_carousel", None):
            with self.assertRaises(QueueError):
                validate_manifest(manifest(item(kind="carousel", media_urls=[URL, URL+"-two"],
                                                distribution_mode=bad)))
        with self.assertRaisesRegex(QueueError, "only to photo carousels"):
            validate_manifest(manifest(item(distribution_mode="native_music_carousel")))

    def test_two_step_carousel_needs_owner_and_exact_track(self):
        base = item(kind="carousel", media_urls=[URL, URL + "-second"],
                    distribution_mode="api_carousel_then_native_music")
        invalid = [
            base,
            dict(base, owner_authorized_two_step_music="true",
                 music_track="Example Instrumental", music_artist="Artist Name"),
            dict(base, owner_authorized_two_step_music=True,
                 music_track="Example Instrumental"),
        ]
        for entry in invalid:
            with self.subTest(entry=entry):
                with self.assertRaises(QueueError):
                    validate_manifest(manifest(entry))
        ready = dict(base, owner_authorized_two_step_music=True,
                     music_track="Example Instrumental", music_artist="Artist Name")
        defer = dict(base, owner_authorized_two_step_music=True)
        self.assertEqual(plan(validate_manifest(manifest(defer)), empty_state(), NOW)[0]["status"], "due")
        posts = validate_manifest(manifest(ready))
        self.assertEqual(plan(posts, empty_state(), NOW)[0]["status"], "due")
        # The switch from silent release to music-required is a material change.
        different = dict(ready, music_track="Different Instrumental")
        self.assertNotEqual(fingerprint(ready), fingerprint(different))
        self.assertNotEqual(fingerprint(ready), fingerprint(dict(ready,
            distribution_mode="native_music_carousel")))

    def test_two_step_meta_success_records_awaiting_music_not_completion(self):
        post = item(kind="carousel", media_urls=[URL, URL + "-second"],
                    distribution_mode="api_carousel_then_native_music",
                    owner_authorized_two_step_music=True,
                    music_track="Example Instrumental", music_artist="Artist Name")
        state = empty_state()
        events = []
        poster = Mock()
        poster.publish.return_value = published()
        def persist(document, message):
            events.append(deepcopy(document["items"][post["id"]]))
        result = run_queue(validate_manifest(manifest(post)), state, NOW,
                           execute=True, enabled=True,
                           persist=persist, poster_factory=lambda: poster)
        self.assertEqual([e["status"] for e in events], ["claimed", "awaiting_native_music"])
        self.assertEqual(result["status"], "awaiting_native_music")
        self.assertEqual(result["media_id"], "222")
        self.assertEqual(state["items"][post["id"]]["music_track"], "Example Instrumental")
        self.assertEqual(plan(validate_manifest(manifest(post)), state, NOW)[0]["status"],
                         "awaiting_native_music")
        self.assertEqual(validate_state(state), state)
        run_queue(validate_manifest(manifest(post)), state, NOW + timedelta(minutes=10),
                  execute=True, enabled=True, persist=persist, poster_factory=lambda: poster)
        poster.publish.assert_called_once()
        self.assertEqual(len(events), 2)

    def test_two_step_without_track_still_marks_audio_pending(self):
        post = item(kind="carousel", media_urls=[URL, URL + "-second"],
                    distribution_mode="api_carousel_then_native_music",
                    owner_authorized_two_step_music=True)
        state = empty_state()
        poster = Mock()
        poster.publish.return_value = published()
        result = run_queue(validate_manifest(manifest(post)), state, NOW,
                           execute=True, enabled=True,
                           persist=Mock(), poster_factory=lambda: poster)
        self.assertEqual(result["status"], "awaiting_native_music")
        self.assertNotIn("music_track", state["items"][post["id"]])
        self.assertEqual(plan(validate_manifest(manifest(post)), state, NOW)[0]["status"],
                         "awaiting_native_music")

    def test_two_step_without_approval_does_not_post(self):
        post = item(kind="carousel", media_urls=[URL, URL + "-second"],
                    distribution_mode="api_carousel_then_native_music",
                    owner_authorized_two_step_music=True,
                    music_track="Example Instrumental", music_artist="Artist Name",
                    approved=False)
        poster = Mock()
        run_queue(validate_manifest(manifest(post)), empty_state(), NOW,
                  execute=True, enabled=True, persist=Mock(), poster_factory=lambda: poster)
        poster.publish.assert_not_called()

    def test_byte_hashes_bind_claim_and_require_one_hash_per_media(self):
        post = item(media_sha256=["a" * 64])
        validate_manifest(manifest(post))
        self.assertNotEqual(fingerprint(post), fingerprint(item(media_sha256=["b" * 64])))
        for hashes in ([], ["not-a-hash"], ["a" * 64, "b" * 64]):
            with self.assertRaises(QueueError):
                validate_manifest(manifest(item(media_sha256=hashes)))

    def test_malformed_ledger_fails_closed(self):
        for invalid in ({}, {"version": 1, "items": []},
                        {"version": 1, "items": {"id": {"status": "retry", "fingerprint": "a" * 64}}}):
            with self.assertRaises(QueueError):
                validate_state(invalid)

    def test_cli_defaults_to_dry_run_even_when_enabled_and_has_no_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest(item())), encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with patch.dict(os.environ, {"INSTAGRAM_SCHEDULER_ENABLED": "true"}, clear=True), \
                    patch("instagram_queue.FacebookConfig.from_env") as configured, \
                    redirect_stdout(out), redirect_stderr(err):
                result = main(["--manifest", str(path), "--state", str(path.parent / "absent.json"),
                               "--now", "2026-10-31T22:00:00Z"])
            self.assertEqual(result, 0)
            self.assertEqual(err.getvalue(), "")
            self.assertEqual(json.loads(out.getvalue())["mode"], "dry_run")
            configured.assert_not_called()

    def test_cli_refuses_clock_override_for_actual_execution(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(main(["--execute", "--now", "2026-10-31T22:00:00Z"]), 1)
        self.assertEqual(out.getvalue(), "")
        self.assertIn("clock override", err.getvalue())


class DurableGitLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.remote, self.checkout = self.base / "remote.git", self.base / "checkout"
        self.checkout.mkdir()
        self.git("init", "--bare", str(self.remote), cwd=self.base)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Queue Test Automation")
        self.git("config", "user.email", "queue@example.test")
        self.path = self.checkout / "content" / "publication-state.json"
        self.path.parent.mkdir()
        self.path.write_text(json.dumps(empty_state()) + "\n", encoding="utf-8")
        self.git("add", "content/publication-state.json")
        self.git("commit", "-m", "Initialize local ledger test")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")

    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd or self.checkout, check=True,
                              capture_output=True, text=True, timeout=20).stdout

    def remote_state(self):
        return json.loads(self.git("--git-dir=" + str(self.remote), "show",
                                   "main:content/publication-state.json", cwd=self.base))

    def test_remote_claim_is_visible_before_publisher_is_called(self):
        poster = Mock()
        def publish(*args):
            remote = self.remote_state()
            self.assertEqual(remote["items"][item()["id"]]["status"], "claimed")
            return published()
        poster.publish.side_effect = publish
        with working_directory(self.checkout):
            ledger = GitLedger(Path("content/publication-state.json"))
            result = run_queue(validate_manifest(manifest(item())), empty_state(), NOW,
                               execute=True, enabled=True, persist=ledger, poster_factory=lambda: poster)
        self.assertTrue(result["ok"])
        self.assertEqual(self.remote_state()["items"][item()["id"]]["status"], "published")

    def test_push_failure_blocks_meta_and_leaves_remote_ledger_unchanged(self):
        self.git("remote", "set-url", "origin", str(self.base / "missing-remote.git"))
        poster = Mock()
        with working_directory(self.checkout):
            ledger = GitLedger(Path("content/publication-state.json"))
            with self.assertRaises(QueueError):
                run_queue(validate_manifest(manifest(item())), empty_state(), NOW,
                          execute=True, enabled=True, persist=ledger, poster_factory=lambda: poster)
        poster.publish.assert_not_called()
        self.assertEqual(self.remote_state(), empty_state())

    def test_unrelated_staged_file_prevents_claim_push(self):
        unrelated = self.checkout / "unrelated.txt"
        unrelated.write_text("Do not include this file.\n", encoding="utf-8")
        self.git("add", "unrelated.txt")
        with working_directory(self.checkout):
            ledger = GitLedger(Path("content/publication-state.json"))
            with self.assertRaises(QueueError):
                ledger({"version": 1, "items": {}}, "Invalid staged files")
        self.assertEqual(self.remote_state(), empty_state())


if __name__ == "__main__":
    unittest.main()

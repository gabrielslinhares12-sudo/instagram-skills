"""Offline tests for Facebook Login account discovery and approved publishing."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from secrets import token_urlsafe
import unittest
from unittest.mock import Mock, patch

from facebook_poster import FacebookConfig, FacebookPoster, main
from meta_poster import MetaError


# Ephemeral synthetic credentials test separation and redaction.
USER_TOKEN = token_urlsafe(24)
PAGE_TOKEN = token_urlsafe(24)
IG_TOKEN = token_urlsafe(24)
TARGET = "https://www.instagram.com/temumaexplicacao/"
CONFIG = FacebookConfig(USER_TOKEN, "v25.0", "temumaexplicacao")
ENV = {"FACEBOOK_USER_ACCESS_TOKEN": USER_TOKEN, "INSTAGRAM_API_VERSION": "v25.0",
       "INSTAGRAM_ACCESS_TOKEN": IG_TOKEN}


def response(body, status=200):
    result = Mock(status_code=status)
    result.json.return_value = body
    return result


def page(page_id="123", instagram_id="456", username="temumaexplicacao", token=PAGE_TOKEN):
    return {"id": page_id, "name": "Untrusted Page Name", "access_token": token,
            "instagram_business_account": {"id": instagram_id, "username": username}}


def pages(*items, paging=None):
    body = {"data": list(items)}
    if paging is not None:
        body["paging"] = paging
    return response(body)


def relationship(page_id="123", instagram_id="456", username="temumaexplicacao"):
    return response({"id": page_id,
                     "instagram_business_account": {"id": instagram_id, "username": username}})


def payload(**overrides):
    result = {"kind": "post", "target_url": TARGET, "approved": True,
              "draft_text": "Legenda aprovada.", "media_urls": ["https://media.example.test/image.jpg"]}
    result.update(overrides)
    return result


class FacebookPosterTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.poster = FacebookPoster(CONFIG, self.session)

    def test_check_discovers_then_rechecks_page_using_separate_credentials(self):
        self.session.request.side_effect = [pages(page()), relationship()]
        checked = self.poster.check_identity()
        self.assertEqual(checked, {"ok": True, "mode": "check", "login": "facebook", "page_id": "123",
                                   "instagram_user_id": "456", "username": "temumaexplicacao"})
        calls = self.session.request.call_args_list
        self.assertEqual([call.args[0] for call in calls], ["GET", "GET"])
        self.assertEqual(calls[0].args[1], "https://graph.facebook.com/v25.0/me/accounts")
        self.assertEqual(calls[0].kwargs["headers"], {"Authorization": f"Bearer {USER_TOKEN}"})
        self.assertEqual(calls[1].args[1], "https://graph.facebook.com/v25.0/123")
        self.assertEqual(calls[1].kwargs["headers"], {"Authorization": f"Bearer {PAGE_TOKEN}"})
        for call in calls:
            self.assertIs(call.kwargs["allow_redirects"], False)
            self.assertNotIn("access_token", call.kwargs["params"])
        public = json.dumps(checked)
        for secret in (USER_TOKEN, PAGE_TOKEN, IG_TOKEN, "Untrusted Page Name"):
            self.assertNotIn(secret, public)

    def test_paging_uses_cursor_and_never_follows_untrusted_next(self):
        next_url = f"https://attacker.example.test/capture?access_token={USER_TOKEN}"
        self.session.request.side_effect = [
            pages(page(username="different"), paging={"next": next_url, "cursors": {"after": "cursor-two"}}),
            pages(page()), relationship(),
        ]
        self.poster.check_identity()
        calls = self.session.request.call_args_list
        self.assertEqual(calls[1].args[1], "https://graph.facebook.com/v25.0/me/accounts")
        self.assertEqual(calls[1].kwargs["params"]["after"], "cursor-two")
        self.assertTrue(all(call.args[1].startswith("https://graph.facebook.com/") for call in calls))

    def test_missing_page_token_wrong_account_and_missing_link_prevent_writes(self):
        cases = [pages(), pages(page(token=None)), pages(page(username="different")),
                 pages({"id": "123", "access_token": PAGE_TOKEN})]
        for batch in cases:
            with self.subTest(batch=batch):
                self.session.reset_mock()
                self.session.request.side_effect = None
                self.session.request.return_value = batch
                with self.assertRaises(MetaError):
                    self.poster.publish("post", TARGET, payload())
                self.assertEqual(self.session.request.call_count, 1)
                self.assertEqual(self.session.request.call_args.args[0], "GET")

    def test_changed_relationship_never_creates_media(self):
        for wrong in (relationship(instagram_id="999"), relationship(username="different"),
                      relationship(page_id="999"), response({"id": "123"})):
            with self.subTest(relationship=wrong):
                self.session.reset_mock()
                self.session.request.side_effect = [pages(page()), wrong]
                with self.assertRaises(MetaError):
                    self.poster.publish("post", TARGET, payload())
                self.assertEqual([call.args[0] for call in self.session.request.call_args_list], ["GET", "GET"])

    def test_ambiguous_pages_fail_unless_expected_filters_select_one(self):
        self.session.request.return_value = pages(page(), page(page_id="789", instagram_id="987"))
        with self.assertRaises(MetaError):
            self.poster.check_identity()
        selected = FacebookPoster(FacebookConfig(USER_TOKEN, "v25.0", "temumaexplicacao", "789", "987"), self.session)
        self.session.request.side_effect = [pages(page(), page(page_id="789", instagram_id="987")),
                                            relationship(page_id="789", instagram_id="987")]
        self.assertEqual(selected.check_identity()["page_id"], "789")

    def test_mismatched_expected_id_filter_prevents_writes(self):
        configured = FacebookConfig(USER_TOKEN, "v25.0", "temumaexplicacao", instagram_user_id="999")
        poster = FacebookPoster(configured, self.session)
        self.session.request.return_value = pages(page())
        with self.assertRaises(MetaError):
            poster.publish("post", TARGET, payload())
        self.session.request.assert_called_once()

    def test_success_order_and_page_token_for_all_publication_calls(self):
        self.session.request.side_effect = [pages(page()), relationship(), response({"id": "111"}),
                                            response({"status_code": "FINISHED"}), response({"id": "222"})]
        result = self.poster.publish("post", TARGET, payload())
        self.assertEqual(result["media_id"], "222")
        self.assertEqual(result["page_id"], "123")
        calls = self.session.request.call_args_list
        self.assertEqual([call.args[0] for call in calls], ["GET", "GET", "POST", "GET", "POST"])
        self.assertEqual([call.args[1] for call in calls], [
            "https://graph.facebook.com/v25.0/me/accounts", "https://graph.facebook.com/v25.0/123",
            "https://graph.facebook.com/v25.0/456/media", "https://graph.facebook.com/v25.0/111",
            "https://graph.facebook.com/v25.0/456/media_publish",
        ])
        for call in calls[1:]:
            self.assertEqual(call.kwargs["headers"], {"Authorization": f"Bearer {PAGE_TOKEN}"})
        self.assertNotIn(IG_TOKEN, repr(calls))

    def test_unsupported_payload_rejected_before_discovery(self):
        for document in (payload(approved=False), payload(media=["/tmp/file.jpg"]),
                         payload(scheduled_time="2099-01-01T00:00:00Z"),
                         payload(kind="reel"), payload(media_urls=[])):
            with self.subTest(document=document):
                with self.assertRaises(MetaError):
                    self.poster.publish(document["kind"], TARGET, document)
                self.session.request.assert_not_called()

    def test_processing_failure_does_not_publish_and_keeps_container_id(self):
        self.session.request.side_effect = [pages(page()), relationship(), response({"id": "111"}),
                                            response({"status_code": "ERROR"})]
        with self.assertRaises(MetaError) as caught:
            self.poster.publish("post", TARGET, payload())
        public = caught.exception.public()
        self.assertEqual(public["creation_id"], "111")
        self.assertIn("Do not retry automatically", public["retry_notice"])
        self.assertEqual(self.session.request.call_count, 4)

    def test_errors_redact_both_tokens_and_raw_next_url(self):
        raw_next = f"https://other.example.test/?access_token={USER_TOKEN}"
        self.session.request.side_effect = [
            pages(page(), paging={"next": raw_next, "cursors": {"after": "cursor"}}),
            response({"error": {"message": f"{PAGE_TOKEN} {raw_next}", "code": 190, "error_subcode": 463}}, 400),
        ]
        with self.assertRaises(MetaError) as caught:
            self.poster.check_identity()
        public = json.dumps(caught.exception.public())
        for secret in (USER_TOKEN, PAGE_TOKEN, IG_TOKEN, raw_next):
            self.assertNotIn(secret, public)
        self.assertEqual(caught.exception.code, 190)
        self.assertEqual(caught.exception.subcode, 463)

    def test_pagination_repeated_cursor_and_limit_fail_without_writing(self):
        batch = pages(page(), paging={"next": "https://ignored.test", "cursors": {"after": "same"}})
        self.session.request.return_value = batch
        with self.assertRaises(MetaError):
            self.poster.check_identity()
        self.assertEqual(self.session.request.call_count, 2)
        self.session.reset_mock()
        self.session.request.side_effect = [batch]
        with patch("facebook_poster.MAX_PAGE_BATCHES", 1):
            with self.assertRaises(MetaError):
                self.poster.check_identity()
        self.session.request.assert_called_once()

    def test_check_cli_reads_only_without_consuming_stdin(self):
        self.session.request.side_effect = [pages(page()), relationship()]
        output, errors, stdin = io.StringIO(), io.StringIO(), Mock()
        with patch.dict("os.environ", ENV, clear=True), patch("meta_poster.UrllibTransport", return_value=self.session):
            with patch("sys.stdin", stdin), redirect_stdout(output), redirect_stderr(errors):
                result = main(["--check"])
        self.assertEqual(result, 0)
        self.assertEqual(errors.getvalue(), "")
        self.assertEqual(json.loads(output.getvalue())["instagram_user_id"], "456")
        self.assertEqual([call.args[0] for call in self.session.request.call_args_list], ["GET", "GET"])
        stdin.read.assert_not_called()
        for secret in (USER_TOKEN, PAGE_TOKEN, IG_TOKEN):
            self.assertNotIn(secret, output.getvalue())

    def test_config_never_falls_back_to_instagram_login_token(self):
        with self.assertRaises(MetaError):
            FacebookConfig.from_env({"INSTAGRAM_ACCESS_TOKEN": IG_TOKEN, "INSTAGRAM_API_VERSION": "v25.0"})
        configured = FacebookConfig.from_env(ENV)
        self.assertEqual(configured.user_access_token, USER_TOKEN)
        for variable, value in (("INSTAGRAM_API_VERSION", ""),
                                ("FACEBOOK_PAGE_ID", "not-id"),
                                ("FACEBOOK_INSTAGRAM_USER_ID", "https://wrong.test")):
            invalid = dict(ENV)
            invalid[variable] = value
            with self.subTest(variable=variable), self.assertRaises(MetaError):
                FacebookConfig.from_env(invalid)


if __name__ == "__main__":
    unittest.main()

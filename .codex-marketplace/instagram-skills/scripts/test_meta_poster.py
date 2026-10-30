"""Offline contract and publication-boundary tests for the Meta custom poster."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from secrets import token_urlsafe
import unittest
from unittest.mock import Mock, patch
from urllib.error import URLError

from meta_poster import Config, MetaError, MetaPoster, NoRedirect, UrllibTransport, main


TARGET = "https://www.instagram.com/temumaexplicacao/"
# Ephemeral synthetic credentials test redaction without embedded tokens.
TOKEN = token_urlsafe(24)
IMAGE_URL = "https://media.example.test/private-image.jpg?signature=secret"
CONFIG = Config(TOKEN, "12345", "v25.0", "temumaexplicacao")
ENV = {"INSTAGRAM_ACCESS_TOKEN": TOKEN, "INSTAGRAM_USER_ID": "12345",
       "INSTAGRAM_API_VERSION": "v25.0"}


def response(body, status=200):
    result = Mock(status_code=status)
    result.json.return_value = body
    return result


def payload(**overrides):
    result = {"kind": "post", "target_url": TARGET, "draft_text": "Legenda aprovada.",
              "approved": True, "media_urls": [IMAGE_URL]}
    result.update(overrides)
    return result


def identity(username="temumaexplicacao", user_id="12345"):
    return response({"user_id": user_id, "username": username})


class MetaPosterTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.poster = MetaPoster(CONFIG, self.session)

    def test_identity_mismatch_prevents_write(self):
        for wrong_identity in (identity(username="different"), identity(user_id="999")):
            with self.subTest(identity=wrong_identity):
                self.session.reset_mock()
                self.session.request.return_value = wrong_identity
                with self.assertRaises(MetaError):
                    self.poster.publish("post", TARGET, payload())
                self.assertEqual(self.session.request.call_count, 1)
                self.assertEqual(self.session.request.call_args.args[0], "GET")

    def test_invalid_payloads_prevent_all_requests(self):
        cases = [
            ("reel", TARGET, payload(kind="reel")),
            ("carousel", TARGET, payload(kind="carousel")),
            ("story", TARGET, payload(kind="story")),
            ("post", TARGET, payload(scheduled_time="2099-01-01T00:00:00Z")),
            ("post", TARGET, payload(media=["/tmp/image.jpg"])),
            ("post", TARGET, payload(approved=False)),
            ("post", TARGET, payload(approved="true")),
            ("post", TARGET, payload(media_urls=[IMAGE_URL, IMAGE_URL])),
            ("post", TARGET, payload(media_urls=["http://example.test/image.jpg"])),
            ("post", TARGET, payload(media_urls=["https://user:password@example.test/image.jpg"])),
            ("post", TARGET, payload(media_urls=["https://example.test:bad/image.jpg"])),
            ("post", TARGET, payload(kind="reel")),
            ("post", TARGET, payload(target_url="https://www.instagram.com/different/")),
            ("post", "https://www.instagram.com/p/abc/", payload(target_url="https://www.instagram.com/p/abc/")),
            ("post", "https://www.instagram.com/different/", payload(target_url="https://www.instagram.com/different/")),
            ("post", TARGET, payload(draft_text="x" * 2201)),
            ("post", TARGET, payload(platform_settings={"instagram": {"videoType": "REELS"}})),
        ]
        for kind, target, document in cases:
            with self.subTest(kind=kind, document=document):
                with self.assertRaises(MetaError):
                    self.poster.publish(kind, target, document)
                self.session.request.assert_not_called()

    def test_processing_failure_preserves_creation_id_and_never_publishes(self):
        self.session.request.side_effect = [identity(), response({"id": "444"}),
                                            response({"status_code": "ERROR"})]
        with self.assertRaises(MetaError) as caught:
            self.poster.publish("post", TARGET, payload())
        public = caught.exception.public()
        self.assertEqual(public["creation_id"], "444")
        self.assertIn("Do not retry automatically", public["retry_notice"])
        self.assertEqual(self.session.request.call_count, 3)
        self.assertFalse(any(call.args[1].endswith("/media_publish")
                             for call in self.session.request.call_args_list))

    def test_processing_timeout_never_publishes(self):
        self.session.request.side_effect = [identity(), response({"id": "444"})]
        with patch("meta_poster.time.monotonic", side_effect=[0, 121]):
            with self.assertRaises(MetaError) as caught:
                self.poster.publish("post", TARGET, payload())
        self.assertEqual(caught.exception.creation_id, "444")
        self.assertEqual(self.session.request.call_count, 2)

    def test_late_finished_response_does_not_publish_after_deadline(self):
        self.session.request.side_effect = [identity(), response({"id": "444"}),
                                            response({"status_code": "FINISHED"})]
        with patch("meta_poster.time.monotonic", side_effect=[0, 1, 121]):
            with self.assertRaises(MetaError) as caught:
                self.poster.publish("post", TARGET, payload())
        self.assertEqual(caught.exception.creation_id, "444")
        self.assertEqual(self.session.request.call_count, 3)

    def test_success_order_and_fixed_transport(self):
        self.session.request.side_effect = [identity(), response({"id": "444"}),
                                            response({"status_code": "IN_PROGRESS"}),
                                            response({"status_code": "FINISHED"}),
                                            response({"id": "555"})]
        with patch("meta_poster.time.sleep"):
            result = self.poster.publish("post", TARGET, payload())
        self.assertEqual(result["media_id"], "555")
        calls = self.session.request.call_args_list
        self.assertEqual([call.args[0] for call in calls], ["GET", "POST", "GET", "GET", "POST"])
        self.assertEqual([call.args[1] for call in calls], [
            "https://graph.instagram.com/v25.0/me",
            "https://graph.instagram.com/v25.0/12345/media",
            "https://graph.instagram.com/v25.0/444",
            "https://graph.instagram.com/v25.0/444",
            "https://graph.instagram.com/v25.0/12345/media_publish",
        ])
        for call in calls:
            self.assertIs(call.kwargs["allow_redirects"], False)
            self.assertEqual(call.kwargs["headers"], {"Authorization": f"Bearer {TOKEN}"})
            self.assertNotIn("access_token", call.kwargs["params"] or {})
            self.assertNotIn("access_token", call.kwargs["data"] or {})
        self.assertEqual(calls[-1].kwargs["data"], {"creation_id": "444"})

    def test_redirect_is_refused_without_disclosing_body(self):
        self.session.request.return_value = response({"error": {"message": TOKEN}}, 302)
        with self.assertRaises(MetaError) as caught:
            self.poster.check_identity()
        public = json.dumps(caught.exception.public())
        self.assertNotIn(TOKEN, public)
        self.assertIn("302", public)
        self.session.request.assert_called_once()
        self.session.request.return_value.json.assert_not_called()

    def test_error_only_reports_numeric_codes(self):
        self.session.request.return_value = response({"error": {
            "message": f"{TOKEN} {IMAGE_URL}", "code": 190, "error_subcode": "463",
            "fbtrace_id": TOKEN,
        }}, 400)
        with self.assertRaises(MetaError) as caught:
            self.poster.check_identity()
        public = caught.exception.public()
        self.assertEqual(public, {"ok": False, "error": "Meta rejected the request.",
                                  "http_status": 400, "code": 190, "subcode": 463})
        self.assertNotIn(TOKEN, json.dumps(public))
        self.assertNotIn(IMAGE_URL, json.dumps(public))

    def test_transport_error_is_sanitized_and_write_not_retried(self):
        self.session.request.side_effect = [identity(), URLError(f"{TOKEN} {IMAGE_URL}")]
        with self.assertRaises(MetaError) as caught:
            self.poster.publish("post", TARGET, payload())
        public = json.dumps(caught.exception.public())
        self.assertNotIn(TOKEN, public)
        self.assertNotIn(IMAGE_URL, public)
        self.assertIn("Do not retry automatically", public)
        self.assertEqual(self.session.request.call_count, 2)

    def test_check_cli_only_reads_and_does_not_consume_stdin(self):
        session = Mock()
        session.request.return_value = identity()
        output, errors = io.StringIO(), io.StringIO()
        stdin = Mock()
        with patch.dict("os.environ", ENV, clear=True), patch("meta_poster.UrllibTransport", return_value=session):
            with patch("sys.stdin", stdin), redirect_stdout(output), redirect_stderr(errors):
                code = main(["--check"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["mode"], "check")
        self.assertEqual(errors.getvalue(), "")
        self.assertEqual(session.request.call_args.args[0], "GET")
        session.request.assert_called_once()
        stdin.read.assert_not_called()
        self.assertNotIn(TOKEN, output.getvalue())

    def test_cli_sanitizes_invalid_json(self):
        output, errors = io.StringIO(), io.StringIO()
        with patch.dict("os.environ", ENV, clear=True), patch("meta_poster.UrllibTransport") as factory:
            with patch("sys.stdin", io.StringIO(TOKEN)), redirect_stdout(output), redirect_stderr(errors):
                code = main(["post", TARGET])
        self.assertEqual(code, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertNotIn(TOKEN, errors.getvalue())
        factory.return_value.request.assert_not_called()

    def test_configuration_requires_version_and_numeric_id(self):
        for variable, value in (("INSTAGRAM_API_VERSION", ""),
                                ("INSTAGRAM_API_VERSION", "https://bad.test"),
                                ("INSTAGRAM_USER_ID", "not-id")):
            with self.subTest(variable=variable):
                environment = dict(ENV)
                environment[variable] = value
                with self.assertRaises(MetaError):
                    Config.from_env(environment)

    def test_standard_transport_installs_redirect_refusal(self):
        with patch("meta_poster.build_opener") as build:
            UrllibTransport()
        handler = build.call_args.args[0]
        self.assertIsInstance(handler, NoRedirect)
        self.assertIsNone(handler.redirect_request(None, None, 302, "Found", {}, "https://other.test"))

    def test_standard_transport_keeps_token_in_header_and_encodes_caption(self):
        remote = Mock(code=200)
        remote.read.return_value = b'{"id":"444"}'
        remote.__enter__ = Mock(return_value=remote)
        remote.__exit__ = Mock(return_value=False)
        with patch("meta_poster.build_opener") as build:
            build.return_value.open.return_value = remote
            transport = UrllibTransport()
            result = transport.request("POST", "https://graph.instagram.com/v25.0/12345/media",
                                       headers={"Authorization": f"Bearer {TOKEN}"}, params=None,
                                       data={"caption": "Legenda com ação & paz", "image_url": IMAGE_URL},
                                       timeout=20, allow_redirects=False)
        request = build.return_value.open.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), f"Bearer {TOKEN}")
        self.assertNotIn(TOKEN, request.full_url)
        self.assertNotIn(TOKEN.encode(), request.data)
        self.assertIn(b"a%C3%A7%C3%A3o", request.data)
        self.assertEqual(result.json(), {"id": "444"})


if __name__ == "__main__":
    unittest.main()

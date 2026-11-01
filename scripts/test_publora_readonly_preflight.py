"""Offline checks for Publora connection probe; never accesses Publora."""
import io
import json
import unittest

from publora_readonly_preflight import evaluate, URL, EXPECTED_USERNAME


class FakeResponse:
    def __init__(self, response):
        self.data = json.dumps(response).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self, limit):
        return self.data[:limit]


def response(username="temumaexplicacao", token="valid", status="active"):
    return {"success": True, "connections": [{
        "platformId": "instagram-17841433004716815",
        "username": username,
        "tokenStatus": token,
        "connectionStatus": status,
    }]}


class PubloraReadOnlyTests(unittest.TestCase):
    def test_no_configuration_never_calls_network(self):
        def never(*args, **kwargs):
            raise AssertionError("network request forbidden")
        data = evaluate(None, None, never)
        self.assertEqual(data["mode"], "not_configured")
        self.assertFalse(data["mutations"])
        self.assertFalse(data["music_via_publora_api"])

    def test_incomplete_credentials_never_calls_network(self):
        def never(*args, **kwargs):
            raise AssertionError("network request forbidden")
        data = evaluate("sk_test", "invalid", never)
        self.assertEqual(data["mode"], "incomplete_credentials_or_platform_id")

    def test_get_only_and_exact_username(self):
        def fake(request, timeout):
            self.assertEqual(request.full_url, URL)
            self.assertEqual(request.get_method(), "GET")
            self.assertEqual(request.get_header("X-publora-key"), "sk_example")
            self.assertEqual(timeout, 15)
            return FakeResponse(response())
        result = evaluate("sk_example", "instagram-17841433004716815", fake)
        self.assertEqual(result["mode"], "verified")
        self.assertTrue(result["ok"])
        self.assertFalse(result["music_via_publora_api"])

    def test_wrong_account_is_rejected(self):
        def fake(request, timeout):
            return FakeResponse(response(username="someone_else"))
        result = evaluate("sk_example", "instagram-17841433004716815", fake)
        self.assertFalse(result["ok"])
        self.assertEqual(result["mode"], "account_or_token_not_ready")

    def test_expired_token_is_rejected(self):
        def fake(request, timeout):
            return FakeResponse(response(token="expired"))
        self.assertFalse(evaluate("sk_example", "instagram-17841433004716815", fake)["ok"])

    def test_missing_connection_is_rejected(self):
        def fake(request, timeout):
            return FakeResponse({"success": True, "connections": []})
        result = evaluate("sk_example", "instagram-17841433004716815", fake)
        self.assertEqual(result["mode"], "platform_id_not_found")


if __name__ == "__main__":
    unittest.main()

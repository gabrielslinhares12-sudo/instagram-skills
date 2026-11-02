from __future__ import annotations
import unittest
from instagram_preflight import REQUIRED, check
from meta_poster import MetaError


class FakePoster:
    def __init__(self, records):
        self.records = records
        self.identity_calls = 0
        self.requests = []

    def _request(self, method, endpoint):
        self.requests.append((method, endpoint))
        return {'data': self.records}

    def check_identity(self):
        self.identity_calls += 1
        return {'ok': True, 'username': 'temumaexplicacao'}


class PreflightTests(unittest.TestCase):
    def test_declined_publishing_grant_blocks_readiness_despite_other_grants(self):
        poster = FakePoster([{'permission': name, 'status': 'declined' if name ==
                             'instagram_content_publish' else 'granted'} for name in REQUIRED])
        self.assertEqual(check(poster)['missing_permissions'], ['instagram_content_publish'])
        self.assertEqual(poster.identity_calls, 0)

    def test_success_still_checks_identity_and_never_posts(self):
        poster = FakePoster([{'permission': name, 'status': 'granted'} for name in REQUIRED])
        result = check(poster)
        self.assertTrue(result['ok'])
        self.assertFalse(result['publishing_exercised'])
        self.assertEqual(poster.identity_calls, 1)
        self.assertEqual(poster.requests, [('GET', 'me/permissions')])

    def test_permission_inspection_error_200_checks_identity_but_not_grants(self):
        class BrokenPermissionPoster(FakePoster):
            def _request(self, method, endpoint):
                raise MetaError("Meta rejected the request.", http_status=400, code=200)
        poster = BrokenPermissionPoster([])
        result = check(poster)
        self.assertFalse(result['ok'])
        self.assertEqual(result['permission_inspection'], 'denied_code_200')
        self.assertFalse(result['permissions_verified'])
        self.assertEqual(result['required_permissions_granted'], [])
        self.assertFalse(result['publishing_exercised'])
        self.assertEqual(poster.identity_calls, 1)

    def test_permission_inspection_error_200_still_blocks_wrong_account(self):
        class WrongAccountPoster(FakePoster):
            def _request(self, method, endpoint):
                raise MetaError("Meta rejected the request.", http_status=400, code=200)
            def check_identity(self):
                return {'ok': True, 'username': 'different_user'}
        with self.assertRaises(MetaError) as caught:
            check(WrongAccountPoster([]))
        self.assertEqual(caught.exception.preflight_stage, "verify_account_identity")

    def test_other_permission_inspection_error_still_fails_closed(self):
        class ExpiredTokenPoster(FakePoster):
            def _request(self, method, endpoint):
                raise MetaError("Meta rejected the request.", http_status=401, code=190)
        with self.assertRaises(MetaError) as caught:
            check(ExpiredTokenPoster([]))
        self.assertEqual(caught.exception.preflight_stage, "read_permissions")
        self.assertEqual(caught.exception.public()["code"], 190)

    def test_account_identity_error_identifies_stage(self):
        class BrokenIdentityPoster(FakePoster):
            def check_identity(self):
                raise MetaError("Meta rejected the request.", http_status=400, code=200)
        poster = BrokenIdentityPoster([{"permission": x, "status": "granted"} for x in REQUIRED])
        with self.assertRaises(MetaError) as caught:
            check(poster)
        self.assertEqual(caught.exception.preflight_stage, "verify_account_identity")

    def test_invalid_permission_payload_rejected(self):
        with self.assertRaises(MetaError):
            check(FakePoster('untrusted invalid response'))


if __name__ == '__main__':
    unittest.main()

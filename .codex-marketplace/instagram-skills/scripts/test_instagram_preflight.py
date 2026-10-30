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

    def test_invalid_permission_payload_rejected(self):
        with self.assertRaises(MetaError):
            check(FakePoster('untrusted invalid response'))


if __name__ == '__main__':
    unittest.main()

"""Offline safety tests for TUE artifact retention."""
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import tue_verified_drive_artifact_cleanup as c

class SafetyTests(unittest.TestCase):
    def meta(self, name='tue-drive-backed-safe'):
        return {'id':123, 'name':name,'expired':False,
                'created_at':(datetime.now(timezone.utc)-timedelta(days=2)).isoformat()}

    def test_reject_other_artifact(self):
        with self.assertRaisesRegex(RuntimeError,'ARTIFACT_NAME_MISMATCH'):
            c.choose({'artifact_name':'faker-b'},self.meta('faker-a'),1)

    def test_reject_ledger_even_if_name_matches(self):
        with self.assertRaisesRegex(RuntimeError,'PROTECTED_ARTIFACT_TYPE'):
            c.choose({'artifact_name':'instagram-ledger-123'},self.meta('instagram-ledger-123'),1)

    def test_refuse_new_upload(self):
        x = self.meta()
        x['created_at']=datetime.now(timezone.utc).isoformat()
        with self.assertRaisesRegex(RuntimeError,'ARTIFACT_STILL_TOO_RECENT'):
            c.choose({'artifact_name':x['name']},x,1)

    def test_refuse_expired(self):
        x=self.meta()
        x['expired']=True
        with self.assertRaisesRegex(RuntimeError,'EXPIRED_OR_INVALID_ARTIFACT'):
            c.choose({'artifact_name':x['name']},x,1)

    def test_require_oauth(self):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaisesRegex(RuntimeError,'DRIVE_OAUTH_MISSING'):
                c.drive_token()

    def test_unique_drive_copy_required(self):
        import io, json
        class Response(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self, *args): self.close()
        with patch.object(c.request,'urlopen',return_value=Response(json.dumps({'files':[]}).encode())):
            with self.assertRaisesRegex(RuntimeError,'DRIVE_EXACT_NAME_NOT_UNIQUE'):
                c.drive_find_exact('something.zip','token')

if __name__=='__main__':
    unittest.main()
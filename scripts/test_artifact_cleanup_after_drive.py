import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("verified_cleanup", Path(__file__).with_name("after_drive_cleanup.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ROW = dict(artifact_id=13762140586, run_id=42808350863,
           artifact_name="faker-v54-official-riot-2023-native1080",
           size_bytes=17714302, drive_file_id="1hmglWzT346tnSJeJYvAOzRRBzE7Bke4E",
           drive_name="FAKER_V54_FOOTAGE_PRIVADO_QC_faker-v54-riot-2023-native1080.zip",
           drive_parent_id="1ZcO0TNjW8Cf18BKRXHfqY8qJc_6SoAgE",
           sha256="9368977491998b7e74721640a3c988c913a247df730f324d680909659cac5038")
ARTIFACT = dict(id=ROW['artifact_id'],name=ROW['artifact_name'],size_in_bytes=ROW['size_bytes'],
                expired=False,workflow_run={'id':ROW['run_id']})

class SafeCleanupTests(unittest.TestCase):
    def test_valid_receipt_and_metadata(self):
        mod.validate_row(ROW)
        mod.validate_artifact_metadata(ARTIFACT, ROW)

    def test_bad_artifact_name_blocks(self):
        with self.assertRaises(RuntimeError):
            mod.validate_artifact_metadata({**ARTIFACT, 'name':'different'},ROW)

    def test_wrong_run_blocks(self):
        with self.assertRaises(RuntimeError):
            mod.validate_artifact_metadata({**ARTIFACT,'workflow_run':{'id':2}},ROW)

    def test_wrong_size_blocks(self):
        with self.assertRaises(RuntimeError):
            mod.validate_artifact_metadata({**ARTIFACT,'size_in_bytes':ROW['size_bytes']-1},ROW)

    def test_bad_checksum_blocks(self):
        with self.assertRaises(ValueError):
            mod.validate_row({**ROW,'sha256':'1234'})

    def test_bad_drive_id_blocks(self):
        with self.assertRaises(ValueError):
            mod.validate_row({**ROW,'drive_file_id':'x'})

    def test_expired_blocks(self):
        with self.assertRaises(RuntimeError):
            mod.validate_artifact_metadata({**ARTIFACT,'expired':True},ROW)

    def test_redirect_sanitizes_auth(self):
        handler = mod.SafeRedirect()
        import urllib.request
        req=urllib.request.Request('https://api.github.com/something', headers={'Authorization':'Bearer secret'})
        redirect=handler.redirect_request(req,None,302,'Found',{},'https://objects.githubusercontent.com/path')
        self.assertIsNone(redirect.get_header('Authorization'))
        with self.assertRaises(RuntimeError):
            handler.redirect_request(req,None,302,'Found',{},'https://evil.test/path')

if __name__ == '__main__':
    unittest.main()
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import instagram_duoplus_readiness as m

class DuoPlusReadinessTests(unittest.TestCase):
    def test_no_credentials_no_network(self):
        with patch.dict(m.os.environ,{},clear=True),patch.object(m,"request_status") as fn:
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(m.main(),0)
            fn.assert_not_called()
            self.assertIn("api_key_not_connected",output.getvalue())
    def test_no_phone_no_network_and_no_secret_log(self):
        with patch.dict(m.os.environ,{"DUOPLUS_API_KEY":"secret-key"},clear=True),patch.object(m,"request_status") as fn:
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(m.main(),0)
            fn.assert_not_called()
            self.assertNotIn("secret-key",output.getvalue())
    def test_ready_requires_http_enabled(self):
        for status,http,expected in [(1,1,True),(1,0,False),(2,1,False)]:
            self.assertEqual(m.check({"code":200,"data":{"list":[{
                "id":"p1","status":status,"http_status":http}]}}, "p1")["ready"],expected)
    def test_wrong_device_not_ready(self):
        self.assertFalse(m.check({"code":200,"data":{"list":[{"id":"other","status":1,"http_status":1}]}}, "p1")["ready"])
    def test_redact_sensitive_fields(self):
        result=m.check({"code":200,"data":{"list":[{
            "id":"p1","status":1,"http_status":1,"os":"Android 15",
            "ip":"10.3.4.5","adb_password":"hiddenpwd","name":"real person"}]}}, "p1")
        self.assertTrue(result["ready"])
        self.assertNotIn("10.3.4.5",str(result))
        self.assertNotIn("hiddenpwd",str(result))
        self.assertNotIn("real person",str(result))
    def test_api_rejection(self):
        self.assertFalse(m.check({"code":401,"message":"some private error"}, "p1")["ready"])

if __name__=="__main__":unittest.main()

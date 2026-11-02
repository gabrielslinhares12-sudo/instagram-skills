#!/usr/bin/env python3
import unittest
from instagram_android_official_app_preflight import classify,parse_nodes

def make(*items):
    return parse_nodes("<hierarchy>"+"".join(
        '<node text="{}" content-desc="" package="{}" enabled="true" bounds="[0,0][100,70]"/>'.format(*i)
        for i in items)+"</hierarchy>")

class Gate(unittest.TestCase):
    def test_google_login_blocks_install(self):
        nodes=make(("Instagram","com.android.vending"),("Install","com.android.vending"),
                   ("Sign in","com.android.vending"))
        self.assertEqual(classify(nodes),"google_sign_in_required")
    def test_official_store_install_only(self):
        self.assertEqual(classify(make(("Instagram","com.android.vending"),
                                       ("Install","com.android.vending"))),"install_available")
    def test_wrong_package_cannot_install(self):
        self.assertEqual(classify(make(("Instagram","com.android.vending"),
                                       ("Install","com.evil.apk"))),"official_install_unavailable")
    def test_installed_overrides_signin(self):
        self.assertEqual(classify(make(("Sign in","com.android.vending")),True),"instagram_installed")
    def test_unknown_ui_blocks(self):
        self.assertEqual(classify([]),"ui_unavailable")

if __name__=="__main__":unittest.main()

"""Offline-only tests for Android audio automation, without an attached phone."""
import unittest
from instagram_mobile_music import matches, normalized, parse_nodes, select_pending, QueueError


def xml(*nodes):
    tags = []
    for text, desc, bounds in nodes:
        tags.append('<node text="'+text+'" content-desc="'+desc+
                    '" bounds="'+bounds+'" clickable="true" resource-id=""/>')
    return "<hierarchy>"+ "".join(tags) + "</hierarchy>"


class MusicUiTests(unittest.TestCase):
    def test_handles_native_ptbr_and_english_labels(self):
        nodes = parse_nodes(xml(("Adicionar música", "", "[0,100][400,200]"),
                                ("", "Mais opções", "[410,100][500,200]")))
        self.assertEqual(len(matches(nodes, ("Adicionar musica",))), 1)
        self.assertEqual(len(matches(nodes, ("Mais opções",))), 1)
        self.assertEqual(normalized("História"), "historia")

    def test_refuses_duplicate_controls(self):
        nodes = parse_nodes(xml(("Salvar", "", "[0,0][100,50]"),
                                ("Salvar", "", "[0,100][100,150]")))
        self.assertEqual(len(matches(nodes, ("Salvar",))), 2)

    def test_invalid_xml_fails_closed(self):
        with self.assertRaises(QueueError):
            parse_nodes("not XML")

    def test_requires_exact_existing_post_and_approved_music_mode(self):
        post={"id":"my-carousel","kind":"carousel","approved":True,
              "username":"temumaexplicacao","target_url":"https://www.instagram.com/temumaexplicacao/",
              "caption":"Teste","due_at":"2026-11-01T17:00:00Z",
              "media_urls":["https://example.com/1.jpg","https://example.com/2.jpg"],
              "distribution_mode":"api_carousel_then_native_music",
              "owner_authorized_two_step_music":True}
        from instagram_queue import fingerprint
        state={"version":1,"items":{"my-carousel":{
            "status":"awaiting_native_music",
            "fingerprint":fingerprint(post),
            "media_id":"18107496023215107",
            "permalink":"https://www.instagram.com/p/DfNVlLDmC8P/"}}}
        result=select_pending({"version":1,"posts":[post]},state,None)
        self.assertEqual(result["id"],"my-carousel")
        state["items"]["my-carousel"]["status"]="published"
        with self.assertRaises(QueueError):
            select_pending({"version":1,"posts":[post]},state,None)
        state["items"]["my-carousel"]["status"]="awaiting_native_music"
        state["items"]["my-carousel"]["permalink"]="https://evil.example/post"
        with self.assertRaises(QueueError):
            select_pending({"version":1,"posts":[post]},state,None)

    def test_never_assumes_music_without_configured_track(self):
        from instagram_queue import fingerprint
        post={"id":"test","kind":"carousel","approved":True,
              "username":"temumaexplicacao","target_url":"https://www.instagram.com/temumaexplicacao/",
              "caption":"Teste","due_at":"2026-11-01T17:00:00Z",
              "media_urls":["https://example.com/a.jpg","https://example.com/b.jpg"],
              "distribution_mode":"api_carousel_then_native_music",
              "owner_authorized_two_step_music":True}
        state={"version":1,"items":{"test":{"status":"awaiting_native_music",
              "fingerprint":fingerprint(post),"media_id":"18107496023215107",
              "permalink":"https://www.instagram.com/p/DfNVlLDmC8P/"}}}
        task=select_pending({"version":1,"posts":[post]},state,"test")
        self.assertIsNone(task["track"])
        self.assertIsNone(task["artist"])


if __name__=="__main__":
    unittest.main()

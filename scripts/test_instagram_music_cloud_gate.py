"""Offline cloud-only contract: preserve original post and never fabricate edits."""
import unittest
from pathlib import Path
from unittest.mock import patch
import instagram_music_cloud_gate as gate

class CloudMusicGateTests(unittest.TestCase):
    def test_gate_can_audit_existing_approved_halloween_without_mutation(self):
        state_path = gate.ROOT / "content/publication-state.json"
        before = state_path.read_bytes()
        result = gate.audit()
        self.assertTrue(result["ok"])
        self.assertEqual(result["media_id"], "18107496023215107")
        self.assertEqual((result["approved_track"],result["approved_artist"]),
                         ("Thriller","Michael Jackson"))
        self.assertEqual(result["images_preserved"],8)
        self.assertFalse(result["official_graph_native_audio_edit_supported"])
        self.assertFalse(result["documented_instagrapi_existing_carousel_audio_edit_supported"])
        self.assertFalse(result["cloud_audio_edit_attempted"])
        self.assertFalse(result["new_post_created"])
        self.assertEqual(before,state_path.read_bytes())

    def test_wrong_song_rejected_without_touching_instagram(self):
        assignment=gate.load_music_assignments()
        with patch.object(gate,"load_music_assignments",
             return_value={gate.ID:dict(assignment[gate.ID],track="Cover")}):
            with self.assertRaises(gate.QueueError):
                gate.audit()

    def test_unconfirmed_receipt_rejected(self):
        original=gate.read_document
        def alter(path, *args, **kwargs):
            data=original(path,*args,**kwargs)
            if str(path).endswith("publication-state.json"):
                from copy import deepcopy
                data=deepcopy(data)
                data["items"][gate.ID]["media_id"]="000"
            return data
        with patch.object(gate,"read_document",side_effect=alter):
            with self.assertRaises(gate.QueueError):
                gate.audit()

if __name__ == "__main__":
    unittest.main()

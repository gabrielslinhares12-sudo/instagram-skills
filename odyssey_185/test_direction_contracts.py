#!/usr/bin/env python3
"""Valida o roteiro de direcao 185 s; nao aprova renders nem autoriza publicacao."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "odyssey_185" / "ROTEIRO_DIRECAO_COMPLETA_TUE_MESTRE_01.md"
CONTRACT = ROOT / "odyssey_185" / "shot_direction_185.json"
MANIFEST = ROOT / "odyssey_185" / "manifest_v9.json"
MASTER = "odyssey_v8/PADRAO_MESTRE_TUE_ANIMACAO.md"


class Direction185Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.text = SCRIPT.read_text(encoding="utf-8")

    def test_master_exists_and_everything_uses_it(self):
        self.assertTrue((ROOT / MASTER).is_file())
        self.assertEqual(self.contract["production_standard"], MASTER)
        self.assertEqual(self.manifest["production_standard"], MASTER)
        self.assertIn("TUE-ANIMACAO-MESTRE-01", self.text)

    def test_narration_is_verbatim_and_ordered(self):
        a, b = self.contract["scenes"], self.manifest["scenes"]
        self.assertEqual(len(a), len(b))
        self.assertEqual(len(a), 16)
        for expected, actual in zip(b, a):
            self.assertEqual(actual["id"], expected["id"])
            self.assertEqual(actual["narration"], expected["narration"])
            self.assertIn(actual["narration"], self.text)
            self.assertEqual(actual["start_seconds"], expected["start_seconds"])
            self.assertEqual(actual["end_seconds"], expected["end_seconds"])

    def test_shots_cover_entire_185_seconds_at_60fps(self):
        scenes = self.contract["scenes"]
        self.assertEqual(scenes[0]["start_seconds"], 0)
        self.assertEqual(scenes[-1]["end_seconds"], 185)
        count, frames = 0, 0
        previous_end = 0.0
        for s in scenes:
            self.assertAlmostEqual(s["start_seconds"], previous_end, places=5)
            shots = s["shots"]
            self.assertTrue(shots)
            self.assertAlmostEqual(shots[0]["start_seconds"], s["start_seconds"], places=5)
            last = s["start_seconds"]
            for shot in shots:
                self.assertAlmostEqual(shot["start_seconds"], last, places=5)
                self.assertGreater(shot["end_seconds"], shot["start_seconds"])
                self.assertEqual(shot["frames"], round(60 * (shot["end_seconds"] - shot["start_seconds"])))
                self.assertTrue(shot["action"].strip())
                self.assertTrue(shot["lens"].strip())
                self.assertTrue(shot["foley"].strip())
                frames += shot["frames"]
                count += 1
                last = shot["end_seconds"]
            self.assertAlmostEqual(last, s["end_seconds"], places=5)
            previous_end = s["end_seconds"]
        self.assertEqual(count, 74)
        self.assertEqual(frames, 11_100)

    def test_each_scene_declares_actors_props_and_3d_art_direction(self):
        for s in self.contract["scenes"]:
            with self.subTest(scene=s["id"]):
                self.assertTrue(s["cast"])
                self.assertEqual(len(s["cast"]), len(set(s["cast"])))
                self.assertTrue(s["props"])
                self.assertTrue(s["set_id"].startswith("SET_"))
                self.assertTrue(s["art_and_environment"])
                self.assertTrue(s["camera_direction"])
                self.assertTrue(s["continuity"])
                self.assertTrue(s["negative_rules"])
                self.assertFalse(s["approved"])
        self.assertFalse(self.contract["publication_allowed"])
        self.assertFalse(self.contract["film_generated"])
        self.assertFalse(self.contract["audio_generated"])

    def test_ithaca_is_faithful_to_sleeping_arrival(self):
        ithaca = self.contract["scenes"][11]
        self.assertIn("adormecido", ithaca["continuity"])
        self.assertIn("adormecido", " ".join(x["action"] for x in ithaca["shots"]))
        self.assertIn("PROP_LEITO_OLIVEIRA", self.contract["scenes"][15]["props"])
        self.assertIn("PROP_PEDRA_SELAMENTO", self.contract["scenes"][3]["props"])


if __name__ == "__main__":
    unittest.main()

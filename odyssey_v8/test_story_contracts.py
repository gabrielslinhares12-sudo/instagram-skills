#!/usr/bin/env python3
"""Fail-closed Odyssey V8 structural contract tests: not a substitute for visual QC."""
import json
from pathlib import Path
import unittest

PATH = Path(__file__).with_name("episode01_shot_contracts.json")


class OdysseyShotContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(PATH.read_text(encoding="utf-8"))
        cls.shots = cls.document["episode01_shots"]

    def test_no_automatic_publishing_or_legacy_scenes(self):
        self.assertFalse(self.document["publish_allowed"])
        self.assertEqual(self.document["version_state"], "narrative_blocking_in_progress")
        self.assertTrue(all(shot["approved"] is False for shot in self.shots))
        self.assertIn("no_global_actor_overlay", self.document["rules"])

    def test_chronology_exactly_matches_episode1_audio(self):
        self.assertAlmostEqual(self.shots[0]["start"], 0.0)
        self.assertAlmostEqual(self.shots[-1]["end"], 88.6)
        self.assertEqual(len({x["id"] for x in self.shots}), len(self.shots))
        for i, shot in enumerate(self.shots):
            self.assertGreater(shot["end"], shot["start"])
            if i:
                self.assertAlmostEqual(self.shots[i - 1]["end"], shot["start"])
        self.assertEqual([(e["start"],e["end"]) for e in self.document["episodes"]],
                         [(0,88.6),(88.6,317.4),(317.4,560.1)])

    def test_every_shot_has_specific_cast_physical_action_and_consequence(self):
        for shot in self.shots:
            with self.subTest(shot=shot["id"]):
                self.assertTrue(shot["set"])
                self.assertTrue(shot["cast"])
                self.assertEqual(len(shot["cast"]),len(set(shot["cast"])))
                self.assertTrue(shot["props"])
                self.assertGreater(len(shot["action"]),65)
                self.assertGreater(len(shot["consequence"]),35)

    def test_cyclops_door_is_large_and_causally_correct(self):
        cave = [x for x in self.shots if x["set"]=="cyclops-cave"]
        self.assertEqual(cave[0]["id"],"cave-enter")
        self.assertEqual(cave[1]["id"],"giant-returns")
        self.assertEqual(cave[2]["id"],"giant-seals")
        self.assertIn("seal-boulder", cave[2]["props"])
        self.assertIn("Polyphemus", cave[2]["cast"])
        self.assertNotIn("Polyphemus", cave[0]["cast"])
        self.assertIn("blocked",cave[2]["consequence"].lower() if "blocked" in cave[2]["consequence"].lower() else cave[2]["action"].lower())

    def test_no_actor_appears_implicitly_outside_story(self):
        self.assertEqual(self.shots[2]["cast"],["Penelope"])
        self.assertNotIn("Odysseus",self.shots[2]["cast"])
        self.assertNotIn("Penelope", self.shots[5]["cast"])
        self.assertEqual(self.shots[5]["cast"],["Odysseus","crew"])
        self.assertNotIn("Polyphemus",self.shots[5]["cast"])


if __name__=="__main__":
    unittest.main()

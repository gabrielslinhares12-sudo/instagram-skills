#!/usr/bin/env python3
"""TUE-MESTRE-01 tests: explicit lock against generic art passing as approved."""
import copy
import unittest
from instagram_preset_mestre import (
    IDENTITY, REFERENCE_SHA, LUMINO_SHA, PresetError,
    check_brief, check_release, verify
)


class MasterPresetTests(unittest.TestCase):
    def setUp(self):
        self.preset = verify()
        self.brief = {
            "preset_id": IDENTITY, "reference_sha256": REFERENCE_SHA,
            "lumino_sha256": LUMINO_SHA,
            "status": "draft_review_no_publication", "approved": False,
            "kind": "carousel", "sources": ["TSE: exemplo verificado"],
            "slides": [
                {"headline": "Gancho editorial forte", "new_information": "Contexto factual aprofundado",
                 "distinct_scene": "Cena fotográfica de urna real", "visual_direction": "Modelo 1 com pincelada amarelo",
                 "source_credit": "Autor de imagem identificado", "uses_original_lumino": True},
                {"headline": "Explicação com detalhes", "new_information": "Exemplo numérico com lógica",
                 "distinct_scene": "Cena com gráfica da divisão", "visual_direction": "Infográfico contextual foto",
                 "source_credit": "Dados ilustrativos com fonte", "uses_original_lumino": True},
            ]
        }

    def test_profile_and_source_assets_exist(self):
        self.assertEqual(self.preset["id"], IDENTITY)

    def test_valid_draft_not_approved(self):
        self.assertEqual(check_brief(self.brief, self.preset)["draft_only"], True)

    def test_missing_invocation_blocked(self):
        self.brief.pop("preset_id")
        with self.assertRaisesRegex(PresetError, IDENTITY):
            check_brief(self.brief, self.preset)

    def test_missing_canonical_mascot_blocked(self):
        self.brief["slides"][0]["uses_original_lumino"] = False
        with self.assertRaisesRegex(PresetError, "original"):
            check_brief(self.brief, self.preset)

    def test_identical_scene_rejected(self):
        self.brief["slides"][1]["distinct_scene"] = self.brief["slides"][0]["distinct_scene"]
        with self.assertRaisesRegex(PresetError, "repetidas"):
            check_brief(self.brief, self.preset)

    def test_auto_approval_rejected(self):
        self.brief["approved"] = True
        with self.assertRaisesRegex(PresetError, "automaticamente"):
            check_brief(self.brief, self.preset)

    def test_release_requires_review_ledger(self):
        with self.assertRaisesRegex(PresetError, "não foi ativado"):
            check_release({"approved": True})
        with self.assertRaisesRegex(PresetError, "Comparação visual"):
            check_release({"preset_id": IDENTITY})

    def test_release_requires_quality_on_all_screens(self):
        qc = {"reference_sha256": REFERENCE_SHA, "reviewer_note": "Comparei cada lâmina com o modelo 1 e qualidade visual interna."}
        qc.update({v: True for v in (
            "cover_matches_model_1","inner_pages_match_cover_quality",
            "original_lumino_visually_confirmed","all_text_readable",
            "all_facts_checked","sources_and_rights_checked",
            "no_unnecessary_repeated_scenes","swipe_cue_verified",
            "no_visible_page_numbers")})
        check_release({"preset_id": IDENTITY, "human_visual_qc": qc})
        qc["inner_pages_match_cover_quality"] = False
        with self.assertRaisesRegex(PresetError, "página por página"):
            check_release({"preset_id": IDENTITY, "human_visual_qc": qc})


if __name__ == "__main__":
    unittest.main()

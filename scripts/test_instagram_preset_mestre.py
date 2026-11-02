#!/usr/bin/env python3
"""TUE-MESTRE-01 tests: explicit lock against generic art passing as approved."""
import copy
import unittest
from instagram_preset_mestre import (
    IDENTITY, LUMINO_SHA, PresetError,
    check_brief, check_release, verify
)


class MasterPresetTests(unittest.TestCase):
    def setUp(self):
        self.preset = verify()
        self.brief = {
            "preset_id": IDENTITY, "reference_standard_id": IDENTITY,
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
        qc = {"reference_standard_id": IDENTITY, "reviewer_note": "Comparei cada lâmina com o modelo 1 e qualidade visual interna."}
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


    def test_week_topics_must_be_unique_and_posts_independent(self):
        from instagram_preset_mestre import check_week
        def make(post_id, day, slot, topic):
            return {"id":post_id,"day":day,"slot":slot,"topic_id":topic,
                    "subject_id":"assunto-"+topic,"approved":False,
                    "part_of_series":False}
        first=make("p1","2026-11-02","11:00","ondas-cruzadas")
        second=make("p2","2026-11-02","15:00","geladeira-juri")
        week={"preset_id":IDENTITY,"status":"draft_review_no_publication",
              "posts":[first,second]}
        self.assertTrue(check_week(week)["independent_subjects"])
        second["topic_id"]="ondas-cruzadas"
        with self.assertRaisesRegex(PresetError,"duplicados"):
            check_week(week)
        second["topic_id"]="geladeira-juri"
        second["companion_to"]="p1"
        with self.assertRaisesRegex(PresetError,"derivada"):
            check_week(week)

    def test_week_subject_reuse_across_dates_is_blocked(self):
        from instagram_preset_mestre import check_week
        week={"preset_id":IDENTITY,"status":"draft_review_no_publication",
              "posts":[
                {"id":"p1","day":"2026-11-02","slot":"11:00",
                 "topic_id":"mar-quadrado","subject_id":"ondas-cruzadas","approved":False},
                {"id":"p2","day":"2026-11-03","slot":"15:00",
                 "topic_id":"outra-forma-do-mar","subject_id":"ondas-cruzadas","approved":False}
              ]}
        with self.assertRaisesRegex(PresetError,"duplicados"):
            check_week(week)

    def test_reels_stories_provenance_and_order(self):
        from pathlib import Path
        import json
        from validate_instagram_weekly_briefs import verify_reels_and_stories
        base=Path(__file__).resolve().parent.parent
        feed=json.loads((base/"content/editorial/semana-independente-2026-11-02-a-08/grade.json").read_text(encoding="utf-8"))
        plan=json.loads((base/"content/editorial/REELS-E-STORIES-2026-11-02-a-08.json").read_text(encoding="utf-8"))
        self.assertEqual(verify_reels_and_stories(plan,feed)["reels_planned"],7)
        changed=copy.deepcopy(plan)
        changed["reels"][0]["story_published"]=True
        with self.assertRaisesRegex(PresetError,"Story não pode preceder"):
            verify_reels_and_stories(changed,feed)
        changed=copy.deepcopy(plan)
        changed["reels"][0]["approved"]=True
        with self.assertRaisesRegex(PresetError,"origem verificadas"):
            verify_reels_and_stories(changed,feed)
        changed=copy.deepcopy(plan)
        changed["reels"][0]["topic_id"]=feed["posts"][0]["topic_id"]
        with self.assertRaisesRegex(PresetError,"repete tema"):
            verify_reels_and_stories(changed,feed)

if __name__ == "__main__":
    unittest.main()

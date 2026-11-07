#!/usr/bin/env python3
"""Odyssey 2D editorial consistency gate: checks shot uniqueness and prohibits publication without shot-by-shot artistic approval."""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path


def verify(path: Path, require_approved: bool = False) -> dict:
    payload = json.loads(path.read_text(encoding='utf-8'))
    shots = payload['shots']
    assert payload['scene_count'] == 16 and len(shots) == payload['shot_count'] == 68
    assert abs(payload['audio_seconds'] - 220.56) < .01
    assert payload['audio_original_sha256'] == '9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667'
    assert payload['hero_source_asset'] == 'ODISSEU_ORIGINAL_TROIA_SPRITE_CANONICO.png'
    assert payload['horse_source_asset'] == 'CAVALO_TROIA_ORIGINAL_RGBA.png'
    assert abs(payload['scale_ratio'] - 5.5/1.84) < 1e-9
    assert collections.Counter(int(s['scene']) for s in shots) == {i:(8 if i==4 else 4) for i in range(1,17)}
    for key in ('shot_id', 'narrative_action', 'environment_identity'):
        assert len({s[key] for s in shots}) == len(shots), f'DUPLICATED_{key}'
    for i,shot in enumerate(shots):
        assert shot['shot_id'] == f"S{shot['scene']:02d}_A{shot['beat']:02d}"
        assert shot['end_seconds_estimate'] > shot['start_seconds_estimate']
        assert len(shot['cast']) > 0 and len(shot['environment_identity']) > 5
        assert shot['continuous_spatial_blocking_required']
        assert shot['pose_keyframes_required'] >= 4
        if i:
            assert abs(shot['start_seconds_estimate'] - shots[i-1]['end_seconds_estimate']) < .005
    assert abs(shots[0]['start_seconds_estimate']) < 1e-4
    assert abs(shots[-1]['end_seconds_estimate'] - payload['audio_seconds']) < .01
    approved = sum(bool(s['artist_qc_approved']) for s in shots)
    report = {'scenes':16, 'planned_shots':68, 'distinct_action_descriptions':68,
              'distinct_environment_descriptions':68, 'artist_approved_shots': approved,
              'all_cinematography_rendered_and_verified':False,
              'all_audio_wordlevel_synced_verified':False,
              'publication_allowed':False}
    if require_approved:
        assert approved == 68, 'BLOCKED: each scene must pass visual and audio editorial QC'
        assert payload['editorial_qc_approved'] and payload['publication_allowed'], 'BLOCKED: final editorial approval missing'
        # Manual signed render QC still needed; this gate can't infer pixel-level quality.
        raise AssertionError('BLOCKED: no independent frame-by-frame cinematic proof attached')
    assert payload['publication_allowed'] is False, 'UNAUTHORIZED_PUBLICATION_SETTING'
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('contract',type=Path)
    parser.add_argument('--require-approved', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.contract,args.require_approved),ensure_ascii=False,indent=2))
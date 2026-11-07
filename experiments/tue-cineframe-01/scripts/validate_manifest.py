#!/usr/bin/env python3
"""Validacao de contrato TUE-CINEFRAME-01, somente biblioteca padrao Python."""
import json
import sys
from pathlib import Path

REQUIRED = (
    "shot_id", "scene_id", "duration_sec", "characters", "set_id",
    "action", "preparation", "consequence", "start_state", "end_state",
    "camera", "physical_contacts", "lighting", "narration_exact",
    "audio_timecode", "motion_mode", "start_reference", "end_reference",
    "negative_constraints"
)

def validate(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    if data.get("standard_id") != "TUE-CINEFRAME-01":
        errors.append("standard_id incorreto")
    if data.get("status") != "experimental":
        errors.append("status deve permanecer experimental")
    if data.get("release_policy") != "never_auto_publish":
        errors.append("publicacao automatica proibida")
    output = data.get("output", {})
    for key, value in [("width", 2160), ("height", 3840), ("fps", 60), ("aspect_ratio", "9:16")]:
        if output.get(key) != value:
            errors.append(f"output.{key} esperado {value}")
    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        errors.append("shots vazio")
        shots = []
    ids = set()
    for i, shot in enumerate(shots, start=1):
        for field in REQUIRED:
            if field not in shot or shot[field] in ("", None, []):
                errors.append(f"tomada {i}: falta {field}")
        identity = shot.get("shot_id")
        if identity in ids:
            errors.append(f"shot_id repetido: {identity}")
        ids.add(identity)
        duration = shot.get("duration_sec")
        if not isinstance(duration, (float, int)) or isinstance(duration, bool) or duration <= 0:
            errors.append(f"tomada {i}: duration_sec invalida")
        elif duration > 8 and not shot.get("long_shot_justification"):
            errors.append(f"tomada {i}: >8s exige long_shot_justification")
        if shot.get("motion_mode") not in ("rig_2d", "image_to_video"):
            errors.append(f"tomada {i}: motion_mode invalido")
        if not isinstance(shot.get("characters"), list):
            errors.append(f"tomada {i}: characters deve ser lista")
        if not isinstance(shot.get("negative_constraints"), list):
            errors.append(f"tomada {i}: negative_constraints deve ser lista")
    return errors, sum(s.get("duration_sec", 0) for s in shots
                       if isinstance(s.get("duration_sec"), (float, int)) and
                       not isinstance(s.get("duration_sec"), bool))

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 validate_manifest.py <manifest.json>")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERRO: arquivo nao encontrado: {path}")
        return 2
    try:
        errors, duration = validate(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}")
        return 2
    if errors:
        for err in errors:
            print(f"FALHA: {err}")
        return 1
    print(f"OK: padrao valido, duracao ilustrativa {duration:.1f}s; sem publicacao.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

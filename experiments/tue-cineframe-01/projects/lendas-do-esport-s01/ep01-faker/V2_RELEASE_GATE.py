#!/usr/bin/env python3
"""TUE-CINEFRAME-01 EP01 Faker V2 — gate fail-closed.

Nunca chama de pronto um arquivo que só tenha dimensões 4K60 ou um rig vetorial
esquemático. O teste depende também das etapas editoriais verificadas.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def probe_video(path):
    if shutil.which("ffprobe") is None:
        return None, ["ffprobe indisponível"]
    if not Path(path).is_file():
        return None, ["MP4 final não encontrado"]
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "stream=width,height,avg_frame_rate,codec_name,duration:format=duration",
             "-of", "json", str(path)],
            capture_output=True, text=True, check=True, timeout=90,
        )
        j = json.loads(p.stdout)
    except (OSError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        return None, [f"Falha de ffprobe: {exc}"]
    v = next((s for s in j.get("streams", []) if s.get("width") and s.get("height")), None)
    if not v:
        return None, ["Stream de vídeo ausente"]
    try:
        n, d = map(int, v.get("avg_frame_rate", "0/1").split("/"))
        fps = n / d
    except (ValueError, ZeroDivisionError):
        fps = 0
    errors = []
    if v.get("width") != 2160 or v.get("height") != 3840:
        errors.append("dimensão diferente de 2160x3840")
    if abs(fps - 60) > .01:
        errors.append(f"FPS diferente de 60: {fps}")
    if v.get("codec_name") != "h264":
        errors.append("codec diferente de h264")
    duration = float(j.get("format", {}).get("duration") or 0)
    if duration <= 0:
        errors.append("Duração ausente")
    return {"width": v["width"], "height": v["height"], "fps": fps, "duration": duration}, errors


def validate(m, movie=None):
    problems = []
    if m.get("standard_id") != "TUE-CINEFRAME-01":
        problems.append("modelo errado")
    if m.get("release_policy") != "NO_PREVIEW_UNTIL_QUALITY_PASS":
        problems.append("bloqueio de prévia não configurado")
    refs = m.get("references") or {}
    if (refs.get("canonical_character_sheet") or {}).get("drive_file_id") != "163C38f5RBR1mtf7r8z9FBYuQfrJubQnF":
        problems.append("concept sheet oficial não está ancorado")
    output = m.get("output") or {}
    if (output.get("width"), output.get("height"), output.get("fps")) != (2160, 3840, 60):
        problems.append("contrato de exportação 4K60 incorreto")
    if output.get("upscale_as_native") is not False:
        problems.append("falsa qualidade nativa não está proibida")
    motion = m.get("motion_director") or {}
    if motion.get("sample_frames", 0) < 6720 or motion.get("planned_shots") != 14:
        problems.append("dados de movimento 14 tomadas/60fps ausentes")
    if motion.get("technical_curves_qc_passed") is not True:
        problems.append("QA de trajetórias de movimento reprovado")
    if motion.get("rendered_in_final_art") is not True:
        problems.append("curvas ainda não aplicadas à arte final aprovada")
    if motion.get("visual_movement_qc_approved") is not True:
        problems.append("atuação animada real não validada visualmente")
    art = m.get("art_assets") or {}
    if not art.get("rig_layer_pack") or not art.get("layer_pack_approved"):
        problems.append("rig completo, fiel à ficha, ainda não aprovado")
    if not art.get("source_licenses_verified"):
        problems.append("direitos dos assets não verificados")
    for k, v in (art.get("character_views") or {}).items():
        if not v:
            problems.append("vista de personagem ausente: " + k)
    for k, v in (art.get("stage_sets") or {}).items():
        if not v:
            problems.append("cenário final ausente: " + k)
    if not m.get("voice", {}).get("audio_present") or not m.get("voice", {}).get("file_sha256"):
        problems.append("áudio Rasalgethi original verificado ausente")
    shots = m.get("shots") or []
    if len(shots) < 14:
        problems.append("faltam tomadas do roteiro")
    seen = set()
    for shot in shots:
        sid = shot.get("id", "SEM_ID")
        if sid in seen:
            problems.append("tomada duplicada " + sid)
        seen.add(sid)
        if not shot.get("clip_file"):
            problems.append(f"{sid}: MP4 da tomada ausente")
        for k in ("rig_and_background_verified", "first_mid_last_qc", "actor_and_prop_contact_qc"):
            if shot.get(k) is not True:
                problems.append(f"{sid}: QC {k} não aprovado")
    for k, v in (m.get("review") or {}).items():
        if v is not True:
            problems.append("QC bloqueante: " + k)
    delivery = m.get("delivery") or {}
    if not delivery.get("uploaded_video_id") or not delivery.get("readback_verified"):
        problems.append("Drive final sem leitura de verificação")
    if delivery.get("instagram_publish") is not False:
        problems.append("publicação automatizada deve permanecer proibida")
    if movie:
        _, errors = probe_video(movie)
        problems.extend(errors)
    else:
        problems.append("MP4 final não informado")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--movie", type=Path)
    args = ap.parse_args()
    if not args.manifest.is_file():
        print("REPROVADO: manifesto ausente")
        return 2
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        failures = validate(data, args.movie)
    except (OSError, ValueError) as exc:
        print("REPROVADO: ", exc)
        return 2
    if failures:
        print(f"REPROVADO: {len(failures)} critérios pendentes")
        for reason in failures[:30]:
            print(" -", reason)
        if len(failures) > 30:
            print(" - ... mais", len(failures) - 30)
        return 1
    print("LIBERADO PARA ENTREGA AO USUÁRIO: todos os critérios técnicos/editoriais comprovados")
    print("NÃO significa autorização de postagem")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

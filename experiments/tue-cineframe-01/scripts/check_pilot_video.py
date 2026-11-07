#!/usr/bin/env python3
"""Verificador bloqueante para pilotos TUE-CINEFRAME-01.

Checa metadados do arquivo final usando ffprobe. Origem das imagens/rigs
precisa de atestação editorial separada; metadados NÃO provam 4K nativo.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def check(path: Path):
    if not path.is_file():
        return ["arquivo MP4 nao encontrado"]
    if shutil.which("ffprobe") is None:
        return ["ffprobe nao instalado"]
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,avg_frame_rate,r_frame_rate,codec_name",
             "-show_entries", "format=format_name,duration",
             "-of", "json", str(path)],
            text=True, capture_output=True, check=True, timeout=60,
        )
        data = json.loads(result.stdout)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError) as exc:
        return [f"ffprobe nao concluiu: {exc}"]
    videos = data.get("streams") or []
    if not videos:
        return ["nenhum stream de video"]
    stream = videos[0]
    errors = []
    if (stream.get("width"), stream.get("height")) != (2160, 3840):
        errors.append("resolucao diferente de 2160x3840 (9:16)")
    rate = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
    try:
        num, den = map(int, rate.split("/"))
        fps = num / den
    except (ValueError, ZeroDivisionError):
        fps = 0.0
    if abs(fps - 60) > 0.02:
        errors.append(f"FPS incompatível: {fps:.3f}; exigido 60")
    if stream.get("codec_name") != "h264":
        errors.append(f"codec inesperado: {stream.get('codec_name')}; exigir h264")
    if not data.get("format", {}).get("duration"):
        errors.append("duracao ausente no MP4")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument(
        "--source-quality-reviewed",
        action="store_true",
        help="Somente depois de verificar visualmente que as fontes e a composicao nao sao simples upscale de baixa resolucao",
    )
    args = parser.parse_args()
    errors = check(args.video)
    if not args.source_quality_reviewed:
        errors.append("origem dos quadros nao atestada: falta --source-quality-reviewed")
    if errors:
        for item in errors:
            print("BLOQUEADO:", item)
        return 1
    print("OK: metadados de piloto 4K60 aceitos; ainda exige QC editorial, upload e confirmacao do link do Drive")
    return 0


if __name__ == "__main__":
    sys.exit(main())

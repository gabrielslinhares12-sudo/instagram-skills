#!/usr/bin/env python3
"""Faker EP01 narration with Gemini 3.8 Flash TTS, confirmed FREE tier only.
Fails before making API calls if dedicated no-billing configuration is absent.
"""
import hashlib
import os
import re
import sys
import wave
from pathlib import Path

VOICE="Rasalgethi"
MODEL="gemini-3.8-flash-tts"
SCRIPT_FILE=Path(__file__).with_name("narracao_faker_v28.txt")
OUT=Path("output/faker-v28-rasalgethi.wav")

def guarded():
    if os.environ.get("TUE_GEMINI_FREE_TIER_ONLY") != "true":
        raise RuntimeError("BLOCKED: TUE_GEMINI_FREE_TIER_ONLY must be true")
    if os.environ.get("TUE_APPROVED_FREE_TIER_TTS") != "true":
        raise RuntimeError("BLOCKED: free-tier explicit approval switch absent")
    key=os.environ.get("GEMINI_FREE_TIER_API_KEY","")
    if not key or len(key)<15:
        raise RuntimeError("BLOCKED: dedicated free-tier key missing")
    if os.environ.get("TUE_ALLOW_BILLABLE_CALLS") == "true":
        raise RuntimeError("BLOCKED: billable mode present")
    return key

def convert_audio(blob,mime_type,dest):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not blob:
        raise RuntimeError("No audio returned")
    if mime_type.startswith("audio/wav") or blob[:4]==b"RIFF":
        dest.write_bytes(blob)
    elif mime_type.startswith("audio/L16") or mime_type.startswith("audio/pcm"):
        m=re.search(r"rate=(\d+)",mime_type)
        sr=int(m.group(1)) if m else 24000
        if len(blob)%2:
            raise RuntimeError("Odd PCM")
        with wave.open(str(dest),"wb") as wf:
            wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes(blob)
    else:
        raise RuntimeError("Unknown audio mime "+repr(mime_type))
    with wave.open(str(dest),"rb") as wf:
        if wf.getnframes()<24000 or wf.getnchannels() not in (1,2):
            raise RuntimeError("Invalid or empty WAV")
        duration=wf.getnframes()/wf.getframerate()
        if not (70<=duration<=180):
            raise RuntimeError("Unexpected duration; manual review "+str(duration))
        print("WAV_QC",duration,wf.getframerate(),wf.getnchannels())
    print("WAV_SHA256",hashlib.sha256(dest.read_bytes()).hexdigest())

def main():
    try:
        key=guarded()
    except RuntimeError as e:
        print(e);return 2
    text=SCRIPT_FILE.read_text(encoding="utf-8").strip()
    if len(text)<500:
        print("BLOCKED: script too short");return 3
    from google import genai
    from google.genai import types
    client=genai.Client(api_key=key)
    print("FREE_TIER_ONLY ONE REQUEST",MODEL,VOICE,hashlib.sha256(text.encode()).hexdigest(),flush=True)
    response=client.models.generate_content(
        model=MODEL,
        contents="Narre em português brasileiro, com voz masculina calma, informativa, ritmo cinematográfico natural. Não acrescente texto. Leia exatamente este roteiro, respeitando as pausas de parágrafo:\n\n"+text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(voice=VOICE)),
        )
    )
    for cand in response.candidates or []:
        for part in cand.content.parts or []:
            inline=getattr(part,"inline_data",None)
            if inline is not None and getattr(inline,"data",None):
                convert_audio(inline.data,getattr(inline,"mime_type","") or "audio/pcm;rate=24000",OUT)
                return 0
    raise RuntimeError("No audio generated")

if __name__=="__main__":
    sys.exit(main())

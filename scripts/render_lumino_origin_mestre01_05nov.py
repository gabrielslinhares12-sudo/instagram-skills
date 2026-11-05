#!/usr/bin/env python3
"""Rebuild Lúmino's six-slide origin story with the *canonical* TUE-MESTRE-01 master.

This is a new review-only version. Never publishes. Never redraws Lúmino.
It uses the exact approved mascot PNG, the signed master JPEG, distinct licensed
photographs and 6 different editorial arrangements with active 6-dot swipe UI.
"""
from __future__ import annotations
import hashlib
import io
import json
import os
from pathlib import Path
import random
import sys
import zipfile

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_tue_mestre_04nov_rework import (
    W, H, S, PAPER, INK, YELLOW, RED, base, brush, mascot, photo, header,
    footer, draw_text, stroke, get_font, load_photo, fitted_photo,
)

OUT = ROOT / 'content/media/instagram/2026-11-05/LUMINO-ORIGEM-MESTRE01-REFEITO'
OUT.mkdir(parents=True, exist_ok=True)
MASTER_SHA = '571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9'
LUMINO_SHA = 'f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b'

PHOTO_URLS = [
 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=1700&q=88',
 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=1700&q=88',
 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=1700&q=88',
 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=1700&q=88',
 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1700&q=88',
 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1700&q=88',
]
PHOTO_FALLBACKS = [
 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=1700&q=87',
 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1700&q=87',
 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1700&q=87',
 'https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1700&q=87',
 'https://images.unsplash.com/photo-1535223289827-42f1e9919769?auto=format&fit=crop&w=1700&q=87',
 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1700&q=87',
]

def check_reference():
    files = [
        (ROOT/'content/brand/lumino-original.png', LUMINO_SHA),
        (ROOT/'content/brand/REFERENCIA-VISUAL-OFICIAL-TUE-MESTRE-01-02NOV2026.jpg', MASTER_SHA),
    ]
    for p, digest in files:
        assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == digest, 'Reference mismatch '+str(p)

def draw_lines(im,lines,x,y,size,dy,color=INK, align='la',maxw=960):
    d = ImageDraw.Draw(im)
    for j,line in enumerate(lines):
        draw_text(d,(x,y+j*dy),line,size,ink=color,font='display',maxw=maxw,anchor=align)
    return im

def panel(im, bounds, rgba=(249,245,237,244),radius=0):
    lay=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(lay)
    x0,y0,x1,y1=[round(z*S) for z in bounds]
    if radius:
        d.rounded_rectangle((x0,y0,x1,y1),radius=radius*S,fill=rgba)
    else:
        d.rectangle((x0,y0,x1,y1),fill=rgba)
    im.paste(lay,(0,0),lay)

def arrow(im,x0,y0,x1,y1):
    d=ImageDraw.Draw(im)
    d.line([(x0*S,y0*S),(x1*S,y1*S)],fill=RED,width=6*S)
    d.polygon([((x1-15)*S,(y1-10)*S),(x1*S,y1*S),((x1-15)*S,(y1+10)*S)],fill=RED)

def photo_stripe(im, pic, x,y,w,h, angle=0):
    photo(im,pic,(x,y,w,h),seed=42,angle=angle)

def cinematic_background(im,pic,text_side='left'):
    """Bright full-bleed photographic composition; mask allows massive mascot foreground."""
    fitted=fitted_photo(pic,1080,1244)
    fitted=ImageEnhance.Color(fitted).enhance(.88)
    fitted=ImageEnhance.Contrast(fitted).enhance(.91)
    im.paste(fitted,(0,0))
    veil=Image.new('RGBA',(W,1244*S),(0,0,0,0))
    v=ImageDraw.Draw(veil)
    v.rectangle((0,0,W,155*S),fill=(250,246,239,254))
    for x in range(0,815*S,20*S):
        alpha=max(0,int(245*(1-x/(815*S))**1.24))
        if text_side=='left':a,b=x,x+20*S
        else:a,b=W-x-20*S,W-x
        v.rectangle((a,155*S,b,1244*S),fill=(248,245,238,alpha))
    im.paste(veil,(0,0),veil)

def small_story(im,lines,xx=67,yy=805,maxw=555):
    panel(im,(xx-12,yy-19,xx+maxw+10,yy+128),(250,247,240,246))
    d=ImageDraw.Draw(im)
    for j,line in enumerate(lines):
        draw_text(d,(xx,yy+j*45),line,28,INK,'bold',maxw=maxw)
    stroke(d,xx,yy+117,xx+maxw-75,yy+117,5)

def headline(im,lines,x,y,width=590,sizes=(91,91,91),dy=106,brush_y=0):
    d=ImageDraw.Draw(im)
    if brush_y:brush(im,(x-15,brush_y,x+width+15,brush_y+118),160+int(y))
    for i,line in enumerate(lines):
        draw_text(d,(x,y+i*dy),line,sizes[min(i,len(sizes)-1)],INK,'display',maxw=width)

def page_1(im,pic):
    cinematic_background(im,pic,'left')
    header(im,'A HISTÓRIA DO LÚMINO','PERSONAGEM')
    headline(im,['QUEM É','O LÚMINO?'],56,189,width=555,sizes=(111,103),dy=126,brush_y=306)
    mascot(im,428,212,790)
    small_story(im,['Antes de qualquer resposta,','existiu uma pergunta.'],62,794,535)
    draw_text(ImageDraw.Draw(im),(65,1005),'E ASSIM NASCEU UMA NOVA LUZ.',28,RED,'bold',maxw=555)

def page_2(im,pic):
    cinematic_background(im,pic,'left')
    header(im,'A PRIMEIRA PERGUNTA','O UNIVERSO')
    headline(im,['UM MUNDO','CHEIO DE','MISTÉRIOS.'],55,185,width=554,sizes=(89,91,89),dy=102,brush_y=362)
    mascot(im,437,228,790)
    small_story(im,['Do céu noturno ao mar,','tudo merecia uma explicação.'],60,803,548)
    draw_text(ImageDraw.Draw(im),(62,1003),'O SEGREDO ERA NÃO PARAR DE PERGUNTAR.',24,RED,'bold',maxw=550)

def page_3(im,pic):
    cinematic_background(im,pic,'right')
    header(im,'UM PERSONAGEM NASCE','A LUZ')
    headline(im,['UMA LUZ','SE ACENDE.'],526,204,width=520,sizes=(95,87),dy=113,brush_y=310)
    mascot(im,-178,239,839)
    panel(im,(512,673,1025,989),(250,247,241,247))
    d=ImageDraw.Draw(im)
    draw_text(d,(536,692),'UMA LANTERNA QUE',37,INK,'display',maxw=450)
    draw_text(d,(536,765),'NÃO ILUMINA SÓ',37,INK,'display',maxw=452)
    draw_text(d,(536,838),'CAMINHOS.',47,RED,'display',maxw=450)
    draw_text(d,(534,914),'ILUMINA IDEIAS.',35,INK,'bold',maxw=460)

def page_4(im,pic):
    cinematic_background(im,pic,'left')
    header(im,'A MISSÃO DE LÚMINO','EXPLORAR')
    headline(im,['DO FUNDO','DO OCEANO...'],49,182,width=588,sizes=(94,85),dy=116,brush_y=297)
    mascot(im,434,242,792)
    small_story(im,['Da natureza às estrelas,','cada pista abre outra história.'],58,822,554)
    draw_text(ImageDraw.Draw(im),(61,1029),'...ATÉ OS LIMITES DO CONHECIMENTO.',24,RED,'bold',maxw=565)

def page_5(im,pic):
    cinematic_background(im,pic,'left')
    header(im,'COMO ELE INVESTIGA','O MÉTODO')
    headline(im,['ELE NÃO','ADIVINHA.'],53,198,width=581,sizes=(96,100),dy=113,brush_y=307)
    mascot(im,432,231,783)
    small_story(im,['Lúmino observa, busca pistas','e confere cada explicação.'],54,777,560)
    draw_text(ImageDraw.Draw(im),(58,1005),'A CURIOSIDADE PRECISA DE EVIDÊNCIAS.',25,RED,'bold',maxw=568)

def page_6(im,pic):
    cinematic_background(im,pic,'left')
    header(im,'A PRÓXIMA AVENTURA','COM VOCÊ')
    headline(im,['AGORA É','COM VOCÊ.'],55,190,width=570,sizes=(104,102),dy=120,brush_y=305)
    mascot(im,427,221,806)
    small_story(im,['Ele não tem todas as respostas.','Quer encontrá-las com você.'],55,793,561)
    panel(im,(40,1040,1033,1174),(26,35,43,246))
    d=ImageDraw.Draw(im)
    draw_text(d,(69,1059),'QUAL MISTÉRIO VAMOS INVESTIGAR?',42,(255,243,206),'display',maxw=931)
    draw_text(d,(73,1127),'CONTE NOS COMENTÁRIOS.',26,(255,211,32),'bold',maxw=901)

def load_verified_photo(index):
    problems=[]
    for url in (PHOTO_URLS[index], PHOTO_FALLBACKS[index]):
        try:
            pic=load_photo(url)
            if pic.width < 600 or pic.height < 400:
                raise ValueError('Low resolution photographic source')
            return pic,url
        except Exception as exc:
            problems.append(str(exc)[:160])
    raise RuntimeError('Could not fetch verified photographic background: '+str(index)+'; '+repr(problems))

def main():
    check_reference()
    records=[]
    sheets=[]
    painter=[page_1,page_2,page_3,page_4,page_5,page_6]
    for i,draw_page in enumerate(painter):
        pic,url=load_verified_photo(i)
        canvas=base(785+i*31)
        draw_page(canvas,pic)
        footer(canvas,i,len(painter),'PERSONAGEM FICTÍCIO · TEM UMA EXPLICAÇÃO')
        final=canvas.resize((1080,1350),Image.Resampling.LANCZOS)
        filename='LUMINO-MESTRE01-'+str(i+1).zfill(2)+'.jpg'
        output=OUT/filename
        final.save(output,'JPEG',quality=96,subsampling=0,optimize=True)
        records.append({'filename':filename,'image_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'width':1080,'height':1350,
            'has_swipe_to_next':i<len(painter)-1,'photo_url':url,'photographic_source_provider':'Unsplash',
            'canonical_mascot':True})
        sheets.append(final.resize((324,405),Image.Resampling.LANCZOS))
        print('RENDERED',filename,output.stat().st_size,'bytes',flush=True)
    mont=Image.new('RGB',(324*3,405*2),(244,238,225))
    for i,p in enumerate(sheets):mont.paste(p,((i%3)*324,(i//3)*405))
    mont.save(OUT/'PREVIA-06-LAMINAS.jpg',quality=88,optimize=True)
    manifest={
      'date':'2026-11-05','preset':'TUE-MESTRE-01','approved_visual_master_sha256':MASTER_SHA,
      'lumino_canonical_png_sha256':LUMINO_SHA,'total_pages':6,'narrative':'Fictional mascot origin story',
      'result':'six_new_individual_review_jpegs','approved':False,
      'visual_reviewed':False,'publication_blocked':True,'manual_original_comparison_required':True,
      'instagram_posted':False,'pages':records,
      'rights':'Unsplash photo sources, original TUE Lúmino source, editorial overlays',
      'qa_notes':'6 individual 1080x1350 JPEGs, six progress dots, last slide no arrow; final artistic approval pending'
    }
    (OUT/'QC-MESTRE01.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    caption='''QUEM É O LÚMINO? 💡🔎

Antes de qualquer resposta, existe uma pergunta. Foi assim que nasceu o Lúmino, nosso detetive da curiosidade.

Sua lanterna se acende diante dos mistérios: ele observa, procura pistas e confere explicações — do fundo dos oceanos até as estrelas.

Lúmino é um personagem fictício do Tem Uma Explicação. Ele não sabe tudo. E essa é a graça: descobrir com você.

Qual mistério vamos investigar primeiro?

#Lumino #TemUmaExplicacao #Curiosidades #Ciencia #Investigacao'''
    (OUT/'LEGENDA-INSTAGRAM.txt').write_text(caption,encoding='utf-8')
    with zipfile.ZipFile(OUT/'LUMINO-ORIGEM-6-LAMINAS-MESTRE01.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for row in records:z.write(OUT/row['filename'],row['filename'])
        z.write(OUT/'LEGENDA-INSTAGRAM.txt','LEGENDA-INSTAGRAM.txt')
        z.write(OUT/'QC-MESTRE01.json','QC-MESTRE01.json')
    print('COMPLETE=6_ORIGINAL_MASCOT_REVIEW_ONLY_NOT_PUBLISHED',flush=True)

if __name__ == '__main__':main()

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
    footer, draw_text, stroke, get_font, load_photo,
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

def page_1(im,pic):
    header(im,'A HISTÓRIA DO LÚMINO','NOSSO PERSONAGEM')
    brush(im,(50,190,1025,395),110)
    draw_lines(im,['ANTES DE UMA','RESPOSTA...'],72,173,95,112)
    photo_stripe(im,pic,50,446,945,608,angle=-1)
    panel(im,(40,956,735,1085),(249,243,232,238))
    draw_lines(im,['EXISTIU UMA','PERGUNTA.'],70,944,53,62)
    mascot(im,592,608,455)
    stroke(ImageDraw.Draw(im),65,1093,540,1093,7)
    draw_text(ImageDraw.Draw(im),(72,1142),'E FOI ASSIM QUE SUA LUZ COMEÇOU.',25,INK,'bold',maxw=935)

def page_2(im,pic):
    header(im,'PRIMEIRA DESCOBERTA','O COMEÇO')
    photo_stripe(im,pic,48,184,612,856,angle=-1)
    panel(im,(447,193,1012,728),(249,243,232,250))
    brush(im,(463,242,1006,335),117)
    draw_lines(im,['O MUNDO','ERA CHEIO','DE MISTÉRIOS.'],487,239,56,76,maxw=494)
    stroke(ImageDraw.Draw(im),489,475,958,475,5)
    draw_text(ImageDraw.Draw(im),(488,515),'DO CÉU NOTURNO',29,RED,'bold',maxw=490)
    draw_text(ImageDraw.Draw(im),(488,568),'À TERRA QUE PISAMOS.',24,INK,'bold',maxw=490)
    mascot(im,596,733,424)
    panel(im,(80,1080,1018,1185),(249,243,232,245))
    draw_text(ImageDraw.Draw(im),(104,1100),'TODA DESCOBERTA COMEÇA COM UM “POR QUÊ?”.',27,INK,'bold',maxw=880)

def page_3(im,pic):
    header(im,'A LUZ DA CURIOSIDADE','O PROPÓSITO')
    brush(im,(54,179,1014,285),122)
    draw_lines(im,['NÃO ERA MAGIA.'],75,174,83,88)
    draw_lines(im,['ERA VONTADE','DE ENTENDER.'],80,280,72,81)
    photo_stripe(im,pic,70,493,941,548,angle=1)
    panel(im,(61,773,540,1036),(249,243,232,243))
    draw_text(ImageDraw.Draw(im),(81,798),'UMA LUZ QUE',45,INK,'display',maxw=440)
    draw_text(ImageDraw.Draw(im),(81,866),'ACENDE A CADA',42,INK,'display',maxw=450)
    draw_text(ImageDraw.Draw(im),(81,934),'NOVA PERGUNTA.',39,RED,'display',maxw=440)
    mascot(im,560,668,483)
    stroke(ImageDraw.Draw(im),83,1083,956,1083,6)
    draw_text(ImageDraw.Draw(im),(83,1120),'NÃO É SOBRE SABER TUDO.',30,INK,'bold',maxw=920)

def page_4(im,pic):
    header(im,'SEM LIMITE PARA EXPLORAR','OS MISTÉRIOS')
    photo_stripe(im,pic,49,170,964,874,angle=0)
    panel(im,(53,189,977,413),(249,243,232,246))
    brush(im,(71,228,935,333),127)
    draw_lines(im,['DO OCEANO...'],88,214,79,87)
    draw_text(ImageDraw.Draw(im),(91,343),'A CURIOSIDADE NÃO CONHECE FRONTEIRAS.',23,RED,'bold',maxw=880)
    mascot(im,592,606,440)
    panel(im,(49,944,994,1112),(249,243,232,245))
    draw_lines(im,['...ATÉ AS ESTRELAS.'],80,948,59,63)
    draw_text(ImageDraw.Draw(im),(79,1036),'CIÊNCIA, NATUREZA E HISTÓRIAS REAIS.',24,RED,'bold',maxw=870)
    stroke(ImageDraw.Draw(im),80,1150,845,1150,5)

def page_5(im,pic):
    header(im,'O MÉTODO DO DETETIVE','AS PISTAS')
    brush(im,(53,178,1014,295),130)
    draw_lines(im,['NÃO BASTA','ADIVINHAR.'],75,170,88,96)
    photo_stripe(im,pic,64,404,577,654,angle=-2)
    panel(im,(470,498,1007,800),(249,243,232,245))
    draw_lines(im,['OBSERVAR.','INVESTIGAR.','CONFERIR.'],498,512,47,83,maxw=496)
    for y in [573,655,738]: stroke(ImageDraw.Draw(im),498,y,914,y,3)
    mascot(im,650,727,365)
    panel(im,(53,1106,1014,1195),(249,243,232,250))
    draw_text(ImageDraw.Draw(im),(79,1120),'AS PISTAS VALEM MAIS QUE OS CHUTES.',28,RED,'bold',maxw=926)

def page_6(im,pic):
    header(im,'A HISTÓRIA CONTINUA','SUA VEZ')
    photo_stripe(im,pic,50,180,962,845,angle=1)
    panel(im,(51,192,1009,485),(249,243,232,245))
    brush(im,(65,255,1000,380),134)
    draw_lines(im,['A PRÓXIMA','PERGUNTA É SUA.'],75,204,73,98)
    mascot(im,534,547,511)
    panel(im,(59,1020,1015,1201),(249,243,232,249))
    draw_text(ImageDraw.Draw(im),(88,1038),'QUAL MISTÉRIO VAMOS INVESTIGAR?',38,INK,'display',maxw=870)
    stroke(ImageDraw.Draw(im),89,1111,992,1111,6)
    draw_text(ImageDraw.Draw(im),(90,1143),'CONTE NOS COMENTÁRIOS.',31,RED,'bold',maxw=840)

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

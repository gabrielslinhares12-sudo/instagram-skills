#!/usr/bin/env python3
"""Reprova fotos originais horizontais/quadradas e qualquer esticamento."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]); assets=json.loads(p.read_text(encoding='utf-8'))['assets']; errors=[]
for a in assets:
    if a.get('type')!='photo':continue
    n=a.get('name','sem nome');w=a.get('original_width');h=a.get('original_height')
    if not isinstance(w,int) or not isinstance(h,int) or w<=0 or h<=0 or w>=h:errors.append(f'{n}: source not verified portrait: {w}x{h}')
    if a.get('fit') in ('fill','stretch','distort') or a.get('scale_x',1)!=a.get('scale_y',1) or a.get('fake_background'):errors.append(f'{n}: distortion/fake fill prohibited')
    if a.get('source_verified') is not True:errors.append(f'{n}: original metadata not verified')
    if isinstance(w,int) and isinstance(h,int) and (w<2160 or h<3840):print(f'WARN {n}: {w}x{h} < 4K native')
for e in errors:print('FAIL',e)
print('PASS' if not errors else 'FAIL',len(assets),'assets')
sys.exit(bool(errors))

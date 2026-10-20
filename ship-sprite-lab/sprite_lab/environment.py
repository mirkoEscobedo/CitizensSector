import importlib.metadata, os, platform, shutil, sys
from pathlib import Path
from PIL import Image
from .core import *

def doctor():
    cfg=load_json(ROOT/'experiment.json')
    blender=cfg.get('blender_executable') or shutil.which('blender')
    probes=['C:/Program Files/Blender Foundation','E:/Programs/Blender Foundation']
    for root in probes:
        if not blender and Path(root).exists():
            found=list(Path(root).glob('Blender*/blender.exe'))
            if found: blender=str(found[-1])
    game=Path(os.environ.get('STARSECTOR_HOME',cfg['game_install']))
    models=[str(p.relative_to(ROOT)) for ext in ('*.blend','*.obj','*.fbx','*.glb','*.gltf') for p in REFS.rglob(ext)]
    data={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),
          'versions':{n:importlib.metadata.version(n) for n in ('Pillow','numpy')},
          'dependency_mode':'scoped venv, system-site-packages from read-only bundled runtime; pip bootstrap not required',
          'blender':blender,'blender_probes':probes,'render_engines':'UNKNOWN; no executable discovered' if not blender else 'requires engine probe',
          'source_models':models,'editable_friend_source':False,'game_install':str(game),
          'game_available':(game/'starsector-core/data/hulls/eagle.ship').exists(),
          'image_generation':{'provider':'built-in image_gen tool available in agent session; not a local Python API','model':'NOT RETURNED','seed':'NOT EXPOSED','cost':'UNKNOWN','supports_mask_or_strength':'NOT EXPOSED'},
          'interactive_game_capture':'NOT AVAILABLE in this tool session; native computer APIs disabled',
          'probe_scope':'PATH, configured path, common Program Files/E Programs locations; not an exhaustive disk scan',
          'arm_availability':{'M0':'AVAILABLE','M1':'AVAILABLE','M2':'BLOCKED: no supplied genuine mesh',
                              'M3':'BLOCKED: Blender executable and bpy unavailable' if not blender else 'AVAILABLE',
                              'M4':'AVAILABLE via agent tool; cached result adapter','M5':'AVAILABLE'}}
    save_json(OUT/'capabilities.json',data)
    if data['game_available']: ingest_game(game)
    return data

def ingest_game(game):
    folder=ROOT/'reference-private'; folder.mkdir(exist_ok=True)
    records=[]; panels=[]
    for name in ('eagle','apogee','doom'):
        hullpath=game/f'starsector-core/data/hulls/{name}.ship'
        hull=load_json(hullpath); src=game/'starsector-core'/hull['spriteName']
        target=folder/f'{name}.png'; shutil.copyfile(src,target)
        shutil.copyfile(hullpath,folder/f'{name}.ship')
        im=Image.open(src).convert('RGBA')
        records.append({'id':name,'source':str(src),'sha256':sha(src),'hull_data_sha256':sha(hullpath),
                        'texture_dimensions':list(im.size),'draw_dimensions':[hull['width'],hull['height']],
                        'alpha_bbox':im.getchannel('A').getbbox(),'center':hull['center'],
                        'rights':'installed game asset; private comparison only, excluded from distributable export'})
        # Keep exact native pixels; no enlargement.
        panels.append(panel(im,label=f'{name} {im.width}x{im.height}'))
    sheet=Image.new('RGB',(sum(p.width for p in panels)+32,max(p.height for p in panels)),(14,17,25)); x=0
    for p in panels: sheet.paste(p,(x,0)); x+=p.width+10
    sheet.save(OUT/'native-cohort.png'); save_json(OUT/'native-reference-inventory.json',records)

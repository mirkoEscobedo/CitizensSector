import csv, io, re, shutil, zipfile
from .core import *
from .anatomy import point

def convex_hull(points):
    pts=sorted(set(points))
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]; hi=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0: hi.pop()
        hi.append(p)
    return lo[:-1]+hi[:-1]

def build_manifest(candidate='A04'):
    geom=load_json(ASSETS/'geometry.json'); sources=load_json(OUT/'inventory.json')
    im=Image.open(OUT/f'{candidate}.png')
    data={'ship':'Idris','interpretation':'gray render supplied by user; assembled full ship',
        'sources':sources,'canonical':{**load_json(ASSETS/'baseline-transform.json'),'bow':'UP','mirrored':False,
            'aspect_ratio':333/640,'mask':'assets/idris/canonical-mask.png','openings':geom['openings'],
            'margin':16,'color_space':'sRGB straight RGBA; resize in linear premultiplied space'},
        'source_registrations':load_json(ASSETS/'source-registrations.json'),
        'geometry':'assets/idris/geometry.json','landmarks':geom['landmarks'],'component_counts':geom['component_counts'],
        'materials':'presets/faction.json','chosen_candidate':candidate,'candidate_sha256':sha(OUT/f'{candidate}.png'),
        'export':{'texture_dimensions':list(im.size),'hull_bbox_dimensions':[333,640],
            'draw_dimensions_development_only':list(im.size),'verified_game_scale':False,'center_from_bottom_left':[182.5,336],
            'canonical_to_game':'forwardX = drawHeight - centerBottomY - imageY; leftY = centerX - imageX (1 draw unit / pixel, provisional)',
            'source_to_game':'source -> clockwise rotation -> crop -> half-pixel-aware resize -> 16px margin -> above transform',
            'weapon_policy':'all existing weapon pixels retained as static art; weaponSlots empty to avoid double drawing; functional mounts deferred',
            'collision_policy':'convex enclosure of alpha>=128, intentionally covers holes; placeholder requiring combat review',
            'engine_annotations':'four inferred exits, uncertainty ±2 final pixels; no baked exhaust',
            'load_test':'NOT RUN: no available native interactive capture/control; installation inspected read-only'},
        'uncertainties':['manual semantic regions, not approved CAD geometry','inferred mount/engine locations',
            'no editable friend source','no genuine Idris mesh','no second distinct Star Citizen input','no developer art ratings'],
        'seed':431,'tool_versions':load_json(OUT/'capabilities.json')['versions']}
    save_json(ASSETS/'manifest.json',data); return data

def export(candidate='A04'):
    if candidate not in ('A01','A04','A07'):
        raise ValueError('Only reviewed source-geometry-preserving A01/A04/A07 may enter this development scaffold.')
    manifest=build_manifest(candidate); cfg=load_json(ROOT/'experiment.json'); game=Path(cfg['game_install'])
    folder=OUT/'export/idris_lab'
    for sub in ('graphics/ships','data/hulls','data/variants','data/missions/idris_lab'):
        (folder/sub).mkdir(parents=True,exist_ok=True)
    shutil.copyfile(OUT/f'{candidate}.png',folder/'graphics/ships/idris_lab.png')
    im=Image.open(OUT/f'{candidate}.png'); center=[182.5,336]
    def to_game(p): return [round(672-center[1]-p[1],3),round(center[0]-p[0],3)]
    mask=np.asarray(im)[...,3]>=128
    pts=[]
    for y in range(0,672,3):
        xs=np.where(mask[y])[0]
        if len(xs): pts.extend([(int(xs[0]),y),(int(xs[-1]),y)])
    bounds=[n for p in convex_hull(pts) for n in to_game(p)]
    geo=load_json(ASSETS/'geometry.json')
    hull={'hullId':'idris_lab','hullName':'Idris LAB','hullSize':'CAPITAL_SHIP','style':'MIDLINE',
          'spriteName':'graphics/ships/idris_lab.png','width':365,'height':672,'center':center,
          'collisionRadius':340,'bounds':bounds,'shieldCenter':[0,0],'shieldRadius':340,'viewOffset':0,
          'weaponSlots':[],'engineSlots':[{'angle':180,'contrailSize':32,'length':48,
              'width':9 if l['id'].startswith('small') else 15,'location':to_game(l['canonical']),'style':'MIDLINE'}
              for l in geo['landmarks'] if l['type']=='engine']}
    save_json(folder/'data/hulls/idris_lab.ship',hull)
    # Real installed CSV headers and baseline row, no invented schema.
    csvpath=game/'starsector-core/data/hulls/ship_data.csv'
    if csvpath.exists():
        with csvpath.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f); headers=reader.fieldnames; row=next(r for r in reader if r['id']=='eagle')
        row.update({'id':'idris_lab','name':'Idris LAB','designation':'Private art test','tech/manufacturer':'LAB',
                    'system id':'','shield type':'NONE','defense id':'','codex variant id':'idris_lab_unarmed',
                    'tags':'hide_in_codex','hints':'','logistics n/a reason':'Development only'})
        with (folder/'data/hulls/ship_data.csv').open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=headers); writer.writeheader(); writer.writerow(row)
    variant={'variantId':'idris_lab_unarmed','hullId':'idris_lab','displayName':'Art inspection (unarmed)',
             'goalVariant':False,'fluxCapacitors':0,'fluxVents':0,'hullMods':[],'permaMods':[],'sMods':[],'weaponGroups':[]}
    save_json(folder/'data/variants/idris_lab_unarmed.variant',variant)
    save_json(folder/'mod_info.json',{'id':'idris_lab','name':'Idris Sprite Lab - private development test',
        'author':'Local experiment','version':'0.1.0','gameVersion':'0.98a','description':'UNVALIDATED art smoke test; assembled decorative weapon art, no functional weapon mounts.'})
    save_json(folder/'data/missions/idris_lab/descriptor.json',{'title':'Idris LAB art inspection','difficulty':'EASY',
        'icon':'graphics/ships/idris_lab.png','background':'graphics/backgrounds/background4.jpg'})
    (folder/'data/missions/mission_list.csv').write_text('mission,\nidris_lab,\n',encoding='utf-8')
    (folder/'data/missions/idris_lab/MissionDefinition.java').write_text('''package data.missions.idris_lab;
import com.fs.starfarer.api.fleet.FleetGoal;
import com.fs.starfarer.api.fleet.FleetMemberType;
import com.fs.starfarer.api.mission.FleetSide;
import com.fs.starfarer.api.mission.MissionDefinitionAPI;
import com.fs.starfarer.api.mission.MissionDefinitionPlugin;
public class MissionDefinition implements MissionDefinitionPlugin {
  public void defineMission(MissionDefinitionAPI api) {
    api.initFleet(FleetSide.PLAYER, "LAB", FleetGoal.ATTACK, false);
    api.initFleet(FleetSide.ENEMY, "REF", FleetGoal.ATTACK, true);
    api.setFleetTagline(FleetSide.PLAYER, "Unarmed assembled-art inspection");
    api.setFleetTagline(FleetSide.ENEMY, "Native scale and effects reference");
    api.addToFleet(FleetSide.PLAYER, "idris_lab_unarmed", FleetMemberType.SHIP, "Idris LAB", true);
    api.addToFleet(FleetSide.PLAYER, "eagle_Assault", FleetMemberType.SHIP, "Reference Eagle", false);
    api.addToFleet(FleetSide.ENEMY, "lasher_Standard", FleetMemberType.SHIP, "Effects reference", true);
    api.addBriefingItem("Rotate and zoom: inspect bow, four engines, negative spaces and baked static turrets.");
    api.initMap(-6000f, 6000f, -6000f, 6000f);
  }
}
''',encoding='utf-8')
    save_json(OUT/'export/enabled_mods.json',{'enabledMods':['idris_lab']})
    save_json(OUT/'export/export-status.json',{'status':'SCAFFOLD; actual game load NOT RUN','schema_evidence':
        [{'path':str(game/f'starsector-core/{p}'),'sha256':sha(game/f'starsector-core/{p}')} for p in
         ['data/hulls/eagle.ship','data/hulls/apogee.ship','data/hulls/ship_data.csv','data/missions/afistfulofcredits/MissionDefinition.java','starsector_minimal.bat']],
        'version_evidence':'com/fs/starfarer/Version.class in installed starfarer_obf.jar contains 0.98a-RC8 and RC8p strings',
        'coordinate_evidence':'native-coordinate-evidence.png projects Eagle engine and weapon positions using bottom-left .ship center and forward-X / left-Y mount frame',
        'production_compatibility':False,'functional_weapon_alignment':'NOT RUN; weaponSlots intentionally empty, pivot suggestions in overlay/manifest only'})
    debug_overlay(im,geo,to_game)
    native_coordinate_evidence()
    return folder

def debug_overlay(im,geo,to_game):
    bg=Image.new('RGBA',im.size,(27,31,39,255)); bg.alpha_composite(im)
    draw=ImageDraw.Draw(bg)
    for i,l in enumerate(geo['landmarks']):
        x,y=l['canonical']; color=(255,200,60) if l['type']=='engine' else (50,230,220)
        draw.line((x-5,y,x+5,y),fill=color,width=1); draw.line((x,y-5,x,y+5),fill=color,width=1)
        draw.text((x+5,y-8),str(i),fill=color,font=font(12))
    bg.save(OUT/'debug-overlay.png')
    save_json(OUT/'debug-overlay-key.json',[{'index':i,**l,'game_forward_left':to_game(l['canonical'])} for i,l in enumerate(geo['landmarks'])])

def native_coordinate_evidence():
    hull=load_json(ROOT/'reference-private/eagle.ship'); im=Image.open(ROOT/'reference-private/eagle.png').convert('RGBA')
    bg=Image.new('RGBA',im.size,(25,29,35,255)); bg.alpha_composite(im); draw=ImageDraw.Draw(bg)
    cx,cy=hull['center']; H=hull['height']
    for e in hull['engineSlots']:
        f,l=e['location']; x,y=cx-l,H-cy-f
        draw.ellipse((x-2,y-2,x+2,y+2),outline=(255,150,50),width=1)
    for e in hull['weaponSlots']:
        f,l=e['locations']; x,y=cx-l,H-cy-f
        draw.line((x-3,y,x+3,y),fill=(50,240,220)); draw.line((x,y-3,x,y+3),fill=(50,240,220))
    bg.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(OUT/'native-coordinate-evidence.png')

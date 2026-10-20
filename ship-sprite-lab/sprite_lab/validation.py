from PIL import ImageFilter
from .core import *
from .anatomy import point,inverse

METHODS={'A01':'M0 gray untreated','A02':'M0 flat independent interpretation','A03':'M0 friend finished native sprite (enlarged here)',
         'A04':'M0 masked material finish','A05':'M1 semantic 2D reconstruction','A06':'M4 fresh generated edit',
         'A07':'M5 deterministic hybrid of M0 finish + selective edges',
         'A08':'supplied prior generated study 1','A09':'supplied prior generated study 2'}

def aligned(im,width):
    result=Image.new('RGBA',(width,672)); result.paste(im,((width-im.width)//2,0)); return result

def manual_generated_landmarks():
    # Measured visually on the returned ORIGINAL 924x1702 PNG; uncertain ±6 raw px.
    # Never inferred from matching the reference mask or accepted as exact mounts.
    return {'bow':[462,26],'forward_weapon_pivot':[462,186], 'center_deck':[463,674],
        'rear_ring':[465,1440],'small_engine_left':[202,769],'small_engine_right':[727,770],
        'large_engine_left':[56,1384],'large_engine_right':[873,1384],
        'aft_weapon_left':[395,1538],'aft_weapon_right':[532,1538],
        'aft_outer_weapon_left':[184,974],'aft_outer_weapon_right':[741,974]}

def projected_generated_landmarks():
    raw=Image.open(OUT/'raw/M4-attempt-01.png'); box=raw.getchannel('A').getbbox()
    result=Image.open(OUT/'A06.png'); sx=(result.width-32)/(box[2]-box[0]); sy=640/(box[3]-box[1])
    return {k:[16+(p[0]-box[0]+.5)*sx-.5,16+(p[1]-box[1]+.5)*sy-.5] for k,p in manual_generated_landmarks().items()}

def validate():
    cfg=load_json(ROOT/'experiment.json'); geo=load_json(ASSETS/'geometry.json')
    reference=Image.open(OUT/'A01.png').convert('RGBA')
    results=[]
    generated_points=projected_generated_landmarks() if (OUT/'A06.png').exists() else {}
    for cid,method in METHODS.items():
        path=OUT/f'{cid}.png'
        if not path.exists(): continue
        im=Image.open(path).convert('RGBA'); alpha=np.asarray(im)[...,3]
        width=max(reference.width,im.width)
        ref=np.asarray(aligned(reference,width))[...,3]>=128
        cand=np.asarray(aligned(im,width))[...,3]>=128
        overlap=float((ref&cand).sum()/max(1,(ref|cand).sum()))
        box=im.getchannel('A').getbbox(); margins=[box[0],box[1],im.width-box[2],im.height-box[3]]
        interior=np.asarray(Image.fromarray((alpha>=128).astype('uint8')*255).filter(ImageFilter.MinFilter(7)))>0
        opaque=float((alpha[interior]>=254).mean()) if interior.any() else 0
        opening=[]
        for hole in geo['openings']:
            x,y=hole['canonical']; x+=(im.width-reference.width)/2
            a=int(alpha[round(y),round(x)]) if 0<=x<im.width and 0<=y<im.height else 255
            opening.append({'id':hole['name'],'alpha':a,'pass':a<=cfg['thresholds']['opening_alpha_max']})
        errors=[]
        for landmark in geo['landmarks']:
            key=landmark['id']
            if cid in ('A01','A04','A07'):
                measured=landmark['canonical']; evidence='same source pixels; no warp, not independent manual detection'
            elif cid=='A05' and landmark['type'] in ('circle','weapon'):
                measured=landmark['canonical']; evidence='authored location, inferred annotation; does not verify full component shape'
            elif cid=='A06' and key in generated_points:
                measured=generated_points[key].copy(); measured[0]-=(im.width-reference.width)/2
                evidence='manual returned-image observation ±6 raw px (~2.3 final px)'
            else: continue
            err=float(np.linalg.norm(np.array(measured)-landmark['canonical']))
            errors.append({'id':key,'final_pixel_deviation':err,'evidence':evidence})
        if cid in ('A01','A04','A07'): component='PASS: source RGB geometry retained (four pods, ring, deck, framing)'
        elif cid=='A05': component='FAIL: four pod shapes and ring authored, medium machinery incomplete, center deck over-simplified'
        elif cid=='A06': component='FAIL: four pods retained as count, but larger/thicker pods, altered aft supports, deck/vent/mount geometry'
        else: component='FAIL: independent interpretation; source geometry not established'
        gates={'rgba':Image.open(path).mode=='RGBA','hull_long_edge_640':box[3]-box[1] in range(638,643),
               'margins':min(margins)>=14,'aspect_ratio':abs((im.width-32)/333-1)<=.015,
               'silhouette':overlap>=cfg['thresholds']['mask_iou_min'],'opaque_interior':opaque>=.98,
               'openings':all(o['pass'] for o in opening),'orientation':'PASS: visually bow UP; no automated bow detector',
               'landmarks':bool(errors) and max(e['final_pixel_deviation'] for e in errors)<=3,
               'components':component.startswith('PASS')}
        structural=all(v for v in gates.values() if isinstance(v,bool))
        result={'id':cid,'method':method,'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'dimensions':list(im.size),
            'hull_alpha_bbox':box,'margins':margins,'alpha_range':[int(alpha.min()),int(alpha.max())],
            'interior_fraction_alpha_ge_254':opaque,'silhouette_iou_before_any_forced_mask':overlap,
            'source_mask_policy':'M1 starts from canonical alpha, so IoU is construction-controlled, not reconstruction evidence' if cid=='A05' else 'no post-generation source alpha forced',
            'openings':opening,'landmarks':errors,'component_review':component,'gates':gates,'structural_pass':structural,
            'game_load_test':'NOT RUN','production_ready':False}
        results.append(result)
        edge_overlay(reference,im,OUT/f'diagnostics/{cid}-edge-overlay.png')
    save_json(OUT/'validation.json',{'thresholds':cfg['thresholds'],'ratings_are_not_gates':True,'results':results})
    return results

def edge_overlay(ref,im,path):
    width=max(ref.width,im.width); a=np.asarray(aligned(ref,width).getchannel('A'))>=128; b=np.asarray(aligned(im,width).getchannel('A'))>=128
    out=np.zeros((672,width,3),dtype='uint8')+18
    out[a&b]=[100,111,126]; out[a&~b]=[230,50,80]; out[b&~a]=[20,220,220]
    path.parent.mkdir(parents=True,exist_ok=True); Image.fromarray(out).save(path)

def software_tests():
    """Existing math/image/data gates, runnable without generated art or game data."""
    # Reversibility, handedness, real small opening, compositing edge colors.
    points=[(2,533),(510,776),(510,290),(170,533),(1710,54)]
    roundtrip=max(float(np.linalg.norm(np.array(inverse(point(p)))-p)) for p in points)
    assert roundtrip<1e-8,roundtrip
    assert point((510,776))[0] < point((510,290))[0]
    mask=Image.open(ASSETS/'canonical-mask.png')
    for o in load_json(ASSETS/'geometry.json')['openings']:
        assert mask.getpixel(tuple(round(x) for x in o['canonical']))<=8,o
    # Saturated red foreground touching fully transparent green should never
    # acquire a green fringe when reduced. Check composites on black and white.
    a=np.zeros((8,8,4),dtype='uint8'); a[:,:,:3]=[0,255,0]; a[:,0:4]=[255,0,0,255]
    reduced=resize_rgba(Image.fromarray(a),(3,3))
    aa=np.asarray(reduced); assert int(aa[aa[...,3]>0,1].max())<=1
    for color in ((0,0,0,255),(255,255,255,255)):
        comp=np.asarray(Image.alpha_composite(Image.new('RGBA',reduced.size,color),reduced))
        assert np.all(comp[...,1]==comp[...,2])
    # Preserving a tiny known opening under a scale change is a real failure mode.
    hole=np.ones((32,32,4),dtype='uint8')*255; hole[12:20,12:20]=0
    resized=resize_rgba(Image.fromarray(hole),(16,16)); assert resized.getpixel((8,8))[3]==0
    manifest=load_json(ASSETS/'manifest.json')
    for key in ('sources','canonical','landmarks','export','materials','geometry'):
        assert key in manifest,key
    center=manifest['export']['center_from_bottom_left']
    for p in [point(p) for p in points]:
        game=[672-center[1]-p[1],center[0]-p[0]]
        back=[center[0]-game[1],672-center[1]-game[0]]
        assert np.linalg.norm(np.array(p)-back)<1e-8
    result={'passed':7,'checks':['source/canonical transform round trips','bow and left/right handedness','four observed transparent sample openings',
        'linear premultiplied edge behavior on black/white','small synthetic opening resize','required manifest fields','canonical/game transform round trip'],
        'largest_source_roundtrip_error_px':roundtrip,'scope':'software and data checks, no in-game execution'}
    return result


def meaningful_tests():
    result=software_tests()
    export=load_json(OUT/'export/idris_lab/data/hulls/idris_lab.ship')
    assert export['weaponSlots']==[],'Baked turrets must not be duplicated'
    result['checks'][5]='required manifest fields and no doubled turrets'
    save_json(OUT/'tests.json',result); return result

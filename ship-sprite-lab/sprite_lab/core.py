from pathlib import Path
import hashlib, json, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'idris'
ASSETS = ROOT / 'assets' / 'idris'
REFS = ROOT / 'docs' / 'references'
LONG, MARGIN = 640, 16

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')

def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def linear(x):
    return np.where(x <= .04045, x / 12.92, ((x + .055) / 1.055) ** 2.4)

def srgb(x):
    x = np.maximum(x, 0)
    return np.where(x <= .0031308, x * 12.92, 1.055 * x ** (1/2.4) - .055)

def resize_rgba(im, size, filt=Image.Resampling.BICUBIC):
    """Filter each premultiplied linear channel once; export straight sRGB RGBA."""
    a = np.asarray(im.convert('RGBA'), dtype=np.float32) / 255
    alpha = a[..., 3]
    premul = linear(a[..., :3]) * alpha[..., None]
    def channel(x):
        return np.asarray(Image.fromarray(x.astype(np.float32)).resize(size, filt))
    aa = np.clip(channel(alpha), 0, 1)
    pp = np.stack([channel(premul[..., i]) for i in range(3)], axis=-1)
    rgb = np.clip(srgb(np.divide(pp, aa[..., None], out=np.zeros_like(pp), where=aa[..., None] > 1e-6)), 0, 1)
    result = np.dstack([rgb, aa])
    result[aa < .5/255] = 0
    return Image.fromarray(np.round(result * 255).astype('uint8'))

def normalize(im, direction='up', long=LONG, margin=MARGIN):
    im = im.convert('RGBA')
    if direction == 'left': im = im.transpose(Image.Transpose.ROTATE_270)
    if direction == 'right': im = im.transpose(Image.Transpose.ROTATE_90)
    box = im.getchannel('A').getbbox()
    if box is None: raise ValueError('Source contains no visible pixels')
    hull = im.crop(box)
    size = (round(hull.width * long / hull.height), long)
    hull = resize_rgba(hull, size)
    out = Image.new('RGBA', (size[0]+2*margin, size[1]+2*margin))
    out.paste(hull, (margin, margin))
    return out, box

def font(size=16):
    try: return ImageFont.truetype('C:/Windows/Fonts/consola.ttf', size)
    except OSError: return ImageFont.load_default()

def panel(im, bg=(14,17,25), label='', size=None):
    if size: im = resize_rgba(im, size)
    p = Image.new('RGB', (im.width, im.height+32), bg)
    p.paste(im, (0,32), im)
    ImageDraw.Draw(p).text((6,6), label, font=font(15), fill=(230,232,236))
    return p

def inventory():
    roles = {'starcitizen_og_model':'geometry authority; supplied render PNG, not a mesh',
             'fanmadepixelart':'independent flat interpretation, optional color guide',
             'bychatgpt':'prior generated study, unknown prompt/provider; not a new lab run',
             'mfz_idris':'friend standalone finished sprite; independent interpretation, editable source absent',
             'handmadeidrisvs':'flattened screenshot style reference; native sprite resolutions unknown'}
    rows=[]
    for p in sorted(REFS.rglob('*.png')):
        im=Image.open(p); a=np.asarray(im.convert('RGBA'))[...,3]
        rows.append({'path':p.relative_to(ROOT).as_posix(), 'sha256':sha(p),'dimensions':list(im.size),
                     'mode':im.mode,'embedded_icc_profile':bool(im.info.get('icc_profile')),
                     'source_color_interpretation':'assumed sRGB for this experiment; source rendering/view transform unknown',
                     'alpha_range':[int(a.min()),int(a.max())],
                     'alpha_partial_pixels':int(((a>0)&(a<255)).sum()),'alpha_bbox':im.convert('RGBA').getchannel('A').getbbox(),
                     'role':next((v for k,v in roles.items() if k in str(p)), 'unassigned'),
                     'provenance':'user supplied; author/redistribution grant not independently verified; private lab only'})
    save_json(OUT/'inventory.json',rows)
    return rows

def baseline():
    OUT.mkdir(parents=True,exist_ok=True); ASSETS.mkdir(parents=True,exist_ok=True)
    rows=inventory()
    src=next(REFS.glob('starcitizen_og_model/*.png'))
    im,box=normalize(Image.open(src),'left')
    im.save(OUT/'A01.png'); im.getchannel('A').save(ASSETS/'canonical-mask.png')
    flat=next(REFS.glob('fanmadepixelart/*.png'))
    normalize(Image.open(flat),'right')[0].save(OUT/'A02.png')
    friend=REFS/'mfz_idris_hand_made_by_bro.png'
    normalize(Image.open(friend),'up')[0].save(OUT/'A03.png')
    panels=[panel(Image.open(OUT/f'A0{i}.png'),label=f'A0{i} | 640 hull px') for i in (1,2,3)]
    sheet=Image.new('RGB',(sum(p.width for p in panels),max(p.height for p in panels)),(14,17,25))
    x=0
    for p in panels: sheet.paste(p,(x,0)); x+=p.width
    sheet.save(OUT/'baseline-contact.png')
    save_json(ASSETS/'baseline-transform.json', {'source':src.relative_to(ROOT).as_posix(),'source_sha256':sha(src),
        'source_dimensions':list(Image.open(src).size),'rotation':'clockwise 90 degrees, no reflection',
        'rotated_crop_bbox':box,'output_dimensions':list(im.size),'hull_dimensions':[im.width-32,640],
        'source_to_rotated_pixel_center':[['x_rot','1065-y'],['y_rot','x']],
        'rotated_to_canonical_pixel_center':'((p-crop_min+0.5)*scale)-0.5+16; scale=(rounded_width/crop_width,640/crop_height)',
        'interpretation':'complete assembled ship, existing turrets retained; not hull-only'})
    registrations=[]
    for row in rows:
        p=ROOT/row['path']; source=Image.open(p).convert('RGBA'); w,h=source.size
        if 'handmadeidrisvs' in p.name:
            registrations.append({'source':row['path'],'role':'comparison-only flattened lineup; not registered as ship geometry','transform':None}); continue
        direction='left' if 'starcitizen_og_model' in str(p) else 'right' if 'fanmadepixelart' in str(p) else 'up'
        if direction=='left':
            rot=np.array([[0,-1,h-1],[1,0,0],[0,0,1]],float); turned=source.transpose(Image.Transpose.ROTATE_270)
        elif direction=='right':
            rot=np.array([[0,1,0],[-1,0,w-1],[0,0,1]],float); turned=source.transpose(Image.Transpose.ROTATE_90)
        else: rot=np.eye(3); turned=source
        bb=turned.getchannel('A').getbbox(); hh=bb[3]-bb[1]; ww=bb[2]-bb[0]
        ow=round(ww*640/hh); sx,sy=ow/ww,640/hh
        fit=np.array([[sx,0,16-.5+sx*(.5-bb[0])],[0,sy,16-.5+sy*(.5-bb[1])],[0,0,1]],float)
        registration=np.eye(3); registration[0,2]=(365-(ow+32))/2
        registrations.append({'source':row['path'],'source_sha256':row['sha256'],'bow_original':direction,'mirrored':False,
            'rotated_alpha_crop':bb,'own_output_dimensions':[ow+32,672],'source_to_own_output_affine_pixel_centers':(fit@rot).tolist(),
            'source_to_centered_canonical_frame_affine':(registration@fit@rot).tolist(),
            'registration_scope':'long-edge/center registration only; independent designs are not warped into geometric agreement' if direction!='left' else 'authoritative frame',
            'uncertainty':'prior generated alpha bounds include unwanted background; own normalization is diagnostic only' if 'bychatgpt' in str(p) else 'manual interpretation; no geometric averaging'})
    save_json(ASSETS/'source-registrations.json',registrations)
    return rows

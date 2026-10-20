import html
from PIL import ImageOps
from .core import *
from .validation import METHODS

def tiles(images,columns=3,gap=12,bg=(20,23,30)):
    cellw=max(i.width for i in images); cellh=max(i.height for i in images)
    sheet=Image.new('RGB',(columns*cellw+(columns-1)*gap,((len(images)+columns-1)//columns)*(cellh+gap)-gap),bg)
    for idx,im in enumerate(images): sheet.paste(im,((idx%columns)*(cellw+gap),(idx//columns)*(cellh+gap)))
    return sheet

def checker(size):
    yy,xx=np.mgrid[:size[1],:size[0]]; v=np.where((xx//12+yy//12)%2,155,115).astype('uint8')
    return Image.fromarray(np.stack([v]*3,axis=-1))

def background_panel(im,color,label):
    bg=checker(im.size) if color=='checker' else Image.new('RGB',im.size,color)
    bg.paste(im,(0,0),im)
    result=Image.new('RGB',(im.width,im.height+32),(20,23,30)); result.paste(bg,(0,32))
    ImageDraw.Draw(result).text((5,6),label,font=font(14),fill='white'); return result

def hull_fit(im,long=200):
    return normalize(im,long=long,margin=8)[0]

def compare():
    folder=OUT/'diagnostics'; folder.mkdir(exist_ok=True)
    results=load_json(OUT/'validation.json')['results']
    previews=[]; review_panels=[]
    # Private native originals are not enlarged in style sheets.
    cohort=[Image.open(ROOT/f'reference-private/{n}.png').convert('RGBA') for n in ('eagle','apogee','doom')]
    cohort_panels=[panel(hull_fit(im),label=n) for n,im in zip(('Eagle','Apogee','Doom'),cohort)]
    style_cohort=tiles(cohort_panels,3)
    style_cohort.save(OUT/'style-cohort-200.png')
    for r in results:
        cid=r['id']; im=Image.open(OUT/f'{cid}.png').convert('RGBA')
        previews.append(panel(hull_fit(im),label=f'{cid} 200px'))
        for factor in (1,.5,.25):
            size=tuple(round(s*factor) for s in im.size)
            img=im if factor==1 else resize_rgba(im,size)
            img.save(folder/f'{cid}-{int(factor*100)}percent.png')
        gray=ImageOps.grayscale(im).convert('RGBA'); gray.putalpha(im.getchannel('A')); gray.save(folder/f'{cid}-gray.png')
        silhouette=Image.new('RGBA',im.size,'white'); silhouette.putalpha(im.getchannel('A')); silhouette.save(folder/f'{cid}-silhouette.png')
        im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(folder/f'{cid}-nearest-2x.png')
        # Fixed-size useful pixel inspection crop; at intended location, no source warp.
        x=im.width//2
        crop=im.crop((x-62,380,x+62,530)).resize((372,450),Image.Resampling.NEAREST)
        panel(crop,label=f'{cid} | aft crop, 3x nearest').save(folder/f'{cid}-pixel-crop.png')
        backgrounds=[background_panel(im,c,f'{cid} | {label}') for c,label in
                     [((10,13,22),'dark'),((128,128,128),'gray'),((238,238,233),'light'),('checker','checker')]]
        tiles(backgrounds,4).save(folder/f'{cid}-backgrounds.png')
        native=panel(im,label=f'{cid} | {im.width}x{im.height}, 640 hull')
        # Actual 640 candidate next to unscaled native references. This is NOT
        # a game-scale comparison; equal-hull style comparison is separate below.
        right=Image.open(OUT/'native-cohort.png')
        sheet=Image.new('RGB',(native.width+right.width+12,max(native.height,right.height)),(14,17,25))
        sheet.paste(native,(0,0)); sheet.paste(right,(native.width+12,0)); sheet.save(folder/f'{cid}-native-with-cohort.png')
    tiles(previews,5).save(OUT/'contact-200.png')
    for percentage in (50,25):
        imgs=[panel(Image.open(folder/f'{r["id"]}-{percentage}percent.png'),label=f'{r["id"]} {percentage}%') for r in results]
        tiles(imgs,5).save(OUT/f'contact-{percentage}percent.png')
    # Match native friend asset to 640-candidate reduced to SAME 262px hull,
    # while showing exact original file separately in the HTML.
    pair=[panel(hull_fit(Image.open(OUT/'A04.png'),262),label='A04 262px'),
          panel(hull_fit(Image.open(REFS/'mfz_idris_hand_made_by_bro.png'),262),label='friend 262px')]
    tiles(pair,2).save(OUT/'friend-native-comparison.png')
    resolution=[]
    for scale in (1,2,4):
        for filt in ('bicubic','lanczos'):
            path=OUT/f'resolution/M1-{scale}x-{filt}.png'
            if path.exists():
                im=Image.open(path).crop((140,205,225,340)).resize((255,405),Image.Resampling.NEAREST)
                resolution.append(panel(im,label=f'M1 {scale}x {filt}, 640 hull'))
    if resolution: tiles(resolution,3).save(OUT/'resolution-contact.png')
    m0=[]
    for filt in ('area','bicubic','lanczos'):
        path=OUT/f'resolution/M0-source-{filt}.png'
        if path.exists():
            crop=Image.open(path).crop((120,215,245,365)).resize((375,450),Image.Resampling.NEAREST)
            m0.append(panel(crop,label=f'M0 source -> {filt}, 3x crop'))
    if m0: tiles(m0,3).save(OUT/'filter-contact.png')
    write_html(results)

def write_html(results):
    body=['''<!doctype html><html lang="en"><meta charset="utf-8"><title>Idris ship sprite lab</title>
<style>body{background:#11151c;color:#e2e7ef;font:16px/1.5 system-ui;margin:28px}a{color:#8fcaff}h1,h2,h3{line-height:1.2}button{padding:9px}img{max-width:none;object-fit:contain;vertical-align:top}figure{margin:12px 0;overflow:auto}section{border-top:1px solid #485160;padding:18px 0}.row{display:flex;gap:20px;overflow:auto}.box{padding:15px;background:#202733}.small{font-size:14px}table{border-collapse:collapse}td,th{border:1px solid #485160;padding:6px}details{margin:12px 0}summary{cursor:pointer}code{color:#e9c48b}</style>
<h1>Idris: controlled ship-art experiment</h1><p>20 October 2026. Private lab; provisional agent visual review. No developer ratings and no in-game launch.</p>
<p class="box"><strong>Recommendation:</strong> A04, masked material finish of the supplied gray render, for this image-only input. Geometry retained; bounded semantic annotation required. A06 is a useful style study and fails structural/alpha acceptance. Fleet generalization is UNTESTED.</p>
<p><a href="review.md">Full evidence and recommendation</a> · <a href="validation.json">Technical gates</a> · <a href="effort.json">Effort / missing capabilities</a> · <a href="../../README.md">Run instructions</a></p>
<p>All candidates: 640px hull long edge, separate 16px margins, bow up. Native cohort images retain native pixels. These are style/display comparisons, not verified relative game scale.</p>
<button onclick="physical=!physical;calibrate()">Toggle CSS / physical pixel mapping</button> <span id="scale"></span>
<p class="small">For 1 image pixel per device pixel use physical mode, browser zoom 100%, and an unscaled image viewer. Physical mode divides CSS width by devicePixelRatio. Browser/OS capture pipelines may rescale: exact linked PNGs are authoritative. Large sheets scroll horizontally.</p>
<h2>Equal hull style comparison: 200 pixels</h2><figure><img src="contact-200.png" data-native><figcaption>Neutral candidate IDs; full method key is below. Source images are preserved.</figcaption></figure><figure><img src="style-cohort-200.png" data-native><figcaption>Native Eagle, Apogee, Doom reduced only; no screenshot blur judged as native art.</figcaption></figure>
<h2>Small display tests</h2><figure><img src="contact-50percent.png" data-native><figcaption>50% output display; not a verified game zoom.</figcaption></figure><figure><img src="contact-25percent.png" data-native><figcaption>25% output display; not a verified game zoom.</figcaption></figure>
<h2>Friend's native finished asset</h2><figure><img src="../../docs/references/mfz_idris_hand_made_by_bro.png" data-native><img src="friend-native-comparison.png" data-native><figcaption>Left: original 175x280 file. Right: A04 reduced to the friend's 262px native hull. A03's 640px enlargement is for geometry diagnostics only.</figcaption></figure>''']
    for r in results:
        cid=r['id']; status='PASS' if r['structural_pass'] else 'FAIL'
        body.append(f'<section><h2>{cid}</h2><p>Structural gate: {status}; alpha-mask IoU {r["silhouette_iou_before_any_forced_mask"]:.3f}. Game load NOT RUN.</p>')
        body.append(f'<figure><a href="{cid}.png"><img src="diagnostics/{cid}-native-with-cohort.png" data-native></a><figcaption>{cid}: exact output beside native cohort. Sizes are labeled; native refs are smaller.</figcaption></figure>')
        body.append(f'<details><summary>Four backgrounds at native output size</summary><figure><img src="diagnostics/{cid}-backgrounds.png" data-native></figure></details>')
        body.append(f'<details><summary>Grayscale, silhouette, source edge overlay and nearest-neighbor pixel diagnosis</summary><figure class="row"><img src="diagnostics/{cid}-gray.png" data-native><img src="diagnostics/{cid}-silhouette.png" data-native><img src="diagnostics/{cid}-edge-overlay.png" data-native><img src="diagnostics/{cid}-pixel-crop.png" data-native></figure><p>Edge overlay: red = missing reference area, cyan = extra candidate area, gray = overlap.</p><a href="diagnostics/{cid}-nearest-2x.png">Entire image at 2x nearest-neighbor</a></details></section>')
    body.append('<h2>Resolution and filtering</h2><figure><img src="resolution-contact.png" data-native></figure><figure><img src="filter-contact.png" data-native></figure><p>M1 source is genuinely rendered at 1x/2x/4x with fixed feature sizes. M0 is a filter comparison of the fixed supplied raster, not higher resolution rendering. Generated resolution is uncontrolled.</p>')
    body.append('<h2>Coordinate evidence</h2><figure><img src="debug-overlay.png" data-native><img src="native-coordinate-evidence.png" data-native></figure><p>Left: inferred Idris points; see <a href="debug-overlay-key.json">numbered key</a>. Right: installed Eagle data projected back onto its sprite; orange engines, cyan mount pivots, enlarged 3x nearest for inspection.</p>')
    body.append('<h2>Method key (after neutral visual review)</h2><table><tr><th>ID</th><th>Method</th></tr>')
    body.extend(f'<tr><td>{k}</td><td>{html.escape(v)}</td></tr>' for k,v in METHODS.items())
    body.append('''</table><script>let physical=true;function calibrate(){let d=window.devicePixelRatio||1;document.querySelectorAll('img[data-native]').forEach(im=>{let apply=()=>{im.style.width=(im.naturalWidth/(physical?d:1))+'px';im.style.height='auto'};if(im.complete)apply();else im.onload=apply});document.getElementById('scale').textContent='devicePixelRatio='+d+'; '+(physical?'physical-pixel mode':'CSS-pixel mode')}window.addEventListener('resize',calibrate);calibrate();</script></html>''')
    (OUT/'report.html').write_text('\n'.join(body),encoding='utf-8')

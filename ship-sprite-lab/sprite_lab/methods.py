import datetime, shutil
from PIL import ImageChops, ImageFilter
from .core import *
from .anatomy import point, region_mask, write_definition

def tinted(im, geometry, preset):
    arr=np.asarray(im.convert('RGBA')).astype(np.float32)/255
    luminance=arr[...,:3]@np.array([.2126,.7152,.0722])
    # Retain observed lighting; these values do not claim to recover normals.
    base=np.stack([luminance]*3,axis=-1)
    out=base.copy()
    for reg in geometry['regions']:
        mask=region_mask(reg).filter(ImageFilter.GaussianBlur(.55))
        m=np.asarray(mask).astype(np.float32)/255
        color=np.array(preset[reg['material']])/255
        value=np.clip(luminance*.85+.03,.025,.90)
        painted=np.clip(value[...,None]*(color/.60),0,1)
        out=out*(1-m[...,None])+painted*m[...,None]
    # Unannotated exposed structure stays neutral and somewhat darker.
    result=np.dstack([np.clip(out,0,1),arr[...,3]])
    return Image.fromarray(np.round(result*255).astype('uint8'))

def plane_render(geometry,preset,scale=1):
    """New semantic plane reconstruction, source alpha only, no gray RGB reused."""
    size=(365*scale,672*scale)
    alpha=Image.open(ASSETS/'canonical-mask.png')
    if scale!=1: alpha=alpha.resize(size,Image.Resampling.BICUBIC)
    h,w=size[1],size[0]
    yy,xx=np.mgrid[:h,:w]
    # A single canonical lighting field, including geometrically paired parts.
    grad=.90+.16*(1-xx/w)+.05*(1-yy/h)
    out=np.ones((h,w,3),np.float32)*np.array(preset['machinery'])/255*grad[...,None]*.75
    svg=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="365" height="672" viewBox="0 0 365 672">',
         '<defs><mask id="hull"><image href="canonical-mask.png" width="365" height="672"/></mask><linearGradient id="plane" x2="1" y2="1"><stop stop-color="#d8e0e4"/><stop offset="1" stop-color="#535f6b"/></linearGradient></defs>',
         '<g mask="url(#hull)"><rect width="365" height="672" fill="#303740"/>']
    for reg in geometry['regions']:
        mask=region_mask(reg,scale); m=np.asarray(mask).astype(np.float32)/255
        color=np.array(preset[reg['material']])/255
        # Local face gradient and layer-height-derived contact shadow. Height is
        # a semantic annotation, never inferred from the input's brightness.
        bbox=mask.getbbox()
        local=np.clip((xx-bbox[0])/max(1,bbox[2]-bbox[0]),0,1)
        face=.80+.35*(1-local)+.06*(1-yy/h)
        shadow=Image.new('L',size)
        shift=round(reg['height_semantic']*1.3*scale)
        shadow.paste(mask,(shift,shift))
        shade_mask=np.asarray(shadow.filter(ImageFilter.GaussianBlur(.8*scale))).astype(np.float32)/255
        out*=1-.22*shade_mask[...,None]
        # Narrow directional bevel: shifting uses explicit zero padding, not wraparound.
        r=max(1,round(preset['bevel_final_px']*scale))
        shifted=Image.new('L',size); shifted.paste(mask,(r,r))
        lower=Image.new('L',size); lower.paste(mask,(-r,-r))
        hi=np.maximum(m-np.asarray(shifted)/255,0)
        lo=np.maximum(m-np.asarray(lower)/255,0)
        shade=np.clip(color[None,None,:]*face[...,None]+hi[...,None]*.17-lo[...,None]*.17,0,1)
        out=out*(1-m[...,None])+shade*m[...,None]
        coords=' '.join(f'{point(p)[0]:.2f},{point(p)[1]:.2f}' for p in reg['polygon_source'])
        rgb='#'+''.join(f'{int(v):02x}' for v in preset[reg['material']])
        svg.append(f'<polygon id="{reg["name"]}" points="{coords}" fill="{rgb}" stroke="#9ca8b2" stroke-width="0.6"/>')
    image=Image.fromarray(np.round(np.clip(out,0,1)*255).astype('uint8')).convert('RGBA')
    draw=ImageDraw.Draw(image)
    for c in geometry['circles']:
        x,y=point(c['source_center'],scale); r=c['source_radius']*640/2047*scale
        for factor,col in ((1,(55,65,76)),(.90,(160,172,176)),(.78,(78,91,103)),(.64,(122,133,141))):
            rr=r*factor; draw.ellipse((x-rr,y-rr,x+rr,y+rr),fill=col,width=max(1,scale))
        svg.append(f'<circle cx="{x/scale}" cy="{y/scale}" r="{r/scale}" fill="#687984" stroke="#b6c0c6" stroke-width="1.2"/>')
    # Reusable service louvres, aligned within known center deck, sized in final px.
    for side in (-1,1):
        for cy in (267,275,283,291):
            cx=182+side*13
            draw.line([(int((cx-4)*scale),int(cy*scale)),(int((cx+4)*scale),int(cy*scale))],fill=(40,47,54),width=2*scale)
    for landmark in geometry['landmarks']:
        if landmark['type']!='weapon': continue
        cx,cy=point(landmark['source'],scale); r=4.2*scale
        draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(44,50,56),outline=(153,159,159),width=scale)
        draw.rectangle((cx-1.5*scale,cy-8*scale,cx+1.5*scale,cy),fill=(83,94,102))
    image.putalpha(alpha)
    pixels=np.array(image); pixels[pixels[...,3]==0,:3]=0
    image=Image.fromarray(pixels)
    svg.append('</g></svg>')
    (ASSETS/'planes.svg').write_text('\n'.join(svg),encoding='utf-8')
    return image

def hybrid(base,geometry,preset):
    """Non-generative hybrid: retained render relief plus localized value hierarchy."""
    arr=np.asarray(base).astype(np.float32)/255
    out=arr[...,:3].copy()
    # Focused darker machinery and narrow selected plate edges. No global sharpening.
    for reg in geometry['regions']:
        mask=region_mask(reg)
        m=np.asarray(mask).astype(np.float32)/255
        if reg['material']=='machinery': out*=1-.18*m[...,None]
        if reg['name'] in ('forward_shoulder','forward_shoulder_opposite','main_deck','aft_outer_frame','aft_outer_frame_opposite'):
            shifted=Image.new('L',base.size); shifted.paste(mask,(1,1))
            edge=np.clip(m-np.asarray(shifted)/255,0,1)
            out+=edge[...,None]*.055
    # Luminance compression avoids blown armor, keeps existing source topology.
    result=np.dstack([np.clip(out,0,1),arr[...,3]])
    return Image.fromarray(np.round(result*255).astype('uint8'))

def run_methods():
    start=time.perf_counter()
    baseline(); geometry=write_definition(); preset=load_json(ROOT/'presets/faction.json')
    base=Image.open(OUT/'A01.png').convert('RGBA')
    events=[]
    def timed(method,fn,path):
        t=time.perf_counter(); im=fn(); im.save(path)
        events.append({'method':method,'operation':'render/process/export','elapsed_seconds':time.perf_counter()-t,'path':path.relative_to(ROOT).as_posix()})
        return im
    finished=timed('M0',lambda:tinted(base,geometry,preset),OUT/'A04.png')
    timed('M1',lambda:plane_render(geometry,preset),OUT/'A05.png')
    timed('M5',lambda:hybrid(finished,geometry,preset),OUT/'A07.png')
    raw=OUT/'raw/M4-attempt-01.png'
    if raw.exists():
        timed('M4',lambda:normalize(Image.open(raw))[0],OUT/'A06.png')
        save_json(OUT/'M4-record.json',{'provider':'built-in image_gen','model':'NOT RETURNED','cost':'UNKNOWN','seed':'NOT EXPOSED',
            'prompt_path':'assets/idris/generation-prompt.txt','prompt_sha256':sha(ASSETS/'generation-prompt.txt'),
            'references':[{ 'path':str(p.relative_to(ROOT)), 'sha256':sha(p)} for p in [OUT/'A01.png',OUT/'raw/M4-input-native-cohort.png',REFS/'mfz_idris_hand_made_by_bro.png'] if p.exists()],
            'input_hash_caveat':'Native cohort sheet was relabeled after generation, then its original input layout was reconstructed from unchanged native pixels. Hash recorded post hoc; exact at-call byte hash not captured. Source A01 and friend unchanged.',
            'attempts':1,'provider_latency_seconds':34.175,'requested_resolution':'640px hull reference; no tool resolution argument available',
            'returned_resolution':list(Image.open(raw).size),'transparent_background':True,'mask_control':False,'edit_strength_control':False,
            'raw':str(raw.relative_to(ROOT)),'raw_sha256':sha(raw),'normalization':'crop alpha bbox, uniform long-edge fit, no mirroring, no source-mask correction',
            'repeatability':'cached output is reproducible downstream; provider re-generation not seed deterministic'})
    # Prior studies are never counted as runs performed by this lab.
    for idx,p in enumerate(sorted((REFS/'bychatgpt').glob('*.png')),8):
        normalize(Image.open(p))[0].save(OUT/f'A{idx:02}.png')
    times={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-start,'events':events}
    history_path=OUT/'render-history.json'
    history=load_json(history_path) if history_path.exists() else []
    previous=OUT/'render-times.json'
    if not history and previous.exists(): history.append(load_json(previous))
    history.append(times)
    save_json(history_path,history); save_json(previous,times)
    return events

def resolution_experiment():
    geometry=load_json(ASSETS/'geometry.json'); preset=load_json(ROOT/'presets/faction.json')
    folder=OUT/'resolution'; folder.mkdir(exist_ok=True)
    records=[]
    for scale in (1,2,4):
        t=time.perf_counter(); raw=plane_render(geometry,preset,scale)
        raw.save(folder/f'M1-{scale}x-source.png')
        for name,filt in [('bicubic',Image.Resampling.BICUBIC),('lanczos',Image.Resampling.LANCZOS)]:
            final=resize_rgba(raw,(365,672),filt) if scale!=1 else raw
            final.save(folder/f'M1-{scale}x-{name}.png')
        records.append({'method':'M1','source_scale':scale,'elapsed_seconds':time.perf_counter()-t,'geometry_fixed':True,
                        'alpha_note':'raster canonical mask enlarged at 2x/4x; silhouette supersampling is confounded by limited native mask',
                        'feature_sizes':'all bevels and louvres expressed in final pixels'})
    # Existing PNG: resolution trials are resampling, NEVER a higher-resolution render.
    src=Image.open(next(REFS.glob('starcitizen_og_model/*.png')))
    for name,filt in [('area',Image.Resampling.BOX),('bicubic',Image.Resampling.BICUBIC),('lanczos',Image.Resampling.LANCZOS)]:
        rotated=src.convert('RGBA').transpose(Image.Transpose.ROTATE_270)
        hull=resize_rgba(rotated,(333,640),filt)
        im=Image.new('RGBA',(365,672)); im.paste(hull,(16,16)); im.save(folder/f'M0-source-{name}.png')
    save_json(folder/'experiment.json',{'records':records,'M0':'fixed existing raster; resampling filter test only; no native 4x source available',
        'M4':'one returned 924x1702 image; no independent resolution study and no upscale labeled as re-render'})

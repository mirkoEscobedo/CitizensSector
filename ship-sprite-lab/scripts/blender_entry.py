"""UNEXECUTED Blender adapter, not an M2/M3 result or a validated rig.

Blender --background --python scripts/blender_entry.py -- --doctor
M3: --mode M3 --geometry assets/idris/geometry.json --out outputs/idris/M3
M2: --mode M2 --mesh supplied.glb --out outputs/idris/M2
M2 axes must be prepared explicitly: +Y bow, +Z top, XY plane; no automatic
axis guessing. M3 uses annotated semantic plate heights, no grayscale depth.
Requires Blender's bpy; test against installed-version documentation before use.
"""
import argparse, json, math, sys
from pathlib import Path

def main():
    try: import bpy
    except ImportError: raise SystemExit('BLOCKED: bpy unavailable. Supply a Blender executable; run this script inside Blender.')
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser(); p.add_argument('--doctor',action='store_true'); p.add_argument('--mode',choices=['M2','M3'])
    p.add_argument('--mesh'); p.add_argument('--geometry'); p.add_argument('--out',default='outputs/idris/blender')
    opts=p.parse_args(args)
    engines=[x.identifier for x in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    if opts.doctor:
        print(json.dumps({'version':bpy.app.version_string,'engines':engines})); return
    if not opts.mode: p.error('--mode or --doctor required')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if opts.mode=='M2':
        if not opts.mesh or not Path(opts.mesh).is_file(): p.error('M2 requires a genuine supplied mesh, never a substitute')
        ext=Path(opts.mesh).suffix.lower()
        if ext in ('.glb','.gltf'): bpy.ops.import_scene.gltf(filepath=str(Path(opts.mesh).resolve()))
        elif ext=='.obj': bpy.ops.wm.obj_import(filepath=str(Path(opts.mesh).resolve()))
        elif ext=='.fbx': bpy.ops.import_scene.fbx(filepath=str(Path(opts.mesh).resolve()))
        else: p.error('Adapter supports glTF/OBJ/FBX only; inspect and prepare other assets manually')
    else:
        if not opts.geometry: p.error('M3 requires semantic geometry annotations')
        data=json.loads(Path(opts.geometry).read_text(encoding='utf-8'))
        # Approximate plate model only: genuine silhouette/opening reconstruction
        # and repeated components still require verification after this first run.
        for reg in data['regions']:
            xyz=[]
            for x,y in reg['polygon_source']:
                u=16+(1065-y+.5)*333/1066-.5; v=16+(x+.5)*640/2047-.5
                xyz.append((u-182.5,336-v,reg['height_semantic']*3))
            mesh=bpy.data.meshes.new(reg['name']); mesh.from_pydata(xyz,[],[list(range(len(xyz)))]); mesh.update()
            obj=bpy.data.objects.new(reg['name'],mesh); bpy.context.collection.objects.link(obj)
            solid=obj.modifiers.new('shallow plate','SOLIDIFY'); solid.thickness=2
            bevel=obj.modifiers.new('selected plate bevel','BEVEL'); bevel.width=1.2; bevel.segments=2
            colors={'paint':(.32,.40,.50,1),'pale':(.60,.59,.53,1),'machinery':(.08,.10,.12,1),'framing':(.35,.40,.43,1)}
            mat=bpy.data.materials.new(reg['material']); mat.diffuse_color=colors[reg['material']]; obj.data.materials.append(mat)
    scene=bpy.context.scene
    meshes=[o for o in scene.objects if o.type=='MESH']
    if not meshes: raise RuntimeError('No mesh objects imported or authored')
    from mathutils import Vector
    coords=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    xmin,xmax=min(v.x for v in coords),max(v.x for v in coords); ymin,ymax=min(v.y for v in coords),max(v.y for v in coords)
    height=ymax-ymin; width=xmax-xmin; scale=height/640
    camera_data=bpy.data.cameras.new('sprite orthographic'); camera=bpy.data.objects.new('sprite orthographic',camera_data)
    scene.collection.objects.link(camera); camera.location=((xmin+xmax)/2,(ymin+ymax)/2,max(v.z for v in coords)+height*2)
    camera.rotation_euler=(0,0,0); camera_data.type='ORTHO'; camera_data.ortho_scale=height+32*scale; scene.camera=camera
    scene.render.engine='CYCLES'; scene.cycles.samples=32
    for name,loc,power,size in [('key',(-height,height,height*1.5),height*height*8,height*.7),('fill',(height,0,height),height*height*.8,height)]:
        data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size
        light=bpy.data.objects.new(name,data); scene.collection.objects.link(light); light.location=loc
        direction=Vector(((xmin+xmax)/2,(ymin+ymax)/2,0))-light.location; light.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
    scene.render.resolution_y=672; scene.render.resolution_x=round(width/scale)+32; scene.render.resolution_percentage=100
    scene.render.film_transparent=True; scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='Standard'; scene.view_settings.exposure=0; scene.view_settings.gamma=1
    layer=scene.view_layers[0]; layer.use_pass_z=True; layer.use_pass_normal=True
    scene.render.use_file_extension=True; scene.render.use_compositing=False
    folder=Path(opts.out).resolve(); folder.mkdir(parents=True,exist_ok=True)
    scene.render.filepath=str(folder/'beauty.png'); bpy.ops.wm.save_as_mainfile(filepath=str(folder/'scene.blend'))
    bpy.ops.render.render(write_still=True)
    # Multi-layer EXR preserves actual enabled passes, not invented AO support.
    scene.render.image_settings.file_format='OPEN_EXR_MULTILAYER'; bpy.data.images['Render Result'].save_render(str(folder/'passes.exr'),scene=scene)
    (folder/'rig.json').write_text(json.dumps({'version':bpy.app.version_string,'engine':scene.render.engine,'passes':['Combined','Depth','Normal'],
        'AO':'NOT REQUESTED; inspect actual engine support','material_masks':'NOT IMPLEMENTED in first adapter',
        'status':'first adapter output requires inspection; M3 incomplete geometry possible','view':'Standard; alternative look not tested'},indent=2))

if __name__=='__main__': main()

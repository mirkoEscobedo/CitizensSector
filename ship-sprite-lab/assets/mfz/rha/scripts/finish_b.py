import json, numpy as np
from PIL import Image, ImageDraw
SP=r'<STAGING_DIR>'
im=Image.open(SP+r'\raR_4302.png').convert("RGBA"); W,H=im.size
a=np.array(im).astype(float)
# ---- hangar dimming (left panel + mirror)
reg=np.zeros(a.shape[:2],bool)
for x0,x1 in ((36,60),(W-60,W-36)): reg[56:110,x0:x1]=True
r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
mx=a[...,:3].max(2); mn=a[...,:3].min(2); sat=(mx-mn)/np.maximum(mx,1)
lum=0.299*r+0.587*g+0.114*b
panel=reg&(al>0)&(r>=g)&(g>=b)&(sat>0.25)&(lum<190)
corner=np.zeros(a.shape[:2],bool)
for x0,x1 in ((43,52),(W-52,W-43)): corner[98:110,x0:x1]=True
panel=panel|(corner&(al>0)&(sat>0.5)&(lum>100))
print("panel px",int(panel.sum()))
SAT,GAIN=0.70,0.66
for c in range(3):
    v=(lum+(a[...,c]-lum)*SAT)*GAIN
    a[...,c]=np.where(panel,np.clip(v,0,255),a[...,c])
dimmed=Image.fromarray(a.astype(np.uint8),"RGBA"); dimmed.save(SP+r'\raB_dim.png')
# ---- vanilla sockets
G='<STARSECTOR_HOME>/starsector-core/graphics/ships/'
src=Image.open(G+'hammerhead/hammerhead_base.png').convert('RGBA')
def disc(cx,cy,r):
    R=int(r+1); cr=src.crop((cx-R,cy-R,cx+R+1,cy+R+1))
    m=Image.new('L',cr.size,0); ImageDraw.Draw(m).ellipse((R-r,R-r,R+r,R+r),fill=255); cr.putalpha(m); return cr
small=disc(38,37,6).resize((10,10),Image.LANCZOS)
# (type, left top-left x0, y0); mirrored partner at W-x0-10; 'c' = centreline
pairs=[('BALLISTIC',15,95),('MISSILE',31,175)]
centre=[]
out=dimmed.copy(); alpha=dimmed.getchannel('A'); slots=[]
def put(t,x0,y0):
    out.alpha_composite(small,(x0,y0)); slots.append(dict(type=t,size='SMALL',x=x0+5,y=y0+5))
for t,x0,y0 in pairs: put(t,x0,y0); put(t,W-x0-10,y0)
for t,x0,y0 in centre: put(t,x0,y0)
out.putalpha(alpha); out.save(SP+r'\raB_armed.png')
json.dump(slots,open(SP+r'\raB_armed_slots.json','w'),indent=1); print(out.size,len(slots))

import json, math, numpy as np
from PIL import Image
im=Image.open(r'<MOD_DIR>\graphics\ships\mfz_rha.png').convert('RGBA'); W,H=im.size
al=np.array(im)[...,3]>128
cx,cy=W/2,H/2   # 68,123
def loc(px,py): return [round(cy-py,1), round(cx-px,1)]   # [forward, left]
# ---- bounds: outer silhouette per row, shrunk 2px inside
rows=[]
for y in range(0,H,1):
    xs=np.where(al[y])[0]
    if len(xs): rows.append((y,xs.min()+2,xs.max()-2))
def rdp(pts,eps):
    if len(pts)<3: return pts
    a,b=np.array(pts[0]),np.array(pts[-1]); d=b-a; n=np.hypot(*d)
    dist=[abs(d[0]*(p[1]-a[1])-d[1]*(p[0]-a[0]))/n if n else np.hypot(*(np.array(p)-a)) for p in pts]
    i=int(np.argmax(dist))
    if dist[i]>eps: return rdp(pts[:i+1],eps)[:-1]+rdp(pts[i:],eps)
    return [pts[0],pts[-1]]
right=[(r,y) for y,l,r in rows]            # top->bottom along right edge (px right = negative y)
left=[(l,y) for y,l,r in rows][::-1]       # bottom->top along left edge
outline=rdp(right,2.2)+rdp(left,2.2)
bounds=[]
for px,py in outline: bounds+=loc(px,py)
rad=max(math.hypot(bounds[i],bounds[i+1]) for i in range(0,len(bounds),2))
print("bounds pts",len(bounds)//2,"max r",round(rad,1))
bay=lambda i,px,py:dict(angle=0,arc=360,id=f"WS{i:04d}",locations=loc(px,py),mount="HIDDEN",size="LARGE",type="LAUNCH_BAY")
turret=lambda i,px,py,t,ang,arc:dict(angle=ang,arc=arc,id=f"WS{i:04d}",locations=loc(px,py),mount="TURRET",size="SMALL",type=t)
slots=[
 turret(1,20,100,"ENERGY",0,250),   # left wing shoulder
 turret(2,116,100,"ENERGY",0,250),  # right wing shoulder
 turret(3,36,180,"MISSILE",0,200),  # left stern pod
 turret(4,100,180,"MISSILE",0,200), # right stern pod
 bay(5,48,85),                       # left hangar
 bay(6,88,85),                       # right hangar
]
def eng(px,py,w,l,c): return dict(angle=180,contrailSize=c,length=l,location=loc(px,py),style="CUSTOM",styleId="MFZ_GOLD",width=w)
engines=[eng(38,197,10,40,10),eng(98,197,10,40,10),eng(50,203,9,32,9),eng(86,203,9,32,9)]
ship=dict(hullName="Rha",hullId="mfz_rha",hullSize="DESTROYER",spriteName="graphics/ships/mfz_rha.png",style="MFZ_RHA",
 height=H,width=W,center=[cx,cy],collisionRadius=round(rad,1),shieldCenter=[0,0],shieldRadius=125,viewOffset=0,
 weaponSlots=slots,engineSlots=engines,bounds=bounds)
# pretty print with compact number lists
out=json.dumps(ship,indent=2)
import re
out=re.sub(r'\[\s+([-\d\.,\s]+?)\s+\]',lambda m:'['+re.sub(r'\s+',' ',m.group(1))+']',out)
open(r'<MOD_DIR>\data\hulls\mfz_rha.ship','w').write(out+"\n")
print(len(out))

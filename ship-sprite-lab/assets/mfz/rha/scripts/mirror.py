import sys
from PIL import Image, ImageChops
import numpy as np
src,out=sys.argv[1:3]
im=Image.open(src).convert("RGB"); a=np.array(im)
m=a.max(2)>14
xs=np.where(m.any(0))[0]; ys=np.where(m.any(1))[0]
cx=(xs.min()+xs.max())/2; print("bbox",xs.min(),xs.max(),ys.min(),ys.max(),"cx",cx,"canvas",im.size)
# crop symmetric about cx, mirror left half
half=int(round(min(cx-xs.min(), xs.max()-cx)))+2
c=int(round(cx))
left=im.crop((c-half,0,c,im.height))
canvas=Image.new("RGB",im.size,(0,0,0))
W=im.width
canvas.paste(left,(W//2-half,0))
canvas.paste(left.transpose(Image.FLIP_LEFT_RIGHT),(W//2,0))
canvas.save(out)

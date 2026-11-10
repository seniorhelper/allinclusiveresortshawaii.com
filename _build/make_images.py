# Generates original site graphics (no stock): og.jpg, logo.png, favicon.svg
from PIL import Image, ImageDraw, ImageFont
import os
R=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'assets')
W,H=1200,630
img=Image.new('RGB',(W,H))
d=ImageDraw.Draw(img)
top=(5,59,82); bot=(8,118,133)
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
d.ellipse([930,70,1110,250],fill=(242,165,65))
import math
pts=[(x,520+18*math.sin(x/70)) for x in range(0,W+10,10)]+[(W,H),(0,H)]
d.polygon(pts,fill=(253,248,240))
F='C:/Windows/Fonts/'
big=ImageFont.truetype(F+'georgiab.ttf',74); sm=ImageFont.truetype(F+'segoeui.ttf',36)
d.text((70,150),"All-inclusive",font=big,fill='white')
d.text((70,240),"resorts in Hawaii?",font=big,fill='white')
d.text((72,350),"The honest guide: what exists, what it costs,",font=sm,fill=(225,245,247))
d.text((72,398),"and how to get the same easy feeling.",font=sm,fill=(225,245,247))
d.text((72,555),"allinclusiveresortshawaii.com",font=sm,fill=(5,59,82))
img.save(os.path.join(R,'og.jpg'),quality=82,optimize=True,progressive=True)
# logo 512
L=Image.new('RGBA',(512,512),(0,0,0,0)); g=ImageDraw.Draw(L)
g.ellipse([8,8,504,504],fill=(8,131,149)); g.ellipse([290,110,440,260],fill=(242,165,65))
g.polygon([(x,330+30*math.sin(x/45)) for x in range(20,500,6)]+[(470,430),(256,504),(42,430)],fill=(253,248,240))
L.save(os.path.join(R,'logo.png'),optimize=True)
open(os.path.join(R,'favicon.svg'),'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#088395"/><circle cx="27" cy="14" r="6" fill="#f2a541"/><path d="M3 25c5-4 9-4 14 0s9 4 14 0 6-3 6-3v8a19 19 0 0 1-34 0z" fill="#fdf8f0"/></svg>')

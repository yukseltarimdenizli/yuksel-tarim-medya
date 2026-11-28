import sys, json, pathlib
sys.path.insert(0,'/home/claude/yuksel-tarim-medya/motor')
import dayi_video as dv, arka
from toprak_sahneler import hap
from cizim import FPS
from PIL import Image
im=Image.open('/tmp/three/traktor3d.png'); bb=im.getchannel('A').getbbox(); im.crop(bb).save('/tmp/three/traktor_crop.png')
N={"agirlik":[939.3,551.7],"arkateker":[319.0,396.4]}
W=860; s=W/(bb[2]-bb[0]); H=round((bb[3]-bb[1])*s); X=90; Y=1268-H
P=lambda k:((N[k][0]-bb[0])*s+X,(N[k][1]-bb[1])*s+Y)
def ok(hx,hy,k):
    x,y=P(k); return (f'<line x1="{hx}" y1="{hy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#14281A" stroke-width="9" stroke-linecap="round"/>'
                      f'<line x1="{hx}" y1="{hy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#FFD54F" stroke-width="4" stroke-linecap="round"/>'
                      f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="#FFD54F" stroke="#14281A" stroke-width="4"/>')
def s_tr3d(p):
    g=arka.manzara()
    g+=f'<image href="file:///tmp/three/traktor_crop.png" x="{X}" y="{Y}" width="{W}" height="{H}"/>'
    g+=ok(260,600,"arkateker")+ok(690,1215,"agirlik")
    g+=hap(260,600,"Lastik basıncı 🔧","#14281A","#FFD54F",38)+hap(690,1215,"Ön ağırlık (balast)","#14281A","#FFD54F",36)
    g+="<!--UST-->"+dv.baslik("PATİNAJ!","#c62828","#fff",360)+dv.pip(925,460,110)
    return g,(540,960,1.0,1.0)
dv.SAHNELER["tr3d"]=s_tr3d
dv.JS_EK+="\nObject.assign(SAHNE,{tr3d(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); }});\n"
m="Traktör patinaj yapıyorsa iki şeye bak: ağırlık ve lastik basıncı."
w=m.split(); kt=[round(0.2+i*0.33,2) for i in range(len(w))]
sen={"bant":"DAYI SORUYOR","parcalar":[{"sahne":"tr3d","konusan":"usta","metin":m,"sure":4.2,"kelime_t":kt,"konusma":[[0.2,kt[-1]+0.4]]}]}
dv.ses_zarfi(sen,'/tmp/three/sessiz.wav')
pathlib.Path('/tmp/three/tv.html').write_text(dv.html(sen))
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--allow-file-access-from-files']); pg=b.new_page(viewport={'width':1080,'height':1920}); e=[]
    pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('file:///tmp/three/tv.html'); pg.wait_for_timeout(600)
    pg.evaluate(f'window.renderFrame({int((kt[8]+0.1)*FPS)})'); pg.wait_for_timeout(300)
    pg.screenshot(path='/tmp/three/traktor_sahne.png'); b.close(); print('hata',e[:3])

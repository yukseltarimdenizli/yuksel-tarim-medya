import sys, json, pathlib
sys.path.insert(0,'/home/claude/yuksel-tarim-medya/motor')
import dayi_video as dv, kis_sahneler, soguk_sahneler, toprak_sahneler, yem_sahneler
from cizim import FPS
from PIL import Image
w,h=Image.open('/tmp/three/kazan_crop.png').size; W=640; H=round(h*W/w); X=540-W//2; Y=1210-H
yem_sahneler.karma_kazan=lambda *a,**k: f'<image href="file:///tmp/three/kazan_crop.png" x="{X}" y="{Y}" width="{W}" height="{H}"/><g class="yemler" display="none"></g><g class="helezon" display="none"></g>'
print('kutu',X,Y,W,H)
from playwright.sync_api import sync_playwright
sen=json.load(open('/tmp/is/dayi6/senaryo.json'))
dv.ses_zarfi(sen,'/tmp/is/dayi6/ses/birlesik.wav')
pathlib.Path('/tmp/three/v.html').write_text(dv.html(sen))
bas=sum(round(p['sure']*FPS) for p in sen['parcalar'][:5]); n=round(sen['parcalar'][5]['sure']*FPS)
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--allow-file-access-from-files']); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///tmp/three/v.html'); pg.wait_for_timeout(600)
    pg.evaluate(f'window.renderFrame({bas+int(n*0.97)})'); pg.wait_for_timeout(300)
    pg.screenshot(path='/tmp/three/ornek_3d_sahne.png'); b.close()

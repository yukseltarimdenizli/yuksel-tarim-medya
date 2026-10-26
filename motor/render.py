"""Yüksel Tarım post görseli üretici.
Kullanım: python3 render.py <post.json> <cikti_klasoru>
post.json: {"slug","template","kicker","title","body","bullets":[...],"photo":opsiyonel}
Her post için hem 1080x1350 (Facebook) hem 1080x1920 (TikTok) PNG üretir.
"""
import base64, json, sys, pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
LOGO = base64.b64encode((ROOT / "assets/logo.png").read_bytes()).decode()

GREEN, GREEN_DK, GOLD, CREAM = "#2F5737", "#1F3D26", "#D4A445", "#F5F0E3"

def b64img(path):
    p = pathlib.Path(path)
    ext = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
    return f"data:image/{ext};base64," + base64.b64encode(p.read_bytes()).decode()

CSS = f"""
@font-face {{ font-family: P; src: local('Poppins'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:var(--h); font-family:Poppins, sans-serif; background:{CREAM}; color:{GREEN_DK}; overflow:hidden; position:relative; }}
.main {{ position:absolute; top:190px; bottom:170px; left:0; right:0; display:flex; flex-direction:column; justify-content:var(--jc); }}
.top {{ display:flex; align-items:center; gap:22px; padding:56px 64px 0; }}
.top img {{ width:96px; height:auto; }}
.brand {{ line-height:1.05; }}
.brand b {{ display:block; font-size:34px; font-weight:700; letter-spacing:1px; color:{GREEN}; }}
.brand span {{ font-size:20px; font-weight:500; letter-spacing:6px; color:{GOLD}; }}
.kicker {{ display:inline-block; margin:0 64px; align-self:flex-start; padding:10px 22px; background:{GOLD}; color:#fff; font-weight:600; font-size:26px; border-radius:40px; letter-spacing:1px; }}
h1 {{ margin:26px 64px 0; white-space:normal; overflow-wrap:normal; font-size:var(--h1); line-height:1.08; font-weight:700; color:{GREEN}; }}
h1 em {{ font-style:normal; color:{GOLD}; }}
p.body {{ margin:28px 64px 0; font-size:34px; line-height:1.4; font-weight:400; color:#3c4a3f; max-width:900px; }}
ul {{ list-style:none; margin:30px 64px 0; }}
li {{ font-size:32px; font-weight:500; padding:12px 0 12px 52px; position:relative; color:{GREEN_DK}; }}
li:before {{ content:""; position:absolute; left:0; top:20px; width:30px; height:30px; border-radius:50%; background:{GOLD}; box-shadow: inset 0 0 0 8px {CREAM}, 0 0 0 3px {GOLD}; }}
.photo {{ margin:36px 64px 0; height:var(--ph); border-radius:28px; background-size:cover; background-position:center; box-shadow:0 18px 40px rgba(31,61,38,.25); }}
.wm {{ position:absolute; right:-140px; bottom:120px; width:620px; opacity:.07; }}
.foot {{ position:absolute; left:0; right:0; bottom:0; height:150px; background:{GREEN}; display:flex; align-items:center; justify-content:space-between; padding:0 64px; color:#fff; }}
.foot:before {{ content:""; position:absolute; top:-14px; left:0; right:0; height:14px; background:{GOLD}; }}
.foot .l {{ font-size:28px; font-weight:600; }}
.foot .l small {{ display:block; font-size:22px; font-weight:400; opacity:.85; }}
.foot .r {{ font-size:26px; font-weight:500; color:{GOLD}; text-align:right; }}
"""

SIZES = {"fb": (1350, 108, "center", 560), "tiktok": (1920, 122, "center", 760)}

def build(post, size):
    h, h1, jc, ph = SIZES[size]
    e = html.escape
    title = e(post["title"]).replace("[", "<em>").replace("]", "</em>")
    parts = [f'<img class="wm" src="data:image/png;base64,{LOGO}">',
             f'<div class="top"><img src="data:image/png;base64,{LOGO}"><div class="brand"><b>YÜKSEL TARIM</b><span>DENİZLİ</span></div></div>',
             '<div class="main">', f'<div class="kicker">{e(post["kicker"])}</div>', f'<h1>{title}</h1>']
    if post.get("photo"):
        parts.append(f'<div class="photo" style="background-image:url({b64img(post["photo"])})"></div>')
    if post.get("body"):
        parts.append(f'<p class="body">{e(post["body"])}</p>')
    if post.get("bullets"):
        parts.append("<ul>" + "".join(f"<li>{e(b)}</li>" for b in post["bullets"]) + "</ul>")
    parts.append('</div>')
    parts.append(f'<div class="foot"><div class="l">{e(post.get("footer_left","Tarım makinelerinde güvenilir adres"))}'
                 f'<small>{e(post.get("footer_sub","Denizli ve tüm Türkiye’ye gönderim"))}</small></div>'
                 f'<div class="r">www.yukseltarimdenizli.com.tr</div></div>')
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body style="--h:{h}px;--h1:{h1}px;--jc:{jc};--ph:{ph}px">{"".join(parts)}</body></html>'), h

def render(post, outdir):
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for size in SIZES:
            doc, h = build(post, size)
            pg = b.new_page(viewport={"width": 1080, "height": h})
            pg.set_content(doc); pg.wait_for_timeout(300)
            pg.evaluate('''() => {
              const h=document.querySelector('h1'); let fs=parseFloat(getComputedStyle(h).fontSize);
              while (h.scrollWidth > h.clientWidth && fs > 50) { fs -= 3; h.style.fontSize = fs+'px'; }
              const m=document.querySelector('.main'); let k=1;
              while (m.scrollHeight > m.clientHeight + 2 && k > 0.6) { k -= 0.04; m.style.zoom = k; }
            }''')
            f = outdir / f'{post["slug"]}_{size}.png'
            pg.screenshot(path=str(f)); out.append(str(f)); pg.close()
        b.close()
    return out

if __name__ == "__main__":
    print("\n".join(render(json.loads(pathlib.Path(sys.argv[1]).read_text()), sys.argv[2])))

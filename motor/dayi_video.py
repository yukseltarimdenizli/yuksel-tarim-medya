"""'Dayı Soruyor' videosu (1080x1920, 30 fps) — iki karakterli soru-cevap.
Kullanım: python3 dayi_video.py <senaryo.json> <cikti.mp4> [--ses ses.m4a] [--muzik m.mp3 --muzik-bas 0]
senaryo: {"bant": "DAYI SORUYOR", "kapak": {...}, "parcalar": [{"sahne","konusan":"dayi|usta","metin","sure"}]}
Sahneler: dayi_soru, pulluk, rotavator, taban, tepki, kapanis.
Ses verilirse cizim.ses_hizala ile parçalara bölünür; ağız hareketi ses zarfından çıkar.
"""
import json, math, pathlib, re, shutil, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright
import cizim, usta, arka, dayi
from cizim import FPS, W, H, etiket, teker, traktor, on_toprak, YER

DAYI_AD, USTA_AD = dayi.DAYI_AD, dayi.USTA_AD


def kisi(x, y, s, model, poz, ifade, cls):
    return f'<g class="{cls}" data-x="{x}" data-y="{y}" data-s="{s}" transform="translate({x} {y}) scale({s})">{usta.usta(model, poz, ifade)}</g>'


def pip(cx, cy, r, poz="isaret", ifade="mutlu"):
    dayi._PIP[0] += 1
    cid = f"vpip{dayi._PIP[0]}"
    s = r / 190
    return (f'<g class="pipg" data-x="{cx}" data-y="{cy}"><defs><clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r+12}" fill="#E2B654" filter="url(#golge)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#pipzemin)"/>'
            f'<g clip-path="url(#{cid})"><g class="kisi-usta" transform="translate({cx} {cy + 860*s + 60*s}) scale({s})">{usta.usta("genc", poz, ifade)}</g></g>'
            + dayi.isim(cx, cy + r + 34, USTA_AD) + '</g>')


def baslik(metin, renk, yazi="#fff", w=None):
    w = w or len(metin) * 34 + 120
    return (f'<g class="bslk"><rect x="{540-w/2}" y="210" width="{w}" height="100" rx="50" fill="{renk}" filter="url(#golge)"/>'
            f'<text x="540" y="278" text-anchor="middle" font-size="58" font-weight="900" fill="{yazi}">{metin}</text></g>')


def doku(x, y, w, h, op=.6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#a_doku)" opacity="{op}"/>'


# ---------------------------------------------------------------- sahneler
def s_dayi_soru(p):
    g = arka.manzara()
    g += kisi(870, 1290, .6, "genc", "duz", "normal", "kisi-usta")
    g += kisi(330, 2050, 1.42, "kasketli", "bel", "endise", "kisi-dayi")
    g += '<!--UST--><g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["Kırk yıldır [pulluk] sürerim,", "rotavatör neyime yarar?"]), 300, 640, 58) + '</g>'
    return g, (340, 860, 1.0, 1.14)


def s_pulluk(p):
    Y, D = 820, 190
    g = ('<rect width="1080" height="1920" fill="url(#a_gok)"/>' + arka._bulut(800, 420, .7) +
         f'<defs><linearGradient id="v_alt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a98060"/><stop offset="1" stop-color="#7d5a3f"/></linearGradient>'
         f'<linearGradient id="v_ust" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5333"/><stop offset="1" stop-color="#5c3e25"/></linearGradient></defs>'
         f'<rect x="0" y="{Y+D}" width="1080" height="{1920-Y-D}" fill="url(#v_alt)"/>'
         + "".join(f'<ellipse cx="{(k*97)%1080}" cy="{Y+D+60+(k*53)%700}" rx="{12+k%4*7}" ry="{8+k%3*4}" fill="#8a6a50"/><ellipse cx="{(k*97)%1080-4}" cy="{Y+D+56+(k*53)%700}" rx="{5+k%4*3}" ry="{3+k%3*2}" fill="#c4a688" opacity=".7"/>' for k in range(34))
         + doku(0, Y + D, 1080, 1920 - Y - D, .5) +
         f'<rect x="620" y="{Y}" width="460" height="{D}" fill="url(#v_ust)"/>' + doku(620, Y, 460, D, .7)
         + "".join(f'<path d="M{x} {Y} l-4 -26 M{x+9} {Y} l4 -22" stroke="#d9b866" stroke-width="5" stroke-linecap="round"/>' for x in range(630, 1080, 20)))

    def dilim(px, aci, cls="", veri=""):
        sap = "".join(f'<path d="M{x} {-D} l-3 -24 M{x+8} {-D} l3 -20" stroke="#d9b866" stroke-width="5" stroke-linecap="round"/>' for x in range(6, 130, 18))
        return (f'<g class="{cls}" {veri} transform="translate({px} {Y+D}) rotate({aci})"><rect x="0" y="{-D}" width="130" height="{D}" rx="6" fill="url(#v_ust)" stroke="#3e2816" stroke-width="4"/>'
                f'<rect x="0" y="{-D}" width="130" height="{D}" filter="url(#a_doku)" opacity=".7"/>{sap}'
                + "".join(f'<circle cx="{14+(k*29)%110}" cy="{-D+20+(k*41)%(D-30)}" r="{4+k%3*2}" fill="#4a311c"/>' for k in range(8)) + '</g>')
    for px in [-30, 100, 230, 360]:
        g += dilim(px, -120)
    g += dilim(490, 0, "donen", 'data-px="490"')
    g += ('<g class="ok" opacity="0"><path d="M600 740 Q560 600 430 640" stroke="#c62828" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M452 604 L414 648 L466 664 Z" fill="#c62828"/></g>'
          f'<path d="M620 {Y} L620 {Y+D}" stroke="#3e2816" stroke-width="4"/>')
    g += (f'<g transform="translate(900 {Y})"><rect x="-22" y="0" width="44" height="{D}" rx="6" fill="#fff8e1" stroke="#8d6e63" stroke-width="3"/>'
          + "".join(f'<path d="M-22 {k*D/4:.0f} h20" stroke="#5d4037" stroke-width="4"/>' for k in range(5)) + '</g>')
    g += etiket(360, 560, 430, 760, "Toprağı ters çevirir", 30, "#c62828") + etiket(370, 1130, 260, 1050, "Anız alta gömülür", 100, "#2e7d32") + etiket(720, 760, 900, 900, "Derin sürüm", 120, "#14281A")
    g += '<text x="540" y="470" text-anchor="middle" font-size="44" font-weight="800" fill="#455a64" letter-spacing="3">TOPRAK KESİTİ</text>'
    g += '<!--UST-->' + baslik("PULLUK", "#c62828") + pip(925, 460, 110)
    return g, (560, 860, 1.12, 1.18)


def s_rotavator(p):
    g = arka.manzara()
    g += ('<defs><clipPath id="inceKes"><rect class="incerect" x="0" y="1100" width="300" height="300"/></clipPath></defs>'
          '<g clip-path="url(#inceKes)">' + dayi.tarla_ince(0, 1080, 1158, 104) + '</g>')
    g += (f'<g class="hareket" data-x0="520" transform="translate(520 {YER}) scale(.72)">{traktor("mutlu")}<g transform="translate(-235 -120)">{dayi.rotavator(1.0)}</g></g>')
    g += '<g class="toz"></g>'
    g += etiket(300, 560, 150, 1185, "Toprağı inceltir", 40, "#ef6c00") + etiket(400, 690, 330, 1190, "Ekim yatağı hazırlar", 90, "#2e7d32")
    g += '<!--UST-->' + baslik("ROTAVATÖR", "#ef6c00") + pip(925, 460, 110)
    return g, (540, 1000, 1.0, 1.07)


def s_taban(p):
    Y, T = 880, 1080
    g = ('<rect width="1080" height="1920" fill="url(#a_gok)"/>' + arka._bulut(220, 700, .6) +
         f'<rect x="0" y="{Y}" width="1080" height="{T-Y}" fill="#6f4b2e"/>' + doku(0, Y, 1080, T - Y, .8)
         + "".join(f'<circle cx="{(k*61)%1080}" cy="{Y+12+(k*37)%(T-Y-20)}" r="{5+k%4*3}" fill="#4f3520"/>' for k in range(60)) +
         f'<rect class="tabanb" x="0" y="{T}" width="1080" height="80" fill="url(#taban)"/><rect x="0" y="{T}" width="1080" height="6" fill="#2b2622"/>'
         f'<rect x="0" y="{T+80}" width="1080" height="{1920-T-80}" fill="#a1795a"/>' + doku(0, T + 80, 1080, 1920 - T - 80, .45)
         + "".join(f'<ellipse cx="{(k*113)%1080}" cy="{T+140+(k*71)%700}" rx="{12+k%4*6}" ry="{8+k%3*3}" fill="#8a6a50"/>' for k in range(22)))
    for i, x in enumerate((180, 420, 660, 900)):
        g += (f'<g class="bitki" data-x="{x}" data-y="{Y}" opacity="0"><path d="M{x} {Y} L{x} {Y-150}" stroke="#7cb342" stroke-width="10" stroke-linecap="round"/>'
              + "".join(f'<path d="M{x} {Y-40-k*36} q{18 if k%2 else -18} -16 {36 if k%2 else -36} -30" stroke="#8bc34a" stroke-width="8" fill="none" stroke-linecap="round"/>' for k in range(3)) +
              f'<ellipse cx="{x}" cy="{Y-166}" rx="12" ry="28" fill="#e2b654"/></g>'
              f'<path class="kok" pathLength="1" d="M{x} {Y} Q{x-8} {T-80} {x} {T-6} Q{x+40} {T-12} {x+110} {T-14}" stroke="#f3e5c0" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
              f'<path class="kok" pathLength="1" d="M{x} {Y+40} Q{x-50} {T-60} {x-110} {T-12}" stroke="#f3e5c0" stroke-width="5" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/>')
    g += '<g class="su" opacity="0">' + "".join(f'<ellipse cx="{70+k*120}" cy="{T-10}" rx="34" ry="10" fill="#4fc3f7" opacity=".85"/>' for k in range(9)) + '</g>'
    g += f'<path d="M0 {T} H1080" stroke="#FFD54F" stroke-width="6" stroke-dasharray="22 14"/>'
    g += (f'<g class="gecis" transform="translate(-400 {Y}) scale(.58)">{traktor("normal")}<g transform="translate(-235 -120)">{dayi.rotavator(1.0)}</g></g>'
          '<g class="toz"></g>')
    ust = ('<g class="yil"><rect x="50" y="360" width="250" height="84" rx="42" fill="#c62828" filter="url(#golge)"/>'
          '<text class="yiltxt" x="175" y="417" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">1. YIL</text></g>')
    g += (etiket(300, 1215, 200, T, "Her yıl aynı derinlik", 15, "#c62828") + etiket(800, 1215, 860, T + 40, "SERT TABAN", 110, "#14281A")
          + etiket(540, 975, 540, T - 10, "Su birikir, kök inemez", 210, "#1565c0"))
    g += '<!--UST-->' + ust + baslik("⚠ DİKKAT", "#14281A", "#FFD54F", 420) + pip(925, 460, 110, "isaret", "normal")
    return g, (540, 900, 1.0, 1.05)


def s_tepki(p):
    g = arka.manzara()
    g += kisi(820, 1420, .8, "genc", "basparmak", "mutlu", "kisi-usta")
    g += kisi(300, 1700, 1.1, "kasketli", "basparmak", "mutlu", "kisi-dayi")
    g += '<!--UST--><g class="balon" data-x="540" data-y="380">' + dayi.balon(60, 230, 960, 280, p.get("balon", ["Yani [ikisi de] lazımmış,", "hah! 😄"]), 280, 600, 62) + '</g>'
    return g, (540, 1100, 1.1, 1.0)


def s_kapanis(p):
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70)])
    g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
    g += kisi(560, 1640, 1.05, "genc", "salla", "mutlu", "kisi-usta")
    g += '<!--UST--><g class="balon" data-x="540" data-y="360">' + dayi.balon(60, 210, 960, 290, ["Sorunu [yorumlara] yaz,", "sıradaki videoda cevaplayalım!"], 600, 600, 54) + '</g>'
    g += ('<g class="takip" transform="translate(30 690)"><rect class="btn" width="330" height="96" rx="48" fill="#FE2C55" filter="url(#golge)"/>'
          '<text class="btnyazi" x="165" y="64" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">+ Takip et</text><text class="el" x="190" y="175" font-size="100">👆</text></g>')
    return g, (540, 1100, 1.0, 1.04)


def s_kapak(p):
    g = arka.manzara()
    g += kisi(300, 1440, .74, "kasketli", "bel", "normal", "kisi-dayi") + kisi(790, 1440, .74, "genc", "isaret", "mutlu", "kisi-usta")
    return g, (540, 960, 1.0, 1.0)


SAHNELER = {"dayi_soru": s_dayi_soru, "pulluk": s_pulluk, "rotavator": s_rotavator, "taban": s_taban, "tepki": s_tepki, "kapanis": s_kapanis, "kapak": s_kapak}

JS_EK = r"""
function agiz(el,sn,i){ const P=window.PARCALAR[i], k=P.konusan; if(!k) return; const Z=window.ZARF&&window.ZARF[i];
  let acik=false; if(Z){ const f=Math.floor(sn*FPS); acik=(Z[f]||0)>0.18; }
  else { const kon=P.konusma||[[0.15,P.sure*0.9]]; const ic=kon.some(([a,b])=>sn>=a&&sn<=b); acik= ic && (Math.sin(sn*26)+0.5*Math.sin(sn*41+1))>0.15; }
  $$('.kisi-'+k,el).forEach(g=>{ const a1=$('.agiz1',g), a2=$('.agiz2',g); if(a1&&a2){ a1.setAttribute('opacity',acik?0:1); a2.setAttribute('opacity',acik?1:0);} });
  const diger=k==='dayi'?'usta':'dayi'; $$('.kisi-'+diger,el).forEach(g=>{ const a1=$('.agiz1',g), a2=$('.agiz2',g); if(a1&&a2){ a1.setAttribute('opacity',1); a2.setAttribute('opacity',0);} }); }
function kamera(el,lt,d){ const k=$('.kam',el); if(!k) return; const [cx,cy,s0,s1]=k.dataset.k.split(',').map(Number); const e=ease(lt/d); const s=s0+(s1-s0)*(1-Math.pow(1-lt/d,2));
  k.setAttribute('transform',`translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`); }
function sallan(el,t){ $$('.kisi-dayi, .kisi-usta',el).forEach((g,i)=>{ if(!g.dataset.x) return; const x=+g.dataset.x, y=+g.dataset.y, s=+g.dataset.s; const b=Math.sin(t*0.08+i*1.3)*4*s;
  g.setAttribute('transform',`translate(${x} ${y+b}) scale(${s}) rotate(${Math.sin(t*0.05+i)*0.6})`); }); }
function balon(el,t){ const b=$('.balon',el); if(!b) return; const e=spring(t-4,0.22), x=+b.dataset.x, y=+b.dataset.y; b.setAttribute('transform',`translate(${x} ${y}) scale(${Math.min(e,1.08)}) translate(${-x} ${-y})`); b.setAttribute('opacity',Math.min(1,e*1.5)); }
function pipf(el,t){ $$('.pipg',el).forEach(g=>{ const e=spring(t-2,0.2), x=+g.dataset.x, y=+g.dataset.y; g.setAttribute('transform',`translate(${x} ${y}) scale(${Math.min(e,1.06)}) translate(${-x} ${-y})`); }); }
function bslk(el,t){ const b=$('.bslk',el); if(b){ const e=spring(t-1,0.22); b.setAttribute('transform',`translate(540 260) scale(${Math.min(e,1.08)}) translate(-540 -260)`); } }
Object.assign(SAHNE,{
 statik(el,t){},
 kapak(el,t){ clouds(el,0); },
 dayi_soru(el,t){ clouds(el,t); sallan(el,t); balon(el,t); },
 tepki(el,t){ clouds(el,t); balon(el,t); $$('.kisi-dayi',el).forEach(g=>{ const x=+g.dataset.x,y=+g.dataset.y,s=+g.dataset.s; const b=Math.abs(Math.sin(t*0.5))*-10; g.setAttribute('transform',`translate(${x} ${y+b}) scale(${s})`); });
   $$('.kisi-usta',el).forEach(g=>{ const x=+g.dataset.x,y=+g.dataset.y,s=+g.dataset.s; g.setAttribute('transform',`translate(${x} ${y+Math.sin(t*0.1)*4}) scale(${s})`); }); },
 pulluk(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); const d=$('.donen',el); const e=ease((t-62)/48); d.setAttribute('transform',`translate(490 1010) rotate(${-120*e})`); $('.ok',el).setAttribute('opacity', ease((t-52)/10)*(1-ease((t-118)/10))); },
 rotavator(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); wheels(el,t,1.6); beacon(el,t); const x=520+t*1.2; $('.hareket',el).setAttribute('transform',`translate(${x} 1222) scale(.72)`);
   $('.incerect',el).setAttribute('width', Math.max(0,x-150));
   $$('.rotor',el).forEach(r=>r.setAttribute('transform',`translate(-230 92) rotate(${t*14})`)); puffs($('.duman',el),t,312,-570,4,'#9e9e9e',.8);
   let s=''; for(let i=0;i<12;i++){ const p=((t*1.5+i*9)%40)/40; s+=`<circle cx="${x-200-p*140}" cy="${1205-Math.sin(p*Math.PI)*60}" r="${4+i%3*2}" fill="#8a6440" opacity="${(1-p).toFixed(2)}"/>`; } $('.toz',el).innerHTML=s; },
 taban(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); wheels(el,t,2.4); beacon(el,t);
   const GS=5, GL=40, k=Math.floor((t-GS)/GL), gp=((t-GS)%GL)/GL, aktif=t>=GS && k<3;
   const x=aktif? -400+gp*1900 : 1700; $('.gecis',el).setAttribute('transform',`translate(${x} 880) scale(.58)`);
   $$('.rotor',el).forEach(r=>r.setAttribute('transform',`translate(-230 92) rotate(${t*16})`));
   let s=''; if(aktif){ for(let i=0;i<14;i++){ const p=((t*1.6+i*7)%30)/30; s+=`<circle cx="${x-150-p*120}" cy="${890-Math.sin(p*Math.PI)*50}" r="${4+i%3*2}" fill="#6f4b2c" opacity="${(1-p).toFixed(2)}"/>`; } } $('.toz',el).innerHTML=s;
   const yil=Math.min(3, Math.max(1, k+1)); $('.yiltxt',el).textContent=yil+'. YIL'; $('.yil',el).setAttribute('opacity', t<GS+3*GL+5 ? 1 : (1-ease((t-GS-3*GL-5)/10)).toFixed(2));
   const tamam=Math.min(3, Math.max(0,(t-GS)/GL)); $('.tabanb',el).setAttribute('opacity', (0.15+0.85*tamam/3).toFixed(2));
   $$('.bitki',el).forEach((b,i)=>{ const e=ease((t-128-i*4)/22), bx=+b.dataset.x, by=+b.dataset.y; b.setAttribute('transform',`translate(${bx} ${by}) scale(1 ${Math.max(0.001,e)}) translate(${-bx} ${-by})`); b.setAttribute('opacity', e>0?1:0); });
   $$('.kok',el).forEach((kk,i)=>kk.setAttribute('stroke-dashoffset', (1-ease((t-148-i*3)/55)).toFixed(3)));
   $('.su',el).setAttribute('opacity', ease((t-205)/20)); },
 kapanis(el,t){ balon(el,t); sallan(el,t); const tap=t-60, bas=tap>0&&tap<8, ya=tap>=4; const elx=$('.el',el);
   elx.setAttribute('transform',`translate(${(1-ease((t-30)/18))*200} ${(1-ease((t-30)/18))*160 + (bas?-12:0)})`); elx.setAttribute('opacity', ease((t-28)/6));
   $('.btn',el).setAttribute('fill', ya?'#43a047':'#FE2C55'); $('.btnyazi',el).textContent = ya?'✓ Takip edildi':'+ Takip et'; },
});
const _rf=window.renderFrame;
window.renderFrame=function(f){ _rf(f); let acc=0; const P=window.PARCALAR, K=window.KAPAK; if(K && f<Math.round((K.sure||0.2)*FPS)) return;
  for(let i=0;i<P.length;i++){ const d=Math.round(P[i].sure*FPS); if(f>=acc&&f<acc+d){ const el=document.getElementById('p'+i), svg=el.querySelector('svg'), lt=f-acc;
      agiz(svg, lt/FPS, i); kamera(svg, lt, d); const kt=el.querySelector('.konusan'); if(kt) kt.style.opacity=ease(lt/5); }
    acc+=d; } };
"""

CSS_EK = """.konusan{position:absolute;left:50%;top:1290px;transform:translateX(-50%);font-size:34px;font-weight:900;padding:8px 26px;border-radius:30px;color:#fff;letter-spacing:1px;white-space:nowrap;box-shadow:0 6px 16px rgba(0,0,0,.3)}
.konusan.dayi{background:#83303f;border:3px solid #E2B654}.konusan.usta{background:#2F5737;border:3px solid #E2B654}"""


def rotor_sinifi(svg):
    # dayi.rotavator içindeki bıçak grubunu döndürülebilir yap
    return svg.replace('<g transform="translate(-230 92)"><circle r="30" fill="#455a64"/>', '<g class="rotor" transform="translate(-230 92)"><circle r="30" fill="#455a64"/>')


def html(sen):
    logo = cizim.logo_uri()
    bant = sen.get("bant", "DAYI SORUYOR")
    parts = []
    for i, p in enumerate(sen["parcalar"]):
        kz = cizim.kelime_zamanlari(p)
        kel = "".join(f'<span class="w" data-ch="{k}" data-ts="{t:.3f}">{w}</span>' for k, ob in enumerate(cizim.obekler(kz)) for w, t in ob)
        icerik, kam = SAHNELER[p["sahne"]](p)
        icerik = rotor_sinifi(icerik).replace('href="LOGO"', f'href="{logo}"')
        kon = p.get("konusan")
        etk = f'<div class="konusan {kon}">{DAYI_AD if kon=="dayi" else USTA_AD}</div>' if kon else ""
        parts.append(f'<div class="p" id="p{i}"><svg viewBox="0 0 1080 1920" width="1080" height="1920" font-family="Poppins">'
                     f'<g class="kam" data-k="{",".join(map(str, kam))}">{icerik.split("<!--UST-->")[0]}</g>{arka.isik()}<rect width="1080" height="1920" fill="url(#vinyet)"/>'
                     f'{"".join(icerik.split("<!--UST-->")[1:])}</svg>'
                     f'<div class="bant"><img src="{logo}"><b>YÜKSEL TARIM</b><span>· {bant}</span></div>{etk}<div class="alt">{kel}</div></div>')
    kp = sen.get("kapak")
    if kp:
        icerik, _ = SAHNELER["kapak"](kp)
        icerik = icerik.replace('href="LOGO"', f'href="{logo}"')
        bas = re.sub(r"\[(.+?)\]", r"<i>\1</i>", kp.get("baslik", ""))
        parts.append(f'<div class="kapak" id="kapak"><svg viewBox="0 0 1080 1920" width="1080" height="1920" font-family="Poppins">{icerik}{arka.isik()}<rect width="1080" height="1920" fill="url(#vinyet)"/></svg><div class="kk"></div>'
                     f'<div class="bant"><img src="{logo}"><b>YÜKSEL TARIM</b><span>· {bant}</span></div>'
                     + (f'<div class="ust">{kp["ust"]}</div>' if kp.get("ust") else "") + f'<h1>{bas}</h1>'
                     + (f'<div class="altp">{kp["alt"]}</div>' if kp.get("alt") else "") + '</div>')
    kpj = dict(kp, sahne="statik") if kp else None
    return (f"<html><head><meta charset='utf-8'><style>{cizim.CSS}{CSS_EK}</style></head><body>{cizim.DEFS}{usta.USTA_DEFS}{dayi.EK_DEFS}{arka.ARKA_DEFS}{''.join(parts)}"
            f"<script>window.PARCALAR={json.dumps(sen['parcalar'], ensure_ascii=False)};window.KAPAK={json.dumps(kpj, ensure_ascii=False)};window.ZARF={json.dumps(sen.get('_zarf'))};{cizim.JS}{JS_EK}</script></body></html>")


def ses_zarfi(sen, ses):
    """Her parça için kare başına ses şiddeti (0-1) — ağız hareketi için."""
    import array
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", ses, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    a = array.array("h", raw)
    per = 8000 // FPS
    tum = [math.sqrt(sum(x * x for x in a[i:i+per]) / max(1, len(a[i:i+per]))) for i in range(0, len(a), per)]
    mx = max(tum) or 1
    tum = [v / mx for v in tum]
    z, bas = [], 0.0
    for p in sen["parcalar"]:
        f0 = round(bas * FPS); n = round(p["sure"] * FPS)
        z.append([round(v, 3) for v in tum[f0:f0+n]]); bas += p["sure"]
    sen["_zarf"] = z


def render(sen, out, ses=None, muzik=None, muzik_bas=0):
    if ses:
        cizim.ses_hizala(sen, ses); ses_zarfi(sen, ses)
    total = sum(round(p["sure"] * FPS) for p in sen["parcalar"])
    tmp = pathlib.Path(tempfile.mkdtemp())
    (tmp / "v.html").write_text(html(sen))
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}); hata = []
        pg.on("pageerror", lambda e: hata.append(str(e)))
        pg.goto((tmp / "v.html").as_uri()); pg.wait_for_timeout(500)
        for f in range(total):
            pg.evaluate(f"window.renderFrame({f})"); pg.screenshot(path=str(tmp / f"f{f:05d}.png"))
        b.close()
        if hata:
            print("JS HATA:", hata[:3])
    sessiz = tmp / "s.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", str(sessiz)], check=True)
    dur = total / FPS
    if ses or muzik:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(sessiz)]; filt = []
        if ses:
            cmd += ["-i", ses]; filt.append(f"[1:a]aresample=48000,loudnorm=I=-14:TP=-1.5,aresample=48000,apad=whole_dur={dur},atrim=0:{dur},asetpts=PTS-STARTPTS[v]")
        if muzik:
            cmd += ["-ss", str(muzik_bas), "-i", muzik]; mi = 2 if ses else 1
            filt.append(f"[{mi}:a]aresample=48000,atrim=0:{dur},asetpts=PTS-STARTPTS,volume={0.14 if ses else 0.8},afade=t=out:st={dur-1.5:.2f}:d=1.5[m]")
        if ses and muzik:
            filt.append("[v][m]amix=inputs=2:duration=longest:normalize=0[a]")
        else:
            filt[-1] = filt[-1].rsplit("[", 1)[0] + "[a]"
        cmd += ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur}", str(out)]
        subprocess.run(cmd, check=True)
    else:
        shutil.copy(sessiz, out)
    shutil.rmtree(tmp)
    return out, dur


if __name__ == "__main__":
    a = sys.argv[1:]
    sen = json.loads(pathlib.Path(a[0]).read_text())
    ses = a[a.index("--ses") + 1] if "--ses" in a else None
    muz = a[a.index("--muzik") + 1] if "--muzik" in a else None
    mb = float(a[a.index("--muzik-bas") + 1]) if "--muzik-bas" in a else 0
    print(render(sen, a[1], ses, muz, mb))

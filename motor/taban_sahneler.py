"""Dayı Soruyor — sert taban / pulluk tabanı sahneleri (ilk kullanım: #5).
Toprak kesiti kesit(): üstte gök, sürüm katmanı, gri "beton" taban katmanı (parçalı, çatlatılabilir), alt toprak.
Sahneler:
  tdayi     dayı tarlada, traktör zorlanıyor; kanca hapı
  t3        görünmez beton: PULLUK TABANI etiketi + 3 adım kartı (3. altın)
  tsebep    dayi_video 'taban' sahnesi (rotavatör 3 yıl aynı derinlik) — başlık SEBEP, bitki/su yok
  tbelirti  aynı kesit, taban hazır: bitkiler, su göllenir, kökler yana kıvrılır, solma hapı
  tcubuk    demir çubuk testi: çubuk iner, tabanda TAK! (1/3)
  tdip      dipkazan tabanın altından geçer, taban çatlar; çamur uyarısı (2/3)
  tyonca    yonca kökleri tabanı deler (3/3)
  tkapanis  4 maddelik özet + takip
Diğerleri: soguk_sahneler.smadde/skaydet, kis_sahneler.ktepki.
"""
import re
import dayi_video as dv
import dayi
import arka
import kis_sahneler as ks
import soguk_sahneler as ss
from cizim import traktor, etiket
from toprak_sahneler import pop, hap, kart, emo, zemin_krem, _kt

U = "<!--UST-->"
Y0, T0 = 760, 1010      # kesit: yüzey, taban üstü
TK = 70                  # taban kalınlığı


def kesit(Y=Y0, T=T0, parcali=True):
    g = ('<rect width="1080" height="1920" fill="url(#a_gok)"/>' + arka._bulut(200, 520, .5) + arka._bulut(760, 600, .4)
         + f'<rect x="0" y="{Y}" width="1080" height="{T-Y}" fill="#6f4b2e"/>' + dv.doku(0, Y, 1080, T - Y, .8)
         + "".join(f'<circle cx="{(k*61)%1080}" cy="{Y+14+(k*37)%(T-Y-24)}" r="{5+k%4*3}" fill="#4f3520"/>' for k in range(50))
         + f'<path d="M0 {Y} Q270 {Y-14} 540 {Y} T1080 {Y}" fill="none" stroke="#5a3b22" stroke-width="10"/>'
         + f'<rect x="0" y="{T+TK}" width="1080" height="{1920-T-TK}" fill="#a1795a"/>' + dv.doku(0, T + TK, 1080, 1920 - T - TK, .45)
         + "".join(f'<ellipse cx="{(k*113)%1080}" cy="{T+TK+50+(k*71)%600}" rx="{12+k%4*6}" ry="{8+k%3*3}" fill="#8a6a50"/>' for k in range(20)))
    # taban: 18 parça (çatlatılabilir)
    w = 60
    for i in range(18):
        x = i * w
        g += (f'<g class="parca" data-x="{x+w/2}" data-i="{i}"><rect x="{x}" y="{T}" width="{w+1}" height="{TK}" fill="#7d7469"/>'
              + "".join(f'<path d="M{x+6+j*14} {T+8} l10 {TK-16}" stroke="#5f574e" stroke-width="3" opacity=".7"/>' for j in range(4))
              + f'<path class="catlak" d="M{x+w/2} {T} l-8 18 l12 16 l-10 18 l8 18" stroke="#2b2622" stroke-width="4" fill="none" opacity="0"/></g>')
    g += f'<path d="M0 {T} H1080" stroke="#FFD54F" stroke-width="5" stroke-dasharray="22 14"/>'
    return g


def rozet(no, renk="#2F5737"):
    return ss.rozet(no, 3, renk)


# ---------------------------------------------------------------- sahneler
def s_tdayi(p):
    A = p.get("_a", {})
    g = arka.manzara()
    g += f'<g class="trkz" data-x="600" data-y="1150"><g transform="translate(600 1150) scale(.44)">{traktor("normal")}</g></g><g class="kdum"></g>'
    g += dv.kisi(920, 1300, .55, "genc", "duz", "normal", "kisi-usta")
    g += dv.kisi(300, 2050, 1.42, "kasketli", "bel", "endise", "kisi-dayi")
    g += U
    if p.get("kanca"):
        g += pop(hap(540, 196, p["kanca"], "#c62828", "#fff", 38), A.get("kanca", 12), 540, 196)
    g += '<g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["?"]), 300, 640, 52) + '</g>'
    return g, (340, 860, 1.0, 1.12)


def s_t3(p):
    A = p.get("_a", {})
    g = kesit()
    g += etiket(300, 1200, 300, T0 + 35, "PULLUK TABANI", A.get("pulluk", 40), "#14281A")
    for i, (ad, renk, yazi) in enumerate([("1. KONTROL", "#fff", "#2F5737"), ("2. ÇÖZÜM", "#fff", "#2F5737"), ("3. ?", "#E2B654", "#c62828")]):
        cx = 160 + i * 240
        g += pop(kart(cx - 110, 540, 220, 120, renk, 30) + f'<text x="{cx}" y="612" text-anchor="middle" font-size="34" font-weight="900" fill="{yazi}">{ad}</text>',
                 A.get(f"k{i}", 90 + i * 5), cx, 600)
    g += pop(hap(760, 1120, "Görünmez beton! 🧱", "#c62828", "#fff", 38), A.get("beton", 20), 760, 1120)
    g += U + dv.baslik("SERT TABAN", "#14281A", "#FFD54F", 420) + dv.pip(925, 460, 110)
    g += pop(hap(420, 712, "Sonuncusunu çoğu kişi atlıyor 👇", "#c62828", "#fff", 34), A.get("son", 150), 420, 712)
    return g, (540, 900, 1.0, 1.03)


def _taban_baslik(p, yeni):
    g, kam = dv.s_taban(p)
    g = g.replace(dv.baslik("⚠ DİKKAT", "#14281A", "#FFD54F", 420), dv.baslik(yeni, "#14281A", "#FFD54F", 420))
    return g, kam


def s_tsebep(p):
    return _taban_baslik(p, "SEBEP")


def s_tbelirti(p):
    A = p.get("_a", {})
    g, kam = _taban_baslik(p, "BELİRTİLER")
    g = g.replace('<g class="yil">', '<g class="yil" style="display:none">')
    g += pop(hap(440, 650, "Kuraklıkta ürün çabuk solar 🥀", "#c62828", "#fff", 36), A.get("solar", 9999), 440, 650)
    return g, kam


def s_tcubuk(p):
    A = p.get("_a", {})
    g = kesit()
    g += ('<g class="cubuk"><rect x="-6" y="-330" width="12" height="330" rx="6" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
          '<rect x="-60" y="-344" width="120" height="20" rx="10" fill="#455a64"/><path d="M-6 0 L0 16 L6 0 Z" fill="#455a64"/></g>')
    g += f'<g class="tak" opacity="0"><text x="740" y="{T0-30}" font-size="64" font-weight="900" fill="#c62828" stroke="#fff" stroke-width="8" paint-order="stroke">TAK!</text></g>'
    g += etiket(330, 1190, 680, T0 + 20, "Taban burada", A.get("orada", 9999), "#c62828")
    g += pop(hap(320, 600, "Toprak tavındayken 💧", "#2F5737", "#fff", 36), A.get("tav", 20), 320, 600)
    g += U + rozet(1) + dv.baslik("1. KONTROL", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_tdip(p):
    A = p.get("_a", {})
    g = kesit()
    # dipkazan: çerçeve + tabanın altına inen kavisli ayak
    g += ('<g class="dip"><rect x="-120" y="-90" width="240" height="34" rx="8" fill="#c62828" stroke="#7f1414" stroke-width="4"/>'
          f'<path d="M-14 -60 L14 -60 L14 {T0-Y0+TK+30} Q14 {T0-Y0+TK+60} 46 {T0-Y0+TK+70} L46 {T0-Y0+TK+84} Q-14 {T0-Y0+TK+80} -14 {T0-Y0+TK+30} Z" fill="#455a64" stroke="#263238" stroke-width="4"/>'
          '<path d="M-120 -74 L-260 -74" stroke="#455a64" stroke-width="12"/></g>')
    g += pop(hap(330, 580, "Kuruyken ya da tavında ✅", "#2F5737", "#fff", 36), A.get("kuru", 9999), 330, 580)
    g += pop(hap(330, 670, "Çamurda çekme ❌", "#c62828", "#fff", 40), A.get("camur", 9999), 330, 670)
    g += etiket(760, 1190, 700, T0 + TK + 20, "Tabanın altına in", A.get("alt", 9999), "#2F5737")
    g += U + rozet(2) + dv.baslik("2. ÇÖZÜM: DİPKAZAN", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_tyonca(p):
    A = p.get("_a", {})
    g = kesit()
    for i, x in enumerate((150, 330, 510, 690, 870)):
        g += (f'<g class="yonca" data-x="{x}" data-y="{Y0}" opacity="0">' + "".join(
              f'<g transform="translate({x+dx} {Y0-40-dy})"><circle r="15" fill="#43a047"/><circle cx="14" cy="-8" r="13" fill="#66bb6a"/><circle cx="-12" cy="-10" r="13" fill="#4caf50"/></g>'
              for dx, dy in ((-18, 10), (16, 30), (0, 60))) + f'<path d="M{x} {Y0} V{Y0-60}" stroke="#2e7d32" stroke-width="7"/></g>'
              f'<path class="yk" pathLength="1" d="M{x} {Y0} Q{x+10} {T0-40} {x-4} {T0+TK+60} Q{x-14} {T0+TK+160} {x+6} {T0+TK+230}" stroke="#f3e5c0" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
              f'<path class="yk" pathLength="1" d="M{x} {Y0+80} Q{x+60} {T0+20} {x+50} {T0+TK+120}" stroke="#f3e5c0" stroke-width="6" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/>')
    g += pop(hap(450, 580, "Derin köklü bitki: yonca 🌿", "#2F5737", "#fff", 38), A.get("yonca", 30), 450, 580)
    g += etiket(540, 1200, 520, T0 + TK + 40, "Toprağı aşağıdan gevşetir", A.get("gevset", 9999), "#2F5737")
    g += U + rozet(3, "#b8860b") + dv.baslik("EKİM NÖBETİ", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_tkapanis(p):
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70)])
    g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
    g += '<text x="540" y="400" text-anchor="middle" font-size="46" font-weight="900" fill="#E2B654">TARLAN RAHAT NEFES ALSIN</text>'
    M = [("🔍", "Çubukla kontrol"), ("🚜", "Dipkazan (kuru)"), ("🔄", "Derinliği değiştir"), ("🌿", "Yonca ek")]
    for i, (e, ad) in enumerate(M):
        x, y = 285 + (i % 2) * 470, 500 + (i // 2) * 112
        g += pop(f'<rect x="{x-215}" y="{y-44}" width="430" height="88" rx="44" fill="#fff" filter="url(#golge)"/>' + emo(x - 160, y + 17, e, 42)
                 + f'<text x="{x-115}" y="{y+12}" font-size="32" font-weight="900" fill="#2F5737">{ad}</text>', 4 + i * 5, x, y)
    g += dv.kisi(300, 1770, .95, "kasketli", "salla", "mutlu", "kisi-dayi")
    g += ('<g class="takip" transform="translate(600 860)"><rect class="btn" width="400" height="110" rx="55" fill="#FE2C55" filter="url(#golge)"/>'
          '<text class="btnyazi" x="200" y="74" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">+ Takip et</text><text class="el" x="230" y="200" font-size="110">👆</text></g>')
    g += '<text x="760" y="1200" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">Seri devam ediyor!</text>'
    return g, (540, 1100, 1.0, 1.03)


dv.SAHNELER.update({"tdayi": s_tdayi, "t3": s_t3, "tsebep": s_tsebep, "tbelirti": s_tbelirti, "tcubuk": s_tcubuk,
                    "tdip": s_tdip, "tyonca": s_tyonca, "tkapanis": s_tkapanis})

BUYUK = 99999


def _sebep(p, kt, n):
    gs = _kt(kt, "her", 40) - 6
    ge = _kt(kt, "oluşuyor", n - 20) + 6
    return {"gs": gs, "gl": max(24, (ge - gs) / 3), "sert": _kt(kt, "sert", ge) - 4, "bitki": BUYUK, "su": BUYUK, "kok0": BUYUK, "kokd": 30}


def _belirti(p, kt, n):
    k0 = _kt(kt, "kökler", 120) - 2
    return {"gs": -400, "gl": 40, "sert": -10, "bitki": 4, "su": _kt(kt, "göllenir", 90) - 4,
            "kok0": k0, "kokd": max(20, _kt(kt, "kıvrılır", k0 + 40) + 10 - k0), "solar": _kt(kt, "kuraklıkta", 200) - 2}


dv.ANIM_EK.update({
    "tdayi": lambda p, kt, n: {"kanca": 12},
    "t3": lambda p, kt, n: {"beton": _kt(kt, "beton", 20) - 2, "pulluk": _kt(kt, "pulluk", 40) - 2,
                            **{f"k{i}": _kt(kt, "üç", 90) + i * 5 for i in range(3)}, "son": _kt(kt, "sonuncusunu", 150) - 2},
    "tsebep": _sebep,
    "tbelirti": _belirti,
    "tcubuk": lambda p, kt, n: {"tav": _kt(kt, "tavındayken", 20) - 2, "bas": _kt(kt, "bastır", 60) - 6,
                                "sert": _kt(kt, "sertleşiyorsa", 120) - 2, "orada": _kt(kt, "orada", 150) - 2},
    "tdip": lambda p, kt, n: {"dip0": _kt(kt, "dipkazanla", 30) - 6, "dip1": _kt(kt, "in", 110) + 6, "alt": _kt(kt, "altına", 80) - 2,
                              "kuru": _kt(kt, "kuruyken", 140) - 2, "camur": _kt(kt, "çamurda", 200) - 2},
    "tyonca": lambda p, kt, n: {"yonca": _kt(kt, "yonca", 30) - 4, "kok0": _kt(kt, "kökleri", 80) - 4, "gevset": _kt(kt, "gevşetir", 120) - 4},
    "tkapanis": lambda p, kt, n: {"tap": _kt(kt, "takip", 40)},
})

dv.JS_EK += r"""
Object.assign(SAHNE,{
 tdayi(el,t){ clouds(el,t); sallan(el,t); balon(el,t); poplar(el,t); const tr=$('.trkz',el); if(tr){ tr.setAttribute('transform',`translate(${(Math.sin(t*1.7)*3).toFixed(1)} ${(Math.abs(Math.sin(t*2.3))*-3).toFixed(1)})`); }
   let s=''; for(let i=0;i<6;i++){ const p=((t*0.9+i*7)%40)/40; s+=`<circle cx="${(640+p*40).toFixed(1)}" cy="${(1000-p*160).toFixed(1)}" r="${(10+p*26).toFixed(1)}" fill="#424242" opacity="${(0.55*(1-p)).toFixed(2)}"/>`; } $('.kdum',el).innerHTML=s; },
 t3(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); poplar(el,t); },
 tsebep(el,t){ SAHNE.taban(el,t); },
 tbelirti(el,t){ SAHNE.taban(el,t); poplar(el,t); },
 tcubuk(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), B=A.bas??60, S=A.sert??120;
   const Y=760, T=1010; let tip; if(t<B) tip=Y-20; else if(t<S) tip=Y-20+(T-Y+20)*ease((t-B)/Math.max(1,S-B)); else tip=T;
   const sh = (t>=S && t<S+8) ? Math.sin(t*3)*5 : 0; $('.cubuk',el).setAttribute('transform',`translate(${(680+sh).toFixed(1)} ${tip.toFixed(1)})`);
   const k=$('.tak',el); k.setAttribute('opacity', t>=S ? Math.max(0,1-(t-S-30)/10) : 0); },
 tdip(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), D0=A.dip0??30, D1=Math.max(D0+30,A.dip1??110);
   const x = t<D0 ? -300 : (t<D1 ? -300+1600*((t-D0)/(D1-D0)) : 1400); $('.dip',el).setAttribute('transform',`translate(${x.toFixed(1)} 760)`);
   $$('.parca',el).forEach(pc=>{ const px=+pc.dataset.x, i=+pc.dataset.i; const k = x+40>px ? Math.min(1,(x+40-px)/80) : 0; const r=(i%2?1:-1)*5*k, dy=(i%3-1)*5*k;
     pc.setAttribute('transform',`rotate(${r.toFixed(2)} ${px} 1045) translate(0 ${dy.toFixed(1)})`); const c=$('.catlak',pc); if(c) c.setAttribute('opacity',k.toFixed(2)); }); },
 tyonca(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), YO=A.yonca??30, K0=A.kok0??80;
   $$('.yonca',el).forEach((b,i)=>{ const e=ease((t-YO-i*4)/14), bx=+b.dataset.x, by=+b.dataset.y; b.setAttribute('transform',`translate(${bx} ${by}) scale(${Math.max(0.001,e)}) translate(${-bx} ${-by})`); b.setAttribute('opacity', e>0?1:0); });
   $$('.yk',el).forEach((k,i)=>k.setAttribute('stroke-dashoffset',(1-ease((t-K0-i*3)/50)).toFixed(3)));
   const kx=[150,330,510,690,870]; const kk=ease((t-K0-25)/30); $$('.parca',el).forEach(pc=>{ const px=+pc.dataset.x; const yakin=kx.some(v=>Math.abs(v-px)<35); const c=$('.catlak',pc); if(c) c.setAttribute('opacity', yakin? kk.toFixed(2):0); }); },
 tkapanis(el,t){ SAHNE.skapanis(el,t); },
});
"""

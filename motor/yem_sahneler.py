"""Dayı Soruyor — yem karma / elle karıştırma sahneleri (ilk kullanım: #6 "Yem karma mı, elle karıştırma mı?").
Sahneler:
  ydayi     dayı yemlik başında, yemlikte saman kalmış; kanca hapı
  y3        YEM SEÇİYOR: yemlikte ayrı duran saman/silaj/kesif yem + 3 fark kartı (3. altın)
  ykarma    dikey yem karma kazanı: helezon döner, renkli yemler karışır (1/3)
  ykapanis  4 maddelik özet + yorum çağrısı + takip
Diğerleri: soguk_sahneler.smadde/skaydet, kis_sahneler.ktepki.
"""
import dayi_video as dv
import dayi
import arka
import kis_sahneler as ks
import soguk_sahneler as ss
from cizim import etiket
from toprak_sahneler import pop, hap, kart, emo, zemin_krem, _kt

U = "<!--UST-->"
SAMAN, SILAJ, KESIF = "#e8c547", "#7cb342", "#8d5a2b"


def yemlik(x, y, w=620, h=150, dolu="ayri"):
    """Ahşap yemlik. dolu='ayri': dipte saman kalmış (hayvan seçmiş); 'karisik': her yer aynı karışım."""
    g = (f'<g transform="translate({x} {y})"><ellipse cx="0" cy="{h+16}" rx="{w/2+20}" ry="18" fill="#000" opacity=".18"/>'
         f'<path d="M{-w/2} 0 L{w/2} 0 L{w/2-40} {h} L{-w/2+40} {h} Z" fill="#8d6e4e" stroke="#5d4037" stroke-width="8" stroke-linejoin="round"/>'
         + "".join(f'<path d="M{-w/2+20+k*4} {32+k*38} H{w/2-20-k*4}" stroke="#6d4c33" stroke-width="4" opacity=".7"/>' for k in range(3)))
    if dolu == "ayri":
        g += "".join(f'<path d="M{-w/2+50+(k*53)%(w-100)} {-4-(k*7)%18} l{18+(k%3)*8} {-14-(k*5)%12}" stroke="{SAMAN}" stroke-width="7" stroke-linecap="round"/>' for k in range(28))
    elif dolu == "karisik":
        g += "".join(f'<circle cx="{-w/2+50+(k*37)%(w-100)}" cy="{-6-(k*11)%22}" r="{7+k%3*2}" fill="{[SAMAN, SILAJ, KESIF][k%3]}"/>' for k in range(42))
    return g + '</g>'


def rozet(no, renk="#2F5737"):
    return ss.rozet(no, 3, renk)


# ---------------------------------------------------------------- sahneler
def s_ydayi(p):
    A = p.get("_a", {})
    g = arka.manzara()
    g += yemlik(640, 1150, 560, 130)
    g += '<text x="860" y="1120" font-size="84">🐄</text>'
    g += dv.kisi(300, 2050, 1.42, "kasketli", "bel", "endise", "kisi-dayi")
    g += U
    if p.get("kanca"):
        g += pop(hap(540, 196, p["kanca"], "#c62828", "#fff", 38), A.get("kanca", 12), 540, 196)
    g += '<g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["?"]), 300, 640, 52) + '</g>'
    return g, (340, 860, 1.0, 1.12)


def s_y3(p):
    A = p.get("_a", {})
    g = zemin_krem()
    # yemlikte ayrı duran yemler
    g += yemlik(540, 950, 760, 140, "bos")
    for i, (ad, renk, x) in enumerate([("Saman", SAMAN, 300), ("Silaj", SILAJ, 540), ("Kesif yem", KESIF, 780)]):
        g += (f'<g>' + "".join(f'<circle cx="{x-70+(k*29)%140}" cy="{930-(k*13)%40}" r="{12+k%3*3}" fill="{renk}"/>' for k in range(14))
              + f'<text x="{x}" y="868" text-anchor="middle" font-size="34" font-weight="900" fill="#14281A">{ad}</text></g>')
    g += pop(hap(540, 1195, "Karışmamış: hayvan seçer 🐄", "#c62828", "#fff", 40), A.get("secer", 20), 540, 1195)
    for i, (ad, renk, yazi) in enumerate([("1. FARK", "#fff", "#2F5737"), ("2. FARK", "#fff", "#2F5737"), ("3. ?", "#E2B654", "#c62828")]):
        cx = 160 + i * 240
        g += pop(kart(cx - 110, 530, 220, 110, renk, 30) + f'<text x="{cx}" y="597" text-anchor="middle" font-size="36" font-weight="900" fill="{yazi}">{ad}</text>',
                 A.get(f"k{i}", 90 + i * 5), cx, 585)
    g += U + dv.baslik("YEM SEÇİYOR!", "#c62828", "#fff", 460) + dv.pip(925, 460, 110)
    g += pop(hap(420, 700, "Sonuncusunu çoğu kişi bilmiyor 👇", "#c62828", "#fff", 32), A.get("son", 150), 420, 700)
    return g, (540, 900, 1.0, 1.03)


def karma_kazan(x=520, y=760, s=1.0):
    """Dikey yem karma: kesik koni kazan, ortada helezon, tekerlekli şasi."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<ellipse cx="0" cy="560" rx="380" ry="30" fill="#000" opacity=".18"/>'
            '<rect x="-330" y="410" width="660" height="70" rx="14" fill="#37474f"/>'
            '<circle cx="-220" cy="500" r="62" fill="#212121"/><circle cx="-220" cy="500" r="26" fill="#9e9e9e"/>'
            '<circle cx="220" cy="500" r="62" fill="#212121"/><circle cx="220" cy="500" r="26" fill="#9e9e9e"/>'
            '<path d="M-360 450 L-470 470" stroke="#37474f" stroke-width="20" stroke-linecap="round"/>'
            '<defs><clipPath id="kazanic"><path d="M-300 0 L300 0 L240 410 L-240 410 Z"/></clipPath></defs>'
            '<path d="M-300 0 L300 0 L240 410 L-240 410 Z" fill="#fff8e1" stroke="#c62828" stroke-width="12" stroke-linejoin="round"/>'
            '<g clip-path="url(#kazanic)"><g class="yemler"></g>'
            '<rect x="-14" y="30" width="28" height="380" fill="#78909c"/><g class="helezon"></g></g>'
            '<path d="M-300 0 L300 0 L240 410 L-240 410 Z" fill="none" stroke="#c62828" stroke-width="12" stroke-linejoin="round"/>'
            '<rect x="-320" y="-18" width="640" height="30" rx="12" fill="#b71c1c"/>'
            '<text x="0" y="330" text-anchor="middle" font-size="34" font-weight="900" fill="#c62828" opacity=".25">YEM KARMA</text></g>')


def s_ykarma(p):
    A = p.get("_a", {})
    g = zemin_krem()
    g += karma_kazan(520, 640, .85)
    g += pop(hap(430, 560, "Doğrar + karıştırır 🔄", "#2F5737", "#fff", 40), A.get("dograr", 20), 430, 560)
    g += pop(hap(540, 1190, "Her lokmada aynı yem ✅", "#14281A", "#FFD54F", 40), A.get("lokma", 9999), 540, 1190)
    g += U + rozet(1) + dv.baslik("1. FARK", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.02)


def s_ykapanis(p):
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70)])
    g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
    g += '<text x="540" y="400" text-anchor="middle" font-size="46" font-weight="900" fill="#E2B654">HER LOKMA AYNI OLSUN</text>'
    M = [("🔄", "Yem karma"), ("🌾", "Önce kuru ot"), ("⏳", "Uzun karıştırma"), ("🩺", "Rasyon: uzmana")]
    for i, (e, ad) in enumerate(M):
        x, y = 285 + (i % 2) * 470, 500 + (i // 2) * 112
        g += pop(f'<rect x="{x-215}" y="{y-44}" width="430" height="88" rx="44" fill="#fff" filter="url(#golge)"/>' + emo(x - 160, y + 17, e, 42)
                 + f'<text x="{x-115}" y="{y+12}" font-size="32" font-weight="900" fill="#2F5737">{ad}</text>', 4 + i * 5, x, y)
    g += dv.kisi(300, 1770, .95, "kasketli", "salla", "mutlu", "kisi-dayi")
    g += ('<g class="takip" transform="translate(600 860)"><rect class="btn" width="400" height="110" rx="55" fill="#FE2C55" filter="url(#golge)"/>'
          '<text class="btnyazi" x="200" y="74" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">+ Takip et</text><text class="el" x="230" y="200" font-size="110">👆</text></g>')
    g += '<text x="760" y="1200" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">Yorumlara yazın 💬</text>'
    return g, (540, 1100, 1.0, 1.03)


dv.SAHNELER.update({"ydayi": s_ydayi, "y3": s_y3, "ykarma": s_ykarma, "ykapanis": s_ykapanis})

dv.ANIM_EK.update({
    "ydayi": lambda p, kt, n: {"kanca": 12},
    "y3": lambda p, kt, n: {"secer": _kt(kt, "seçiyor", 20) - 2, **{f"k{i}": _kt(kt, "üç", 90) + i * 5 for i in range(3)},
                            "son": _kt(kt, "sonuncusunu", 150) - 2},
    "ykarma": lambda p, kt, n: {"dograr": _kt(kt, "doğrar", 20) - 4, "karis": _kt(kt, "karıştırır", 60) - 4, "lokma": _kt(kt, "her", 120) - 2},
    "ykapanis": lambda p, kt, n: {"tap": _kt(kt, "takip", 40)},
})

dv.JS_EK += r"""
Object.assign(SAHNE,{
 ydayi(el,t){ clouds(el,t); sallan(el,t); balon(el,t); poplar(el,t); },
 y3(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 ykarma(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), K=A.karis??60;
   const sp = t<K ? 0.25 : 1; const ph=t*0.22*sp + (t>=K ? (K*0.22*0.25 - K*0.22) : 0);
   let h=''; for(let i=0;i<7;i++){ const y=60+i*52, s=Math.sin(ph+i*0.9); h+=`<path d="M0 ${y} Q${(150*s).toFixed(1)} ${y+26} 0 ${y+52}" stroke="#455a64" stroke-width="14" fill="none" stroke-linecap="round"/>`; } $('.helezon',el).innerHTML=h;
   const m = Math.max(0, Math.min(1, (t-K)/90)); let y='';
   const R=[['#e8c547',0],['#7cb342',1],['#8d5a2b',2]];
   for(let k=0;k<60;k++){ const c=R[k%3], band=c[1];
     const sy = 300+band*45 + ((k*17)%40), sx = -200+((k*53)%400);
     const ang = k*0.7 + t*0.06*(1+m*3), rr = 60+((k*29)%170), my = 60+((k*41)%330);
     const x = sx*(1-m) + Math.cos(ang)*rr*m, yy = sy*(1-m) + (my + Math.sin(ang)*20)*m;
     y+=`<circle cx="${x.toFixed(1)}" cy="${yy.toFixed(1)}" r="${(10+k%3*3)}" fill="${c[0]}"/>`; }
   $('.yemler',el).innerHTML=y; },
 ykapanis(el,t){ SAHNE.skapanis(el,t); },
});
"""

"""Dayı Soruyor — kış bakımı sahneleri (ilk kullanım: "Traktörü kışa nasıl hazırlarım?" bölümü).
Sahneler: kdayi (karlı dayı sorusu), kgiris (soğuk neyi zorlar), kkontrol (traktör üstünde tek kontrol: antifriz/akü/yakıt/yağ/lastik/park),
kozet (6 maddelik özet), ktepki (karlı tepki). Kullanım: import kis_sahneler (dayi_video'yu genişletir).
kkontrol parametreleri: no (1-6), baslik, renk, prop (antifriz|aku|yakit|yag|lastik|park),
etiketler: [[metin, kelime_koku, renk, x, y, hedef_x, hedef_y], ...]  (hedef = traktör üstündeki nokta, ekran koordinatı).
"""
import dayi_video as dv
import dayi, arka
from cizim import traktor
from toprak_sahneler import pop, hap, kart, emo, tik, zemin_krem, _kt

U = "<!--UST-->"
TX, TY, TS = 330, 1210, 0.72          # traktör yerleşimi (arka teker zemin teması, ölçek)


def tp(lx, ly):
    """Traktörün yerel koordinatını ekran koordinatına çevirir."""
    return round(TX + lx * TS), round(TY + ly * TS)


# önemli noktalar (ekran)
RADYATOR = tp(486, -300)
AKU = tp(430, -235)
DEPO = tp(110, -250)
MOTOR = tp(300, -190)
ARKA_TEKER = tp(0, -165)
ON_TEKER = tp(390, -100)
ASKI = tp(-235, -120)


def kis_arka(zemin=1180):
    g = ('<defs><linearGradient id="k_gok" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb4c6"/><stop offset=".6" stop-color="#d9e3eb"/><stop offset="1" stop-color="#eef3f7"/></linearGradient>'
         '<linearGradient id="k_kar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7fafc"/><stop offset="1" stop-color="#dfe8ef"/></linearGradient></defs>'
         '<rect width="1080" height="1920" fill="url(#k_gok)"/>')
    # uzak tepeler
    g += (f'<path d="M0 {zemin-210} Q160 {zemin-330} 330 {zemin-250} Q520 {zemin-170} 700 {zemin-290} Q880 {zemin-380} 1080 {zemin-240} L1080 {zemin} L0 {zemin} Z" fill="#c9d6e1"/>'
          f'<path d="M0 {zemin-120} Q220 {zemin-210} 470 {zemin-140} Q700 {zemin-80} 1080 {zemin-170} L1080 {zemin} L0 {zemin} Z" fill="#e3ebf1"/>')
    # yapraksız kavaklar
    for x, h in [(70, 300), (150, 250), (940, 330), (1020, 270)]:
        y0 = zemin - 100
        g += f'<path d="M{x} {y0} L{x} {y0-h}" stroke="#6d5a4c" stroke-width="7" stroke-linecap="round"/>'
        g += "".join(f'<path d="M{x} {y0-h*k/6} l{(-1)**k*28} -{36+k*4}" stroke="#6d5a4c" stroke-width="4" stroke-linecap="round"/>' for k in range(1, 6))
        g += f'<ellipse cx="{x}" cy="{y0}" rx="26" ry="7" fill="#fff" opacity=".9"/>'
    # karlı zemin
    g += f'<rect x="0" y="{zemin-60}" width="1080" height="{1980-zemin}" fill="url(#k_kar)"/>'
    g += f'<path d="M0 {zemin-60} Q270 {zemin-90} 540 {zemin-62} Q810 {zemin-36} 1080 {zemin-70}" stroke="#fff" stroke-width="10" fill="none"/>'
    g += "".join(f'<ellipse cx="{(k*131)%1080}" cy="{zemin+40+(k*67)%640}" rx="{40+k%4*22}" ry="{8+k%3*4}" fill="#cfdbe5" opacity=".6"/>' for k in range(18))
    return g


def kar_katmani():
    return '<g class="kar"></g>'


def trk():
    return f'<g transform="translate({TX} {TY}) scale({TS})">{traktor("normal")}</g>'


def no_rozet(no, renk):
    return (f'<g><rect x="50" y="360" width="210" height="96" rx="48" fill="{renk}" filter="url(#golge)"/>'
            f'<text x="155" y="424" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">{no}/6</text></g>')


def etk(x, y, tx, ty, metin, t, renk):
    """cizim.etiket'in pop'lu sürümü + hedefte nabız halkası."""
    w = len(metin) * 24 + 56
    return (f'<path class="ciz" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" data-t="{int(t)}" data-d="10" d="M{x} {y} L{tx} {ty}" stroke="#14281A" stroke-width="6" stroke-linecap="round"/>'
            + f'<circle class="halka" data-t="{int(t)}" cx="{tx}" cy="{ty}" r="18" fill="none" stroke="{renk}" stroke-width="6" opacity="0"/>'
            + pop(f'<circle cx="{tx}" cy="{ty}" r="13" fill="{renk}" stroke="#fff" stroke-width="5"/>', t, tx, ty)
            + pop(f'<rect x="{x-w/2:.0f}" y="{y-38}" width="{w}" height="76" rx="38" fill="#fff" stroke="{renk}" stroke-width="6" filter="url(#golge)"/>'
                  f'<text x="{x}" y="{y+14}" text-anchor="middle" font-size="40" font-weight="900" fill="{renk}">{metin}</text>', t, x, y))


# ---------------------------------------------------------------- props (sağ alt köşe, zemin y≈1180)
def p_antifriz(x=930, y=1185):
    g = (f'<g transform="translate({x} {y})"><ellipse cx="0" cy="6" rx="95" ry="12" fill="#000" opacity=".18"/>'
         '<path d="M-80 0 L-80 -200 Q-80 -230 -50 -236 L20 -236 L20 -262 L54 -262 L54 -236 Q80 -232 80 -200 L80 0 Z" fill="#26a69a" stroke="#00695c" stroke-width="5"/>'
         '<rect x="14" y="-286" width="46" height="30" rx="6" fill="#ffca28" stroke="#c79100" stroke-width="4"/>'
         '<path d="M-60 -220 Q-40 -260 -6 -236" stroke="#00695c" stroke-width="12" fill="none" stroke-linecap="round"/>'
         '<rect x="-66" y="-170" width="132" height="92" rx="10" fill="#fff"/>'
         '<text x="0" y="-130" text-anchor="middle" font-size="25" font-weight="900" fill="#00695c">ANTİFRİZ</text>'
         '<text x="0" y="-94" text-anchor="middle" font-size="36">❄️</text>'
         '<path d="M58 -190 L58 -20" stroke="#fff" stroke-opacity=".35" stroke-width="12" stroke-linecap="round"/></g>')
    return g


def p_termometre(x=960, y=1180, cls="termo"):
    return (f'<g transform="translate({x} {y})"><rect x="-26" y="-330" width="52" height="300" rx="26" fill="#fff" stroke="#90a4ae" stroke-width="5" filter="url(#golge)"/>'
            '<circle cx="0" cy="-30" r="40" fill="#1e88e5" stroke="#90a4ae" stroke-width="5"/>'
            f'<rect class="{cls}" data-h0="230" data-h1="40" x="-12" y="-290" width="24" height="230" rx="12" fill="#1e88e5"/>'
            + "".join(f'<path d="M26 {-300+k*40} h16" stroke="#90a4ae" stroke-width="4"/>' for k in range(7)) +
            '<text x="0" y="-350" text-anchor="middle" font-size="40">❄️</text></g>')


def p_aku(x=910, y=1205):
    return (f'<g transform="translate({x} {y})"><ellipse cx="0" cy="6" rx="110" ry="12" fill="#000" opacity=".18"/>'
            '<rect x="-100" y="-170" width="200" height="170" rx="14" fill="#37474f" stroke="#1c262b" stroke-width="5"/>'
            '<rect x="-100" y="-170" width="200" height="34" rx="12" fill="#546e7a"/>'
            '<rect x="-74" y="-196" width="34" height="28" rx="6" fill="#c62828"/><rect x="40" y="-196" width="34" height="28" rx="6" fill="#212121"/>'
            '<text x="-57" y="-206" text-anchor="middle" font-size="34" font-weight="900" fill="#c62828">+</text><text x="57" y="-204" text-anchor="middle" font-size="40" font-weight="900" fill="#212121">−</text>'
            '<text x="0" y="-92" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">AKÜ</text>'
            '<rect x="-70" y="-62" width="140" height="36" rx="8" fill="#1c262b"/>'
            + "".join(f'<rect class="sarj" data-k="{k}" x="{-64+k*32}" y="-56" width="26" height="24" rx="4" fill="{["#e53935","#fb8c00","#fdd835","#43a047"][k]}" opacity="0"/>' for k in range(4)) + '</g>')


def p_yakit(x=880, y=1080):
    import cizim
    return f'<g class="yakitk">{cizim.kadran(x, y, 108, "yakit")}</g>'


def p_yag(x=900, y=1205):
    return (f'<g transform="translate({x} {y})"><ellipse cx="0" cy="6" rx="120" ry="12" fill="#000" opacity=".18"/>'
            '<path d="M-90 0 L-80 -150 L40 -150 L60 0 Z" fill="#f9a825" stroke="#8d6e00" stroke-width="5"/>'
            '<path d="M40 -140 L120 -200 L128 -190 L52 -120 Z" fill="#f9a825" stroke="#8d6e00" stroke-width="4"/>'
            '<rect x="-56" y="-178" width="60" height="30" rx="6" fill="#8d6e00"/>'
            '<text x="-18" y="-60" text-anchor="middle" font-size="34" font-weight="900" fill="#5d4300">YAĞ</text>'
            '<g class="damla"><path d="M126 -186 q10 18 0 28 q-10 -10 0 -28" fill="#8d6e00"/></g>'
            '<g transform="translate(-150 0)"><rect x="-40" y="-110" width="80" height="110" rx="12" fill="#ef6c00" stroke="#a84300" stroke-width="5"/>'
            '<rect x="-40" y="-110" width="80" height="20" rx="8" fill="#455a64"/>'
            + "".join(f'<path d="M-30 {-80+k*16} h60" stroke="#a84300" stroke-width="4"/>' for k in range(5)) +
            '<text x="0" y="30" text-anchor="middle" font-size="24" font-weight="800" fill="#455a64">FİLTRE</text></g></g>')


def p_lastik(x=920, y=1100):
    return (f'<g transform="translate({x} {y})"><circle r="92" fill="#eceff1" stroke="#455a64" stroke-width="10" filter="url(#golge)"/>'
            '<path d="M-64 30 A70 70 0 1 1 64 30" stroke="#cfd8dc" stroke-width="14" fill="none"/>'
            '<path d="M-64 30 A70 70 0 0 1 -50 -48" stroke="#e53935" stroke-width="14" fill="none"/>'
            '<path d="M50 -48 A70 70 0 0 1 64 30" stroke="#e53935" stroke-width="14" fill="none"/>'
            '<path d="M-50 -48 A70 70 0 0 1 50 -48" stroke="#43a047" stroke-width="14" fill="none"/>'
            '<g class="ibre2"><path d="M-6 0 L0 -62 L6 0 Z" fill="#263238"/></g><circle r="10" fill="#263238"/>'
            '<text y="52" text-anchor="middle" font-size="22" font-weight="800" fill="#455a64">BASINÇ</text>'
            '<path d="M0 92 Q0 150 -60 170" stroke="#263238" stroke-width="12" fill="none" stroke-linecap="round"/></g>')


def p_ahir():
    """Traktörün arkasında kapalı ahır/sundurma (pop'lu)."""
    return ('<rect x="40" y="560" width="900" height="640" fill="#7b3a2c" stroke="#4e2219" stroke-width="8"/>'
            '<rect x="90" y="640" width="800" height="560" fill="#3e2723"/>'
            + "".join(f'<path d="M{90+k*80} 640 V1200" stroke="#4e342e" stroke-width="4"/>' for k in range(11)) +
            '<path d="M0 580 L490 330 L980 580 Z" fill="#5d2b20" stroke="#3e1a12" stroke-width="8" stroke-linejoin="round"/>'
            '<path d="M0 580 L490 330 L980 580" stroke="#fff" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            '<rect x="420" y="470" width="140" height="70" rx="8" fill="#E2B654"/><text x="490" y="520" text-anchor="middle" font-size="34" font-weight="900" fill="#4e2219">AHIR</text>')


PROPLAR = {"antifriz": lambda: p_antifriz(900, 1205), "aku": p_aku, "yakit": p_yakit, "yag": p_yag, "lastik": p_lastik, "park": lambda: ""}


# ---------------------------------------------------------------- sahneler
def s_kdayi(p):
    g = kis_arka()
    g += f'<g transform="translate(560 1150) scale(.42)">{traktor("normal")}</g>'
    g += dv.kisi(900, 1300, .58, "genc", "duz", "normal", "kisi-usta")
    g += dv.kisi(330, 2050, 1.42, "kasketli", "bel", "endise", "kisi-dayi")
    g += kar_katmani()
    g += U + '<g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["?"]), 300, 640, 54) + '</g>'
    return g, (340, 860, 1.0, 1.12)


def s_kgiris(p):
    A = p.get("_a", {})
    g = kis_arka() + trk() + p_termometre(980, 1215) + kar_katmani()
    g += etk(840, 700, *AKU, "Akü", A.get("aku", 40), "#c62828")
    g += etk(820, 800, *MOTOR, "Motor", A.get("motor", 60), "#ef6c00")
    g += etk(170, 1265, *ARKA_TEKER, "Lastik", A.get("lastik", 80), "#14281A")
    g += pop(hap(400, 610, "Kışa girmeden 6 kontrol", "#1565c0", "#fff", 46), A.get("alti", 120), 400, 610)
    g += U + dv.baslik("KIŞ GELDİ ❄", "#1565c0") + dv.pip(925, 460, 110)
    return g, (520, 980, 1.0, 1.05)


def s_kkontrol(p):
    A = p.get("_a", {})
    renk = p.get("renk", "#1565c0")
    g = kis_arka()
    if p.get("prop") == "park":
        g += pop(p_ahir(), A.get("park", 30), 490, 900)
    g += trk() + PROPLAR.get(p.get("prop"), lambda: "")() + kar_katmani()
    for i, e in enumerate(p.get("etiketler", [])):
        metin, _, er, x, y, hx, hy = e
        g += etk(x, y, hx, hy, metin, A.get(f"e{i}", 20 + i * 40), er)
    g += U + no_rozet(p.get("no", 1), renk) + dv.baslik(p.get("baslik", ""), renk) + dv.pip(925, 460, 110)
    return g, (520, 960, 1.0, 1.05)


def s_kozet(p):
    A = p.get("_a", {})
    g = zemin_krem()
    maddeler = [("🧊", "Antifriz", "antifriz"), ("🔋", "Akü ve kutup başları", "aku"), ("⛽", "Depo dolu", "yakit"),
                ("🛢️", "Yağ ve filtre", "yag"), ("🔧", "Lastik ve gres", "lastik"), ("🏠", "Kuru, kapalı park", "park")]
    for i, (e, ad, k) in enumerate(maddeler):
        y = 666 + i * 100
        t = A.get(k, 20 + i * 24)
        icerik = (kart(70, y - 44, 940, 88, "#fff", 44) + emo(150, y + 20, e, 50)
                  + f'<text x="215" y="{y+15}" font-size="42" font-weight="900" fill="#2F5737">{ad}</text>'
                  + pop(tik(950, y, 30, True), t + 8, 950, y))
        g += pop(icerik, t, 540, y)
    g += pop('<text x="540" y="1252" text-anchor="middle" font-size="36" font-weight="800" fill="#7a6a48">📘 Değerler için kullanım kılavuzuna bak</text>', A.get("kilavuz", 200), 540, 1240)
    g += U + dv.baslik("ÖZETLE", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.02)


def s_ktepki(p):
    g = kis_arka()
    g += dv.kisi(820, 1420, .8, "genc", "basparmak", "mutlu", "kisi-usta")
    g += dv.kisi(300, 1700, 1.1, "kasketli", "basparmak", "mutlu", "kisi-dayi")
    g += kar_katmani()
    g += U + '<g class="balon" data-x="540" data-y="380">' + dayi.balon(60, 230, 960, 280, p.get("balon", ["?"]), 280, 600, 58) + '</g>'
    return g, (540, 1100, 1.1, 1.0)


dv.SAHNELER.update({"kdayi": s_kdayi, "kgiris": s_kgiris, "kkontrol": s_kkontrol, "kozet": s_kozet, "ktepki": s_ktepki})


def _kontrol_anim(p, kt, n):
    a = {}
    for i, e in enumerate(p.get("etiketler", [])):
        a[f"e{i}"] = _kt(kt, e[1], 20 + i * 40) - 2
    if p.get("prop") == "park":
        a["park"] = _kt(kt, "kapalı", 30) - 6
    a["dolu"] = _kt(kt, "dolu", 40)
    a["sarj"] = _kt(kt, "şarjını", 80)
    a["basinc"] = _kt(kt, "basıncına", 30)
    return a


dv.ANIM_EK.update({
    "kgiris": lambda p, kt, n: {"aku": _kt(kt, "aküyü", 40) - 2, "motor": _kt(kt, "motoru", 60) - 2, "lastik": _kt(kt, "lastiği", 80) - 2, "alti": _kt(kt, "altı", 120) - 2},
    "kkontrol": _kontrol_anim,
    "kozet": lambda p, kt, n: {"antifriz": _kt(kt, "antifriz", 20) - 4, "aku": _kt(kt, "akü", 40) - 4, "yakit": _kt(kt, "yakıt", 60) - 4, "yag": _kt(kt, "yağ", 80) - 4,
                               "lastik": _kt(kt, "lastik", 100) - 4, "park": _kt(kt, "kapalı", 120) - 4, "kilavuz": _kt(kt, "kullanım", 200) - 4},
})

dv.JS_EK += r"""
function kar(el,t){ const k=$('.kar',el); if(!k) return; let s=''; for(let i=0;i<70;i++){ const sp=1.2+(i%5)*0.45, x=((i*137.5)%1080)+Math.sin(t*0.05+i)*24, y=((i*263)%1920 + t*sp)%1960-20;
  s+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${3+i%4*1.6}" fill="#fff" opacity="${(0.55+0.4*((i*7)%10)/10).toFixed(2)}"/>`; } k.innerHTML=s; }
function halkalar(el,t){ $$('.halka',el).forEach(h=>{ const d=t-(+h.dataset.t); if(d<6){ h.setAttribute('opacity',0); return; } const p=((d-6)%30)/30; h.setAttribute('r',(18+p*40).toFixed(1)); h.setAttribute('opacity',(1-p).toFixed(2)); }); }
Object.assign(SAHNE,{
 kdayi(el,t){ kar(el,t); sallan(el,t); balon(el,t); },
 ktepki(el,t){ SAHNE.tepki(el,t); kar(el,t); },
 kgiris(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); halkalar(el,t); const m=$('.termo',el); if(m){ const e=ease(t/40), h=230-190*e; m.setAttribute('y',-60-h); m.setAttribute('height',h); } },
 kkontrol(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); halkalar(el,t); const A=JSON.parse(el.dataset.a||'{}');
   const m=$('.termo2',el); if(m){ const e=ease(t/30), h=230-190*e; m.setAttribute('y',-60-h); m.setAttribute('height',h); }
   $$('.sarj',el).forEach(s=>{ const k=+s.dataset.k; s.setAttribute('opacity', t>=(A.sarj??80)+k*6 ? 1 : 0.12); });
   const ib=$('.yakitk .ibre',el); if(ib){ const e=ease((t-(A.dolu??40))/24); ib.setAttribute('transform',`rotate(${(-80+160*e).toFixed(1)})`); }
   const ib2=$('.ibre2',el); if(ib2){ const e=ease((t-(A.basinc??30))/20); ib2.setAttribute('transform',`rotate(${(-110+110*e+Math.sin(t*0.3)*3).toFixed(1)})`); }
   const dm=$('.damla',el); if(dm){ const p=(t%24)/24; dm.setAttribute('transform',`translate(0 ${(p*60).toFixed(1)})`); dm.setAttribute('opacity',(1-p).toFixed(2)); } },
 kozet(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
});
"""

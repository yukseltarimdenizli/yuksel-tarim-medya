"""Dayı Soruyor — ek sahne kütüphanesi (ilk kullanım: Toprak analizi bölümü).
Sahneler: dayi (proplu dayı sorusu), lab, rapor, karsilastir, zaman, harita, kacin, karistir, teslim, muhendis, takvim, ozet.
Zamanlanan her öğe .pop (data-t = kare) ya da .ciz (yol çizimi, data-t/data-d) olarak işaretlenir; kareler seslendirmedeki
kelimelerden gelir (ANIM_EK). Kullanım: import toprak_sahneler (dayi_video.SAHNELER/JS_EK/ANIM_EK'i genişletir).
"""
import math
import dayi_video as dv
import usta, arka, dayi
from cizim import teker

U = "<!--UST-->"


# ---------------------------------------------------------------- yardımcılar
def pop(icerik, t, x, y, ek=""):
    return f'<g class="pop" data-t="{int(t)}" data-x="{x}" data-y="{y}" opacity="0" {ek}>{icerik}</g>'


def hap(x, y, metin, renk="#2F5737", yazi="#fff", fs=40, w=None):
    w = w or len(metin) * fs * 0.58 + 70
    return (f'<rect x="{x-w/2:.0f}" y="{y-fs*0.95:.0f}" width="{w:.0f}" height="{fs*1.9:.0f}" rx="{fs*0.95:.0f}" fill="{renk}" filter="url(#golge)"/>'
            f'<text x="{x}" y="{y+fs*0.36:.0f}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="{yazi}">{metin}</text>')


def kart(x, y, w, h, fill="#fff", rx=30, ek=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" filter="url(#golge)" {ek}/>'


def emo(x, y, e, fs=110):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{fs}">{e}</text>'


def tik(x, y, r=30, ok=True):
    if ok:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#43a047" stroke="#fff" stroke-width="5"/>'
                f'<path d="M{x-r*.45} {y} L{x-r*.1} {y+r*.35} L{x+r*.5} {y-r*.35}" stroke="#fff" stroke-width="{r*.24:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e53935" stroke="#fff" stroke-width="5"/>'
            f'<path d="M{x-r*.38} {y-r*.38} L{x+r*.38} {y+r*.38} M{x+r*.38} {y-r*.38} L{x-r*.38} {y+r*.38}" stroke="#fff" stroke-width="{r*.24:.0f}" stroke-linecap="round"/>')


def zemin_krem():
    return ('<rect width="1080" height="1920" fill="#F7F1E3"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#efe5cc"/>' for x, y, r in [(120, 1320, 90), (980, 1300, 140), (1000, 240, 60), (90, 420, 70)]))


def cuval(x, y, s=1.0, yazi="GÜBRE"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M-90 0 Q-104 -140 -70 -230 Q-40 -250 0 -246 Q40 -250 70 -230 Q104 -140 90 0 Z" fill="#f2ead6" stroke="#9c8a62" stroke-width="5"/>'
            '<path d="M-56 -232 Q0 -268 56 -232 L40 -262 Q0 -280 -40 -262 Z" fill="#e2d6b5" stroke="#9c8a62" stroke-width="4"/>'
            '<path d="M-44 -246 Q0 -232 44 -246" stroke="#7a5f3a" stroke-width="7" fill="none"/>'
            '<path d="M60 -40 Q80 -120 58 -200" stroke="#000" stroke-opacity=".12" stroke-width="16" fill="none"/>'
            f'<rect x="-66" y="-170" width="132" height="64" rx="8" fill="#2F5737"/><text x="0" y="-126" text-anchor="middle" font-size="30" font-weight="900" fill="#E2B654">{yazi}</text>'
            '<text x="0" y="-60" text-anchor="middle" font-size="26" font-weight="800" fill="#7a6a48">50 kg</text></g>')


def bugday(x, y, h, renk="#c9a227", yaprak="#8bbd4a", saglikli=True):
    g = f'<path d="M{x} {y} Q{x+4} {y-h*.5} {x} {y-h}" stroke="{yaprak}" stroke-width="{6 if saglikli else 4}" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M{x} {y-h*.35} q{h*.2} -{h*.12} {h*.3} -{h*.28}" stroke="{yaprak}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    for k in range(5 if saglikli else 3):
        yy = y - h - k * 14
        g += f'<ellipse cx="{x-7}" cy="{yy}" rx="7" ry="11" fill="{renk}" transform="rotate(-25 {x-7} {yy})"/><ellipse cx="{x+7}" cy="{yy}" rx="7" ry="11" fill="{renk}" transform="rotate(25 {x+7} {yy})"/>'
    return g


def para(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><circle r="30" fill="#f6c343" stroke="#b8860b" stroke-width="5"/>'
            '<circle r="20" fill="none" stroke="#b8860b" stroke-width="3"/><text y="10" text-anchor="middle" font-size="28" font-weight="900" fill="#8a6100">₺</text></g>')


# ---------------------------------------------------------------- sahneler
def s_dayi(p):
    """Dayı sorusu; p['balon'] satırları, p['prop']: gubre | kurek | rapor | None."""
    g = arka.manzara()
    g += dv.kisi(870, 1290, .6, "genc", "duz", "normal", "kisi-usta")
    prop = p.get("prop")
    poz = "isaret" if prop == "rapor" else "bel"
    if prop == "gubre":
        g += cuval(640, 1260, 1.05)
    if prop == "kurek":
        g += ('<g transform="translate(640 1270) rotate(8)"><rect x="-9" y="-470" width="18" height="400" rx="8" fill="#a0784f"/>'
              '<rect x="-34" y="-500" width="68" height="34" rx="14" fill="#6d4c41"/>'
              '<path d="M-60 -80 L60 -80 L50 10 Q0 50 -50 10 Z" fill="url(#metal)" stroke="#55656d" stroke-width="4"/></g>')
    g += dv.kisi(330, 2050, 1.42, "kasketli", poz, "endise", "kisi-dayi")
    if prop == "rapor":
        g += ('<g transform="translate(790 1020) rotate(10)"><rect x="-90" y="-120" width="180" height="230" rx="10" fill="#fff" stroke="#9aa5ad" stroke-width="4" filter="url(#golge)"/>'
              '<text x="0" y="-78" text-anchor="middle" font-size="22" font-weight="900" fill="#2F5737">ANALİZ</text>'
              + "".join(f'<rect x="-66" y="{-50+k*34}" width="{60+((k*37)%60)}" height="14" rx="7" fill="{["#43a047","#e53935","#43a047","#fb8c00","#43a047"][k]}"/>' for k in range(5)) + '</g>')
    g += U + '<g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["?"]), 300, 640, 56) + '</g>'
    return g, (340, 860, 1.0, 1.12)


def s_lab(p):
    A = p.get("_a", {})
    g = ('<defs><linearGradient id="t_duvar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9f2f6"/><stop offset="1" stop-color="#cfe0e8"/></linearGradient></defs>'
         '<rect width="1080" height="1920" fill="url(#t_duvar)"/>'
         + "".join(f'<path d="M0 {y} H1080" stroke="#bcd0da" stroke-width="2"/>' for y in range(360, 1100, 90))
         + "".join(f'<path d="M{x} 360 V1100" stroke="#bcd0da" stroke-width="2"/>' for x in range(60, 1080, 120)))
    # raf ve şişeler
    g += '<rect x="60" y="430" width="300" height="16" rx="6" fill="#8d6e63"/>' + "".join(
        f'<rect x="{80+k*70}" y="{350-(k%2)*20}" width="44" height="{80+(k%2)*20}" rx="10" fill="{c}" opacity=".85"/><rect x="{92+k*70}" y="{336-(k%2)*20}" width="20" height="18" rx="4" fill="#546e7a"/>'
        for k, c in enumerate(["#ffcc80", "#a5d6a7", "#90caf9", "#ce93d8"]))
    # tezgâh
    g += ('<rect x="0" y="1100" width="1080" height="40" fill="#eceff1"/><rect x="0" y="1100" width="1080" height="8" fill="#fff"/>'
          '<rect x="0" y="1140" width="1080" height="780" fill="#b0bec5"/>'
          + "".join(f'<rect x="{x}" y="1170" width="240" height="160" rx="10" fill="#c5d1d7" stroke="#90a4ae" stroke-width="3"/><rect x="{x+100}" y="1240" width="40" height="10" rx="5" fill="#78909c"/>' for x in (30, 290, 550, 810)))
    # toprak kavanozu + "..."
    g += ('<g transform="translate(200 1100)"><rect x="-80" y="-200" width="160" height="200" rx="26" fill="#e3f2fd" fill-opacity=".55" stroke="#90a4ae" stroke-width="5"/>'
          '<path d="M-74 -110 Q0 -126 74 -110 L74 -26 Q74 -6 54 -6 L-54 -6 Q-74 -6 -74 -26 Z" fill="#6f4b2c"/>'
          + "".join(f'<circle cx="{-50+k*22}" cy="{-80+(k*13)%60}" r="{5+k%3*2}" fill="#4f3520"/>' for k in range(6)) +
          '<rect x="-88" y="-226" width="176" height="34" rx="10" fill="#546e7a"/><rect x="-60" y="-150" width="120" height="34" rx="6" fill="#fff"/>'
          '<text y="-125" text-anchor="middle" font-size="22" font-weight="800" fill="#5d4037">NUMUNE</text></g>')
    pass
    # tüp rafı
    g += '<g transform="translate(470 1100)"><rect x="-120" y="-70" width="240" height="70" rx="10" fill="#a1887f"/><rect x="-120" y="-90" width="240" height="24" rx="8" fill="#8d6e63"/>'
    for k, c in enumerate(["#ffb74d", "#fff176", "#81c784", "#64b5f6", "#f48fb1"]):
        x = -96 + k * 48
        g += (f'<rect x="{x-14}" y="-250" width="28" height="200" rx="14" fill="#fff" fill-opacity=".6" stroke="#90a4ae" stroke-width="3"/>'
              f'<rect class="sivi" data-k="{k}" x="{x-11}" y="-140" width="22" height="88" rx="10" fill="{c}"/>')
    g += '</g>'
    # pH ölçer
    g += ('<g transform="translate(800 1100)"><rect x="-110" y="-200" width="190" height="200" rx="22" fill="#37474f"/><rect x="-90" y="-180" width="150" height="80" rx="10" fill="#c8e6c9"/>'
          '<text x="-15" y="-124" text-anchor="middle" font-size="40" font-weight="900" fill="#1b5e20" font-family="monospace">pH</text>'
          '<circle cx="-50" cy="-50" r="16" fill="#90a4ae"/><circle cx="20" cy="-50" r="16" fill="#90a4ae"/>'
          '<path d="M80 -150 Q140 -150 150 -60" stroke="#263238" stroke-width="7" fill="none"/>'
          '<path d="M120 -110 L180 -110 L196 0 L104 0 Z" fill="#e3f2fd" fill-opacity=".6" stroke="#90a4ae" stroke-width="4"/><path d="M110 -50 L190 -50 L196 0 L104 0 Z" fill="#a1887f" opacity=".8"/>'
          '<rect x="142" y="-170" width="16" height="140" rx="8" fill="#263238"/></g>')
    # değer etiketleri (söylendikçe)
    chips = [("pH", "ph", 270, 600), ("Tuz", "tuz", 650, 600), ("Kireç", "kireç", 270, 720), ("Organik madde", "organik", 650, 720), ("Fosfor", "fosfor", 270, 840), ("Potasyum", "potasyum", 650, 840)]
    for i, (ad, k, x, y) in enumerate(chips):
        g += pop(hap(x, y, ad, ["#1565c0", "#00838f", "#6d4c41", "#2e7d32", "#c62828", "#6a1b9a"][i], fs=40), A.get(k, 60 + i * 20), x, y)
    g += U + dv.baslik("LABORATUVAR", "#1565c0") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.05)


def s_rapor(p):
    A = p.get("_a", {})
    g = zemin_krem()
    g += '<g transform="rotate(-2 470 800)">' + kart(110, 380, 720, 860, "#fff", 24)
    g += ('<rect x="110" y="380" width="720" height="110" rx="24" fill="#2F5737"/><rect x="110" y="450" width="720" height="40" fill="#2F5737"/>'
          '<text x="470" y="452" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">TOPRAK ANALİZ RAPORU</text>')
    satir = [("pH", .55, "uygun"), ("Tuz", .35, "uygun"), ("Kireç", .6, "uygun"), ("Organik madde", .4, "uygun"), ("Fosfor", .15, "eksik"), ("Potasyum", .92, "fazla")]
    for i, (ad, oran, dur) in enumerate(satir):
        y = 560 + i * 108
        renk = {"uygun": "#43a047", "eksik": "#e53935", "fazla": "#fb8c00"}[dur]
        g += (f'<text x="150" y="{y+12}" font-size="34" font-weight="800" fill="#263238">{ad}</text>'
              f'<rect x="420" y="{y-14}" width="250" height="30" rx="15" fill="#eceff1"/>'
              f'<rect class="cubuk" data-t="{8+i*5}" data-w="{250*oran:.0f}" x="420" y="{y-14}" width="0" height="30" rx="15" fill="{renk}"/>')
        if dur == "uygun":
            g += pop(f'<text x="752" y="{y+11}" text-anchor="middle" font-size="26" font-weight="900" fill="#2e7d32">UYGUN</text>', 20 + i * 5, 752, y)
        else:
            t = A.get("eksik", 50) if dur == "eksik" else A.get("fazla", 80)
            g += pop(f'<rect x="690" y="{y-26}" width="124" height="54" rx="27" fill="{renk}"/><text x="752" y="{y+12}" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">{dur.upper()}</text>', t, 752, y)
    g += '<path d="M150 1200 H500" stroke="#b0bec5" stroke-width="4"/><text x="150" y="1180" font-size="22" fill="#90a4ae">Örnek rapor görünümüdür</text></g>'
    g += U + dv.pip(925, 460, 110)
    return g, (470, 800, 1.0, 1.04)


def s_karsilastir(p):
    A = p.get("_a", {})
    g = zemin_krem()

    def panel(x0, baslik, renk, sag):
        h = kart(x0, 660, 480, 600, "#fff", 28)
        h += f'<rect x="{x0}" y="660" width="480" height="90" rx="28" fill="{renk}"/><rect x="{x0}" y="720" width="480" height="30" fill="{renk}"/>'
        h += f'<text x="{x0+240}" y="722" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">{baslik}</text>'
        h += f'<rect x="{x0+20}" y="1120" width="440" height="70" rx="14" fill="#8a6440"/><rect x="{x0+20}" y="1114" width="440" height="12" rx="6" fill="#6b9a3e"/>'
        if not sag:
            h += cuval(x0 + 110, 1120, .5) + cuval(x0 + 190, 1120, .5) + cuval(x0 + 150, 1000, .5) + cuval(x0 + 70, 1000, .45)
            h += "".join(bugday(x0 + 290 + k * 30, 1120, 90 + (k % 2) * 12, "#d8c37a", "#b5b56a", False) for k in range(6))
            h += '<g class="ucanpara"></g>'
        else:
            h += cuval(x0 + 110, 1120, .5)
            h += "".join(para(x0 + 220, 1100 - k * 18, .8) for k in range(4))
            h += "".join(bugday(x0 + 290 + k * 30, 1120, 210 + (k % 3) * 14) for k in range(6))
        return h
    g += pop(panel(40, "GÖZ KARARI", "#c62828", False), 4, 280, 960)
    g += pop(panel(560, "ANALİZLE", "#2e7d32", True), A.get("analiz", 120), 800, 960)
    g += pop(hap(690, 1214, "💰 Masraf ↓", "#14281A", "#FFD54F", 34), A.get("masraf", 180), 690, 1214)
    g += pop(hap(915, 1214, "🌾 Verim ↑", "#14281A", "#FFD54F", 34, 200), A.get("verim", 210), 915, 1214)
    g += U + dv.baslik("Göz kararı mı, analiz mi?", "#14281A", "#FFD54F", 760) + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.03)


def s_zaman(p):
    A = p.get("_a", {})
    g = zemin_krem()
    tak = ('<g transform="translate(150 410)"><rect width="200" height="190" rx="20" fill="#fff" stroke="#b0bec5" stroke-width="4" filter="url(#golge)"/>'
           '<rect width="200" height="56" rx="20" fill="#c62828"/><rect y="36" width="200" height="20" fill="#c62828"/>'
           '<rect x="44" y="-16" width="16" height="40" rx="8" fill="#455a64"/><rect x="140" y="-16" width="16" height="40" rx="8" fill="#455a64"/>'
           + "".join(f'<rect x="{22+c*40}" y="{76+r*36}" width="26" height="22" rx="5" fill="{"#43a047" if (r,c) in ((1,2),(2,0)) else "#eceff1"}"/>' for r in range(3) for c in range(4)) + '</g>')
    g += pop(tak, 2, 250, 505)
    g += pop(f'<text x="400" y="500" font-size="56" font-weight="900" fill="#2F5737">Numune</text><text x="400" y="566" font-size="56" font-weight="900" fill="#2F5737">ne zaman?</text>', 4, 560, 520)

    def k(x, y, w, h, e, ad, ok):
        return (kart(x, y, w, h, "#fff", 26) + emo(x + w / 2, y + h * .55, e, 100 if w > 350 else 84)
                + f'<text x="{x+w/2}" y="{y+h-26}" text-anchor="middle" font-size="{36 if w > 350 else 32}" font-weight="900" fill="#263238">{ad}</text>' + tik(x + w - 30, y + 30, 30, ok))
    g += pop(k(60, 660, 450, 290, "🌾", "Hasattan sonra", True), A.get("hasat", 20), 285, 805)
    g += pop(k(570, 660, 450, 290, "🌱", "Ekimden önce", True), A.get("ekim", 50), 795, 805)
    g += pop(k(40, 990, 320, 250, "🌧️", "Çok ıslak", False), A.get("islak", 110), 200, 1115)
    g += pop(k(380, 990, 320, 250, "☀️", "Çok kuru", False), A.get("kuru", 125), 540, 1115)
    g += pop(k(720, 990, 320, 250, "❄️", "Donmuş", False), A.get("donmus", 140), 880, 1115)
    g += U + dv.baslik("NE ZAMAN?", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.03)


NOKTALAR = [(250, 560), (360, 900), (470, 640), (560, 980), (640, 700), (720, 1040), (780, 760), (880, 1000), (900, 720), (470, 1100), (300, 1060), (180, 820)]
TARLA = (80, 420, 1000, 1170)


def _harita(kenarlar=True):
    x0, y0, x1, y1 = TARLA
    g = '<rect width="1080" height="1920" fill="#9cc46c"/>' + "".join(f'<circle cx="{(k*137)%1080}" cy="{(k*91)%1500+300}" r="{6+k%4}" fill="#86b25a"/>' for k in range(60))
    g += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="14" fill="#8a6440" stroke="#5d7f35" stroke-width="10"/>'
    g += "".join(f'<path d="M{x0+10} {y} H{x1-10}" stroke="#6f4b2c" stroke-width="12" opacity=".55"/>' for y in range(y0 + 30, y1, 42))
    g += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" filter="url(#a_doku)" opacity=".5"/>'
    # yol (alt), ağaç (sol alt), gübre yığını (sağ alt)
    g += ('<rect x="0" y="1196" width="1080" height="90" fill="#9e9e9e"/><path d="M0 1241 H1080" stroke="#fff" stroke-width="6" stroke-dasharray="40 30"/>'
          '<g transform="translate(140 1110)"><circle r="96" fill="#2f6b2a" opacity=".35"/><circle cx="-30" cy="-20" r="58" fill="#3f7d36"/><circle cx="34" cy="-10" r="62" fill="#4c8c3f"/><circle cx="0" cy="30" r="56" fill="#3a7433"/><circle cx="-10" cy="-30" r="22" fill="#6fae52" opacity=".6"/></g>'
          '<g transform="translate(880 1090)"><ellipse rx="96" ry="56" fill="#4a3220"/><ellipse cx="-20" cy="-14" rx="60" ry="32" fill="#5d4027"/><ellipse cx="-30" cy="-26" rx="24" ry="10" fill="#7a5634" opacity=".7"/></g>')
    return g


def s_harita(p):
    A = p.get("_a", {})
    g = _harita()
    yol = "M" + " L".join(f"{x} {y}" for x, y in NOKTALAR)
    g += f'<path class="ciz" data-t="{A.get("nokta0", 10)}" data-d="{A.get("noktad", 70)}" pathLength="1" d="{yol}" stroke="#fff" stroke-width="6" stroke-dasharray="1 1" stroke-dashoffset="1" fill="none" opacity=".8"/>'
    t0, d = A.get("nokta0", 10), A.get("noktad", 70)
    for i, (x, y) in enumerate(NOKTALAR):
        g += pop(f'<circle cx="{x}" cy="{y}" r="26" fill="#ff7043" stroke="#fff" stroke-width="6"/><text x="{x}" y="{y+10}" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">{i+1}</text>',
                 t0 + d * i / len(NOKTALAR), x, y)
    g += pop(hap(600, 540, "10-15 farklı nokta", "#ff7043", "#fff", 40), A.get("on", 30), 600, 540)
    # kesit penceresi (derinlik)
    kes = ('<g>' + kart(560, 820, 420, 330, "#fff", 24) +
           '<rect x="580" y="900" width="380" height="230" rx="12" fill="#7a5634"/><rect x="580" y="900" width="380" height="14" fill="#6b9a3e"/>'
           '<path d="M700 914 L760 1060 L820 914 Z" fill="#3e2a17"/><rect x="756" y="914" width="10" height="140" fill="#a1795a"/>'
           '<rect x="860" y="914" width="40" height="190" rx="6" fill="#fff8e1" stroke="#8d6e63" stroke-width="3"/>'
           + "".join(f'<path d="M860 {914+k*45} h18" stroke="#5d4037" stroke-width="4"/>' for k in range(5)) +
           '<path d="M690 914 L690 1060" stroke="#FFD54F" stroke-width="5" stroke-dasharray="10 8"/>'
           '<text x="770" y="870" text-anchor="middle" font-size="40" font-weight="900" fill="#c62828">20-30 cm</text></g>')
    g += pop(kes, A.get("derin", 110), 770, 985)
    g += U + dv.baslik("NASIL ALINIR?", "#ff7043") + dv.pip(925, 460, 110)
    return g, (540, 800, 1.0, 1.04)


def s_kacin(p):
    A = p.get("_a", {})
    g = _harita()
    g += '<g opacity=".35">' + "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="#ff7043" stroke="#fff" stroke-width="5"/>' for x, y in NOKTALAR) + '</g>'

    def isaret(x, y, r, ad, lx, ly):
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#e53935" stroke-width="10" stroke-dasharray="20 10"/>' + tik(x + r * .7, y - r * .7, 30, False)
                + hap(lx, ly, ad, "#e53935", "#fff", 38))
    g += pop(isaret(540, 1180, 120, "Tarla kenarı", 540, 1010), A.get("kenar", 6), 540, 1100)
    g += pop(isaret(140, 1110, 120, "Ağaç altı", 300, 900), A.get("agac", 35), 160, 1060)
    g += pop(isaret(880, 1090, 120, "Gübre yığını", 790, 880), A.get("gubre", 65), 860, 1040)
    g += U + dv.baslik("BURALARDAN ALMA!", "#e53935") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.04)


def s_karistir(p):
    A = p.get("_a", {})
    g = zemin_krem() + '<rect x="0" y="1180" width="1080" height="740" fill="#e6dcc3"/>'
    # kova
    g += ('<g transform="translate(330 1170)"><ellipse cx="0" cy="8" rx="210" ry="26" fill="#000" opacity=".15"/>'
          '<path d="M-190 -330 L-150 0 L150 0 L190 -330 Z" fill="#1e88e5"/><path d="M-190 -330 L-150 0 L-110 0 L-146 -330 Z" fill="#1565c0" opacity=".6"/>'
          '<path d="M150 -330 L190 -330 L150 0 L120 0 Z" fill="#0d47a1" opacity=".35"/>'
          '<ellipse cx="0" cy="-330" rx="190" ry="44" fill="#1976d2"/><ellipse cx="0" cy="-326" rx="170" ry="36" fill="#6f4b2c"/>'
          + "".join(f'<circle cx="{-120+k*40}" cy="{-326+(k*17)%24-10}" r="{8+k%3*3}" fill="#4f3520"/>' for k in range(7)) +
          '<path d="M-186 -300 Q0 -520 186 -300" stroke="#90a4ae" stroke-width="10" fill="none"/>'
          '<rect x="-170" y="-200" width="340" height="16" fill="#fff" opacity=".25"/></g>'
          '<g class="karistirici" data-cx="330" data-cy="844"><rect x="320" y="620" width="20" height="260" rx="10" fill="#a0784f" transform="rotate(18 330 844)"/></g>')
    g += pop(hap(330, 1228, "Temiz plastik kova", "#1565c0", "#fff", 34), A.get("kova", 30), 330, 1260)
    # taş/kesek ayıklama
    g += '<g class="taslar" opacity="0">' + "".join(f'<ellipse cx="{560+k*30}" cy="{1150-(k%2)*16}" rx="{18+k%3*6}" ry="{12+k%2*5}" fill="{["#9e9e9e","#5d4027","#bdbdbd","#4a3220"][k%4]}"/>' for k in range(5)) + '</g>'
    g += pop(hap(620, 1080, "Taş · kesek ✗", "#e53935", "#fff", 30), A.get("tas", 90), 620, 1080)
    # poşet
    g += ('<g transform="translate(830 1170)"><path d="M-130 0 L-118 -400 Q0 -420 118 -400 L130 0 Z" fill="#e3f2fd" fill-opacity=".55" stroke="#90a4ae" stroke-width="5"/>'
          '<clipPath id="poset"><path d="M-128 -2 L-117 -396 Q0 -416 117 -396 L128 -2 Z"/></clipPath>'
          '<g clip-path="url(#poset)"><rect class="dolum" x="-140" y="0" width="280" height="0" fill="#6f4b2c"/></g>'
          '<path d="M-118 -400 Q0 -380 118 -400" stroke="#90a4ae" stroke-width="5" fill="none"/></g>')
    g += pop(hap(830, 700, "1 kg", "#6f4b2c", "#fff", 46, 170), A.get("kilo", 140), 830, 700)
    # etiket
    et = ('<g transform="translate(830 920) rotate(-6)"><rect x="-110" y="-90" width="220" height="190" rx="12" fill="#fffde7" stroke="#c8b46a" stroke-width="4" filter="url(#golge)"/>'
          '<circle cx="-84" cy="-64" r="8" fill="#c8b46a"/>')
    for i, (ad, k) in enumerate([("Ad", "adini"), ("Yer", "yerini"), ("Ürün", "urunu")]):
        y = -34 + i * 52
        et += f'<text x="-90" y="{y+8}" font-size="28" font-weight="900" fill="#5d4037">{ad}:</text><path class="ciz" data-t="{A.get(k, 170+i*12)}" data-d="10" pathLength="1" d="M-14 {y} q20 -12 40 0 t40 0 t40 0" stroke="#1565c0" stroke-width="5" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
    et += '</g>'
    g += pop(et, A.get("etiket", 160), 830, 920)
    g += U + dv.baslik("KARIŞTIR · POŞETLE", "#6f4b2c") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.03)


def s_teslim(p):
    A = p.get("_a", {})
    g = arka.manzara()
    g += ('<g transform="translate(560 1170)"><rect x="0" y="-460" width="470" height="460" fill="#f5f5f5"/><rect x="330" y="-460" width="140" height="460" fill="#e0e0e0"/>'
          '<rect x="-14" y="-484" width="498" height="34" fill="#90a4ae"/>'
          + "".join(f'<rect x="{30+c*110}" y="{-420+r*120}" width="80" height="80" rx="6" fill="#81d4fa" stroke="#fff" stroke-width="6"/>' for r in range(2) for c in range(4)) +
          '<rect x="170" y="-170" width="130" height="170" fill="#5d4037"/><rect x="180" y="-160" width="50" height="150" fill="#81d4fa" opacity=".6"/><rect x="240" y="-160" width="50" height="150" fill="#81d4fa" opacity=".6"/>'
          '<rect x="20" y="-620" width="430" height="130" rx="16" fill="#1565c0" filter="url(#golge)"/>'
          '<text x="235" y="-566" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">TOPRAK ANALİZ</text>'
          '<text x="235" y="-516" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">LABORATUVARI</text>'
          '<rect x="140" y="-490" width="10" height="40" fill="#78909c"/><rect x="320" y="-490" width="10" height="40" fill="#78909c"/></g>')
    g += ('<g class="tasinan" data-t0="' + str(A.get("yola", 10)) + '" data-t1="' + str(A.get("var", 80)) + '">'
          '<g transform="translate(0 0)"><path d="M-60 0 L-52 -120 Q0 -130 52 -120 L60 0 Z" fill="#e3f2fd" fill-opacity=".7" stroke="#90a4ae" stroke-width="4"/>'
          '<path d="M-58 -2 L-54 -70 Q0 -78 54 -70 L58 -2 Z" fill="#6f4b2c"/><rect x="-36" y="-110" width="72" height="44" rx="6" fill="#fffde7" stroke="#c8b46a" stroke-width="3"/>'
          '<text y="-80" text-anchor="middle" font-size="18" font-weight="900" fill="#5d4037">NUMUNE</text></g></g>')
    g += pop(tik(860, 960, 46, True), A.get("var", 80) + 6, 860, 960)
    g += U + dv.baslik("LABORATUVARA", "#1565c0") + dv.pip(155, 460, 110)
    return g, (600, 1000, 1.0, 1.05)


def s_muhendis(p):
    A = p.get("_a", {})
    g = zemin_krem() + '<rect x="0" y="1250" width="1080" height="670" fill="#e6dcc3"/>'
    g += dv.kisi(250, 1330, .8, "muhendis", "isaret", "mutlu", "kisi-muh")
    g += dayi.isim(250, 1300, "Ziraat Mühendisi", "#1565c0")
    plan = (kart(510, 650, 520, 560, "#fff", 26) + '<rect x="510" y="650" width="520" height="100" rx="26" fill="#2F5737"/><rect x="510" y="720" width="520" height="30" fill="#2F5737"/>'
            '<text x="770" y="716" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">GÜBRE PLANI</text>'
            '<g transform="translate(560 790)"><rect width="150" height="190" rx="10" fill="#f5f5f5" stroke="#b0bec5" stroke-width="3"/>'
            + "".join(f'<rect x="18" y="{30+k*30}" width="{60+((k*29)%50)}" height="12" rx="6" fill="{["#43a047","#43a047","#43a047","#43a047","#e53935"][k]}"/>' for k in range(5)) +
            '<text x="75" y="22" text-anchor="middle" font-size="16" font-weight="900" fill="#2F5737">RAPOR</text></g>'
            '<text x="740" y="850" font-size="30" font-weight="800" fill="#455a64">Rapora göre</text><text x="740" y="892" font-size="30" font-weight="800" fill="#455a64">ölçülü gübre</text>')
    g += pop(plan, A.get("rapor", 10), 770, 930)
    g += pop(tik(580, 1060, 30, True) + '<text x="630" y="1072" font-size="38" font-weight="900" fill="#2e7d32">Eksik olanı ver</text>', A.get("eksik", 120), 760, 1060)
    g += pop(tik(580, 1150, 30, False) + '<text x="630" y="1162" font-size="38" font-weight="900" fill="#c62828">Fazlasını atma</text>', A.get("fazla", 160), 760, 1150)
    g += U + dv.baslik("RAPOR GELİNCE", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.03)


def s_takvim(p):
    A = p.get("_a", {})
    g = zemin_krem()
    g += pop('<text x="80" y="520" font-size="62" font-weight="900" fill="#c62828">Bir kere yapıp</text><text x="80" y="596" font-size="62" font-weight="900" fill="#c62828">bırakma! 🔁</text>', 4, 360, 540)

    def tak(x, ad, e, metin1, metin2):
        h = kart(x, 680, 450, 520, "#fff", 26) + f'<rect x="{x}" y="680" width="450" height="110" rx="26" fill="#c62828"/><rect x="{x}" y="750" width="450" height="40" fill="#c62828"/>'
        h += "".join(f'<rect x="{x+90+k*230}" y="656" width="22" height="60" rx="11" fill="#455a64"/>' for k in range(2))
        h += f'<text x="{x+225}" y="756" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">{ad}</text>'
        h += emo(x + 225, 960, e, 150)
        h += f'<text x="{x+225}" y="1080" text-anchor="middle" font-size="40" font-weight="900" fill="#263238">{metin1}</text><text x="{x+225}" y="1132" text-anchor="middle" font-size="40" font-weight="900" fill="#263238">{metin2}</text>'
        return h
    g += pop(tak(60, "TARLA BİTKİLERİ", "🌾", "Her ekimden", "önce"), A.get("tarla", 60), 285, 940)
    g += pop(tak(570, "BAĞ · BAHÇE", "🍇", "4-5 yılda", "bir"), A.get("bag", 130), 795, 940)
    g += U + dv.baslik("NE SIKLIKLA?", "#c62828") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.03)


def s_ozet(p):
    A = p.get("_a", {})
    g = zemin_krem()
    maddeler = [("⏰", "Doğru zamanda al", "zaman"), ("📍", "Doğru yerden al", "yer"), ("🪣", "İyi karıştır", "karis"), ("🧪", "Laboratuvara götür", "lab"), ("🌱", "Sonuca göre gübrele", "gubre")]
    for i, (e, ad, k) in enumerate(maddeler):
        y = 690 + i * 132
        t = A.get(k, 20 + i * 30)
        icerik = (kart(70, y - 56, 940, 112, "#fff", 56) + emo(150, y + 26, e, 62)
                  + f'<text x="220" y="{y+16}" font-size="48" font-weight="900" fill="#2F5737">{ad}</text>'
                  + pop(tik(950, y, 34, True), t + 8, 950, y))
        g += pop(icerik, t, 540, y)
    g += U + dv.baslik("ÖZETLE", "#2F5737") + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.02)


dv.SAHNELER.update({"dayi": s_dayi, "lab": s_lab, "rapor": s_rapor, "karsilastir": s_karsilastir, "zaman": s_zaman, "harita": s_harita,
                    "kacin": s_kacin, "karistir": s_karistir, "teslim": s_teslim, "muhendis": s_muhendis, "takvim": s_takvim, "ozet": s_ozet})


# ---------------------------------------------------------------- zamanlama (kelimelerden)
def _kt(kt, kok, vars):
    v = kt(kok)
    return vars if v is None else v


dv.ANIM_EK.update({
    "lab": lambda p, kt, n: {k: _kt(kt, k, 60) - 2 for k in ["ph", "tuz", "kireç", "organik", "fosfor", "potasyum"]},
    "rapor": lambda p, kt, n: {"eksik": _kt(kt, "eksik", 40), "fazla": _kt(kt, "fazla", 70)},
    "karsilastir": lambda p, kt, n: {"analiz": _kt(kt, "analizle", 120) - 4, "masraf": _kt(kt, "masraf", 180), "verim": _kt(kt, "verim", 210)},
    "zaman": lambda p, kt, n: {"hasat": _kt(kt, "hasattan", 20), "ekim": _kt(kt, "ekimden", 50), "islak": _kt(kt, "ıslak", 110), "kuru": _kt(kt, "kuru", 125), "donmus": _kt(kt, "donmuş", 140)},
    "harita": lambda p, kt, n: {"nokta0": _kt(kt, "tarlanın", 6), "noktad": max(30, _kt(kt, "noktasından", 60) + 15 - _kt(kt, "tarlanın", 6)),
                                "on": _kt(kt, "on", 20), "derin": _kt(kt, "yirmi", 100) - 4},
    "kacin": lambda p, kt, n: {"kenar": _kt(kt, "tarla", 4), "agac": _kt(kt, "ağaç", 35), "gubre": _kt(kt, "gübre", 65)},
    "karistir": lambda p, kt, n: {"kova": _kt(kt, "temiz", 20), "tas": _kt(kt, "taşı", 90), "kilo": _kt(kt, "kilosunu", 140), "etiket": _kt(kt, "üstüne", 160),
                                  "adini": _kt(kt, "adını", 170), "yerini": _kt(kt, "yerini", 182), "urunu": _kt(kt, "ürünü", 194), "karis": _kt(kt, "karıştır", 40)},
    "teslim": lambda p, kt, n: {"yola": _kt(kt, "tarım", 10), "var": _kt(kt, "laboratuvarına", 80) + 10},
    "muhendis": lambda p, kt, n: {"rapor": 6, "eksik": _kt(kt, "eksik", 120), "fazla": _kt(kt, "fazla", 160)},
    "takvim": lambda p, kt, n: {"tarla": _kt(kt, "tarla", 60), "bag": _kt(kt, "bağ", 130)},
    "ozet": lambda p, kt, n: {"zaman": _kt(kt, "zamanda", 20) - 4, "yer": _kt(kt, "yerden", 50) - 4, "karis": _kt(kt, "karıştır", 80) - 4, "lab": _kt(kt, "laboratuvara", 110) - 4, "gubre": _kt(kt, "gübrele", 140) - 6},
})

dv.JS_EK += r"""
function poplar(el,t){ $$('.pop',el).forEach(g=>{ const e=spring(t-(+g.dataset.t),0.22), x=+g.dataset.x, y=+g.dataset.y; g.setAttribute('opacity',Math.min(1,e*1.6).toFixed(2));
    g.setAttribute('transform',`translate(${x} ${y}) scale(${Math.min(e,1.08).toFixed(3)}) translate(${-x} ${-y})`); });
  $$('.ciz',el).forEach(c=>{ c.setAttribute('stroke-dashoffset',(1-ease((t-(+c.dataset.t))/(+c.dataset.d||20))).toFixed(3)); }); }
Object.assign(SAHNE,{
 dayi(el,t){ SAHNE.dayi_soru(el,t); },
 lab(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); $$('.sivi',el).forEach(s=>{ const k=+s.dataset.k, h=60+30*Math.sin(t*0.12+k); s.setAttribute('y',-52-h); s.setAttribute('height',h); }); },
 rapor(el,t){ pipf(el,t); poplar(el,t); $$('.cubuk',el).forEach(c=>c.setAttribute('width',(+c.dataset.w*ease((t-(+c.dataset.t))/14)).toFixed(1))); },
 karsilastir(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); let s=''; for(let i=0;i<5;i++){ const p=((t*1.2+i*16)%80)/80; if(t<10) continue; s+=`<g transform="translate(${280+Math.sin(p*7+i)*80} ${1000-p*300}) rotate(${p*200})" opacity="${Math.sin(p*Math.PI).toFixed(2)}"><circle r="22" fill="#f6c343" stroke="#b8860b" stroke-width="4"/><text y="8" text-anchor="middle" font-size="22" font-weight="900" fill="#8a6100">₺</text></g>`; } const u=$('.ucanpara',el); if(u) u.innerHTML=s; },
 zaman(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 harita(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 kacin(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 karistir(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'); const k=$('.karistirici',el); const aktif=t>=(A.karis??40)&&t<(A.tas??90)+20;
   k.setAttribute('transform', aktif?`rotate(${Math.sin(t*0.5)*22} 330 844)`:'');
   const ts=$('.taslar',el); const e=ease((t-(A.tas??90))/14); ts.setAttribute('opacity',e); ts.setAttribute('transform',`translate(${(1-e)*-180} ${(1-e)*-200})`);
   const d=$('.dolum',el); const h=330*ease((t-(A.kilo??140))/24); d.setAttribute('y',-h); d.setAttribute('height',h); },
 teslim(el,t){ clouds(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const g=$('.tasinan',el), t0=+g.dataset.t0, t1=+g.dataset.t1; const e=ease((t-t0)/Math.max(10,t1-t0));
   const x=140+e*(800-140), y=1160-Math.sin(e*Math.PI)*260; g.setAttribute('transform',`translate(${x} ${y}) scale(${1-0.35*e})`); g.setAttribute('opacity', t>t1+8?(1-ease((t-t1-8)/8)).toFixed(2):1); },
 muhendis(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); sallan(el,t); },
 takvim(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 ozet(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
});
"""

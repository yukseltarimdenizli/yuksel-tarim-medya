"""Yüksel Tarım — "usta bilgisi" çizim videosu (1080x1920, 30 fps).
Detaylı vektör çizimler (traktör, pulluk, çiftçi, tarla, gökyüzü) + karaoke altyazı.
Kanca → ❌ sonuçlar → ✅ altın kural → yorum sorusu.
Kullanım: python3 cizim.py <senaryo.json> <cikti.mp4> [--ses ses.m4a] [--muzik m.mp3 --muzik-bas 0]
senaryo.json: {"bant": "USTA BİLGİSİ", "parcalar": [{"sahne": "kanca", "metin": "...", "sure": 5.0}, ...]}
Ses verilirse parça süreleri `sure` alanlarından okunur (ses senkronu için süreleri sese göre ayarlayın).
Sahneler: kanca, secim, hiz, patinaj, yakit, kural, dort (4 kart; "kartlar": [anahtar kelimeler]), dogru, soru (takip et butonlu).
"""
import base64, json, math, pathlib, re, shutil, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

FPS, W, H = 30, 1080, 1920
ASSETS = pathlib.Path(__file__).parent / "assets"
UFUK = 1150      # ufuk çizgisi (çim şeridi)
YER = 1222       # traktörün bastığı zemin


def logo_uri():
    return "data:image/png;base64," + base64.b64encode((ASSETS / "logo.png").read_bytes()).decode()


# ---------------------------------------------------------------- ortak tanımlar
DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<radialGradient id="jant" cx=".38" cy=".34" r=".75"><stop offset="0" stop-color="#fff4c2"/><stop offset=".55" stop-color="#ecc452"/><stop offset="1" stop-color="#a87b1f"/></radialGradient>
<radialGradient id="lastik" cx=".5" cy=".5" r=".5"><stop offset=".62" stop-color="#363636"/><stop offset=".9" stop-color="#1e1e1e"/><stop offset="1" stop-color="#111"/></radialGradient>
<linearGradient id="kaput" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b9ee6"/><stop offset=".45" stop-color="#2f6fb8"/><stop offset="1" stop-color="#1c4a80"/></linearGradient>
<linearGradient id="kaputyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c4a80"/><stop offset=".25" stop-color="#2f6fb8"/><stop offset=".8" stop-color="#3a7cc6"/><stop offset="1" stop-color="#1c4a80"/></linearGradient>
<linearGradient id="cam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e3f5ff" stop-opacity=".55"/><stop offset=".5" stop-color="#a9d6f0" stop-opacity=".28"/><stop offset="1" stop-color="#6aa8cf" stop-opacity=".42"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbfdfe"/><stop offset=".4" stop-color="#c5d2d8"/><stop offset="1" stop-color="#6c7d86"/></linearGradient>
<linearGradient id="metalyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7d8f98"/><stop offset=".45" stop-color="#eef4f6"/><stop offset="1" stop-color="#8a9ba3"/></linearGradient>
<linearGradient id="kirmizi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ef5a4f"/><stop offset=".5" stop-color="#c62828"/><stop offset="1" stop-color="#8e1c1c"/></linearGradient>
<linearGradient id="koyugri" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a4a"/><stop offset="1" stop-color="#232323"/></linearGradient>
<linearGradient id="tarla" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a7149"/><stop offset="1" stop-color="#5a3e25"/></linearGradient>
<linearGradient id="surulmus" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f4b2c"/><stop offset="1" stop-color="#553820"/></linearGradient>
<radialGradient id="gunes" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6c8" stop-opacity=".95"/><stop offset=".45" stop-color="#ffe082" stop-opacity=".45"/><stop offset="1" stop-color="#ffe082" stop-opacity="0"/></radialGradient>
<radialGradient id="ten" cx=".38" cy=".35" r=".7"><stop offset="0" stop-color="#ffd9b0"/><stop offset=".7" stop-color="#eab486"/><stop offset="1" stop-color="#c98d5f"/></radialGradient>
<radialGradient id="kabuk" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#f4c58a"/><stop offset=".7" stop-color="#c98a45"/><stop offset="1" stop-color="#8d5a26"/></radialGradient>
<linearGradient id="kadran" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e3e8ea"/></linearGradient>
<linearGradient id="cerceve" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d6a70"/><stop offset=".5" stop-color="#263238"/><stop offset="1" stop-color="#11181c"/></linearGradient>
<linearGradient id="bidon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8e1c1c"/><stop offset=".35" stop-color="#e53935"/><stop offset="1" stop-color="#9e2222"/></linearGradient>
<linearGradient id="para" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b7e3a8"/><stop offset="1" stop-color="#5fa356"/></linearGradient>
<linearGradient id="dislisi" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfd8dc"/><stop offset=".5" stop-color="#90a4ae"/><stop offset="1" stop-color="#546e7a"/></linearGradient>
<linearGradient id="telefon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f44"/><stop offset="1" stop-color="#15181b"/></linearGradient>
<pattern id="kareli" width="26" height="26" patternUnits="userSpaceOnUse"><rect width="26" height="26" fill="#c0392b"/><rect width="13" height="26" fill="#8e2a20" opacity=".55"/><rect width="26" height="13" fill="#8e2a20" opacity=".45"/><path d="M0 6.5H26M6.5 0V26" stroke="#f3d6a8" stroke-width="1.6" opacity=".55"/></pattern>
<pattern id="kot" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#34506e"/><path d="M0 10L10 0" stroke="#2a425c" stroke-width="2"/></pattern>
<filter id="golge" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000" flood-opacity=".28"/></filter>
<filter id="yumusak"><feGaussianBlur stdDeviation="6"/></filter>
<radialGradient id="vinyet" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></radialGradient>
</defs></svg>"""


# ---------------------------------------------------------------- çizim parçaları
def teker(cx, cy, r, cls=""):
    """Tırnaklı traktör lastiği + jant. Dönmesi için .whl grubu döndürülür."""
    n = max(14, int(r / 7.5))
    tirnak = "".join(
        f'<path d="M{cx-r*.13:.1f} {cy-r*1.0:.1f} L{cx+r*.03:.1f} {cy-r*1.0:.1f} L{cx+r*.13:.1f} {cy-r*.8:.1f} L{cx-r*.03:.1f} {cy-r*.8:.1f} Z" '
        f'fill="#1c1c1c" stroke="#4a4a4a" stroke-width="{max(1.5, r*.012):.1f}" stroke-linejoin="round" transform="rotate({k*360/n:.2f} {cx} {cy})"/>' for k in range(n))
    delik = "".join(f'<ellipse cx="{cx+math.cos(a)*r*.36:.1f}" cy="{cy+math.sin(a)*r*.36:.1f}" rx="{r*.07:.1f}" ry="{r*.05:.1f}" fill="#7a5a14" '
                    f'transform="rotate({math.degrees(a):.1f} {cx+math.cos(a)*r*.36:.1f} {cy+math.sin(a)*r*.36:.1f})"/>'
                    for a in [k * math.pi / 4 for k in range(8)])
    civata = "".join(f'<circle cx="{cx+math.cos(k*math.pi/3)*r*.11:.1f}" cy="{cy+math.sin(k*math.pi/3)*r*.11:.1f}" r="{r*.022:.1f}" fill="#d9d9d9"/>' for k in range(6))
    return (f'<g class="whl {cls}" data-cx="{cx}" data-cy="{cy}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.88}" fill="url(#lastik)"/>{tirnak}'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.76}" fill="none" stroke="#2c2c2c" stroke-width="{r*.03}"/>'
            f'<path d="M{cx-r*.62} {cy-r*.5} A{r*.8} {r*.8} 0 0 1 {cx+r*.3} {cy-r*.74}" stroke="#fff" stroke-opacity=".13" stroke-width="{r*.06}" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.57}" fill="url(#jant)" stroke="#8a6416" stroke-width="{r*.025}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.46}" fill="none" stroke="#b58b2a" stroke-width="{r*.03}"/>'
            f'{delik}<circle cx="{cx}" cy="{cy}" r="{r*.19}" fill="#c9a03c" stroke="#7a5a14" stroke-width="{r*.02}"/>{civata}'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.06}" fill="#4d3a0e"/></g>')


def yuz(ifade="normal"):
    """Sağa (3/4) bakan çiftçi başı; merkez (0,0), yarıçap ~50. Kasket firma yeşili."""
    g = ('<ellipse cx="-38" cy="4" rx="10" ry="14" fill="#e3a676"/>'
         '<circle r="50" fill="url(#ten)"/>'
         '<path d="M-50 -2 Q-48 34 -14 48 Q-40 30 -42 -4 Z" fill="#c98d5f" opacity=".35"/>'
         '<circle cx="30" cy="16" r="10" fill="#f28b82" opacity=".45"/>'
         '<path d="M44 -4 Q60 6 46 16" fill="#eab486" stroke="#c98d5f" stroke-width="3"/>')
    if ifade == "mutlu":
        g += ('<path d="M12 -12 Q20 -20 28 -12" stroke="#2b1d14" stroke-width="5" fill="none" stroke-linecap="round"/>'
              '<path d="M8 -28 Q20 -34 32 -27" stroke="#4a3426" stroke-width="5" fill="none" stroke-linecap="round"/>')
    else:
        g += ('<ellipse cx="21" cy="-10" rx="9" ry="11" fill="#fff"/><circle cx="25" cy="-9" r="5.5" fill="#2b1d14"/><circle cx="27" cy="-11" r="1.8" fill="#fff"/>')
        if ifade == "endise":
            g += '<path d="M6 -24 Q18 -34 34 -32" stroke="#4a3426" stroke-width="6" fill="none" stroke-linecap="round" transform="rotate(14 20 -28)"/>'
        else:
            g += '<path d="M8 -26 Q20 -33 33 -27" stroke="#4a3426" stroke-width="5" fill="none" stroke-linecap="round"/>'
    g += '<path d="M10 20 Q26 10 52 18 Q48 28 34 26 Q24 30 10 20 Z" fill="#4a3426"/>'
    if ifade == "mutlu":
        g += '<path d="M16 30 Q30 44 44 30 Q30 36 16 30 Z" fill="#7a2e22"/>'
    elif ifade == "endise":
        g += '<path d="M18 36 Q24 30 30 36 Q36 42 42 36" stroke="#5b2a1e" stroke-width="4" fill="none" stroke-linecap="round"/>'
    else:
        g += '<path d="M20 33 Q30 38 40 32" stroke="#5b2a1e" stroke-width="4" fill="none" stroke-linecap="round"/>'
    g += ('<path d="M-52 -8 Q-50 -58 4 -60 Q46 -58 54 -20 L-52 -8 Z" fill="#2F5737"/>'
          '<path d="M-52 -10 L54 -22 L54 -14 L-52 -2 Z" fill="#E2B654"/>'
          '<path d="M40 -20 Q74 -24 92 -12 Q70 -6 42 -10 Z" fill="#244530"/>'
          '<circle cx="2" cy="-60" r="6" fill="#244530"/>'
          '<path d="M-30 -48 Q-10 -56 14 -54" stroke="#4f8a5c" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>')
    return g


def traktor(ifade="normal"):
    """Yandan traktör. Yerel koordinat: (0,0) arka teker zemin teması, sağa bakar.
    Arka teker r=165 (0,-165), ön teker r=100 (390,-100). 3 nokta askı ucu (-235,-120)."""
    g = '<g class="trk"><ellipse cx="170" cy="6" rx="380" ry="20" fill="#000" opacity=".22" filter="url(#yumusak)"/>'
    # egzoz + hava filtresi (kabin önü)
    g += ('<rect x="300" y="-520" width="22" height="210" rx="6" fill="url(#metalyan)"/><rect x="296" y="-548" width="30" height="36" rx="6" fill="#3a3a3a"/>'
          '<path d="M294 -548 L330 -562 L330 -548 Z" fill="#555"/><g class="duman"></g>'
          '<rect x="384" y="-430" width="16" height="96" fill="#333"/><rect x="370" y="-470" width="44" height="46" rx="12" fill="#262626"/>'
          '<rect x="376" y="-462" width="32" height="6" rx="3" fill="#555"/>')
    # 3 nokta askı
    g += ('<path d="M-110 -150 L-235 -120" stroke="#2b2b2b" stroke-width="18" stroke-linecap="round"/>'
          '<path d="M-150 -330 L-262 -330" stroke="#3a3a3a" stroke-width="14" stroke-linecap="round"/>'
          '<path d="M-150 -330 L-262 -330" stroke="#888" stroke-width="4" stroke-dasharray="10 8"/>'
          '<path d="M-90 -260 L-120 -150" stroke="#2b2b2b" stroke-width="10"/>')
    # şasi, motor, ağırlıklar
    g += '<rect x="-70" y="-205" width="540" height="64" rx="14" fill="url(#koyugri)"/>'
    g += '<rect x="170" y="-222" width="270" height="62" rx="10" fill="#3d3d3d"/>' + "".join(
        f'<circle cx="{190+i*36}" cy="-178" r="5" fill="#8a8a8a"/>' for i in range(7))
    g += "".join(f'<rect x="478" y="{-244+i*22}" width="50" height="20" rx="4" fill="#3d3d3d" stroke="#1f1f1f" stroke-width="2"/>' for i in range(5))
    g += '<rect x="488" y="-260" width="30" height="16" rx="4" fill="#555"/>'
    # kaput
    g += ('<path d="M128 -360 L440 -360 Q482 -360 486 -318 L490 -222 L128 -222 Z" fill="url(#kaput)"/>'
          '<path d="M140 -350 L436 -350 Q470 -348 474 -322" stroke="#a9d1ff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".75"/>')
    g += "".join(f'<path d="M{300+i*24} -328 L{288+i*24} -268" stroke="#163a66" stroke-width="9" stroke-linecap="round"/>' for i in range(6))
    g += ('<path d="M132 -262 L488 -262 L488 -250 L132 -250 Z" fill="#fff" opacity=".9"/><path d="M132 -246 L488 -246 L488 -239 L132 -239 Z" fill="#E2B654"/>'
          '<rect x="480" y="-350" width="18" height="124" rx="6" fill="#163a66"/>'
          + "".join(f'<rect x="483" y="{-342+i*14}" width="12" height="7" rx="2" fill="#0d243f"/>' for i in range(8)) +
          '<rect x="452" y="-312" width="36" height="22" rx="8" fill="#fff8c4" stroke="#8a8a8a" stroke-width="3"/>'
          '<path d="M490 -306 L560 -326 L560 -276 L490 -296 Z" fill="#fff6b0" opacity=".25"/>')
    # yakıt deposu + basamak
    g += ('<rect x="70" y="-282" width="78" height="66" rx="16" fill="url(#kaput)"/><rect x="96" y="-294" width="24" height="14" rx="4" fill="#222"/>'
          '<path d="M112 -210 L112 -120 M96 -170 H128 M96 -132 H128" stroke="#2b2b2b" stroke-width="7" stroke-linecap="round"/>')
    # sürücü (kabin içinde)
    g += ('<rect x="-70" y="-470" width="72" height="96" rx="16" fill="#263238"/>'
          '<path d="M-44 -500 Q-6 -520 34 -498 L46 -392 L-52 -392 Z" fill="url(#kareli)"/>'
          '<path d="M-44 -500 Q-30 -508 -20 -506 L-26 -392 L-52 -392 Z" fill="#2F5737"/>'
          '<path d="M24 -480 Q70 -460 96 -452" stroke="url(#kareli)" stroke-width="26" fill="none" stroke-linecap="round"/>'
          '<circle cx="102" cy="-450" r="14" fill="url(#ten)"/>'
          '<ellipse cx="112" cy="-446" rx="10" ry="38" fill="none" stroke="#1d1d1d" stroke-width="9" transform="rotate(28 112 -446)"/>'
          '<path d="M112 -446 L150 -380" stroke="#1d1d1d" stroke-width="9"/>'
          f'<g transform="translate(0 -560) scale(.78)">{yuz(ifade)}</g>'
          '<g class="ter" opacity="0"><path d="M50 -620 q10 18 0 28 q-10 -10 0 -28" fill="#7fc8ff"/><path d="M-44 -606 q9 16 0 25 q-9 -9 0 -25" fill="#7fc8ff"/></g>')
    # kabin camı, dikmeler, tavan, ayna, tepe lambası
    g += ('<path d="M-152 -660 L176 -660 L190 -372 L-152 -372 Z" fill="url(#cam)"/>'
          '<path d="M-110 -650 L-40 -650 L-150 -470 Z M40 -650 L80 -650 L-40 -400 L-70 -400 Z" fill="#fff" opacity=".22"/>'
          '<path d="M-152 -660 L-152 -372 M176 -660 L190 -372 M14 -660 L18 -372" stroke="#1f1f1f" stroke-width="14" stroke-linecap="round"/>'
          '<path d="M-152 -372 L190 -372" stroke="#1f1f1f" stroke-width="10"/>'
          '<rect x="-182" y="-710" width="392" height="54" rx="20" fill="url(#kaput)"/>'
          '<path d="M-170 -700 L196 -700" stroke="#a9d1ff" stroke-width="6" stroke-linecap="round" opacity=".7"/>'
          '<rect x="-182" y="-664" width="392" height="10" fill="#163a66"/>'
          '<rect x="40" y="-736" width="40" height="28" rx="10" fill="#ff9800"/><rect x="48" y="-740" width="24" height="8" rx="4" fill="#ffcc80"/>'
          '<g class="tepe"></g>'
          '<path d="M190 -600 L232 -606" stroke="#1f1f1f" stroke-width="6"/><rect x="226" y="-640" width="22" height="50" rx="8" fill="#263238" stroke="#9e9e9e" stroke-width="3"/>')
    # arka çamurluk (teker üstü), kabin tabanı
    g += ('<path d="M-205 -200 A205 205 0 0 1 205 -200 L178 -200 A178 178 0 0 0 -178 -200 Z" fill="url(#kaput)"/>'
          '<path d="M-196 -230 A200 200 0 0 1 -70 -386" stroke="#a9d1ff" stroke-width="6" fill="none" stroke-linecap="round" opacity=".6"/>'
          '<rect x="-160" y="-388" width="360" height="22" rx="8" fill="#163a66"/>')
    g += teker(0, -165, 165, "arka") + teker(390, -100, 100, "on") + '</g>'
    return g


def pulluk(n=3, s=1.0, toprak=False):
    """Asılır kulaklı pulluk. (0,0) alt askı pimi; pulluk sola uzanır; zemin y=120*s civarı."""
    L = 70 + n * 130
    g = f'<g class="plk" transform="scale({s})">'
    g += ('<path d="M0 0 L-28 -212 L-70 0" fill="none" stroke="url(#kirmizi)" stroke-width="18" stroke-linejoin="round"/>'
          '<path d="M-14 -100 L-56 -100" stroke="#a31f1f" stroke-width="10"/>'
          '<circle cx="-28" cy="-212" r="11" fill="#333"/><circle cx="0" cy="0" r="12" fill="#333"/><circle cx="0" cy="0" r="5" fill="#bbb"/>')
    g += (f'<rect x="{-L-10}" y="-24" width="{L-40}" height="44" rx="9" fill="url(#kirmizi)"/>'
          f'<path d="M{-L} -15 H-60" stroke="#ff9d93" stroke-width="5" opacity=".7" stroke-linecap="round"/>')
    for i in range(n):
        x = -110 - i * 130
        g += (f'<rect x="{x-16}" y="-30" width="32" height="56" rx="6" fill="#7d1717"/><circle cx="{x-6}" cy="-10" r="4" fill="#ddd"/><circle cx="{x+6}" cy="8" r="4" fill="#ddd"/>'
              f'<path d="M{x+48} 12 L{x+54} 104" stroke="#555" stroke-width="10"/><circle cx="{x+54}" cy="118" r="30" fill="url(#metal)" stroke="#5b6b73" stroke-width="3" opacity=".9"/><circle cx="{x+54}" cy="118" r="7" fill="#555"/>'
              f'<path d="M{x} 16 C{x+6} 56 {x-2} 84 {x-16} 110" stroke="#8e1c1c" stroke-width="22" fill="none" stroke-linecap="round"/>'
              f'<path d="M{x+22} 152 L{x-4} 96 Q{x-44} 74 {x-104} 86 Q{x-78} 114 {x-72} 152 Z" fill="url(#metal)" stroke="#55656d" stroke-width="3"/>'
              f'<path d="M{x-12} 102 Q{x-48} 90 {x-90} 96" stroke="#fff" stroke-width="5" opacity=".85" fill="none" stroke-linecap="round"/>'
              f'<path d="M{x+50} 154 L{x+10} 138 L{x-74} 148 L{x-70} 160 Z" fill="#37474f"/>')
        if toprak:
            g += (f'<path d="M{x-74} 150 Q{x-100} 96 {x-138} 104 Q{x-150} 128 {x-128} 152 Z" fill="#6f4b2c"/>'
                  f'<circle cx="{x-120}" cy="110" r="9" fill="#5a3d24"/><circle cx="{x-136}" cy="124" r="7" fill="#8a6440"/>')
    if n >= 4:
        xe = -L - 6
        g += (f'<path d="M{xe+30} 0 L{xe} 92" stroke="#7d1717" stroke-width="14"/><circle cx="{xe}" cy="104" r="40" fill="#263238"/>'
              f'<circle cx="{xe}" cy="104" r="24" fill="url(#metal)"/><circle cx="{xe}" cy="104" r="7" fill="#333"/>')
    return g + '</g>'


def ciftci(poz="isaret", ifade="mutlu"):
    """Ayakta çiftçi; (0,0) ayak altı, boy ~520, sağa bakar. poz: isaret | salla | dur"""
    g = '<ellipse cx="6" cy="4" rx="90" ry="14" fill="#000" opacity=".2" filter="url(#yumusak)"/>'
    g += ('<path d="M-44 -228 L-6 -228 L-10 -20 L-42 -20 Z" fill="url(#kot)"/><path d="M6 -228 L44 -228 L42 -20 L10 -20 Z" fill="url(#kot)"/>'
          '<path d="M-48 -24 L-6 -24 Q4 -24 6 -2 L-50 -2 Z" fill="#4e342e"/><path d="M6 -24 L48 -24 Q66 -22 70 -2 L6 -2 Z" fill="#4e342e"/>'
          '<path d="M-44 -20 H-8 M10 -20 H44" stroke="#2a425c" stroke-width="4"/>')
    # gövde: kareli gömlek + yelek
    g += ('<path d="M-66 -420 Q0 -440 66 -420 L58 -222 L-58 -222 Z" fill="url(#kareli)"/>'
          '<path d="M-66 -420 Q-40 -430 -18 -432 L-12 -222 L-58 -222 Z" fill="#2F5737"/>'
          '<path d="M66 -420 Q40 -430 18 -432 L12 -222 L58 -222 Z" fill="#2F5737"/>'
          '<path d="M-40 -330 h22 M22 -330 h22" stroke="#244530" stroke-width="5"/>'
          '<circle cx="-14" cy="-380" r="4" fill="#E2B654"/><circle cx="-13" cy="-330" r="4" fill="#E2B654"/><circle cx="-12" cy="-280" r="4" fill="#E2B654"/>'
          '<rect x="-60" y="-236" width="120" height="18" rx="4" fill="#4e342e"/><rect x="-10" y="-238" width="22" height="22" rx="4" fill="none" stroke="#E2B654" stroke-width="4"/>'
          '<rect x="-18" y="-462" width="38" height="40" rx="10" fill="#e3a676"/>'
          '<path d="M-22 -428 L0 -404 L22 -428" fill="#f3d6a8"/>')
    # arka kol
    if poz == "salla":
        g += '<path d="M-56 -404 Q-92 -330 -70 -250" stroke="url(#kareli)" stroke-width="34" fill="none" stroke-linecap="round"/><circle cx="-68" cy="-240" r="18" fill="url(#ten)"/>'
    else:
        g += '<path d="M-56 -404 Q-104 -340 -60 -280" stroke="url(#kareli)" stroke-width="34" fill="none" stroke-linecap="round"/><circle cx="-56" cy="-272" r="18" fill="url(#ten)"/>'
    # ön kol
    if poz == "isaret":
        g += ('<g class="kol"><path d="M50 -404 Q110 -420 168 -450" stroke="url(#kareli)" stroke-width="34" fill="none" stroke-linecap="round"/>'
              '<circle cx="182" cy="-456" r="19" fill="url(#ten)"/><rect x="190" y="-470" width="42" height="13" rx="6.5" fill="url(#ten)" transform="rotate(-24 190 -470)"/></g>')
    elif poz == "salla":
        g += ('<g class="kol" data-ox="50" data-oy="-404"><path d="M50 -404 Q110 -460 118 -560" stroke="url(#kareli)" stroke-width="34" fill="none" stroke-linecap="round"/>'
              '<ellipse cx="120" cy="-588" rx="24" ry="28" fill="url(#ten)"/>'
              + "".join(f'<rect x="{104+k*9}" y="-628" width="9" height="30" rx="4.5" fill="url(#ten)"/>' for k in range(4)) + '</g>')
    else:
        g += '<path d="M50 -404 Q80 -330 60 -250" stroke="url(#kareli)" stroke-width="34" fill="none" stroke-linecap="round"/><circle cx="58" cy="-240" r="18" fill="url(#ten)"/>'
    g += f'<g transform="translate(6 -500) scale(1.1)">{yuz(ifade)}</g>'
    return g


def bulut(x, y, s, sp):
    return (f'<g class="bulut" data-x="{x}" data-y="{y}" data-sp="{sp}" transform="translate({x} {y})"><g transform="scale({s})">'
            '<ellipse cx="0" cy="24" rx="132" ry="30" fill="#c9dcec"/>'
            '<circle cx="-70" cy="4" r="46" fill="#fff"/><circle cx="-8" cy="-26" r="66" fill="#fff"/><circle cx="62" cy="-2" r="50" fill="#fff"/>'
            '<ellipse cx="0" cy="16" rx="128" ry="30" fill="#fff"/><ellipse cx="10" cy="26" rx="100" ry="12" fill="#e3eef7"/></g></g>')


def kavak(x, y, h):
    return (f'<rect x="{x-4}" y="{y-h*.25}" width="8" height="{h*.25}" fill="#5d4037"/>'
            f'<ellipse cx="{x}" cy="{y-h*.58}" rx="{h*.15}" ry="{h*.45}" fill="#3e7b3a"/>'
            f'<path d="M{x} {y-h*1.03} Q{x+h*.17} {y-h*.6} {x} {y-h*.14} Z" fill="#2f6430"/>')


def agac(x, y, r):
    return (f'<rect x="{x-6}" y="{y-r*1.1}" width="12" height="{r*1.1}" fill="#5d4037"/>'
            f'<circle cx="{x-r*.5}" cy="{y-r*1.3}" r="{r*.7}" fill="#4c8c3f"/><circle cx="{x+r*.45}" cy="{y-r*1.35}" r="{r*.75}" fill="#3f7d36"/>'
            f'<circle cx="{x}" cy="{y-r*1.8}" r="{r*.8}" fill="#57a046"/><circle cx="{x-r*.2}" cy="{y-r*2.0}" r="{r*.3}" fill="#6fb85a" opacity=".7"/>')


def ev(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect x="70" y="-150" width="18" height="40" fill="#8d6e63"/>'
            '<rect x="0" y="-90" width="150" height="90" fill="#f5e6c8"/><rect x="0" y="-90" width="150" height="10" fill="#e0cba3"/>'
            '<path d="M-14 -86 L75 -150 L164 -86 Z" fill="#b5442f"/><path d="M-14 -86 L75 -150 L80 -146 L-6 -84 Z" fill="#d35a42"/>'
            '<rect x="20" y="-62" width="34" height="30" fill="#7fb6d9" stroke="#fff" stroke-width="4"/><rect x="96" y="-56" width="32" height="56" fill="#795548"/>'
            '<circle cx="122" cy="-28" r="3" fill="#E2B654"/></g>')


_GID = [0]


def gok(ust="#bfe3ff", alt="#fff4dc", ufuk=UFUK, gunes=True, manzara=True):
    _GID[0] += 1
    gid = f"gk{_GID[0]}"
    g = (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ust}"/><stop offset="1" stop-color="{alt}"/></linearGradient></defs>'
         f'<rect width="1080" height="1920" fill="url(#{gid})"/>')
    if gunes:
        g += ('<circle cx="860" cy="400" r="190" fill="url(#gunes)"/><circle cx="860" cy="400" r="78" fill="#ffd54f"/>'
              '<circle cx="836" cy="378" r="30" fill="#ffe89a" opacity=".8"/>')
    g += bulut(230, 330, .9, .5) + bulut(700, 560, .65, .35) + bulut(1000, 250, .55, .25)
    if manzara:
        g += (f'<path d="M0 {ufuk-170} L120 {ufuk-280} L230 {ufuk-200} L380 {ufuk-330} L520 {ufuk-210} L640 {ufuk-290} L780 {ufuk-190} L920 {ufuk-300} L1080 {ufuk-200} L1080 {ufuk} L0 {ufuk} Z" fill="#b8cdd9"/>'
              f'<path d="M380 {ufuk-330} L420 {ufuk-292} L398 {ufuk-286} L380 {ufuk-300} L360 {ufuk-292} Z M920 {ufuk-300} L952 {ufuk-270} L920 {ufuk-276} L900 {ufuk-268} Z" fill="#fff" opacity=".85"/>'
              f'<path d="M0 {ufuk-120} Q160 {ufuk-200} 330 {ufuk-140} T700 {ufuk-150} T1080 {ufuk-130} L1080 {ufuk} L0 {ufuk} Z" fill="#a8cf80"/>')
        g += "".join(kavak(x, ufuk - 118 + (x % 3) * 6, 120 + (x % 5) * 8) for x in range(560, 900, 46))
        g += ev(150, ufuk - 118, .8) + agac(380, ufuk - 110, 34) + agac(960, ufuk - 112, 38)
        g += (f'<path d="M0 {ufuk-50} Q300 {ufuk-100} 600 {ufuk-60} T1080 {ufuk-70} L1080 {ufuk} L0 {ufuk} Z" fill="#8cbc5c"/>'
              + "".join(f'<rect x="{x}" y="{ufuk-62}" width="8" height="42" fill="#8d6e63"/>' for x in range(20, 1080, 90))
              + f'<path d="M0 {ufuk-50} H1080 M0 {ufuk-34} H1080" stroke="#8d6e63" stroke-width="5"/>')
    g += f'<rect x="0" y="{ufuk-8}" width="1080" height="16" fill="#6b9a3e"/>'
    g += "".join(f'<path d="M{x} {ufuk+6} l6 -22 l4 18 l6 -26 l4 26 l6 -16 l4 20 Z" fill="#5e8d36"/>' for x in range(10, 1080, 74))
    return g


def tarla(ufuk=UFUK, sur_x=None, sur_cls=""):
    """Zemin: üst şerit (çalışılan sıra) + perspektif sıralar. sur_x: bu x'in solu sürülmüş."""
    g = f'<rect x="0" y="{ufuk+8}" width="1080" height="{1920-ufuk}" fill="url(#tarla)"/>'
    y, k = ufuk + 120, 0
    while y < 1920:
        g += f'<path d="M0 {y} Q270 {y-8} 540 {y} T1080 {y}" stroke="#4a321d" stroke-width="{4+k*1.6:.1f}" fill="none" opacity=".45"/>'
        g += f'<path d="M0 {y+6+k} Q270 {y-2+k} 540 {y+6+k} T1080 {y+6+k}" stroke="#b08860" stroke-width="{2+k*.8:.1f}" fill="none" opacity=".35"/>'
        k += 1; y += 34 + k * 14
    # anız (sürülmemiş) sapları
    g += "".join(f'<path d="M{x} {ufuk+30+(x*7)%70} l-3 -16 M{x+8} {ufuk+34+(x*11)%60} l3 -14" stroke="#d9b866" stroke-width="4" stroke-linecap="round"/>' for x in range(14, 1080, 38))
    if sur_x is not None:
        g += (f'<g class="surulmus {sur_cls}"><rect x="0" y="{ufuk+10}" width="{sur_x}" height="104" fill="url(#surulmus)"/>'
              + "".join(f'<path d="M{x} {ufuk+28+r*28} q24 -18 48 0" stroke="#4b311b" stroke-width="7" fill="none" stroke-linecap="round"/>'
                        f'<path d="M{x+4} {ufuk+22+r*28} q20 -12 40 0" stroke="#93694a" stroke-width="4" fill="none" stroke-linecap="round"/>'
                        for r in range(3) for x in range(-20 + r * 26, 1080, 74)) + '</g>')
    g += "".join(f'<ellipse cx="{x}" cy="{yy}" rx="{rx}" ry="{rx*.55}" fill="#9e9e9e"/><ellipse cx="{x-rx*.3}" cy="{yy-rx*.2}" rx="{rx*.4}" ry="{rx*.2}" fill="#d0d0d0"/>'
                 for x, yy, rx in [(150, 1560, 16), (880, 1720, 22), (420, 1840, 14), (980, 1420, 12)])
    return g


def on_toprak(x1, x2, y, alt=44):
    """Pulluk gövdelerini / teker altını örten toprak yığını (alt kenarı yumuşak)."""
    pts, x = [], x1
    while x < x2:
        pts.append(f"Q{x+18} {y-24 - (x*13)%16} {x+36} {y}")
        x += 36
    return (f'<path d="M{x1} {y+30} L{x1} {y} {" ".join(pts)} Q{x+30} {y+20} {x} {y+44} Q{(x1+x)/2} {y+alt+26} {x1} {y+alt} Z" fill="#62422a"/>'
            f'<path d="M{x1} {y+30} Q{(x1+x)/2} {y+58} {x} {y+34}" stroke="#4a3019" stroke-width="10" fill="none" opacity=".6"/>'
            + "".join(f'<circle cx="{xx}" cy="{y-6-(xx*7)%10}" r="{5+(xx%3)*2}" fill="#8a6440"/>' for xx in range(x1 + 10, x2, 44)))


def kadran(cx, cy, r, tur="hiz"):
    """Gösterge paneli kadranı (yarım daire üstü). İbre .ibre grubu, (0,0) merkez, yukarı bakar."""
    g = f'<g transform="translate({cx} {cy})" filter="url(#golge)">'
    g += (f'<path d="M{-r-36} 30 A{r+36} {r+36} 0 0 1 {r+36} 30 Z" fill="url(#cerceve)"/>'
          f'<path d="M{-r-14} 20 A{r+14} {r+14} 0 0 1 {r+14} 20 Z" fill="#11181c"/>'
          f'<path d="M{-r} 14 A{r} {r} 0 0 1 {r} 14 Z" fill="url(#kadran)"/>')
    if tur == "hiz":
        bolge = [(-90, -30, "#e53935"), (-30, 30, "#fbc02d"), (30, 90, "#43a047")]
        for a1, a2, c in bolge:
            p1 = (math.sin(math.radians(a1)) * r * .86, -math.cos(math.radians(a1)) * r * .86)
            p2 = (math.sin(math.radians(a2)) * r * .86, -math.cos(math.radians(a2)) * r * .86)
            g += f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{r*.86:.1f} {r*.86:.1f} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" stroke="{c}" stroke-width="{r*.07:.1f}" fill="none"/>'
        for v in range(0, 41, 2):
            a = math.radians(-90 + v / 40 * 180); big = v % 10 == 0
            r1 = r * (.7 if big else .76)
            g += f'<path d="M{math.sin(a)*r1:.1f} {-math.cos(a)*r1:.1f} L{math.sin(a)*r*.8:.1f} {-math.cos(a)*r*.8:.1f}" stroke="#263238" stroke-width="{7 if big else 3}" stroke-linecap="round"/>'
            if big:
                g += f'<text x="{math.sin(a)*r*.56:.1f}" y="{-math.cos(a)*r*.56+16:.1f}" text-anchor="middle" font-size="{r*.15:.0f}" font-weight="800" fill="#263238">{v}</text>'
        g += f'<text y="{-r*.25:.0f}" text-anchor="middle" font-size="{r*.1:.0f}" font-weight="700" fill="#78909c">km/sa</text>'
    else:  # yakıt
        g += f'<path d="M{-r*.86*math.sin(math.radians(80)):.1f} {-r*.86*math.cos(math.radians(80)):.1f} A{r*.86:.1f} {r*.86:.1f} 0 0 1 {-r*.86*math.sin(math.radians(50)):.1f} {-r*.86*math.cos(math.radians(50)):.1f}" stroke="#e53935" stroke-width="{r*.08:.1f}" fill="none"/>'
        for k in range(9):
            a = math.radians(-80 + k * 20); big = k % 4 == 0
            r1 = r * (.68 if big else .75)
            g += f'<path d="M{math.sin(a)*r1:.1f} {-math.cos(a)*r1:.1f} L{math.sin(a)*r*.8:.1f} {-math.cos(a)*r*.8:.1f}" stroke="#263238" stroke-width="{8 if big else 4}" stroke-linecap="round"/>'
        for a, t in [(-80, "E"), (0, "½"), (80, "F")]:
            ar = math.radians(a)
            g += f'<text x="{math.sin(ar)*r*.55:.1f}" y="{-math.cos(ar)*r*.55+20:.1f}" text-anchor="middle" font-size="{r*.18:.0f}" font-weight="900" fill="{"#e53935" if t=="E" else "#263238"}">{t}</text>'
        g += (f'<g transform="translate(0 {-r*.28:.0f}) scale({r/260:.2f})"><rect x="-26" y="-40" width="40" height="60" rx="6" fill="#455a64"/><rect x="-18" y="-32" width="24" height="18" rx="3" fill="#cfd8dc"/>'
              '<path d="M14 -24 h12 q8 0 8 8 v26 q0 8 6 8" stroke="#455a64" stroke-width="7" fill="none"/></g>'
              f'<g class="lamba" opacity="0"><circle cx="{-r*.5:.0f}" cy="{-r*.08:.0f}" r="{r*.07:.0f}" fill="#ff7043"/><circle cx="{-r*.5:.0f}" cy="{-r*.08:.0f}" r="{r*.14:.0f}" fill="#ff7043" opacity=".3"/></g>')
    g += (f'<g class="ibre"><path d="M-10 0 L-3 {-r*.82:.0f} L3 {-r*.82:.0f} L10 0 Z" fill="#d32f2f"/><path d="M-4 0 L-1 {-r*.8:.0f} L0 0 Z" fill="#ff8a80"/></g>'
          f'<circle r="{r*.11:.0f}" fill="#263238"/><circle r="{r*.05:.0f}" fill="#90a4ae"/>'
          f'<path d="M{-r*.82:.0f} {-r*.12:.0f} A{r*.86:.0f} {r*.86:.0f} 0 0 1 {-r*.2:.0f} {-r*.84:.0f}" stroke="#fff" stroke-width="{r*.05:.0f}" fill="none" opacity=".55" stroke-linecap="round"/>'
          '</g>')
    return g


def salyangoz():
    return ('<g class="sly"><ellipse cx="0" cy="4" rx="90" ry="10" fill="#000" opacity=".18"/>'
            '<path class="slygov" d="M-80 0 Q-80 -24 -40 -26 L60 -30 Q96 -32 100 -64 Q104 -84 116 -84 Q128 -80 122 -50 Q118 -10 80 0 Z" fill="#b9cf8f" stroke="#7d9a55" stroke-width="4"/>'
            '<path d="M104 -80 L96 -128 M116 -82 L122 -128" stroke="#7d9a55" stroke-width="6" stroke-linecap="round"/>'
            '<circle cx="96" cy="-132" r="9" fill="#2b2b2b"/><circle cx="122" cy="-132" r="9" fill="#2b2b2b"/><circle cx="98" cy="-135" r="3" fill="#fff"/><circle cx="124" cy="-135" r="3" fill="#fff"/>'
            '<path d="M106 -60 Q114 -52 122 -60" stroke="#3e5a24" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<circle cx="0" cy="-74" r="64" fill="url(#kabuk)" stroke="#7a4a1c" stroke-width="5"/>'
            '<path d="M0 -74 m0 -8 a8 8 0 1 1 -8 8 a16 16 0 1 1 16 16 a26 26 0 1 1 -26 -26 a38 38 0 1 1 38 38" stroke="#7a4a1c" stroke-width="6" fill="none" stroke-linecap="round"/>'
            '<path d="M-36 -116 Q-10 -134 22 -126" stroke="#ffe0b2" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>'
            '</g>')


def bidon():
    return ('<g><ellipse cx="0" cy="6" rx="120" ry="14" fill="#000" opacity=".2" filter="url(#yumusak)"/>'
            '<path d="M-110 0 L-110 -250 Q-110 -280 -80 -290 L40 -290 L110 -230 L110 0 Z" fill="url(#bidon)" stroke="#6d1414" stroke-width="5"/>'
            '<path d="M-80 -266 L10 -266 Q24 -266 24 -250 L24 -226 L-80 -226 Z" fill="none" stroke="#6d1414" stroke-width="12" stroke-linejoin="round"/>'
            '<path d="M-90 -190 L90 -40 M90 -190 L-90 -40" stroke="#b71c1c" stroke-width="10" opacity=".55"/>'
            '<rect x="-100" y="-210" width="200" height="190" rx="10" fill="none" stroke="#b71c1c" stroke-width="8" opacity=".55"/>'
            '<path d="M60 -270 L100 -320 L120 -306 L88 -256 Z" fill="#424242"/><rect x="92" y="-336" width="34" height="22" rx="6" fill="#212121" transform="rotate(35 108 -324)"/>'
            '<path d="M-96 -230 L-96 -40" stroke="#ff8a80" stroke-width="8" opacity=".6" stroke-linecap="round"/></g>')


def disli(r, dis=12, catlak=True):
    pts = []
    for k in range(dis * 2):
        a = math.pi * k / dis
        rr = r if k % 2 == 0 else r * .8
        for d in (-.12, .12):
            pts.append(f"{math.cos(a+d)*rr:.1f},{math.sin(a+d)*rr:.1f}")
    g = (f'<polygon points="{" ".join(pts)}" fill="url(#dislisi)" stroke="#455a64" stroke-width="4"/>'
         f'<circle r="{r*.55}" fill="#b0bec5" stroke="#546e7a" stroke-width="4"/><circle r="{r*.22}" fill="#37474f"/>'
         + "".join(f'<circle cx="{math.cos(k*math.pi/3)*r*.38:.1f}" cy="{math.sin(k*math.pi/3)*r*.38:.1f}" r="{r*.07:.1f}" fill="#546e7a"/>' for k in range(6)))
    if catlak:
        g += f'<path class="catlak" d="M{r*.2} {-r*.9} L{r*.05} {-r*.6} L{r*.22} {-r*.45} L{r*.02} {-r*.2}" stroke="#d32f2f" stroke-width="6" fill="none" stroke-linejoin="round"/>'
    return g


def ikon(tur, x, y, r=56):
    c = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F7F1E3" stroke="#2F5737" stroke-width="6"/>'
    if tur == "agirlik":
        c += f'<path d="M{x-34} {y+34} L{x-24} {y-14} L{x+24} {y-14} L{x+34} {y+34} Z" fill="#2F5737"/><circle cx="{x}" cy="{y-26}" r="14" fill="none" stroke="#2F5737" stroke-width="8"/><text x="{x}" y="{y+22}" font-size="26" text-anchor="middle" fill="#fff" font-weight="800">kg</text>'
    elif tur == "cekis":
        c += f'<circle cx="{x-6}" cy="{y+4}" r="30" fill="#2F5737"/><circle cx="{x-6}" cy="{y+4}" r="14" fill="#E2B654"/>' + "".join(
            f'<rect x="{x-11}" y="{y-30}" width="10" height="10" fill="#2F5737" transform="rotate({a} {x-6} {y+4})"/>' for a in range(0, 360, 45)) + f'<path d="M{x+22} {y-26} L{x+44} {y-26} L{x+36} {y-36} M{x+44} {y-26} L{x+36} {y-16}" stroke="#E2B654" stroke-width="6" fill="none" stroke-linecap="round"/>'
    elif tur == "arazi":
        c += f'<path d="M{x-46} {y+30} L{x-14} {y-22} L{x+4} {y+4} L{x+22} {y-14} L{x+46} {y+30} Z" fill="#2F5737"/><path d="M{x-14} {y-22} L{x-4} {y-6} L{x-20} {y-10} Z" fill="#fff"/><circle cx="{x+26}" cy="{y-30}" r="10" fill="#E2B654"/>'
    elif tur == "derinlik":
        c += f'<rect x="{x-44}" y="{y-4}" width="88" height="40" rx="6" fill="#8d6e4a"/><path d="M{x-6} {y-42} L{x-6} {y+18} L{x+14} {y+26} L{x+6} {y-42} Z" fill="#2F5737"/>' + "".join(
            f'<rect x="{x+18}" y="{y-34+k*14}" width="14" height="4" fill="#2F5737"/>' for k in range(4))
    return c


def terazi():
    g = ('<g class="terazi"><rect x="510" y="760" width="60" height="420" rx="14" fill="#8d6e63"/><rect x="520" y="770" width="16" height="400" rx="8" fill="#a1887f"/>'
         '<path d="M400 1180 Q540 1120 680 1180 Z" fill="#6d4c41"/><circle cx="540" cy="760" r="30" fill="#E2B654" stroke="#a87b1f" stroke-width="5"/>'
         '<g class="kiris"><rect x="200" y="742" width="680" height="34" rx="17" fill="#E2B654" stroke="#a87b1f" stroke-width="5"/>'
         '<circle cx="220" cy="759" r="12" fill="#a87b1f"/><circle cx="860" cy="759" r="12" fill="#a87b1f"/></g>')
    for cls, inner in [("kefe1", f'<g transform="translate(-48 -46) scale(.3)">{traktor("mutlu")}</g>'),
                       ("kefe2", f'<g transform="translate(76 -112) scale(.48)">{pulluk(3, 1)}</g>')]:
        g += (f'<g class="{cls}"><path d="M0 0 L-110 240 M0 0 L110 240" stroke="#a87b1f" stroke-width="4"/>'
              f'<g transform="translate(0 240)">{inner}<path d="M-140 0 Q0 60 140 0 Z" fill="#E2B654" stroke="#a87b1f" stroke-width="5"/></g></g>')
    return g + '</g>'


def telefon():
    g = ('<g transform="translate(600 620) scale(.88)" filter="url(#golge)"><rect width="420" height="760" rx="56" fill="url(#telefon)"/>'
         '<rect x="18" y="18" width="384" height="724" rx="42" fill="#f6f7f9"/><rect x="160" y="32" width="100" height="22" rx="11" fill="#15181b"/>'
         '<text x="44" y="118" font-size="34" font-weight="900" fill="#14281A">Yorumlar</text><text x="372" y="118" font-size="34" text-anchor="end" fill="#90a4ae">✕</text>'
         '<rect x="36" y="138" width="348" height="3" fill="#e0e0e0"/>')
    for i, w in enumerate([260, 200, 290]):
        y = 176 + i * 120
        g += (f'<g class="yr" data-i="{i}"><circle cx="70" cy="{y+30}" r="28" fill="{["#a5d6a7","#ffcc80","#90caf9"][i]}"/>'
              f'<rect x="112" y="{y+6}" width="120" height="18" rx="9" fill="#cfd8dc"/><rect x="112" y="{y+36}" width="{w}" height="16" rx="8" fill="#e3e7ea"/>'
              f'<rect x="112" y="{y+62}" width="{w-70}" height="16" rx="8" fill="#e3e7ea"/></g>')
    g += ('<rect x="30" y="610" width="360" height="96" rx="48" fill="#fff" stroke="#2F5737" stroke-width="4"/>'
          '<text class="yazi" x="62" y="670" font-size="30" font-weight="700" fill="#14281A"></text>'
          '<rect class="imlec" x="62" y="638" width="4" height="40" fill="#2F5737"/>'
          '<g class="gonder"><circle cx="342" cy="658" r="34" fill="#2F5737"/><path d="M326 642 L362 658 L326 674 L332 658 Z" fill="#E2B654"/></g></g>')
    return g


def etiket(x, y, tx, ty, metin, gecikme=0, renk="#c62828"):
    """Oklu açıklama etiketi; (x,y) etiket merkezi, (tx,ty) gösterdiği nokta. gecikme: kare."""
    w = len(metin) * 24 + 56
    return (f'<g class="etk" data-g="{gecikme}" data-x="{x}" data-y="{y}" opacity="0">'
            f'<path d="M{x} {y} L{tx} {ty}" stroke="#14281A" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/>'
            f'<circle cx="{tx}" cy="{ty}" r="12" fill="{renk}" stroke="#fff" stroke-width="5"/>'
            f'<rect x="{x-w/2}" y="{y-38}" width="{w}" height="76" rx="38" fill="#fff" stroke="{renk}" stroke-width="6" filter="url(#golge)"/>'
            f'<text x="{x}" y="{y+14}" text-anchor="middle" font-size="40" font-weight="900" fill="{renk}">{metin}</text></g>')


def saat(x, y, r=86):
    return (f'<g transform="translate({x} {y})" filter="url(#golge)">'
            f'<path d="M{-r*.75} {-r*.75} L{-r*.95} {-r*1.05} M{r*.75} {-r*.75} L{r*.95} {-r*1.05}" stroke="#263238" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="{-r*.62}" cy="{-r*.95}" r="{r*.3}" fill="#c62828"/><circle cx="{r*.62}" cy="{-r*.95}" r="{r*.3}" fill="#c62828"/>'
            f'<circle r="{r}" fill="#fff" stroke="#263238" stroke-width="12"/>'
            + "".join(f'<rect x="-4" y="{-r*.86}" width="8" height="{r*.16}" rx="4" fill="#263238" transform="rotate({k*30})"/>' for k in range(12)) +
            f'<g class="akrep"><rect x="-6" y="{-r*.5}" width="12" height="{r*.56}" rx="6" fill="#263238"/></g>'
            f'<g class="yelkovan"><rect x="-4" y="{-r*.76}" width="8" height="{r*.82}" rx="4" fill="#c62828"/></g>'
            f'<circle r="10" fill="#263238"/></g>')


def kart(x, y, no, baslik, icerik, ts, w=460, h=470):
    return (f'<g class="kart" data-ts="{ts:.3f}" data-x="{x+w/2}" data-y="{y+h/2}" opacity="0">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="#fff" filter="url(#golge)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="92" rx="34" fill="#2F5737"/><rect x="{x}" y="{y+60}" width="{w}" height="32" fill="#2F5737"/>'
            f'<circle cx="{x+50}" cy="{y+46}" r="28" fill="#E2B654"/><text x="{x+50}" y="{y+58}" text-anchor="middle" font-size="34" font-weight="900" fill="#14281A">{no}</text>'
            f'<text x="{x+92}" y="{y+59}" font-size="34" font-weight="900" fill="#fff">{baslik}</text>'
            f'<g class="tik" opacity="0"><circle cx="{x+w-34}" cy="{y+46}" r="24" fill="#43a047" stroke="#fff" stroke-width="4"/><path d="M{x+w-46} {y+46} L{x+w-37} {y+55} L{x+w-20} {y+36}" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
            f'<g transform="translate({x} {y})">{icerik}</g></g>')


def kart_agirlik():
    return ('<g class="okl">' + "".join(f'<path d="M{x} 118 v52 m-22 -22 l22 26 l22 -26" stroke="#c62828" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for x in (70, 390)) + '</g>'
            f'<g transform="translate(160 372) scale(.27)">{traktor("normal")}</g>'
            '<rect x="40" y="372" width="380" height="24" rx="8" fill="#90a4ae"/><rect x="40" y="372" width="380" height="7" rx="3" fill="#cfd8dc"/>'
            '<rect x="64" y="396" width="332" height="44" rx="8" fill="#546e7a"/><rect x="170" y="404" width="120" height="30" rx="6" fill="#102027"/>'
            '<text class="kg" x="230" y="428" text-anchor="middle" font-size="26" font-weight="800" fill="#76ff03" font-family="monospace">kg</text>')


def kart_cekis():
    izler = "".join(f'<path d="M{x} 384 l14 -12 l14 12" stroke="#5a3d24" stroke-width="7" fill="none" stroke-linecap="round"/>' for x in range(10, 120, 32))
    return ('<rect x="0" y="360" width="460" height="110" fill="#8a6440"/><rect x="0" y="352" width="460" height="12" fill="#6b9a3e"/>' + izler +
            teker(210, 250, 110) + '<g class="topr"></g>'
            '<g class="ok"><path d="M336 250 H420" stroke="#43a047" stroke-width="26" stroke-linecap="round"/><path d="M402 214 L446 250 L402 286 Z" fill="#43a047"/></g>')


def kart_arazi():
    g = '<rect x="20" y="118" width="420" height="16" rx="6" fill="#6b9a3e"/>'
    kol = [(30, "#8d5a3b", "Killi"), (172, "#9a7149", "Taşlı"), (314, "#e3c08a", "Kumlu")]
    for i, (x, c, ad) in enumerate(kol):
        g += f'<g class="kolon" data-i="{i}"><rect x="{x}" y="134" width="116" height="250" fill="{c}"/>'
        if ad == "Killi":
            g += "".join(f'<path d="M{x+20+k*30} {150+k*60} l12 18 l-8 14 l14 20" stroke="#5d3a22" stroke-width="4" fill="none"/>' for k in range(3))
        elif ad == "Taşlı":
            g += "".join(f'<ellipse cx="{x+18+(k*37)%90}" cy="{160+k*26}" rx="{10+k%3*5}" ry="{7+k%2*4}" fill="#9e9e9e" stroke="#616161" stroke-width="2"/>' for k in range(9))
        else:
            g += "".join(f'<circle cx="{x+10+(k*23)%100}" cy="{146+(k*37)%230}" r="3" fill="#b58a55"/>' for k in range(40))
        g += f'<text x="{x+58}" y="432" text-anchor="middle" font-size="34" font-weight="900" fill="#14281A">{ad}</text></g>'
    return g


def kart_derinlik():
    g = ('<rect x="20" y="118" width="420" height="14" rx="6" fill="#6b9a3e"/>'
         '<rect x="20" y="132" width="420" height="120" fill="#6f4b2c"/><rect x="20" y="252" width="420" height="130" fill="#a1795a"/>'
         '<rect x="20" y="382" width="420" height="60" fill="#8d8d8d"/>'
         + "".join(f'<path d="M{x} 134 q-6 30 4 60" stroke="#c9a26a" stroke-width="3" fill="none"/>' for x in range(150, 440, 40))
         + "".join(f'<ellipse cx="{30+(k*53)%400}" cy="{396+(k*17)%40}" rx="14" ry="9" fill="#616161"/>' for k in range(12))
         + '<rect x="40" y="132" width="44" height="300" rx="6" fill="#fff8e1" stroke="#8d6e63" stroke-width="3"/>')
    for k in range(0, 5):
        yy = 132 + k * 70
        g += f'<path d="M40 {yy} h22" stroke="#5d4037" stroke-width="4"/><text x="94" y="{yy+10}" font-size="24" font-weight="800" fill="#fff">{k*10}</text>'
    g += '<text x="62" y="460" text-anchor="middle" font-size="24" font-weight="800" fill="#14281A">cm</text>'
    g += ('<g class="govde"><path d="M330 -60 L330 0" stroke="#8e1c1c" stroke-width="18" stroke-linecap="round"/>'
          '<path d="M360 40 L334 -10 Q294 -30 236 -18 Q262 8 266 40 Z" fill="url(#metal)" stroke="#55656d" stroke-width="3"/>'
          '<path d="M390 42 L350 28 L262 38 L266 50 Z" fill="#37474f"/></g>'
          '<path class="cizgi" d="M130 0 H440" stroke="#FFD54F" stroke-width="5" stroke-dasharray="14 10"/>')
    return g


# ---------------------------------------------------------------- sahneler
def sahne_svg(ad, p=None):
    if ad == "kanca":   # gücünden büyük pulluk: traktör şaha kalkıyor, kara duman
        return (gok() + tarla(sur_x=380) +
                f'<g class="hareket" transform="translate(690 {YER}) scale(.66)">{traktor("endise")}'
                f'<g transform="translate(-235 -120)">{pulluk(5, 1.2, toprak=True)}</g></g>'
                + on_toprak(-40, 560, YER + 4, 96) +
                '<g class="sicrama"></g>' + etiket(250, 930, 300, 1125, "AĞIR PULLUK", 14) + etiket(470, 640, 650, 800, "ZORLANAN TRAKTÖR", 34) +
                '<g class="uyari" opacity="0"><path d="M940 640 L1000 750 L880 750 Z" fill="#fbc02d" stroke="#5d4037" stroke-width="8" stroke-linejoin="round"/>'
                '<rect x="934" y="670" width="12" height="46" rx="6" fill="#5d4037"/><circle cx="940" cy="734" r="7" fill="#5d4037"/></g>')
    if ad == "secim":   # çiftçi en büyük pulluğu gösteriyor
        g = gok("#cfeaff", "#fff4dc") + tarla()
        g += (f'<g class="sec" data-i="0" data-x="1050" data-y="1060">{pulluk(6, .72)}</g>'
              '<g class="etiket" data-i="0" opacity="0"><path d="M820 840 L820 960" stroke="#5d4037" stroke-width="4"/><rect x="740" y="760" width="160" height="84" rx="16" fill="#E2B654" stroke="#a87b1f" stroke-width="5"/><text x="820" y="818" text-anchor="middle" font-size="44" font-weight="900" fill="#14281A">6\'lı</text></g>'
              f'<g class="sec" data-i="1" data-x="640" data-y="1130">{pulluk(2, .62)}</g>'
              '<g class="etiket" data-i="1" opacity="0"><path d="M540 950 L540 1040" stroke="#5d4037" stroke-width="4"/><rect x="470" y="876" width="140" height="78" rx="16" fill="#fff" stroke="#bdbdbd" stroke-width="5"/><text x="540" y="930" text-anchor="middle" font-size="40" font-weight="900" fill="#14281A">2\'li</text></g>'
              f'<g class="adam" transform="translate(190 {YER+40})">{ciftci("isaret", "mutlu")}</g>'
              '<g class="parilti"></g>'
              '<g class="balon" opacity="0"><path d="M90 300 Q90 250 140 250 L900 250 Q950 250 950 300 L950 450 Q950 500 900 500 L330 500 L240 590 L260 500 L140 500 Q90 500 90 450 Z" fill="#fff" stroke="#2b2b2b" stroke-width="6" filter="url(#golge)"/>'
              '<text x="520" y="360" text-anchor="middle" font-size="58" font-weight="900" fill="#2b2b2b">"Büyük olsun,</text>'
              '<text x="520" y="440" text-anchor="middle" font-size="58" font-weight="900" fill="#c62828">iş çabuk bitsin!"</text></g>')
        return g
    if ad == "hiz":     # hız göstergesi düşüyor, salyangoz traktörü geçiyor
        g = gok("#ffe9cf", "#fff6e6") + tarla(sur_x=330)
        g += kadran(540, 760, 330, "hiz")
        g += f'<text x="540" y="850" text-anchor="middle" font-size="58" font-weight="900" fill="#263238">ÇALIŞMA HIZI</text>'
        g += (f'<g class="hareket" transform="translate(560 {YER}) scale(.42)">{traktor("endise")}<g transform="translate(-235 -120)">{pulluk(6, 1.2, toprak=True)}</g></g>'
              + on_toprak(0, 420, YER + 2) + etiket(900, 930, 760, 1100, "YAVAŞ!", 26) + f'<g class="slyk" transform="translate(110 1300) scale(.8)">{salyangoz()}</g>')
        return g
    if ad == "patinaj":  # yakın plan: teker gömülüyor, çamur sıçrıyor
        g = gok("#e3edf2", "#f7f3e8", gunes=False) + tarla()
        g += ('<g class="cukur"><ellipse cx="560" cy="1232" rx="330" ry="46" fill="#3e2a17"/></g>'
              '<g class="titre"><path d="M190 900 A370 370 0 0 1 930 900 L880 900 A320 320 0 0 0 240 900 Z" fill="url(#kaput)"/>'
              '<path d="M210 860 A360 360 0 0 1 420 590" stroke="#a9d1ff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".6"/>'
              '<rect x="880" y="700" width="200" height="120" rx="30" fill="url(#kaput)"/><rect x="930" y="684" width="40" height="22" rx="6" fill="#222"/>'
              '<path d="M950 820 L950 980 M920 870 H990 M920 930 H990" stroke="#2b2b2b" stroke-width="12" stroke-linecap="round"/>'
              + teker(560, 990, 285, "buyuk") + '</g>'
              '<g class="toz"></g>' + on_toprak(180, 950, 1234) +
              '<g class="hiz-cizgi"></g>' + saat(130, 660) +
              '<g class="patlama" transform="translate(540 450)"><polygon points="' +
              " ".join(f"{math.cos(math.pi*k/9)*(300 if k%2==0 else 200):.0f},{math.sin(math.pi*k/9)*(150 if k%2==0 else 100):.0f}" for k in range(18)) +
              '" fill="#fbc02d" stroke="#5d4037" stroke-width="8" stroke-linejoin="round"/>'
              '<text y="34" text-anchor="middle" font-size="104" font-weight="900" fill="#c62828" stroke="#fff" stroke-width="8" paint-order="stroke">PATİNAJ!</text></g>')
        return g
    if ad == "yakit":    # yakıt göstergesi E'ye iniyor, para uçuyor, dişli çatlıyor
        g = gok("#ffeedd", "#fff8ef", gunes=False, manzara=False)
        g += '<rect x="0" y="1180" width="1080" height="740" fill="url(#tarla)"/><rect x="0" y="1172" width="1080" height="16" fill="#6b9a3e"/>'
        g += kadran(540, 700, 320, "yakit")
        g += '<text x="540" y="790" text-anchor="middle" font-size="58" font-weight="900" fill="#263238">YAKIT</text>'
        g += f'<g transform="translate(260 1186)">{bidon()}</g><g class="damla"></g>'
        g += '<g class="paralar"></g>'
        g += (f'<g class="disli1" transform="translate(800 1010)">{disli(120)}</g><g class="disli2" transform="translate(952 1104)">{disli(70, 9, False)}</g>'
              '<g class="yipran" opacity="0"><rect x="640" y="1180" width="400" height="76" rx="38" fill="#fff" filter="url(#golge)"/>'
              '<text x="840" y="1232" text-anchor="middle" font-size="40" font-weight="900" fill="#c62828">⚠ Yıpranma</text></g>')
        return g
    if ad == "kural":
        g = '<rect width="1080" height="1920" fill="#F7F1E3"/>'
        g += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#efe5cc"/>' for x, y, r in [(120, 520, 90), (980, 1220, 140), (900, 260, 60), (160, 1250, 50)])
        g += ('<g class="rozet" filter="url(#golge)"><rect x="190" y="300" width="700" height="120" rx="60" fill="#2F5737"/>'
              '<text x="540" y="382" text-anchor="middle" font-size="62" font-weight="900" fill="#E2B654">✅ ALTIN KURAL</text></g>')
        g += '<text class="t1" x="540" y="530" text-anchor="middle" font-size="58" font-weight="800" fill="#2b2b2b">Sadece beygire bakma!</text>'
        g += terazi()
        for i, (t, l) in enumerate([("agirlik", "Traktör ağırlığı"), ("cekis", "Çekiş gücü"), ("arazi", "Arazi yapısı"), ("derinlik", "Çalışma derinliği")]):
            y = 680 + i * 160
            g += (f'<g class="madde" data-i="{i}" opacity="0"><rect x="110" y="{y-66}" width="860" height="132" rx="66" fill="#fff" stroke="#e0d7c0" stroke-width="4" filter="url(#golge)"/>'
                  f'{ikon(t, 186, y, 52)}<text x="270" y="{y+20}" font-size="56" font-weight="800" fill="#2F5737">{l}</text>'
                  f'<g class="tik" opacity="0"><circle cx="900" cy="{y}" r="36" fill="#43a047"/><path d="M882 {y} L895 {y+14} L920 {y-14}" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>')
        return g
    if ad == "dogru":    # doğru eşleşme: rahat sürüm, martılar
        g = gok() + tarla(sur_x=420, sur_cls="dinamik")
        g += (f'<g class="hareket" transform="translate(600 {YER}) scale(.66)">{traktor("mutlu")}<g transform="translate(-235 -120)">{pulluk(3, 1.0, toprak=True)}</g></g>'
              '<g class="ontop"></g><g class="kuslar"></g>' + etiket(300, 880, 250, 1140, "UYUMLU PULLUK", 40, "#2e7d32"))
        g += ('<g class="onay" opacity="0"><circle cx="540" cy="400" r="116" fill="#43a047" filter="url(#golge)"/><circle cx="540" cy="400" r="96" fill="none" stroke="#a5d6a7" stroke-width="6"/>'
              '<path d="M482 400 L528 446 L606 354" stroke="#fff" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
        for i, t in enumerate(["⛽ Daha az yakıt", "😌 Daha rahat iş"]):
            g += (f'<g class="cip" data-i="{i}" opacity="0"><rect x="{100+i*460}" y="560" width="420" height="104" rx="52" fill="#fff" filter="url(#golge)"/>'
                  f'<text x="{310+i*460}" y="628" text-anchor="middle" font-size="46" font-weight="800" fill="#2F5737">{t}</text></g>')
        return g
    if ad == "dort":
        ts = (p or {}).get("_kart_ts", [0.3, 1.3, 2.3, 3.3])
        g = '<rect width="1080" height="1920" fill="#F7F1E3"/>'
        g += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#efe5cc"/>' for x, y, r in [(120, 1320, 90), (980, 1300, 120), (1000, 240, 60)])
        g += ('<g class="rozet2"><rect x="290" y="190" width="500" height="80" rx="40" fill="#E2B654"/>'
              '<text x="540" y="244" text-anchor="middle" font-size="40" font-weight="900" fill="#14281A">BİRLİKTE DÜŞÜN</text></g>')
        g += kart(60, 300, 1, "Traktör ağırlığı", kart_agirlik(), ts[0])
        g += kart(560, 300, 2, "Çekiş gücü", kart_cekis(), ts[1])
        g += kart(60, 800, 3, "Arazi yapısı", kart_arazi(), ts[2])
        g += kart(560, 800, 4, "Çalışma derinliği", kart_derinlik(), ts[3])
        return g
    if ad == "soru":
        g = '<rect width="1080" height="1920" fill="#2F5737"/>'
        g += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70), (200, 1650, 90)])
        g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
        g += ('<g class="takip"><circle cx="540" cy="330" r="104" fill="#F7F1E3" stroke="#E2B654" stroke-width="10" filter="url(#golge)"/>'
              '<image href="LOGO" x="452" y="242" width="176" height="176"/>'
              '<g class="buton"><rect class="btn" x="365" y="462" width="350" height="100" rx="50" fill="#FE2C55" filter="url(#golge)"/>'
              '<text class="btnyazi" x="540" y="527" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">+ Takip et</text></g>'
              '<text class="el" x="640" y="640" font-size="120">👆</text></g>')
        g += ('<g class="soru"><path d="M40 560 Q40 480 120 480 L220 480 Q300 480 300 560 Q300 640 220 640 L200 640 L220 700 L160 640 L120 640 Q40 640 40 560 Z" fill="#fff" filter="url(#golge)"/>'
              '<text x="170" y="610" text-anchor="middle" font-size="130" font-weight="900" fill="#E2B654" stroke="#14281A" stroke-width="6" paint-order="stroke">?</text></g>')
        g += f'<g transform="translate(250 1300) scale(1.0)">{ciftci("salla", "mutlu")}</g>'
        g += telefon()
        return g
    raise ValueError(ad)


JS = r"""
const FPS=30, $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), ease=x=>1-Math.pow(1-cl(x,0,1),3);
function spring(f,k=0.16){ if(f<=0) return 0; return 1-Math.exp(-k*f)*Math.cos(f*0.24); }
function wheels(el,t,sp){ $$('.whl',el).forEach(w=>{const cx=+w.dataset.cx, cy=+w.dataset.cy, k=w.classList.contains('on')?1.65:1; w.setAttribute('transform',`rotate(${t*sp*k} ${cx} ${cy})`);}); }
function clouds(el,t){ $$('.bulut',el).forEach(b=>{ const x=((+b.dataset.x + t*(+b.dataset.sp) + 300)%1700)-300; b.setAttribute('transform',`translate(${x} ${b.dataset.y})`); }); }
function puffs(g,t,x,y,n=6,c='#555',big=1){ if(!g) return; let s=''; for(let i=0;i<n;i++){ const p=((t*1.6+i*14)%84)/84; s+=`<circle cx="${x-p*90*big}" cy="${y-p*240}" r="${(16+p*54)*big}" fill="${c}" opacity="${((1-p)*0.6).toFixed(2)}"/>`;} g.innerHTML=s; }
function beacon(el,t){ $$('.tepe',el).forEach(g=>{ const o=(Math.sin(t*0.5)+1)/2; g.innerHTML=`<circle cx="60" cy="-724" r="${30+o*18}" fill="#ffb300" opacity="${(0.15+o*0.25).toFixed(2)}"/>`; }); }
function sweat(el,t){ $$('.ter',el).forEach(g=>{ const p=(t%30)/30; g.setAttribute('opacity',(1-p).toFixed(2)); g.setAttribute('transform',`translate(0 ${p*40})`); }); }
function kuslar(g,x0,y0,t){ let s=''; [[0,0],[90,-60],[170,10]].forEach(([dx,dy],i)=>{ const x=x0+dx+Math.sin(t*0.05+i)*30, y=y0+dy+Math.sin(t*0.08+i*2)*16, h=18*Math.sin(t*0.45+i*1.7);
  s+=`<path d="M${x-40} ${y} Q${x-20} ${y-h-8} ${x} ${y} Q${x+20} ${y-h-8} ${x+40} ${y}" stroke="#37474f" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="${x}" cy="${y+2}" r="6" fill="#eceff1" stroke="#37474f" stroke-width="3"/>`; }); g.innerHTML=s; }
const SAHNE={
 kanca(el,t){ clouds(el,t); wheels(el,t,0.9); beacon(el,t); sweat(el,t);
   const tilt=-1.5-2.5*Math.max(0,Math.sin(t*0.22)), j=Math.sin(t*2.3)*2.5;
   $('.hareket',el).setAttribute('transform',`translate(${690+j} ${1222+Math.abs(Math.sin(t*1.7))*-3}) rotate(${tilt}) scale(.66)`);
   puffs($('.duman',el),t,312,-570,8,'#2b2b2b',1.4);
   let s=''; for(let i=0;i<10;i++){ const p=((t*1.3+i*9)%50)/50; s+=`<circle cx="${560-p*90-i*6}" cy="${1200-Math.sin(p*Math.PI)*90}" r="${6+(i%3)*3}" fill="#6f4b2c" opacity="${(1-p).toFixed(2)}"/>`;} $('.sicrama',el).innerHTML=s;
   const u=$('.uyari',el); u.setAttribute('opacity', t>24? (0.6+0.4*Math.sin(t*0.6)).toFixed(2):0); },
 secim(el,t){ clouds(el,t);
   $$('.sec',el).forEach(g=>{const i=+g.dataset.i, s=spring(t-4-i*10); g.style.opacity=Math.min(1,s*1.5); g.setAttribute('transform',`translate(${g.dataset.x} ${+g.dataset.y - (1-Math.min(1,s))*360})`);});
   $$('.etiket',el).forEach(g=>{const i=+g.dataset.i; g.setAttribute('opacity', ease((t-22-i*8)/8)); });
   const a=$('.adam',el); a.setAttribute('transform',`translate(190 ${1262 + Math.abs(Math.sin(t*0.18))*-6})`);
   $('.balon',el).setAttribute('opacity', ease((t-34)/10)); $('.balon',el).setAttribute('transform',`translate(0 ${(1-ease((t-34)/10))*30})`);
   let s=''; if(t>26){ for(let i=0;i<5;i++){ const p=((t+i*11)%40)/40, x=[640,760,900,1000,700][i], y=[880,830,860,930,960][i]; s+=`<path d="M${x} ${y-24*p} l6 -18 l6 18 l18 6 l-18 6 l-6 18 l-6 -18 l-18 -6 Z" fill="#fff59d" opacity="${(Math.sin(p*Math.PI)).toFixed(2)}"/>`;} } $('.parilti',el).innerHTML=s; },
 hiz(el,t){ clouds(el,t); const v=14-11*ease(t/40)+0.6*Math.sin(t*0.5); $('.ibre',el).setAttribute('transform',`rotate(${-90+v/40*180})`);
   wheels(el,t,0.25); beacon(el,t); sweat(el,t); puffs($('.duman',el),t,312,-570,6,'#3a3a3a',1.2);
   $('.hareket',el).setAttribute('transform',`translate(${560+t*0.25} 1222) scale(.42)`);
   const sx=110+t*4.2; $('.slyk',el).setAttribute('transform',`translate(${sx} 1300) scale(.8)`);
   const st=1+0.06*Math.sin(t*0.6); $('.slygov',el).setAttribute('transform',`scale(${st} 1)`); },
 patinaj(el,t){ clouds(el,t); wheels(el,t,16); const ak=$('.akrep',el), yk=$('.yelkovan',el); if(ak){ ak.setAttribute('transform',`rotate(${t*2})`); yk.setAttribute('transform',`rotate(${t*24})`); }
   $('.titre',el).setAttribute('transform',`translate(${Math.sin(t*3.1)*5} ${Math.sin(t*2.3)*4+Math.min(t,40)*0.5})`);
   let s=''; for(let i=0;i<34;i++){ const p=((t*2.2+i*7)%60)/60, ang=(196+(i%9)*5)*Math.PI/180, sp=380+(i%5)*70;
     s+=`<ellipse cx="${560+Math.cos(ang)*(285+p*sp)}" cy="${1170+Math.sin(ang)*sp*p*0.9+p*p*420}" rx="${9+(i%4)*5}" ry="${7+(i%3)*4}" fill="${i%3?'#5a3d24':'#7a5634'}" opacity="${(1-p).toFixed(2)}"/>`;} $('.toz',el).innerHTML=s;
   let c=''; for(let i=0;i<3;i++){ const a=Math.PI*1.08+((t*0.25+i*0.9)%(Math.PI*0.75)); c+=`<path d="M${560+Math.cos(a)*340} ${990+Math.sin(a)*340} A340 340 0 0 1 ${560+Math.cos(a+0.45)*340} ${990+Math.sin(a+0.45)*340}" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".7"/>`;} $('.hiz-cizgi',el).innerHTML=c;
   const b=spring(t-2,0.2), pu=1+0.04*Math.sin(t*0.7); $('.patlama',el).setAttribute('transform',`translate(540 450) scale(${b*pu}) rotate(${Math.sin(t*0.3)*3})`); },
 yakit(el,t){ clouds(el,t); const lv=1-ease(t/80)*0.92; $('.ibre',el).setAttribute('transform',`rotate(${-80+lv*160})`);
   $('.lamba',el).setAttribute('opacity', lv<0.3 ? ((Math.sin(t*0.8)+1)/2).toFixed(2) : 0);
   let s=''; for(let i=0;i<4;i++){ const p=((t*1.5+i*20)%80)/80; s+=`<path d="M${356} ${1050+p*120} q14 24 0 36 q-14 -12 0 -36" fill="#ffb300" opacity="${(1-p).toFixed(2)}"/>`;} $('.damla',el).innerHTML=s;
   let m=''; for(let i=0;i<6;i++){ const p=((t*1.1+i*16)%96)/96; if(t<8+i*6) continue; const x=380+p*260+Math.sin(p*6+i)*50, y=1120-p*300, r=(t*4+i*60)%360;
     m+=`<g transform="translate(${x} ${y}) rotate(${r*0.4-20})" opacity="${Math.sin(p*Math.PI).toFixed(2)}"><rect x="-70" y="-38" width="140" height="76" rx="8" fill="url(#para)" stroke="#2e7d32" stroke-width="4"/><circle r="22" fill="none" stroke="#2e7d32" stroke-width="4"/><text y="12" text-anchor="middle" font-size="32" font-weight="900" fill="#1b5e20">₺</text></g>`;} $('.paralar',el).innerHTML=m;
   $('.disli1',el).setAttribute('transform',`translate(800 1010) rotate(${t*1.2})`); $('.disli2',el).setAttribute('transform',`translate(952 1104) rotate(${-t*2.06+10})`);
   const y=$('.yipran',el); y.setAttribute('opacity', ease((t-40)/12)); },
 kural(el,t){ const KT=window.KURAL_T||110; const r=spring(t-2); $('.rozet',el).setAttribute('transform',`translate(540 360) scale(${r}) translate(-540 -360)`); $('.t1',el).setAttribute('opacity', ease((t-10)/10));
   const tz=$('.terazi',el), fo=1-ease((t-KT+12)/10); tz.setAttribute('opacity', (ease((t-8)/12)*fo).toFixed(2));
   const ang=16*Math.exp(-Math.max(0,t-30)/40)*Math.cos(Math.max(0,t-30)*0.12)*(t<30?1:1);
   $('.kiris',el).setAttribute('transform',`rotate(${-ang} 540 759)`);
   const rad=-ang*Math.PI/180, L=320; const p1=[540-Math.cos(rad)*L, 759-Math.sin(rad)*L], p2=[540+Math.cos(rad)*L, 759+Math.sin(rad)*L];
   $('.kefe1',el).setAttribute('transform',`translate(${p1[0]} ${p1[1]})`); $('.kefe2',el).setAttribute('transform',`translate(${p2[0]} ${p2[1]})`);
   $$('.madde',el).forEach(g=>{const i=+g.dataset.i, s=ease((t-KT-i*22)/12); g.setAttribute('opacity', s); g.setAttribute('transform',`translate(${(1-s)*-200} 0)`); $('.tik',g).setAttribute('opacity', ease((t-KT-i*22-10)/6));}); },
 dogru(el,t){ clouds(el,t); wheels(el,t,2.2); beacon(el,t); const x=520+t*1.4;
   $('.hareket',el).setAttribute('transform',`translate(${x} ${1222+Math.sin(t*0.9)*1.5}) scale(.66)`);
   puffs($('.duman',el),t,312,-570,4,'#9e9e9e',.8);
   const sr=$('.surulmus rect',el); if(sr) sr.setAttribute('width', x-150);
   kuslar($('.kuslar',el), x-520, 900, t);
   const s=spring(t-8); $('.onay',el).setAttribute('opacity',Math.min(1,s)); $('.onay',el).setAttribute('transform',`translate(540 400) scale(${s}) translate(-540 -400)`);
   $$('.cip',el).forEach(g=>{const i=+g.dataset.i, e=ease((t-28-i*14)/10); g.setAttribute('opacity', e); g.setAttribute('transform',`translate(0 ${(1-e)*30})`);}); },
 dort(el,t){ const sn=t/FPS; $('.rozet2',el).setAttribute('opacity', ease(t/8)); wheels(el,t,3);
   $$('.kart',el).forEach((g,i)=>{ const e=spring((sn-(+g.dataset.ts))*FPS+4,0.22), x=+g.dataset.x, y=+g.dataset.y; g.setAttribute('opacity',Math.min(1,e*1.6).toFixed(2)); g.setAttribute('transform',`translate(${x} ${y}) scale(${0.6+0.4*Math.min(e,1.08)}) translate(${-x} ${-y})`);
     const tk=$('.tik',g); tk.setAttribute('opacity', ease((sn-(+g.dataset.ts))*FPS/6-2)); });
   $$('.okl path',el).forEach((p,i)=>p.setAttribute('transform',`translate(0 ${Math.abs(Math.sin(t*0.2+i))*14})`));
   const kg=$('.kg',el); if(kg) kg.textContent = (Math.min(1,Math.max(0,(sn-(+$$('.kart',el)[0].dataset.ts))/1.2))*100<99 ? Math.floor(Math.random()*9000+1000) : '✓ kg');
   const ok=$('.ok',el); if(ok) ok.setAttribute('transform',`translate(${Math.sin(t*0.4)*10} 0)`);
   let s=''; for(let i=0;i<6;i++){ const p=((t*1.4+i*10)%40)/40; s+=`<circle cx="${110-p*90}" cy="${350-Math.sin(p*Math.PI)*70}" r="${5+i%3*2}" fill="#6f4b2c" opacity="${(1-p).toFixed(2)}"/>`; } const tp=$('.topr',el); if(tp) tp.innerHTML=s;
   $$('.kolon',el).forEach(g=>{ const i=+g.dataset.i, k=$$('.kart',el)[2], e=ease(((sn-(+k.dataset.ts))*FPS-4-i*6)/8); g.setAttribute('opacity',e); g.setAttribute('transform',`translate(0 ${(1-e)*40})`); });
   const k4=$$('.kart',el)[3], d=ease(((sn-(+k4.dataset.ts))*FPS-4)/24), yy=150+d*170; const gv=$('.govde',el); if(gv) gv.setAttribute('transform',`translate(0 ${yy})`); const cz=$('.cizgi',el); if(cz) cz.setAttribute('transform',`translate(0 ${yy+42})`); },
 soru(el,t){ const s=1+0.06*Math.sin(t*0.2); $('.soru',el).setAttribute('transform',`translate(170 560) scale(${s}) rotate(${Math.sin(t*0.15)*6}) translate(-170 -560)`);
   const tk=$('.takip',el), e=spring(t-2,0.2); tk.setAttribute('transform',`translate(540 400) scale(${e}) translate(-540 -400)`);
   const elx=$('.el',el), tap=t-34, bas=tap>0&&tap<8, ya=tap>=4; elx.setAttribute('transform',`translate(${(1-ease((t-14)/16))*240} ${(1-ease((t-14)/16))*200 + (bas?-12:0)})`); elx.setAttribute('opacity', ease((t-12)/6));
   $('.btn',el).setAttribute('fill', ya?'#43a047':'#FE2C55'); $('.btnyazi',el).textContent = ya?'✓ Takip edildi':'+ Takip et';
   $('.buton',el).setAttribute('transform', `translate(540 512) scale(${bas?0.94:1}) translate(-540 -512)`);
   const k=$('.kol',el); if(k) k.setAttribute('transform',`rotate(${Math.sin(t*0.35)*14} 50 -404)`);
   $$('.yr',el).forEach(g=>{const i=+g.dataset.i, e=ease((t-6-i*8)/8); g.setAttribute('opacity',e); g.setAttribute('transform',`translate(0 ${(1-e)*24})`);});
   const metin='Traktörüm: ', n=Math.floor(cl((t-36)/3,0,metin.length)); $('.yazi',el).textContent=metin.slice(0,n);
   const im=$('.imlec',el); im.setAttribute('x', 62+n*17.5); im.setAttribute('opacity', Math.floor(t/12)%2?0:1);
   const gp=1+0.1*Math.max(0,Math.sin(t*0.4)); $('.gonder',el).setAttribute('transform',`translate(342 658) scale(${gp}) translate(-342 -658)`); },
};
function etiketler(el,lt){ $$('.etk',el).forEach(g=>{ const e=spring(lt-(+g.dataset.g),0.2), x=+g.dataset.x, y=+g.dataset.y; g.setAttribute('opacity',Math.min(1,e*1.6).toFixed(2)); g.setAttribute('transform',`translate(${x} ${y}) scale(${Math.min(e,1.1)}) translate(${-x} ${-y})`); }); }
window.renderFrame=function(f){
  let acc=0; const P=window.PARCALAR, K=window.KAPAK, kd=document.getElementById('kapak');
  if(K && kd){ const kf=Math.round((K.sure||0.2)*FPS);
    if(f<kf){ kd.style.opacity=1; const svg=kd.querySelector('svg'); SAHNE[K.sahne||'kanca'](svg, K.t||45); etiketler(svg, 999);
      P.forEach((_,i)=>document.getElementById('p'+i).style.opacity=0); return; }
    kd.style.opacity=0; }
  for(let i=0;i<P.length;i++){ const d=Math.round(P[i].sure*FPS), el=document.getElementById('p'+i);
    if(f>=acc && f<acc+d){ el.style.opacity=1; const lt=f-acc, sn=lt/FPS, svg=el.querySelector('svg');
      SAHNE[P[i].sahne](svg, (P[i].devam||0)+lt); etiketler(svg, lt);
      const ws=[...el.querySelectorAll('.alt .w')]; if(ws.length){ let ak=0; ws.forEach((w,k)=>{ if(+w.dataset.ts<=sn) ak=k; });
        const ch=ws[ak].dataset.ch, cs=+ws.find(w=>w.dataset.ch===ch).dataset.ts, basladi=+ws[ak].dataset.ts<=sn;
        ws.forEach((w,k)=>{ w.classList.toggle('goster', w.dataset.ch===ch); w.classList.toggle('on', k===ak && basladi); });
        const al=el.querySelector('.alt'); al.style.transform = basladi ? `scale(${0.8+0.2*ease((sn-cs)/0.12)})` : 'scale(1)'; al.style.opacity = ease(lt/4); }
    } else el.style.opacity=0;
    acc+=d; }
};
"""

CSS = """*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:Poppins,sans-serif;background:#000}
.p{position:absolute;inset:0;opacity:0}.p svg{position:absolute;inset:0}
.bant{position:absolute;left:50%;top:84px;transform:translateX(-50%);display:flex;align-items:center;gap:14px;background:rgba(20,40,26,.92);padding:10px 26px 10px 12px;border-radius:50px;border:3px solid #E2B654;white-space:nowrap;box-shadow:0 6px 18px rgba(0,0,0,.25)}
.bant img{width:58px;height:58px;border-radius:50%;background:#F7F1E3;padding:4px}.bant b{color:#fff;font-size:30px;letter-spacing:1px}.bant span{color:#E2B654;font-size:26px;font-weight:800;margin-left:6px}
.alt{position:absolute;left:30px;right:30px;top:1365px;height:250px;display:flex;flex-wrap:wrap;justify-content:center;align-content:center;font-size:84px;line-height:1.12;font-weight:900;color:#fff;transform-origin:50% 50%}
.kapak{position:absolute;inset:0;opacity:0}.kapak svg{position:absolute;inset:0}
.kapak .kk{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,32,20,.92) 0%,rgba(14,32,20,.78) 30%,rgba(14,32,20,0) 52%)}
.kapak .ust{position:absolute;left:50%;top:290px;transform:translateX(-50%);background:#E2B654;color:#14281A;font-size:46px;font-weight:900;padding:10px 36px;border-radius:40px;letter-spacing:2px;white-space:nowrap;box-shadow:0 8px 20px rgba(0,0,0,.3)}
.kapak h1{position:absolute;left:40px;right:40px;top:390px;text-align:center;font-size:124px;line-height:1.04;font-weight:900;color:#fff;-webkit-text-stroke:10px #0b1a10;paint-order:stroke fill;text-shadow:0 10px 28px rgba(0,0,0,.5)}
.kapak h1 i{font-style:normal;color:#FFD54F}
.kapak .altp{position:absolute;left:50%;top:1478px;transform:translateX(-50%);background:#c62828;color:#fff;font-size:54px;font-weight:900;padding:14px 44px;border-radius:50px;white-space:nowrap;border:5px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.4)}
.alt .w{display:none;margin:6px 8px;padding:2px 18px 8px;border-radius:22px;-webkit-text-stroke:12px #000;paint-order:stroke fill;text-shadow:0 8px 20px rgba(0,0,0,.45)}
.alt .w.goster{display:inline-block}.alt .w.on{background:#FFD54F;color:#14281A;-webkit-text-stroke:0;text-shadow:none;box-shadow:0 6px 0 #c9a227,0 10px 22px rgba(0,0,0,.35)}
"""


def kelime_zamanlari(p):
    """Her kelimenin parça içindeki başlama saniyesi (konuşma aralıklarına harf sayısıyla dağıtılır)."""
    ws = [w for w in p["metin"].split() if _temiz(w)]
    L = [len(_temiz(w)) + 1 for w in ws]; top = sum(L) or 1
    kon = p.get("konusma") or [[0.15, p["sure"] * 0.9]]
    tp = sum(b - a for a, b in kon) or 1

    def zaman(fr):
        h = fr * tp
        for a, b in kon:
            if h <= b - a:
                return a + h
            h -= b - a
        return kon[-1][1]
    out, c = [], 0
    for w, l in zip(ws, L):
        out.append((w, zaman(c / top))); c += l
    return out


def obekler(kz, en_cok=3, harf=15):
    ch, cur = [], []
    for w, t in kz:
        cur.append((w, t))
        if re.search(r"[,.!?:;]$", w) or len(cur) >= en_cok or sum(len(x) for x, _ in cur) >= harf:
            ch.append(cur); cur = []
    if cur:
        ch.append(cur)
    return ch


def html(sen):
    logo = logo_uri()
    bant = sen.get("bant", "USTA BİLGİSİ")
    parts = []
    for i, p in enumerate(sen["parcalar"]):
        kz = kelime_zamanlari(p)
        if p["sahne"] == "dort":
            anahtar = p.get("kartlar", [])
            tsl = []
            for j in range(4):
                t = None
                if j < len(anahtar):
                    t = next((tt for w, tt in kz if _temiz(w).lower().startswith(anahtar[j].lower())), None)
                tsl.append(t if t is not None else 0.3 + j * p["sure"] / 5)
            p["_kart_ts"] = tsl
        kel = "".join(f'<span class="w" data-ch="{k}" data-ts="{t:.3f}">{w}</span>' for k, ob in enumerate(obekler(kz)) for w, t in ob)
        svg = sahne_svg(p["sahne"], p).replace('href="LOGO"', f'href="{logo}"')
        parts.append(f'<div class="p" id="p{i}"><svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg" font-family="Poppins">{svg}'
                     f'<rect width="1080" height="1920" fill="url(#vinyet)"/></svg>'
                     f'<div class="bant"><img src="{logo}"><b>YÜKSEL TARIM</b><span>· {bant}</span></div><div class="alt">{kel}</div></div>')
    kp = sen.get("kapak")
    if kp:
        bas = re.sub(r"\[(.+?)\]", r"<i>\1</i>", kp.get("baslik", ""))
        parts.append(f'<div class="kapak" id="kapak"><svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg" font-family="Poppins">'
                     f'<rect width="1080" height="1920" fill="#cfe6f7"/><g transform="translate(0 {kp.get("kaydir", 210)})">{sahne_svg(kp.get("sahne", "kanca"), {})}</g>'
                     f'<rect width="1080" height="1920" fill="url(#vinyet)"/></svg><div class="kk"></div>'
                     f'<div class="bant"><img src="{logo}"><b>YÜKSEL TARIM</b><span>· {bant}</span></div>'
                     + (f'<div class="ust">{kp["ust"]}</div>' if kp.get("ust") else "") + f'<h1>{bas}</h1>'
                     + (f'<div class="altp">{kp["alt"]}</div>' if kp.get("alt") else "") + '</div>')
    return (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{DEFS}{''.join(parts)}"
            f"<script>window.PARCALAR={json.dumps(sen['parcalar'], ensure_ascii=False)};window.KAPAK={json.dumps(sen.get('kapak'), ensure_ascii=False)};window.KURAL_T={sen.get('kural_t', 99999)};{JS}</script></body></html>")


def devam_ayarla(sen):
    """Aynı sahne arka arkaya geliyorsa animasyon kaldığı yerden devam etsin."""
    onceki, birikim, prev = None, 0, 0
    for p in sen["parcalar"]:
        if p["sahne"] == onceki:
            birikim += round(prev * FPS); p["devam"] = birikim
        else:
            birikim = 0; p["devam"] = 0
        onceki, prev = p["sahne"], p["sure"]
    return sen


def _temiz(m):
    return re.sub(r"[^\wçğıöşüÇĞİÖŞÜ ]", "", m).strip()


def ses_hizala(sen, ses, kuyruk=1.0, esik=None):
    """Seslendirmeyi cümle aralarındaki duraklamalardan böler; her parçanın `sure`'sini ve
    `konusma` (parça içi konuşma aralıkları, sn) alanını yazar. Bölme noktaları, metin uzunluğuna
    göre beklenen zamanlara en yakın duraklamalar arasından (sıra korunarak) seçilir."""
    T = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ses],
                             capture_output=True, text=True).stdout)
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", ses, "-af", "silencedetect=noise=-38dB:d=0.25", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    bas = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    son = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = list(zip(bas, son + [T] * (len(bas) - len(son))))
    P = sen["parcalar"]; n = len(P)
    L = [max(1, len(re.findall("[aeıioöuüAEIİOÖUÜ]", p["metin"]))) for p in P]
    bek = [T * sum(L[:i + 1]) / sum(L) for i in range(n - 1)]
    # duraklama eşiği: önce uzun (eklenmiş) duraklamalar; yetmezse doğal nefes araları
    for e in ([esik] if esik else [0.6, 0.45, 0.3, 0.25]):
        aday = [(a + b) / 2 for a, b in sil if b - a >= e and a > 0.3 and b < T - 0.1]
        if len(aday) >= n - 1:
            break
    if len(aday) < n - 1:
        raise ValueError(f"{n-1} cümle arası gerekiyor, {len(aday)} duraklama bulundu (aralara duraklama ekleyin)")
    INF = float("inf"); m = len(aday)
    dp = [[INF] * (m + 1) for _ in range(n)]; geri = [[0] * (m + 1) for _ in range(n)]
    dp[0] = [0.0] * (m + 1)
    for i in range(1, n):
        for j in range(i, m + 1):
            yeni = dp[i - 1][j - 1] + abs(aday[j - 1] - bek[i - 1])
            if yeni < dp[i][j - 1] if j > i else True:
                dp[i][j], geri[i][j] = yeni, j - 1
            else:
                dp[i][j], geri[i][j] = dp[i][j - 1], geri[i][j - 1]
    secim, j = [], m
    for i in range(n - 1, 0, -1):
        k = geri[i][j]; secim.append(aday[k]); j = k
    sinir = [0.0] + secim[::-1] + [T + kuyruk]
    for i, p in enumerate(P):
        a, b = sinir[i], sinir[i + 1]
        p["sure"] = round(b - a, 3)
        kon, t = [], a
        for s0, s1 in sil:
            if s1 <= a or s0 >= b:
                continue
            if s0 > t:
                kon.append([round(t - a, 3), round(s0 - a, 3)])
            t = max(t, s1)
        if t < min(b, T):
            kon.append([round(t - a, 3), round(min(b, T) - a, 3)])
        p["konusma"] = kon or [[0, p["sure"]]]
    for i in range(n - 1):   # kural listesi ikinci kural parçasıyla açılsın
        if P[i]["sahne"] == "kural" and P[i + 1]["sahne"] == "kural":
            sen["kural_t"] = round(P[i]["sure"] * FPS) + 4
            break
    return sen


def render(sen, out_mp4, ses=None, muzik=None, muzik_bas=0):
    devam_ayarla(sen)
    total = sum(round(p["sure"] * FPS) for p in sen["parcalar"])
    tmp = pathlib.Path(tempfile.mkdtemp())
    (tmp / "v.html").write_text(html(sen))
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto((tmp / "v.html").as_uri()); pg.wait_for_timeout(400)
        for f in range(total):
            pg.evaluate(f"window.renderFrame({f})"); pg.screenshot(path=str(tmp / f"f{f:05d}.png"))
        b.close()
    sessiz = tmp / "s.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"), "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "19", "-pix_fmt", "yuv420p", str(sessiz)], check=True)
    dur = total / FPS
    if ses or muzik:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(sessiz)]
        filt = []
        if ses:
            cmd += ["-i", ses]; filt.append(f"[1:a]aresample=48000,loudnorm=I=-14:TP=-1.5,aresample=48000,apad=whole_dur={dur},atrim=0:{dur},asetpts=PTS-STARTPTS[v]")
        if muzik:
            cmd += ["-ss", str(muzik_bas), "-i", muzik]; mi = 2 if ses else 1
            filt.append(f"[{mi}:a]aresample=48000,atrim=0:{dur},asetpts=PTS-STARTPTS,volume={0.14 if ses else 0.8},afade=t=out:st={dur-1.5:.2f}:d=1.5[m]")
        if ses and muzik:
            filt.append("[v][m]amix=inputs=2:duration=longest:normalize=0[a]")
        else:
            filt[-1] = filt[-1].rsplit("[", 1)[0] + "[a]"
        cmd += ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur}", str(out_mp4)]
        subprocess.run(cmd, check=True)
    else:
        shutil.copy(sessiz, out_mp4)
    shutil.rmtree(tmp)
    return out_mp4, dur


if __name__ == "__main__":
    a = sys.argv[1:]
    sen = json.loads(pathlib.Path(a[0]).read_text())
    ses = a[a.index("--ses") + 1] if "--ses" in a else None
    muz = a[a.index("--muzik") + 1] if "--muzik" in a else None
    mb = float(a[a.index("--muzik-bas") + 1]) if "--muzik-bas" in a else 0
    if ses and "--hizalama-yok" not in a:
        ses_hizala(sen, ses)
        for p in sen["parcalar"]:
            print(f'{p["sure"]:6.2f} sn  {p["konusma"]}  {p["metin"][:50]}')
    print(render(sen, a[1], ses, muz, mb))

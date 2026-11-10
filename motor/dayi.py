"""'Dayı Soruyor' serisi — ek çizimler ve sahne taslağı (storyboard) üretici.
Çizimler: rotavator(), kesit_pulluk(), kesit_taban(), balon(), pip(), isim().
Karakterler usta.py'den: dayı = "kasketli", usta = "genc".
Storyboard: python3 dayi.py <cikti_klasoru>
"""
import pathlib, sys
from playwright.sync_api import sync_playwright
import cizim, usta
from cizim import gok, tarla, traktor, etiket, on_toprak, YER

EK_DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="turuncu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffa040"/><stop offset=".5" stop-color="#ef6c00"/><stop offset="1" stop-color="#b53d00"/></linearGradient>
<pattern id="taban" width="18" height="18" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#4b4540"/><path d="M0 18 L18 0" stroke="#37322e" stroke-width="4"/></pattern>
<radialGradient id="pipzemin" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#cfeaff"/><stop offset="1" stop-color="#8cc4e8"/></radialGradient>
</defs></svg>"""

DAYI, USTA = "kasketli", "genc"


def rotavator(s=1.0, toprak=True):
    """Asılır rotavatör; (0,0) alt askı pimi, sola uzanır, zemin ~y=120."""
    g = f'<g transform="scale({s})">'
    g += ('<path d="M0 0 L-28 -200 L-70 0" fill="none" stroke="#b53d00" stroke-width="18" stroke-linejoin="round"/>'
          '<circle cx="-28" cy="-200" r="11" fill="#333"/><circle cx="0" cy="0" r="12" fill="#333"/>'
          '<path d="M34 -36 L-200 -36" stroke="#555" stroke-width="16" stroke-linecap="round"/><path d="M34 -36 L-200 -36" stroke="#999" stroke-width="5" stroke-dasharray="18 10"/>'
          '<rect x="-270" y="-76" width="96" height="70" rx="12" fill="#37474f"/><rect x="-262" y="-68" width="80" height="12" rx="4" fill="#607d8b"/>')
    blad = "".join(f'<path d="M0 -64 L0 -30 L16 -26" stroke="#90a4ae" stroke-width="9" fill="none" stroke-linecap="round" transform="rotate({k*30})"/>' for k in range(12))
    g += f'<g transform="translate(-230 92)"><circle r="30" fill="#455a64"/>{blad}<circle r="12" fill="#263238"/></g>'
    g += ('<path d="M-30 -8 L-400 -8 Q-436 -8 -436 28 L-436 92 L-404 92 L-404 30 Q-404 22 -396 22 L-56 22 L-56 92 L-30 92 Z" fill="url(#turuncu)" stroke="#8a3000" stroke-width="4"/>'
          '<path d="M-40 2 H-396" stroke="#ffcc80" stroke-width="5" opacity=".7" stroke-linecap="round"/>'
          '<rect x="-210" y="-4" width="110" height="18" rx="4" fill="#fff" opacity=".9"/>'
          '<path d="M-436 30 L-490 126" stroke="#8a3000" stroke-width="14" stroke-linecap="round"/><path d="M-436 30 L-490 126" stroke="url(#turuncu)" stroke-width="8" stroke-linecap="round"/>'
          '<path d="M-400 -8 L-470 60" stroke="#555" stroke-width="5"/><circle cx="-436" cy="30" r="8" fill="#333"/>'
          '<path d="M-90 92 L-60 120 L-150 120 L-130 92 Z" fill="#455a64"/>')
    if toprak:
        g += "".join(f'<circle cx="{-470-k*22-(k%3)*8}" cy="{112-(k%4)*10}" r="{4+(k%3)*2}" fill="#8a6440"/>' for k in range(10))
    return g + '</g>'


def tarla_ince(x1, x2, y, h=96):
    """Rotavatörle inceltilmiş toprak şeridi."""
    return (f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="{h}" fill="#7b5636"/>'
            + "".join(f'<circle cx="{x1+(k*37)%(x2-x1)}" cy="{y+6+(k*23)%(h-10)}" r="{2+k%3}" fill="#a07a52"/>' for k in range(int((x2-x1)/6))))


def kesit_pulluk():
    """Önden toprak kesiti: pulluk dilimi ters çevirir, anız alta gömülür."""
    Y, D = 820, 190
    g = ('<rect width="1080" height="1920" fill="#d9eefc"/>'
         f'<rect x="0" y="{Y+D}" width="1080" height="{1920-Y-D}" fill="#a1795a"/>'
         + "".join(f'<ellipse cx="{(k*97)%1080}" cy="{Y+D+60+(k*53)%420}" rx="{10+k%4*6}" ry="{7+k%3*3}" fill="#8a6a50"/>' for k in range(26)) +
         f'<rect x="620" y="{Y}" width="460" height="{D}" fill="#6f4b2c"/>'
         + "".join(f'<path d="M{x} {Y} l-4 -24 M{x+9} {Y} l4 -20" stroke="#d9b866" stroke-width="5" stroke-linecap="round"/>' for x in range(630, 1080, 22)))

    def dilim(px, aci, ton="#6f4b2c"):
        sap = "".join(f'<path d="M{x} {-D} l-3 -22 M{x+8} {-D} l3 -18" stroke="#d9b866" stroke-width="5" stroke-linecap="round"/>' for x in range(6, 130, 20))
        return (f'<g transform="translate({px} {Y+D}) rotate({aci})"><rect x="0" y="{-D}" width="130" height="{D}" fill="{ton}" stroke="#4a311c" stroke-width="4"/>'
                f'{sap}' + "".join(f'<circle cx="{14+(k*29)%110}" cy="{-D+20+(k*41)%(D-30)}" r="{4+k%3*2}" fill="#5a3d24"/>' for k in range(8)) + '</g>')
    for k, px in enumerate([360, 230, 100, -30]):
        g += dilim(px, -120, "#664428")
    g += dilim(490, -62)
    g += ('<path d="M600 740 Q560 600 430 640" stroke="#c62828" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M452 604 L414 648 L466 664 Z" fill="#c62828"/>'
          f'<path d="M620 {Y} L620 {Y+D}" stroke="#4a311c" stroke-width="4"/>')
    g += (f'<g transform="translate(980 {Y})"><rect x="-22" y="0" width="44" height="{D}" rx="6" fill="#fff8e1" stroke="#8d6e63" stroke-width="3"/>'
          + "".join(f'<path d="M-22 {k*D/4:.0f} h20" stroke="#5d4037" stroke-width="4"/>' for k in range(5)) + '</g>')
    g += etiket(300, 560, 410, 760, "Toprağı ters çevirir", 0, "#c62828")
    g += etiket(260, 1180, 250, 1050, "Anız alta gömülür", 0, "#2e7d32")
    g += etiket(800, 720, 975, 900, "Derin sürüm", 0, "#14281A")
    g += '<text x="540" y="430" text-anchor="middle" font-size="44" font-weight="800" fill="#455a64" letter-spacing="3">TOPRAK KESİTİ</text>'
    return g


def kesit_taban():
    """Hep aynı derinlikte sürüm → sert taban; kökler aşağı inemez, su birikir."""
    Y, T = 760, 960
    g = ('<rect width="1080" height="1920" fill="#d9eefc"/>'
         f'<rect x="0" y="{Y}" width="1080" height="{T-Y}" fill="#7a5634"/>'
         + "".join(f'<circle cx="{(k*61)%1080}" cy="{Y+12+(k*37)%(T-Y-20)}" r="{5+k%4*3}" fill="#5e4027"/>' for k in range(60)) +
         f'<rect x="0" y="{T}" width="1080" height="80" fill="url(#taban)"/><rect x="0" y="{T}" width="1080" height="6" fill="#2b2622"/>'
         f'<rect x="0" y="{T+80}" width="1080" height="{1920-T-80}" fill="#a1795a"/>')
    for x in (180, 420, 660, 900):
        g += (f'<path d="M{x} {Y} L{x} {Y-150}" stroke="#7cb342" stroke-width="10" stroke-linecap="round"/>'
              + "".join(f'<path d="M{x} {Y-40-k*36} q{18 if k%2 else -18} -16 {36 if k%2 else -36} -30" stroke="#8bc34a" stroke-width="8" fill="none" stroke-linecap="round"/>' for k in range(3)) +
              f'<ellipse cx="{x}" cy="{Y-166}" rx="12" ry="28" fill="#e2b654"/>'
              f'<path d="M{x} {Y} Q{x-8} {T-80} {x} {T-6} Q{x+40} {T-12} {x+110} {T-14}" stroke="#f3e5c0" stroke-width="7" fill="none" stroke-linecap="round"/>'
              f'<path d="M{x} {Y+40} Q{x-50} {T-60} {x-110} {T-12}" stroke="#f3e5c0" stroke-width="5" fill="none" stroke-linecap="round"/>')
    g += "".join(f'<ellipse cx="{70+k*120}" cy="{T-10}" rx="34" ry="10" fill="#4fc3f7" opacity=".85"/>' for k in range(9))
    g += f'<path d="M0 {T} H1080" stroke="#FFD54F" stroke-width="6" stroke-dasharray="22 14"/>'
    for k, x in enumerate((230, 520, 810)):
        g += f'<g transform="translate({x} {Y-220}) scale(.32)" opacity=".9">{rotavator(1, False)}</g>'
    g += f'<path d="M60 {Y-300} H840" stroke="#c62828" stroke-width="6" stroke-dasharray="4 14" stroke-linecap="round"/>'
    g += etiket(420, 420, 420, Y - 300, "Her yıl aynı derinlik", 0, "#c62828")
    g += etiket(330, 1180, 300, T + 40, "SERT TABAN", 0, "#14281A")
    g += etiket(780, 1180, 800, T - 10, "Su birikir, kök inemez", 0, "#1565c0")
    return g


def balon(x, y, w, h, satirlar, kx, ky, fs=54, renk="#14281A"):
    """Konuşma balonu; (kx,ky) kuyruk ucu. Satırda [kelime] altın vurgulu."""
    import re
    g = (f'<g filter="url(#golge)"><path d="M{x+40} {y} H{x+w-40} Q{x+w} {y} {x+w} {y+40} V{y+h-40} Q{x+w} {y+h} {x+w-40} {y+h} '
         f'H{min(max(kx+50, x+80), x+w-60)} L{kx} {ky} L{min(max(kx-10, x+40), x+w-120)} {y+h} H{x+40} Q{x} {y+h} {x} {y+h-40} V{y+40} Q{x} {y} {x+40} {y} Z" '
         f'fill="#fff" stroke="{renk}" stroke-width="7" stroke-linejoin="round"/></g>')
    top = y + h / 2 - (len(satirlar) - 1) * fs * 0.6 + fs * 0.36
    for i, s in enumerate(satirlar):
        s = re.sub(r"\[(.+?)\]", r'<tspan fill="#c62828">\1</tspan>', s)
        g += f'<text x="{x+w/2}" y="{top+i*fs*1.2:.0f}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="{renk}">{s}</text>'
    return g


_PIP = [0]


def pip(cx, cy, r, model, poz="isaret", ifade="mutlu", ad=None):
    _PIP[0] += 1
    cid = f"pip{_PIP[0]}"
    s = r / 190
    return (f'<defs><clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r+12}" fill="#E2B654" filter="url(#golge)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#pipzemin)"/>'
            f'<g clip-path="url(#{cid})"><g transform="translate({cx} {cy + 860*s + 60*s}) scale({s})">{usta.usta(model, poz, ifade)}</g></g>'
            + (isim(cx, cy + r + 34, ad) if ad else ""))


def isim(x, y, ad, renk="#2F5737"):
    w = len(ad) * 22 + 48
    return (f'<rect x="{x-w/2}" y="{y-30}" width="{w}" height="60" rx="30" fill="{renk}" stroke="#E2B654" stroke-width="4"/>'
            f'<text x="{x}" y="{y+12}" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">{ad}</text>')


def kisi(x, y, s, model, poz, ifade):
    return f'<g transform="translate({x} {y}) scale({s})">{usta.usta(model, poz, ifade)}</g>'


# ---------------------------------------------------------------- storyboard
DAYI_AD, USTA_AD = "Hasan Dayı", "Usta Mert"


def kareler():
    K = []
    # 1 kapak
    g = gok() + tarla()
    g += kisi(300, 1440, .74, DAYI, "bel", "normal") + kisi(790, 1440, .74, USTA, "isaret", "mutlu")
    K.append(("Kapak (ilk 0,2 sn)", g, {"ust": "DAYI SORUYOR", "baslik": "Pulluk mu, [rotavatör mü?]", "alt": "Usta cevaplıyor 👇"}, None))
    # 2 dayı soruyor
    g = gok() + tarla()
    g += kisi(860, 1290, .6, USTA, "duz", "normal")
    g += kisi(330, 2050, 1.42, DAYI, "bel", "endise")
    g += balon(70, 250, 940, 300, ["40 yıldır [pulluk] sürerim,", "rotavatör neyime yarar?"], 300, 640, 58)
    K.append(("Dayı soruyor (0-5 sn)", g, None, ("rotavatör", "neyime yarar?")))
    # 3 pulluk kesiti
    g = kesit_pulluk() + '<g><rect x="300" y="210" width="480" height="100" rx="50" fill="#c62828" filter="url(#golge)"/><text x="540" y="278" text-anchor="middle" font-size="58" font-weight="900" fill="#fff">PULLUK</text></g>'
    g += pip(925, 460, 110, USTA, "isaret", "mutlu", USTA_AD)
    K.append(("Usta: pulluk ne yapar? (5-14 sn)", g, None, ("toprağı derin", "çevirir,")))
    # 4 rotavatör
    g = gok() + tarla()
    g += tarla_ince(0, 400, 1158, 104)
    g += f'<g transform="translate(690 {YER}) scale(.72)">{traktor("mutlu")}<g transform="translate(-235 -120)">{rotavator(1.0)}</g></g>' + on_toprak(60, 470, YER + 6, 40)
    g += '<g><rect x="250" y="210" width="580" height="100" rx="50" fill="#ef6c00" filter="url(#golge)"/><text x="540" y="278" text-anchor="middle" font-size="58" font-weight="900" fill="#fff">ROTAVATÖR</text></g>'
    g += etiket(300, 560, 150, 1185, "Toprağı inceltir", 0, "#ef6c00") + etiket(400, 690, 330, 1190, "Ekim yatağı hazırlar", 0, "#2e7d32")
    g += pip(925, 460, 110, USTA, "isaret", "mutlu", USTA_AD)
    K.append(("Usta: rotavatör ne yapar? (14-22 sn)", g, None, ("ekim yatağını", "hazırlar.")))
    # 5 sert taban
    g = kesit_taban() + '<g><rect x="330" y="210" width="420" height="100" rx="50" fill="#14281A" filter="url(#golge)"/><text x="540" y="278" text-anchor="middle" font-size="58" font-weight="900" fill="#FFD54F">⚠ DİKKAT</text></g>'
    g += pip(925, 460, 110, USTA, "isaret", "normal", USTA_AD)
    K.append(("Usta: hep aynı derinlik → sert taban (22-31 sn)", g, None, ("sert bir", "taban yapar.")))
    # 6 dayı tepki
    g = gok() + tarla()
    g += kisi(300, 1700, 1.1, DAYI, "basparmak", "mutlu") + kisi(820, 1420, .8, USTA, "basparmak", "mutlu")
    g += balon(60, 230, 960, 280, ["Yani [ikisi de] lazımmış,", "hah! 😄"], 280, 600, 62)
    K.append(("Dayının tepkisi (31-37 sn)", g, None, ("ikisi de", "lazımmış,")))
    # 7 kapanış
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70)])
    g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
    g += kisi(560, 1640, 1.05, USTA, "salla", "mutlu")
    g += balon(60, 210, 960, 290, ["Sorunu [yorumlara] yaz,", "sıradaki videoda cevaplayalım!"], 600, 600, 54)
    g += ('<g transform="translate(70 1180)"><rect width="330" height="96" rx="48" fill="#FE2C55" filter="url(#golge)"/>'
          '<text x="165" y="64" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">+ Takip et</text><text x="250" y="170" font-size="110">👆</text></g>')
    K.append(("Kapanış: soru + takip (37-45 sn)", g, None, ("yorumlara", "yaz,")))
    return K


def storyboard(klasor):
    klasor = pathlib.Path(klasor); klasor.mkdir(parents=True, exist_ok=True)
    logo = cizim.logo_uri()
    css = cizim.CSS + ".alt .w{display:inline-block}"
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        dosyalar = []
        for i, (ad, svg, kapak, alt) in enumerate(kareler()):
            svg = svg.replace('href="LOGO"', f'href="{logo}"')
            ust = ""
            if kapak:
                import re
                bas = re.sub(r"\[(.+?)\]", r"<i>\1</i>", kapak["baslik"])
                ust = (f'<div class="kk"></div><div class="ust">{kapak["ust"]}</div><h1>{bas}</h1><div class="altp">{kapak["alt"]}</div>')
            altyazi = ""
            if alt:
                altyazi = f'<div class="alt"><span class="w">{alt[0].split()[0]}</span>' + "".join(f'<span class="w{" on" if k==0 else ""}">{w}</span>' for k, w in enumerate(" ".join([*alt[0].split()[1:], alt[1]]).split())) + '</div>'
                altyazi = altyazi.replace('<span class="w">', '<span class="w goster">', 1).replace('class="w on"', 'class="w goster on"').replace('class="w"', 'class="w goster"')
            html = (f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{cizim.DEFS}{usta.USTA_DEFS}{EK_DEFS}"
                    f'<div class="{"kapak" if kapak else "p"}" style="opacity:1"><svg viewBox="0 0 1080 1920" width="1080" height="1920" font-family="Poppins">{svg}<rect width="1080" height="1920" fill="url(#vinyet)"/></svg>'
                    f'{ust}<div class="bant"><img src="{logo}"><b>YÜKSEL TARIM</b><span>· DAYI SORUYOR</span></div>{altyazi}</div>'
                    "<script>document.querySelectorAll('.etk').forEach(e=>e.setAttribute('opacity',1))</script></body></html>")
            pg.set_content(html); pg.wait_for_timeout(250)
            f = klasor / f"kare{i+1}.png"; pg.screenshot(path=str(f)); dosyalar.append((ad, f))
        b.close()
    return dosyalar


if __name__ == "__main__":
    for ad, f in storyboard(sys.argv[1]):
        print(f, ad)

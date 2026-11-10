"""Yüksel Tarım çizim videoları — detaylı 'usta' karakteri (önden, hafif 3/4).
usta(model, poz, ifade) → SVG grubu. Yerel koordinat: (0,0) ayak altı ortası, boy ~1000.
model: "yelekli" | "tulumlu" | "kasketli" | "genc"
poz:   "duz" | "bel" | "salla" | "basparmak" | "isaret"
ifade: "mutlu" | "normal" | "endise"
Gereken ortak tanımlar cizim.DEFS'te (ten, kareli, kot, golge) + USTA_DEFS.
"""

CIZGI = "#3b2a1f"

USTA_DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="u_ten" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9965f"/><stop offset=".35" stop-color="#f2bf8e"/><stop offset=".7" stop-color="#f7cfa3"/><stop offset="1" stop-color="#e2a874"/></linearGradient>
<linearGradient id="u_kot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a4766"/><stop offset=".5" stop-color="#3f6690"/><stop offset="1" stop-color="#2c4a6b"/></linearGradient>
<linearGradient id="u_yesil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1f3d27"/><stop offset=".5" stop-color="#2F5737"/><stop offset="1" stop-color="#22432b"/></linearGradient>
<linearGradient id="u_polo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2b5e36"/><stop offset=".5" stop-color="#3f8a4d"/><stop offset="1" stop-color="#2d6238"/></linearGradient>
<linearGradient id="u_bordo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a1f2a"/><stop offset=".5" stop-color="#83303f"/><stop offset="1" stop-color="#5e2230"/></linearGradient>
<linearGradient id="u_haki" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a7a55"/><stop offset=".5" stop-color="#b3a173"/><stop offset="1" stop-color="#8f7f58"/></linearGradient>
<linearGradient id="u_gri" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f4a45"/><stop offset=".5" stop-color="#6e675f"/><stop offset="1" stop-color="#524c46"/></linearGradient>
<linearGradient id="u_bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a4b2a"/><stop offset="1" stop-color="#4a2c18"/></linearGradient>
<linearGradient id="u_beyaz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9dde0"/><stop offset=".5" stop-color="#fbfbfb"/><stop offset="1" stop-color="#dfe3e6"/></linearGradient>
<pattern id="u_tvid" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#7d776e"/><path d="M0 7 L7 0 M7 14 L14 7" stroke="#6a645c" stroke-width="3"/><path d="M0 0 L14 14" stroke="#8c867d" stroke-width="1.5"/></pattern>
<pattern id="u_orgu" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="url(#u_bordo)"/><path d="M0 0 L8 8 L16 0 M0 8 L8 16 L16 8" stroke="#6b2533" stroke-width="2.5" fill="none"/></pattern>
<linearGradient id="u_zeytin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f4a2c"/><stop offset=".5" stop-color="#77703f"/><stop offset="1" stop-color="#55502f"/></linearGradient>
<pattern id="u_mkareli" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#4f7fae"/><rect width="15" height="30" fill="#2f5d8a" opacity=".55"/><rect width="30" height="15" fill="#2f5d8a" opacity=".45"/><path d="M0 7.5H30M7.5 0V30" stroke="#e8f1fa" stroke-width="1.8" opacity=".55"/></pattern>
<pattern id="u_kareli" width="34" height="34" patternUnits="userSpaceOnUse"><rect width="34" height="34" fill="#c0392b"/><rect width="17" height="34" fill="#8e2a20" opacity=".55"/><rect width="34" height="17" fill="#8e2a20" opacity=".45"/><path d="M0 8.5H34M8.5 0V34" stroke="#f3d6a8" stroke-width="2" opacity=".5"/><path d="M0 25.5H34M25.5 0V34" stroke="#2b1a14" stroke-width="1.5" opacity=".35"/></pattern>
</defs></svg>"""

MODELLER = {
    "yelekli":  dict(gomlek="url(#u_kareli)", ust="yelek", yelek="url(#u_yesil)", pantolon="url(#u_kot)", bot="url(#u_bot)",
                     sapka="kep", sapka_renk="#2F5737", sac="#4a3426", biyik="#3e2a1d", biyik_ac="#6b4a35", yas=1, kol="uzun"),
    "tulumlu":  dict(gomlek="url(#u_mkareli)", ust="tulum", tulum="url(#u_zeytin)", pantolon="url(#u_zeytin)", bot="url(#u_bot)",
                     sapka="kep", sapka_renk="#2F5737", sac="#2b2420", biyik="#231c18", biyik_ac="#4a3a30", yas=0, kol="kisa"),
    "kasketli": dict(gomlek="url(#u_beyaz)", ust="orgu", pantolon="url(#u_gri)", bot="url(#u_bot)",
                     sapka="kasket", sapka_renk="url(#u_tvid)", sac="#cfcfcf", biyik="#ececec", biyik_ac="#ffffff", yas=2, kol="uzun"),
    "genc":     dict(gomlek="url(#u_polo)", ust="polo", pantolon="url(#u_haki)", bot="#5d4037",
                     sapka="kep", sapka_renk="#2F5737", sac="#2b2420", biyik=None, sakal=True, yas=0, kol="kisa"),
}

KOLLAR = {  # (omuz, dirsek, bilek) — sağ kol için; sol kol x aynalanır
    "duz": ((118, -684), (150, -560), (146, -436)),
    "bel": ((118, -684), (206, -580), (124, -494)),
    "salla": ((118, -684), (226, -730), (250, -872)),
    "basparmak": ((118, -684), (176, -566), (232, -650)),
    "isaret": ((118, -684), (214, -668), (318, -716)),
}


def _kol(o, d, b, kumas, ten, kisa):
    p = f"M{o[0]} {o[1]} Q{d[0]} {d[1]} {b[0]} {b[1]}"
    g = f'<path d="{p}" stroke="{CIZGI}" stroke-width="72" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    if kisa:  # kısa kol: üst kol kumaş, ön kol ten
        mx, my = (o[0] + d[0]) / 2, (o[1] + d[1]) / 2
        g += f'<path d="{p}" stroke="url(#u_ten)" stroke-width="58" fill="none" stroke-linecap="round"/>'
        g += f'<path d="M{o[0]} {o[1]} L{mx} {my}" stroke="{CIZGI}" stroke-width="80" stroke-linecap="round"/>'
        g += f'<path d="M{o[0]} {o[1]} L{mx} {my}" stroke="{kumas}" stroke-width="70" stroke-linecap="round"/>'
    else:
        g += f'<path d="{p}" stroke="{kumas}" stroke-width="62" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        g += f'<circle cx="{b[0]}" cy="{b[1]}" r="31" fill="{kumas}" stroke="{CIZGI}" stroke-width="4"/>'
        g += f'<path d="M{(o[0]+d[0])/2-8} {(o[1]+d[1])/2+6} q10 12 22 4" stroke="#000" stroke-opacity=".25" stroke-width="5" fill="none"/>'
    if o[0] > 0:
        g += f'<path d="{p}" stroke="#000" stroke-opacity=".14" stroke-width="{58 if not kisa else 52}" fill="none" stroke-linecap="round" stroke-dasharray="0 0"/>'
    g += f'<path d="M{o[0]-(14 if o[0]<0 else -4)} {o[1]+16} Q{d[0]-(16 if o[0]<0 else -2)} {d[1]} {b[0]-(12 if o[0]<0 else 0)} {b[1]-20}" stroke="#fff" stroke-opacity=".14" stroke-width="10" fill="none" stroke-linecap="round"/>'
    return g


def _el(b, tur, yon=1):
    x, y = b
    s = f'stroke="{CIZGI}" stroke-width="4"'
    if tur == "acik":
        return (f'<g transform="translate({x} {y-18})">' + "".join(
            f'<rect x="{-30+k*15}" y="-72" width="15" height="52" rx="7.5" fill="url(#u_ten)" {s} transform="rotate({-12+k*8} {-22+k*15} -20)"/>' for k in range(4)) +
                f'<ellipse cx="0" cy="0" rx="34" ry="32" fill="url(#u_ten)" {s}/><rect x="{24*yon}" y="-14" width="14" height="40" rx="7" fill="url(#u_ten)" {s} transform="rotate({-40*yon} {24*yon} 0)"/></g>')
    if tur == "basparmak":
        return (f'<g transform="translate({x} {y})"><rect x="-30" y="-28" width="58" height="54" rx="20" fill="url(#u_ten)" {s}/>'
                + "".join(f'<path d="M-30 {-14+k*13} h22" stroke="{CIZGI}" stroke-width="3"/>' for k in range(3)) +
                f'<rect x="-2" y="-84" width="24" height="64" rx="12" fill="url(#u_ten)" {s}/><path d="M2 -78 h14" stroke="#fff" stroke-opacity=".5" stroke-width="4"/></g>')
    if tur == "isaret":
        return (f'<g transform="translate({x} {y}) rotate(-22)"><rect x="-30" y="-26" width="54" height="50" rx="18" fill="url(#u_ten)" {s}/>'
                f'<rect x="14" y="-22" width="62" height="18" rx="9" fill="url(#u_ten)" {s}/><rect x="-10" y="-40" width="20" height="30" rx="10" fill="url(#u_ten)" {s} transform="rotate(30 0 -25)"/></g>')
    return f'<ellipse cx="{x}" cy="{y+14}" rx="30" ry="36" fill="url(#u_ten)" {s}/><path d="M{x-12} {y+30} q12 8 24 0" stroke="{CIZGI}" stroke-width="3" fill="none"/>'


def _bas(m, ifade):
    s = f'stroke="{CIZGI}" stroke-width="4"'
    g = ''
    # kulaklar, saç yanları
    for sx in (-1, 1):
        g += (f'<ellipse cx="{sx*88}" cy="6" rx="20" ry="30" fill="#e8a979" {s}/><path d="M{sx*88} -8 q{sx*8} 12 0 26" stroke="#b97a4e" stroke-width="5" fill="none"/>')
    g += f'<path d="M-88 -10 Q-100 -70 -60 -96 L60 -96 Q100 -70 88 -10 L84 30 Q60 -40 0 -44 Q-60 -40 -84 30 Z" fill="{m["sac"]}" {s}/>'
    # yüz
    g += f'<path d="M-84 -30 Q-88 70 -40 104 Q0 124 40 104 Q88 70 84 -30 Q80 -78 0 -80 Q-80 -78 -84 -30 Z" fill="url(#u_ten)" {s}/>'
    g += '<path d="M-84 -20 Q-84 60 -42 98 Q-70 50 -66 -20 Z" fill="#c98552" opacity=".35"/>'
    g += '<circle cx="-50" cy="38" r="20" fill="#ef8a7a" opacity=".35"/><circle cx="50" cy="38" r="20" fill="#ef8a7a" opacity=".35"/>'
    if m.get("sakal"):
        g += '<path d="M-82 10 Q-84 72 -40 104 Q0 124 40 104 Q84 72 82 10 Q70 70 40 82 Q0 96 -40 82 Q-70 70 -82 10 Z" fill="#3b2f28" opacity=".38"/><path d="M-30 96 Q0 110 30 96" stroke="#3b2f28" stroke-opacity=".3" stroke-width="10" fill="none"/>'
        pass
    # kaşlar
    kalin = 14 if m["yas"] < 2 else 12
    kas_renk = m["biyik"] or m["sac"]
    egim = {"endise": 10, "mutlu": -4}.get(ifade, 0)
    for sx in (-1, 1):
        g += f'<path d="M{sx*14} -30 Q{sx*36} {-44+(egim if sx<0 else egim)} {sx*60} -30" stroke="{kas_renk if m["yas"]<2 else "#bdbdbd"}" stroke-width="{kalin}" fill="none" stroke-linecap="round" transform="rotate({sx*egim*-1} {sx*36} -36)"/>'
    # gözler
    for sx in (-1, 1):
        ex = sx * 34
        if ifade == "mutlu":
            g += f'<path d="M{ex-16} -2 Q{ex} -18 {ex+16} -2" stroke="{CIZGI}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            g += f'<path d="M{ex-14} 8 Q{ex} 14 {ex+14} 8" stroke="#c98552" stroke-width="3" fill="none"/>'
        else:
            g += (f'<ellipse cx="{ex}" cy="-4" rx="17" ry="14" fill="#fff" {s}/><circle cx="{ex+3}" cy="-3" r="10" fill="#6d4c41"/><circle cx="{ex+3}" cy="-3" r="5.5" fill="#1b1410"/>'
                  f'<circle cx="{ex+7}" cy="-7" r="3.2" fill="#fff"/><path d="M{ex-18} -10 Q{ex} -24 {ex+18} -10" stroke="{CIZGI}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        if m["yas"] >= 1:
            g += f'<path d="M{sx*58} -6 l{sx*12} -6 M{sx*58} 2 l{sx*13} 2" stroke="#b97a4e" stroke-width="3" stroke-linecap="round"/>'
    if m["yas"] >= 2:
        g += '<path d="M-36 -58 Q0 -66 36 -58 M-28 -50 Q0 -56 28 -50" stroke="#c98552" stroke-width="3" fill="none"/>'
    # burun
    g += ('<path d="M-4 -6 Q-10 22 -16 34 Q0 48 16 34 Q10 22 4 -6" fill="#e9a878"/>'
          '<ellipse cx="0" cy="34" rx="20" ry="15" fill="#eaa676" stroke="#b97a4e" stroke-width="3"/><ellipse cx="-4" cy="29" rx="7" ry="4" fill="#fff" opacity=".45"/>'
          '<path d="M-12 40 q4 4 8 0 M4 40 q4 4 8 0" stroke="#8a5233" stroke-width="3" fill="none"/>')
    # ağız + bıyık
    if ifade == "mutlu":
        g += '<path d="M-34 66 Q0 104 34 66 Q0 80 -34 66 Z" fill="#7a2e22" stroke="#3b2a1f" stroke-width="3"/><path d="M-26 68 Q0 78 26 68 L24 74 Q0 82 -24 74 Z" fill="#fff"/>'
    elif ifade == "endise":
        g += '<path d="M-22 80 Q-11 70 0 80 Q11 90 22 80" stroke="#5b2a1e" stroke-width="5" fill="none" stroke-linecap="round"/>'
    else:
        g += '<path d="M-22 76 Q0 88 22 76" stroke="#5b2a1e" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if m["biyik"]:
        g += (f'<path d="M0 46 Q-24 40 -50 52 Q-66 60 -70 74 Q-50 68 -34 70 Q-14 70 0 60 Q14 70 34 70 Q50 68 70 74 Q66 60 50 52 Q24 40 0 46 Z" fill="{m["biyik"]}" {s}/>'
              + "".join(f'<path d="M{sx*k} {50+k*0.15} q{sx*6} 8 {sx*12} 12" stroke="{m["biyik_ac"]}" stroke-width="2.5" fill="none" opacity=".8"/>' for sx in (-1, 1) for k in (10, 24, 38, 52)))
    # şapka
    g += '<g transform="translate(0 -18)">'
    if m["sapka"] == "kep":
        g += (f'<path d="M-92 -40 Q-96 -138 0 -142 Q96 -138 92 -40 Z" fill="{m["sapka_renk"]}" {s}/>'
              '<path d="M-30 -138 Q-40 -90 -46 -42 M30 -138 Q40 -90 46 -42" stroke="#000" stroke-opacity=".2" stroke-width="4" fill="none"/>'
              '<path d="M-70 -110 Q-40 -132 -6 -134" stroke="#fff" stroke-opacity=".3" stroke-width="8" fill="none" stroke-linecap="round"/>'
              f'<circle cx="0" cy="-141" r="9" fill="{m["sapka_renk"]}" {s}/>'
              '<circle cx="0" cy="-90" r="27" fill="#F7F1E3" stroke="#E2B654" stroke-width="4"/><image href="LOGO" x="-23" y="-113" width="46" height="46"/>'
              f'<path d="M-100 -44 Q0 -66 100 -44 Q116 -20 0 -10 Q-116 -20 -100 -44 Z" fill="{m["sapka_renk"]}" {s}/>'
              '<path d="M-96 -40 Q0 -58 96 -40 Q100 -30 0 -22 Q-100 -30 -96 -40 Z" fill="#000" opacity=".22"/>'
              '<path d="M-80 -12 Q0 4 80 -12 L80 -2 Q0 12 -80 -2 Z" fill="#000" opacity=".12"/>')
    else:
        g += (f'<path d="M-100 -36 Q-112 -112 0 -122 Q112 -112 100 -36 Z" fill="{m["sapka_renk"]}" {s}/>'
              '<path d="M-60 -112 Q0 -126 60 -112" stroke="#fff" stroke-opacity=".25" stroke-width="7" fill="none"/>'
              '<path d="M-104 -40 Q0 -24 104 -40 Q100 -18 0 -10 Q-100 -18 -104 -40 Z" fill="#5f5a53" stroke="#3b2a1f" stroke-width="4"/>'
              '<path d="M-80 -10 Q0 2 80 -10 L80 0 Q0 10 -80 0 Z" fill="#000" opacity=".12"/>')
    return g + '</g>'


def usta(model="yelekli", poz="duz", ifade="mutlu", stil="ince"):
    """stil: "modern" (dış çizgisiz, yumuşak gölge) | "ince" (ince renkli çizgi) | "cizgili" (kalın çizgi)."""
    svg = _usta(model, poz, ifade)
    if stil == "modern":
        svg = (svg.replace(f'stroke="{CIZGI}" stroke-width="4"', 'stroke="none"')
                  .replace(f'stroke="{CIZGI}" stroke-width="3"', 'stroke="none"')
                  .replace(f'stroke="{CIZGI}" stroke-width="72"', 'stroke="none" stroke-width="0"')
                  .replace(f'stroke="{CIZGI}" stroke-width="80"', 'stroke="none" stroke-width="0"')
                  .replace(f'stroke="{CIZGI}" stroke-width="30"', 'stroke="none" stroke-width="0"'))
    elif stil == "ince":
        svg = (svg.replace(f'stroke="{CIZGI}" stroke-width="4"', 'stroke="#5a3f2e" stroke-opacity=".55" stroke-width="2.5"')
                  .replace(f'stroke="{CIZGI}" stroke-width="72"', 'stroke="#5a3f2e" stroke-opacity=".5" stroke-width="66"')
                  .replace(f'stroke="{CIZGI}" stroke-width="80"', 'stroke="#5a3f2e" stroke-opacity=".5" stroke-width="74"'))
    return svg


def _usta(model="yelekli", poz="duz", ifade="mutlu"):
    m = MODELLER[model]
    s = f'stroke="{CIZGI}" stroke-width="4"'
    g = ('<ellipse cx="70" cy="8" rx="240" ry="26" fill="#2a1a0c" opacity=".26" filter="url(#a_yumusak)"/>'
         '<ellipse cx="0" cy="4" rx="150" ry="16" fill="#1a0f06" opacity=".3"/>')
    # bacaklar + botlar
    # bacaklar: hafif açık duruş, dizden incelen paçalar, sağ tarafta gölge (ışık soldan)
    g += f'<path d="M-116 -490 L116 -490 L112 -400 L-112 -400 Z" fill="{m["pantolon"]}" {s}/>'
    for sx in (-1, 1):
        g += (f'<path d="M{sx*4} -470 L{sx*116} -488 Q{sx*124} -380 {sx*112} -270 Q{sx*106} -170 {sx*110} -82 L{sx*24} -82 Q{sx*22} -170 {sx*20} -272 Q{sx*12} -380 {sx*4} -470 Z" fill="{m["pantolon"]}" {s}/>'
              f'<path d="M{sx*(116 if sx>0 else 30)} -480 Q{sx*(124 if sx>0 else 36)} -380 {sx*(112 if sx>0 else 30)} -270 Q{sx*(106 if sx>0 else 26)} -170 {sx*(110 if sx>0 else 30)} -84 L{sx*(84 if sx>0 else 24)} -84 Q{sx*(80 if sx>0 else 22)} -170 {sx*(86 if sx>0 else 22)} -272 Q{sx*(96 if sx>0 else 14)} -380 {sx*(90 if sx>0 else 8)} -478 Z" fill="#000" opacity="{.2 if sx>0 else .12}"/>'
              f'<path d="M{sx*44} -292 q{sx*18} 12 {sx*40} 2 M{sx*50} -262 q{sx*14} 8 {sx*30} 0" stroke="#000" stroke-opacity=".22" stroke-width="5" fill="none" stroke-linecap="round"/>'
              f'<path d="M{sx*30} -420 Q{sx*40} -360 {sx*36} -300" stroke="#000" stroke-opacity=".12" stroke-width="5" fill="none"/>'
              f'<path d="M{sx*26} -100 L{sx*108} -100" stroke="#000" stroke-opacity=".25" stroke-width="5"/>')
    g += '<path d="M-100 -470 Q-108 -380 -98 -280" stroke="#fff" stroke-opacity=".14" stroke-width="10" fill="none" stroke-linecap="round"/>'
    for sx in (-1, 1):
        g += (f'<path d="M{sx*14} -80 L{sx*108} -80 Q{sx*112} -40 {sx*140} -24 Q{sx*150} -4 {sx*126} 0 L{sx*16} 0 Q{sx*8} -30 {sx*14} -80 Z" fill="{m["bot"]}" {s}/>'
              f'<path d="M{sx*14} -8 L{sx*140} -8 L{sx*136} 0 L{sx*16} 0 Z" fill="#1d130c"/>'
              f'<path d="M{sx*40} -66 l{sx*30} 10 M{sx*42} -50 l{sx*30} 10" stroke="#d7b98c" stroke-width="4"/>'
              f'<path d="M{sx*96} -70 Q{sx*104} -40 {sx*124} -30" stroke="#fff" stroke-opacity=".2" stroke-width="6" fill="none"/>')
    # gövde (gömlek)
    gov = "M-122 -690 Q-138 -600 -114 -470 L114 -470 Q138 -600 122 -690 Q60 -716 0 -712 Q-60 -716 -122 -690 Z"
    g += f'<path d="{gov}" fill="{m["gomlek"]}" {s}/>'
    g += '<path d="M114 -680 Q132 -600 108 -476 L70 -476 Q94 -590 84 -688 Z" fill="#000" opacity=".2"/>'
    g += '<path d="M-110 -670 Q-126 -600 -106 -490" stroke="#fff" stroke-opacity=".16" stroke-width="12" fill="none" stroke-linecap="round"/>'
    g += '<path d="M-60 -500 q16 -14 30 -2 M30 -506 q16 -12 30 0 M-20 -640 q10 20 4 44" stroke="#000" stroke-opacity=".16" stroke-width="5" fill="none" stroke-linecap="round"/>'
    ust = m["ust"]
    if ust == "yelek":
        for sx in (-1, 1):
            g += (f'<path d="M{sx*122} -690 Q{sx*138} -600 {sx*114} -470 L{sx*26} -470 L{sx*34} -560 L{sx*44} -690 Q{sx*80} -704 {sx*122} -690 Z" fill="{m["yelek"]}" {s}/>'
                  f'<rect x="{sx*52 - (40 if sx>0 else 0)}" y="-560" width="40" height="44" rx="6" fill="#244530" stroke="{CIZGI}" stroke-width="3"/>'
                  f'<path d="M{sx*52 - (40 if sx>0 else 0)} -548 h40" stroke="#16301f" stroke-width="5"/>'
                  f'<path d="M{sx*96} -620 l{sx*0} 24 M{sx*90} -600 h{sx*-30}" stroke="#E2B654" stroke-width="3" opacity=".6"/>')
        g += '<circle cx="-30" cy="-610" r="6" fill="#E2B654"/><circle cx="-29" cy="-560" r="6" fill="#E2B654"/><circle cx="-28" cy="-510" r="6" fill="#E2B654"/>'
    elif ust == "tulum":
        g += (f'<path d="M-76 -640 L76 -640 L84 -470 L-84 -470 Z" fill="{m["tulum"]}" {s}/><rect x="-40" y="-614" width="80" height="62" rx="8" fill="#5f5933" stroke="{CIZGI}" stroke-width="3"/>'
              '<path d="M-40 -600 h80" stroke="#E2B654" stroke-width="3" stroke-dasharray="6 5"/>'
              f'<path d="M-70 -640 L-104 -700 M70 -640 L104 -700" stroke="{CIZGI}" stroke-width="30" stroke-linecap="round"/><path d="M-70 -640 L-104 -700 M70 -640 L104 -700" stroke="#77703f" stroke-width="22" stroke-linecap="round"/>'
              '<circle cx="-68" cy="-632" r="10" fill="#E2B654" stroke="#a87b1f" stroke-width="3"/><circle cx="68" cy="-632" r="10" fill="#E2B654" stroke="#a87b1f" stroke-width="3"/>')
    elif ust == "orgu":
        g += (f'<path d="M-118 -684 Q-132 -600 -112 -470 L112 -470 Q132 -600 118 -684 Q80 -700 46 -700 L0 -590 L-46 -700 Q-80 -700 -118 -684 Z" fill="url(#u_orgu)" {s}/>'
              '<path d="M-46 -700 L0 -590 L46 -700" stroke="#4d1a24" stroke-width="10" fill="none"/>'
              + "".join(f'<path d="M{x} -490 v20" stroke="#4d1a24" stroke-width="4"/>' for x in range(-104, 110, 14)))
    elif ust == "polo":
        g += ('<path d="M-12 -700 L-12 -620 L12 -620 L12 -700" fill="#2b5e36" stroke="#1d3f25" stroke-width="3"/><circle cx="0" cy="-680" r="4" fill="#E2B654"/><circle cx="0" cy="-650" r="4" fill="#E2B654"/>'
              '<circle cx="62" cy="-620" r="24" fill="#F7F1E3" stroke="#E2B654" stroke-width="3"/><image href="LOGO" x="42" y="-640" width="40" height="40"/>')
    # kemer (tulum hariç)
    if ust != "tulum":
        g += f'<rect x="-114" y="-492" width="228" height="26" rx="6" fill="#4e342e" {s}/><rect x="-18" y="-496" width="36" height="34" rx="6" fill="none" stroke="#E2B654" stroke-width="6"/>'
    # boyun + yaka
    g += f'<path d="M-36 -770 L36 -770 L40 -700 L-40 -700 Z" fill="#e3a676" {s}/><path d="M-36 -730 Q0 -712 36 -730 L38 -706 L-38 -706 Z" fill="#c98552" opacity=".5"/>'
    yaka = {"yelek": "#a93226", "tulum": "#2f5d8a", "orgu": "#f4f4f4", "polo": "#2b5e36"}[ust]
    g += (f'<path d="M-44 -712 L-6 -676 L-30 -650 L-62 -700 Z" fill="{yaka}" {s}/><path d="M44 -712 L6 -676 L30 -650 L62 -700 Z" fill="{yaka}" {s}/>')
    # kollar + eller
    kisa = m["kol"] == "kisa"
    sol = KOLLAR["bel" if poz in ("salla", "basparmak", "isaret") else poz]
    sol = tuple((-x, y) for x, y in sol)
    sag = KOLLAR[poz]
    kumas = m["gomlek"]
    g += _kol(*sol, kumas, None, kisa) + _el(sol[2], "yumruk" if poz != "duz" else "duz", -1)
    g += _kol(*sag, kumas, None, kisa)
    g += _el(sag[2], {"salla": "acik", "basparmak": "basparmak", "isaret": "isaret"}.get(poz, "duz"), 1)
    # baş
    g += f'<g transform="translate(0 -860)">{_bas(m, ifade)}</g>'
    return f'<g class="usta">{g}</g>'

"""Yüksel Tarım çizim videoları — kaliteli arka plan (derinlikli manzara + perspektif tarla).
manzara(ufuk=1150, sur=None) → SVG parçası. Işık sol üstten (güneş solda).
ARKA_DEFS bir kez sayfaya eklenmeli.
"""
import math, random

ARKA_DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="a_gok" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f93d1"/><stop offset=".5" stop-color="#9fd0f0"/><stop offset=".82" stop-color="#e9f3f2"/><stop offset="1" stop-color="#fbe7c4"/></linearGradient>
<radialGradient id="a_gunes" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fffbe6"/><stop offset=".18" stop-color="#fff2b8" stop-opacity=".95"/><stop offset=".5" stop-color="#ffe7a0" stop-opacity=".35"/><stop offset="1" stop-color="#ffe7a0" stop-opacity="0"/></radialGradient>
<linearGradient id="a_dag1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9c0d6"/><stop offset="1" stop-color="#d4e2ea"/></linearGradient>
<linearGradient id="a_dag2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8eaa9f"/><stop offset="1" stop-color="#bccfbf"/></linearGradient>
<linearGradient id="a_tepe1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc46c"/><stop offset="1" stop-color="#7fa955"/></linearGradient>
<linearGradient id="a_tepe2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb04d"/><stop offset="1" stop-color="#5f8f36"/></linearGradient>
<linearGradient id="a_tarla" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a88158"/><stop offset=".25" stop-color="#8d6640"/><stop offset="1" stop-color="#5a3c22"/></linearGradient>
<linearGradient id="a_sis" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6ead2" stop-opacity="0"/><stop offset="1" stop-color="#f6ead2" stop-opacity=".55"/></linearGradient>
<linearGradient id="a_isik" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1c9" stop-opacity=".28"/><stop offset=".55" stop-color="#fff1c9" stop-opacity="0"/><stop offset="1" stop-color="#3a2a1a" stop-opacity=".18"/></linearGradient>
<filter id="a_yumusak" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="a_bulanik" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="a_doku" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".75 .55" numOctaves="2" seed="4"/>
 <feColorMatrix type="matrix" values="0 0 0 0 .16  0 0 0 0 .1  0 0 0 0 .05  0 0 0 -1.6 1.05"/></filter>
<filter id="a_doku2" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".035 .12" numOctaves="3" seed="9"/>
 <feColorMatrix type="matrix" values="0 0 0 0 .2  0 0 0 0 .13  0 0 0 0 .06  0 0 0 -1.3 .75"/></filter>
</defs></svg>"""


def _bulut(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#a_yumusak)">'
            '<ellipse cx="0" cy="34" rx="170" ry="34" fill="#dbe8f1"/>'
            '<circle cx="-92" cy="8" r="56" fill="#fff"/><circle cx="-20" cy="-30" r="80" fill="#fff"/><circle cx="70" cy="-8" r="62" fill="#fff"/><circle cx="130" cy="20" r="40" fill="#fff"/>'
            '<ellipse cx="0" cy="26" rx="168" ry="34" fill="#fff"/><ellipse cx="20" cy="40" rx="140" ry="14" fill="#d6e4ee"/></g>')


def _agac(x, y, r, rnd):
    """Gölgeli yuvarlak ağaç (ışık soldan)."""
    g = f'<path d="M{x-5} {y} L{x-3} {y-r*1.1} L{x+3} {y-r*1.1} L{x+6} {y} Z" fill="#5a4030"/>'
    for dx, dy, rr, c in [(-.45, 1.25, .7, "#4f8a3a"), (.45, 1.3, .72, "#3f7530"), (0, 1.75, .82, "#5c9a43"), (-.15, 2.1, .5, "#6fae52")]:
        g += f'<circle cx="{x+dx*r:.1f}" cy="{y-dy*r:.1f}" r="{rr*r:.1f}" fill="{c}"/>'
    g += f'<path d="M{x+r*.1:.1f} {y-r*2.5:.1f} A{r*.9:.1f} {r*.9:.1f} 0 0 1 {x+r*1.1:.1f} {y-r*1.3:.1f} A{r*.7:.1f} {r*.7:.1f} 0 0 1 {x+r*.2:.1f} {y-r*.7:.1f} Z" fill="#2f5e26" opacity=".45"/>'
    g += f'<circle cx="{x-r*.4:.1f}" cy="{y-r*2.0:.1f}" r="{r*.22:.1f}" fill="#9fd07a" opacity=".55"/>'
    return g


def _kavak(x, y, h):
    return (f'<path d="M{x-3} {y} L{x-2} {y-h*.2} L{x+2} {y-h*.2} L{x+3} {y} Z" fill="#5a4030"/>'
            f'<path d="M{x} {y-h} C{x-h*.2} {y-h*.75} {x-h*.17} {y-h*.3} {x} {y-h*.14} C{x+h*.17} {y-h*.3} {x+h*.2} {y-h*.75} {x} {y-h} Z" fill="#4a8538"/>'
            f'<path d="M{x} {y-h} C{x+h*.2} {y-h*.75} {x+h*.17} {y-h*.3} {x} {y-h*.14} Z" fill="#336628"/>'
            f'<path d="M{x-h*.06} {y-h*.8} q-{h*.05} {h*.2} 0 {h*.4}" stroke="#7cbf5c" stroke-width="3" fill="none" opacity=".6"/>')


def _ev(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect x="104" y="-176" width="20" height="44" fill="#8d6e63"/><rect x="100" y="-180" width="28" height="8" fill="#6d4c41"/>'
            '<rect x="0" y="-100" width="180" height="100" fill="#f3e3c3"/><rect x="120" y="-100" width="60" height="100" fill="#dcc9a4"/>'
            '<path d="M-16 -96 L90 -170 L196 -96 Z" fill="#b5442f"/><path d="M90 -170 L196 -96 L170 -96 L90 -150 Z" fill="#8f3322"/>'
            '<path d="M-16 -96 L196 -96" stroke="#7a2a1c" stroke-width="5"/>'
            '<rect x="22" y="-70" width="38" height="34" fill="#7fb6d9" stroke="#fff" stroke-width="5"/><path d="M41 -70 V-36 M22 -53 H60" stroke="#fff" stroke-width="3"/>'
            '<rect x="118" y="-62" width="36" height="62" fill="#6d4c41"/><circle cx="146" cy="-30" r="3" fill="#E2B654"/>'
            '<rect x="-6" y="-4" width="192" height="8" fill="#9e8a6a"/></g>')


def manzara(ufuk=1150, sur=None, gunes=True, tohum=3):
    """Gökyüzü + derinlikli arka plan + perspektif tarla. sur: (x1,x2) sürülmüş bölge (ön planda koyu)."""
    rnd = random.Random(tohum)
    U = ufuk
    g = '<rect width="1080" height="1920" fill="url(#a_gok)"/>'
    if gunes:
        g += '<circle cx="230" cy="430" r="330" fill="url(#a_gunes)"/><circle cx="230" cy="430" r="74" fill="#fff6d0"/>'
    g += _bulut(760, 330, 1.0) + _bulut(160, 620, .7) + _bulut(980, 640, .55) + _bulut(520, 520, .45)
    # uzak dağlar (puslu)
    g += (f'<path d="M0 {U-250} L90 {U-300} L170 {U-270} L300 {U-390} L400 {U-320} L520 {U-360} L640 {U-290} L760 {U-380} L880 {U-300} L1000 {U-350} L1080 {U-310} L1080 {U} L0 {U} Z" fill="url(#a_dag1)" filter="url(#a_bulanik)"/>'
          f'<path d="M300 {U-390} L340 {U-352} L318 {U-346} L300 {U-360} L280 {U-344} L262 {U-350} Z M760 {U-380} L798 {U-344} L776 {U-340} L760 {U-352} L740 {U-338} Z" fill="#f4f8fb" opacity=".9"/>'
          f'<path d="M0 {U-190} Q140 {U-260} 280 {U-215} T560 {U-235} T840 {U-205} T1080 {U-230} L1080 {U} L0 {U} Z" fill="url(#a_dag2)"/>')
    # tepeler
    g += f'<path d="M0 {U-120} Q200 {U-190} 420 {U-135} T820 {U-150} T1080 {U-125} L1080 {U} L0 {U} Z" fill="url(#a_tepe1)"/>'
    for x in range(600, 1000, 34):
        g += _kavak(x + rnd.randint(-6, 6), U - 132 + rnd.randint(-4, 6), 96 + rnd.randint(0, 34))
    g += _ev(120, U - 118, .62) + _agac(330, U - 112, 26, rnd) + _agac(380, U - 108, 20, rnd) + _agac(1020, U - 120, 30, rnd)
    g += f'<path d="M0 {U-62} Q300 {U-112} 640 {U-70} T1080 {U-80} L1080 {U} L0 {U} Z" fill="url(#a_tepe2)"/>'
    for x in range(0, 1080, 10):  # çim kenar
        g += f'<path d="M{x} {U-6} l3 -{8+rnd.randint(0,8)} l3 {8}" fill="#4d7a2c"/>'
    g += f'<rect x="0" y="{U-70}" width="1080" height="70" fill="url(#a_sis)"/>'
    # çit (perspektifte)
    for k in range(12):
        x = 40 + k * 92
        g += f'<rect x="{x}" y="{U-58}" width="7" height="44" rx="2" fill="#7a5a44"/>'
    g += f'<path d="M0 {U-48} H1080 M0 {U-30} H1080" stroke="#8a6a52" stroke-width="4"/>'
    # tarla zemin + perspektif sıralar (kaçış noktası ufukta, x=600)
    VP = (600, U - 40)
    g += f'<rect x="0" y="{U}" width="1080" height="{1920-U}" fill="url(#a_tarla)"/>'
    n = 46
    for k in range(-n, n + 1):
        x_alt = VP[0] + k * 150
        x_ust = VP[0] + k * 9
        t0 = U
        if k % 2 == 0:
            x_alt2, x_ust2 = VP[0] + (k + 1) * 150, VP[0] + (k + 1) * 9
            g += f'<path d="M{x_ust} {t0} L{x_ust2} {t0} L{x_alt2} 1920 L{x_alt} 1920 Z" fill="#000" opacity=".09"/>'
        g += f'<path d="M{x_ust} {t0} L{x_alt} 1920" stroke="#3e2a17" stroke-width="{1.5}" opacity=".35"/>'
    # anız (perspektif ölçekli)
    for _ in range(900):
        y = U + 6 + (rnd.random() ** 1.7) * (1920 - U - 10)
        d = (y - U) / (1920 - U)
        x = rnd.uniform(-40, 1120)
        h = 4 + d * 26
        w = 1 + d * 3
        g += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(-.3,.3)*h:.1f} -{h:.1f}" stroke="#e0c27a" stroke-width="{w:.1f}" stroke-linecap="round" opacity="{.55+d*.4:.2f}"/>'
    # toprak dokusu
    g += f'<rect x="0" y="{U}" width="1080" height="{1920-U}" filter="url(#a_doku)" opacity=".55"/>'
    g += f'<rect x="0" y="{U}" width="1080" height="{1920-U}" filter="url(#a_doku2)" opacity=".5"/>'
    # ufuk pusu
    g += f'<rect x="0" y="{U-10}" width="1080" height="70" fill="#f6ead2" opacity=".25"/>'
    # ön plan çim öbekleri
    for cx, cy, s in [(30, 1890, 1.2), (1050, 1880, 1.1), (160, 1910, .8), (920, 1915, .8)]:
        for j in range(14):
            a = -70 + j * 10
            L = (60 + (j % 4) * 22) * s
            ex, ey = cx + math.sin(math.radians(a)) * L, cy - math.cos(math.radians(a)) * L
            g += f'<path d="M{cx-6} {cy} Q{(cx+ex)/2:.0f} {(cy+ey)/2-10:.0f} {ex:.0f} {ey:.0f} Q{(cx+ex)/2+8:.0f} {(cy+ey)/2:.0f} {cx+6} {cy} Z" fill="{["#5f8f36","#77a84a","#4d7a2c"][j%3]}"/>'
    return g


def isik():
    """Sahnenin en üstüne konur: sol üstten sıcak ışık, sağ alttan hafif gölge."""
    return '<rect width="1080" height="1920" fill="url(#a_isik)"/>'

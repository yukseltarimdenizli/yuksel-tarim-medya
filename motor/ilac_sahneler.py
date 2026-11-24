"""Dayı Soruyor — ilaçlama makinesi (pülverizatör) kış bakımı sahneleri (ilk kullanım: #4).
Pülverizatör arkadan görünüşle çizilir (depo, pompa + yağ haznesi, manometre, memeli bom): pulv().
Sahneler:
  idayi     karlı dayı sorusu; ahır önünde pülverizatör; kanca hapı
  ibes      'pompa çatlar' + 5 adım kartı (5. altın)
  icalkala  depo 3 kez dolup boşalır, sayaç; eldiven + maske hapı (1/5)
  idok      çalkalama suyu: tarlaya ✅, çeşme/dere/kanal ❌
  ifiltre   şema: depo → emiş filtresi → pompa → basınç filtresi → bom + meme filtreleri (2/5)
  imeme     büyük meme: yumuşak fırça ✅, iğne/tel ❌ (2/5)
  idon      su donar, pompa + manometre çatlar (3/5)
  iyag      yağ gözetleme camı: normal ↔ süt gibi (4/5)
  itest     meme testi: kaplar dolar (faz 1) / sapma, aşınmış meme (faz 2) (5/5)
  ikapanis  5 adım özeti + takip
Diğerleri soguk_sahneler'den: smadde, skaydet, ktepki.
"""
import dayi_video as dv
import dayi
import kis_sahneler as ks
import soguk_sahneler as ss
from toprak_sahneler import pop, hap, kart, emo, tik, zemin_krem, _kt

U = "<!--UST-->"
_N = [0]
TURUNCU = "#ef6c00"
MAVI = "#1565c0"


# ---------------------------------------------------------------- pülverizatör (arkadan, yerel: zemin y=0, merkez x=0)
def pulv(su=0.0, memeler=9, bom=520, catlak=False):
    _N[0] += 1
    cid = f"pvt{_N[0]}"
    y_alt, y_ust = -254, -566
    h = (y_alt - y_ust) * su
    g = '<ellipse cx="0" cy="8" rx="320" ry="18" fill="#000" opacity=".15"/>'
    # bom (en arkada)
    g += (f'<path d="M{-bom} -70 H{bom}" stroke="#37474f" stroke-width="18" stroke-linecap="round"/>'
          f'<path class="suyol" d="M{-bom+8} -70 H{bom-8}" stroke="#90a4ae" stroke-width="7" stroke-linecap="round"/>')
    adim = (2 * bom - 80) / max(1, memeler - 1)
    for k in range(memeler):
        x = -bom + 40 + k * adim
        g += (f'<g class="meme" data-x="{x:.0f}"><rect x="{x-9:.0f}" y="-66" width="18" height="22" fill="#546e7a"/>'
              f'<path d="M{x-14:.0f} -46 H{x+14:.0f} L{x+7:.0f} -24 H{x-7:.0f} Z" fill="{TURUNCU}" stroke="#a84300" stroke-width="3"/></g>')
    # şase ve ayaklar
    g += ('<rect x="-212" y="-236" width="26" height="236" rx="6" fill="#37474f"/><rect x="186" y="-236" width="26" height="236" rx="6" fill="#37474f"/>'
          '<rect x="-244" y="-252" width="488" height="30" rx="8" fill="#455a64"/>'
          '<rect x="-236" y="-12" width="70" height="14" rx="6" fill="#263238"/><rect x="166" y="-12" width="70" height="14" rx="6" fill="#263238"/>')
    # depo
    g += (f'<defs><clipPath id="{cid}"><rect x="-224" y="-596" width="448" height="342" rx="66"/></clipPath></defs>'
          '<rect x="-230" y="-602" width="460" height="354" rx="70" fill="#f5f5f5" stroke="#90a4ae" stroke-width="8"/>'
          f'<g clip-path="url(#{cid})"><rect class="su" data-alt="{y_alt}" data-ust="{y_ust}" x="-230" y="{y_alt-h:.0f}" width="460" height="{h:.0f}" fill="#4fc3f7" opacity=".8"/>'
          f'<path class="dalga" d="" fill="#81d4fa" opacity=".9"/></g>'
          + "".join(f'<path d="M150 {-300-k*60} h40" stroke="#90a4ae" stroke-width="5"/>' for k in range(5)) +
          '<path d="M-190 -560 Q-200 -420 -190 -290" stroke="#fff" stroke-width="16" stroke-linecap="round" fill="none" opacity=".8"/>'
          '<rect x="-64" y="-632" width="128" height="36" rx="12" fill="#ef6c00" stroke="#a84300" stroke-width="5"/>')
    # hortumlar (pompa → bom, depo → pompa)
    g += ('<path d="M-40 -250 V-210" stroke="#263238" stroke-width="22"/><path class="suyol" d="M-40 -250 V-210" stroke="#90a4ae" stroke-width="9"/>'
          '<path d="M44 -150 Q130 -150 140 -76" stroke="#263238" stroke-width="22" fill="none" stroke-linecap="round"/>'
          '<path class="suyol" d="M44 -150 Q130 -150 140 -76" stroke="#90a4ae" stroke-width="9" fill="none" stroke-linecap="round"/>')
    # pompa + yağ haznesi
    g += ('<g class="pompa"><rect x="-120" y="-210" width="164" height="112" rx="20" fill="#c62828" stroke="#7f1414" stroke-width="6"/>'
          '<circle cx="-38" cy="-154" r="34" fill="#7f1414"/><circle class="suyol pompaic" cx="-38" cy="-154" r="24" fill="#90a4ae"/>'
          '<rect x="-112" y="-262" width="40" height="54" rx="8" fill="#ffe082" fill-opacity=".85" stroke="#8d6e63" stroke-width="4"/>'
          '<rect class="yagkap" x="-108" y="-240" width="32" height="30" rx="5" fill="#f9a825"/>'
          + ('<path class="catlak" d="M-100 -206 l22 26 l-14 18 l26 22 l-10 20" stroke="#212121" stroke-width="6" fill="none" stroke-linejoin="round" opacity="0"/>' if catlak else "")
          + '</g>')
    # manometre
    g += ('<path d="M226 -246 V-386" stroke="#455a64" stroke-width="12"/>'
          '<g class="mano"><circle cx="226" cy="-430" r="46" fill="#fff" stroke="#455a64" stroke-width="8"/>'
          '<path d="M196 -420 A32 32 0 1 1 256 -420" stroke="#cfd8dc" stroke-width="6" fill="none"/>'
          '<path class="mibre" d="M226 -430 L248 -452" stroke="#c62828" stroke-width="6" stroke-linecap="round"/><circle cx="226" cy="-430" r="6" fill="#263238"/>'
          + ('<path class="catlak" d="M200 -462 l18 20 l-8 14 l22 18" stroke="#212121" stroke-width="5" fill="none" opacity="0"/>' if catlak else "")
          + '</g>')
    return g


def rozet(no, renk):
    return ss.rozet(no, 5, renk)


def ahir(x, y, s):
    return f'<g transform="translate({x} {y}) scale({s})">{ks.p_ahir()}</g>'


# ---------------------------------------------------------------- sahneler
def s_idayi(p):
    A = p.get("_a", {})
    g = ks.kis_arka()
    g += ahir(400, 470, .62)
    g += f'<g transform="translate(700 1185) scale(.5)">{pulv(0)}</g>'
    g += dv.kisi(925, 1300, .55, "genc", "duz", "normal", "kisi-usta")
    g += dv.kisi(300, 2050, 1.42, "kasketli", "bel", "mutlu", "kisi-dayi")
    g += ks.kar_katmani()
    g += U
    if p.get("kanca"):
        g += pop(hap(540, 196, p["kanca"], "#c62828", "#fff", 38), A.get("kanca", 12), 540, 196)
    g += '<g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["?"]), 300, 640, 52) + '</g>'
    return g, (340, 860, 1.0, 1.12)


def s_ibes(p):
    A = p.get("_a", {})
    g = zemin_krem()
    g += pop(hap(440, 545, "Baharda pompa çatlak çıkar! 💥", "#c62828", "#fff", 38), A.get("catlak", 30), 440, 545)
    yer = [(220, 750), (540, 750), (860, 750), (380, 990), (700, 990)]
    for i, (cx, cy) in enumerate(yer):
        son = i == 4
        icerik = (kart(cx - 140, cy - 110, 280, 220, "#E2B654" if son else "#fff", 32)
                  + f'<text x="{cx}" y="{cy-34}" text-anchor="middle" font-size="40" font-weight="900" fill="{"#14281A" if son else "#7a6a48"}">{i+1}. ADIM</text>'
                  + f'<text x="{cx}" y="{cy+82}" text-anchor="middle" font-size="110" font-weight="900" fill="{"#c62828" if son else "#2F5737"}">?</text>')
        g += pop(icerik, A.get(f"k{i}", 60 + i * 6), cx, cy)
    g += pop(hap(540, 1180, "Sonuncusunu çoğu kişi bilmiyor 👇", "#c62828", "#fff", 40), A.get("son", 110), 540, 1180)
    g += U + dv.baslik("5 ADIM VAR", TURUNCU) + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_icalkala(p):
    A = p.get("_a", {})
    g = ks.kis_arka(1210) + f'<g transform="translate(540 1210) scale(.68)">{pulv(.0)}</g>' + ks.kar_katmani()
    g += pop(hap(410, 520, "Depoyu boşalt", "#455a64", "#fff", 38), A.get("bosalt", 20), 410, 520)
    for k in range(3):
        x = 140 + k * 120
        g += pop(f'<circle cx="{x}" cy="640" r="50" fill="{MAVI}" stroke="#fff" stroke-width="6" filter="url(#golge)"/>'
                 f'<text x="{x}" y="660" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">{k+1}</text>', A.get(f"c{k}", 60 + k * 30), x, 640)
    g += pop('<text x="430" y="658" font-size="46" font-weight="900" fill="#14281A">kere çalkala</text>', A.get("c2", 120), 560, 640)
    g += pop(hap(380, 1265, "🧤 Eldiven  ·  😷 Maske", "#2e7d32", "#fff", 38), A.get("eldiven", 150), 380, 1265)
    g += U + rozet(1, MAVI) + dv.baslik("ÇALKALA", MAVI) + dv.pip(925, 460, 110)
    return g, (540, 1000, 1.0, 1.04)


def s_idok(p):
    A = p.get("_a", {})
    g = zemin_krem()
    g += pop(kart(90, 620, 820, 180, "#e8f5e9", 40) + emo(200, 745, "🌾", 96)
             + '<text x="290" y="700" font-size="48" font-weight="900" fill="#2e7d32">İlaçladığın</text>'
             + '<text x="290" y="764" font-size="48" font-weight="900" fill="#2e7d32">tarlaya sık</text>'
             + tik(840, 710, 44, True), A.get("tarla", 30), 500, 710)
    for i, (e, ad) in enumerate([("🚰", "Çeşme başı"), ("🏞️", "Dere"), ("💧", "Kanal")]):
        cx = 220 + i * 320
        g += pop(kart(cx - 140, 840, 280, 240, "#fff", 36) + emo(cx, 965, e, 90)
                 + f'<text x="{cx}" y="1040" text-anchor="middle" font-size="34" font-weight="900" fill="#c62828">{ad}</text>'
                 + f'<path d="M{cx-105} 870 L{cx+105} 1050 M{cx+105} 870 L{cx-105} 1050" stroke="#e53935" stroke-width="11" stroke-linecap="round" opacity=".55"/>',
                 A.get(f"x{i}", 90 + i * 10), cx, 950)
    g += pop(hap(500, 1190, "ASLA DÖKME!", "#c62828", "#fff", 50), A.get("asla", 130), 500, 1190)
    g += U + dv.baslik("ÇALKALAMA SUYU", MAVI) + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def filtre(x, y, ad, t, yika, lx, ly):
    return (f'<g><rect x="{x-34}" y="{y-56}" width="68" height="112" rx="16" fill="#eceff1" stroke="#455a64" stroke-width="6"/>'
            f'<rect class="kir" data-t="{int(yika)}" x="{x-22}" y="{y-42}" width="44" height="84" rx="8" fill="#8d6e63"/>'
            + "".join(f'<path d="M{x-22} {y-30+k*18} h44" stroke="#5d4037" stroke-width="3" opacity=".6"/>' for k in range(4)) + '</g>'
            + ks.etk(lx, ly, x, y + 60, ad, t, TURUNCU))


def s_ifiltre(p):
    A = p.get("_a", {})
    Y, B = 700, 980
    g = zemin_krem()
    boru = 'stroke="#455a64" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    g += f'<path d="M180 620 V{Y} H880 V{B}" {boru}/><path d="M140 {B} H940" {boru}/>'
    g += ('<rect x="90" y="470" width="180" height="160" rx="32" fill="#f5f5f5" stroke="#90a4ae" stroke-width="7"/>'
          '<rect x="96" y="548" width="168" height="76" rx="24" fill="#4fc3f7" opacity=".8"/>'
          '<text x="180" y="528" text-anchor="middle" font-size="32" font-weight="900" fill="#455a64">DEPO</text>')
    g += (f'<rect x="470" y="{Y-60}" width="150" height="120" rx="20" fill="#c62828" stroke="#7f1414" stroke-width="6"/>'
          f'<text x="545" y="{Y+12}" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">POMPA</text>')
    yika = A.get("yika", 200)
    g += filtre(330, Y, "Emiş filtresi", A.get("emis", 40), yika, 290, 850)
    g += filtre(740, Y, "Basınç filtresi", A.get("basinc", 80), yika, 720, 850)
    for k in range(5):
        x = 180 + k * 180
        g += (f'<rect x="{x-12}" y="{B+6}" width="24" height="26" fill="#546e7a"/><path d="M{x-18} {B+30} H{x+18} L{x+9} {B+56} H{x-9} Z" fill="{TURUNCU}"/>'
              f'<rect class="kir" data-t="{int(yika)}" x="{x-10}" y="{B-20}" width="20" height="18" rx="4" fill="#8d6e63"/>')
    g += pop(hap(540, 1090, "Meme filtreleri", TURUNCU, "#fff", 38), A.get("meme", 120), 540, 1090)
    g += pop(hap(540, 1200, "Sök, bol suyla yıka 💦", "#2e7d32", "#fff", 42), yika, 540, 1200)
    g += '<g class="damlalar"></g>'
    g += U + rozet(2, TURUNCU) + dv.baslik("FİLTRELER", TURUNCU) + dv.pip(925, 460, 110)
    return g, (540, 860, 1.0, 1.03)


def s_imeme(p):
    A = p.get("_a", {})
    g = zemin_krem()
    # büyük meme (yandan)
    g += ('<g transform="translate(540 650)"><rect x="-60" y="-200" width="120" height="110" rx="14" fill="#546e7a" stroke="#37474f" stroke-width="6"/>'
          '<path d="M-120 -96 H120 L80 70 H-80 Z" fill="#ef6c00" stroke="#a84300" stroke-width="8" stroke-linejoin="round"/>'
          '<rect x="-36" y="62" width="72" height="26" rx="8" fill="#a84300"/><rect x="-26" y="70" width="52" height="10" rx="5" fill="#212121"/>'
          '<text x="0" y="0" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">MEME</text>'
          '<g class="sprey" opacity="0">' + "".join(f'<path d="M0 92 L{dx} 230" stroke="#4fc3f7" stroke-width="8" stroke-linecap="round" opacity=".8"/>' for dx in (-120, -60, 0, 60, 120)) + '</g></g>')
    g += '<g class="firca"><text x="300" y="850" text-anchor="middle" font-size="120">🪥</text></g>'
    g += pop(kart(90, 930, 420, 150, "#e8f5e9", 36) + '<text x="300" y="995" text-anchor="middle" font-size="40" font-weight="900" fill="#2e7d32">Yumuşak fırça</text>'
             + '<text x="300" y="1048" text-anchor="middle" font-size="34" font-weight="800" fill="#2e7d32">ile temizle</text>' + tik(470, 935, 34, True), A.get("firca", 50), 300, 1000)
    g += pop(kart(530, 930, 420, 150, "#ffebee", 36) + emo(610, 1030, "📍", 70)
             + '<text x="770" y="995" text-anchor="middle" font-size="40" font-weight="900" fill="#c62828">İğne, tel</text>'
             + '<text x="770" y="1048" text-anchor="middle" font-size="34" font-weight="800" fill="#c62828">ile kurcalama</text>' + tik(910, 935, 34, False), A.get("igne", 110), 740, 1000)
    g += pop(hap(510, 1185, "Deliği bozulur, ilacı eşit atmaz!", "#c62828", "#fff", 40), A.get("bozulur", 170), 510, 1185)
    g += U + rozet(2, TURUNCU) + dv.baslik("MEMELER", TURUNCU) + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_idon(p):
    A = p.get("_a", {})
    g = ks.kis_arka(1190) + f'<g transform="translate(480 1190) scale(.7)">{pulv(0, catlak=True)}</g>' + ks.p_termometre(985, 1190, "termo") + ks.kar_katmani()
    g += '<g class="buzlar"></g>'
    # pompa ≈ (500-30, 1250-124), hortum ≈ (590,1130), bom ≈ (200, 1194), manometre ≈ (681, 906)
    g += ks.etk(190, 880, 453, 1082, "Pompa", A.get("pompa", 40), "#c62828")
    g += ks.etk(800, 1010, 560, 1096, "Hortum", A.get("hortum", 60), MAVI)
    g += ks.etk(170, 1000, 130, 1141, "Borular", A.get("boru", 80), MAVI)
    g += pop(hap(470, 660, "Donan su pompayı çatlatır!", "#c62828", "#fff", 40), A.get("catla", 150), 470, 660)
    g += pop(hap(380, 545, "En önemlisi!", "#c62828", "#fff", 40), A.get("onemli", 20), 380, 545)
    g += U + rozet(3, "#c62828") + dv.baslik("İÇERİDE SU BIRAKMA", MAVI) + dv.pip(925, 460, 110)
    return g, (520, 1000, 1.0, 1.04)


def gozcam(x, y, cls, renk, ad, adrenk):
    return (f'<g transform="translate({x} {y})"><rect x="-120" y="-200" width="240" height="330" rx="36" fill="#c62828" stroke="#7f1414" stroke-width="8"/>'
            '<circle cx="0" cy="-36" r="96" fill="#7f1414"/><circle cx="0" cy="-36" r="80" fill="#fff"/>'
            f'<circle class="{cls}" cx="0" cy="-36" r="74" fill="{renk}"/>'
            '<path d="M-44 -82 Q-60 -40 -40 0" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".6"/>'
            f'<text x="0" y="104" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">{ad}</text></g>')


def s_iyag(p):
    A = p.get("_a", {})
    g = zemin_krem()
    g += pop(gozcam(250, 770, "yag1", "#f9a825", "NORMAL", "#fff") + tik(340, 610, 40, True), A.get("bak", 50), 250, 770)
    g += pop(gozcam(690, 770, "yag2", "#f9a825", "SÜT GİBİ", "#fff") + f'<g class="yagx" opacity="0">{tik(780, 610, 40, False)}</g>', A.get("bak", 50) + 6, 690, 770)
    g += pop(hap(690, 960, "Membran delinmiş", "#c62828", "#fff", 36), A.get("delik", 140), 690, 960)
    g += pop(hap(480, 1070, "Membranı değiştir 🔧", "#14281A", "#FFD54F", 42), A.get("degis", 190), 480, 1070)
    g += pop(hap(480, 1185, "Yağı yenile 🛢️", "#2e7d32", "#fff", 42), A.get("yenile", 220), 480, 1185)
    g += U + rozet(4, "#8d6e00") + dv.baslik("POMPA YAĞI", "#8d6e00") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_itest(p):
    A = p.get("_a", {})
    faz = p.get("faz", 1)
    g = zemin_krem()
    BY, KU, KA, KH = 650, 880, 1110, 210      # bom y, kap üstü, kap tabanı, dolu yükseklik ölçeği
    xs = [150 + k * 156 for k in range(6)]
    g += f'<path d="M90 {BY} H990" stroke="#37474f" stroke-width="20" stroke-linecap="round"/>'
    sev = p.get("seviye", [0.62, 0.6, 0.63, 0.86, 0.61, 0.6])
    for k, x in enumerate(xs):
        kotu = faz == 2 and sev[k] > 0.75
        g += (f'<rect x="{x-10}" y="{BY+6}" width="20" height="26" fill="#546e7a"/><path d="M{x-18} {BY+30} H{x+18} L{x+9} {BY+54} H{x-9} Z" fill="{TURUNCU}" stroke="#a84300" stroke-width="3"/>'
              f'<g class="sprey2" opacity="0">' + "".join(f'<path d="M{x} {BY+58} L{x+dx} {KU-10}" stroke="#4fc3f7" stroke-width="6" stroke-linecap="round" opacity=".7"/>' for dx in (-40, -14, 14, 40)) + '</g>')
        g += (f'<g><path d="M{x-56} {KU} L{x-48} {KA+4} H{x+48} L{x+56} {KU}" fill="#fff" fill-opacity=".7" stroke="{"#c62828" if kotu else "#90a4ae"}" stroke-width="{8 if kotu else 6}"/>'
              f'<rect class="kap" data-h="{sev[k]*KH:.0f}" data-b="{KA}" x="{x-50}" y="{KA}" width="100" height="0" fill="{"#ef5350" if kotu else "#4fc3f7"}" opacity=".8"/>'
              + "".join(f'<path d="M{x+26} {KA-j*48} h22" stroke="#90a4ae" stroke-width="4"/>' for j in range(1, 5)) + '</g>')
    if faz == 1:
        g += pop(hap(440, 545, "Çoğu kişi bunu atlıyor!", "#c62828", "#fff", 40), A.get("atla", 30), 440, 545)
        g += pop(hap(540, 1200, "Baharda, ilk ilaçlamadan önce", "#2F5737", "#fff", 40), A.get("bahar", 90), 540, 1200)
        g += pop(f'<g transform="translate(540 {(BY+KU)//2+10})"><rect x="-190" y="-52" width="380" height="96" rx="48" fill="#14281A" filter="url(#golge)"/>'
                 '<text x="0" y="14" text-anchor="middle" font-size="48" font-weight="900" fill="#FFD54F">⏱ 1 dakika</text></g>', A.get("dakika", 200), 540, (BY + KU) // 2)
    else:
        ort = KA - 0.615 * KH
        g += pop(f'<path d="M80 {ort:.0f} H1000" stroke="#2e7d32" stroke-width="6" stroke-dasharray="18 12"/>'
                 f'<text x="90" y="{ort-14:.0f}" font-size="32" font-weight="900" fill="#2e7d32">ORTALAMA</text>', A.get("ort", 20), 540, ort)
        kx = xs[max(range(6), key=lambda i: sev[i])]
        g += pop(hap(kx - 60, (BY + KU) // 2 + 10, "%10'dan fazla! ❌", "#c62828", "#fff", 36), A.get("fazla", 60), kx - 60, (BY + KU) // 2)
        g += pop(hap(540, 1200, "Aşınmış meme → DEĞİŞTİR", "#c62828", "#fff", 42), A.get("degis", 90), 540, 1200)
        g += pop(hap(440, 545, "İlaç boşa gider, ürün zarar görür", "#14281A", "#FFD54F", 34), A.get("bosa", 160), 440, 545)
    g += U + rozet(5, "#b8860b") + dv.baslik("MEME TESTİ", "#b8860b") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_ikapanis(p):
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70)])
    g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
    g += '<text x="540" y="400" text-anchor="middle" font-size="46" font-weight="900" fill="#E2B654">BAHARDA İLK GÜNDEN HAZIR</text>'
    M = [("💦", "Çalkala"), ("🧽", "Filtre, meme"), ("🧊", "Su bırakma"), ("🛢️", "Pompa yağı"), ("📏", "Meme testi")]
    for i, (e, ad) in enumerate(M):
        x, y = (290 + (i % 2) * 500, 500 + (i // 2) * 112) if i < 4 else (290, 724)
        g += pop(f'<rect x="{x-225}" y="{y-44}" width="450" height="88" rx="44" fill="#fff" filter="url(#golge)"/>' + emo(x - 160, y + 17, e, 46)
                 + f'<text x="{x-115}" y="{y+15}" font-size="42" font-weight="900" fill="#2F5737">{ad}</text>', 4 + i * 5, x, y)
    g += dv.kisi(300, 1770, .95, "kasketli", "salla", "mutlu", "kisi-dayi")
    g += ('<g class="takip" transform="translate(600 860)"><rect class="btn" width="400" height="110" rx="55" fill="#FE2C55" filter="url(#golge)"/>'
          '<text class="btnyazi" x="200" y="74" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">+ Takip et</text><text class="el" x="230" y="200" font-size="110">👆</text></g>')
    g += '<text x="760" y="1200" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">Seri devam ediyor!</text>'
    return g, (540, 1100, 1.0, 1.03)


dv.SAHNELER.update({"idayi": s_idayi, "ibes": s_ibes, "icalkala": s_icalkala, "idok": s_idok, "ifiltre": s_ifiltre, "imeme": s_imeme,
                    "idon": s_idon, "iyag": s_iyag, "itest": s_itest, "ikapanis": s_ikapanis})


def _calkala(p, kt, n):
    s0 = _kt(kt, "temiz", 40)
    s1 = max(s0 + 90, _kt(kt, "eldivenini", n - 40) - 4)
    a = {"bosalt": _kt(kt, "boşalt", 20) - 2, "s0": s0, "s1": s1, "eldiven": _kt(kt, "eldivenini", 150) - 2}
    for k in range(3):
        a[f"c{k}"] = int(s0 + (k + 0.5) * (s1 - s0) / 3)
    return a


dv.ANIM_EK.update({
    "idayi": lambda p, kt, n: {"kanca": 12},
    "ibes": lambda p, kt, n: {"catlak": _kt(kt, "çatlak", 30) - 4, **{f"k{i}": _kt(kt, "beş", 60) + i * 5 for i in range(5)}, "son": _kt(kt, "sonuncusunu", 110) - 2},
    "icalkala": _calkala,
    "idok": lambda p, kt, n: {"tarla": _kt(kt, "ilaçladığın", 30) - 2, "x0": _kt(kt, "çeşme", 90) - 2, "x1": _kt(kt, "dereye", 100) - 2, "x2": _kt(kt, "kanala", 110) - 2, "asla": _kt(kt, "asla", 130) - 2},
    "ifiltre": lambda p, kt, n: {"emis": _kt(kt, "emiş", 40) - 2, "basinc": _kt(kt, "basınç", 80) - 2, "meme": _kt(kt, "meme", 120) - 2, "yika": _kt(kt, "bol", 200) - 2},
    "imeme": lambda p, kt, n: {"firca": _kt(kt, "yumuşak", 50) - 2, "igne": _kt(kt, "iğneyle", 110) - 2, "bozulur": _kt(kt, "deliği", 170) - 2},
    "idon": lambda p, kt, n: {"onemli": _kt(kt, "önemlisi", 20) - 4, "pompa": _kt(kt, "pompada", 40) - 2, "hortum": _kt(kt, "hortumda", 60) - 2, "boru": _kt(kt, "borularda", 80) - 2,
                              "don": _kt(kt, "donunca", 120) - 4, "catla": _kt(kt, "çatlatır", 150) - 4},
    "iyag": lambda p, kt, n: {"bak": _kt(kt, "membranlı", 50) - 2, "sut": _kt(kt, "süt", 110) - 2, "delik": _kt(kt, "delinmiştir", 140) - 4, "degis": _kt(kt, "değiştir", 190) - 2, "yenile": _kt(kt, "yenile", 220) - 4},
    "itest": lambda p, kt, n: ({"atla": _kt(kt, "atladığı", 30) - 4, "bahar": _kt(kt, "baharda", 90) - 2, "kap": _kt(kt, "kap", 160) - 2, "sprey": _kt(kt, "kap", 160) - 2, "dakika": _kt(kt, "dakika", 200) - 2}
                               if p.get("faz", 1) == 1 else {"ort": _kt(kt, "ortalamadan", 20) - 2, "fazla": _kt(kt, "fazla", 60) - 2, "degis": _kt(kt, "değiştir", 90) - 2, "bosa": _kt(kt, "boşa", 160) - 4}),
    "ikapanis": lambda p, kt, n: {"tap": _kt(kt, "takip", 40)},
})

dv.JS_EK += r"""
function suseviye(el,f){ const s=$('.su',el); if(!s) return; const a=+s.dataset.alt, u=+s.dataset.ust, h=(a-u)*Math.max(0,Math.min(1,f)); s.setAttribute('y',(a-h).toFixed(1)); s.setAttribute('height',h.toFixed(1)); }
Object.assign(SAHNE,{
 idayi(el,t){ kar(el,t); sallan(el,t); balon(el,t); poplar(el,t); },
 ibes(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 icalkala(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), S0=A.s0??40, S1=A.s1??200;
   let f; if(t<(A.bosalt??20)) f=0.55; else if(t<S0) f=0.55*(1-ease((t-(A.bosalt??20))/12)); else if(t<S1){ const p=(t-S0)/(S1-S0)*3; f=0.5*Math.sin((p%1)*Math.PI); } else f=0;
   suseviye(el,f); const d=$('.dalga',el); if(d&&f>0.02){ const a=+$('.su',el).dataset.alt, u=+$('.su',el).dataset.ust, y=a-(a-u)*f; let s=`M-230 ${y}`; for(let x=-230;x<=230;x+=20){ s+=` L${x} ${(y+Math.sin(x*0.03+t*0.5)*10*Math.min(1,f*4)).toFixed(1)}`; } s+=` L230 ${y+14} L-230 ${y+14} Z`; d.setAttribute('d',s);} else if(d) d.setAttribute('d',''); },
 idok(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 ifiltre(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); halkalar(el,t); $$('.kir',el).forEach(k=>{ const e=ease((t-(+k.dataset.t)-6)/14); k.setAttribute('fill', e>=1?'#e3f2fd':`rgb(${Math.round(141+86*e)},${Math.round(110+132*e)},${Math.round(99+154*e)})`); });
   const A=JSON.parse(el.dataset.a||'{}'), Y=A.yika??200; let s=''; if(t>=Y){ for(let i=0;i<14;i++){ const p=((t-Y)*1.4+i*9)%40/40; [330,740].forEach(x=>{ s+=`<circle cx="${x-30+(i*17)%60}" cy="${(640+p*140).toFixed(1)}" r="5" fill="#29b6f6" opacity="${(1-p).toFixed(2)}"/>`; }); } } $('.damlalar',el).innerHTML=s; },
 imeme(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), F=A.firca??50, I=A.igne??110; const fr=$('.firca',el);
   const aktif=t>=F&&t<I; const e=ease((t-F)/10); fr.setAttribute('transform', `translate(${(e*180+(aktif?Math.sin(t*0.9)*30:0)).toFixed(1)} ${(-e*60).toFixed(1)})`); fr.setAttribute('opacity', t<F-2?0:(t>=I?Math.max(0,1-(t-I)/10):1));
   $('.sprey',el).setAttribute('opacity', t>=I-10&&t<I? 1:0); },
 idon(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); halkalar(el,t); const A=JSON.parse(el.dataset.a||'{}'), D=A.don??120, C=A.catla??150;
   const m=$('.termo',el); if(m){ const e=ease(t/40), h=230-190*e; m.setAttribute('y',-60-h); m.setAttribute('height',h); }
   const k=ease((t-D)/16); $$('.suyol',el).forEach(s=>{ const c=`rgb(${Math.round(79+150*k)},${Math.round(195+50*k)},${Math.round(247+5*k)})`; if(s.tagName==='circle') s.setAttribute('fill',t<10?'#90a4ae':c); else s.setAttribute('stroke',t<10?'#90a4ae':c); });
   $$('.catlak',el).forEach(c=>c.setAttribute('opacity', t>=C?1:0)); let s=''; if(t>=D){ [[453,1082],[557,1096],[200,1141],[410,1141],[690,1141]].forEach(([x,y],i)=>{ const e=spring(t-D-i*3,0.25); s+=`<text x="${x}" y="${y+14}" text-anchor="middle" font-size="${(44*Math.min(e,1.1)).toFixed(1)}">❄️</text>`; }); } $('.buzlar',el).innerHTML=s;
   const mn=$('.mano',el); if(mn&&t>=C&&t<C+8){ mn.setAttribute('transform',`translate(${Math.sin(t*3)*4} 0)`); } else if(mn) mn.setAttribute('transform',''); },
 iyag(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), S=A.sut??110; const e=ease((t-S)/16);
   const y=$('.yag2',el); if(y) y.setAttribute('fill',`rgb(${Math.round(249+(245-249)*e)},${Math.round(168+(243-168)*e)},${Math.round(37+(230-37)*e)})`); const x=$('.yagx',el); if(x) x.setAttribute('opacity',e>=1?1:0); },
 itest(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), P=window.PARCALAR[+el.closest('.p').id.slice(1)], faz=P.faz||1;
   const SP=A.sprey??200; const on = faz===1 ? t>=SP : t<22; $$('.sprey2',el).forEach((s,i)=>s.setAttribute('opacity', on? (0.6+0.4*Math.sin(t*0.8+i)).toFixed(2):0));
   $$('.kap',el).forEach(k=>{ const H=+k.dataset.h; const f= faz===1 ? 0.55*Math.min(1,Math.max(0,(t-SP)/60)) : 0.55+0.45*ease(t/24); const h=H*f; k.setAttribute('y',(+k.dataset.b-h).toFixed(1)); k.setAttribute('height',h.toFixed(1)); }); },
 ikapanis(el,t){ SAHNE.skapanis(el,t); },
});
"""

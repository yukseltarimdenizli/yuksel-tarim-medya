"""Dayı Soruyor — soğukta zor çalışma / beyaz duman sahneleri (ilk kullanım: #3 "Traktör soğukta geç çalışıyor").
Sahneler:
  sdayi     karlı dayı sorusu; egzozdan beyaz duman (duman: false ile kapatılır), kanca: ilk saniyede merak hapı
  sdort     4 sebep kartı (1-3 '?', 4. altın 'çoğu kişi bilmiyor')
  ssilindir dizel silindir: piston havayı sıkıştırır, ısınır, yakıt püskürür, ateşler
  sduman    karlı traktör + beyaz duman + termometre, etiketli
  skontrol  kis_sahneler.kkontrol + toplam (no/toplam rozet) + hap [metin, kok, renk] + sarj_yok + prop 'mum'
  skizdirma gösterge paneli: kontak, kızdırma lambası yanar/söner, sonra marş
  skaydet   'Kaydet, lazım olur' + sağ kenardaki kaydet tuşuna el
  smadde    krem liste: maddeler [[emoji, metin, kok, isaret(ok|x|uyari)], ...]
  sates     depo altında ateş + yasak işareti + hap
  skapanis  4 sebep özeti + takip düğmesi + el sallayan Hasan Dayı
Kullanım: import soguk_sahneler (kis_sahneler'i de yükler).
"""
import dayi_video as dv
import dayi
import kis_sahneler as ks
from cizim import traktor
from toprak_sahneler import pop, hap, kart, emo, tik, zemin_krem, _kt

U = "<!--UST-->"
EGZOZ = ks.tp(311, -560)


def uyari_isaret(x, y, r=30):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fb8c00" stroke="#fff" stroke-width="5"/>'
            f'<text x="{x}" y="{y+r*.42:.0f}" text-anchor="middle" font-size="{r*1.3:.0f}" font-weight="900" fill="#fff">!</text>')


def isaret(kind, x, y, r=30):
    if kind == "x":
        return tik(x, y, r, False)
    if kind == "uyari":
        return uyari_isaret(x, y, r)
    return tik(x, y, r, True)


def rozet(no, toplam, renk):
    return (f'<g><rect x="50" y="360" width="210" height="96" rx="48" fill="{renk}" filter="url(#golge)"/>'
            f'<text x="155" y="424" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">{no}/{toplam}</text></g>')


# ---------------------------------------------------------------- props
def p_mum(x=905, y=1205):
    """Yazlık motorin bidonu + içi mum (parafin) kristalli filtre kabı."""
    g = (f'<g transform="translate({x} {y})"><ellipse cx="-20" cy="6" rx="130" ry="12" fill="#000" opacity=".18"/>'
         # bidon
         '<g transform="translate(-120 0)"><path d="M-55 0 L-55 -150 Q-55 -170 -35 -172 L30 -172 L55 -150 L55 0 Z" fill="#c62828" stroke="#7f1414" stroke-width="5"/>'
         '<rect x="-30" y="-196" width="34" height="26" rx="5" fill="#212121"/>'
         '<rect x="-44" y="-120" width="88" height="62" rx="8" fill="#fff"/>'
         '<text x="0" y="-94" text-anchor="middle" font-size="19" font-weight="900" fill="#7f1414">YAZLIK</text>'
         '<text x="0" y="-68" text-anchor="middle" font-size="19" font-weight="900" fill="#7f1414">MAZOT</text></g>'
         # filtre kabı (şeffaf)
         '<g transform="translate(40 0)"><rect x="-46" y="-210" width="92" height="40" rx="8" fill="#455a64"/>'
         '<path d="M-40 -170 L-40 -20 Q-40 0 -20 0 L20 0 Q40 0 40 -20 L40 -170 Z" fill="#fff59d" fill-opacity=".55" stroke="#607d8b" stroke-width="5"/>'
         + "".join(f'<g class="mumk" data-k="{k}" opacity="0"><path d="M{-24+(k*29)%48} {-28-(k*37)%130} l6 -6 l6 6 l-6 6 Z" fill="#fff" stroke="#b0bec5" stroke-width="2"/></g>' for k in range(16)) +
         '<text x="0" y="40" text-anchor="middle" font-size="22" font-weight="800" fill="#455a64">FİLTRE</text></g></g>')
    return g


ks.PROPLAR["mum"] = p_mum


# ---------------------------------------------------------------- sahneler
def s_sdayi(p):
    A = p.get("_a", {})
    g = ks.kis_arka()
    g += f'<g transform="translate(560 1150) scale(.42)">{traktor("normal")}</g>'
    g += dv.kisi(900, 1300, .58, "genc", "duz", "normal", "kisi-usta")
    g += dv.kisi(330, 2050, 1.42, "kasketli", "bel", "endise", "kisi-dayi")
    g += ks.kar_katmani()
    g += U
    if p.get("kanca"):
        g += pop(hap(540, 196, p["kanca"], "#c62828", "#fff", 38), A.get("kanca", 12), 540, 196)
    g += '<g class="balon" data-x="540" data-y="420">' + dayi.balon(70, 250, 940, 300, p.get("balon", ["?"]), 300, 640, 52) + '</g>'
    return g, (340, 860, 1.0, 1.12)


def s_sdort(p):
    A = p.get("_a", {})
    g = zemin_krem()
    for i in range(4):
        cx, cy = 300 + (i % 2) * 480, 760 + (i // 2) * 280
        son = i == 3
        icerik = (kart(cx - 200, cy - 125, 400, 250, "#E2B654" if son else "#fff", 36)
                  + f'<text x="{cx}" y="{cy-40}" text-anchor="middle" font-size="44" font-weight="900" fill="{"#14281A" if son else "#7a6a48"}">{i+1}. SEBEP</text>'
                  + f'<text x="{cx}" y="{cy+90}" text-anchor="middle" font-size="130" font-weight="900" fill="{"#c62828" if son else "#2F5737"}">?</text>')
        g += pop(icerik, A.get(f"k{i}", 6 + i * 8), cx, cy)
    g += pop(hap(540, 1235, "Sonuncusunu çoğu kişi bilmiyor 👇", "#c62828", "#fff", 40), A.get("son", 50), 540, 1235)
    g += U + dv.baslik("4 SEBEP VAR", "#c62828") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_ssilindir(p):
    A = p.get("_a", {})
    g = zemin_krem()
    cx, top, bot = 400, 520, 1180
    # silindir gövdesi
    g += (f'<rect x="{cx-170}" y="{top}" width="340" height="{bot-top}" rx="18" fill="#eceff1" stroke="#455a64" stroke-width="10"/>'
          f'<rect class="hava" x="{cx-160}" y="{top+10}" width="320" height="400" fill="#90caf9" opacity=".55"/>'
          f'<g class="havanok"></g>'
          # enjektör
          f'<rect x="{cx-22}" y="{top-80}" width="44" height="92" rx="8" fill="#546e7a" stroke="#263238" stroke-width="5"/>'
          f'<g class="sprey" opacity="0">' + "".join(f'<path d="M{cx} {top+14} L{cx+dx} {top+90}" stroke="#ffb300" stroke-width="6" stroke-linecap="round"/>' for dx in (-46, -22, 0, 22, 46)) + '</g>'
          f'<g class="alev" opacity="0"><ellipse cx="{cx}" cy="{top+90}" rx="150" ry="80" fill="#ff7043" opacity=".85"/><ellipse cx="{cx}" cy="{top+90}" rx="95" ry="50" fill="#ffca28"/>'
          f'<text x="{cx}" y="{top+120}" text-anchor="middle" font-size="90">🔥</text></g>'
          # piston + biyel (silindir içine kırpılı)
          f'<defs><clipPath id="silklip"><rect x="{cx-165}" y="{top}" width="330" height="{bot-top-5}"/></clipPath></defs><g clip-path="url(#silklip)"><g class="piston" data-y0="{bot-140}" data-y1="{top+190}"><rect x="{cx-156}" y="0" width="312" height="130" rx="10" fill="#78909c" stroke="#37474f" stroke-width="6"/>'
          + "".join(f'<path d="M{cx-156} {14+k*16} h312" stroke="#455a64" stroke-width="5"/>' for k in range(3)) +
          f'<path d="M{cx} 130 L{cx} 600" stroke="#455a64" stroke-width="40" stroke-linecap="round"/></g></g>')
    g += ks.etk(800, 830, cx + 170, 780, "Hava sıkışır", A.get("sikis", 20), "#1565c0")
    g += ks.etk(800, 720, cx + 170, 650, "Isınır 🌡", A.get("isi", 50), "#ef6c00")
    g += pop(hap(800, 960, "Sıcak hava ateşler", "#c62828", "#fff", 38), A.get("ates", 90), 800, 960)
    g += U + dv.baslik("DİZEL NASIL ATEŞLER?", "#14281A") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_sduman(p):
    A = p.get("_a", {})
    g = ks.kis_arka() + ks.trk() + ks.p_termometre(980, 1215) + ks.kar_katmani()
    g += ks.etk(800, 800, *ks.MOTOR, "Soğuk motor", A.get("motor", 20), "#1565c0")
    g += ks.etk(800, 700, EGZOZ[0] + 10, EGZOZ[1] + 10, "Yanmayan yakıt", A.get("yanmayan", 80), "#455a64")
    g += pop(hap(540, 1235, "Beyaz duman = yanmayan yakıt", "#14281A", "#FFD54F", 40), A.get("duman", 110), 540, 1235)
    g += U + dv.baslik("BEYAZ DUMAN NEDEN?", "#455a64") + dv.pip(925, 460, 110)
    return g, (520, 980, 1.0, 1.05)


def s_skontrol(p):
    g, kam = ks.s_kkontrol(p)
    A = p.get("_a", {})
    alt, ust = g.split(U, 1)
    if p.get("hap"):
        m, _, r = p["hap"]
        alt += pop(hap(420, 610, m, r, "#fff", 40), A.get("hap", 60), 420, 610)
    ust = ust.replace(ks.no_rozet(p.get("no", 1), p.get("renk", "#1565c0")), rozet(p.get("no", 1), p.get("toplam", 4), p.get("renk", "#1565c0")))
    return alt + U + ust, kam


def gosterge(x, y):
    """Kızdırma lambası (bobin simgesi)."""
    return (f'<g transform="translate({x} {y})"><circle class="lamba" r="70" fill="#3e2723" stroke="#5d4037" stroke-width="8"/>'
            '<path class="bobin" d="M-42 0 q8 -26 16 0 q8 26 16 0 q8 -26 16 0 q8 26 16 0 q8 -26 16 0" stroke="#6d4c41" stroke-width="9" fill="none" stroke-linecap="round"/>'
            '<path d="M-52 -2 h-14 M52 -2 h14" stroke="#6d4c41" stroke-width="9" stroke-linecap="round"/></g>')


def s_skizdirma(p):
    A = p.get("_a", {})
    g = ks.kis_arka() + ks.kar_katmani()
    g += kart(110, 600, 860, 430, "#263238", 60)
    g += '<rect x="140" y="628" width="800" height="374" rx="44" fill="#37474f"/>'
    g += gosterge(360, 790)
    g += '<text x="360" y="910" text-anchor="middle" font-size="36" font-weight="900" fill="#cfd8dc">KIZDIRMA</text>'
    # kontak
    g += ('<g transform="translate(720 800)"><circle r="96" fill="#90a4ae" stroke="#cfd8dc" stroke-width="8"/><circle r="64" fill="#546e7a"/>'
          '<text x="0" y="132" text-anchor="middle" font-size="30" font-weight="900" fill="#cfd8dc">KONTAK</text>'
          '<g class="anahtar"><rect x="-14" y="-74" width="28" height="148" rx="10" fill="#ffd54f" stroke="#c79100" stroke-width="5"/><circle cy="-92" r="36" fill="#ffd54f" stroke="#c79100" stroke-width="6"/></g></g>')
    g += '<text class="marsyazi" x="720" y="985" text-anchor="middle" font-size="34" font-weight="900" fill="#546e7a">MARŞ</text>'
    g += pop(hap(540, 1110, "Lamba sönsün, sonra marş", "#2e7d32", "#fff", 42), A.get("son", 120), 540, 1110)
    g += pop('<g transform="translate(540 1212)"><rect x="-360" y="-44" width="720" height="80" rx="40" fill="#fff" stroke="#c62828" stroke-width="6"/>'
             '<text x="0" y="12" text-anchor="middle" font-size="36" font-weight="900" fill="#c62828">✕ Lamba yanarken marşa basma</text></g>', A.get("basma", 150), 540, 1212)
    g += U + rozet(2, 4, "#ef6c00") + dv.baslik("KIZDIRMA BUJİSİ", "#ef6c00") + dv.pip(925, 460, 110)
    return g, (540, 900, 1.0, 1.03)


def s_skaydet(p):
    A = p.get("_a", {})
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(120, 600, 120), (980, 1500, 210), (950, 340, 80)])
    g += ('<g class="kaydetikon" transform="translate(470 760)"><path d="M-110 -150 H110 V170 L0 90 L-110 170 Z" fill="#FFD54F" stroke="#fff" stroke-width="12" stroke-linejoin="round" filter="url(#golge)"/>'
          '<text x="0" y="30" text-anchor="middle" font-size="110">📌</text></g>')
    g += pop('<text x="470" y="1080" text-anchor="middle" font-size="84" font-weight="900" fill="#fff">Kaydet,</text>'
             '<text x="470" y="1180" text-anchor="middle" font-size="84" font-weight="900" fill="#FFD54F">lazım olur!</text>', A.get("kaydet", 8), 470, 1120)
    # sağ kenardaki kaydet düğmesine giden ok + el
    g += ('<g class="kaydetok" opacity="0"><path d="M760 1000 Q930 1060 960 1200" stroke="#FFD54F" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="4 26"/>'
          '<text x="940" y="1290" text-anchor="middle" font-size="90">👉</text></g>')
    g += U + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.03)


def s_smadde(p):
    A = p.get("_a", {})
    g = zemin_krem()
    M = p.get("maddeler", [])
    adim = 112 if len(M) <= 4 else 100
    y0 = 680 if len(M) <= 4 else 666
    for i, (e, metin, _, kind) in enumerate(M):
        y = y0 + i * adim
        t = A.get(f"m{i}", 20 + i * 30)
        fs = min(42, int(700 / max(1, len(metin) * 0.6)))
        renk = "#c62828" if kind == "x" else "#2F5737"
        icerik = (kart(70, y - 44, 940, 88, "#fff", 44) + emo(150, y + 18, e, 48)
                  + f'<text x="215" y="{y+fs*0.36:.0f}" font-size="{fs}" font-weight="900" fill="{renk}">{metin}</text>'
                  + pop(isaret(kind, 962, y, 28), t + 8, 962, y))
        g += pop(icerik, t, 540, y)
    g += U + dv.baslik(p.get("baslik", ""), p.get("renk", "#2F5737")) + dv.pip(925, 460, 110)
    return g, (540, 960, 1.0, 1.02)


def s_sates(p):
    A = p.get("_a", {})
    g = ks.kis_arka() + ks.trk() + ks.kar_katmani()
    fx, fy = ks.DEPO[0], 1185
    g += f'<g class="atesg"><text class="ates" x="{fx}" y="{fy}" text-anchor="middle" font-size="120">🔥</text></g>'
    g += pop(f'<circle cx="{fx}" cy="{fy-50}" r="118" fill="none" stroke="#e53935" stroke-width="22"/>'
             f'<path d="M{fx-84} {fy-134} L{fx+84} {fy+34}" stroke="#e53935" stroke-width="22" stroke-linecap="round"/>', A.get("sakin", 4), fx, fy - 50)
    g += pop(hap(540, 690, "Yakıtın yanında ateş = can kaybı", "#c62828", "#fff", 40), A.get("can", 40), 540, 690)
    g += pop(hap(540, 790, "Marşa uzun basma, bekle, tekrar dene", "#14281A", "#FFD54F", 38), A.get("uzun", 140), 540, 790)
    g += U + dv.baslik("SAKIN!", "#c62828") + dv.pip(925, 460, 110)
    return g, (520, 980, 1.0, 1.05)


def s_skapanis(p):
    A = p.get("_a", {})
    g = '<rect width="1080" height="1920" fill="#2F5737"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#36633f"/>' for x, y, r in [(100, 700, 120), (1000, 1500, 200), (960, 300, 70)])
    g += '<rect x="0" y="1300" width="1080" height="620" fill="#264a2e"/>'
    g += '<text x="540" y="400" text-anchor="middle" font-size="46" font-weight="900" fill="#E2B654">SABAH İLK MARŞTA ÇALIŞSIN</text>'
    for i, (e, ad) in enumerate([("🔋", "Akü"), ("🔥", "Kızdırma"), ("⛽", "Yakıt"), ("🛢️", "Yağ")]):
        x, y = 290 + (i % 2) * 500, 500 + (i // 2) * 120
        g += pop(f'<rect x="{x-215}" y="{y-46}" width="430" height="92" rx="46" fill="#fff" filter="url(#golge)"/>' + emo(x - 140, y + 18, e, 50)
                 + f'<text x="{x-90}" y="{y+16}" font-size="46" font-weight="900" fill="#2F5737">{ad}</text>', 4 + i * 5, x, y)
    g += dv.kisi(300, 1700, 1.05, "kasketli", "salla", "mutlu", "kisi-dayi")
    g += ('<g class="takip" transform="translate(600 820)"><rect class="btn" width="400" height="110" rx="55" fill="#FE2C55" filter="url(#golge)"/>'
          '<text class="btnyazi" x="200" y="74" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">+ Takip et</text><text class="el" x="230" y="200" font-size="110">👆</text></g>')
    g += '<text x="760" y="1180" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">Seri devam ediyor!</text>'
    return g, (540, 1100, 1.0, 1.03)


dv.SAHNELER.update({"sdayi": s_sdayi, "sdort": s_sdort, "ssilindir": s_ssilindir, "sduman": s_sduman, "skontrol": s_skontrol, "skizdirma": s_skizdirma,
                    "skaydet": s_skaydet, "smadde": s_smadde, "sates": s_sates, "skapanis": s_skapanis})


def _skontrol_anim(p, kt, n):
    a = ks._kontrol_anim(p, kt, n)
    if p.get("hap"):
        a["hap"] = _kt(kt, p["hap"][1], 60) - 2
    if p.get("sarj_yok"):
        a["sarj"] = 99999
    a["mum"] = _kt(kt, "mum", 40)
    return a


dv.ANIM_EK.update({
    "sdayi": lambda p, kt, n: {"kanca": 12},
    "sdort": lambda p, kt, n: {"k0": 4, "k1": 10, "k2": 16, "k3": 22, "son": _kt(kt, "sonuncusunu", 50) - 2},
    "ssilindir": lambda p, kt, n: {"sikis": _kt(kt, "sıkıştırdığı", 20) - 2, "isi": _kt(kt, "sıcaklığıyla", 50) - 2, "ates": _kt(kt, "ateşler", 90) - 2},
    "sduman": lambda p, kt, n: {"motor": _kt(kt, "motor", 20) - 2, "yanmayan": _kt(kt, "yanmayan", 80) - 2, "duman": _kt(kt, "beyaz", 110) - 2},
    "skontrol": _skontrol_anim,
    "skizdirma": lambda p, kt, n: {"kontak": _kt(kt, "kontağı", 40), "yanar": _kt(kt, "yanar", 70), "son": _kt(kt, "sönmeden", 120), "basma": _kt(kt, "basma", 150)},
    "skaydet": lambda p, kt, n: {"kaydet": _kt(kt, "kaydet", 8) - 2},
    "smadde": lambda p, kt, n: {f"m{i}": _kt(kt, m[2], 20 + i * 30) - 4 for i, m in enumerate(p.get("maddeler", []))},
    "sates": lambda p, kt, n: {"sakin": _kt(kt, "sakın", 4), "can": _kt(kt, "can", 40) - 2, "uzun": _kt(kt, "uzun", 140) - 2},
    "skapanis": lambda p, kt, n: {"tap": _kt(kt, "takip", 40)},
})

dv.JS_EK += r"""
function beyazduman(el,t,n){ const g=$('.trk .duman',el); if(!g) return; let s=''; for(let i=0;i<n;i++){ const p=((t*1.3+i*12)%72)/72;
  s+=`<circle cx="${(312-p*110).toFixed(1)}" cy="${(-575-p*260).toFixed(1)}" r="${(18+p*70).toFixed(1)}" fill="#fff" stroke="#b0bec5" stroke-width="4" opacity="${((1-p)*0.85).toFixed(2)}"/>`; } g.innerHTML=s; }
Object.assign(SAHNE,{
 sdayi(el,t){ kar(el,t); sallan(el,t); balon(el,t); poplar(el,t); const P=window.PARCALAR[+el.closest('.p').id.slice(1)]; if(P.duman!==false) beyazduman(el,t,6); },
 sdort(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 ssilindir(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); halkalar(el,t); const A=JSON.parse(el.dataset.a||'{}');
   const pi=$('.piston',el), y0=+pi.dataset.y0, y1=+pi.dataset.y1, S=A.sikis??20, F=A.ates??90; const e=ease((t-S+6)/Math.max(20,F-S)); const y=y0+(y1-y0)*e;
   pi.setAttribute('transform',`translate(0 ${y.toFixed(1)})`);
   const h=$('.hava',el); const top=530, hh=Math.max(10,y-top); h.setAttribute('height',hh.toFixed(1)); const k=Math.min(1,Math.max(0,e));
   h.setAttribute('fill',`rgb(${Math.round(144+111*k)},${Math.round(202-90*k)},${Math.round(249-200*k)})`);
   $('.sprey',el).setAttribute('opacity', t>=F-6&&t<F+10?1:0);
   const al=$('.alev',el); const ae=t>=F? Math.min(1,(t-F)/6):0; al.setAttribute('opacity',(ae*(0.85+0.15*Math.sin(t*0.9))).toFixed(2)); },
 sduman(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); halkalar(el,t); beyazduman(el,t,7);
   const m=$('.termo',el); if(m){ const e=ease(t/40), h=230-190*e; m.setAttribute('y',-60-h); m.setAttribute('height',h); } },
 skontrol(el,t){ SAHNE.kkontrol(el,t); const A=JSON.parse(el.dataset.a||'{}'); $$('.mumk',el).forEach(m=>{ const k=+m.dataset.k; m.setAttribute('opacity', t>=(A.mum??40)+k*3?1:0); }); },
 skizdirma(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), K=A.kontak??40, Y=A.yanar??70, S=(A.son??120)+12;
   $('.anahtar',el).setAttribute('transform',`rotate(${(60*ease((t-K)/10)).toFixed(1)})`);
   const on=t>=Y&&t<S; $('.lamba',el).setAttribute('fill',on?'#ff9800':'#3e2723'); $('.bobin',el).setAttribute('stroke',on?'#fff3e0':'#6d4c41');
   $('.lamba',el).setAttribute('filter',on?'url(#golge)':''); const mz=$('.marsyazi',el); mz.setAttribute('fill', t>=S?'#69f0ae':'#546e7a'); },
 skaydet(el,t){ pipf(el,t); poplar(el,t); const ik=$('.kaydetikon',el); const e=spring(t-2,0.2), b=1+0.05*Math.sin(t*0.35); ik.setAttribute('transform',`translate(470 760) scale(${(Math.min(e,1.08)*b).toFixed(3)})`);
   const ok=$('.kaydetok',el); ok.setAttribute('opacity',ease((t-24)/10)); ok.setAttribute('transform',`translate(${(Math.sin(t*0.3)*10).toFixed(1)} 0)`); },
 smadde(el,t){ pipf(el,t); bslk(el,t); poplar(el,t); },
 sates(el,t){ kar(el,t); pipf(el,t); bslk(el,t); poplar(el,t); const f=$('.ates',el); if(f){ const s=1+0.08*Math.sin(t*0.9), x=+f.getAttribute('x'), y=+f.getAttribute('y'); f.setAttribute('transform',`translate(${x} ${y}) scale(${s.toFixed(3)} ${(2-s).toFixed(3)}) translate(${-x} ${-y})`); } },
 skapanis(el,t){ sallan(el,t); poplar(el,t); const A=JSON.parse(el.dataset.a||'{}'), TP=A.tap??40, tap=t-TP, bas=tap>0&&tap<8, ya=tap>=4; const elx=$('.el',el);
   elx.setAttribute('transform',`translate(${(1-ease((t-TP+30)/22))*-160} ${(1-ease((t-TP+30)/22))*220 + (bas?-12:0)})`); elx.setAttribute('opacity', ease((t-TP+32)/6));
   $('.btn',el).setAttribute('fill', ya?'#43a047':'#FE2C55'); $('.btnyazi',el).textContent = ya?'✓ Takip edildi':'+ Takip et'; },
});
"""

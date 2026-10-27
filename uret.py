#!/usr/bin/env python3
"""Yüksel Tarım paylaşım üretim hattı.

Adımlar (CLAUDE.md'deki çalışma talimatı bunları sırayla kullanır):

  python3 uret.py taslak <kayit.json> <is_klasoru>
      Plan kaydını okur; her ürünün sayfasından ad, fiyat ve fotoğrafları çeker,
      fotoğraf seçer, <is_klasoru>/config.json ve urunler.json yazar,
      her ürün için fotoğraf kontrol sayfası (kontrol_<n>.png) üretir.

  python3 uret.py uret <is_klasoru> [--muzik dosya.mp4 --muzik-bas <sn>] [--son a,b]
  python3 uret.py muzik_sec <kayit.json> [--son a,b]   -> hangi müzik (dini mesajda müzik yok)
      config.json'a göre videoyu (format Video) ya da görseli (format Görsel) üretir.
      Çıktının yolunu yazdırır.

  python3 uret.py yukle <dosya> <hedef_ad>
      Dosyayı depoya (videolar/ ya da gorseller/) koyup gönderir, herkese açık linki yazdırır.

  python3 uret.py urun_listesi <cikti.json>
      Sitenin Ürünler sayfasındaki tüm ürünleri (ad + adres) çıkarır.
"""
import json, re, sys, html, pathlib, subprocess, urllib.request, io, shutil

REPO = pathlib.Path(__file__).resolve().parent
MOTOR = REPO / "motor"
SITE = "https://www.yukseltarimdenizli.com.tr"
RAW = "https://raw.githubusercontent.com/yukseltarimdenizli/yuksel-tarim-medya/main/"
MUZIK_BASLANGIC = 17.48  # acoustic_folk.mp3: tüm enstrümanların girdiği vuruş

MARKALAR = ["LS Tractor", "Fortis", "Alpler", "Alper", "Aydın", "İzelmak", "Paksan", "Fimaks", "Fimax", "Hisarlar",
            "Metkarsan", "Elibol", "Ser-Sed", "Ser-sed", "Sersed", "Öncel", "Kayhan Ertuğrul", "Özdöken", "Azim"]
KATEGORILER = [("traktör", "TRAKTÖR"), ("tractor", "TRAKTÖR"), ("pulluk", "PULLUK"), ("yem karma", "YEM KARMA"),
               ("römork", "RÖMORK"), ("rotovatör", "ROTOVATÖR"), ("rotavatör", "ROTAVATÖR"), ("çizel", "ÇİZEL"),
               ("goble", "GOBLE"), ("diskaro", "DİSKARO"), ("mibzer", "MİBZER"), ("balya", "BALYA"), ("silaj", "SİLAJ"),
               ("tırmık", "TIRMIK"), ("çapa", "ÇAPA"), ("tanker", "TANKER"), ("gübre", "GÜBRE DAĞITMA"), ("parçalama", "PARÇALAMA")]
KICKER = {"Kampanya": "KAMPANYA", "Ürün tanıtımı": "YÜKSEL TARIM'DA", "Firma tanıtımı": "YÜKSEL TARIM · DENİZLİ",
          "Usta ipucu": "USTA İPUCU", "Teslimat / müşteri": "TESLİMAT", "Özel gün": "YÜKSEL TARIM"}
VURGU = {"kampanya", "dev", "indirim", "fırsat", "yeni", "güç", "güçlü", "özel"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (YukselTarim medya botu)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


# ---------------------------------------------------------------- ürün bilgisi
def urun_bilgisi(url):
    page = get(url)
    m = re.search(r'<meta property="og:title" content="([^"]+)"', page) or re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    ad = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else url.rsplit("/", 1)[-1]
    ad = re.sub(r"\s*[-|–]\s*Yüksel Tarım.*$", "", ad, flags=re.I).strip()
    fiyat = None
    m = re.search(r'"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)', page)
    if m:
        fiyat = int(float(m.group(1)))
    # galeri sırasıyla, ilk görüldüğü yere göre
    yollar = []
    for mm in re.finditer(r"(?:%2F|/)api(?:%2F|/)uploads(?:%2F|/)products(?:%2F|/)(\d+)(?:%2F|/)(\d+)\.webp", page):
        y = f"/api/uploads/products/{mm.group(1)}/{mm.group(2)}.webp"
        if y not in yollar:
            yollar.append(y)
    ikinci_el = bool(re.search(r'itemCondition"\s*:\s*"[^"]*Used', page)) or "İkinci El" in page[:60000]
    return {"url": url, "ad": ad, "fiyat": fiyat, "ikinci_el": ikinci_el, "fotograflar": [SITE + y for y in yollar]}


def foto_puani(w, h, sira):
    r = w / h
    if r > 2.0 or r < 0.55 or (w == h and w <= 900):  # afiş/banner/tanıtım kartı
        return -99
    p = 3 if 1.2 <= r <= 1.85 else (1 if r > 1 else 0)
    return p - sira * 0.15  # galerideki ilk fotoğraflar genelde ana fotoğraf


def beyaz_kirp(im):
    """Fotoğrafın kenarındaki düz beyaz şeritleri (dolgu) kırp."""
    import numpy as np
    a = np.asarray(im).min(axis=2)
    cols = np.where((a < 238).mean(axis=0) > 0.02)[0]; rows = np.where((a < 238).mean(axis=1) > 0.02)[0]
    if len(cols) < 50 or len(rows) < 50:
        return im
    box = (int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1)
    return im.crop(box) if (box[2] - box[0]) * (box[3] - box[1]) < 0.97 * im.width * im.height else im


def foto_indir(info, klasor, n, en_fazla=10):
    from PIL import Image, ImageFilter, ImageDraw
    adaylar = []
    for i, u in enumerate(info["fotograflar"][:en_fazla]):
        try:
            im = beyaz_kirp(Image.open(io.BytesIO(get(u, binary=True))).convert("RGB"))
        except Exception:
            continue
        adaylar.append({"sira": i, "url": u, "w": im.width, "h": im.height, "puan": foto_puani(im.width, im.height, i), "im": im})
    if not adaylar:
        return None, []
    # kontrol sayfası: CLAUDE.md'ye göre çalışan oturum bakıp gerekirse seçimi değiştirir
    tw, th, cols = 300, 230, 5
    rows = (len(adaylar) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white"); d = ImageDraw.Draw(sheet)
    for k, a in enumerate(adaylar):
        t = a["im"].copy(); t.thumbnail((tw - 6, th - 30)); x, y = (k % cols) * tw, (k // cols) * th
        sheet.paste(t, (x + 3, y + 3)); d.text((x + 6, y + th - 22), f"#{a['sira']}  {a['w']}x{a['h']}  puan {a['puan']:.1f}", fill="black")
    sheet.save(klasor / f"kontrol_{n}.png")
    for a in adaylar:  # hepsini kaydet ki seçim değiştirilebilsin
        im = a["im"].resize((a["w"] * 2, a["h"] * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
        im.save(klasor / f"urun{n}_foto{a['sira']}.jpg", quality=93)
    en_iyi = max(adaylar, key=lambda a: a["puan"])
    return str(klasor / f"urun{n}_foto{en_iyi['sira']}.jpg"), [a["sira"] for a in adaylar]


def odeme_secenekleri(ikinci_el):
    """Firma kuralı: sıfırda 5 yıl kredi + kredi kartı, 2. elde sadece kredi kartı; her üründe takas."""
    return (["Kredi kartına taksit"] if ikinci_el else ["5 yıl kredi", "Kredi kartına taksit"]) + ["Takas imkânı"]


def kisa_ad(ad):
    s = ad
    for b in MARKALAR:
        s = re.sub(re.escape(b), "", s, flags=re.I)
    s = re.sub(r"\b(Sıfır|Marka|Yapımı|Denizli|Yüksel Tarım'?[a-zıüşçöğ]*|Model)\b", "", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip(" -–'")
    return s or ad


def etiketler(ad):
    pats = [r"\d+\s?'?(?:li|lı|lü|lu)\b", r"\d+\s?(?:No|Numara)\b", r"\d+(?:[.,]\d+)?\s?HP", r"\d+\s?(?:m3|m³)", r"4x4",
            r"\bDönerli\b", r"\bKabinli\b", r"\bKabinsiz\b", r"\bKantarlı\b", r"\bDikey\b", r"\bYatay\b", r"\bHidrolik\b", r"\bDamperli\b"]
    out = []
    for p in pats:
        m = re.search(p, ad, re.I)
        if m and m.group(0) not in out:
            out.append(m.group(0).replace("Numara", "No"))
    return out[:3]


def etiket_ust(ad):
    marka = next((b for b in MARKALAR if b.lower() in ad.lower()), "")
    kat = next((k for key, k in KATEGORILER if key in ad.lower()), "")
    return " · ".join(x for x in [marka.upper().replace("İ", "İ"), kat] if x) or "YÜKSEL TARIM"


def baslik_vurgula(t):
    out, done = [], False
    for w in t.split():
        if not done and w.lower().strip(".,!") in VURGU:
            out.append(f"[{w}]"); done = True
        else:
            out.append(w)
    return " ".join(out)


def taslak(kayit_yolu, klasor):
    kayit = json.loads(pathlib.Path(kayit_yolu).read_text())
    klasor = pathlib.Path(klasor); klasor.mkdir(parents=True, exist_ok=True)
    urunler = kayit.get("products") or ([{"name": kayit["product"], "url": kayit.get("productUrl", "")}] if kayit.get("product") else [])
    bilgiler = []
    for n, u in enumerate(urunler):
        b = {"plan_adi": u["name"], "url": u.get("url", ""), "ad": u["name"], "fiyat": None, "foto": None, "adaylar": [], "hata": None}
        if u.get("url"):
            try:
                inf = urun_bilgisi(u["url"]); b.update(ad=inf["ad"], fiyat=inf["fiyat"], ikinci_el=inf["ikinci_el"])
                b["foto"], b["adaylar"] = foto_indir(inf, klasor, n)
            except Exception as e:
                b["hata"] = f"ürün sayfası okunamadı: {e}"
        else:
            b["hata"] = "sitede eşleşen ürün yok"
        bilgiler.append(b)
    (klasor / "urunler.json").write_text(json.dumps(bilgiler, ensure_ascii=False, indent=1))

    title = kayit.get("title") or (bilgiler[0]["plan_adi"] if bilgiler else "Yüksel Tarım")
    cfg = {"format": "Video", "kayit_id": kayit.get("id"), "scenes": []}  # kullanıcı tercihi: hep video
    tur = kayit.get("type")
    satirlar = [re.sub(r"^\s*(\d+[).]|[-•*])\s*", "", x).strip() for x in re.split(r"\n|(?<=\.)\s+(?=\d+\))", kayit.get("note", "")) if x.strip()]
    if cfg["format"] == "Video" and tur == "Özel gün":
        cfg["scenes"] = [{"type": "intro", "overlap": 24},
                         {"type": "greeting", "kicker": "YÜKSEL TARIM", "title": baslik_vurgula(title), "sub": ""},
                         {"type": "outro", "cta": ""}]
    elif cfg["format"] == "Video" and tur in ("Usta ipucu", "Firma tanıtımı"):
        cfg["scenes"] = [{"type": "intro", "overlap": 24},
                         {"type": "list", "kicker": "USTA İPUCU" if tur == "Usta ipucu" else "YÜKSEL TARIM · DENİZLİ", "title": title, "items": satirlar[:4]}]
        for n, b in enumerate(bilgiler):
            if b["foto"]:
                ad = kisa_ad(b["plan_adi"])
                cfg["scenes"].append({"type": "photo", "wipe": True, "label": etiket_ust(b["plan_adi"]), "name": ad,
                                      "name_fs": 130 if len(ad) <= 12 else max(64, int(130 * 12 / len(ad))), "image": b["foto"],
                                      "frame_h": 620, "kb": [20, 0, 1.04, -30, -10, 1.18], "desc": "Yüksel Tarım güvencesiyle.",
                                      "chips": (["2. El"] if b.get("ikinci_el") else ["Sıfır"]) + etiketler(b["plan_adi"])[:2],
                                      "perks": odeme_secenekleri(b.get("ikinci_el")), "dur": 110})
        cfg["scenes"].append({"type": "outro", "cta": "Bilgi için hemen arayın"})
    elif cfg["format"] == "Video":
        cfg["scenes"].append({"type": "intro", "overlap": 24})
        cfg["scenes"].append({"type": "headline", "kicker": KICKER.get(kayit.get("type"), "YÜKSEL TARIM"),
                              "title": baslik_vurgula(title), "sub": "" if any(b["fiyat"] for b in bilgiler) else kayit.get("note", "")[:140]})
        for b in bilgiler:
            if not b["foto"]:
                continue
            ad = kisa_ad(b["plan_adi"])
            sc = {"type": "photo", "wipe": True, "label": etiket_ust(b["plan_adi"]), "name": ad,
                  "name_fs": 130 if len(ad) <= 12 else max(64, int(130 * 12 / len(ad))), "image": b["foto"], "frame_h": 620,
                  "kb": [20, 0, 1.04, -30, -10, 1.18], "desc": "Yüksel Tarım güvencesiyle.", "chips": (["2. El"] if b.get("ikinci_el") else ["Sıfır"]) + etiketler(b["plan_adi"])[:2], "dur": 115}
            sc["perks"] = odeme_secenekleri(b.get("ikinci_el"))
            if b["fiyat"]:
                sc["price"] = b["fiyat"]; sc["dur"] = 120
                sc["price_label"] = "KAMPANYA FİYATI" if kayit.get("type") == "Kampanya" else "FİYAT"
            cfg["scenes"].append(sc)
        cfg["scenes"].append({"type": "outro", "cta": "Kampanya için hemen arayın" if kayit.get("type") == "Kampanya" else "Bilgi için hemen arayın"})
    else:  # Görsel
        madde = [f'{kisa_ad(b["plan_adi"])}' + (f' – {b["fiyat"]:,} TL'.replace(",", ".") if b["fiyat"] else "") for b in bilgiler]
        cfg["gorsel"] = {"slug": "gorsel", "kicker": KICKER.get(kayit.get("type"), "YÜKSEL TARIM"), "title": baslik_vurgula(title),
                         "body": "" if bilgiler else kayit.get("note", ""), "bullets": madde[:5],
                         "photo": next((b["foto"] for b in bilgiler if b["foto"]), None)}
    cfg["kapak"] = kapak_taslagi(kayit, title, bilgiler, cfg)
    (klasor / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    print(json.dumps({"config": str(klasor / "config.json"), "urunler": bilgiler}, ensure_ascii=False, indent=1))


KAPAK_UST = {"Kampanya": "KAMPANYA", "Ürün tanıtımı": "YÜKSEL TARIM'DA", "Firma tanıtımı": "YÜKSEL TARIM",
             "Usta ipucu": "USTA İPUCU", "Teslimat / müşteri": "TESLİMAT", "Özel gün": ""}


def kapak_taslagi(kayit, title, bilgiler, cfg):
    """Kapak (videonun ilk yarım saniyesi) için varsayılan ayarlar. Çalışan oturum `baslik`ı 2-4 kelimelik
    vurucu bir kapak yazısına çevirir; kullanıcı plan sayfasında `kapakYazisi`/`kapak` verdiyse onlar geçerli."""
    tur = kayit.get("type")
    secim = (kayit.get("kapak") or "Otomatik").strip()
    yazi = (kayit.get("kapakYazisi") or "").strip()
    if tur == "Özel gün":
        sablon = secim if secim in list("ABCDE") else "auto"
        return {"tur": "kutlama", "sablon": sablon, "ust": "", "baslik": yazi or title, "alt": "", "buyuk": ""}
    fiyatli = tur not in ("Usta ipucu", "Firma tanıtımı")
    sahne_foto = [sc for sc in cfg.get("scenes", []) if sc.get("type") == "photo"]
    urunler = []
    for b in bilgiler:
        if not b.get("foto"):
            continue
        sc = next((x for x in sahne_foto if x.get("image") == b["foto"]), {})
        urunler.append({"ad": sc.get("name") or kisa_ad(b["plan_adi"]), "foto": b["foto"],
                        "fiyat": b.get("fiyat") if fiyatli else None, "ikinci_el": bool(b.get("ikinci_el")),
                        "fiyat_etiket": "BAŞLAYAN FİYATLARLA" if "hububat" in b["plan_adi"].lower() else ""})
    sablon = secim if secim in list("12345") else "auto"
    return {"tur": "urun", "sablon": sablon, "ust": KAPAK_UST.get(tur, ""), "baslik": yazi or baslik_vurgula(title),
            "urunler": urunler, "rozetler": fiyatli and bool(urunler)}


def kapak_hazirla(klasor, cfg, son=()):
    """config'teki kapağı üretir; sablon 'auto' ise tekrar etmeyecek şekilde seçer. Kapak PNG yolunu döner."""
    sys.path.insert(0, str(MOTOR)); import kapak as K
    kp = cfg.get("kapak")
    if not kp:
        return None
    if kp.get("sablon", "auto") == "auto":
        if kp.get("tur") == "kutlama":
            kp["sablon"] = K.kutlama_sablonu_oner(kp.get("baslik", "") + " " + kp.get("ust", "") + " " + kp.get("alt", ""), son)
        else:
            kp["sablon"] = K.urun_sablonu_sec(len(kp.get("urunler", [])), son)
    yol = pathlib.Path(klasor) / "kapak.png"
    K.kapak_uret(kp, yol)
    (pathlib.Path(klasor) / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    print("KAPAK_SABLONU", kp["sablon"], file=sys.stderr)
    return yol


KAPAK_SURE = 0.5  # sn — kullanıcı kararı

# ---------------------------------------------------------------- müzik seçimi
MUZIKLER = json.loads((pathlib.Path(__file__).parent / "muzikler.json").read_text())
DINI = ["cuma", "kandil", "ramazan", "kurban", "şeker bayram", "hicri", "mevlid", "mevlit", "kadir gece", "regaip",
        "miraç", "mirac", "berat", "aşure", "asure", "arefe", "iftar", "sahur", "oruç", "hac ", "mübarek", "mubarek", "bayram"]
MILLI = ["cumhuriyet", "29 ekim", "23 nisan", "19 mayıs", "19 mayis", "30 ağustos", "zafer bayram", "15 temmuz",
         "atatürk", "ataturk", "10 kasım", "milli", "çiftçi", "ciftci", "yılbaşı", "yeni yıl", "öğretmen", "anneler", "babalar"]


def dini_mi(kayit):
    """Kullanıcı kararı: Cuma ve dini günlerin mesajlarında müzik kullanılmaz."""
    if kayit.get("type") != "Özel gün":
        return False
    m = " ".join(str(kayit.get(a, "")) for a in ("title", "note", "kapakYazisi")).lower().replace("İ", "i")
    if any(w in m for w in MILLI) and not any(w in m for w in ("cuma", "kandil", "ramazan", "kurban", "mübarek")):
        return False
    return any(w in m for w in DINI)


def muzik_sec(kayit, son=()):
    """{anahtar, asset, baslangic, kredi} ya da {anahtar: None, neden}."""
    P = MUZIKLER["parcalar"]; secim = (kayit.get("muzik") or "Otomatik").strip()
    if dini_mi(kayit):
        return {"anahtar": None, "neden": "dini mesaj: müzik kullanılmaz"}
    if secim == "Müziksiz":
        return {"anahtar": None, "neden": "kullanıcı müziksiz istedi"}
    if secim in P:
        a = secim
    else:
        aday = MUZIKLER["turlere_gore"].get(kayit.get("type"), list(P))
        son = [x for x in son if x]
        uygun = [x for x in aday if x not in son[-2:]] or aday
        # en uzun süredir kullanılmayanı seç (hiç kullanılmamışlar önce, listedeki sıraya göre)
        uygun.sort(key=lambda x: (son[::-1].index(x) if x in son else -1), reverse=True)
        uygun.sort(key=lambda x: x in son)
        a = uygun[0]
    return {"anahtar": a, **P[a]}


def uret(klasor, muzik=None, son=(), muzik_bas=None):
    klasor = pathlib.Path(klasor); cfg = json.loads((klasor / "config.json").read_text())
    # Güvence: satış koşulu rozetleri (kredi/kart/takas) ürün sahnelerinden asla düşmesin.
    ikinci = {}
    if (klasor / "urunler.json").exists():
        for b in json.loads((klasor / "urunler.json").read_text()):
            if b.get("foto"):
                ikinci[pathlib.Path(b["foto"]).name.split("_foto")[0]] = b.get("ikinci_el", False)
    eklendi = False
    for sc in cfg.get("scenes", []):
        if sc.get("type") == "photo" and not sc.get("perks") and not sc.get("perks_yok"):
            anahtar = pathlib.Path(sc.get("image", "")).name.split("_foto")[0]
            sc["perks"] = odeme_secenekleri(ikinci.get(anahtar, "2. El" in sc.get("chips", [])))
            eklendi = True
    if eklendi:
        (klasor / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
        print("UYARI: perks eksikti, otomatik eklendi", file=sys.stderr)
    if cfg["format"] == "Video":
        govde = klasor / "video_govde.mp4"
        subprocess.run([sys.executable, str(MOTOR / "motion2.py"), str(klasor / "config.json"), str(govde)], check=True)
        sessiz = klasor / "video_sessiz.mp4"
        kp = kapak_hazirla(klasor, cfg, son)
        if kp:  # ilk yarım saniye kapak, sonra video
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-t", str(KAPAK_SURE), "-i", str(kp), "-i", str(govde),
                            "-filter_complex", "[0:v]scale=1080:1920,setsar=1,format=yuv420p[k];[1:v]scale=1080:1920,setsar=1,format=yuv420p[g];[k][g]concat=n=2:v=1:a=0[v]",
                            "-map", "[v]", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(sessiz)], check=True)
        else:
            shutil.copy(govde, sessiz)
        out = klasor / "video.mp4"
        if muzik:
            dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(sessiz)]).decode())
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(sessiz), "-ss", str(MUZIK_BASLANGIC if muzik_bas is None else muzik_bas), "-i", muzik, "-filter_complex",
                            f"[1:a]atrim=0:{dur},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.25,afade=t=out:st={dur-1.8:.2f}:d=1.8[a]",
                            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", str(out)], check=True)
        else:
            shutil.copy(sessiz, out)
    else:
        g = dict(cfg["gorsel"]); (klasor / "gorsel.json").write_text(json.dumps(g, ensure_ascii=False))
        subprocess.run([sys.executable, str(MOTOR / "render.py"), str(klasor / "gorsel.json"), str(klasor)], check=True)
        out = klasor / "gorsel_fb.png"
    print(out)


def yukle(dosya, hedef_ad):
    dosya = pathlib.Path(dosya)
    alt = "videolar" if dosya.suffix == ".mp4" else "gorseller"
    hedef = REPO / alt / hedef_ad; hedef.parent.mkdir(exist_ok=True); shutil.copy(dosya, hedef)
    rel = f"{alt}/{hedef_ad}"
    g = lambda *a: subprocess.run(["git", "-C", str(REPO), *a], check=True, capture_output=True, text=True)
    g("pull", "-q", "--rebase", "origin", "main")
    g("add", rel)
    g("-c", "user.name=Yüksel Tarım", "-c", "user.email=noreply@yukseltarimdenizli.com.tr", "commit", "-q", "-m",
      f"{hedef_ad} eklendi\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
    g("push", "-q", "origin", "main")
    print(RAW + rel)


def tr_baslik(s):
    def w(x):
        if not x or x[0].isdigit() or x.isupper() and len(x) > 1:
            return x
        f = {"i": "İ", "ı": "I"}.get(x[0], x[0].upper())
        return f + x[1:]
    s = " ".join(x.upper() if re.match(r"^[A-Za-z]{1,3}\d", x) else w(x) for x in s.split())
    s = re.sub(r"\b(Xu|Xj|Xr|Mt)\b", lambda m: m.group(1).upper(), s)
    return re.sub(r"\bLs\b", "LS", re.sub(r"\bHp\b", "HP", s))


def foto(url, klasor, ad):
    """Herhangi bir site fotoğrafını indirip videoya hazırlar (firma tanıtımı vb.)."""
    from PIL import Image, ImageFilter
    im = beyaz_kirp(Image.open(io.BytesIO(get(url, binary=True))).convert("RGB"))
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    out = pathlib.Path(klasor) / ad; im.save(out, quality=93); print(out)


def urun_listesi(cikti):
    page = get(SITE + "/urunler")
    out, seen = [], set()
    for m in re.finditer(r'href="/urunler/([a-z0-9\-]+)"[^>]*>(.*?)</a>', page, re.S):
        slug = m.group(1)
        if slug in seen:
            continue
        txt = html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
        txt = re.sub(r"\s+", " ", txt).strip()
        txt = re.sub(r"\s*(arrow_forward|Ürünü İncele).*$", "", txt, flags=re.I)
        parcalar = re.split(r"₺|Fiyat İçin Arayın", txt, maxsplit=1)
        ad = parcalar[1] if len(parcalar) > 1 else txt
        ad = re.split(r"\s*(?:Tipi|Türü)\s*:", ad)[0].strip(" .")
        ad = re.sub(r"\s+(den|dan|'den|'dan)$", "", ad, flags=re.I)
        ad = re.sub(r"\s*i̇?kinci el\b", "", ad, flags=re.I).strip()
        ad = re.split(r"\.\s*(?:yüksel|denizli)", ad, flags=re.I)[0]
        ad = re.sub(r"\s*(yüksel tarım\S*|denizli\S*)\s*", " ", ad, flags=re.I).strip(" .-")
        if len(ad) < 4:
            continue
        fiyat = re.search(r"([\d.]+)\s*₺", txt)
        seen.add(slug)
        out.append({"name": tr_baslik(ad)[:90], "slug": slug, "ikinci_el": "2. El" in txt or "İkinci El" in txt,
                    "fiyat": int(fiyat.group(1).replace(".", "")) if fiyat else None})
    pathlib.Path(cikti).write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(len(out), "ürün")


if __name__ == "__main__":
    k = sys.argv[1]
    if k == "taslak": taslak(sys.argv[2], sys.argv[3])
    elif k == "uret": uret(sys.argv[2], sys.argv[sys.argv.index("--muzik") + 1] if "--muzik" in sys.argv else None,
                           [x for x in (sys.argv[sys.argv.index("--son") + 1].split(",") if "--son" in sys.argv else []) if x],
                           float(sys.argv[sys.argv.index("--muzik-bas") + 1]) if "--muzik-bas" in sys.argv else None)
    elif k == "muzik_sec":
        son = [x for x in (sys.argv[sys.argv.index("--son") + 1].split(",") if "--son" in sys.argv else []) if x]
        print(json.dumps(muzik_sec(json.loads(pathlib.Path(sys.argv[2]).read_text()), son), ensure_ascii=False))
    elif k == "yukle": yukle(sys.argv[2], sys.argv[3])
    elif k == "urun_listesi": urun_listesi(sys.argv[2])
    elif k == "foto": foto(sys.argv[2], sys.argv[3], sys.argv[4])
    else: print(__doc__)

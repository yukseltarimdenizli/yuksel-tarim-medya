"""Yüksel Tarım video kapakları (1080x1920 PNG).

Videonun ilk yarım saniyesi bu kapak olur; TikTok/YouTube/Facebook ilk kareyi kapak alır.
Yazılar TikTok profil ızgarasının (3:4, y 240-1680) ve Facebook 4:5 kırpmasının (y 285-1635) içinde kalır.

Ürün şablonları (1-5): 1 tam fotoğraf · 2 yeşil çerçeve · 3 krem dergi · 4 afiş · 5 sade yazı
Kutlama şablonları (A-E): A yeşil halka · B kırmızı (milli bayram) · C gece mavisi (kandil) · D krem kurdele (bayram) · E buğday (çiftçi)

Kullanım: python3 kapak.py <kapak.json> <cikti.png>
kapak.json:
  {"tur": "urun", "sablon": "1".."5", "ust": "STOKLARLA SINIRLI", "baslik": "Alpler 5'li [Dönerli]",
   "urunler": [{"ad": "5'li 14 No", "foto": "/yol/foto.jpg", "fiyat": 218000, "fiyat_etiket": "", "ikinci_el": false}],
   "rozetler": true}
  {"tur": "kutlama", "sablon": "A".."E", "ust": "29 EKİM", "baslik": "Cumhuriyetimizin 103. yılı kutlu olsun",
   "buyuk": "103.", "alt": "29 Ekim Cumhuriyet Bayramı"}
`baslik` içinde [kelime] altın renkle vurgulanır.
"""
import base64, html, json, pathlib, random, re, sys

ROOT = pathlib.Path(__file__).parent
URUN_SABLONLARI = ["1", "2", "3", "4", "5"]
KUTLAMA_SABLONLARI = ["A", "B", "C", "D", "E", "F", "G"]


def _u(p):
    p = pathlib.Path(p)
    mt = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mt};base64," + base64.b64encode(p.read_bytes()).decode()


def _e(s):
    return html.escape(str(s or ""))


def _vurgu(s, renk="#D4A445"):
    return re.sub(r"\[([^\]]+)\]", rf'<em style="font-style:normal;color:{renk}">\1</em>', _e(s))


def _ust(s):
    """Türkçe büyük harf (i→İ, ı→I)."""
    return (s or "").replace("i", "İ").replace("ı", "I").upper()


def _fiyat(n):
    return f"{int(n):,}".replace(",", ".")


def _bin(n):
    n = int(n)
    return f"{n // 1000} BİN" if n % 1000 == 0 and n >= 10000 else _fiyat(n)


def _fs(metin, taban, genislik_karakter):
    """Başlık uzunluğuna göre yazı boyutu: en uzun kelime satıra sığsın."""
    temiz = re.sub(r"[\[\]]", "", metin or "")
    en_uzun = max((len(w) for w in temiz.split()), default=6)
    return int(min(taban, taban * genislik_karakter / max(en_uzun, 1)))


BASE = ("*{margin:0;padding:0;box-sizing:border-box} body{width:1080px;height:1920px;overflow:hidden;"
        "font-family:Poppins,sans-serif;position:relative} .a{position:absolute} .c{left:0;right:0;text-align:center}")


def _logo(L, renk="#fff", w=120, top=300, left=60, orta=False, kutu=False):
    pos = "left:0;right:0;justify-content:center" if orta else f"left:{left}px"
    if kutu:  # parlak fotoğraf üstünde okunsun diye koyu zemin
        pos += ";background:rgba(13,26,16,.85);padding:12px 30px 12px 16px;border-radius:22px"
    return (f'<div class="a" style="{pos};top:{top}px;display:flex;align-items:center;gap:18px;color:{renk}">'
            f'<img src="{L}" style="width:{w}px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35))"><div style="line-height:1.05">'
            f'<div style="font-size:{int(w * .36)}px;font-weight:800;letter-spacing:2px">YÜKSEL TARIM</div>'
            f'<div style="font-size:{int(w * .24)}px;font-weight:700;letter-spacing:{int(w * .09)}px;color:#D4A445">DENİZLİ</div></div></div>')


def _rozet_metni(urunler):
    if not urunler:
        return ""
    if all(u.get("ikinci_el") for u in urunler):
        return "Kredi kartına taksit · Takas"
    if any(u.get("ikinci_el") for u in urunler):
        return "Sıfırda 5 yıl kredi · Karta taksit · Takas"
    return "5 yıl kredi · Kredi kartına taksit · Takas"


def _fiyat_satiri(u):
    if not u.get("fiyat"):
        return ""
    return _fiyat(u["fiyat"])


# --------------------------------------------------------------------------- ürün şablonları
def urun_html(k, L):
    s = k["sablon"]; ust = _e(k.get("ust", "")); bas = k.get("baslik", ""); U = k.get("urunler", [])[:3]
    roz = _rozet_metni(U) if k.get("rozetler", True) else ""
    n = len(U)
    f = [_u(x["foto"]) if x.get("foto") else "" for x in U]
    # tek ürünün fiyat etiketi (BAŞLAYAN FİYATLARLA gibi)
    etiket = (U[0].get("fiyat_etiket") or "") if n == 1 else ""

    if s == "1":
        if n <= 1:
            fy = f"<div class='a' style='left:60px;top:1290px;color:#fff;font-size:92px;font-weight:800'>{_fiyat_satiri(U[0])} <span style='font-size:46px'>TL</span></div>" if n and U[0].get("fiyat") else ""
            et = f"<div class='a' style='left:60px;top:1255px;color:#D4A445;font-size:30px;font-weight:800;letter-spacing:2px'>{_e(etiket)}</div>" if etiket and fy else ""
            bg = f"<div class='a' style='inset:0;background:url({f[0]}) center/cover'></div>" if n else "<div class='a' style='inset:0;background:#2F5737'></div>"
            return (f"{bg}<div class='a' style='inset:0;background:linear-gradient(180deg,rgba(10,20,12,.6) 0%,rgba(10,20,12,0) 26%,rgba(10,20,12,0) 42%,rgba(10,20,12,.95) 70%,#0d1a10)'></div>"
                    f"{_logo(L, w=130)}" + (f"<div class='a' style='left:60px;top:960px;background:#D4A445;color:#14281A;font-weight:800;font-size:32px;padding:8px 24px;border-radius:12px'>{ust}</div>" if ust else "")
                    + f"<div class='a' style='left:60px;right:60px;top:1030px;color:#fff;font-size:{_fs(bas, 116, 13)}px;font-weight:800;line-height:1;letter-spacing:-2px'>{_vurgu(bas)}</div>"
                    + et + fy + (f"<div class='a' style='left:60px;right:60px;top:1420px;color:#F5F0E3;font-size:30px;font-weight:700'>{roz}</div>" if roz else ""))
        # iki/üç ürün: ekran yatay bölünür
        h = 1920 // n; parcalar = ""
        for i in range(n):
            parcalar += f"<div class='a' style='left:0;right:0;top:{i * h}px;height:{h}px;background:url({f[i]}) center/cover'></div>"
        etiketler = ""
        konumlar = [(660, "left"), (1070, "right"), (1300, "left")] if n == 2 else [(470, "left"), (900, "right"), (1250, "left")]
        for i, x in enumerate(U):
            y, yan = konumlar[i]
            etiketler += (f"<div class='a' style='{yan}:60px;top:{y}px;background:rgba(13,26,16,.88);color:#fff;border-radius:20px;padding:12px 24px;text-align:{yan}'>"
                          f"<div style='font-size:32px;font-weight:700'>{_e(x.get('ad', ''))}</div>"
                          + (f"<div style='font-size:60px;font-weight:800;color:#D4A445;line-height:1'>{_fiyat(x['fiyat'])} TL</div>" if x.get("fiyat") else "") + "</div>")
        return (parcalar + "<div class='a' style='inset:0;background:linear-gradient(180deg,rgba(10,20,12,.65) 0%,rgba(10,20,12,.1) 25%,rgba(10,20,12,.1) 75%,rgba(10,20,12,.85) 100%)'></div>"
                f"{_logo(L, w=110, kutu=True)}<div class='a c' style='top:{(h if n == 2 else h) - 80}px'><span style='background:#14281A;color:#fff;font-size:{_fs(bas, 64, 24)}px;font-weight:800;padding:10px 34px;border-radius:18px;border:5px solid #D4A445'>{_vurgu(bas)}</span></div>"
                + etiketler + (f"<div class='a c' style='top:1420px'><span style='background:rgba(13,26,16,.88);color:#F5F0E3;font-size:30px;font-weight:700;padding:12px 30px;border-radius:16px'>{roz}</span></div>" if roz else ""))

    if s == "2":
        G = "<style>body{background:radial-gradient(ellipse at 50% 35%,#2F5737,#14281A 70%)}</style>"
        tt = f"<div class='a' style='left:50px;right:50px;top:460px;text-align:center;color:#fff;font-size:{_fs(bas, 98, 15)}px;font-weight:800;line-height:1.02'>{_vurgu(bas)}</div>"
        alt = f"<div class='a c' style='top:1450px;color:rgba(255,255,255,.9);font-size:32px;font-weight:600'>{roz}</div>" if roz else ""
        if n <= 1:
            foto = f"<div class='a' style='left:70px;right:70px;top:730px;height:520px;border-radius:34px;background:url({f[0]}) center/cover;outline:6px solid #D4A445;outline-offset:-6px;box-shadow:0 30px 70px rgba(0,0,0,.55)'></div>" if n else ""
            fy = ""
            if n and U[0].get("fiyat"):
                fy = (f"<div class='a' style='left:50%;top:1200px;transform:translateX(-50%) rotate(-3deg);background:#D4A445;color:#14281A;border-radius:24px;padding:14px 40px;text-align:center;white-space:nowrap'>"
                      f"<div style='font-size:28px;font-weight:800'>{_e(etiket or ust)}</div><div style='font-size:88px;font-weight:800;line-height:1'>{_fiyat(U[0]['fiyat'])} <span style='font-size:42px'>TL</span></div></div>")
            return G + _logo(L, w=120, orta=True, top=290) + tt + foto + fy + alt
        h = 330 if n == 2 else 230; out = ""
        for i, x in enumerate(U):
            y = 680 + i * (h + 60)
            out += f"<div class='a' style='left:70px;right:70px;top:{y}px;height:{h}px;border-radius:28px;background:url({f[i]}) center/cover;outline:5px solid #D4A445;outline-offset:-5px;box-shadow:0 20px 50px rgba(0,0,0,.5)'></div>"
            if x.get("fiyat"):
                yan, rot = ("left", -3) if i % 2 == 0 else ("right", 3)
                out += (f"<div class='a' style='{yan}:40px;top:{y + h - 100}px;background:#D4A445;color:#14281A;border-radius:18px;padding:8px 24px;transform:rotate({rot}deg);white-space:nowrap'>"
                        f"<span style='font-size:30px;font-weight:800'>{_e(x.get('ad', ''))}</span> <span style='font-size:56px;font-weight:800'>{_fiyat(x['fiyat'])} TL</span></div>")
        return G + _logo(L, w=120, orta=True, top=290) + tt + out + alt

    if s == "3":
        G = "<style>body{background:#F5F0E3}</style>" + f"<img class='a' src='{L}' style='right:-220px;top:200px;width:820px;opacity:.06'>"
        hd = (_logo(L, renk="#2F5737", w=120) + (f"<div class='a' style='left:64px;top:450px;color:#D4A445;font-weight:800;font-size:34px;letter-spacing:8px'>{ust}</div>" if ust else "")
              + f"<div class='a' style='left:64px;right:64px;top:500px;color:#2F5737;font-size:{_fs(bas, 140, 10)}px;font-weight:800;line-height:.95;letter-spacing:-3px'>{_vurgu(_ust(bas), '#B8862A')}</div>")
        alt = f"<div class='a' style='left:64px;top:1440px;color:#2F5737;font-size:32px;font-weight:700'>{roz}</div>" if roz else ""
        if n <= 1:
            foto = f"<div class='a' style='left:64px;right:64px;top:820px;height:560px;background:url({f[0]}) center/cover;clip-path:polygon(0 0,100% 0,100% 82%,86% 100%,0 100%)'></div>" if n else ""
            dm = ""
            if n and U[0].get("fiyat"):
                dm = (f"<div class='a' style='right:60px;top:1200px;width:280px;height:280px;border-radius:50%;background:#2F5737;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-12deg);border:8px solid #D4A445'>"
                      + (f"<span style='font-size:22px;font-weight:800;color:#D4A445'>{_e(etiket.split()[0] if etiket else '')}</span>" if etiket else "")
                      + f"<b style='font-size:64px;line-height:1'>{_bin(U[0]['fiyat'])}</b><span style='font-size:28px;font-weight:700;color:#D4A445'>TL</span></div>")
            return G + hd + foto + dm + alt
        out = ""; w = 470 if n == 2 else 320
        poz = [(50, 850, -4), (560, 900, 4)] if n == 2 else [(30, 860, -5), (380, 900, 2), (730, 850, 5)]
        for i, x in enumerate(U):
            xx, yy, r = poz[i]
            out += (f"<div class='a' style='left:{xx}px;top:{yy}px;width:{w}px;padding:14px 14px 70px;background:#fff;box-shadow:0 18px 40px rgba(20,40,26,.25);transform:rotate({r}deg)'>"
                    f"<div style='height:{int(w * .85)}px;background:url({f[i]}) center/cover'></div>"
                    f"<div style='position:absolute;left:0;right:0;bottom:12px;text-align:center;color:#2F5737;font-size:{36 if n == 2 else 28}px;font-weight:800'>{_e(x.get('ad', ''))}"
                    + (f" · <span style='color:#B8862A'>{_bin(x['fiyat'])}</span>" if x.get("fiyat") else "") + "</div></div>")
        return G + hd + out + alt

    if s == "4":
        G = "<style>body{background:#D4A445}</style>"
        if n <= 1:
            foto = f"<div class='a' style='left:0;right:0;top:0;height:1040px;background:url({f[0]}) center/cover'></div>" if n else "<div class='a' style='left:0;right:0;top:0;height:1040px;background:#2F5737'></div>"
        else:
            w = 1080 // n
            foto = "".join(f"<div class='a' style='left:{i * w}px;width:{w}px;top:0;height:1000px;background:url({f[i]}) center/cover;border-left:{8 if i else 0}px solid #D4A445'></div>" for i in range(n))
        foto += "<div class='a' style='left:0;right:0;top:760px;height:280px;background:linear-gradient(transparent,#D4A445)'></div>"
        lg = "<div class='a' style='left:50px;top:290px;width:540px;height:150px;background:rgba(20,40,26,.92);border-radius:22px'></div>" + _logo(L, w=110, left=74, top=310)
        tt = f"<div class='a' style='left:60px;right:60px;top:980px;color:#14281A;font-size:{_fs(bas, 124, 11)}px;font-weight:900;line-height:.95;letter-spacing:-3px'>{_vurgu(_ust(bas), '#F5F0E3')}</div>"
        if n <= 1:
            fy = (f"<div class='a' style='left:60px;top:1250px;color:#14281A;font-size:96px;font-weight:900'>{_fiyat(U[0]['fiyat'])} <span style='font-size:44px'>TL</span>"
                  + (f" <span style='font-size:30px;font-weight:700'>{_e(etiket.replace('I','ı').replace('İ','i').lower())}</span>" if etiket else "") + "</div>") if n and U[0].get("fiyat") else ""
        else:
            fy = ("<div class='a' style='left:60px;right:60px;top:1220px;display:flex;gap:16px'>"
                  + "".join(f"<div style='flex:1;background:#14281A;color:#fff;border-radius:18px;padding:12px 18px'><div style='font-size:28px;font-weight:700;color:#D4A445'>{_e(x.get('ad', ''))}</div>"
                            + (f"<div style='font-size:{60 if n == 2 else 44}px;font-weight:900;line-height:1'>{_fiyat(x['fiyat'])} TL</div>" if x.get("fiyat") else "") + "</div>" for x in U) + "</div>")
        alt = f"<div class='a' style='left:60px;right:60px;top:1420px;background:#14281A;color:#F5F0E3;font-size:30px;font-weight:700;padding:14px;border-radius:14px;text-align:center'>{_ust(roz)}</div>" if roz else ""
        return G + foto + lg + tt + fy + alt

    # s == "5"
    G = ("<style>body{background:#14281A;color:#fff}</style><div class='a' style='inset:0;background:repeating-linear-gradient(115deg,rgba(212,164,69,.05) 0 2px,transparent 2px 60px)'></div>"
         f"<div class='a c' style='top:290px'><img src='{L}' style='width:190px'></div>"
         f"<div class='a' style='left:40px;right:40px;top:520px;text-align:center;font-size:{_fs(bas, 150, 8)}px;font-weight:900;line-height:.92;letter-spacing:-4px'>{_vurgu(_ust(bas))}</div>")
    alt = f"<div class='a c' style='top:1440px;font-size:30px;font-weight:600;color:rgba(255,255,255,.85)'>{roz}</div>" if roz else ""
    if n == 0:  # ürünsüz (firma tanıtımı vb.): yazı ortada, altında alt yazı + web adresi
        G = G.replace("top:290px'><img src='" + L + "' style='width:190px'", "top:330px'><img src='" + L + "' style='width:230px'").replace("top:520px;text-align:center", "top:640px;text-align:center")
        a2 = f"<div class='a c' style='top:1120px;font-size:44px;font-weight:600;color:#F5F0E3;padding:0 80px'>{_vurgu(k['alt'])}</div>" if k.get("alt") else ""
        web = "<div class='a c' style='top:1300px'><span style='border:3px solid #D4A445;color:#D4A445;font-size:34px;font-weight:700;padding:14px 34px;border-radius:40px'>www.yukseltarimdenizli.com.tr</span></div>"
        return G + a2 + web
    if n <= 1:
        foto = f"<div class='a' style='left:60px;right:60px;top:860px;height:420px;border-radius:26px;background:url({f[0]}) center/cover;border:6px solid #D4A445'></div>" if n else ""
        fy = (f"<div class='a c' style='top:1320px;font-size:40px;font-weight:600'>{_e(U[0].get('ad', ''))} <b style='color:#D4A445;font-size:64px'>{_fiyat(U[0]['fiyat'])} TL</b></div>") if n and U[0].get("fiyat") else ""
        return G + foto + fy + alt
    kutu = ("<div class='a' style='left:60px;right:60px;top:870px;height:400px;display:flex;gap:20px'>"
            + "".join(f"<div style='flex:1;display:flex;flex-direction:column;gap:12px'><div style='flex:1;border-radius:24px;background:url({f[i]}) center/cover;border:5px solid #D4A445'></div>"
                      f"<div style='text-align:center;font-size:28px;font-weight:700'>{_e(x.get('ad', ''))}"
                      + (f"<b style='color:#D4A445;font-size:{42 if n == 2 else 32}px;display:block;line-height:1.05'>{_fiyat(x['fiyat'])} TL</b>" if x.get("fiyat") else "") + "</div></div>" for i, x in enumerate(U))
            + "</div>")
    return G + kutu + alt


# --------------------------------------------------------------------------- kutlama şablonları
def kutlama_html(k, L):
    s = k["sablon"]; ust = _e(k.get("ust", "")); bas = k.get("baslik", ""); alt = _e(k.get("alt", "")); buyuk = _e(k.get("buyuk", ""))
    marka = lambda renk="#fff", acc="#D4A445", top=1380: f"<div class='a c' style='top:{top}px;color:{renk};font-size:40px;font-weight:800;letter-spacing:6px'>YÜKSEL TARIM <span style='color:{acc}'>DENİZLİ</span></div>"
    if s == "A":
        return ("<style>body{background:radial-gradient(ellipse at 50% 38%,#3a6b45,#14281A 68%)}</style>"
                "<div class='a' style='left:50%;top:330px;width:620px;height:620px;margin-left:-310px;border-radius:50%;background:radial-gradient(circle,#F5F0E3 0 60%,rgba(245,240,227,.25) 61%,rgba(245,240,227,0) 72%)'></div>"
                f"<img class='a' src='{L}' style='left:50%;top:420px;width:400px;margin-left:-200px'>"
                + (f"<div class='a c' style='top:975px;color:#D4A445;font-size:34px;font-weight:700;letter-spacing:10px'>{ust}</div>" if ust else "")
                + f"<div class='a c' style='left:40px;right:40px;top:1030px;color:#fff;font-size:{_fs(bas, 120, 11)}px;font-weight:800;line-height:1.02'>{_vurgu(bas)}</div>" + marka(top=1400))
    if s == "B":
        return ("<style>body{background:linear-gradient(160deg,#C8102E,#7A0A18)}</style>"
                "<div class='a' style='left:0;right:0;top:300px;height:14px;background:#fff;opacity:.9'></div><div class='a' style='left:0;right:0;top:1500px;height:14px;background:#fff;opacity:.9'></div>"
                f"<div class='a' style='left:50%;top:380px;width:400px;height:400px;margin-left:-200px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 60px rgba(0,0,0,.35)'><img src='{L}' style='width:290px'></div>"
                + (f"<div class='a c' style='top:820px;color:#fff;font-size:250px;font-weight:900;line-height:1;letter-spacing:-6px'>{buyuk}</div>"
                   f"<div class='a c' style='left:40px;right:40px;top:1080px;color:#fff;font-size:{_fs(bas, 76, 18)}px;font-weight:800;line-height:1.05'>{_vurgu(bas, '#FFD9A0')}</div>"
                   if buyuk else f"<div class='a c' style='left:40px;right:40px;top:860px;color:#fff;font-size:{_fs(bas, 110, 12)}px;font-weight:800;line-height:1.05'>{_vurgu(bas, '#FFD9A0')}</div>")
                + (f"<div class='a c' style='top:1290px;color:#FFD9A0;font-size:36px;font-weight:600;letter-spacing:4px'>{alt.upper()}</div>" if alt else "") + marka(acc="#FFD9A0", top=1400))
    if s == "C":
        yildiz = "".join(f"<div class='a' style='left:{(i * 137) % 1040 + 20}px;top:{(i * 263) % 1500 + 260}px;width:{4 + i % 5}px;height:{4 + i % 5}px;border-radius:50%;background:#F3D58A;opacity:{.3 + (i % 4) * .15}'></div>" for i in range(60))
        return ("<style>body{background:radial-gradient(ellipse at 50% 30%,#1d3157,#0a1428 70%)}</style>" + yildiz
                + "<div class='a' style='left:640px;top:320px;width:220px;height:220px;border-radius:50%;box-shadow:-40px 20px 0 0 #F3D58A'></div>"
                f"<div class='a' style='left:50%;top:560px;width:430px;height:430px;margin-left:-215px;border-radius:50%;border:6px solid #D4A445;background:#F5F0E3;display:flex;align-items:center;justify-content:center'><img src='{L}' style='width:310px'></div>"
                + (f"<div class='a c' style='top:1060px;color:#F3D58A;font-size:42px;font-weight:600;letter-spacing:10px'>{ust}</div>" if ust else "")
                + f"<div class='a c' style='left:40px;right:40px;top:1130px;color:#fff;font-size:{_fs(bas, 106, 14)}px;font-weight:800;line-height:1.02'>{_vurgu(bas, '#F3D58A')}</div>" + marka(acc="#F3D58A", top=1400))
    if s == "D":
        return ("<style>body{background:#F5F0E3}</style>"
                f"<img class='a' src='{L}' style='left:-260px;top:420px;width:1600px;opacity:.05'><img class='a' src='{L}' style='left:50%;top:330px;width:500px;margin-left:-250px;filter:drop-shadow(0 18px 30px rgba(47,87,55,.25))'>"
                f"<div class='a' style='left:-40px;right:-40px;top:1000px;height:200px;background:#D4A445;transform:rotate(-4deg);display:flex;align-items:center;justify-content:center;color:#14281A;font-size:{_fs(bas, 108, 14)}px;font-weight:900;letter-spacing:-2px;box-shadow:0 14px 30px rgba(0,0,0,.15);white-space:nowrap'>{_ust(_e(re.sub(r'[\[\]]', '', bas)))}</div>"
                + (f"<div class='a c' style='top:1250px;color:#2F5737;font-size:40px;font-weight:600'>{alt}</div>" if alt else "") + marka(renk="#2F5737", top=1380))
    if s == "G":  # gece göğü: lacivert-yeşil gök, yıldızlar, parlayan hilal, alt yarıda dev altın cami (kullanıcı seçimi, dini günler)
        from cami import cami_svg
        yildiz = "".join(f"<div class='a' style='left:{(i * 137) % 1040 + 20}px;top:{(i * 263) % 900 + 150}px;width:{3 + i % 4}px;height:{3 + i % 4}px;border-radius:50%;background:#F5D58A;opacity:{.25 + (i % 4) * .12}'></div>" for i in range(90))
        return ("<style>body{background:linear-gradient(180deg,#0a1428 0%,#14281A 75%)}</style>" + yildiz
                + "<div class='a' style='left:690px;top:250px;width:260px;height:260px;border-radius:50%;box-shadow:-46px 24px 0 0 #F5D58A;filter:drop-shadow(0 0 30px rgba(245,213,138,.5))'></div>"
                + f"<img class='a' src='{L}' style='left:64px;top:300px;width:110px'>"
                + (f"<div class='a c' style='top:560px;color:#F5D58A;font-size:34px;font-weight:700;letter-spacing:10px'>{ust}</div>" if ust else "")
                + f"<div class='a c' style='left:40px;right:40px;top:610px;color:#fff;font-size:{_fs(bas, 100, 13)}px;font-weight:800;line-height:1.05'>{_vurgu(bas, '#F5D58A')}</div>"
                + "<div class='a' style='left:50%;top:745px;width:420px;height:6px;margin-left:-210px;background:#D4A445;border-radius:6px'></div>"
                + (f"<div class='a c' style='left:60px;right:60px;top:775px;color:rgba(255,255,255,.9);font-size:38px'>{alt}</div>" if alt else "")
                + "<div class='a' style='left:-60px;top:1010px;width:1200px'>" + cami_svg(1080, 520).replace('width="1080" height="520"', 'width="1200" height="578"', 1) + "</div>"
                + "<div class='a' style='left:0;right:0;bottom:0;height:150px;background:rgba(20,40,26,.92);border-top:6px solid #D4A445;display:flex;align-items:center;justify-content:center;color:#fff;font-size:38px;font-weight:600'>www.yukseltarimdenizli.com.tr</div>")
    if s == "F":  # cami silüeti (Cuma, kandil, dini bayram)
        from cami import cami_svg
        yildiz = "".join(f"<div class='a' style='left:{(i * 137) % 1040 + 20}px;top:{(i * 263) % 640 + 260}px;width:{3 + i % 4}px;height:{3 + i % 4}px;border-radius:50%;background:#F5D58A;opacity:{.25 + (i % 4) * .12}'></div>" for i in range(40))
        return ("<style>body{background:radial-gradient(ellipse at 50% 30%,#2F5737,#0f2014 72%)}</style>" + yildiz
                + "<svg class='a' viewBox='0 0 100 100' style='right:110px;top:300px;width:150px'><defs><mask id='hm'><rect width='100' height='100' fill='white'/><circle cx='62' cy='42' r='36' fill='black'/></mask></defs><circle cx='48' cy='50' r='40' fill='#F5D58A' mask='url(#hm)'/></svg>"
                f"<div class='a' style='left:50%;top:280px;width:300px;height:300px;margin-left:-150px;border-radius:50%;background:#F5F0E3;border:6px solid #D4A445;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 18px rgba(212,164,69,.18)'><img src='{L}' style='width:215px'></div>"
                + (f"<div class='a c' style='top:625px;color:#F5D58A;font-size:34px;font-weight:700;letter-spacing:10px'>{ust}</div>" if ust else "")
                + f"<div class='a c' style='left:40px;right:40px;top:675px;color:#fff;font-size:{_fs(bas, 112, 12)}px;font-weight:800;line-height:1.02'>{_vurgu(bas, '#F5D58A')}</div>"
                + (f"<div class='a c' style='top:870px;color:rgba(255,255,255,.88);font-size:34px;font-weight:600'>{alt}</div>" if alt else "")
                + f"<div class='a' style='left:0;right:0;top:940px'>{cami_svg(1080, 540)}</div>")
    # E
    bugday = "".join(f"<div class='a' style='left:{(i * 173) % 1100 - 40}px;top:{(i * 311) % 1700 + 150}px;width:8px;height:{90 + i % 4 * 30}px;background:#D4A445;opacity:.10;transform:rotate({(i % 7) * 8 - 24}deg);border-radius:6px'></div>" for i in range(80))
    return ("<style>body{background:linear-gradient(180deg,#2F5737,#14281A)}</style>" + bugday
            + f"<img class='a' src='{L}' style='left:70px;top:320px;width:440px'><div class='a' style='left:70px;top:860px;width:180px;height:10px;background:#D4A445;border-radius:6px'></div>"
            f"<div class='a' style='left:70px;right:70px;top:900px;color:#fff;font-size:{_fs(bas, 104, 12)}px;font-weight:800;line-height:1.02'>{_vurgu(bas)}</div>"
            + (f"<div class='a' style='left:70px;top:1270px;color:rgba(255,255,255,.85);font-size:34px;font-weight:600;letter-spacing:4px'>{alt.upper()}</div>" if alt else "")
            + "<div class='a' style='left:70px;top:1380px;color:#fff;font-size:40px;font-weight:800;letter-spacing:6px'>YÜKSEL TARIM <span style='color:#D4A445'>DENİZLİ</span></div>")


# --------------------------------------------------------------------------- seçim
def kutlama_sablonu_oner(metin, son_kullanilanlar=()):
    t = (metin or "").lower()
    if any(x in t for x in ["29 ekim", "cumhuriyet", "23 nisan", "19 mayıs", "30 ağustos", "zafer", "15 temmuz", "milli"]):
        return "B"
    if "kandil" in t:
        return "C"
    if "bayram" in t:
        return "D"
    if "çiftçi" in t:
        return "E"
    aday = [x for x in ["A", "D", "E"] if x not in list(son_kullanilanlar)[-1:]]  # Cuma vb.: A/D/E dönüşümlü
    return random.choice(aday or ["A"])


def urun_sablonu_sec(urun_sayisi, son_kullanilanlar=()):
    uygun = URUN_SABLONLARI[:] if urun_sayisi <= 2 else ["3", "4", "5"]  # 3+ ürün: 1 ve 2 kalabalıklaşıyor
    son = list(son_kullanilanlar)
    for geri in (3, 2, 1, 0):
        aday = [s for s in uygun if s not in son[-geri:]] if geri else uygun
        if aday:
            return random.choice(aday)


# --------------------------------------------------------------------------- referans (mutlu müşteri) kapağı
def referans_html(k, L):
    """{"tur":"referans","foto":..., "ad":"Yılmaz Aksoy","konum":"Antalya / Serik","urun":"Alpler 3'lü Dönerli Pulluk","ust":"MUTLU MÜŞTERİMİZ"}"""
    f = _u(k["foto"]); ad = _e(k.get("ad", "")); fs = 104 if len(k.get("ad", "")) <= 16 else (84 if len(k.get("ad", "")) <= 22 else 66)
    return (f"<div class='a' style='inset:0;background:url({f}) {k.get('pos', 'center')}/cover'></div>"
            "<div class='a' style='inset:0;background:linear-gradient(180deg,rgba(10,20,12,.55) 0%,rgba(10,20,12,0) 24%,rgba(10,20,12,0) 46%,rgba(10,20,12,.92) 68%,#0d1a10)'></div>"
            + _logo(L, w=120, kutu=True)
            + f"<div class='a' style='left:60px;top:960px;background:#D4A445;color:#14281A;font-weight:800;font-size:34px;padding:10px 28px;border-radius:14px;letter-spacing:1px'>{_e(k.get('ust', 'MUTLU MÜŞTERİMİZ'))}</div>"
            + "<div class='a' style='left:60px;top:1050px;color:#D4A445;font-size:58px;letter-spacing:8px'>★★★★★</div>"
            + f"<div class='a' style='left:60px;right:60px;top:1150px;color:#fff;font-size:{fs}px;font-weight:800;line-height:1.02;letter-spacing:-1px'>{ad}</div>"
            + f"<div class='a' style='left:60px;right:60px;top:{1150 + fs + 30}px;color:#F5F0E3;font-size:38px;font-weight:600'>📍 {_e(k.get('konum', ''))}</div>"
            + (f"<div class='a' style='left:60px;right:60px;top:{1150 + fs + 90}px;color:rgba(245,240,227,.8);font-size:32px;font-weight:500'>{_e(k['urun'])}</div>" if k.get("urun") else ""))


def kapak_uret(k, cikti):
    from playwright.sync_api import sync_playwright
    L = _u(ROOT / "assets/logo.png")
    tur = k.get("tur", "urun")
    govde = urun_html(k, L) if tur == "urun" else (referans_html(k, L) if tur == "referans" else kutlama_html(k, L))
    doc = f"<html><head><meta charset='utf-8'><style>{BASE}</style></head><body>{govde}</body></html>"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(doc); pg.wait_for_timeout(400); pg.screenshot(path=str(cikti)); b.close()
    return cikti


if __name__ == "__main__":
    print(kapak_uret(json.loads(pathlib.Path(sys.argv[1]).read_text()), sys.argv[2]))

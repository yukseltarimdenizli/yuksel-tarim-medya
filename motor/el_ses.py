#!/usr/bin/env python3
"""ElevenLabs API ile seslendirme (Dayı Soruyor). API anahtarı KODDA YOK:
claude.ai/code "Default" ortamındaki ağ gizli anahtarı (api.elevenlabs.io, başlık xi-api-key)
istekleri proxy üzerinden kendisi ekler. Bu betik yalnız o ortamda çalışan oturumlarda işe yarar.

Kullanım:
  python3 motor/el_ses.py <prompt.txt> <dayi|usta> <cikti_klasoru> [--model eleven_v4_turbo]
Çıktı: <klasor>/<karakter>.mp3, <karakter>_zaman.json (karakter hizalaması), <karakter>_bilgi.json (model, karakter sayısı, maliyet başlıkları)
Kelime zamanları: kelime_zamanlari(<..._zaman.json>) → [(kelime, başlangıç, bitiş)], [etiket] parçaları ayrı öğe olarak döner.
"""
import base64, json, os, re, sys, urllib.request

SESLER = {"dayi": "mF7tIc9VLrznhGooGjaT",   # Seyfullah Kartal – Deep and Muffled (Hasan Dayı)
          "usta": "7VqWGAWwo2HMrylfKrcm"}   # Fatih Yıldırım – Deep, Clear and Rich (Ahmet Usta)
AYAR = {"stability": 0.5, "similarity_boost": 0.75}


def uret(metin, karakter, klasor, model="eleven_v4_turbo"):
    os.makedirs(klasor, exist_ok=True)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{SESLER[karakter]}/with-timestamps?output_format=mp3_44100_128"
    govde = json.dumps({"text": metin, "model_id": model, "voice_settings": AYAR}).encode()
    istek = urllib.request.Request(url, data=govde, headers={"Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(istek, timeout=300) as y:
            veri = json.loads(y.read()); bas = dict(y.headers)
    except urllib.error.HTTPError as e:
        print("HATA", e.code, e.read()[:600].decode(errors="replace")); sys.exit(1)
    open(f"{klasor}/{karakter}.mp3", "wb").write(base64.b64decode(veri["audio_base64"]))
    json.dump(veri.get("normalized_alignment") or veri.get("alignment"), open(f"{klasor}/{karakter}_zaman.json", "w"), ensure_ascii=False)
    bilgi = {"model": model, "karakter": len(metin), "basliklar": {k: v for k, v in bas.items() if any(s in k.lower() for s in ("character", "cost", "request-id", "credit"))}}
    json.dump(bilgi, open(f"{klasor}/{karakter}_bilgi.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(bilgi, ensure_ascii=False))


def kelime_zamanlari(yol):
    a = json.load(open(yol)); ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    out, buf, s0, e0 = [], "", None, None
    def bitir():
        nonlocal buf, s0, e0
        if buf.strip(): out.append((buf.strip(), s0, e0))
        buf, s0, e0 = "", None, None
    i = 0
    while i < len(ch):
        c = ch[i]
        if c == "[":
            bitir(); j = i
            while j < len(ch) and ch[j] != "]": j += 1
            out.append(("".join(ch[i:j + 1]), st[i], en[min(j, len(ch) - 1)])); i = j + 1; continue
        if c.isspace():
            bitir()
        else:
            if s0 is None: s0 = st[i]
            buf += c; e0 = en[i]
        i += 1
    bitir()
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    model = "eleven_v4_turbo"
    if "--model" in a:
        k = a.index("--model"); model = a[k + 1]; del a[k:k + 2]
    metin = open(a[0]).read().strip()
    uret(metin, a[1], a[2], model)

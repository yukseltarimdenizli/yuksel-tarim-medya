"""Seslendirme parçalarında kelime zamanlarını sesten bulur (karaoke altyazı senkronu için).
Yöntem: parçanın sesi ince duraklamalarla (silencedetect -36 dB, 0,06 sn) konuşma öbeklerine bölünür; kelimeler (hece sayılarıyla)
öbeklere dinamik programlamayla dağıtılır: hece hızı konuşmacının ortalamasına yakın olmalı, öbek sınırları noktalamaya denk gelmeli.
Kelimesiz öbek (gülme/iç çekme gibi ses etiketleri) başta/sonda ucuz, ortada pahalıdır. Öbeğin önünde etiket varsa ve öbek yavaşsa
kelimeler öbeğin sonuna yaslanır (iç çekmenin üstüne kelime yazılmaz).
Kullanım: hizala.parcalara_uygula(sen, wav_listesi, etiketler={parça: [kelime_indeksi, ...]}) → p["kelime_t"] yazılır.
"""
import re, subprocess

SESLI = "aeıioöuüAEIİOÖUÜâî"


def hece(w):
    return max(1, sum(1 for c in w if c in SESLI))


def obekler(wav, sure, esik="-36dB", d=0.06):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=noise={esik}:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = list(zip(st, en + [sure] * (len(st) - len(en))))
    ch, t = [], 0.0
    for a, b in sil:
        if a > t + 0.04:
            ch.append((t, a))
        t = max(t, b)
    if t < sure - 0.04:
        ch.append((t, sure))
    # 0,16 sn'den kısa kırıntıları (patlamalı ünsüz, nefes) en yakın komşuya kat
    ch = [list(c) for c in ch]
    while True:
        kis = [i for i, (a, b) in enumerate(ch) if b - a < 0.16 and len(ch) > 1]
        if not kis:
            break
        i = kis[0]
        sol = ch[i][0] - ch[i - 1][1] if i > 0 else 9
        sag = ch[i + 1][0] - ch[i][1] if i < len(ch) - 1 else 9
        if sol <= sag:
            ch[i - 1][1] = ch[i][1]
        else:
            ch[i + 1][0] = ch[i][0]
        del ch[i]
    return [tuple(c) for c in ch]


def kelime_zamanlari(metin, ch, r0, etiket=()):
    ws = metin.split()
    H = [hece(w) for w in ws]
    n, m = len(ws), len(ch)
    son_nok = [bool(re.search(r"[,.!?:;]$", w)) for w in ws]
    INF = float("inf")
    sonra = [ch[j + 1][0] - ch[j][1] for j in range(m - 1)] + [0.0]
    dp = [[INF] * (n + 1) for _ in range(m + 1)]
    gr = [[None] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0.0
    for j in range(1, m + 1):
        a, b = ch[j - 1]; dur = max(0.05, b - a)
        for k in range(n + 1):
            if dp[j - 1][k] < INF:  # boş öbek (yalnız etiket sesi: gülme, iç çekme)
                c = dp[j - 1][k] + (0.3 if k in etiket else 3.0 + dur * dur * 4)
                if c < dp[j][k]:
                    dp[j][k], gr[j][k] = c, k
            for k0 in range(k):
                if dp[j - 1][k0] == INF:
                    continue
                syl = sum(H[k0:k])
                etk = k0 in etiket
                ef = dur if not etk else min(dur, syl / r0 * 1.15)
                err = ef - syl / r0
                c = dp[j - 1][k0] + err * err * 4
                if k < n and not son_nok[k - 1]:
                    c += 0.3 + 3 * sonra[j - 1]          # noktalamasız yerde uzun duraklama olmaz
                for q in range(k0, k - 1):               # öbek içinde cümle sonu (duraksız) olmaz
                    if re.search(r"[.!?:;]$", ws[q]):
                        c += 1.5
                    elif ws[q].endswith(","):
                        c += 0.2
                if c < dp[j][k]:
                    dp[j][k], gr[j][k] = c, k0
    # geri izle
    k = n; atama = []
    for j in range(m, 0, -1):
        k0 = gr[j][k]; atama.append((j - 1, k0, k)); k = k0
    atama.reverse()
    t = [None] * n
    for ji, k0, k1 in atama:
        if k1 == k0:
            continue
        a, b = ch[ji]; syl = sum(H[k0:k1])
        if k0 in etiket and (b - a) > syl / r0 * 1.15:
            a = b - syl / r0 * 1.15
        c = 0
        for q in range(k0, k1):
            t[q] = round(a + (b - a) * c / syl, 3); c += H[q]
    return t, dp[m][n]


def parcalara_uygula(sen, wavlar, etiketler=None):
    etiketler = etiketler or {}
    P = sen["parcalar"]
    obs = [obekler(w, p["sure"]) for w, p in zip(wavlar, P)]
    r = {}
    for kim in ("dayi", "usta"):
        s = sum(sum(hece(w) for w in p["metin"].split()) for p in P if p.get("konusan") == kim)
        d = sum(sum(b - a for a, b in o) for o, p in zip(obs, P) if p.get("konusan") == kim)
        r[kim] = s / d if d else 5.5
    rapor = []
    for i, (p, o) in enumerate(zip(P, obs)):
        t, cost = kelime_zamanlari(p["metin"], o, r.get(p.get("konusan"), 5.5), set(etiketler.get(i, [])))
        p["kelime_t"] = t
        p["konusma"] = [[round(a, 3), round(b, 3)] for a, b in o]
        rapor.append((i, round(cost, 2), list(zip(p["metin"].split(), t))))
    return r, rapor

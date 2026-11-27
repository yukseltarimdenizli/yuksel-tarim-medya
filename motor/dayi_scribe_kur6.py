import json, subprocess, array, math, re
W='/tmp/is/dayi6'; S=f'{W}/ses'
LD=["Ahmet Usta, kışlık danalara yemi kürekle karıştırıyorum ama sabah yemliğe bakıyorum, hep saman kalmış! Bunlar benden de seçici çıktı. [laughs]",
"[sighs] Ben de diyordum, bu kadar saman nereye gidiyor!",
"Desene, hayvanlar da sofrada seçiciymiş, tıpkı benim torunlar gibi! [laughs] Sizin hayvanlarınız yemlikte neyi bırakıyor? Yorumlara yazın. Serinin devamı için takip etmeyi unutmayın."]
LU=["Dayı, hayvanların yem seçiyor. Elle karıştırınca bu olur. Yem karmayla farkını üç adımda anlatayım, sonuncusunu çoğu kişi bilmiyor.",
"Önce sorun. Kürekle karıştırınca saman, silaj ve kesif yem tam karışmaz. Hayvan sevdiği kesif yemi seçip yer, samanı bırakır.",
"Bir hayvan fazla kesif yem yer, işkembesi bozulabilir. Öteki aç kalır. Yemliğin dibinde kalan saman da boşa gider.",
"Birinci fark: Yem karma samanı ve kaba yemi doğrar, kesif yemle birlikte karıştırır. Her lokmada aynı yem olur, hayvan seçemez.",
"İkinci fark: Yem israfı azalır, sürü düzenli beslenir. Kürekle saatlerce uğraşmazsın.",
"Bu videoyu kaydet dayı, kışın lazım olur.",
"Üçüncü fark, çoğu kişinin bilmediği: Makine yanlış kullanılırsa fayda etmez. Önce kuru ot ve samanı koy, ıslak yemi en sona bırak.",
"Çok uzun da karıştırma. Saman fazla incelirse işkembe iyi çalışmaz. Süre için makinenin kılavuzuna bak, rasyonu da bir veteriner hekim ya da zooteknistle hazırla."]
def grupla(ws, satirlar):
    out=[]; i=0
    for s in satirlar:
        n=len(s.split()); g=ws[i:i+n]
        for a,b in zip(g, s.split()):
            assert a['text']==b, (a['text'],b)
        out.append(g); i+=n
    assert i==len(ws); return out
def enerji(f):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    a=array.array('h',raw); hop=160  # 10ms
    e=[]
    for i in range(0,len(a)-hop,hop):
        seg=a[i:i+hop]; r=math.sqrt(sum(x*x for x in seg)/hop)
        e.append(20*math.log10(max(r,1)/32768))
    return e
def kesimler(gr, f):
    E=enerji(f); seg=[[g[0]['start'], g[-1]['end']] for g in gr]; rap=[]
    for k in range(len(seg)-1):
        e0=seg[k][1]-0.06; s1=seg[k+1][0]+0.02
        i0=max(0,int(e0*100)); i1=max(i0+1,int(s1*100))
        # en sessiz 40 ms pencere
        best=None
        for i in range(i0, i1-3):
            m=max(E[i:i+4])
            if best is None or m<best[0]-0.5: best=(m,i)
        if best is None: best=(E[i0],i0)
        cut=(best[1]+2)/100
        rap.append((k, round(cut,3), round(best[0],1)))
        seg[k][1]=cut; seg[k+1][0]=cut
    seg[0][0]=max(0,seg[0][0]-0.05)
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    seg[-1][1]=min(dur, seg[-1][1]+0.25)
    return seg, rap
gd=grupla(json.load(open(f'{S}/scribe_dayi.json'))['words'],LD)
gu=grupla(json.load(open(f'{S}/scribe_usta.json'))['words'],LU)
sd,rd=kesimler(gd,f'{S}/dayi.mp3'); su,ru=kesimler(gu,f'{S}/usta.mp3')
print('kesim dayi',rd); print('kesim usta',ru)
P=[
 dict(sahne='ydayi',konusan='dayi',balon=["Yemlikte hep","[saman] kalıyor! 🤔"],kanca="3 fark · sonuncusu sürpriz 👇"),
 dict(sahne='y3',konusan='usta'),
 dict(sahne='smadde',konusan='usta',baslik='ELLE KARIŞTIRINCA',renk='#c62828',maddeler=[["✋","Kürekle tam karışmaz","kürekle","x"],["🌾","Saman, silaj, kesif yem ayrı","saman","x"],["🐄","Hayvan kesif yemi seçer","hayvan","x"],["🍂","Samanı bırakır","samanı","x"]]),
 dict(sahne='smadde',konusan='usta',baslik='SONUÇ',renk='#c62828',maddeler=[["⚠️","Fazla kesif yiyen: işkembe bozulur","işkembesi","uyari"],["😟","Öteki aç kalır","öteki","x"],["🗑️","Dipte kalan saman boşa gider","yemliğin","x"]]),
 dict(sahne='ktepki',konusan='dayi',balon=["Bu kadar [saman]","nereye gidiyor! 😅"]),
 dict(sahne='ykarma',konusan='usta'),
 dict(sahne='smadde',konusan='usta',baslik='2. FARK',renk='#2F5737',maddeler=[["💰","Yem israfı azalır","israfı","ok"],["🐄","Sürü düzenli beslenir","sürü","ok"],["⏱️","Kürekle saatler bitti","kürekle","ok"]]),
 dict(sahne='skaydet',konusan='usta'),
 dict(sahne='smadde',konusan='usta',baslik='3. FARK: SIRA',renk='#b8860b',maddeler=[["❗","Yanlış kullanım fayda etmez","makine","uyari"],["1️⃣","Önce kuru ot ve saman","önce","ok"],["2️⃣","Islak yem en sona","ıslak","ok"]]),
 dict(sahne='smadde',konusan='usta',baslik='DİKKAT',renk='#c62828',maddeler=[["⏳","Çok uzun karıştırma","uzun","uyari"],["🌾","Saman fazla incelmesin","saman","uyari"],["📘","Süre: makinenin kılavuzu","kılavuzuna","ok"],["🩺","Rasyon: veteriner / zooteknist","rasyonu","ok"]]),
 dict(sahne='ykapanis',konusan='dayi'),
]
sira={'dayi':0,'usta':0}; dosyalar=[]
for i,p in enumerate(P):
    k=p['konusan']; j=sira[k]; sira[k]+=1
    a,b=(sd if k=='dayi' else su)[j]; g=(gd if k=='dayi' else gu)[j]; satir=(LD if k=='dayi' else LU)[j]
    on=.25 if i==0 else .15
    son={"ktepki":.5,"ykapanis":1.4,"skaydet":.4}.get(p['sahne'], .45 if k=='dayi' else .3)
    dur=round(on+(b-a)+son,3); out=f'{S}/p{i:02d}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{S}/{k}.mp3','-af',f'atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.012,afade=t=out:st={max(0,b-a-0.025):.3f}:d=0.025,adelay={int(on*1000)}:all=1,apad=whole_dur={dur}','-ac','1','-ar','48000',out],check=True)
    kel=[w for w in g if not w['text'].startswith('[')]
    p['metin']=re.sub(r'\s*\[\w+\]\s*',' ',satir).strip()
    assert len(kel)==len(p['metin'].split()), (i,len(kel),p['metin'])
    p['sure']=dur
    p['kelime_t']=[round(max(0,on+w['start']-a-0.04),3) for w in kel]
    kon=[]
    for w in kel:
        s0=round(on+w['start']-a,3); s1=round(on+min(w['end'],b)-a,3)
        if kon and s0-kon[-1][1]<0.3: kon[-1][1]=s1
        else: kon.append([s0,s1])
    p['konusma']=kon; dosyalar.append(out)
open(f'{S}/liste.txt','w').write(''.join(f"file '{d}'\n" for d in dosyalar))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{S}/liste.txt','-c','copy',f'{S}/birlesik.wav'],check=True)
sen={"bant":"DAYI SORUYOR #6","kapak":{"ust":"DAYI SORUYOR #6","baslik":"Hayvan [yem] seçiyor!","alt":"Usta cevaplıyor 👇","sure":0.2},"parcalar":P}
json.dump(sen,open(f'{W}/senaryo.json','w'),ensure_ascii=False,indent=1)
print('toplam sure', round(sum(p['sure'] for p in P),2), [p['sure'] for p in P])

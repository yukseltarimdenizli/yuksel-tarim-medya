import json, re, subprocess, sys
sys.path.insert(0,'/home/claude/yuksel-tarim-medya/motor'); import el_ses
W='/tmp/is/dayi5'; S=f'{W}/ses'
def satirlar(f): return [l.strip() for l in open(f) if l.strip()]
def grupla(ws, lines):
    out=[]; i=0
    for s in lines:
        n=len(s.split()); g=ws[i:i+n]; i+=n
        assert [w for w,_,_ in g]==s.split(), (g, s)
        out.append(g)
    assert i==len(ws); return out
LD=satirlar(f'{S}/dayi_prompt.txt'); LU=satirlar(f'{S}/usta_prompt.txt')
k=LD[3].index('[laughs]')+len('[laughs]'); LD=LD[:3]+[LD[3][:k].strip(), LD[3][k:].strip()]
WD=el_ses.kelime_zamanlari(f'{S}/dayi_zaman.json'); WU=el_ses.kelime_zamanlari(f'{S}/usta_zaman.json')
GD=grupla(WD,LD); GU=grupla(WU,LU)
DUR={'dayi':float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{S}/dayi.mp3'],capture_output=True,text=True).stdout),
     'usta':float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{S}/usta.mp3'],capture_output=True,text=True).stdout)}
import array, math
def _prof(nm):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f'{S}/{nm}.mp3','-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout
    return array.array('h',raw)
PR={'dayi':_prof('dayi'),'usta':_prof('usta')}
def _db(A,t):
    i=int(t*8000); seg=A[max(0,i-200):i+200]; return 20*math.log10(max(1,math.sqrt(sum(x*x for x in seg)/max(1,len(seg))))/32768)
def kes(G, dur, nm):
    A=PR[nm]
    seg=[[g[0][1], g[-1][2]] for g in G]
    for i in range(len(seg)-1):
        pe, ns = seg[i][1], seg[i+1][0]
        # sessiz aralık ara: ns-0.06'dan geriye doğru, pe-0.8'e kadar; -70 dB altındaki en geç noktanın biraz gerisi
        adaylar=[round(ns-0.06-k*0.01,3) for k in range(int((ns-0.06-(pe-0.8))*100))]
        sessiz=[t for t in adaylar if _db(A,t)<-70]
        if sessiz:
            # en geç sessiz noktadan başlayıp sessizliğin ortasına kay
            son=sessiz[0]; ilk=son
            for t in sessiz[1:]:
                if abs(t-(ilk-0.01))<0.006: ilk=t
                else: break
            cut=(son+ilk)/2
        else:
            cut=min(adaylar,key=lambda t:_db(A,t)); print('UYARI sessizlik yok',nm,i,round(cut,2),round(_db(A,cut)))
        seg[i][1]=round(cut,3); seg[i+1][0]=round(cut,3)
    seg[0][0]=max(0,seg[0][0]-0.05); seg[-1][1]=round(min(dur, seg[-1][1]+0.25),3)
    return seg
SD=kes(GD,DUR['dayi'],'dayi'); SU=kes(GU,DUR['usta'],'usta')
temiz=lambda s: re.sub(r'\s*\[.*?\]\s*',' ',s).strip()
akis=[
 ("tdayi","d",0,{"balon":["Bu tarla her yıl","biraz daha [inatlaşıyor]! 😤"],"kanca":"3 adım · sonuncusu sürpriz 👇"}),
 ("t3","u",0,{}),
 ("tsebep","u",1,{}),
 ("smadde","u",2,{"baslik":"TABANI KALINLAŞTIRAN","renk":"#c62828","maddeler":[["🌧️","Islak toprağa girmek","ıslak","x"],["🚛","Ağır römorkla dolaşmak","ağır","x"]]}),
 ("ktepki","d",1,{"balon":["Yağmurdan sonra hemen","tarlaya [dalardım]! 😅"]}),
 ("tbelirti","u",3,{}),
 ("tcubuk","u",4,{}),
 ("ktepki","d",2,{"balon":["Kırk yıldır göz kararı,","bir de [çubuğa] bakalım! 😄"]}),
 ("smadde","u",5,{"baslik":"ÇUKUR KONTROLÜ","renk":"#2F5737","maddeler":[["⛏️","Kürekle küçük bir çukur kaz","kürekle","ok"],["👀","Sert katmanı gör","sert","ok"],["🌱","Yana kıvrılan kökleri gör","yana","ok"]]}),
 ("skaydet","u",6,{}),
 ("tdip","u",7,{}),
 ("smadde","u",8,{"baslik":"3. TEKRAR OLUŞMASIN","renk":"#b8860b","maddeler":[["↕️","Sürüm derinliğini değiştir","sürüm","ok"],["🌧️","Islak toprağa girme","ıslak","x"],["🛞","Römorku hep aynı izden geçir","römorku","ok"]]}),
 ("tyonca","u",9,{}),
 ("ktepki","d",3,{"balon":["Toprağın da nefes","alması [lazımmış]! 😄"]}),
 ("tkapanis","d",4,{}),
]
parcalar=[]; dos=[]
for i,(sahne,kim,j,ek) in enumerate(akis):
    src=f'{S}/{"dayi" if kim=="d" else "usta"}.mp3'; a,b=(SD if kim=="d" else SU)[j]; g=(GD if kim=="d" else GU)[j]
    satir=(LD if kim=="d" else LU)[j]
    on=.25 if i==0 else .15; son={"ktepki":.5,"tkapanis":1.4,"skaydet":.4}.get(sahne,.45 if kim=="d" else .3)
    dur=round(on+(b-a)+son,3); out=f'{S}/p{i:02d}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-af',f'atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.015,afade=t=out:st={max(0,b-a-0.03):.3f}:d=0.03,adelay={int(on*1000)}:all=1,apad=whole_dur={dur}','-ac','1','-ar','48000',out],check=True)
    kel=[w for w in g if not w[0].startswith('[')]
    metin=temiz(satir); assert len(kel)==len(metin.split())
    kt=[round(max(0,on+s-a-0.04),3) for _,s,_ in kel]
    kon=[]
    for _,s,e in kel:
        s0=round(on+s-a,3); s1=round(on+min(e,b)-a,3)
        if kon and s0-kon[-1][1]<0.3: kon[-1][1]=s1
        else: kon.append([s0,s1])
    parcalar.append(dict(sahne=sahne,konusan="dayi" if kim=="d" else "usta",metin=metin,sure=dur,kelime_t=kt,konusma=kon,**ek)); dos.append(out)
    print(f"{i:2d} {sahne:9s} {a:6.2f}-{b:6.2f} {dur:5.2f} | {kel[0][0]} … {kel[-1][0]}")
open(f'{S}/liste.txt','w').write(''.join(f"file '{f}'\n" for f in dos))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{S}/liste.txt','-c','pcm_s16le',f'{S}/birlesik.wav'],check=True)
sen={"bant":"DAYI SORUYOR #5","kapak":{"ust":"DAYI SORUYOR #5","baslik":"Tarlanda [beton] var!","alt":"Usta cevaplıyor 👇","sure":0.2},"parcalar":parcalar}
json.dump(sen,open(f'{W}/senaryo.json','w'),ensure_ascii=False,indent=1)
print('toplam',round(sum(p['sure'] for p in parcalar),2))
# kesim noktalarında ses düzeyi
for nm,SG in (("dayi",SD),("usta",SU)):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f'{S}/{nm}.mp3','-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout
    A=array.array('h',raw)
    def db(t):
        i=int(t*8000); seg=A[max(0,i-80):i+80]; return 20*math.log10(max(1,math.sqrt(sum(x*x for x in seg)/max(1,len(seg))))/32768)
    print(nm,'kesimler dB:',[f"{s[1]:.2f}:{db(s[1]):.0f}" for s in SG[:-1]])

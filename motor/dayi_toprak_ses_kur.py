import json, re, subprocess, sys
S='/tmp/is/toprak/ses'; D,Uf=f'{S}/dayi.mp3',f'{S}/usta.mp3'
L=json.load(open('/tmp/is/toprak/satirlar.json'))
dk=[0.0,6.23,10.28,13.15,15.57,19.44]
uk=[0.0,9.32,13.72,22.42,28.82,34.49,38.57,47.72,51.84,59.58,67.40,74.54,79.656]
d=lambda i:(D,dk[i],dk[i+1],L['D'][i]); u=lambda i:(Uf,uk[i],uk[i+1],L['U'][i])
akis=[("dayi",d(0),{"balon":["Bu toprak dedemden kalma,","[tahlil] mi yaptıracağım?"]}),
 ("lab",u(0),{}),("rapor",u(1),{}),
 ("dayi",d(1),{"balon":["Ben her yıl aynı gübreyi atarım,","[kaybım] ne?"],"prop":"gubre"}),
 ("karsilastir",u(2),{}),
 ("dayi",d(2),{"balon":["Peki bu [numuneyi]","nasıl alacağız?"],"prop":"kurek"}),
 ("zaman",u(3),{}),("harita",u(4),{}),("kacin",u(5),{}),("karistir",u(6),{}),("teslim",u(7),{}),
 ("dayi",d(3),{"balon":["Eee, sonuç gelince","[ne olacak?]"],"prop":"rapor"}),
 ("muhendis",u(8),{}),("takvim",u(9),{}),("ozet",u(10),{}),
 ("tepki",d(4),{"balon":["Kırk yıl gübreyi [göz kararı]","atmışız yani, hah! 😄"]}),
 ("kapanis",u(11),{})]
parcalar=[]; dosyalar=[]
for i,(sahne,(src,a,b,metin),ek) in enumerate(akis):
    on=.25 if i==0 else .15; son={"tepki":.6,"kapanis":1.0}.get(sahne,.45 if src==D else .3)
    dur=round(on+(b-a)+son,3); out=f'{S}/p{i:02d}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-af',f'atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,adelay={int(on*1000)}:all=1,apad=whole_dur={dur}','-ac','1','-ar','48000',out],check=True)
    log=subprocess.run(['ffmpeg','-hide_banner','-i',out,'-af','silencedetect=noise=-38dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
    sil=list(zip(st,en+[dur]*(len(st)-len(en)))); kon=[]; t=0.0
    for s0,s1 in sil:
        if s0>t+0.05: kon.append([round(t,3),round(s0,3)])
        t=max(t,s1)
    if t<dur-0.05: kon.append([round(t,3),round(dur,3)])
    p=dict(sahne=sahne,konusan="dayi" if src==D else "usta",metin=metin,sure=dur,konusma=kon,**ek); parcalar.append(p); dosyalar.append(out)
    nok=len([w for w in metin.split() if re.search(r'[,.!?:;]$',w)])
    print(f"{i:2d} {sahne:12s} {dur:6.2f} konuşma-aralığı:{len(kon)} noktalama:{nok}")
open(f'{S}/liste.txt','w').write(''.join(f"file '{f}'\n" for f in dosyalar))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{S}/liste.txt','-c','pcm_s16le',f'{S}/birlesik.wav'],check=True)
sen={"bant":"DAYI SORUYOR","kapak":{"ust":"DAYI SORUYOR","baslik":"Toprak analizi [şart mı?]","alt":"Usta cevaplıyor 👇","sure":0.2},"parcalar":parcalar}
json.dump(sen,open('/tmp/is/toprak/senaryo.json','w'),ensure_ascii=False,indent=1)
print("toplam", round(sum(p['sure'] for p in parcalar),2))

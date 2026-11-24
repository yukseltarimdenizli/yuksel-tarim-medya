import json, re, subprocess
W='/tmp/is/dayi4'; S=f'{W}/ses'
sen=json.load(open(f'{W}/senaryo_hiz.json')); P=sen['parcalar']
def kelimeler(f):
    return [w for w in json.load(open(f))['words'] if w['type']=='word']
def satirla(ws, satirlar):
    """scribe kelimelerini satırlara dağıt; etiketleri ([laughs]) ayrı tut"""
    out=[]; i=0
    for s in satirlar:
        hedef=re.sub(r'\[.*?\]','',s).split(); grup=[]; n=0
        kuyruk=len(re.findall(r'\[\w+\]', re.sub(r'^.*[^\]\s]\s', '', s.strip()+' '))) if re.search(r'\]\s*$',s) else 0
        # satır başındaki etiketleri al
        while i<len(ws) and (n<len(hedef) or ws[i]['text'].startswith('[')):
            w=ws[i]
            if w['text'].startswith('['):
                if n==len(hedef):
                    if kuyruk<=0: break
                    kuyruk-=1
                grup.append(w); i+=1; continue
            assert w['text'].lower().strip('.,!?;:')==hedef[n].lower().strip('.,!?;:'), (w['text'],hedef[n])
            grup.append(w); i+=1; n+=1
        out.append(grup)
    assert i==len(ws), (i,len(ws))
    return out
LD=[l.strip() for l in open(f'{W}/dayi_prompt.txt') if l.strip()]
LU=[l.strip() for l in open(f'{W}/usta_prompt.txt') if l.strip()]
# Dayı son satırı ikiye
i=LD[4].index('!')+1; LD=LD[:4]+[LD[4][:i].strip(), LD[4][i:].strip()]
gd=satirla(kelimeler(f'{W}/scribe_dayi.json'),LD); gu=satirla(kelimeler(f'{W}/scribe_usta.json'),LU)
def kesimler(gruplar, dur):
    """her satır için [a,b] ses aralığı: komşu satır arasındaki boşluğu paylaştır"""
    seg=[]
    for k,g in enumerate(gruplar):
        a=g[0]['start']; b=g[-1]['end']
        seg.append([a,b])
    for k in range(len(seg)-1):
        pe=seg[k][1]; ns=seg[k+1][0]
        # scribe 'end' noktalamada boşluğa taşabilir; kesimi bir sonraki kelimenin 0.08 s öncesine koy
        cut=max(pe-0.25, ns-0.08) if ns-pe<0.6 else pe+0.25
        seg[k][1]=round(min(cut,ns-0.05),3); seg[k+1][0]=round(max(cut,seg[k][1]),3)
    seg[0][0]=max(0,seg[0][0]-0.05); seg[-1][1]=min(dur,seg[-1][1]+0.2)
    return seg
DUR={'dayi':31.399,'usta':103.706}
sd=kesimler(gd,DUR['dayi']); su=kesimler(gu,DUR['usta'])
sira={'dayi':0,'usta':0}; dosyalar=[]
for i,p in enumerate(P):
    k=p['konusan']; j=sira[k]; sira[k]+=1
    (a,b)=(sd if k=='dayi' else su)[j]; g=(gd if k=='dayi' else gu)[j]
    src=f'{S}/{k}.mp3'
    on=.25 if i==0 else .15; son={"ktepki":.5,"ikapanis":1.4,"skaydet":.4}.get(p['sahne'],.45 if k=='dayi' else .3)
    dur=round(on+(b-a)+son,3); out=f'{S}/p{i:02d}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-af',f'atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.015,afade=t=out:st={max(0,b-a-0.03):.3f}:d=0.03,adelay={int(on*1000)}:all=1,apad=whole_dur={dur}','-ac','1','-ar','48000',out],check=True)
    kel=[w for w in g if not w['text'].startswith('[')]
    assert len(kel)==len(p['metin'].split()), (i,len(kel),p['metin'])
    p['kelime_t']=[round(on+w['start']-a,3) for w in kel]
    kon=[]
    for w in kel:
        s0=round(on+w['start']-a,3); s1=round(on+min(w['end'],b)-a,3)
        if kon and s0-kon[-1][1]<0.3: kon[-1][1]=s1
        else: kon.append([s0,s1])
    p['konusma']=kon; p['sure']=dur
    print(f"{i:2d} {p['sahne']:9s} {a:7.2f}-{b:7.2f} dur {dur:5.2f} | {kel[0]['text']} … {kel[-1]['text']}")
open(f'{S}/liste.txt','w').write(''.join(f"file '{S}/p{i:02d}.wav'\n" for i in range(len(P))))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{S}/liste.txt','-c','pcm_s16le',f'{S}/birlesik.wav'],check=True)
json.dump(sen,open(f'{W}/senaryo_hiz.json','w'),ensure_ascii=False,indent=1)
print('toplam',round(sum(p['sure'] for p in P),2))

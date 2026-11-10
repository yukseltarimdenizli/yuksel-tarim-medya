# Sesleri satırlara böl, parçalara yerleştir, birleşik ses + senaryo üret
import json, re, subprocess, sys
sys.path.insert(0,'/home/claude/yuksel-tarim-medya/motor')
S='/tmp/is/dayi/ses'
D, U = f'{S}/dayi.mp3', f'{S}/usta.mp3'
# (kaynak, başlangıç, bitiş, ön boşluk, son boşluk)
plan=[(D,0.0,2.89,.25,.45),(U,0.0,6.0,.15,.25),(U,6.0,10.3,.15,.25),(U,10.3,18.65,.15,.25),(D,2.89,4.656,.15,.6),(U,18.65,24.024,.15,1.0)]
sen=json.load(open('/tmp/is/dayi/senaryo1.json'))
parcalar=[]
for i,((src,a,b,on,son),p) in enumerate(zip(plan,sen['parcalar'])):
    dur=round(on+(b-a)+son,3)
    out=f'{S}/p{i}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-af',f'atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,adelay={int(on*1000)}:all=1,apad=whole_dur={dur}','-ac','1','-ar','48000',out],check=True)
    log=subprocess.run(['ffmpeg','-hide_banner','-i',out,'-af','silencedetect=noise=-38dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
    sil=list(zip(st,en+[dur]*(len(st)-len(en))))
    kon=[]; t=0.0
    for s0,s1 in sil:
        if s0>t+0.05: kon.append([round(t,3),round(s0,3)])
        t=max(t,s1)
    if t<dur-0.05: kon.append([round(t,3),round(dur,3)])
    p['sure']=dur; p['konusma']=kon
    print(i,p['sahne'],dur,kon)
open(f'{S}/liste.txt','w').write(''.join(f"file 'p{i}.wav'\n" for i in range(len(plan))))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{S}/liste.txt','-c','pcm_s16le',f'{S}/birlesik.wav'],check=True)
json.dump(sen,open('/tmp/is/dayi/senaryo_sesli.json','w'),ensure_ascii=False,indent=1)
print('toplam',sum(p['sure'] for p in sen['parcalar']), subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{S}/birlesik.wav'],capture_output=True,text=True).stdout)

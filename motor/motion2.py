"""Yüksel Tarım — ürün vitrinli hareketli video (1080x1920, 30 fps).
Sahneler: logo açılışı → başlık → ürün kahraman sahnesi (kesilmiş ürün) → çerçeveli fotoğraf
sahneleri (sinematik kamera hareketi) → kapanış. İçerik video.json'dan gelir.
Kullanım: python3 motion2.py <video.json> <cikti.mp4>   |  önizleme: ... <out_dir> 10,50,90
"""
import base64, json, sys, pathlib, subprocess, shutil, tempfile, html, mimetypes
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS, W, H = 30, 1080, 1920
WEB = "www.yukseltarimdenizli.com.tr"

def uri(p):
    p = ROOT / p; mt = mimetypes.guess_type(str(p))[0] or "image/png"
    return f"data:{mt};base64," + base64.b64encode(p.read_bytes()).decode()

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--g:#2F5737;--gd:#14281A;--au:#D4A445;--cr:#F5F0E3}
body{width:1080px;height:1920px;overflow:hidden;font-family:Poppins,sans-serif;background:var(--gd);position:relative;color:#fff}
.sc{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.abs{position:absolute} canvas{position:absolute;inset:0}
.halo{left:50%;width:640px;height:640px;margin-left:-320px;border-radius:50%;background:radial-gradient(circle,#F5F0E3 0 58%,rgba(245,240,227,.35) 59%,rgba(245,240,227,0) 70%)}
.lg{position:absolute;left:50%;top:700px;width:440px;height:380px;margin-left:-220px}
.lg img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}
.glint{position:absolute;inset:0;background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.8) 50%,transparent 60%);background-size:200% 100%;mix-blend-mode:overlay}
.brand{left:0;right:0;text-align:center;font-weight:700;font-size:82px;letter-spacing:6px;white-space:nowrap}
.brand i{display:inline-block;font-style:normal}
.city{left:0;right:0;text-align:center;color:var(--au);font-size:34px;font-weight:500}
.hdr{left:64px;top:76px;display:flex;align-items:center;gap:20px}
.hdr img{width:86px} .hdr b{display:block;font-size:32px;letter-spacing:1px} .hdr span{font-size:19px;letter-spacing:6px;color:var(--au);font-weight:500}
.kick{padding:14px 30px;background:var(--au);color:var(--gd);font-weight:700;font-size:30px;border-radius:50px;transform-origin:left center;letter-spacing:1px}
.title{font-weight:700;line-height:1.06}
.wd{display:inline-block;overflow:hidden;vertical-align:bottom;padding:0 .2em .08em 0}
.wd i{display:inline-block;font-style:normal} .wd.gold i{color:var(--au)}
.brush{position:absolute;height:22px;background:var(--au);border-radius:12px;transform-origin:left}
.spot{inset:0;background:radial-gradient(ellipse 70% 45% at 50% 62%,rgba(212,164,69,.28),rgba(20,40,26,0) 70%)}
.ghost{left:-40px;right:-40px;text-align:center;font-weight:700;font-size:560px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(212,164,69,.22);letter-spacing:-10px}
.label{left:64px;font-size:34px;font-weight:600;color:var(--au);letter-spacing:8px}
.pname{left:64px;right:64px;font-size:150px;font-weight:700;line-height:1;letter-spacing:-2px}
.pdesc{left:64px;right:64px;font-size:40px;font-weight:500;line-height:1.3;color:rgba(255,255,255,.88)}
.chips{left:64px;right:64px;display:flex;flex-wrap:wrap;gap:18px}
.chip{padding:16px 30px;border-radius:60px;border:3px solid var(--au);background:rgba(20,40,26,.65);font-size:36px;font-weight:600;white-space:nowrap}
.chip b{color:var(--au)}
.hero{left:50%}
.hero img{width:100%;display:block;filter:drop-shadow(0 30px 40px rgba(0,0,0,.45))}
.floor{left:50%;width:900px;height:90px;margin-left:-450px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.55),rgba(0,0,0,0) 70%)}
.bgblur{inset:-80px;background-size:cover;background-position:center;filter:blur(34px) brightness(.42) saturate(1.2)}
.frame{left:48px;right:48px;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55);outline:4px solid rgba(212,164,69,.9);outline-offset:-4px}
.frame .ph{position:absolute;inset:0;background-size:cover;background-position:center;filter:contrast(1.08) saturate(1.15) brightness(1.03)}
.frame:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.45));pointer-events:none}
.inset{width:430px;border-radius:22px;overflow:hidden;border:5px solid var(--au);box-shadow:0 20px 50px rgba(0,0,0,.6)}
.inset img{width:100%;display:block}
.inset .cap{position:absolute;left:0;right:0;bottom:0;padding:10px 16px;background:linear-gradient(transparent,rgba(0,0,0,.8));font-size:24px;font-weight:600}
.wipe{position:absolute;top:-400px;bottom:-400px;width:900px;background:var(--au);transform:skewX(-18deg);z-index:50}
.wipe2{position:absolute;top:-400px;bottom:-400px;width:500px;background:var(--g);transform:skewX(-18deg);z-index:49}
.price{left:64px;display:flex;align-items:baseline;gap:14px;padding:14px 30px 16px;border-radius:24px;background:var(--au);color:var(--gd);box-shadow:0 18px 40px rgba(0,0,0,.45);transform-origin:left center}
.price small{font-size:26px;font-weight:600;letter-spacing:1px;position:absolute;top:-44px;left:6px;color:var(--au)}
.price b{font-size:104px;line-height:1;font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-2px}
.price span{font-size:46px;font-weight:700}
.gcol{left:70px;right:70px;top:640px;display:flex;flex-direction:column;align-items:center;gap:34px}
.gtitle{text-align:center;font-weight:700;line-height:1.08;color:#fff}
.gtitle .wd.gold i{color:var(--au)}
.gsub{padding:0 20px;text-align:center;font-size:42px;line-height:1.45;color:rgba(255,255,255,.9)}
.gline{height:6px;width:420px;background:var(--au);border-radius:6px;transform-origin:center}
.gkick{text-align:center;font-size:32px;font-weight:600;letter-spacing:10px;color:var(--au)}
.glogo{left:50%;width:150px;margin-left:-75px}
.ltitle{font-size:84px;font-weight:700;line-height:1.08;color:var(--g)}
.litem{display:flex;align-items:center;gap:28px;background:#fff;border-radius:28px;padding:26px 30px;box-shadow:0 14px 36px rgba(26,51,33,.14)}
.litem b{flex:none;width:84px;height:84px;border-radius:50%;background:var(--g);color:var(--au);display:grid;place-items:center;font-size:44px;font-weight:700}
.litem span{font-size:40px;font-weight:600;line-height:1.25;color:var(--gd)}
.perks{left:64px;right:64px;display:flex;flex-wrap:wrap;gap:10px}
.perk{display:flex;align-items:center;gap:8px;padding:11px 16px;border-radius:16px;background:var(--cr);color:var(--gd);font-size:27px;font-weight:700;white-space:nowrap;box-shadow:0 10px 24px rgba(0,0,0,.35)}
.perk i{font-style:normal;color:var(--g);font-size:30px}
.web{left:0;right:0;text-align:center;font-size:42px;font-weight:600}
.cta{left:50%;padding:24px 54px;border-radius:70px;background:var(--au);color:var(--gd);font-size:40px;font-weight:700;white-space:nowrap}
.ring{border:4px solid var(--au);border-radius:80px}
.endhalo{left:50%;width:460px;height:460px;margin-left:-230px;border-radius:50%;background:var(--cr);box-shadow:0 0 0 18px rgba(212,164,69,.35)}
"""

JS = r"""
const FPS=30, $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
function spring(f,{damping=12,stiffness=120,mass=1}={}){ if(f<=0) return 0; let x=0,v=0; const dt=1/FPS/4;
  for(let i=0;i<f*4;i++){const a=(-stiffness*(x-1)-damping*v)/mass; v+=a*dt; x+=v*dt;} return x;}
function lerp(f,[a,b],[c,d],e=t=>t){ const t=Math.min(1,Math.max(0,(f-a)/(b-a))); return c+(d-c)*e(t);}
const eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2, eo=t=>1-Math.pow(1-t,3);
const S=(el,o)=>{ if(el) for(const k in o) el.style[k]=o[k]; };
function field(cv,f,color,alpha){ const c=cv.getContext('2d'); c.clearRect(0,0,1080,1920); c.strokeStyle=color; c.lineWidth=3; const vx=540,vy=-300;
  c.globalAlpha=alpha; for(let i=-14;i<=14;i++){c.beginPath();c.moveTo(vx,vy);c.lineTo(540+i*170,1920);c.stroke();}
  c.lineWidth=2; for(let k=0;k<14;k++){const z=((k+f/45)%14)/14,y=vy+(1920-vy)*z*z; c.globalAlpha=alpha*z; c.beginPath();c.moveTo(0,y);c.lineTo(1080,y);c.stroke();} c.globalAlpha=1;}
const P=[...Array(70)].map((_,i)=>({x:(i*397)%1080,y:(i*733)%1920,s:2+(i%5),v:.4+(i%7)/6}));
function dust(cv,f,col){ const c=cv.getContext('2d'); c.fillStyle=col; for(const p of P){const y=(p.y-f*p.v*3+7680)%1920,x=p.x+Math.sin((f+p.y)/40)*18;
  c.globalAlpha=.25+.35*Math.abs(Math.sin((f+p.x)/30)); c.beginPath(); c.arc(x,y,p.s,0,7); c.fill();} c.globalAlpha=1;}
function words(root,t0){ $$('.wd i',root).forEach((el,i)=>{const s=spring(t0-i*4,{damping:13,stiffness:140}); S(el,{transform:`translateY(${(1-s)*115}%) rotate(${(1-s)*8}deg)`});}); }
function pops(root,sel,t0,gap=5){ $$(sel,root).forEach((el,i)=>{const s=spring(t0-i*gap,{damping:9,stiffness:150}); S(el,{transform:`scale(${s})`,opacity:Math.min(1,s*2)});}); }

const SCENES=__SCENES__;
const R={
 intro(el,t,d){ field($('canvas',el),t,'#D4A445',.10); dust($('canvas',el),t,'#D4A445');
   const out=lerp(t,[d-14,d],[0,1],eio), ls=spring(t-4,{damping:11,stiffness:90});
   S($('.halo',el),{transform:`translateY(${-out*300}px) scale(${spring(t,{damping:14,stiffness:70})*(1-out*.5)})`,opacity:1-out});
   S($('.lg',el),{opacity:1-out,transform:`translateY(${-out*300}px) scale(${(.55+.45*ls)*(1-out*.5)})`,filter:`blur(${Math.max(0,(1-ls)*12)}px)`});
   const r=lerp(t,[14,42],[0,210],eo); S($('.la',el),{clipPath:`polygon(0 100%,0 ${100-r}%,${r}% 100%)`});
   S($('.glint',el),{backgroundPosition:`${lerp(t,[42,66],[-600,600])}px 0`});
   $$('.brand i',el).forEach((c,i)=>{const s=spring(t-28-i*2.2,{damping:14,stiffness:160}); S(c,{transform:`translateY(${(1-s)*90}px)`,opacity:Math.min(1,s*1.4)});});
   S($('.brand',el),{opacity:1-out}); S($('.city',el),{opacity:lerp(t,[46,60],[0,1])*(1-out),letterSpacing:`${lerp(t,[46,72],[4,20],eo)}px`}); },
 headline(el,t,d){ field($('canvas',el),t+80,'#2F5737',.06);
   const up=lerp(t,[0,22],[0,1],eio); S(el,{clipPath:`polygon(0 ${100-up*100+(1-up)*9}%,100% ${100-up*100}%,100% 100%,0 100%)`});
   S($('.hdr',el),{transform:`translateX(${(1-spring(t,{damping:16}))*-500}px)`});
   S($('.kick',el),{transform:`scale(${spring(t-6,{damping:9,stiffness:150})})`}); words(el,t-12);
   const gw=$('.wd.gold',el), n=$$('.wd',el).length; if(gw){const r=gw.getBoundingClientRect(),b=lerp(t,[14+n*4,26+n*4],[0,1],eo);
     S($('.brush',el),{left:r.left+'px',top:(r.bottom-26)+'px',width:(r.width*.9)+'px',transform:`scaleX(${b}) skewX(-12deg)`});}
   S($('.wm',el),{transform:`rotate(${-10+t*.08}deg)`}); },
 hero(el,t,d){ field($('canvas',el),t,'#D4A445',.07); dust($('canvas',el),t,'#D4A445');
   S($('.ghost',el),{transform:`translateX(${lerp(t,[0,d],[120,-120])}px)`,opacity:lerp(t,[0,16],[0,1])});
   S($('.hdr',el),{opacity:lerp(t,[4,16],[0,1])});
   S($('.label',el),{opacity:lerp(t,[8,20],[0,1]),letterSpacing:`${lerp(t,[8,30],[2,8],eo)}px`});
   const n=spring(t-12,{damping:14,stiffness:120}); S($('.pname',el),{transform:`translateY(${(1-n)*120}px)`,opacity:Math.min(1,n*1.5),clipPath:`inset(0 0 ${(1-n)*100}% 0)`});
   const dr=spring(t-18,{damping:15,stiffness:70}), push=lerp(t,[30,d],[1,1.06]);
   S($('.hero',el),{transform:`translateX(calc(-50% + ${(1-dr)*1300}px)) scale(${push}) rotate(${(1-dr)*-2}deg)`});
   S($('.floor',el),{opacity:dr,transform:`scaleX(${.6+.4*dr})`});
   S($('.pdesc',el),{opacity:lerp(t,[40,54],[0,1]),transform:`translateY(${lerp(t,[40,56],[30,0],eo)}px)`});
   pops(el,'.chip',t-50,6); S($('.foot',el),{transform:`translateY(${(1-spring(t-20,{damping:16}))*160}px)`}); },
 photo(el,t,d){ const kb=lerp(t,[0,d],[0,1]), cfg=SCENES[el.dataset.i];
   S($('.bgblur',el),{transform:`scale(${1.1+kb*.08})`});
   S($('.hdr',el),{opacity:lerp(t,[2,14],[0,1])});
   const fr=spring(t-2,{damping:15,stiffness:90}); S($('.frame',el),{transform:`translateY(${(1-fr)*260}px) scale(${.85+.15*fr})`,opacity:Math.min(1,fr*2)});
   const [x0,y0,s0,x1,y1,s1]=cfg.kb||[0,0,1.02,-30,-10,1.16]; S($('.frame .ph',el),{transform:`translate(${x0+(x1-x0)*kb}px,${y0+(y1-y0)*kb}px) scale(${s0+(s1-s0)*kb})`});
   S($('.label',el),{opacity:lerp(t,[8,20],[0,1]),letterSpacing:`${lerp(t,[8,30],[2,8],eo)}px`});
   const n=spring(t-10,{damping:14,stiffness:120}); S($('.pname',el),{transform:`translateY(${(1-n)*100}px)`,opacity:Math.min(1,n*1.5)});
   S($('.pdesc',el),{opacity:lerp(t,[22,36],[0,1]),transform:`translateY(${lerp(t,[22,38],[30,0],eo)}px)`});
   pops(el,'.chip',t-30,6); pops(el,'.perk',t-44,7); S($('.foot',el),{transform:`translateY(${(1-spring(t-12,{damping:16}))*160}px)`});
   const pr=$('.price',el); if(pr){ const s=spring(t-14,{damping:10,stiffness:120}); S(pr,{transform:`scale(${s}) rotate(${(1-s)*-6}deg)`,opacity:Math.min(1,s*2)});
     const v=+$('b',pr).dataset.v, k=lerp(t,[18,46],[0,1],eo); $('b',pr).textContent=(Math.round(v*k/1000)*1000).toLocaleString('tr-TR'); }
   const ins=$('.inset',el); if(ins){const s=spring(t-(cfg.inset_at||60),{damping:11,stiffness:110}); S(ins,{transform:`scale(${s}) rotate(${(1-s)*-25+4}deg)`,opacity:Math.min(1,s*2)});} },
 greeting(el,t,d){ field($('canvas',el),t,'#D4A445',.09); dust($('canvas',el),t,'#F5D58A');
   const up=lerp(t,[0,20],[0,1],eio); S(el,{clipPath:`circle(${up*140}% at 50% 50%)`});
   S($('.glogo',el),{transform:`scale(${spring(t-8,{damping:11,stiffness:120})})`});
   S($('.gkick',el),{opacity:lerp(t,[12,24],[0,1]),letterSpacing:`${lerp(t,[12,40],[2,10],eo)}px`});
   words(el,t-18); const n=$$('.wd',el).length;
   S($('.gline',el),{transform:`scaleX(${lerp(t,[22+n*4,40+n*4],[0,1],eo)})`});
   S($('.gsub',el),{opacity:lerp(t,[30+n*4,46+n*4],[0,1]),transform:`translateY(${lerp(t,[30+n*4,48+n*4],[40,0],eo)}px)`}); },
 list(el,t,d){ field($('canvas',el),t+40,'#2F5737',.05);
   const up=lerp(t,[0,22],[0,1],eio); S(el,{clipPath:`polygon(0 ${100-up*100+(1-up)*9}%,100% ${100-up*100}%,100% 100%,0 100%)`});
   S($('.hdr',el),{transform:`translateX(${(1-spring(t,{damping:16}))*-500}px)`});
   S($('.kick',el),{transform:`scale(${spring(t-6,{damping:9,stiffness:150})})`});
   const tt=spring(t-10,{damping:14}); S($('.ltitle',el),{opacity:Math.min(1,tt*1.5),transform:`translateY(${(1-tt)*80}px)`});
   $$('.litem',el).forEach((it,i)=>{ const s=spring(t-26-i*14,{damping:13,stiffness:110}); S(it,{transform:`translateX(${(1-s)*1100}px) rotate(${(1-s)*5}deg)`});
     S($('b',it),{transform:`scale(${spring(t-32-i*14,{damping:8,stiffness:170})})`}); });
   S($('.foot',el),{transform:`translateY(${(1-spring(t-12,{damping:16}))*160}px)`}); },
 outro(el,t,d){ field($('canvas',el),t,'#D4A445',.08); dust($('canvas',el),t,'#D4A445');
   S(el,{clipPath:`circle(${lerp(t,[0,22],[0,140],eio)}% at 50% 72%)`});
   S($('.endhalo',el),{transform:`scale(${spring(t-6,{damping:12,stiffness:90})})`});
   S($('.endlogo',el),{transform:`scale(${spring(t-10,{damping:10,stiffness:110})}) rotate(${(1-spring(t-10))*-20}deg)`});
   [['.brand',18],['.city',23]].forEach(([q,dl])=>{const s=spring(t-dl,{damping:14}); S($(q,el),{opacity:Math.min(1,s),transform:`translateY(${(1-s)*60}px)`});});
   const url=el.dataset.web, k=Math.floor(lerp(t,[28,54],[0,url.length])); $('.web',el).textContent=url.slice(0,k)+((k<url.length&&t>26&&t%10<5)?'|':'');
   if(!$('.cta',el)) return;
   const cs=spring(t-52,{damping:9,stiffness:140}); S($('.cta',el),{transform:`translateX(-50%) scale(${cs})`});
   const cr=$('.cta',el).getBoundingClientRect(), p=((t-60)%30)/30;
   S($('.ring',el),{display:t>60?'block':'none',left:cr.left+'px',top:cr.top+'px',width:cr.width+'px',height:cr.height+'px',transform:`scale(${1+p*.35})`,opacity:1-p}); }
};
window.renderFrame=function(f){
  $$('.sc').forEach((el,i)=>{ const s=SCENES[i], t=f-s.start, vis=t>=-1 && t<s.dur+ (s.overlap||0);
    el.style.visibility=vis?'visible':'hidden'; if(vis) R[s.type](el,t,s.dur); });
  // altın geçiş silmesi
  $$('.wipe,.wipe2').forEach(w=>w.style.left='-2000px');
  for(const w of SCENES.filter(s=>s.wipe)){ const t=f-w.start+10; if(t<0||t>22) continue; const x=lerp(t,[0,22],[1300,-1900],eio);
    S($('.wipe'),{left:x+'px'}); S($('.wipe2'),{left:(x+700)+'px'}); }
};
"""

def esc(s): return html.escape(s)
FOOT_TOP = 1545  # bandın üst kenarı; marka satırı 1350-1470 arasında (Facebook 4:5 ve TikTok için güvenli)
def foot_html():
    return (f'<div class="abs foot" style="left:0;right:0;top:{FOOT_TOP}px;bottom:0;background:#14281A;border-top:8px solid var(--au);color:#fff">'
            f'<div style="height:84px;display:flex;align-items:center;justify-content:center;gap:22px">'
            f'<img src="__LOGO__" style="width:54px">'
            f'<div style="line-height:1.15"><div style="font-size:30px;font-weight:700;letter-spacing:2px">YÜKSEL TARIM <span style="color:var(--au)">DENİZLİ</span></div>'
            f'<div style="font-size:30px;font-weight:500;color:var(--au)">{WEB}</div></div></div></div>')
FOOT = "__FOOT__"

def title_html(t):
    return "".join(f'<span class="wd{" gold" if w.startswith("[") else ""}"><i>{esc(w.strip("[]"))}</i></span>' for w in t.split())

def hdr(logo): return f'<div class="hdr abs"><img src="{logo}"><div><b>YÜKSEL TARIM</b><span>DENİZLİ</span></div></div>'

def build(cfg):
    logo, green, gold = uri("assets/logo.png"), uri("assets/logo_green.png"), uri("assets/logo_gold.png")
    brand = "".join(f"<i>{c if c != ' ' else '&nbsp;'}</i>" for c in "YÜKSEL TARIM")
    scenes, parts, f = [], [], 0
    for i, s in enumerate(cfg["scenes"]):
        s = dict(s); s["start"] = f; t = s["type"]
        if t == "intro":
            s.setdefault("dur", 80)
            parts.append(f'<div class="sc"><canvas width="1080" height="1920"></canvas><div class="halo abs" style="top:600px"></div>'
                         f'<div class="lg"><img src="{green}"><img class="la" src="{gold}"><div class="glint" style="-webkit-mask:url({logo}) center/contain no-repeat"></div></div>'
                         f'<div class="brand abs" style="top:1290px">{brand}</div><div class="city abs" style="top:1400px">DENİZLİ</div></div>')
        elif t == "headline":
            s.setdefault("dur", 95)
            longest = max(len(w.strip("[]")) for w in s["title"].split()); fs = min(130, int(1450 / max(longest, 6)))
            parts.append(f'<div class="sc" style="background:var(--cr);color:var(--g)"><canvas width="1080" height="1920"></canvas>'
                         f'<img class="wm abs" src="{logo}" style="width:900px;right:-260px;bottom:200px;opacity:.06">'
                         f'<div class="hdr abs" style="color:var(--g)"><img src="{logo}"><div><b>YÜKSEL TARIM</b><span>DENİZLİ</span></div></div>'
                         f'<div class="abs" style="left:64px;right:150px;top:290px;bottom:420px;display:flex;flex-direction:column;justify-content:center">'
                         f'<div class="kick" style="align-self:flex-start">{esc(s["kicker"])}</div>'
                         f'<div class="title" style="margin-top:30px;font-size:{fs}px;color:var(--g)">{title_html(s["title"])}</div>'
                         f'<div style="margin-top:34px;font-size:40px;line-height:1.4;color:#3d4b40">{esc(s.get("sub",""))}</div></div><div class="brush"></div></div>')
        elif t == "hero":
            s.setdefault("dur", 130)
            chips = "".join(f'<div class="chip">{c}</div>' for c in s.get("chips", []))
            from PIL import Image as _I
            iw, ih = _I.open(ROOT / s["image"]).size; top = s.get("img_top", 640); bottom = top + int(s.get("img_w", 1000) * ih / iw)
            s["img_top"] = top; floor_y, desc_y = bottom - 50, bottom + 70
            parts.append(f'<div class="sc" style="background:linear-gradient(#0f2014,#1d3a25)"><canvas width="1080" height="1920"></canvas><div class="spot abs"></div>'
                         f'<div class="ghost abs" style="top:720px">{esc(s.get("ghost",""))}</div>{hdr(logo)}'
                         f'<div class="label abs" style="top:300px">{esc(s["label"])}</div><div class="pname abs" style="top:350px">{esc(s["name"])}</div>'
                         f'<div class="floor abs" style="top:{floor_y}px"></div><div class="hero abs" style="top:{s.get("img_top",760)}px;width:{s.get("img_w",1000)}px"><img src="{uri(s["image"])}"></div>'
                         f'<div class="pdesc abs" style="top:{desc_y}px">{esc(s.get("desc",""))}</div><div class="chips abs" style="top:{desc_y+140}px">{chips}</div>{FOOT}</div>')
        elif t == "photo":
            # GÜVENLİ ALAN: Facebook akışı 9:16'yı ortadan 4:5 kırpar (üst/alt ~285px), TikTok altta ~420px ve sağda
            # ~150px'i butonlarla kaplar. Önemli her şey y 285-1480, x 64-930 içinde kalır.
            s.setdefault("dur", 100)
            im = uri(s["image"]); fh = min(s.get("frame_h", 560), 560); FY = 480
            chips = "".join(f'<div class="chip">{c}</div>' for c in s.get("chips", []))
            inset = ""
            if s.get("inset"):
                inset = (f'<div class="inset abs" style="right:40px;top:{FY+fh-200}px;width:360px"><img src="{uri(s["inset"])}">'
                         f'<div class="cap">{esc(s.get("inset_cap",""))}</div></div>')
            y = FY + fh + 60
            price = ""
            if s.get("price"):
                price = (f'<div class="price abs" style="top:{y+40}px"><small>{esc(s.get("price_label","KAMPANYA FİYATI"))}</small>'
                         f'<b data-v="{int(s["price"])}">0</b><span>TL</span></div>')
                y += 190
            perks = ""
            if s.get("perks"):
                perks = (f'<div class="perks abs" style="top:{y}px;right:120px">' +
                         "".join(f'<div class="perk"><i>✓</i>{esc(x)}</div>' for x in s["perks"]) + '</div>')
                alt = ""
            else:
                alt = (f'<div class="pdesc abs" style="top:{y}px;right:150px">{esc(s.get("desc",""))}</div>'
                       f'<div class="chips abs" style="top:{y+120}px;right:150px">{chips}</div>')
            parts.append(f'<div class="sc" data-i="{i}"><div class="bgblur abs" style="background-image:url({im})"></div>{hdr(logo)}'
                         f'<div class="label abs" style="top:300px">{esc(s["label"])}</div><div class="pname abs" style="top:345px;font-size:{min(s.get("name_fs",120),120)}px">{esc(s["name"])}</div>'
                         f'<div class="frame abs" style="top:{FY}px;height:{fh}px"><div class="ph" style="background-image:url({im})"></div></div>'
                         f'{alt}{inset}{price}{perks}{FOOT}</div>')
        elif t == "greeting":
            s.setdefault("dur", 150)
            bg = s.get("bg", "#14281A")
            longest = max(len(w.strip("[]")) for w in s["title"].split()); fs = min(140, int(1500 / max(longest, 6)))
            parts.append(f'<div class="sc" style="background:radial-gradient(ellipse at 50% 40%,{s.get("bg2","#2F5737")},{bg} 70%)"><canvas width="1080" height="1920"></canvas>'
                         f'<div class="halo abs" style="top:300px;width:300px;height:300px;margin-left:-150px"></div><img class="glogo abs" src="{logo}" style="top:370px">'
                         f'<div class="gcol abs"><div class="gkick">{esc(s.get("kicker",""))}</div>'
                         f'<div class="gtitle" style="font-size:{fs}px">{title_html(s["title"])}</div>'
                         f'<div class="gline"></div><div class="gsub">{esc(s.get("sub",""))}</div></div>{FOOT}</div>')
        elif t == "list":
            items = s.get("items", [])
            s.setdefault("dur", 60 + 14 * len(items) + 70)
            li = "".join(f'<div class="litem"><b>{k+1}</b><span>{esc(x)}</span></div>' for k, x in enumerate(items))
            parts.append(f'<div class="sc" style="background:var(--cr);color:var(--g)"><canvas width="1080" height="1920"></canvas>'
                         f'<div class="hdr abs" style="color:var(--g)"><img src="{logo}"><div><b>YÜKSEL TARIM</b><span>DENİZLİ</span></div></div>'
                         f'<div class="abs" style="left:64px;right:150px;top:290px;bottom:420px;display:flex;flex-direction:column;justify-content:center;gap:24px">'
                         f'<div class="kick" style="align-self:flex-start">{esc(s.get("kicker","USTA İPUCU"))}</div>'
                         f'<div class="ltitle">{esc(s["title"])}</div><div style="display:flex;flex-direction:column;gap:22px;margin-top:14px">{li}</div></div>{FOOT}</div>')
        elif t == "outro":
            s.setdefault("dur", 115)
            cta = s.get("cta", "Bilgi için hemen arayın")
            parts.append(f'<div class="sc" data-web="{WEB}" style="background:var(--g)"><canvas width="1080" height="1920"></canvas>'
                         f'<div class="endhalo abs" style="top:500px"></div><img class="endlogo abs" src="{logo}" style="left:50%;top:565px;width:330px;margin-left:-165px">'
                         f'<div class="brand abs" style="top:1000px;font-size:74px;letter-spacing:4px">YÜKSEL TARIM</div><div class="city abs" style="top:1100px;letter-spacing:14px">DENİZLİ</div>'
                         f'<div class="web abs" style="top:1220px"></div>'
                         + (f'<div class="ring abs" style="top:1340px"></div><div class="cta abs" style="top:1340px">{esc(cta)}</div>' if cta else '') + '</div>')
        scenes.append(s); f += s["dur"]
    parts = [x.replace("__FOOT__", foot_html()).replace("__LOGO__", logo) for x in parts]
    doc = (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}'
           f'<div class="wipe2"></div><div class="wipe"></div><script>{JS.replace("__SCENES__", json.dumps(scenes))}</script></body></html>')
    return doc, f

def render(cfg, out_mp4, only=None):
    doc, total = build(cfg)
    frames = only or range(total)
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(doc); pg.wait_for_timeout(600)
        for i, f in enumerate(frames):
            pg.evaluate(f"window.renderFrame({f})"); pg.screenshot(path=str(tmp / f"f{i:05d}.png"))
        b.close()
    if only: return tmp
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out_mp4], check=True)
    shutil.rmtree(tmp); return out_mp4, total / FPS

if __name__ == "__main__":
    cfg = json.loads(pathlib.Path(sys.argv[1]).read_text())
    if len(sys.argv) > 3: print(render(cfg, None, [int(x) for x in sys.argv[3].split(",")]))
    else: print(render(cfg, sys.argv[2]))

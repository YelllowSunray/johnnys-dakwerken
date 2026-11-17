import sys, json
from playwright.sync_api import sync_playwright
PAGES=['/','/diensten/','/diensten/bitumen/','/diensten/kunststof/','/diensten/leien/','/diensten/zinkwerk/','/diensten/isolatie/','/diensten/pannendaken/','/diensten/nieuwbouw-verbouw-renovatie/','/diensten/lekkage-en-reparatie/','/werkwijze/','/over-ons/','/projecten/','/offerte/','/contact/']
STY=['ambachtelijk','nacht','strak']; VW=[(390,844),(768,1024),(1440,900)]
base=sys.argv[1]
sel_p=sys.argv[2:] or PAGES
res=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for st in STY:
        for w,h in VW:
            c=b.new_context(viewport={'width':w,'height':h}); pg=c.new_page()
            for path in sel_p:
                pg.goto(f'{base}{path}?style={st}',wait_until='networkidle'); pg.wait_for_timeout(250)
                r=pg.evaluate("""()=>{const o={};o.hscroll=document.documentElement.scrollWidth>innerWidth+1||document.body.scrollWidth>innerWidth+1;
                 o.small=[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);if(!r.width||!r.height||c.visibility=='hidden'||e.closest('#menu')&&getComputedStyle(document.getElementById('menu')).display=='none')return false;const bg=c.backgroundColor!='rgba(0, 0, 0, 0)';const br=parseFloat(c.borderTopWidth)>0;return (bg||br)&&r.width>60&&r.height<44&&!e.closest('footer')}).map(e=>(e.innerText||'').trim().slice(0,25)+' h='+Math.round(e.getBoundingClientRect().height));
                 o.fonts=[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family+' '+f.style);
                 const hb=document.querySelector('main a.r-btn');o.hero=hb?Math.round(hb.getBoundingClientRect().bottom):null;
                 const im=[...document.querySelectorAll('main img')].find(i=>i.getBoundingClientRect().width>0);if(im){const r=im.getBoundingClientRect();o.imgTop=Math.round(r.top);o.imgVis=Math.round(Math.min(r.bottom,innerHeight)-r.top)}
                 o.h1fam=getComputedStyle(document.querySelector('h1')).fontFamily.slice(0,30);
                 o.clipTxt=[...document.querySelectorAll('main .r-card, main .r-big')].filter(e=>e.scrollWidth>e.clientWidth+1).length;
                 return o}""")
                res.append((st,w,path,r))
            c.close()
    b.close()
bad=0
for st,w,path,r in res:
    flag=[]
    if r['hscroll']: flag.append('HSCROLL')
    if r['small']: flag.append('SMALL:'+str(r['small']))
    if r['clipTxt']: flag.append('CLIPW')
    if w==390 and 'imgTop' in r and r['imgVis']<220 and path in ('/','/diensten/bitumen/','/diensten/leien/','/diensten/zinkwerk/','/diensten/kunststof/','/diensten/pannendaken/'): flag.append('PHOTO<220:'+str(r['imgVis']))
    if flag: bad+=1; print(st,w,path,flag)
print('checked',len(res),'issues',bad)
json.dump(res,open('/tmp/shots2.json','w'))

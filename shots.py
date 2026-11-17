import sys
from playwright.sync_api import sync_playwright
from PIL import Image
pages=sys.argv[1:]
def scroll(pg):
    h=pg.evaluate('document.body.scrollHeight')
    for y in range(0,h,500): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(60)
    pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(500)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for pg in pages:
        n=pg.strip('/').replace('/','_') or 'home'
        m=b.new_page(viewport={'width':390,'height':844}); m.goto('http://localhost:4173'+pg,wait_until='networkidle')
        scroll(m)
        m.screenshot(path=f'/tmp/s_{n}_m.png',full_page=True); m.screenshot(path=f'/tmp/s_{n}_mh.png')
        d=b.new_page(viewport={'width':1440,'height':900}); d.goto('http://localhost:4173'+pg,wait_until='networkidle')
        scroll(d)
        d.screenshot(path=f'/tmp/s_{n}_d.png',full_page=True)
        a=Image.open(f'/tmp/s_{n}_d.png'); a.thumbnail((1000,3000))
        c=Image.open(f'/tmp/s_{n}_m.png'); 
        h=max(a.height,c.height)
        W=Image.new('RGB',(1000+20+390,min(h,3200)),'white'); W.paste(a,(0,0)); W.paste(c,(1020,0)); W.save(f'/tmp/s_{n}.png')
        print(n,a.height,c.height)
    b.close()

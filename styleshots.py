import sys
from playwright.sync_api import sync_playwright
from PIL import Image
path=sys.argv[1] if len(sys.argv)>1 else '/'
tag=sys.argv[2] if len(sys.argv)>2 else 'home'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for st in ['ambachtelijk','nacht','strak']:
        for w,h in [(390,844),(1440,900)]:
            pg=b.new_page(viewport={'width':w,'height':h}); pg.goto(f'http://localhost:4173{path}?style={st}',wait_until='networkidle'); pg.wait_for_timeout(400)
            pg.screenshot(path=f'/tmp/st_{tag}_{st}_{w}.png')
            pg.screenshot(path=f'/tmp/stf_{tag}_{st}_{w}.png',full_page=True)
    b.close()
for kind in ['st']:
    for w in (390,1440):
        ims=[Image.open(f'/tmp/st_{tag}_{s}_{w}.png') for s in ['ambachtelijk','nacht','strak']]
        W=Image.new('RGB',(sum(i.width for i in ims)+40,ims[0].height),'white'); x=0
        for i in ims: W.paste(i,(x,0)); x+=i.width+20
        W.save(f'/tmp/cmp_{tag}_{w}.png')

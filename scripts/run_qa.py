# usage: run_qa.py URL -> /opt/cursor/artifacts/qa3_<slug>_{390,1440,menu,sheet}.png
import os
import sys
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = "/opt/cursor/artifacts"
os.makedirs(OUT, exist_ok=True)
u = sys.argv[1]
n = u.split("//")[1].split(".")[0].replace(":", "_")
P = os.path.join(OUT, f"qa3_{n}")

with sync_playwright() as p:
    b = p.chromium.launch(
        executable_path="/usr/bin/google-chrome",
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    m = b.new_page(viewport={"width": 390, "height": 844})
    m.goto(u, wait_until="networkidle", timeout=60000)
    m.screenshot(path=P + "_390.png", full_page=True)
    bad = m.evaluate(
        """()=>[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);if(!r.width||!r.height||c.visibility=='hidden')return false;const bg=c.backgroundColor!='rgba(0, 0, 0, 0)'&&c.backgroundColor!='transparent';const br=parseFloat(c.borderTopWidth)>0;return (bg||br)&&r.width>60&&r.height<40&&!e.closest('nav,header,footer')}).map(e=>(e.innerText||'').trim().slice(0,30)+' h='+Math.round(e.getBoundingClientRect().height))"""
    )
    print("BUTTON_FAIL" if bad else "BUTTONS_OK", bad)
    for sel in ['button[aria-label*="enu" i]', "button[aria-controls]", "header button"]:
        try:
            m.locator(sel).first.click(timeout=3000)
            break
        except Exception:
            pass
    m.wait_for_timeout(700)
    m.screenshot(path=P + "_menu.png")
    d = b.new_page(viewport={"width": 1440, "height": 900})
    d.goto(u, wait_until="networkidle", timeout=60000)
    d.screenshot(path=P + "_1440.png", full_page=True)
    print(n, d.title())
    b.close()

a = Image.open(P + "_1440.png")
a = a.crop((0, 0, 1440, min(a.height, 2700)))
a.thumbnail((900, 2000))
c = Image.open(P + "_390.png")
c = c.crop((0, 0, 390, min(c.height, 2000)))
e = Image.open(P + "_menu.png")
W = Image.new("RGB", (900 + 20 + 390 + 20 + 390, max(a.height, c.height)), "white")
W.paste(a, (0, 0))
W.paste(c, (920, 0))
W.paste(e, (1330, 0))
W.save(P + "_sheet.png")
print(P + "_sheet.png")
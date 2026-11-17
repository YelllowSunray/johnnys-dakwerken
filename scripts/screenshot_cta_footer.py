#!/usr/bin/env python3
"""Crop screenshots: CTA block through footer top."""
import os, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:43129"
OUT = "/opt/cursor/artifacts/screenshots/cta-footer"
PAGES = [("/", "home"), ("/diensten/bitumen/", "bitumen"), ("/diensten/leien/", "leien")]
STYLES = ["nacht", "strak", "ambachtelijk"]
WIDTHS = [(393, "393"), (1440, "1440")]

os.makedirs(OUT, exist_ok=True)


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for path, slug in PAGES:
            for style in STYLES:
                for w, wtag in WIDTHS:
                    ctx = browser.new_context(viewport={"width": w, "height": 900})
                    page = ctx.new_page()
                    q = "?style=" + style if style != "nacht" else ""
                    if style == "nacht" and "?" not in q:
                        url = BASE.rstrip("/") + path + q
                    else:
                        url = BASE.rstrip("/") + path + ("?style=" + style if style != "nacht" else "")
                    page.goto(url, wait_until="networkidle")
                    page.evaluate(
                        """() => {
                        const cta = document.querySelector('.cta-end');
                        const foot = document.querySelector('footer.site-f');
                        if (!cta || !foot) return {ok:false};
                        const r1 = cta.getBoundingClientRect();
                        const r2 = foot.getBoundingClientRect();
                        return {ok:true, y: Math.max(0, r1.top - 40), h: Math.min(520, r2.top - r1.top + 80)};
                    }"""
                    )
                    box = page.evaluate(
                        """() => {
                        const cta = document.querySelector('.cta-end');
                        const foot = document.querySelector('footer.site-f');
                        const r1 = cta.getBoundingClientRect();
                        const r2 = foot.getBoundingClientRect();
                        return {x:0, y: Math.max(0, r1.top - 32), width: document.documentElement.clientWidth,
                                height: Math.min(480, Math.max(120, r2.top - r1.top + 48))};
                    }"""
                    )
                    fn = f"{slug}_{style}_{wtag}_cta_to_footer.png"
                    page.screenshot(path=os.path.join(OUT, fn), clip=box)
                    full = f"{slug}_{style}_{wtag}_page_bottom.png"
                    h = page.evaluate(
                        "() => { const f=document.querySelector('footer.site-f'); return f ? f.getBoundingClientRect().top + 120 : 800; }"
                    )
                    page.evaluate("y => window.scrollTo(0, Math.max(0, y - 400))", h - 200)
                    page.screenshot(path=os.path.join(OUT, full))
                    ctx.close()
        browser.close()
    print("Wrote", OUT)


if __name__ == "__main__":
    run()
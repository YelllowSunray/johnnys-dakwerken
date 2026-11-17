#!/usr/bin/env python3
"""Mobile hero + QA sheet screenshots for delivery."""
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:43129"
ART = "/opt/cursor/artifacts"
os.makedirs(ART, exist_ok=True)

STYLES = [
    ("strak", ""),
    ("nacht", "?style=nacht"),
    ("ambachtelijk", "?style=ambachtelijk"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, qs in STYLES:
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(BASE + "/" + qs, wait_until="networkidle", timeout=90000)
        page.screenshot(path=os.path.join(ART, f"home-hero-{name}-390.png"))
        ctx.close()

    for name, qs in STYLES:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(BASE + "/" + qs, wait_until="networkidle", timeout=90000)
        page.screenshot(path=os.path.join(ART, f"home-hero-{name}-1440.png"))
        ctx.close()

    # Sticky nav scroll check
    for w in (390, 1440):
        ctx = browser.new_context(viewport={"width": w, "height": 844 if w == 390 else 900})
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="networkidle", timeout=90000)
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(300)
        box = page.locator("header.site-h").bounding_box()
        print(f"header_y@{w}:", box["y"] if box else None)
        ctx.close()

    browser.close()
print("screenshots in", ART)
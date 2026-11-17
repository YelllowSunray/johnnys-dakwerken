#!/usr/bin/env python3
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:43129"
OUT = "/opt/cursor/artifacts/screenshots/mobile"
PAGES = [
    ("/", "home"),
    ("/diensten/", "diensten"),
    ("/over-ons/", "over-ons"),
    ("/projecten/", "projecten"),
    ("/werkwijze/", "werkwijze"),
    ("/contact/", "contact"),
]
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    for path, slug in PAGES:
        ctx = b.new_context(viewport={"width": 393, "height": 852})
        page = ctx.new_page()
        page.goto(BASE + path, wait_until="networkidle", timeout=90000)
        page.screenshot(path=os.path.join(OUT, f"{slug}_nacht_393_full.png"), full_page=True)
        ctx.close()
    b.close()
print("saved", OUT)
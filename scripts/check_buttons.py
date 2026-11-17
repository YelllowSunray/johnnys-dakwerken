#!/usr/bin/env python3
"""Smoke-test internal links and key CTAs on every page."""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:43129/"
PAGES = [
    "/",
    "/diensten/",
    "/werkwijze/",
    "/over-ons/",
    "/projecten/",
    "/offerte/",
    "/contact/",
    "/diensten/bitumen/",
    "/diensten/leien/",
]

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    err = []
    for path in PAGES:
        page.goto(BASE.rstrip("/") + path, wait_until="networkidle", timeout=60000)
        for sel, name in [
            ('a[href="/offerte/"]', "offerte"),
            ('a[href="tel:+31641723759"]', "tel"),
            ('a[href="mailto:info@johnnydakwerken.nl"]', "mail"),
        ]:
            if page.locator(sel).count() == 0:
                err.append(f"{path}: missing {name}")
    b.close()

if err:
    print("CHECK_FAIL", err)
    sys.exit(1)
print("CHECK_OK all pages have offerte, tel, mail links")
#!/usr/bin/env python3
"""Mobile edge audit: 16 pages x 3 styles @ 393px."""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "REPORT.md")
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:43129"
MIN_LEFT = 14
MIN_RIGHT_PAD = 8

PAGES = [
    "/",
    "/diensten/",
    "/werkwijze/",
    "/over-ons/",
    "/projecten/",
    "/contact/",
    "/offerte/",
    "/diensten/bitumen/",
    "/diensten/kunststof/",
    "/diensten/leien/",
    "/diensten/shingles/",
    "/diensten/zinkwerk/",
    "/diensten/isolatie/",
    "/diensten/pannendaken/",
    "/diensten/nieuwbouw-verbouw-renovatie/",
    "/diensten/lekkage-en-reparatie/",
]
STYLES = ["nacht", "strak", "ambachtelijk"]


def audit(page, path, style):
    q = f"?style={style}" if style != "nacht" else ""
    page.goto(BASE.rstrip("/") + path + q, wait_until="networkidle", timeout=90000)
    return page.evaluate(
        """([minLeft, minRightPad]) => {
      const iw = window.innerWidth;
      const sw = document.documentElement.scrollWidth;
      const sel = 'main h1,main h2,main h3,main p,main a,main button,main li,main label,main dt,main dd';
      const items = [...document.querySelectorAll(sel)].filter(el => {
        if (!el.closest('main')) return false;
        const r = el.getBoundingClientRect();
        const st = getComputedStyle(el);
        if (r.width < 2 || r.height < 2) return false;
        if (st.visibility === 'hidden' || st.display === 'none' || st.opacity === '0') return false;
        const t = (el.innerText || el.textContent || '').trim();
        if ((el.tagName === 'A' || el.tagName === 'BUTTON') && !t && !el.querySelector('svg')) return false;
        if (el.getAttribute('aria-hidden') === 'true') return false;
        return true;
      });
      let worstL = minLeft;
      let worstR = iw - minRightPad;
      let offender = '';
      for (const el of items) {
        const r = el.getBoundingClientRect();
        if (r.left < worstL) {
          worstL = r.left;
          offender = 'L:' + (el.innerText || el.tagName).slice(0, 36) + '=' + Math.round(r.left);
        }
        if (r.right > worstR) {
          worstR = r.right;
          offender = 'R:' + (el.innerText || el.tagName).slice(0, 36) + '=' + Math.round(r.right);
        }
      }
      const overflow = sw > iw + 1;
      const ok = worstL >= minLeft && worstR <= iw - minRightPad && !overflow;
      return {
        ok,
        minLeft: Math.round(worstL * 10) / 10,
        maxRight: Math.round(worstR * 10) / 10,
        innerWidth: iw,
        scrollWidth: sw,
        overflow,
        offender,
        n: items.length,
      };
    }""",
        [MIN_LEFT, MIN_RIGHT_PAD],
    )


def main():
    rows = []
    fails = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for path in PAGES:
            for style in STYLES:
                ctx = browser.new_context(viewport={"width": 393, "height": 852}, device_scale_factor=1)
                page = ctx.new_page()
                r = audit(page, path, style)
                ok = r.get("ok")
                status = "PASS" if ok else "FAIL"
                if not ok:
                    fails += 1
                rows.append(
                    f"| {path} | {style} | {status} | {r.get('minLeft')} | {r.get('maxRight')} | "
                    f"{r.get('scrollWidth')} | {r.get('innerWidth')} | {r.get('offender', '')} |"
                )
                ctx.close()
        browser.close()

    block = "\n".join(
        [
            "## Mobile edge audit (393×852)",
            "",
            f"Criteria: visible `main` typography/controls `left ≥ {MIN_LEFT}px`, `right ≤ innerWidth−{MIN_RIGHT_PAD}`, `scrollWidth ≤ innerWidth`.",
            "",
            "| Page | Style | Status | min left | max right | scrollW | innerW | Offender |",
            "|------|-------|--------|----------|-----------|---------|--------|----------|",
            *rows,
            "",
            f"**Summary:** {len(rows) - fails}/{len(rows)} PASS, {fails} FAIL",
            "",
        ]
    )

    text = open(REPORT, encoding="utf-8").read() if os.path.isfile(REPORT) else ""
    mark = "## Mobile edge audit (393×852)"
    if mark in text:
        pre, _, post = text.partition(mark)
        if "\n## " in post:
            post = post[post.index("\n## ") :]
        else:
            post = ""
        text = pre.rstrip() + "\n\n" + block + post.lstrip("\n")
    else:
        text = (text.rstrip() + "\n\n" + block) if text else block
    open(REPORT, "w", encoding="utf-8").write(text)

    for line in rows:
        if "| FAIL |" in line:
            print(line)
    print(f"Mobile edge: {fails} FAIL / {len(rows)}")
    return fails


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Verify hero insets and horizontal overflow across pages/styles/viewports."""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "REPORT.md")
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:43129"

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
WIDTHS = [(393, "393"), (1440, "1440")]
MIN_LEFT = 16


def audit(page, path, style, width):
    q = f"?style={style}" if style != "nacht" else ""
    page.goto(BASE.rstrip("/") + path + q, wait_until="networkidle", timeout=60000)
    return page.evaluate(
        """(minLeft) => {
      const sw = document.documentElement.scrollWidth;
      const cw = document.documentElement.clientWidth;
      const hero = document.querySelector('main > section:first-child');
      if (!hero) return {ok: false, reason: 'no hero', scrollWidth: sw, clientWidth: cw};
      const sel = 'h1,h2,h3,p,a,button,.hero-cta a,label';
      const items = [...hero.querySelectorAll(sel)].filter(el => {
        const r = el.getBoundingClientRect();
        const st = getComputedStyle(el);
        if (r.width < 2 || r.height < 2) return false;
        if (st.visibility === 'hidden' || st.display === 'none') return false;
        const t = (el.innerText || el.textContent || '').trim();
        if (el.tagName === 'A' && !t && !el.querySelector('svg')) return false;
        return true;
      });
      let worst = minLeft;
      let offender = '';
      for (const el of items) {
        const l = el.getBoundingClientRect().left;
        if (l < worst) { worst = l; offender = (el.innerText || el.tagName).slice(0, 40); }
      }
      const overflow = sw > cw + 1;
      return {
        ok: worst >= minLeft && !overflow,
        minLeft: Math.round(worst * 10) / 10,
        offender,
        scrollWidth: sw,
        clientWidth: cw,
        overflow,
        checked: items.length,
      };
    }""",
        MIN_LEFT,
    )


def main():
    rows = []
    fails = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for path in PAGES:
            for style in STYLES:
                for w, wtag in WIDTHS:
                    ctx = browser.new_context(viewport={"width": w, "height": 852 if w < 500 else 900})
                    page = ctx.new_page()
                    r = audit(page, path, style, w)
                    status = "PASS" if r.get("ok") else "FAIL"
                    if status == "FAIL":
                        fails += 1
                    rows.append(
                        f"| {path} | {style} | {wtag} | {status} | {r.get('minLeft', '—')} | "
                        f"{r.get('scrollWidth', '—')} | {r.get('clientWidth', '—')} | {r.get('offender', r.get('reason', ''))} |"
                    )
                    ctx.close()
        browser.close()

    block = [
        "## Hero padding & overflow audit",
        "",
        f"Automated check: first `main > section` hero, min text/button `left` ≥ {MIN_LEFT}px, `scrollWidth ≤ clientWidth`.",
        "",
        "| Page | Style | Width | Status | min left (px) | scrollW | clientW | Worst offender |",
        "|------|-------|-------|--------|---------------|---------|---------|----------------|",
        *rows,
        "",
        f"**Summary:** {len(rows) - fails}/{len(rows)} PASS, {fails} FAIL",
        "",
    ]

    if os.path.isfile(REPORT):
        text = open(REPORT, encoding="utf-8").read()
        if "## Hero padding & overflow audit" in text:
            a, _, c = text.partition("## Hero padding & overflow audit")
            # drop old block until next ## or EOF
            rest = c
            if "\n## " in rest:
                rest = rest[rest.index("\n## ") :]
            else:
                rest = ""
            text = a.rstrip() + "\n\n" + "\n".join(block) + rest.lstrip("\n")
        else:
            text = text.rstrip() + "\n\n" + "\n".join(block)
        open(REPORT, "w", encoding="utf-8").write(text)
    else:
        open(REPORT, "w", encoding="utf-8").write("\n".join(block))

    for line in rows:
        if "| FAIL |" in line:
            print(line)
    print(f"Done: {fails} failures / {len(rows)} checks")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
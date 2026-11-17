#!/usr/bin/env python3
"""Flag main images rendered >1.2× natural dimensions."""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "REPORT.md")
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:43129"
THRESH = 1.2

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


def audit_page(page, path):
    page.goto(BASE.rstrip("/") + path, wait_until="networkidle", timeout=90000)
    return page.evaluate(
        """(thresh) => {
      const imgs = [...document.querySelectorAll('main img')].filter(img => {
        const r = img.getBoundingClientRect();
        return r.width >= 40 && r.height >= 40 && img.naturalWidth > 0;
      });
      const out = [];
      for (const img of imgs) {
        const nw = img.naturalWidth, nh = img.naturalHeight;
        const rw = img.clientWidth, rh = img.clientHeight;
        const sx = rw / nw, sy = rh / nh;
        const scale = Math.max(sx, sy);
        if (scale > thresh) {
          out.push({
            src: img.currentSrc || img.src,
            alt: (img.alt || '').slice(0, 60),
            natural: nw + '×' + nh,
            rendered: Math.round(rw) + '×' + Math.round(rh),
            scale: Math.round(scale * 100) / 100,
            role: img.closest('.hero-ph-in') ? 'hero' : img.closest('.dcard-media') ? 'card' : img.closest('.over-photo') ? 'over' : 'main',
          });
        }
      }
      return out;
    }""",
        THRESH,
    )


def main():
    rows = []
    by_src = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        for path in PAGES:
            for vp in [(1440, 900), (393, 852)]:
                page.set_viewport_size({"width": vp[0], "height": vp[1]})
                for hit in audit_page(page, path):
                    key = (hit["src"], vp[0], path)
                    if key not in by_src:
                        by_src[key] = hit
                        rows.append(
                            f"| {path} | {vp[0]} | {hit['role']} | `{hit['src'].split('/')[-1]}` | {hit['natural']} | {hit['rendered']} | **{hit['scale']}×** |"
                        )
        ctx.close()
        browser.close()

    block = "\n".join(
        [
            "## Image upscale audit (rendered > 1.2× natural)",
            "",
            f"Checked {len(PAGES)} pages at 1440px and 393px viewports.",
            "",
            "| Page | Viewport | Role | File | Natural | Rendered | Scale |",
            "|------|----------|------|------|---------|----------|-------|",
            *(rows if rows else ["| — | — | — | — | — | — | *none* |"]),
            "",
        ]
    )

    text = open(REPORT, encoding="utf-8").read() if os.path.isfile(REPORT) else ""
    mark = "## Image upscale audit (rendered > 1.2× natural)"
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
    print(f"upscale hits: {len(rows)}")
    for r in rows:
        print(r)
    return len(rows)


if __name__ == "__main__":
    raise SystemExit(main())
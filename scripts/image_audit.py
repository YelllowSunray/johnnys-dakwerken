#!/usr/bin/env python3
"""Per-page image inventory from built dist HTML."""
import os, re, html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
REPORT = os.path.join(ROOT, "REPORT.md")

# shingles.jpg removed from site; must never ship in dist
BANNED = {"/img/shingles.jpg"}


def page_path(fp):
    rel = os.path.relpath(fp, DIST).replace("\\", "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def imgs_on_page(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    found = []
    for src, alt in re.findall(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', text):
        if src.startswith("/img") or src.startswith("/video"):
            found.append((src, alt))
    for src in re.findall(r'<video[^>]+poster="([^"]+)"', text):
        found.append((src, "video poster"))
    for src in re.findall(r'src="(/video/[^"]+)"', text):
        if "poster" not in src:
            found.append((src, "video"))
    return found


def main():
    by_page = {}
    for dp, _, files in os.walk(DIST):
        for f in files:
            if f != "index.html" and f != "404.html":
                continue
            fp = os.path.join(dp, f)
            pg = page_path(fp) if f == "index.html" else "/404"
            by_page[pg] = imgs_on_page(fp)

    lines = [
        "# Johnny's Dakwerken — delivery report",
        "",
        "## Image placement rules",
        "- `shingles.jpg` is **not used** anywhere (removed).",
        "- `shingles-dak.jpg` only on **cards** (home, `/diensten/`, related grids) — not on `/diensten/shingles/` hero (text-only).",
        "- **Werk van Johnny** galleries: Johnny's own `werk/*` photos only.",
        "- Bitumen/zink video only on bitumen and zinkwerk pages.",
        "- Each gallery shows only that dienst's photos; otherwise a link to `/projecten/`.",
        "",
        "## Per-page images",
        "",
    ]
    for pg in sorted(by_page.keys(), key=lambda p: (p.count("/"), p)):
        lines.append(f"### `{pg}`")
        lines.append("")
        lines.append("| File | Alt |")
        lines.append("|------|-----|")
        seen = set()
        for src, alt in by_page[pg]:
            if src in seen:
                continue
            seen.add(src)
            flag = ""
            if src in BANNED:
                flag = " **BANNED**"
            lines.append(f"| `{src}` | {htmlmod.escape(alt[:80])}{flag} |")
        lines.append("")

    lines += [
        "## Leien source",
        "- https://commons.wikimedia.org/wiki/File:Roof_slates_Eiktunet.jpg (CC0)",
        "",
    ]
    open(REPORT, "w", encoding="utf-8").write("\n".join(lines))
    violations = sum(1 for pg, imgs in by_page.items() for src, _ in imgs if src in BANNED)
    print("REPORT written;", violations, "banned image hits")


if __name__ == "__main__":
    main()
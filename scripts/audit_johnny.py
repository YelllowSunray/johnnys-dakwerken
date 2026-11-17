#!/usr/bin/env python3
"""Audit dist HTML for bare 'Johnny' (not Johnny's / Johnny&#x27;s)."""
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "dist"
# After entity decode: Johnny's counts as brand; bare Johnny flagged unless allowed
ALLOW_PATTERNS = [
    r"Johnny's Dakwerken",
    r"Johnny's",
    r"Johnny van Ophuizen",
    r"Over Johnny",
    r"Meer over Johnny",
    r"Ik ben Johnny",
    r"Geboren en getogen",
    r"©\s*2026 Johnny van Ophuizen",
    r"Maak kennis met Johnny van Ophuizen",
    r"Over Johnny van Ophuizen",
]

def decode(s: str) -> str:
    return html.unescape(s.replace("&#x27;", "'").replace("&#39;", "'"))

def find_bare_johnny(text: str):
    dec = decode(text)
    out = []
    for m in re.finditer(r"(?<![\w/])Johnny(?![\w'’])", dec):
        start = max(0, m.start() - 40)
        end = min(len(dec), m.end() + 50)
        snippet = dec[start:end].replace("\n", " ")
        # skip if part of allowed phrase in local window
        window = dec[max(0, m.start() - 80) : m.end() + 80]
        if any(re.search(p, window) for p in ALLOW_PATTERNS):
            continue
        if "johnnydakwerken" in window.lower():
            continue
        out.append(snippet)
    return out

def main():
    flagged = []
    allowed_hits = {}
    for path in sorted(ROOT.rglob("*.html")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        dec = decode(raw)
        for pat, label in [
            (r"Ik ben Johnny van Ophuizen", "Home quote (first person)"),
            (r"Over Johnny", "Nav/section label"),
            (r"Meer over Johnny", "Home teaser CTA"),
            (r"Johnny van Ophuizen", "Bio name / copyright / postadres / SEO over-ons"),
            (r"Geboren en getogen in Deventer", "Bio tagline"),
            (r"©\s*2026 Johnny van Ophuizen", "Footer copyright"),
            (r"Johnny's Dakwerken", "Brand name"),
        ]:
            if re.search(pat, dec):
                allowed_hits.setdefault(label, []).append(str(path.relative_to(ROOT)))
        for sn in find_bare_johnny(raw):
            flagged.append((str(path.relative_to(ROOT)), sn))
    print("FLAGGED", len(flagged))
    for p, sn in flagged:
        print(f"  {p}: …{sn}…")
    print("\nALLOWED_CATEGORIES")
    for label, files in sorted(allowed_hits.items()):
        print(f"  {label}: {len(set(files))} page(s)")

if __name__ == "__main__":
    main()
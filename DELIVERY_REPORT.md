# Delivery report — Company voice (t1566 / t1567)

Client feedback: marketing copy should speak as **Johnny's Dakwerken** / **wij**, not as if Johnny alone always visits the site — colleagues also inspect roofs.

## Scope
- Rewrote personal-action phrasing across `src/data.py`, `src/build.py`, and all generated pages: heroes, diensten copy, werkwijze stappen, CTAs, gallery captions, meta/OG descriptions, JSON-LD org name, form intro, 404.
- Patterns updated include: *komt / bekijkt / adviseert / legt / verzorgt / werkt / pakt aan*, *Bel Johnny*, *Werk van Johnny*, *Zo werkt Johnny*, *Waarom Johnny*, *Materialen waarmee Johnny werkt*, *Neem contact op met Johnny*, photo alts implying Johnny personally, etc.

## Unchanged (per brief)
| Item | Location |
|------|----------|
| **Over Johnny** nav label + `/over-ons/` page title block | `src/build.py` nav + over-ons hero |
| Home **Over Johnny** section + first-person quote (*Ik ben Johnny van Ophuizen…*) | Home body |
| **Meer over Johnny** teaser CTA | Home |
| **Geboren en getogen in Deventer** | Over ons |
| Footer **© 2026 Johnny van Ophuizen** | Footer all pages |
| Brand **Johnny's Dakwerken** (logo alt, titles, JSON-LD) | Site-wide |
| Layout, styles, contact flow (no WhatsApp), `vercel.json` build/install/output | — |

## QA — remaining `Johnny` in `dist/` (not followed by `'s` / `&#x27;s`)

Automated audit: `python3 scripts/audit_johnny.py` on built HTML → **FLAGGED: 0** bare personal `Johnny` outside allowed contexts.

Manual `rg` on `dist/**/*.html` for *Johnny komt*, *Bel Johnny*, *Zo werkt Johnny* (without company name), etc. → **no matches**.

| Remaining mention | Reason allowed |
|-------------------|----------------|
| `Johnny's Dakwerken` / `Johnny&#x27;s Dakwerken` | Brand / SEO / org JSON-LD |
| `Over Johnny` | Nav + over-ons kicker (explicitly kept) |
| `Meer over Johnny` | Home teaser CTA (explicitly kept) |
| `Johnny van Ophuizen` | Bio h1, postadres, copyright, over-ons SEO, home quote attribution, portrait `alt` |
| `Ik ben Johnny van Ophuizen…` | First-person quote on home (explicitly kept) |
| `Geboren en getogen in Deventer` | Bio tagline on over-ons |
| `© 2026 Johnny van Ophuizen` | Footer copyright (all pages) |
| `Maak kennis met Johnny van Ophuizen` | Over-ons meta description only |

URLs/domain `johnnydakwerken.nl` are not personal-name copy.

## Other QA
| Check | Result |
|-------|--------|
| `rg -i 'wa\.me\|whatsapp' dist/` | No matches |
| `scripts/run_qa.py` @ `http://127.0.0.1:43187/` (strak) | BUTTONS_OK |
| `?style=nacht` | BUTTONS_OK |
| `?style=ambachtelijk` | BUTTONS_OK |

## Build
`python3 src/build.py` (Tailwind via `npm install` per `vercel.json`).

## Artifacts
- `/opt/cursor/artifacts/dist.zip`
- `/opt/cursor/artifacts/source.tgz`
- `/opt/cursor/artifacts/DELIVERY_REPORT.md`

**Not deployed.**
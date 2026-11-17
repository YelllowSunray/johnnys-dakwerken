# Delivery report — Werkgebied heel Nederland + source bundle

## Content (Samir Nov 17)
Johnny works **door heel Nederland**; **Deventer = vestiging**, not service boundary.

| Area | Change |
|------|--------|
| Home hero kicker | `Dakdekker in heel Nederland` |
| Home H1 | `Uw dak, weer jarenlang waterdicht` (no city in headline) |
| Navbar | `Dakdekker · Heel Nederland` (all styles via `.brand-tag`) |
| Trust stats | `NL` / `Heel Nederland · vanuit Deventer` |
| Werkgebied section | **Actief in heel Nederland, vanuit Deventer** (new on home) |
| Footer | Actief in heel Nederland, vanuit Deventer |
| Meta / page titles | Deventer removed from service-area SEO; `vanuit Deventer` where base is relevant |
| Dienst pages | `TITLES` + pannendaken H2 updated |
| Unchanged on purpose | Deventer skyline hero imagery + alt text; “Geboren en getogen in Deventer” (bio) |

## QA (`scripts/run_qa.py`)
| URL | Result |
|-----|--------|
| `/` (strak default) | BUTTONS_OK |
| `?style=nacht` | BUTTONS_OK |
| `?style=ambachtelijk` | BUTTONS_OK |

Sticky nav after scroll: `header y = 0` @ 390 and 1440.

## Artifacts (`/opt/cursor/artifacts/`)
- `dist.zip` — deployable build
- `source.tgz` — full editable project (`src/`, `public/`, configs, README; **excludes** `dist/`, `node_modules/`)
- `DELIVERY_REPORT.md`
- Mobile heroes: `home-hero-{strak,nacht,ambachtelijk}-390.png`, `home-hero-strak-1440.png`
- QA: `qa3_strak_127_sheet.png`, `qa3_nacht_127_sheet.png`, `qa3_ambachtelijk_127_sheet.png` (+ component PNGs)

## Local repo
- `.gitignore` ignores `dist/` and `node_modules/`
- README: build (`python3 src/build.py` → `dist/`) + Vercel project **johnnydakwerken**

**Not deployed** (per client request).
# Delivery report — WhatsApp removed, e-mail + offerte CTAs

## Changes (Samir Nov 17, t1563/t1564)
Johnny requested **no WhatsApp** anywhere on the site.

| Area | New behaviour |
|------|----------------|
| All heroes | Primary **Offerte aanvragen** → `/offerte/`; secondary **Bel** → `tel:+31641723759` |
| CTA bands (dark) | **Offerte**, **Bel**, **E-mail** |
| Mobile menu | Offerte CTA + **Bel** + **Info@johnnydakwerken.nl** (no WhatsApp) |
| Footer / contact / offerte | **Info@johnnydakwerken.nl** (`mailto:info@johnnydakwerken.nl`) |
| Offerte form | Submit opens **mailto** with prefilled body (no wa.me) |
| JSON-LD | `RoofingContractor` on every page: phone + `info@johnnydakwerken.nl` |
| CSS | Removed all `.btn-wa` / WhatsApp styling |

Werkgebied and visual styles unchanged.

## QA verification
```bash
rg -i 'wa\.me|whatsapp' dist/   # no matches
```
Result: **GREP_OK**

| Check | Result |
|-------|--------|
| `scripts/run_qa.py` `/`, `?style=nacht`, `?style=ambachtelijk` | BUTTONS_OK |
| `scripts/check_buttons.py` | CHECK_OK (offerte, tel, mail on sample pages) |

## Hero screenshots (`/opt/cursor/artifacts/`)
`home-hero-{strak,nacht,ambachtelijk}-{390,1440}.png`

## Artifacts
- `dist.zip`
- `source.tgz` (excludes `dist/`, `node_modules/`; includes `public/vercel.json`, `src/`, configs, README)
- `DELIVERY_REPORT.md`

**Not deployed.**
# Delivery report — Mobile hero Offerte label (t1565)

## Change
On viewports **below 640px**, hero primary button shows **Offerte →** (short label + arrow). From **640px** up: **Offerte aanvragen**.

- Hero row: two equal-width buttons, **48px** height, **≥16px** horizontal padding.
- Removed stray **box-shadow** offset (Strak lime offset block) on hero buttons on mobile — `box-shadow: none !important` on `.hero-cta > a`.
- Applies everywhere `hero_cta()` is used (home, diensten, all dienst heroes).

## vercel.json (repo root + `public/`)
`buildCommand`: `python3 src/build.py` · `installCommand`: `npm install` · `outputDirectory`: `dist` · existing `trailingSlash` + `/fotos/` redirect retained.

## QA
| Check | Result |
|-------|--------|
| `rg -i 'wa\.me\|whatsapp' dist/` | no matches |
| `run_qa.py` strak / nacht / ambachtelijk | BUTTONS_OK |
| Mobile hero short label (390px) | Offerte → verified × 3 styles |

## Artifacts
- `/opt/cursor/artifacts/dist.zip`
- `/opt/cursor/artifacts/source.tgz`
- `/opt/cursor/artifacts/DELIVERY_REPORT.md`
- `/opt/cursor/artifacts/home-hero-{strak,nacht,ambachtelijk}-390.png`

**Not deployed.**
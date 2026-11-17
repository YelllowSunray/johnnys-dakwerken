# Delivery report — Hero materials list (t1573)

Client: pannendak en zink moeten ook in de hero- en samenvattingsregels.

## Changes (`src/build.py`)
| Location | Update |
|----------|--------|
| Home hero (mobile, &lt;1024px) | Bitumen, kunststof, leien, **pannendaken** en **zinkwerk**. … |
| Home hero (desktop) | … leien, **pannendaken**, **zinkwerk** en boeibekleding. … |
| Home `<title>` / OG title | … leien, **pannendaken en zinkwerk** |
| Home meta description | Already listed pannendaken + zinkwerk (unchanged) |
| Footer blurb | … leien, **pannendaken**, **zinkwerk** en boeibekleding … |
| “Waarom” card (20 jaar) | … leien, **pannendaken en zinkwerk** |
| Diensten “Materialen waarmee wij werken” | Added **Pannendaken**; **Zink** → **Zinkwerk** |

No layout/CSS/`vercel.json` changes.

## QA
| Check | Result |
|-------|--------|
| Mobile hero intro line count @ 390px (strak) | **3 lines** |
| `scripts/run_qa.py` strak / nacht / ambachtelijk | BUTTONS_OK × 3 |
| `rg -i 'wa.me\|whatsapp' dist/` | No matches |

## Artifacts
- `/opt/cursor/artifacts/dist.zip`
- `/opt/cursor/artifacts/source.tgz`
- `/opt/cursor/artifacts/DELIVERY_REPORT.md`
- `/opt/cursor/artifacts/home-hero-strak-390.png`

**Not deployed.**
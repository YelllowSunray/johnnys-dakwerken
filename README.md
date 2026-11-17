# Johnny's Dakwerken

Static marketing site for Johnny van Ophuizen — dakdekker actief in heel Nederland, vanuit Deventer. Built with Python (`src/build.py`), Tailwind CSS v4, and assets in `public/`.

## Build locally

```bash
cd /path/to/repo
npm install
python3 src/build.py
```

Output is written to `dist/`.

Preview:

```bash
python3 -m http.server 43129 --directory dist
```

Open [http://127.0.0.1:43129/](http://127.0.0.1:43129/). Use `?style=nacht` or `?style=ambachtelijk`; default is **strak**.

## Deploy to Vercel

Link the Vercel project **johnnydakwerken** (or create it) and deploy the built `dist/` folder as static files:

```bash
python3 src/build.py
cd dist
npx vercel deploy --prod
```

Or connect the GitHub repo in the Vercel dashboard, set the build command to `python3 src/build.py` (and `npm install` if needed for Tailwind), and set the output directory to `dist`.

## QA

```bash
python3 /path/to/johnny_pack/qa.py http://127.0.0.1:43129/
```

Must print `BUTTONS_OK` for `/`, `?style=nacht`, and `?style=ambachtelijk`.
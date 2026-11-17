# -*- coding: utf-8 -*-
import os, shutil, html, json, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import *

ROOT = os.path.dirname(os.path.dirname(__file__))
DIST = os.path.join(ROOT, "dist")
esc = html.escape

TEL_SVG = '<svg class="h-[19px] w-[19px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
MAIL_SVG = '<svg class="h-[19px] w-[19px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16v12H4z"/><path d="M4 7l8 6 8-6"/></svg>'
CHECK = '<svg class="mt-1 h-5 w-5 shrink-0 text-brand" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ARROW = '<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHEV = '<svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

BTN = "inline-flex h-12 items-center justify-center gap-2 r-btn px-4 text-base font-semibold transition hover:-translate-y-0.5 sm:px-6"

def hero_cta(dark=False):
    if dark:
        off = f"{BTN} bg-accent text-white"
        bel = f"{BTN} border-2 border-white/60 bg-transparent text-white"
    else:
        off = f"{BTN} bg-accent text-white shadow-[0_10px_30px_-10px_#2d6a4f]"
        bel = f"{BTN} border-2 border-accent bg-transparent text-brand"
    return (f'<div class="hero-cta flex flex-wrap gap-3">'
            f'<a class="{off}" href="/offerte/"><span class="btn-in">Offerte aanvragen</span></a>'
            f'<a class="{bel}" href="{PHONE_TEL}"><span class="btn-in">{TEL_SVG}Bel</span></a></div>')

def contact_cta(dark=True):
    if dark:
        off = f"{BTN} bg-accent text-white"
        bel = f"{BTN} border-2 border-white/60 bg-transparent text-white"
        em = f"{BTN} border-2 border-white/40 bg-transparent text-white"
    else:
        off = f"{BTN} bg-accent text-white shadow-[0_10px_30px_-10px_#2d6a4f]"
        bel = f"{BTN} border-2 border-accent bg-transparent text-brand"
        em = f"{BTN} border-2 border-line bg-card text-ink"
    return (f'<div class="contact-cta flex flex-col gap-3 sm:flex-row sm:flex-wrap">'
            f'<a class="{off}" href="/offerte/"><span class="btn-in">Offerte aanvragen</span></a>'
            f'<a class="{bel}" href="{PHONE_TEL}"><span class="btn-in">{TEL_SVG}Bel</span></a>'
            f'<a class="{em}" href="{EMAIL_MAILTO}"><span class="btn-in">{MAIL_SVG}E-mail</span></a></div>')

def sec_head(kicker, h2, p=None, center=False):
    return (f'<div class="mb-10 max-w-2xl md:mb-12"><p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">{kicker}</p>'
            f'<h2 class="mt-3 font-serif text-[clamp(1.75rem,4vw,2.75rem)] font-semibold leading-tight tracking-tight text-ink">{h2}</h2>'
            + (f'<p class="mt-4 text-lg text-muted">{p}</p>' if p else '') + '</div>')

def dcard(d, img_lazy=True):
    src = d.get("card_photo") or d.get("photo")
    alt = d.get("card_alt") or d.get("alt", "")
    dims = ' width="426" height="577"' if "shingles-dak" in src else ' width="720" height="540"'
    st = f' style="object-position:{d.get("card_pos", d.get("pos", "50% 50%"))}"'
    return (f'<a class="dcard group flex h-full min-h-0 flex-col overflow-hidden r-card border border-line bg-card transition hover:-translate-y-1 hover:shadow-xl" href="/diensten/{d["slug"]}/">'
            f'<div class="dcard-media relative aspect-[4/3] w-full shrink-0 overflow-hidden bg-band">'
            f'<img src="{src}" alt="{esc(alt)}" loading="eager"{dims} '
            f'class="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]"{st}/></div>'
            f'<div class="dcard-body flex flex-1 flex-col p-6"><h3 class="font-serif text-xl font-semibold text-ink">{esc(d["nav"] if d["slug"] in ("kunststof",) else d["title"])}</h3>'
            f'<p class="mt-2 flex-1 text-[15.5px] leading-relaxed text-muted">{esc(d["card"])}</p>'
            f'<span class="mt-4 inline-flex items-center gap-1.5 pt-1 text-[15px] font-semibold text-brand">Bekijk dienst {ARROW}</span></div></a>')

def projecten_teaser():
    return (f'<section class="sec-pad px-5"><div class="site-hero r-card border border-line bg-card p-6 md:p-8">'
            f'<p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">Foto\'s</p>'
            f'<h2 class="mt-3 font-serif text-[clamp(1.5rem,3.2vw,2.1rem)] font-semibold text-ink">Eigen werk op de projectenpagina</h2>'
            f'<p class="mt-3 max-w-xl text-[17px] text-muted">Voor deze dienst heeft Johnny nog geen aparte fotogalerij op de site. Bekijk zijn bitumen-, zink-, pannendak- en PVC-werk op de projectenpagina.</p>'
            f'<p class="mt-6"><a class="inline-flex min-h-[44px] items-center gap-2 text-[16px] font-semibold text-brand" href="/projecten/">Naar projecten {ARROW}</a></p></div></section>')

def cta_band(h="Lekkage, schade of een dak dat aan vervanging toe is?", p="Neem contact op met Johnny. Een inspectie is vrijblijvend en hij komt zo spoedig mogelijk bij u langs."):
    return (f'<section class="cta-end px-5"><div class="site-hero"><div class="overflow-hidden r-big bg-dark px-6 py-10 md:px-12 md:py-14">'
            f'<div class="grid items-center gap-8 md:grid-cols-[1.4fr_1fr]"><div><h2 class="font-serif text-[clamp(1.6rem,3.6vw,2.4rem)] font-semibold leading-tight text-white">{h}</h2>'
            f'<p class="mt-3 max-w-xl text-[17px] text-slate-300">{p}</p></div>'
            f'<div class="md:justify-self-end">{contact_cta(dark=True)}</div></div></div></div></section>')

NAV = [("/", "Home"), ("/diensten/", "Diensten"), ("/werkwijze/", "Werkwijze"), ("/over-ons/", "Over ons"), ("/projecten/", "Projecten"), ("/contact/", "Contact")]


LOGO_ALT = "Johnny\u2019s Dakwerken, naar de homepage"
def logo(dark=False):
    """Real logo (keyed from Johnny's flat logo). Header swaps variant per style; menu/footer are always dark."""
    if dark:
        return f'<span class="logo-mark"><img class="logo-img logo-fixed" src="/img/logo-dk.webp" width="1020" height="442" alt="Johnny\u2019s Dakwerken"/></span>'
    return ('<span class="logo-mark">'
            '<img class="logo-img logo-lt" src="/img/logo-lt.webp" width="1020" height="442" alt="Johnny\u2019s Dakwerken" fetchpriority="high"/>'
            '<img class="logo-img logo-dk" src="/img/logo-dk.webp" width="1020" height="442" alt="Johnny\u2019s Dakwerken"/></span>')

def header(active):
    items = []
    for href, label in NAV:
        on = "text-ink" if (active == href) else "text-muted"
        items.append(f'<a class="whitespace-nowrap text-[15px] font-medium transition-colors hover:text-ink {on}" href="{href}">{label}</a>')
    nav = "".join(items)
    mm = []
    for href, label in NAV:
        mm.append(f'<a class="flex items-center justify-between border-b border-white/10 py-3 font-serif text-[24px] font-semibold text-white" href="{href}">{label}<span class="text-xl text-white/40">→</span></a>')
    return (f'<header class="site-h sticky top-0 z-40 border-b border-line bg-surface/95 backdrop-blur-md"><div class="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-5 lg:h-[72px]">'
            f'<a class="brand-lockup flex min-w-0 items-center gap-2 sm:gap-2.5" href="/">{logo()}<span class="brand-tag">Dakdekker · Heel Nederland</span></a>'
            f'<nav class="hidden items-center gap-5 xl:gap-7 lg:flex" aria-label="Hoofdmenu">{nav}'
            f'<a class="inline-flex h-11 items-center justify-center r-btn bg-accent px-5 text-[15px] font-semibold text-white shadow-[0_10px_30px_-10px_#2d6a4f] transition hover:-translate-y-0.5" href="/offerte/"><span class="btn-in">Offerte</span></a></nav>'
            f'<button type="button" id="menu-open" aria-controls="menu" aria-expanded="false" aria-label="Menu openen" class="burger-btn lg:hidden"><span class="burger" aria-hidden="true"><i></i><i></i></span></button></div></header>'
            f'<div id="menu" class="fixed inset-0 z-[60] hidden flex-col overflow-y-auto bg-dark px-5 pb-8" role="dialog" aria-modal="true" aria-label="Menu">'
            f'<div class="flex h-16 shrink-0 items-center justify-between"><span class="flex items-center gap-2.5">{logo(True)}</span>'
            f'<button type="button" id="menu-close" aria-label="Sluiten" class="burger-btn"><span class="burger" aria-hidden="true"><i></i><i></i></span></button></div>'
            f'<nav class="mt-2" aria-label="Mobiel menu">{"".join(mm)}</nav>'
            f'<a class="menu-offerte-cta mt-5 flex min-h-[48px] w-full max-w-full items-center justify-center r-btn bg-accent px-5 text-base font-semibold text-white" href="/offerte/"><span class="btn-in">Offerte</span></a>'
            f'<div class="mt-auto pt-6 flex flex-col gap-3">'
            f'<a class="inline-flex h-12 w-full items-center justify-center gap-2 r-btn border-2 border-white/60 text-base font-semibold text-white" href="{PHONE_TEL}"><span class="btn-in">{TEL_SVG}Bel</span></a>'
            f'<a class="inline-flex h-12 w-full items-center justify-center gap-2 r-btn border-2 border-white/40 text-base font-semibold text-white" href="{EMAIL_MAILTO}"><span class="btn-in">{MAIL_SVG}{EMAIL}</span></a></div></div>')

def footer():
    ds = "".join(f'<li><a class="inline-block py-1.5 hover:text-white" href="/diensten/{d["slug"]}/">{esc(d["nav"])}</a></li>' for d in D)
    pg = "".join(f'<li><a class="inline-block py-1.5 hover:text-white" href="{h}">{l}</a></li>' for h, l in NAV if h != "/diensten/") + '<li><a class="inline-block py-1.5 hover:text-white" href="/offerte/">Offerte aanvragen</a></li>'
    return (f'<footer class="site-f bg-dark text-slate-300"><div class="site-hero pb-6 pt-14"><div class="grid gap-10 md:grid-cols-2 lg:grid-cols-[1.3fr_1fr_1fr_1.1fr]">'
            f'<div><div class="flex items-center gap-2.5">{logo(True)}</div><p class="mt-3 max-w-xs text-[15.5px] leading-relaxed">Actief in heel Nederland, vanuit Deventer. Bitumen, kunststof, leien, zink en boeibekleding, met ruim 20 jaar ervaring.</p></div>'
            f'<div><p class="text-sm font-semibold uppercase tracking-[0.14em] text-white">Diensten</p><ul class="mt-3 text-[15.5px]">{ds}</ul></div>'
            f'<div><p class="text-sm font-semibold uppercase tracking-[0.14em] text-white">Pagina\'s</p><ul class="mt-3 text-[15.5px]">{pg}</ul></div>'
            f'<div><p class="text-sm font-semibold uppercase tracking-[0.14em] text-white">Contact</p><ul class="mt-3 text-[15.5px]"><li><a class="inline-block py-1.5 font-semibold text-white" href="{PHONE_TEL}">{PHONE_TXT}</a></li>'
            f'<li><a class="inline-block py-1.5 hover:text-white" href="{EMAIL_MAILTO}">{EMAIL}</a></li><li class="py-1.5">Postbus 101<br/>7450 AC Holten</li><li class="py-1.5">KvK 67684351</li></ul></div></div>'
            f'<div class="mt-12 border-t border-white/15 pt-6 text-sm text-slate-400"><p>© 2026 Johnny van Ophuizen</p></div></div></footer>')

DOCK = ('<div class="style-switch-dock" aria-live="polite"><p class="style-switch-dock-label">STIJLSELECTOR</p>'
        '<div class="style-switch-dock-options" role="radiogroup" aria-label="Stijlselector">'
        '<button type="button" role="radio" aria-checked="true" data-style-option="strak" class="style-switch-dock-btn is-active">Strak</button>'
        '<button type="button" role="radio" aria-checked="false" data-style-option="nacht" class="style-switch-dock-btn">Nacht</button>'
        '<button type="button" role="radio" aria-checked="false" data-style-option="ambachtelijk" class="style-switch-dock-btn">Ambachtelijk</button></div></div>')

STYLE_BOOT = r"""(function(){var h=document.documentElement,TC={nacht:"#0c0d0e",strak:"#0a0a0b",ambachtelijk:"#17191b"},F={ambachtelijk:["playfair","sourcesans","exo2-italic"],nacht:["exo2-italic","07c7676b89ed2778-s.p.2bn3s6zvc0dyp"],strak:["exo2","exo2-italic","07c7676b89ed2778-s.p.2bn3s6zvc0dyp"]};function apply(v){h.setAttribute("data-style",v);if(v!=="ambachtelijk")h.setAttribute("data-lime","");else h.removeAttribute("data-lime");var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute("content",TC[v]||TC.strak);(F[v]||F.strak).forEach(function(f){var l=document.createElement("link");l.rel="preload";l.as="font";l.type="font/woff2";l.crossOrigin="anonymous";l.href="/fonts/"+f+".woff2";document.head.appendChild(l)})}var v="strak";try{var q=new URLSearchParams(location.search).get("style"),k="jd-style";v=q||localStorage.getItem(k)||"strak";if(!/^(ambachtelijk|nacht|strak)$/.test(v))v="strak";if(q)localStorage.setItem(k,v)}catch(e){v="strak"}apply(v)})();"""

JS = """<script>
(function(){var h=document.documentElement,b=document.querySelectorAll('[data-style-option]'),TC={nacht:'#0c0d0e',strak:'#0a0a0b',ambachtelijk:'#17191b'};
function mark(v){b.forEach(function(x){var on=x.getAttribute('data-style-option')===v;x.classList.toggle('is-active',on);x.setAttribute('aria-checked',on?'true':'false')});var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',TC[v]||TC.strak)}
mark(h.getAttribute('data-style')||'strak');
b.forEach(function(x){x.addEventListener('click',function(){var v=x.getAttribute('data-style-option');h.setAttribute('data-style',v);if(v!=='ambachtelijk')h.setAttribute('data-lime','');else h.removeAttribute('data-lime');try{localStorage.setItem('jd-style',v)}catch(e){}mark(v)})})})();
</script>
<script>
(function(){var m=document.getElementById('menu'),o=document.getElementById('menu-open'),c=document.getElementById('menu-close');
function s(v){m.classList.toggle('hidden',!v);m.classList.toggle('flex',v);document.documentElement.style.overflow=v?'hidden':'';o.setAttribute('aria-expanded',v?'true':'false');if(v){requestAnimationFrame(function(){requestAnimationFrame(function(){c.classList.add('on')})})}else{c.classList.remove('on')}}
if(o){o.addEventListener('click',function(){s(true)});c.addEventListener('click',function(){s(false)});m.addEventListener('click',function(e){if(e.target.closest('a'))s(false)});document.addEventListener('keydown',function(e){if(e.key==='Escape')s(false)})}
var f=document.getElementById('offerte-form');
if(f){f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f);var t='Offerte-aanvraag\\n\\nNaam: '+d.get('naam')+'\\nTelefoon: '+d.get('tel')+'\\nAdres/plaats: '+d.get('adres')+'\\nOnderwerp: '+d.get('dienst')+'\\n\\nOmschrijving:\\n'+d.get('bericht');window.location.href='mailto:info@johnnydakwerken.nl?subject='+encodeURIComponent('Offerte-aanvraag')+'&body='+encodeURIComponent(t)})}
})();
</script>"""

def page(path, title, desc, body, active="", breadcrumb_parts=None):
    url = path
    ld = breadcrumb_ld(breadcrumb_parts) if breadcrumb_parts else ""
    out = (f'<!DOCTYPE html><html lang="nl" data-style="strak" data-lime=""><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="icon" href="/favicon.svg" type="image/svg+xml"/><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"/><link rel="apple-touch-icon" href="/apple-touch-icon.png"/>'
           f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"/><meta name="robots" content="noindex"/>'
           f'<meta property="og:title" content="{esc(title)}"/><meta property="og:description" content="{esc(desc)}"/><meta property="og:locale" content="nl_NL"/>'
           f'<meta name="theme-color" content="#0a0a0b"/>'
           f'{org_ld()}{ld}'
           f'<script>{STYLE_BOOT}</script>'
           f'<link rel="stylesheet" href="/assets/app.css"/></head><body>{header(active)}<main>{body}</main>{footer()}{DOCK}{JS}<script src="/motion.js" defer></script></body></html>')
    import re as _re
    if path == '/':
        out = _re.sub(r'(<main><section[^>]*>)', lambda m: m.group(1) + FX_HOME, out, count=1)
    out = out.replace('</section><section', '</section><div class="blade-div" aria-hidden="true"></div><section')
    import re as _re
    out = _re.sub(r'(<p class="[^"]*uppercase[^"]*"[^>]*>(?:<span[^>]*></span>)?)([^<]*)(</p>)', lambda m: m.group(1)+m.group(2).replace(' · ','<span class="kdot">•</span>')+m.group(3), out)
    p = os.path.join(DIST, path.strip("/"), "index.html") if path != "404" else os.path.join(DIST, "404.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(out)

def hero_photo(src, alt, pos="50% 50%", eager=True, pano=False):
    em = "".join(f'<i style="--x:{x}%;--d:{d}s;--dl:{dl}s;--dx:{dx}px"></i>' for x, d, dl, dx in
                 [(8,3.4,0,18),(15,4.2,.8,-14),(23,3.0,1.5,22),(31,4.8,.3,-20),(40,3.6,2.1,12),(48,4.4,1.1,-10),(57,3.2,2.6,24),(66,4.0,.6,-18),(74,3.8,1.9,14),(82,4.6,2.8,-22),(90,3.3,1.3,10),(36,5.0,3.2,-8)])
    pc = ""
    if pano:
        pc = ('<div class="pano-card r-img relative overflow-hidden"><img src="/img/pano-m.webp" width="1000" height="651" loading="eager" fetchpriority="high" alt="De IJssel en de skyline van Deventer"/>'
              '<svg class="arc-m" viewBox="0 0 400 260" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs><linearGradient id="am-g" x1="0" x2="1"><stop offset="0" stop-color="#4cb31a" stop-opacity="0"/><stop offset=".35" stop-color="#9be22b"/><stop offset=".8" stop-color="#d6ff7a"/><stop offset="1" stop-color="#9be22b" stop-opacity=".2"/></linearGradient></defs>'
              '<path class="arc-glow" pathLength="1" d="M-10 250C70 30 280-30 410 120" fill="none" stroke="url(#am-g)" stroke-width="10" stroke-linecap="round"/>'
              '<path class="arc-line" pathLength="1" d="M-10 250C70 30 280-30 410 120" fill="none" stroke="url(#am-g)" stroke-width="3" stroke-linecap="round"/></svg></div>')
    return (f'<div class="hero-ph{" has-pano" if pano else ""} w-full lg:w-[520px] lg:justify-self-end">{pc}<div class="hero-ph-in relative aspect-[4/3] w-full overflow-hidden r-img bg-band shadow-[0_40px_80px_-40px_rgba(0,0,0,0.45)] lg:aspect-[5/4]">'
            f'<img src="{src}" alt="{esc(alt)}" loading="eager" class="absolute inset-0 h-full w-full object-cover" style="object-position:{pos}"/>'
            f'<span class="embers" aria-hidden="true">{em}</span></div></div>')

def roofer_art():
    eb = "".join(f'<i class="e" style="--dx:{dx}px;--dy:{dy}px;--d:{d}s;--dl:{dl}s;--sz:{sz}px"></i>' for dx, dy, d, dl, sz in
                 [(14,-70,2.6,0,3),(34,-112,3.4,.5,2),(-8,-96,3.0,1.1,3),(52,-140,3.8,1.6,2),(22,-60,2.2,2.0,4),(70,-124,4.0,.9,2),(6,-132,3.6,2.4,2),(40,-84,2.8,1.4,3),(-20,-78,2.4,.3,2),(62,-100,3.2,2.9,3),(28,-150,4.2,3.3,2),(10,-52,2.0,1.9,3)])
    return ('<div class="hero-art-w"><img class="hero-art" src="/img/roofer.webp" width="965" height="537" loading="eager" alt="Johnny aan het werk: een dakdekker op een dak met brander en bitumen"/>'
            f'<span class="torch" aria-hidden="true"><i class="t-cast"></i><i class="t-halo"></i><i class="t-core"></i>{eb}</span></div>')

FX = '<div class="fx" aria-hidden="true"></div>'
FX_HOME = ('<div class="fx" aria-hidden="true"><div class="pano">'
      '<picture><source media="(max-width: 1023px)" srcset="/img/pano-m.webp" type="image/webp"/>'
      '<img src="/img/pano-hero.webp" width="1800" height="651" loading="eager" fetchpriority="high" alt="De IJssel en de skyline van Deventer" class="pano-hero-img"/></picture></div>'
      '<svg class="arc" viewBox="0 0 1440 640" preserveAspectRatio="xMidYMid slice" focusable="false"><defs>'
      '<linearGradient id="ar-g" gradientUnits="userSpaceOnUse" x1="760" y1="0" x2="1440" y2="0"><stop offset="0" stop-color="#4cb31a" stop-opacity="0"/><stop offset=".3" stop-color="#9be22b"/><stop offset=".72" stop-color="#d6ff7a"/><stop offset="1" stop-color="#9be22b" stop-opacity=".15"/></linearGradient></defs>'
      '<path class="arc-glow" pathLength="1" d="M860 640C940 60 1240-20 1480 330" fill="none" stroke="url(#ar-g)" stroke-width="12" stroke-linecap="round"/>'
      '<path class="arc-line" pathLength="1" d="M860 640C940 60 1240-20 1480 330" fill="none" stroke="url(#ar-g)" stroke-width="3.5" stroke-linecap="round"/></svg><div class="hero-vignette" aria-hidden="true"></div></div>')
WORDS = ["VAKWERK", "KWALITEIT", "DUURZAAMHEID"]
def _half(): return "".join(f'<span>{w}<b>\u2022</b></span>' for w in WORDS * 4)
MARQ = (f'<div class="marq" aria-hidden="true"><div class="marq-a"><div class="marq-t">{_half()}{_half()}</div></div>'
        f'<div class="marq-b"><div class="marq-t rev">{_half()}{_half()}</div></div></div>')

def work_video():
    return ('<section class="sec-pad px-5"><div class="site-hero">'
            '<p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">In beweging</p>'
            '<h2 class="mt-3 font-serif text-[clamp(1.5rem,3.2vw,2.1rem)] font-semibold text-ink">Johnny aan het werk: bitumen &amp; zinkwerk</h2>'
            '<div class="work-vid-wrap mx-auto mt-6 max-w-[880px]">'
            '<div class="work-vid relative overflow-hidden r-img bg-band">'
            '<video class="block aspect-video w-full object-cover" width="960" height="540" poster="/img/video-poster.webp" muted playsinline loop preload="metadata" data-work-video>'
            '<source src="/video/bitumen_zink.mp4" type="video/mp4"/></video></div>'
            '<p class="work-vid-caption mt-3 px-2 text-[15px] leading-snug text-muted">Johnny aan het werk: bitumen &amp; zinkwerk</p></div></div></section>')

def steps_html(steps):
    return "".join(f'<li class="r-card border border-line bg-card p-6"><span class="grid h-10 w-10 place-items-center r-num bg-accent font-serif text-lg font-semibold text-white">{i+1}</span>'
                   f'<h3 class="mt-4 font-serif text-xl font-semibold text-ink">{esc(t)}</h3><p class="mt-2 text-[15.5px] leading-relaxed text-muted">{esc(p)}</p></li>' for i, (t, p) in enumerate(steps))

SITE_ORIGIN = "https://www.johnnysdakwerken.nl"

def breadcrumb_ld(parts):
    items = []
    for i, (h, name) in enumerate(parts, start=1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if h:
            item["item"] = SITE_ORIGIN.rstrip("/") + h
        items.append(item)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

def org_ld():
    data = {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "name": "Johnny's Dakwerken",
        "url": SITE_ORIGIN,
        "telephone": "+31641723759",
        "email": "info@johnnydakwerken.nl",
        "areaServed": {"@type": "Country", "name": "Netherlands"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Deventer",
            "addressCountry": "NL",
        },
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

def page_head(kicker, h1, intro):
    return (f'<section class="sec-pad bg-surface"><div class="site-hero">'
            f'<p class="flex items-center gap-2.5 text-[13px] font-semibold uppercase tracking-[0.14em] text-brand"><span class="kick-bar h-0.5 w-7 bg-accent" aria-hidden="true"></span>{kicker}</p>'
            f'<h1 class="mt-4 max-w-3xl font-serif text-[clamp(2.1rem,5vw,3.6rem)] font-semibold leading-[1.05] tracking-tight text-ink">{h1}</h1>'
            f'<p class="mt-5 max-w-2xl text-[clamp(17px,1.4vw,19px)] leading-relaxed text-muted">{intro}</p></div></section>')

MATERIEEL = ('<section class="sec-pad px-5"><div class="site-hero r-big border border-line bg-card p-7 md:p-10"><div class="grid items-center gap-6 md:grid-cols-[1.3fr_1fr]">'
  '<div><p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">Eigen materieel</p><h2 class="mt-3 font-serif text-[clamp(1.5rem,3.2vw,2.2rem)] font-semibold leading-tight text-ink">Uitgerust voor het werk</h2>'
  '<p class="mt-3 text-[17px] text-muted">Naast vakmanschap heeft Johnny ook eigen materieel: een ladderlift en een aanhanger met de reclame van Johnny\'s Dakwerken erop.</p></div>'
  '<ul class="grid gap-3 sm:grid-cols-2 md:grid-cols-1">'
  '<li class="flex items-center gap-4 r-img bg-surface p-4"><span class="grid h-12 w-12 shrink-0 place-items-center r-sm bg-accent text-white"><svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 3v18M17 3v18M7 7h10M7 12h10M7 17h10"/></svg></span><span class="font-semibold text-ink">Ladderlift</span></li>'
  '<li class="flex items-center gap-4 r-img bg-surface p-4"><span class="grid h-12 w-12 shrink-0 place-items-center r-sm bg-accent text-white"><svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M2 7h14v9H2zM16 10h4l2 3v3h-6"/><circle cx="7" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg></span><span class="font-semibold text-ink">Aanhanger met onze reclame</span></li></ul></div></div></section>')

def stats():
    items = [("20+", "Jaar ervaring"), ("NL", "Heel Nederland · vanuit Deventer")]
    cells = ""
    for i, (a, b) in enumerate(items):
        cls = "border-r border-line pr-3 mr-3" if i < len(items) - 1 else ""
        a2 = a.replace("20", '<span data-count="20">20</span>', 1) if a == "20+" else (f'<span data-count="{a}">{a}</span>' if a.isdigit() else a)
        cells += f'<div class="min-w-0 {cls}"><dt class="font-serif text-[clamp(1.15rem,3vw,1.65rem)] font-bold tracking-tight text-ink">{a2}</dt><dd class="mt-1 text-[12.5px] text-muted">{b}</dd></div>'
    return f'<dl class="hero-stats grid grid-cols-2 gap-4 border-t border-line pt-5 sm:max-w-md">{cells}</dl>'

# ---------------- pages ----------------
def home():
    cards = "".join(dcard(BY[s]) for s in ["bitumen", "kunststof", "zinkwerk", "shingles", "isolatie", "pannendaken"])
    why = [("Ruim 20 jaar ervaring", "In dakbedekking, bitumen, kunststof, leien en zink."),
           ("Advies per ondergrond", "Voor elke ondergrond een passend, duurzaam en waterdicht daksysteem."),
           ("Spoed bij lekkage", "Bij lekkage of schade komt Johnny zo spoedig mogelijk bij u langs."),
           ("Vrijblijvende inspectie", "Johnny bekijkt uw dak ter plekke en adviseert u eerlijk.")]
    whyh = "".join(f'<li class="r-card border border-line bg-card p-6"><h3 class="font-serif text-lg font-semibold text-ink">{esc(a)}</h3><p class="mt-2 text-[15.5px] leading-relaxed text-muted">{esc(b)}</p></li>' for a, b in why)
    body = (f'<section class="overflow-hidden bg-surface pb-12 pt-6 lg:pb-20 lg:pt-10"><div class="hero-grid site-hero grid items-center gap-6 lg:grid-cols-2 lg:gap-16"><div class="hero-tx min-w-0">'
      f'<p class="mb-4 flex items-center gap-2.5 text-[13px] font-semibold uppercase tracking-[0.14em] text-brand"><span class="kick-bar h-0.5 w-7 bg-accent" aria-hidden="true"></span>Dakdekker in heel Nederland</p>'
      f'<h1 class="font-serif text-[clamp(2.25rem,5.2vw,4.25rem)] font-semibold leading-[1.02] tracking-tight text-ink">Uw dak, <em class="font-semibold not-italic text-brand">weer jarenlang waterdicht</em></h1>'
      f'<p class="mt-4 max-w-[540px] text-[17px] leading-snug text-muted lg:hidden">Bitumen, kunststof, leien en zink. Bij lekkage komt Johnny zo snel mogelijk bij u langs.</p>'
      f'<p class="mt-5 hidden max-w-[540px] text-[clamp(17px,1.45vw,20px)] leading-snug text-muted lg:block">Johnny verzorgt bitumen, kunststof, leien, zink en boeibekleding. Bij lekkage of schade komt hij zo spoedig mogelijk bij u langs.</p>'
      f'<div class="mt-6 lg:mt-8">{hero_cta()}</div><div class="mt-8 hidden lg:block hero-stats-slot">{stats()}</div></div>'
      f'{hero_photo("/img/werk/bit1.webp", "Plat dak met nieuwe bitumineuze dakbedekking", "50% 50%", pano=True)}'
      f'</div></section>'
      f'<div class="hero-stats-after border-t border-line bg-surface px-5 py-4 lg:hidden"><div class="site-hero">{stats()}</div></div>'
      f'{MARQ}'
      f'<section class="sec-pad px-5"><div class="site-hero">{sec_head("Diensten", "Dakwerk voor elk dak", "Van platte daken tot hellende daken en van spoedreparatie tot complete renovatie. Voor elke ondergrond adviseert Johnny een passend systeem.")}'
      f'<div class="diensten-grid diensten-grid-home grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">{cards}</div>'
      f'<p class="mt-8"><a class="inline-flex min-h-[44px] items-center gap-2 text-[16px] font-semibold text-brand" href="/diensten/">Alle diensten bekijken {ARROW}</a></p></div></section>'
      f'<section class="roofer-sec sec-pad px-5"><div class="mx-auto grid max-w-6xl items-center gap-8 md:grid-cols-[1fr_1.2fr] md:gap-10"><div>'
      f'<p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">Aan het werk</p><h2 class="mt-3 font-serif text-[clamp(1.75rem,4vw,2.75rem)] font-semibold leading-tight text-ink">Vakwerk op uw dak</h2>'
      f'<p class="mt-4 max-w-md text-lg text-muted">Johnny pakt het dakwerk aan met vakkennis en eigen materieel. Vraag een offerte aan of bel voor een vrijblijvende inspectie.</p><div class="mt-6">{hero_cta()}</div></div><div>{roofer_art()}</div></div></section>'
      f'<section class="sec-pad border-y border-line bg-band px-5"><div class="mx-auto grid max-w-6xl items-center gap-6 md:grid-cols-[auto_1fr] md:gap-14">'
      f'<div class="relative aspect-[4/5] w-full overflow-hidden r-img shadow-xl md:aspect-[3/4] md:w-[260px]"><img src="/img/johnny.jpg" alt="Johnny van Ophuizen" loading="eager" class="absolute inset-0 h-full w-full object-cover" style="object-position:50% 25%"/></div>'
      f'<div><p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">Over Johnny</p>'
      f'<h2 class="mt-3 font-serif text-[clamp(1.75rem,4vw,2.75rem)] font-semibold leading-tight text-ink">Geboren en getogen in Deventer</h2>'
      f'<p class="mt-4 max-w-2xl text-lg text-muted">“Ik ben Johnny van Ophuizen. Dakdekken is mijn lust en mijn leven. Met ruim 20 jaar ervaring in dakbedekking zorg ik ervoor dat uw dak weer jarenlang bestand is tegen alle weersinvloeden. Kwaliteit en service staan bij mij hoog in het vaandel.”</p>'
      f'<p class="mt-6"><a class="inline-flex min-h-[44px] items-center gap-2 text-[16px] font-semibold text-brand" href="/over-ons/">Meer over Johnny {ARROW}</a></p></div></div></section>'
      f'<section class="sec-pad px-5"><div class="site-hero">{sec_head("Waarom Johnny", "Kwaliteit en service staan voorop")}<ul class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{whyh}</ul>'
      f'<p class="mt-8"><a class="inline-flex min-h-[44px] items-center gap-2 text-[16px] font-semibold text-brand" href="/werkwijze/">Bekijk de werkwijze {ARROW}</a></p></div></section>'
      f'<section class="sec-pad border-y border-line bg-band px-5"><div class="site-hero">{sec_head("Werkgebied", "Actief in heel Nederland, vanuit Deventer", "Johnny werkt door het hele land: van spoedreparatie tot complete renovatie. Zijn vestiging en uitvalsbasis is Deventer.")}'
      f'<p class="-mt-6 max-w-2xl text-lg text-muted">Waar u ook woont in Nederland, u kunt Johnny bellen of appen. Hij komt bij u langs voor een vrijblijvende inspectie en vakkundige uitvoering.</p></div></section>'
      f'{cta_band()}')
    page("/", "Dakdekker heel Nederland | Johnny's Dakwerken: bitumen, kunststof, leien en zink",
         "Johnny's Dakwerken: dakdekker actief in heel Nederland, vanuit Deventer. Ruim 20 jaar ervaring. Bitumen, EPDM en PVC, leien, pannendaken, zinkwerk en isolatie.", body, "/")

def diensten():
    cards = "".join(dcard(d) for d in D)
    EXTRA = ('<a class="group flex flex-col justify-between overflow-hidden r-card bg-dark p-6 transition hover:-translate-y-1 hover:shadow-xl sm:col-span-2 lg:col-span-1" href="/contact/">'
             '<div><h3 class="font-serif text-xl font-semibold text-white">Weet u niet welke dienst u nodig heeft?</h3>'
             '<p class="mt-3 text-[15.5px] leading-relaxed text-slate-300">Stuur Johnny een bericht of bel hem. Hij bekijkt uw dak ter plekke en adviseert per ondergrond een passend systeem.</p></div>'
             f'<span class="mt-6 inline-flex items-center gap-1.5 pt-1 text-[15px] font-semibold text-white">Neem contact op {ARROW}</span></a>')
    mats = "".join(f'<li class="r-btn border border-line bg-card px-4 py-2 text-[15px] font-medium text-ink">{m}</li>' for m in ["Bitumen", "Kunststof", "Leien", "Zink", "Boeibekleding"])
    body = (f'<section class="sec-pad bg-surface"><div class="site-hero"><p class="flex items-center gap-2.5 text-[13px] font-semibold uppercase tracking-[0.14em] text-brand"><span class="kick-bar h-0.5 w-7 bg-accent" aria-hidden="true"></span>Diensten</p>'
      f'<h1 class="mt-4 max-w-3xl font-serif text-[clamp(2.1rem,5vw,3.6rem)] font-semibold leading-[1.05] tracking-tight text-ink">Alle dakwerk van Johnny, op één plek</h1>'
      f'<p class="mt-5 max-w-2xl text-[clamp(17px,1.4vw,19px)] leading-relaxed text-muted">Voor bitumineuze en kunststof dakbedekking bent u bij Johnny aan het juiste adres. Kies hieronder een dienst voor meer informatie.</p>'
      f'<div class="mt-7">{hero_cta()}</div></div></section>'
      f'<section class="sec-pad px-5"><div class="site-hero"><div class="diensten-grid grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{cards}{EXTRA}</div>'
      f'<div class="mt-10 flex flex-col gap-3 r-img border border-line bg-card p-6 md:flex-row md:items-center md:gap-6"><p class="font-semibold text-ink">Materialen waarmee Johnny werkt</p><ul class="flex flex-wrap gap-2">{mats}</ul></div></div></section>'
      f'{MATERIEEL}{cta_band("Weet u niet zeker welke dienst u nodig heeft?", "Stuur Johnny een bericht of bel hem. Hij adviseert per ondergrond een passend systeem.")}')
    page("/diensten/", "Diensten dakdekker heel Nederland | Johnny's Dakwerken",
         "Alle diensten van Johnny's Dakwerken: bitumen, EPDM en PVC, leien, pannendaken, lood- en zinkwerk, isolatie, nieuwbouw, verbouw, renovatie en lekkage. Actief in heel Nederland.", body, "/diensten/")

TITLES = {
 "bitumen": ("Bitumen dakbedekking heel Nederland | Johnny's Dakwerken", "Bitumineuze dakbedekking voor uw platte dak. Johnny legt gemodificeerd bitumen (APP of SBS) aan, actief in heel Nederland vanuit Deventer."),
 "kunststof": ("EPDM en PVC dakbedekking heel Nederland | Johnny's Dakwerken", "Kunststof dakbedekking: EPDM en PVC. Sterk, UV-bestendig en met een bewezen levensduur. Johnny adviseert u ter plekke, door heel Nederland."),
 "leien": ("Leien laten leggen | Johnny's Dakwerken", "Leien op uw hellende dak: een stijlvolle, waterdichte afwerking. Johnny legt leien en adviseert u ter plekke, actief in heel Nederland."),
 "shingles": ("Shingles dakbedekking | Johnny's Dakwerken", "Shingles op uw hellende dak: een klassieke, fraaie afwerking. Johnny legt shingles en adviseert u ter plekke, door heel Nederland."),
 "zinkwerk": ("Lood- en zinkwerk heel Nederland | Johnny's Dakwerken", "Zinkwerk aan vervanging toe? Johnny verzorgt zinken dakgoten, afdekkappen en lood- en zinkwerk. Vraag een vrijblijvende inspectie aan."),
 "isolatie": ("Dakisolatie plat dak | Johnny's Dakwerken", "Isolatie voor uw platte dak: warm dak, PUR, PIR, polystyreen en afschot-isolatie. Meer comfort en lagere stookkosten. Door heel Nederland."),
 "pannendaken": ("Pannendak dakdekker | Johnny's Dakwerken", "Ook pannendaken: Johnny bekijkt uw dak ter plekke en adviseert u. Vrijblijvende inspectie mogelijk, actief in heel Nederland."),
 "nieuwbouw-verbouw-renovatie": ("Dakwerk nieuwbouw, verbouw en renovatie | Johnny's Dakwerken", "Dakwerk bij nieuwbouw, verbouw en renovatie. Johnny heeft ruim 20 jaar ervaring en adviseert voor elke ondergrond een passend daksysteem."),
 "lekkage-en-reparatie": ("Lekkage dak: snel hulp | Johnny's Dakwerken", "Lekkage of schade aan uw dak? Johnny komt zo spoedig mogelijk bij u langs met een vakkundige oplossing. Door heel Nederland. Bel of mail direct."),
}

def dienst(d):
    # hero
    hx = (f'<div class="hero-tx min-w-0"><p class="mb-3 flex items-center gap-2.5 text-[13px] font-semibold uppercase tracking-[0.14em] text-brand lg:mb-5"><span class="kick-bar h-0.5 w-7 bg-accent" aria-hidden="true"></span>{esc(d["kicker"])}</p>'
          f'<h1 class="font-serif text-[clamp(2rem,5vw,3.75rem)] font-semibold leading-[1.04] tracking-tight text-ink">{esc(d["title"])}</h1>'
          f'<p class="mt-4 max-w-[540px] text-[17px] leading-snug text-muted lg:mt-5 lg:text-[19px] lg:max-w-2xl">{esc(d["intro"])}</p>'
          f'<div class="mt-6 lg:mt-8">{hero_cta()}</div></div>')
    if d.get("hero_text_only"):
        hero = (f'<section class="dienst-hero-solo overflow-hidden bg-surface pb-12 pt-6 lg:pb-16 lg:pt-10">'
                f'<div class="site-hero hero-tx-only">{hx}</div></section>')
    else:
        hero = (f'<section class="overflow-hidden bg-surface pb-12 pt-6 lg:pb-16 lg:pt-8"><div class="hero-grid site-hero">'
          f'<div class="grid items-center gap-6 lg:grid-cols-2 lg:gap-16">{hx}{hero_photo(d["photo"], d["alt"], d["pos"])}</div></div></section>')
    paras = "".join(f'<p class="mt-4 text-[17px] leading-relaxed text-muted">{esc(p)}</p>' for p in d["paras"])
    facts = "".join(f'<li class="flex gap-3">{CHECK}<span class="text-[16px] text-ink">{esc(f)}</span></li>' for f in d["facts"])
    when = "".join(f'<li class="flex gap-3">{CHECK}<span class="text-[16px] text-ink">{esc(w)}</span></li>' for w in d["when"])
    info = (f'<section class="sec-pad px-5"><div class="mx-auto grid max-w-6xl gap-10 lg:grid-cols-[1.35fr_1fr] lg:gap-16"><div>'
      f'<h2 class="font-serif text-[clamp(1.6rem,3.6vw,2.4rem)] font-semibold leading-tight text-ink">{esc(d["h2"])}</h2>{paras}</div>'
      f'<div class="space-y-5"><div class="r-card border border-line bg-card p-6"><h3 class="font-serif text-xl font-semibold text-ink">{esc(d["facts_h"])}</h3><ul class="mt-4 space-y-3">{facts}</ul></div>'
      f'<div class="r-card border border-line bg-card p-6"><h3 class="font-serif text-xl font-semibold text-ink">Wanneer neemt u contact op?</h3><ul class="mt-4 space-y-3">{when}</ul></div></div></div></section>')
    gallery = ""
    g = d.get("gallery") or []
    if g:
        spans = ["lg:col-span-2"] * 3 if len(g) == 3 else ["lg:col-span-2"] * 3 + ["lg:col-span-3"] * 2
        gi = "".join(f'<a class="gal group relative block aspect-[4/3] overflow-hidden r-img bg-band {sp}" href="{big}" target="_blank" rel="noopener"><img src="{sm}" alt="{esc(al)}" loading="eager" width="720" height="540" class="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-[1.04]"/></a>' for (sm, big, al), sp in zip(g, spans))
        gallery = (f'<section class="sec-pad px-5"><div class="site-hero"><p class="text-[13px] font-semibold uppercase tracking-[0.16em] text-brand">Foto\'s</p>'
                   f'<h2 class="mb-8 mt-3 font-serif text-[clamp(1.5rem,3.2vw,2.1rem)] font-semibold text-ink">Werk van Johnny</h2><div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">{gi}</div></div></section>')
    blocks = ""
    if d.get("blocks"):
        n = len(d["blocks"])
        cols = "md:grid-cols-2 lg:grid-cols-3" if n % 3 == 0 else "md:grid-cols-2"
        bl = "".join(f'<div class="r-card border border-line bg-card p-6"><h3 class="font-serif text-xl font-semibold text-ink">{esc(t)}</h3><p class="mt-2 text-[15.5px] leading-relaxed text-muted">{esc(p)}</p></div>' for t, p in d["blocks"])
        blocks = f'<section class="sec-pad px-5"><div class="site-hero"><h2 class="mb-8 font-serif text-[clamp(1.5rem,3.2vw,2.1rem)] font-semibold text-ink">{esc(d["blocks_h"])}</h2><div class="grid gap-5 {cols}">{bl}</div></div></section>'
    steps = (f'<section class="sec-pad border-y border-line bg-band px-5"><div class="site-hero">{sec_head("Werkwijze", "Zo gaat Johnny te werk")}'
      f'<ol class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{steps_html(d["steps"])}</ol></div></section>')
    rel = "".join(dcard(BY[s]) for s in d["related"])
    related = (f'<section class="sec-pad px-5"><div class="site-hero"><h2 class="mb-8 font-serif text-[clamp(1.5rem,3.2vw,2.1rem)] font-semibold text-ink">Bekijk ook</h2>'
      f'<div class="diensten-grid grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{rel}</div><p class="mt-8"><a class="inline-flex min-h-[44px] items-center gap-2 text-[16px] font-semibold text-brand" href="/diensten/">Alle diensten {ARROW}</a></p></div></section>')
    vid = work_video() if d["slug"] in ("bitumen", "zinkwerk") else ""
    photos_extra = projecten_teaser() if not g and d["slug"] not in ("bitumen", "zinkwerk") else ""
    t, desc = TITLES[d["slug"]]
    crumbs = [("/", "Home"), ("/diensten/", "Diensten"), (None, d["title"])]
    page(f"/diensten/{d['slug']}/", t, desc, hero + info + vid + gallery + blocks + photos_extra + steps + related + cta_band(), "/diensten/", breadcrumb_parts=crumbs)

def werkwijze():
    long_steps = [
      ("U neemt contact op", "Bel Johnny, mail hem of vraag een offerte aan. Vertel kort wat er aan de hand is: een lekkage, schade, een dak dat aan vervanging toe is, of een nieuw project."),
      ("Johnny bekijkt uw dak", "Ter plekke wordt gekeken naar uw dak en de ondergrond. Heeft u een lekkage of schade, dan komt Johnny zo spoedig mogelijk bij u langs. Een inspectie is vrijblijvend."),
      ("U krijgt advies", "Door zijn brede en jarenlange kennis en ervaring adviseert Johnny voor elke ondergrond een bijpassend daksysteem, gebaseerd op een duurzame en waterdichte constructie."),
      ("Vakkundige uitvoering", "Het werk wordt vakkundig uitgevoerd, zodat uw dak weer jarenlang bestand is tegen alle weersinvloeden.")]
    pts = ["Ruim 20 jaar ervaring in dakbedekking", "Kwaliteit en service staan voorop", "Advies per ondergrond", "Spoed bij lekkage of schade", "Vrijblijvende inspectie"]
    ptsh = "".join(f'<li class="flex gap-3">{CHECK}<span class="text-[16px] text-ink">{p}</span></li>' for p in pts)
    body = (page_head("Werkwijze", "Zo werkt Johnny", "Van uw eerste bericht tot een waterdicht dak: in vier stappen, zonder gedoe.") +
      f'<section class="sec-pad px-5"><div class="site-hero"><ol class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{steps_html(long_steps)}</ol>'
      f'<div class="mt-12 overflow-hidden r-big"><div class="relative aspect-[16/9] w-full md:aspect-[21/8]"><img src="/img/panorama.jpg" alt="De IJssel en de skyline van Deventer" loading="eager" class="absolute inset-0 h-full w-full object-cover"/></div></div></div></section>'
      f'<section class="sec-pad border-y border-line bg-band px-5"><div class="mx-auto grid max-w-6xl gap-10 md:grid-cols-2 md:gap-16"><div>{sec_head("Wat u mag verwachten", "Dakdekker voor heel Nederland")}'
      f'<p class="-mt-6 text-lg text-muted">Johnny van Ophuizen werkt door heel Nederland, met Deventer als vestiging. Voor bitumineuze en kunststof dakbedekking bent u bij hem aan het juiste adres.</p></div>'
      f'<ul class="space-y-4 self-center r-card border border-line bg-surface p-6 md:p-8">{ptsh}</ul></div></section>'
      + cta_band("Klaar om uw dak te laten bekijken?", "Stuur Johnny een bericht of bel hem voor een vrijblijvende inspectie."))
    page("/werkwijze/", "Werkwijze dakdekker | Johnny's Dakwerken",
         "Zo werkt Johnny's Dakwerken: contact, vrijblijvende inspectie ter plekke, advies per ondergrond en vakkundige uitvoering. Actief in heel Nederland, vanuit Deventer.", body, "/werkwijze/")

def over():
    mats = "".join(f'<li><a class="inline-flex min-h-[44px] items-center r-btn border border-line bg-card px-5 text-[15px] font-medium text-ink transition hover:border-accent hover:text-brand" href="/diensten/{s}/">{l}</a></li>' for s, l in [("bitumen", "Bitumen"), ("kunststof", "Kunststof"), ("leien", "Leien"), ("zinkwerk", "Zink"), ("nieuwbouw-verbouw-renovatie", "Boeibekleding")])
    body = (f'<section class="sec-pad bg-surface"><div class="site-hero over-ons-hero">'
      f'<p class="over-kicker flex items-center gap-2.5 text-[13px] font-semibold uppercase tracking-[0.14em] text-brand"><span class="kick-bar h-0.5 w-7 bg-accent" aria-hidden="true"></span>Over Johnny</p>'
      f'<h1 class="over-title mt-1 font-serif text-[clamp(2rem,5vw,3.35rem)] font-semibold leading-[1.05] tracking-tight text-ink">Johnny van Ophuizen</h1>'
      f'<p class="over-sub mt-2 font-serif text-lg text-brand md:text-2xl">Geboren en getogen in Deventer</p>'
      f'<div class="over-photo-wrap"><div class="over-photo-in r-img shadow-md"><img src="/img/johnny.jpg" alt="Johnny van Ophuizen, dakdekker actief in heel Nederland" loading="eager" width="320" height="400"/></div></div>'
      f'<p class="over-quote mt-2 max-w-2xl text-[17px] leading-relaxed text-muted md:mt-0">“Dakdekken is mijn lust en mijn leven. Met ruim 20 jaar ervaring in dakbedekking zorg ik ervoor dat uw dak weer jarenlang bestand is tegen alle weersinvloeden.”</p></div></section>'
      f'<section class="sec-pad px-5"><div class="mx-auto grid max-w-6xl gap-10 md:grid-cols-2 md:gap-16"><div>'
      f'<h2 class="font-serif text-[clamp(1.6rem,3.6vw,2.4rem)] font-semibold leading-tight text-ink">Kwaliteit en service staan bij mij hoog in het vaandel</h2>'
      f'<p class="mt-4 text-[17px] leading-relaxed text-muted">Johnny’s Dakwerken is gespecialiseerd in dakbedekking. Voor bitumineuze en kunststof dakbedekking bent u bij mij aan het juiste adres. Wanneer uw dak aan vervanging toe is of wanneer u een lekkage heeft, neem dan contact op. Ik kom zo spoedig mogelijk bij u langs met een vakkundige oplossing.</p>'
      f'<p class="mt-4 text-[17px] leading-relaxed text-muted">Door mijn brede en jarenlange kennis en ervaring kan ik u voor elke ondergrond een bijpassend daksysteem adviseren.</p></div>'
      f'<div class="r-card border border-line bg-card p-6 md:p-8"><h3 class="font-serif text-xl font-semibold text-ink">De materialen waarmee Johnny werkt</h3><ul class="mt-5 flex flex-wrap gap-2.5">{mats}</ul>'
      f'<div class="mt-8">{stats()}</div></div></div></section>'
      f'{MATERIEEL}{cta_band("Even kennismaken?", "Stuur Johnny een bericht of bel hem. Een inspectie is vrijblijvend.")}')
    page("/over-ons/", "Over Johnny van Ophuizen, dakdekker | Johnny's Dakwerken",
         "Maak kennis met Johnny van Ophuizen: actief in heel Nederland vanuit Deventer, ruim 20 jaar ervaring in dakbedekking. Kwaliteit en service staan voorop.", body, "/over-ons/")

def projecten():
    P = {"bit": ("bitumen", "Bitumineuze dakbedekking"), "zin": ("zinkwerk", "Lood- en zinkwerk"), "pan": ("pannendaken", "Pannendaken"), "pvc": ("kunststof", "Kunststof dakbedekking")}
    ALT = {}
    for dd in D:
        for sm, big, al in dd.get("gallery", []):
            ALT[big.split("/")[-1][:-5]] = al
    ALT.update({"bit2": "Bitumineuze dakbedekking met opstaande randen", "zin6": "Zinken dakbedekking met sluitnaden", "pan1": "Dakpannen met een zinken goot", "pvc1": "Wit PVC-dak met dakdoorvoeren"})
    order = ["pvc1", "bit1", "zin6", "pan1", "bit3", "zin3", "pan3", "bit4"]
    cards = ""
    for n in order:
        sl, lab = P[n[:3]]
        cards += (f'<a class="proj-card group overflow-hidden r-card border border-line bg-card transition hover:-translate-y-1 hover:shadow-xl" href="/diensten/{sl}/">'
                  f'<div class="relative aspect-square w-full overflow-hidden bg-band sm:aspect-[4/3]"><img src="/img/werk/{n}-s.webp" alt="{esc(ALT[n])}" loading="eager" width="720" height="540" class="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]"/></div>'
                  f'<div class="proj-body"><h3 class="proj-title font-serif font-semibold text-ink">{esc(lab)}</h3>'
                  f'<p class="proj-cap mt-1 text-[15px] text-muted">{esc(ALT[n])}</p>'
                  f'<p class="proj-more inline-flex items-center gap-1.5 font-semibold text-brand">Meer {ARROW}</p></div></a>')
    body = (page_head("Projecten", "Werk van Johnny", "Foto's van eigen werk: bitumen, kunststof, zink en pannendaken.") +
      f'<section class="sec-pad px-5"><div class="site-hero"><div class="projecten-grid grid grid-cols-2 gap-3 sm:grid-cols-2 lg:grid-cols-3 lg:gap-5">{cards}</div></div></section>' + cta_band("Uw dak ook een opknapbeurt geven?", "Vraag Johnny om een vrijblijvende inspectie."))
    page("/projecten/", "Projecten en foto's dakwerk | Johnny's Dakwerken",
         "Foto's van het eigen werk van Johnny's Dakwerken: bitumineuze dakbedekking, PVC, zinkwerk en pannendaken. Door heel Nederland.", body, "/projecten/")

def offerte():
    opts = "".join(f'<option>{esc(d["nav"])}</option>' for d in D) + "<option>Anders</option>"
    fld = "mt-1.5 block w-full r-sm border border-line bg-band px-4 text-[16px] text-ink outline-none focus:border-accent focus:ring-2 focus:ring-accent/20"
    body = (page_head("Offerte", "Vraag een vrijblijvende offerte aan", "Vul het formulier in: uw gegevens worden klaargezet in een e-mailbericht aan Johnny. Liever direct bellen of mailen? Zie rechts.") +
      f'<section class="sec-pad px-5"><div class="mx-auto grid max-w-6xl gap-8 lg:grid-cols-[1.4fr_1fr]">'
      f'<form id="offerte-form" class="r-card border border-line bg-card p-6 md:p-8" autocomplete="on"><h2 class="font-serif text-2xl font-semibold text-ink">Uw gegevens</h2><div class="mt-6 grid gap-5 sm:grid-cols-2">'
      f'<label class="block text-sm font-semibold text-ink">Naam<input required name="naam" class="{fld} h-12"/></label>'
      f'<label class="block text-sm font-semibold text-ink">Telefoon<input required name="tel" type="tel" class="{fld} h-12"/></label>'
      f'<label class="block text-sm font-semibold text-ink">Adres en plaats<input required name="adres" class="{fld} h-12"/></label>'
      f'<label class="block text-sm font-semibold text-ink">Waar gaat het om?<select name="dienst" class="{fld} h-12">{opts}</select></label>'
      f'<label class="block text-sm font-semibold text-ink sm:col-span-2">Omschrijving<textarea required name="bericht" rows="5" class="{fld} py-3"></textarea></label></div>'
      f'<button type="submit" class="mt-6 inline-flex h-12 w-full items-center justify-center gap-2 r-btn bg-accent px-7 text-base font-semibold text-white transition hover:-translate-y-0.5 sm:w-auto"><span class="btn-in">{MAIL_SVG}Verstuur per e-mail</span></button></form>'
      f'<aside class="h-fit r-card border border-line bg-card p-6 md:p-8"><h2 class="font-serif text-2xl font-semibold text-ink">Liever direct contact?</h2><p class="mt-3 text-[16px] text-muted">Lekkage of schade? Bel of mail Johnny. Hij komt zo spoedig mogelijk bij u langs.</p>'
      f'<div class="mt-6 flex flex-col gap-3 sm:flex-row"><a class="{BTN} bg-accent text-white shadow-[0_10px_30px_-10px_#2d6a4f]" href="{PHONE_TEL}"><span class="btn-in">{TEL_SVG}Bel {PHONE_TXT}</span></a>'
      f'<a class="{BTN} border-2 border-accent bg-transparent text-brand" href="{EMAIL_MAILTO}"><span class="btn-in">{MAIL_SVG}E-mail</span></a></div>'
      f'<dl class="mt-8 space-y-4 border-t border-line pt-6 text-[16px]"><div><dt class="text-sm font-semibold text-ink">Telefoon</dt><dd><a class="inline-block py-1 text-brand" href="{PHONE_TEL}">{PHONE_TXT}</a></dd></div>'
      f'<div><dt class="text-sm font-semibold text-ink">E-mail</dt><dd><a class="inline-block py-1 text-brand" href="{EMAIL_MAILTO}">{EMAIL}</a></dd></div>'
      f'<div><dt class="text-sm font-semibold text-ink">Postadres</dt><dd class="text-muted">Postbus 101<br/>7450 AC Holten</dd></div><div><dt class="text-sm font-semibold text-ink">KvK</dt><dd class="text-muted">67684351</dd></div></dl></aside></div></section>')
    page("/offerte/", "Offerte aanvragen dakdekker | Johnny's Dakwerken",
         "Vraag een vrijblijvende offerte aan bij Johnny's Dakwerken voor dakbedekking, zinkwerk, isolatie of renovatie. Actief in heel Nederland. Reactie per e-mail of telefoon.", body, "/offerte/")

def contact():
    body = (page_head("Contact", "Neem contact op met Johnny", "Bel of mail voor spoed, advies of een vrijblijvende offerte. Bij lekkage of schade komt Johnny zo spoedig mogelijk bij u langs.") +
      f'<section class="sec-pad px-5"><div class="mx-auto grid max-w-6xl gap-5 md:grid-cols-3">'
      f'<div class="r-card border border-line bg-card p-6 md:col-span-2 md:p-8"><h2 class="font-serif text-2xl font-semibold text-ink">Direct in contact</h2><p class="mt-3 max-w-xl text-[17px] text-muted">Vraag een offerte aan, bel Johnny of stuur een e-mail. Voeg gerust een foto van uw dak of de schade toe.</p><div class="mt-6">{contact_cta(dark=False)}</div>'
      f'<p class="mt-6 text-[16px] text-muted">Liever een offerte op schrift? <a class="font-semibold text-brand" href="/offerte/">Vraag een offerte aan →</a></p></div>'
      f'<div class="r-card border border-line bg-card p-6 md:p-8"><h2 class="font-serif text-2xl font-semibold text-ink">Gegevens</h2><dl class="mt-5 space-y-4 text-[16px]">'
      f'<div><dt class="text-sm font-semibold text-ink">Telefoon</dt><dd><a class="inline-block py-1 text-brand" href="{PHONE_TEL}">{PHONE_TXT}</a></dd></div>'
      f'<div><dt class="text-sm font-semibold text-ink">E-mail</dt><dd><a class="inline-block py-1 text-brand" href="{EMAIL_MAILTO}">{EMAIL}</a></dd></div>'
      f'<div><dt class="text-sm font-semibold text-ink">Postadres</dt><dd class="text-muted">Johnny van Ophuizen<br/>Postbus 101<br/>7450 AC Holten</dd></div>'
      f'<div><dt class="text-sm font-semibold text-ink">KvK</dt><dd class="text-muted">67684351</dd></div></dl></div></div></section>')
    page("/contact/", "Contact dakdekker | Johnny's Dakwerken",
         "Contact met Johnny's Dakwerken: bel of mail voor lekkage, advies of een vrijblijvende offerte. Actief in heel Nederland, vanuit Deventer. Telefoon 06 41 72 37 59.", body, "/contact/")

def notfound():
    body = (f'<section class="sec-pad px-5"><div class="mx-auto max-w-2xl text-center"><h1 class="font-serif text-4xl font-semibold text-ink">Deze pagina bestaat niet</h1><p class="mt-4 text-lg text-muted">Bekijk de diensten van Johnny of ga terug naar de startpagina.</p>'
            f'<div class="mt-8 flex justify-center gap-3"><a class="inline-flex h-12 items-center r-btn bg-accent px-7 font-semibold text-white" href="/"><span class="btn-in">Home</span></a><a class="inline-flex h-12 items-center r-btn border-2 border-accent px-7 font-semibold text-brand" href="/diensten/"><span class="btn-in">Diensten</span></a></div></div></section>')
    page("404", "Pagina niet gevonden | Johnny's Dakwerken", "Deze pagina bestaat niet. Ga naar de startpagina van Johnny's Dakwerken.", body)

if __name__ == "__main__":
    shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "public"), DIST, dirs_exist_ok=True)
    home(); diensten(); werkwijze(); over(); projecten(); offerte(); contact(); notfound()
    for d in D: dienst(d)
    subprocess.check_call(["npx", "tailwindcss", "-i", "src/app.css", "-o", "dist/assets/app.css", "--minify"], cwd=ROOT)
    print("built", sum(1 for _ in os.walk(DIST)))

#!/usr/bin/env python3
"""Verifie qu'il ne reste rien de l'ancien site, et qu'aucun lien ne casse."""
import re, os, glob, sys

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
PAGES = sorted(glob.glob(R + '*/index.html')) + [R + 'index.html', R + 'accueil.html']
PAGES = [p for p in PAGES if '/tools/' not in p and '/cloudflare' not in p]

# Ce qui ne doit plus apparaitre nulle part.
VESTIGES = {
    'Tailwind en CDN':        r'cdn\.tailwindcss\.com',
    'Google Fonts distant':   r'fonts\.(googleapis|gstatic)\.com',
    'Google Analytics':       r'googletagmanager|gtag\(',
    'Banniere cookies':       r'cookieManager',
    'Calendly':               r'calendly',
    'Anciennes polices':      r'Manrope|Poppins|Instrument\+?\s?Serif',
    'Ancienne palette':       r'#(161A22|2A4AD1|4F8268|FAFBFD|E5EAF9|DCEBE2)\b',
    'Ancienne adresse mail':  r'contact@biladesigns\.com',
    'Runtime de maquette':    r'<x-dc|<sc-for|style-hover|x-import|\{\{',
    'Lien mort vers #':       r'href="#"(?![^>]*aria-current)',
}

cibles = {'/'}
for p in glob.glob(R + '*/index.html'):
    d = os.path.basename(os.path.dirname(p))
    cibles.add('/%s/' % d)

probleme = 0
for f in PAGES:
    nom = os.path.relpath(f, R)
    s = open(f, encoding='utf-8').read()
    trouve = []
    for libelle, motif in VESTIGES.items():
        n = len(re.findall(motif, s, re.I))
        if n:
            trouve.append('%s x%d' % (libelle, n))
    # liens internes
    morts = []
    for href in set(re.findall(r'href="(/[^"]*)"', s)):
        chemin = href.split('#')[0].split('?')[0]
        if not chemin:
            continue
        if os.path.splitext(chemin)[1]:
            if not os.path.exists(R + chemin.lstrip('/')):
                morts.append(href)
            continue
        if not chemin.endswith('/'):
            chemin += '/'
        if chemin not in cibles:
            morts.append(href)
    if trouve or morts:
        probleme += 1
        print('%-34s %s %s' % (nom, ' | '.join(trouve), ('liens morts: ' + ', '.join(morts)) if morts else ''))
    else:
        print('%-34s propre' % nom)

# ── Fichiers hors pages ───────────────────────────────────────────────────
# Le favicon et les ressources de marque suivent la meme palette que le
# reste. Le vert de l'ancienne DA y a survecu longtemps parce que ce
# controle ne regardait que les pages.
for f in ['favicon.svg']:
    chemin = R + f
    if not os.path.exists(chemin):
        continue
    t = open(chemin, encoding='utf-8').read()
    vieux = [c for c in ('#0f2f28', '#161A22', '#2A4AD1', '#4F8268', '#FAFBFD')
             if c.lower() in t.lower()]
    if vieux:
        probleme += 1
        print('%-34s ancienne palette : %s' % (f, ', '.join(vieux)))
    else:
        print('%-34s propre' % f)

print()
print('Fichiers avec des restes :', probleme)
sys.exit(1 if probleme else 0)

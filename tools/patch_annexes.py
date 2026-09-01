#!/usr/bin/env python3
"""Pages annexes : redirections, plan du site, page d'accueil racine."""
import os, re

R = '/root/bila-site/'

# ── Anciennes adresses qui n'ont plus de page ─────────────────────────────
# Elles restent valides et menent a ce qui les remplace. Une redirection
# meta plutot qu'une 301 : l'hebergement est un statique sans .htaccess.
REDIRECTIONS = {
    'portfolio':      ('/accueil/#realisations', 'Portfolio'),
    'agence':         ('/accueil/#expertises',   'L’agence'),
    'nouveau-projet': ('/contact/#formulaire',   'Démarrer un projet'),
    'services-old':   (None, None),
}

GABARIT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titre)s — Bila Designs</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://www.biladesigns.com%(cible)s">
<meta http-equiv="refresh" content="0; url=%(cible)s">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/favicon/favicon-180.png">
<meta name="theme-color" content="#101B33">
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/bila.css">
</head>
<body>
<main style="min-height: 60vh; display: flex; flex-direction: column; align-items: flex-start;
             justify-content: center; gap: 18px; padding: 0 var(--gut);">
  <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase;
               color: #2743E3;">Cette page a demenage</span>
  <p style="margin: 0; font-family: 'Fraunces', Georgia, serif; font-size: 34px; line-height: 1.15;
            letter-spacing: -0.02em; color: #101B33;">
    Vous etes redirige vers <a href="%(cible)s">%(titre)s</a>.</p>
</main>
</body>
</html>
"""

for dossier, (cible, titre) in REDIRECTIONS.items():
    if not cible:
        continue
    os.makedirs(R + dossier, exist_ok=True)
    open(R + dossier + '/index.html', 'w', encoding='utf-8').write(
        GABARIT % dict(cible=cible, titre=titre))
    print('redirection       -> /%s/  vers %s' % (dossier, cible))

# ── Racine : plus de page intermediaire, l'accueil est servi directement ──
accueil = open(R + 'accueil/index.html', encoding='utf-8').read()
racine = accueil.replace('href="/assets/', 'href="/assets/').replace(
    '<link rel="canonical" href="https://www.biladesigns.com/accueil">',
    '<link rel="canonical" href="https://www.biladesigns.com/accueil">')
open(R + 'index.html', 'w', encoding='utf-8').write(racine)
print('racine            -> copie de /accueil/ (canonique inchangee)')

# accueil.html : le duplicata que sert l'hebergeur, tenu synchrone.
open(R + 'accueil.html', 'w', encoding='utf-8').write(racine)
print('accueil.html      -> synchronise')

# ── Plan du site ──────────────────────────────────────────────────────────
PAGES = [
    ('/accueil',                   'weekly',  '1.0'),
    ('/services',                  'monthly', '0.9'),
    ('/avocats',                   'monthly', '0.9'),
    ('/contact',                   'monthly', '0.8'),
    ('/mentions-legales',          'yearly',  '0.3'),
    ('/politique-confidentialite', 'yearly',  '0.3'),
]
lignes = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, freq, prio in PAGES:
    lignes += ['  <url>',
               '    <loc>https://www.biladesigns.com%s</loc>' % url,
               '    <lastmod>2026-09-01</lastmod>',
               '    <changefreq>%s</changefreq>' % freq,
               '    <priority>%s</priority>' % prio,
               '  </url>']
lignes.append('</urlset>')
open(R + 'sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lignes) + '\n')
# /automatisations est volontairement absent : la page d'attente est en noindex.
print('sitemap.xml       -> %d adresses (page d’attente exclue)' % len(PAGES))

open(R + 'robots.txt', 'w', encoding='utf-8').write(
    "User-agent: *\n"
    "Allow: /\n"
    "Disallow: /desabonnement\n\n"
    "Sitemap: https://www.biladesigns.com/sitemap.xml\n")
print('robots.txt        -> mis a jour')

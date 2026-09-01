#!/usr/bin/env python3
"""Ajoute une empreinte de contenu aux ressources appelees par les pages.

Hostinger sert les fichiers statiques avec « cache-control: max-age=604800 » :
une feuille de style mise a jour reste servie depuis le cache du CDN jusqu'a
sept jours. Le 1er septembre, le site a ete publie avec le HTML du jour et
la feuille de style de la veille — mise en page cassee pour tout le monde.

L'empreinte change des que le fichier change : l'adresse change avec elle,
le cache ne peut plus repondre a la place du serveur, et la mise a jour est
immediate. Le cache long redevient un avantage au lieu d'un piege.
"""
import os, re, hashlib, glob

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'

RESSOURCES = [
    'assets/css/fonts.css',
    'assets/css/bila.css',
    'assets/js/bila-motion.js',
    'assets/js/bila-ui.js',
]


def empreinte(chemin):
    with open(R + chemin, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


# Les polices sont versionnees d'abord : leur adresse figure dans fonts.css,
# dont l'empreinte doit donc etre calculee apres.
polices = {}
for f in sorted(glob.glob(R + 'assets/fonts/*.woff2')):
    rel = os.path.relpath(f, R)
    polices['/' + rel] = empreinte(rel)

css = open(R + 'assets/css/fonts.css', encoding='utf-8').read()
css_neuf = css
for url, h in polices.items():
    css_neuf = css_neuf.replace('url(%s)' % url, 'url(%s?v=%s)' % (url, h))
if css_neuf != css:
    open(R + 'assets/css/fonts.css', 'w', encoding='utf-8').write(css_neuf)

versions = {'/' + c: empreinte(c) for c in RESSOURCES}
versions.update(polices)

pages = sorted(glob.glob(R + '*/index.html')) + [R + 'index.html', R + 'accueil.html']
total = 0
for page in pages:
    if not os.path.exists(page):
        continue
    s = open(page, encoding='utf-8').read()
    avant = s
    for url, h in versions.items():
        # href="/assets/…" et src="/assets/…", sans toucher a ce qui porte
        # deja une version.
        s = re.sub(r'(["\'])%s(?=["\'])' % re.escape(url), r'\g<1>%s?v=%s' % (url, h), s)
    if s != avant:
        open(page, 'w', encoding='utf-8').write(s)
        total += 1

print('empreintes posees sur %d pages' % total)
for c in RESSOURCES:
    print('  %-28s %s' % (c, versions['/' + c]))

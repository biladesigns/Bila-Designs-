#!/usr/bin/env python3
"""Remplit les emplacements d'image et cable les liens restants."""
import re

R = '/root/bila-site/'
PAGES = ['accueil/index.html', 'services/index.html', 'avocats/index.html',
         'contact/index.html', 'automatisations/index.html']

# ── Emplacements de capture de l'accueil ──────────────────────────────────
CAPTURES = {
    'capture vulpi éducation':      ('/public/images/vulpi-preview.webp',
                                     'Page d’accueil de Vulpi Éducation'),
    'capture orion security':       ('/public/images/orion-preview.webp',
                                     'Page d’accueil du site Orion Security'),
    'capture scierie du marthuret': ('/public/images/marthuret-preview.webp',
                                     'Page d’accueil du site de la Scierie du Marthuret'),
    'capture pierre hamoumou':      ('/public/images/hamoumou-preview.webp',
                                     'Page d’accueil du site de Pierre Hamoumou, avocat'),
}

s = open(R + 'accueil/index.html', encoding='utf-8').read()
place = 0
for libelle, (src, alt) in CAPTURES.items():
    motif = re.compile(
        r'<div style="position: absolute; inset: 0; display: flex; align-items: center; '
        r'justify-content: center;">\s*<span style="font-family: ui-monospace[^"]*">'
        + re.escape(libelle) + r'[^<]*</span>\s*</div>', re.S)
    # Trois largeurs, et une indication de la taille d'affichage reelle :
    # une carte occupe toute la largeur utile sur telephone, la moitie
    # d'une grille de deux colonnes au-dela. Sans « sizes », le navigateur
    # supposerait 100vw et telechargerait toujours le plus gros fichier.
    base = src.replace('.webp', '')
    remplacement = (
        '<img src="%s" '
        'srcset="%s-640.webp 640w, %s-800.webp 800w, %s-1200.webp 1200w, %s 1600w" '
        # « sizes » n'accepte que des longueurs : une variable CSS y est
        # invalide et l'attribut serait ignore en entier, ramenant le
        # navigateur a 100vw. Les valeurs suivent les gouttieres reelles.
        'sizes="(max-width: 640px) calc(100vw - 40px), '
        '(max-width: 900px) calc(100vw - 64px), '
        '(max-width: 1180px) calc(50vw - 80px), '
        '(max-width: 1440px) calc(50vw - 122px), 620px" '
        'alt="%s" width="1600" height="1200" loading="lazy" decoding="async" '
        'style="position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; '
        'object-position: 50%% 0;">' % (src, base, base, base, src, alt))
    s, n = motif.subn(remplacement, s)
    assert n == 1, 'emplacement « %s » : %d' % (libelle, n)
    place += 1

# Le fond quadrille de l'emplacement vide n'a plus lieu d'etre sous une image.
s = s.replace('background-color: #EFEFEC; background-image: linear-gradient(rgba(16,27,51,0.07) 1px, '
              'transparent 1px), linear-gradient(90deg, rgba(16,27,51,0.07) 1px, transparent 1px); '
              'background-size: 100% 25%, 25% 100%;',
              'background-color: #EFEFEC;')

# Liens des cartes de realisation : chaque carte est traitee par son titre,
# pas par sa position, pour qu'un remaniement de la grille ne les melange pas.
LIENS_CARTES = {
    'Vulpi Éducation':      ('https://vulpi.education', 'Voir le site'),
    'Scierie du Marthuret': ('https://scieriedumarthuret.fr', 'Voir le site'),
}
morceaux = s.split('<article ')
for i in range(1, len(morceaux)):
    for titre, (url, libelle) in LIENS_CARTES.items():
        if '>' + titre + '<' not in morceaux[i]:
            continue
        m = re.search(r'<a href="#"([^>]*)>([^<]*)<span', morceaux[i])
        assert m, 'lien introuvable dans la carte « %s »' % titre
        morceaux[i] = morceaux[i].replace(
            m.group(0),
            '<a href="%s" target="_blank" rel="noopener"%s>%s <span' % (url, m.group(1), libelle),
            1)
s = '<article '.join(morceaux)
assert 'vulpi.education' in s and 'scieriedumarthuret.fr' in s, 'liens de cartes non poses'

# « Découvrir notre agence » : la maquette pointe vers une ancre inexistante.
s = s.replace('href="#apropos"', 'href="/contact/"')
open(R + 'accueil/index.html', 'w', encoding='utf-8').write(s)
print('accueil : %d captures placees' % place)

# ── Liens communs a toutes les pages ──────────────────────────────────────
PIED = [
    ('<a href="#" style="font-size: 12px; color: #8A8F9C;">Mentions légales</a>',
     '<a href="/mentions-legales/" style="font-size: 12px; color: #8A8F9C;">Mentions légales</a>'),
    ('<a href="#" style="font-size: 12px; color: #8A8F9C;">Confidentialité</a>',
     '<a href="/politique-confidentialite/" style="font-size: 12px; color: #8A8F9C;">Confidentialité</a>'),
    # Le site ne depose aucun cookie : ce lien ne menait a rien a gerer.
    ('<a href="#" style="font-size: 12px; color: #8A8F9C;">Gestion des cookies</a>', ''),
]

# Les liens externes s'ouvrent dans un nouvel onglet, sans fuite de referent.
EXTERNES = ['https://orionsecurity.fr', 'https://pierrehamoumou-avocat.fr',
            'https://auravocats.com', 'https://fremont-avocat.fr',
            'https://www.instagram.com/biladesigns', 'https://www.linkedin.com/company/biladesigns']

total = 0
for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()
    for avant, apres in PIED:
        s = s.replace(avant, apres)
    for url in EXTERNES:
        s = re.sub(r'<a href="%s"(?![^>]*target=)' % re.escape(url),
                   '<a href="%s" target="_blank" rel="noopener"' % url, s)
    # L'entree de nav de la page courante ne mene nulle part : on la neutralise.
    s = s.replace('<a href="#" style="white-space: nowrap; font-size: 14px; font-weight: 600; color: #2743E3;">',
                  '<a href="#" aria-current="page" style="white-space: nowrap; font-size: 14px; '
                  'font-weight: 600; color: #2743E3;">')
    reste = len(re.findall(r'href="#"', s))
    open(chemin, 'w', encoding='utf-8').write(s)
    total += reste
    print('%-28s  liens "#" restants : %d' % (page, reste))

#!/usr/bin/env python3
"""Priorites de chargement des images de direction artistique.

Les deux heros sont charges tout de suite (ils portent le plus grand
element visible de la page) ; le reste est differe. Les images calees en
absolu ne recoivent pas de width/height : leur taille vient de la mise en
page, pas de leurs attributs, donc les preciser n'evite aucun decalage.
"""
import re

R = '/root/bila-site/'
REGLES = {
    'accueil/index.html':  [('hero-arche-crop.png', 'eager', None)],
    'services/index.html': [('hero-atelier.png', 'eager', None),
                            ('section-arche.png', 'lazy', (1680, 720))],
    'avocats/index.html':  [('hero-avocats.png', 'eager', None)],
}

for page, images in REGLES.items():
    s = open(R + page, encoding='utf-8').read()
    for nom, mode, dims in images:
        m = re.search(r'<img src="/assets/img/%s"[^>]*>' % re.escape(nom), s)
        assert m, '%s : %s introuvable' % (page, nom)
        balise = m.group(0)
        if 'loading=' in balise:
            continue
        ajout = (' loading="eager" fetchpriority="high" decoding="async"' if mode == 'eager'
                 else ' loading="lazy" decoding="async"')
        if dims:
            ajout += ' width="%d" height="%d"' % dims
        s = s.replace(balise, balise[:-1].rstrip() + ajout + '>', 1)
        print('%-22s %-22s %s' % (page, nom, mode))
    open(R + page, 'w', encoding='utf-8').write(s)

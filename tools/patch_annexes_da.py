#!/usr/bin/env python3
"""Harmonise les pages annexes avec la nouvelle direction artistique.

Mentions legales, confidentialite et desabonnement n'ont pas de maquette :
elles gardent leur structure et leur contenu. Seuls la palette et les
caracteres sont repris, pour qu'elles ne jurent pas avec le reste du site.
La page de desabonnement est fonctionnelle : rien de son comportement
n'est touche.
"""
import re

R = '/root/bila-site/'
PAGES = ['mentions-legales', 'politique-confidentialite', 'desabonnement']

COULEURS = {
    '#161A22': '#101B33',   # encre
    '#2A4AD1': '#2743E3',   # bleu accent
    '#1E3AA6': '#1B31A8',   # bleu fonce
    '#FAFBFD': '#FBFBFA',   # fond
    '#4F8268': '#4A5163',   # ancien vert : devient le gris des annotations
    '#2A3340': '#4A5163',   # texte courant
    '#5A6473': '#6B7280',   # texte secondaire
    '#6E7683': '#6B7280',
    '#B9C0CB': '#A0A5B0',
    '#E5EAF9': '#EDF0FB',
    '#DCEBE2': '#EDF0FB',   # ancien vert pale
    '#EEF1F6': '#F6F6F3',   # fond secondaire
    '#e5e7eb': '#E3E5EA',
    '#E5E7EB': '#E3E5EA',
}

for page in PAGES:
    chemin = R + page + '/index.html'
    s = open(chemin, encoding='utf-8').read()
    avant = s

    for vieux, neuf in COULEURS.items():
        s = s.replace(vieux, neuf)

    # Caracteres : Poppins devient Archivo, et les polices sont servies
    # depuis le site plutot que depuis Google.
    s = s.replace("'Poppins'", "'Archivo'").replace('"Poppins"', '"Archivo"')
    s = s.replace("Poppins','system-ui'", "Archivo','system-ui'")
    s = s.replace('Poppins', 'Archivo')
    s = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>\s*', '', s)
    s = re.sub(r'<link[^>]+fonts\.gstatic\.com[^>]*>\s*', '', s)
    if '/assets/css/fonts.css' not in s:
        s = s.replace('</head>',
                      '<link rel="stylesheet" href="/assets/css/fonts.css">\n</head>', 1)

    # Le lien « Gestion des cookies » du nouveau pied de page vise cette ancre.
    if page == 'politique-confidentialite' and 'id="cookies"' not in s:
        m = re.search(r'<h2([^>]*)>\s*([^<]*[Cc]ookie[^<]*)</h2>', s)
        if m:
            s = s.replace(m.group(0), '<h2 id="cookies"%s>%s</h2>' % (m.group(1), m.group(2)), 1)

    open(chemin, 'w', encoding='utf-8').write(s)
    print('%-28s  %s' % (page, 'harmonisee' if s != avant else 'inchangee'))

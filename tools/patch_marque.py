#!/usr/bin/env python3
"""Remplace la marque dessinee en divs par le fichier livre par le designer.

La marque du bandeau et du pied de page etait reconstituee en HTML, avec
deux ecarts au dossier de marque :

  - les jambes etaient navy sur champ bleu, la ou la marque a des jambes
    blanches ;
  - elles faisaient 12 px sur une largeur de 26, soit 46 % de chaque cote :
    il ne restait que 2 px de bleu au centre, contre 45 % dans le dessin
    d'origine (12 sur 44).

Le fond du site est clair. Le dossier est explicite : sur fond clair la
marque doit porter son cadre navy, sinon les jambes blanches se fondent
dans le fond et il ne reste qu'un entonnoir bleu. C'est donc la version
cadree qui est posee, la meme que dans la signature de mail et le favicon.
"""
import re, os, glob

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
SVG = '/assets/marque/logo-mark-framed.svg'

# Le fichier livre fait 58 x 64. Les hauteurs du site sont conservees ;
# les largeurs suivent le rapport de la marque.
TAILLES = [
    (26, 30, 27, 30),   # bandeau
    (22, 26, 24, 26),   # pied de page
]

MOTIF = (r'<div style="position: relative; width: %dpx; height: %dpx; overflow: hidden; '
         r'background: #2743E3;">\s*'
         r'<div style="position: absolute; left: 0; top: 0; width: \d+px; height: %dpx; '
         r'background: #101B33; border-top-right-radius: \d+px %dpx;"></div>\s*'
         r'<div style="position: absolute; right: 0; top: 0; width: \d+px; height: %dpx; '
         r'background: #101B33; border-top-left-radius: \d+px %dpx;"></div>\s*</div>')

pages = sorted(glob.glob(R + '*/index.html')) + [R + 'index.html', R + 'accueil.html']
total = 0
for page in pages:
    if not os.path.exists(page):
        continue
    s = open(page, encoding='utf-8').read()
    n = 0
    for l, h, nl, nh in TAILLES:
        motif = re.compile(MOTIF % (l, h, h, h, h, h), re.S)
        # alt vide : le nom « Bila Designs » est ecrit juste a cote, le
        # repeter ferait dire deux fois la meme chose au lecteur d'ecran.
        img = ('<img src="%s" alt="" width="%d" height="%d" '
               'style="display: block; width: %dpx; height: %dpx; flex: 0 0 auto;">'
               % (SVG, nl, nh, nl, nh))
        s, k = motif.subn(img, s)
        n += k
    if n:
        open(page, 'w', encoding='utf-8').write(s)
        total += n
        print('%-34s %d marque(s)' % (os.path.relpath(page, R), n))

assert total, 'aucune marque remplacee'
print('total : %d' % total)

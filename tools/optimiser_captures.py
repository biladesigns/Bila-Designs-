#!/usr/bin/env python3
"""Decline les captures de realisations en plusieurs largeurs.

Sur telephone la carte fait environ 350px de large : servir un fichier de
1600px revient a telecharger seize fois trop de pixels. Trois largeurs
suffisent a couvrir du telephone au grand ecran retina.
"""
import os
from PIL import Image

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
D = R + 'public/images/'
LARGEURS = [640, 800, 1200, 1600]
CAPTURES = ['vulpi', 'orion', 'marthuret', 'hamoumou']

total_avant = total_apres = 0
for nom in CAPTURES:
    src = D + '%s-preview.webp' % nom
    if not os.path.exists(src):
        print('absente : %s' % src)
        continue
    im = Image.open(src).convert('RGB')
    total_avant += os.path.getsize(src)
    tailles = []
    for l in LARGEURS:
        if l >= im.width:
            dst = src if l == LARGEURS[-1] else None
        else:
            dst = D + '%s-preview-%d.webp' % (nom, l)
        if dst is None:
            continue
        petite = im if l >= im.width else im.resize((l, round(im.height * l / im.width)), Image.LANCZOS)
        petite.save(dst, 'WEBP', quality=78, method=6)
        o = os.path.getsize(dst)
        total_apres += o
        tailles.append('%dw %.0fKo' % (l, o / 1024))
    print('%-12s %s' % (nom, '  '.join(tailles)))

print('\ntotal des declinaisons : %.0f Ko' % (total_apres / 1024))

#!/usr/bin/env python3
"""Convertit les images de direction artistique en WebP.

Les originaux PNG restent dans le depot comme sources ; le site sert les
WebP, dix a vingt fois plus legers a rendu equivalent. Les heros sont le
plus grand element visible de leur page : leur poids fait directement la
note de performance.
"""
import os
from PIL import Image

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
D = R + 'assets/img/'

# Largeur maximale utile : les heros sont affiches sur environ deux tiers
# d'un ecran, un fichier de 2000 px couvre le retina jusqu'en 1920.
LARGEUR_MAX = 2000
QUALITE = 80

for f in sorted(os.listdir(D)):
    if not f.endswith('.png'):
        continue
    src = D + f
    dst = D + f[:-4] + '.webp'
    im = Image.open(src).convert('RGB')
    avant = os.path.getsize(src)
    if im.width > LARGEUR_MAX:
        h = round(im.height * LARGEUR_MAX / im.width)
        im = im.resize((LARGEUR_MAX, h), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=QUALITE, method=6)
    apres = os.path.getsize(dst)
    print('%-24s %8.2f Mo -> %6.0f Ko   %dx%d' % (f, avant / 1e6, apres / 1e3, im.width, im.height))

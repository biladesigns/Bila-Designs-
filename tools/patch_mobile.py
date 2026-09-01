#!/usr/bin/env python3
"""Prepare les pages pour le telephone.

Deux marquages, poses en dernier pour ne pas gener les etapes de cablage :

  .fx-row  sur les rangees horizontales qui ne savent pas passer a la ligne
  .tN      sur les tres petits corps de police (9 a 12px)

Les regles correspondantes vivent dans bila.css, sous media query : le
rendu desktop n'est pas touche.
"""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dc_convert import tag_flex, tag_petits

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
PAGES = ['accueil/index.html', 'services/index.html', 'avocats/index.html',
         'contact/index.html', 'automatisations/index.html',
         'mentions-legales/index.html', 'politique-confidentialite/index.html',
         'desabonnement/index.html']

for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()
    tete, sep, corps = s.partition('<main')
    assert sep, 'pas de <main> dans %s' % page
    corps = tag_petits(tag_flex(sep + corps))
    s = tete + corps
    open(chemin, 'w', encoding='utf-8').write(s)
    print('%-32s fx-row x%-3d  petits corps x%d'
          % (page, s.count('fx-row'), len(re.findall(r'\bt(?:9|10|11|12)\b', s))))

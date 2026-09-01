#!/usr/bin/env python3
"""Reprend la presentation en ecran incline des realisations.

C'est le seul element que Mathieu voulait garder de l'ancien site : les
captures de sites presentees comme des ecrans vus de trois quarts, qui se
redressent au survol. Le principe est repris tel quel de l'ancienne
feuille de style ; l'habillage est adapte a la nouvelle DA — angles vifs
au lieu d'angles arrondis, ombre encree plutot que noire.
"""
import re, os

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
CHEMIN = R + 'accueil/index.html'
s = open(CHEMIN, encoding='utf-8').read()

# Le cadre de chaque capture : c'est lui qui s'incline.
CADRE = ('position: relative; aspect-ratio: 4 / 3; overflow: hidden; '
         'background-color: #EFEFEC;')
assert s.count(CADRE) == 4, 'cadres de capture : %d' % s.count(CADRE)

s = s.replace('<div style="%s">' % CADRE,
              '<div class="ecran-3d"><div class="ecran-3d-plaque" style="%s">' % CADRE)

# Refermer la plaque : chaque cadre est suivi du filet de separation.
FIN = ('</div>\n      <div style="height: 1px; background: rgba(16,27,51,0.14);"></div>')
assert s.count(FIN) == 4, 'fermetures de cadre : %d' % s.count(FIN)
s = s.replace(FIN, '</div></div>\n      <div style="height: 1px; background: rgba(16,27,51,0.14);"></div>')

# Le reflet, pose sur la plaque, s'efface quand l'ecran se redresse.
s = s.replace('<div style="position: absolute; right: 0; bottom: 0; width: 42%; height: 1px; '
              'background: rgba(39,67,227,0.7);"></div>',
              '<div style="position: absolute; right: 0; bottom: 0; width: 42%; height: 1px; '
              'background: rgba(39,67,227,0.7);"></div>'
              '<span class="ecran-3d-reflet" aria-hidden="true"></span>')

open(CHEMIN, 'w', encoding='utf-8').write(s)
print('accueil : 4 captures presentees en ecran incline')

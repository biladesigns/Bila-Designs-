#!/usr/bin/env python3
"""Rend le schema des huit leviers lisible sur un telephone.

Le schema est dessine pour 1240 px de large. Ramene a la largeur utile
d'un telephone il tombe a 350 x 171 : les libelles deviennent des traits
gris. Le reduire davantage n'a pas de sens, l'agrandir non plus tant qu'il
doit tenir dans l'ecran.

Il garde donc sa taille de lecture et devient explorable au doigt, avec
une invite pour que personne ne passe a cote.
"""
import re, os

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
CHEMIN = R + 'services/index.html'
s = open(CHEMIN, encoding='utf-8').read()

i = s.index('<svg viewBox="0 -30 1240 606"')
j = s.index('</svg>', i) + len('</svg>')

s = (s[:i]
     + '<div class="schema-piste">'
     + s[i:j]
     + '</div>\n    <span class="schema-invite" aria-hidden="true">faites glisser pour explorer</span>'
     + s[j:])

assert s.count('schema-piste') == 1
open(CHEMIN, 'w', encoding='utf-8').write(s)
print('services : schema rendu explorable')

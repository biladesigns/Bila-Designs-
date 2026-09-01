#!/usr/bin/env python3
"""Deux corrections sur la page Avocats.

Cadre deontologique — chaque regle portait son propre data-rise, donc sa
propre apparition. Les quatre lignes montaient l'une apres l'autre et il
suffisait d'un defilement rapide pour en surprendre une en cours de
route : elle paraissait alors desalignee. C'est une liste, elle apparait
d'un bloc.

Chaine du dossier — les cinq onglets se partageaient la largeur : a 390 px
ils faisaient 71 px chacun et les libelles se chevauchaient. Ils portent
desormais un repere pour passer en liste verticale sur telephone.
"""
import os

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
CHEMIN = R + 'avocats/index.html'
s = open(CHEMIN, encoding='utf-8').read()

MOTIF = '<span data-rise style="display: flex; align-items: baseline; gap: 16px;'
n = s.count(MOTIF)
assert n == 4, 'regles deontologiques : %d' % n
s = s.replace(MOTIF, '<span style="display: flex; align-items: baseline; gap: 16px;')

ancre = ('<div style="display: flex; flex-direction: column;">\n      '
         '<span style="display: flex; align-items: baseline; gap: 16px; '
         'border-top: 1px solid rgba(39,67,227,0.2);')
assert s.count(ancre) == 1, 'conteneur des regles introuvable'
s = s.replace(ancre, ancre.replace('<div style=', '<div data-rise style=', 1), 1)

ancre = ('<div role="tablist" aria-label="Chaîne du dossier" '
         'style="display: flex; align-items: stretch; border-top: 1px solid rgba(16,27,51,0.22); '
         'border-bottom: 1px solid rgba(16,27,51,0.14);">')
assert s.count(ancre) == 1, 'barre d onglets introuvable'
s = s.replace(ancre, ancre.replace('<div role="tablist"', '<div class="onglets-chaine" role="tablist"', 1), 1)

open(CHEMIN, 'w', encoding='utf-8').write(s)
print('avocats : apparition groupee des regles, onglets reperes')

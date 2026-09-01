#!/usr/bin/env python3
"""Harmonise les trois etapes de la page « Sites web & branding ».

Les vignettes alternaient : a droite pour les phases 1 et 3, a gauche pour
la phase 2. L'alternance se justifie sur une page qui se lit d'un bloc ;
ici les trois cartes se superposent en restant collees, et le saut de la
vignette d'un cote a l'autre se voit comme un defaut.

Elles passent toutes a droite, et se reduisent de 320 a 260 px : la carte
gagne en hauteur, ce qui compte parce qu'une carte plus haute que la
fenetre se fait rogner par le bas quand elle est collante.
"""
import re, os

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
CHEMIN = R + 'services/index.html'
s = open(CHEMIN, encoding='utf-8').read()


def enfants_directs(s, debut):
    """Positions des divs enfants directs du bloc ouvert en `debut`."""
    j = s.index('>', debut) + 1
    prof, k, out = 1, j, []
    while prof > 0 and k < len(s):
        o, f = s.find('<div', k), s.find('</div>', k)
        if f == -1:
            break
        if o != -1 and o < f:
            if prof == 1:
                out.append(o)
            prof += 1
            k = o + 4
        else:
            prof -= 1
            if prof == 1:
                out.append(('fin', f + 6))
            k = f + 6
    return out


# ── Phase 2 : remettre le texte a gauche et la vignette a droite ──────────
i = s.index('id="step-2"')
debut = s.rindex('<div', 0, i)
marques = enfants_directs(s, debut)
bornes = []
courant = None
for m in marques:
    if isinstance(m, tuple):
        if courant is not None:
            bornes.append((courant, m[1]))
            courant = None
    else:
        if courant is None:
            courant = m
assert len(bornes) == 2, 'phase 2 : %d enfants' % len(bornes)

(a0, a1), (b0, b1) = bornes
vignette, texte = s[a0:a1], s[b0:b1]
assert 'data-rise' in vignette and 'flex-direction: column' in texte
s = s[:a0] + texte + '\n      ' + vignette + s[b1:]

# La grille suit le nouvel ordre.
s = s.replace('grid-template-columns: 320px minmax(0, 1fr)',
              'grid-template-columns: minmax(0, 1fr) 320px', 1)

# ── Vignettes plus discretes ──────────────────────────────────────────────
n = s.count('grid-template-columns: minmax(0, 1fr) 320px')
assert n == 3, 'colonnes des etapes : %d' % n
s = s.replace('grid-template-columns: minmax(0, 1fr) 320px',
              'grid-template-columns: minmax(0, 1fr) 260px')

open(CHEMIN, 'w', encoding='utf-8').write(s)
print('services : trois vignettes a droite, 260 px')

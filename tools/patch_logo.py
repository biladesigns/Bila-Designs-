#!/usr/bin/env python3
"""Pose le logotype « Deux encres » dans l'en-tete et le pied de page.

Le logo n'est pas une image : il est compose en HTML, deux lettres en
Fraunces 600 imprimees l'une sur l'autre. Le recouvrement produit une
troisieme encre, et c'est lui qui fait la marque. Le rendu reste net a
toutes les tailles et se sert de la Fraunces deja chargee par le site.

Le verrouillage complet remplace l'ancienne marque *et* le nom qui la
suivait : monogramme, filet vertical, nom en Archivo 700.
"""
import re, os, glob

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'

# Corps du monogramme. Le dossier indique « 26 px environ » pour l'en-tete ;
# 28 conserve la presence de l'ancienne marque, qui faisait 30 px de haut.
CORPS = {'entete': 28, 'pied': 24}


def verrou(corps):
    return (
        '<span class="logo" style="font-size: %dpx;">'
        '<span class="logo-bd" aria-hidden="true">'
        '<span class="logo-b">B</span><span class="logo-d">D</span>'
        '</span>'
        '<span class="logo-filet" aria-hidden="true"></span>'
        '<span class="logo-nom">Bila Designs</span>'
        '</span>' % corps)


# L'ancienne marque : soit le rectangle en divs, soit l'image du cadre
# posee a l'etape precedente. Les deux sont suivies du nom en clair.
MOTIFS = [
    # image (etat courant du depot)
    (r'<img src="/assets/marque/logo-mark-framed\.svg[^>]*>\s*'
     r'<span style="[^"]*">Bila Designs</span>'),
    # rectangle dessine en divs (etat des maquettes)
    (r'<div style="position: relative; width: \d+px; height: \d+px; overflow: hidden; '
     r'background: #2743E3;">.*?</div>\s*'
     r'<span style="[^"]*">Bila Designs</span>'),
]

pages = sorted(glob.glob(R + '*/index.html')) + [R + 'index.html', R + 'accueil.html']
total = 0
for page in pages:
    if not os.path.exists(page):
        continue
    s = open(page, encoding='utf-8').read()
    n = 0
    for motif in MOTIFS:
        # la premiere occurrence est l'en-tete, la seconde le pied de page
        for cle in ('entete', 'pied'):
            s, k = re.subn(motif, verrou(CORPS[cle]), s, count=1, flags=re.S)
            n += k
    if n:
        open(page, 'w', encoding='utf-8').write(s)
        total += n
        print('%-34s %d verrouillage(s)' % (os.path.relpath(page, R), n))

assert total, 'aucun logotype pose'
print('total : %d' % total)

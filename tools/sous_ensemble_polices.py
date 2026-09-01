#!/usr/bin/env python3
"""Reduit les polices aux caracteres dont le site a besoin.

Les fichiers variables de Google couvrent tout l'alphabet latin etendu et
des jeux de chiffres alternatifs : 177 Ko charges sur chaque page pour un
site en francais. On garde le francais complet, la ponctuation
typographique et les fleches utilisees dans les boutons — de quoi ecrire
n'importe quelle page a venir sans retomber sur une police de secours.
"""
import os, subprocess, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
D = R + 'assets/fonts/'
SRC = R + 'tools/polices-source/'

from jeu_caracteres import BASE

os.makedirs(SRC, exist_ok=True)
gain_total = 0

for chemin in sorted(glob.glob(D + '*.woff2')):
    nom = os.path.basename(chemin)
    source = SRC + nom
    # Le premier passage met de cote le fichier complet : les passages
    # suivants repartent toujours de lui, jamais d'un fichier deja reduit.
    if not os.path.exists(source):
        os.replace(chemin, source)
    avant = os.path.getsize(source)

    cmd = [sys.executable, '-m', 'fontTools.subset', source,
           '--text=' + BASE,
           '--output-file=' + chemin,
           '--flavor=woff2',
           '--layout-features=kern,liga,clig,calt,ccmp,locl,mark,mkmk',
           '--no-hinting',
           '--desubroutinize',
           '--name-IDs=1,2,3,4,6',
           '--drop-tables+=DSIG']
    # Les axes variables sont conserves : opsz de Fraunces sert au titre
    # de l'accueil, wght sert partout.
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print('ECHEC %s : %s' % (nom, r.stderr.strip()[:200]))
        continue
    apres = os.path.getsize(chemin)
    gain_total += avant - apres
    print('%-28s %6.0f Ko -> %5.0f Ko   (-%.0f %%)'
          % (nom, avant / 1024, apres / 1024, 100 * (avant - apres) / avant))


# Caveat n'est jamais appelee avec une graisse explicite : l'axe variable
# ne sert a rien et coute 20 Ko sur chaque page. On la fige.
for nom in ('caveat-latin.woff2', 'caveat-latin-ext.woff2'):
    chemin = D + nom
    if not os.path.exists(chemin):
        continue
    avant = os.path.getsize(chemin)
    ttf = '/tmp/' + nom.replace('.woff2', '.ttf')
    r1 = subprocess.run([sys.executable, '-m', 'fontTools.varLib.instancer',
                         chemin, 'wght=500', '-o', ttf], capture_output=True, text=True)
    if r1.returncode:
        print('figeage impossible pour %s' % nom)
        continue
    r2 = subprocess.run([sys.executable, '-m', 'fontTools.ttLib.woff2', 'compress',
                         ttf, '-o', chemin], capture_output=True, text=True)
    if r2.returncode:
        print('recompression impossible pour %s' % nom)
        continue
    apres = os.path.getsize(chemin)
    gain_total += avant - apres
    print('%-28s %6.0f Ko -> %5.0f Ko   (graisse figee a 500)'
          % (nom, avant / 1024, apres / 1024))

print('\ngain total : %.0f Ko' % (gain_total / 1024))

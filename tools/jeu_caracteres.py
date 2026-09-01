#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Caracteres conserves dans les polices du site.

Bien plus large que ce que le site utilise aujourd'hui, pour qu'un texte
ajoute demain reste correctement rendu. tools/audit.py verifie que chaque
page reste couverte : un caractere absent retombe sur une police systeme,
ce qui se voit immediatement.
"""

# Jeu de caracteres conserve : bien plus large que ce que le site utilise
# aujourd'hui, pour qu'un texte ajoute demain reste correctement rendu.
BASE = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'abcdefghijklmnopqrstuvwxyz'
    '0123456789'
    ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    # francais complet
    'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝŸÆŒ'
    'àáâãäåçèéêëìíîïñòóôõöùúûüýÿæœ'
    'ß'
    # latin etendu : noms propres et adresses etrangeres. L'adresse de
    # Hostinger, aux mentions legales, s'ecrit avec un S caron.
    'ŠšŽžĐđĆćČčŁłŃńŐőŘřŚśŤťŮůŰűŹźŻżĀāĒēĪīŌōŪūĂăŞşŢţÐðÞþ'
    # ponctuation et signes typographiques
    '«»“”‘’„‹›–—…·•·°№§¶†‡'
    # signes juridiques et commerciaux. Le © du pied de page figure sur
    # chaque page du site : son absence se voyait immediatement.
    '©®™℠'
    '€£¥¢₽'
    '×÷±≈≠≤≥∞µ'
    # fleches et puces employees dans les boutons et les listes
    '→←↑↓↗↘↙↖⟶▸►▪◆◇○●□■'
    # espaces particuliers : insecable et fine insecable
    '   '
)

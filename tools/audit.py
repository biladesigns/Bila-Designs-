#!/usr/bin/env python3
"""Controles rapides : titres, images, liens morts, restes de prototype."""
import re, sys, os, glob

R = '/root/bila-site/'
pages = ['accueil', 'services', 'avocats', 'contact', 'automatisations']
souci = 0

for p in pages:
    f = R + p + '/index.html'
    s = open(f, encoding='utf-8').read()
    corps = s[s.index('<main'):]

    h1 = len(re.findall(r'<h1\b', corps))
    imgs = re.findall(r'<img\b[^>]*>', corps)
    sans_alt = [i for i in imgs if 'alt=' not in i]
    # Les images calees en absolu ne tirent pas leur taille de leurs
    # attributs : seules les images du flux ont besoin de width/height.
    sans_dim = [i for i in imgs
                if 'position: absolute' not in i and not ('width=' in i and 'height=' in i)]
    reste = len(re.findall(r'\{\{|<sc-for|style-hover|x-import|x-dc', s))

    # ordre des titres
    niveaux = [int(m) for m in re.findall(r'<h([1-6])\b', corps)]
    saut = [(niveaux[i], niveaux[i+1]) for i in range(len(niveaux)-1)
            if niveaux[i+1] > niveaux[i] + 1]

    ok = h1 == 1 and not sans_alt and not reste and not saut
    souci += 0 if ok else 1
    print('%-16s h1=%d  img=%d (sans alt %d, sans dimensions %d)  restes=%d  sauts=%s  %s'
          % (p, h1, len(imgs), len(sans_alt), len(sans_dim), reste, saut or '-',
             'OK' if ok else 'A VOIR'))

# liens internes
cibles = set()
for f in glob.glob(R + '*/index.html') + [R + 'index.html']:
    cibles.add('/' + os.path.relpath(os.path.dirname(f), R).strip('.') + '/')
cibles = {c.replace('//', '/') for c in cibles}

morts = set()
for p in pages:
    s = open(R + p + '/index.html', encoding='utf-8').read()
    for href in re.findall(r'href="(/[^"#]*)(?:#[^"]*)?"', s):
        if href.startswith('/assets') or href.startswith('/public'):
            if not os.path.exists(R + href.lstrip('/')):
                morts.add(href)
            continue
        if os.path.splitext(href)[1]:
            if not os.path.exists(R + href.lstrip('/')):
                morts.add(href)
            continue
        if not href.endswith('/'):
            href += '/'
        if href not in cibles:
            morts.add(href)
print('\nliens internes morts :', sorted(morts) or 'aucun')
sys.exit(1 if (souci or morts) else 0)

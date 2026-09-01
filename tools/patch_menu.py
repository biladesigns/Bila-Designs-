#!/usr/bin/env python3
"""Ajoute le menu de telephone : un bouton et un panneau plein ecran.

En dessous de 768 px, la barre de navigation se repliait sur plusieurs
lignes. Ca tenait, mais ce n'etait pas un menu : c'etait une barre de
bureau qui deborde. Le panneau reprend la grammaire du site — filets de
1 px, angles vifs, losanges, Fraunces pour les entrees.
"""
import re, os, glob, html

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'

BOUTON = """<button type="button" class="menu-bouton" aria-expanded="false" aria-controls="menu-telephone" aria-label="Ouvrir le menu"><span class="menu-trait"></span><span class="menu-trait"></span></button>"""


def panneau(entrees, courante):
    lignes = []
    for i, (href, libelle) in enumerate(entrees, 1):
        actif = ' data-courante' if libelle == courante else ''
        lignes.append(
            '<a href="%s"%s class="menu-entree">'
            '<span class="menu-rang">%02d</span>'
            '<span class="menu-libelle">%s</span>'
            '<span class="menu-losange" aria-hidden="true"></span></a>'
            % (href, actif, i, libelle))
    return """<div id="menu-telephone" class="menu-panneau" hidden role="dialog" aria-modal="true" aria-label="Menu">
  <div class="menu-filets" aria-hidden="true"><span></span><span></span></div>
  <div class="menu-tete">
    <span class="menu-titre">Menu</span>
    <button type="button" class="menu-fermer" aria-label="Fermer le menu"><span></span><span></span></button>
  </div>
  <nav class="menu-liste">
    %s
  </nav>
  <div class="menu-pied">
    <a href="/contact/#formulaire" class="menu-cta">Démarrer un projet</a>
    <a href="mailto:mathieu@biladesigns.com" class="menu-contact">mathieu@biladesigns.com</a>
    <a href="tel:+33659086800" class="menu-contact menu-contact--sobre">06 59 08 68 00</a>
    <span class="menu-note">réponse sous vingt-quatre heures, par un humain</span>
  </div>
</div>""" % ('\n    '.join(lignes))


pages = sorted(glob.glob(R + '*/index.html')) + [R + 'index.html', R + 'accueil.html']
total = 0
for page in pages:
    if not os.path.exists(page):
        continue
    s = open(page, encoding='utf-8').read()
    if 'menu-panneau' in s or '<header' not in s:
        continue

    m = re.search(r'<header\b[^>]*>(.*?)</header>', s, re.S)
    if not m:
        continue
    tete = m.group(1)

    # Les entrees du menu sont celles de la barre : elles restent la seule
    # source, pour que les deux ne divergent jamais.
    entrees, courante = [], None
    for a in re.finditer(r'<a href="([^"]*)"([^>]*)>([^<]+)</a>', tete):
        href, attrs, libelle = a.group(1), a.group(2), html.unescape(a.group(3)).strip()
        if 'Bila Designs' in libelle or 'Démarrer un projet' in libelle:
            continue
        if 'aria-current' in attrs or href == '#':
            courante = libelle
            href = '#'
        entrees.append((href, libelle))
    if not entrees:
        continue

    s = s[:m.end(1)] + BOUTON + s[m.end(1):]
    fin = s.index('</header>', m.start()) + len('</header>')
    s = s[:fin] + '\n' + panneau(entrees, courante) + s[fin:]

    open(page, 'w', encoding='utf-8').write(s)
    total += 1
    print('%-34s %d entrees%s' % (os.path.relpath(page, R), len(entrees),
                                  ('  (courante : %s)' % courante) if courante else ''))

assert total, 'aucun menu pose'
print('total : %d pages' % total)

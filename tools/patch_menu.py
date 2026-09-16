#!/usr/bin/env python3
"""Le menu de telephone : bouton, sous-couches et panneau.

Le geste est repris du StaggeredMenu de React Bits, dont Mathieu voulait
l'allure : deux sous-couches colorees glissent l'une apres l'autre, le
panneau arrive par-dessus, puis les entrees montent en cascade depuis le
bas de leur ligne. La bibliotheque, elle, n'est pas reprise — ni React ni
GSAP : tout tient en transitions CSS decalees et en une quarantaine de
lignes de JavaScript.

Les couleurs, la typographie et les losanges viennent de la DA du site,
pas de celles du composant d'origine.

Le panneau ne porte que la navigation et l'appel a l'action : les
coordonnees et les reseaux y brouillaient la lecture, et ils sont deja
dans le pied de page, a un ecran de defilement.
"""
import re, os, glob, html

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'

BOUTON = (
    '<button type="button" class="menu-bouton" aria-expanded="false" '
    'aria-controls="menu-telephone" aria-label="Ouvrir le menu">'
    '<span class="menu-bouton-mots" aria-hidden="true">'
    '<span class="menu-bouton-defile"><span>Menu</span><span>Fermer</span></span></span>'
    '<span class="menu-bouton-croix" aria-hidden="true"><span></span><span></span></span>'
    '</button>'
)

def panneau(entrees, courante):
    lignes = []
    for i, (href, libelle) in enumerate(entrees, 1):
        actif = ' aria-current="page"' if libelle == courante else ''
        lignes.append(
            '<li class="menu-ligne">'
            '<span class="menu-rang" aria-hidden="true">%02d</span>'
            '<a class="menu-item" href="%s"%s><span class="menu-mot">%s</span></a>'
            '</li>' % (i, href, actif, libelle))

    return """<div class="menu-enveloppe">
  <div class="menu-souscouches" aria-hidden="true"><span></span><span></span></div>
  <aside id="menu-telephone" class="menu-panneau" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="menu-filets" aria-hidden="true"><span></span><span></span></div>
    <ul class="menu-liste" role="list">
      %s
    </ul>
    <div class="menu-pied">
      <a href="/contact/#formulaire" class="menu-cta">Démarrer un projet</a>
      <button type="button" class="menu-retour">
        <span aria-hidden="true">&larr;</span> Retour
      </button>
    </div>
  </aside>
</div>""" % ('\n      '.join(lignes),)


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

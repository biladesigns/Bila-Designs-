#!/usr/bin/env python3
"""Aligne la navigation et le pied de page sur le brief d'implementation.

La maquette de l'accueil porte encore l'ancienne barre de navigation
(Sites web & branding · Automatisations · Portfolio, en ancres internes).
Le brief demande la meme barre sur les quatre pages, avec Avocats en
troisieme entree et « Automatisations » qui mene toujours a la page
d'attente. C'est ce qui est applique ici.
"""
import re

R = '/root/bila-site/'
PAGES = ['accueil/index.html', 'services/index.html', 'avocats/index.html',
         'contact/index.html', 'automatisations/index.html']

# ── Barre de navigation de l'accueil ──────────────────────────────────────
s = open(R + 'accueil/index.html', encoding='utf-8').read()
NAV = [
    ('href="#expertises" style="white-space: nowrap; font-size: 14px; font-weight: 500; color: #2C3348;">Sites web &amp; branding',
     'href="/services/" style="white-space: nowrap; font-size: 14px; font-weight: 500; color: #2C3348;">Sites web &amp; branding'),
    ('href="#agents" style="white-space: nowrap; font-size: 14px; font-weight: 500; color: #2C3348;">Automatisations',
     'href="/automatisations/" style="white-space: nowrap; font-size: 14px; font-weight: 500; color: #2C3348;">Automatisations'),
    ('href="#realisations" style="white-space: nowrap; font-size: 14px; font-weight: 500; color: #2C3348;">Portfolio',
     'href="/avocats/" style="white-space: nowrap; font-size: 14px; font-weight: 500; color: #2C3348;">Avocats'),
]
for avant, apres in NAV:
    assert s.count(avant) == 1, 'entree de nav introuvable : %s' % avant[:40]
    s = s.replace(avant, apres, 1)

# Pied de page de l'accueil : les prestations menent a la page dediee.
s = s.replace('<a href="#expertises" style="font-size: 14px; color: #2C3348;">',
              '<a href="/services/" style="font-size: 14px; color: #2C3348;">')
open(R + 'accueil/index.html', 'w', encoding='utf-8').write(s)
print('accueil : navigation et pied de page alignes sur le brief')

# ── « Demarrer un projet » ────────────────────────────────────────────────
# Sur l'ancien site ce bouton menait a /nouveau-projet. Cette page n'existe
# plus dans la refonte : son role est tenu par le formulaire de la page
# Contact. L'ancienne adresse continue de fonctionner (redirection), mais
# le bouton mene desormais directement au formulaire.
CIBLE = '/contact/#formulaire'
for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()
    n = 0
    for motif in (r'href="#contact"(?=[^>]*background: #2743E3[^>]*>Démarrer un projet)',
                  r'href="#audit"(?=[^>]*background: #2743E3[^>]*>Démarrer un projet)',
                  r'href="#formulaire"(?=[^>]*background: #2743E3[^>]*>Démarrer un projet)'):
        s, k = re.subn(motif, 'href="%s"' % CIBLE, s)
        n += k
    open(chemin, 'w', encoding='utf-8').write(s)
    print('%-28s  bouton « Démarrer un projet » : %d' % (page, n))

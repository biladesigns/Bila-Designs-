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

# ── Normalisation de la barre de navigation sur toutes les pages ──────────
# Les maquettes de l'accueil et de la page « Sites web & branding » portaient
# encore l'ancienne barre : « Automatisations » y menait a une ancre de
# l'accueil, et la troisieme entree etait « Portfolio ». Le brief demande la
# meme barre partout, avec Avocats en troisieme entree et « Automatisations »
# qui mene toujours a la page dediee.
ENTREES = [
    (r'href="/accueil/#agents"(?=[^>]*>Automatisations<)', 'href="/automatisations/"'),
    (r'href="#agents"(?=[^>]*>Automatisations<)', 'href="/automatisations/"'),
]

for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()
    n = 0
    for motif, cible in ENTREES:
        s, k = re.subn(motif, cible, s)
        n += k
    # « Portfolio » en nav devient « Avocats » ; le portfolio reste accessible
    # depuis le pied de page et depuis l'accueil.
    m = re.search(r'<nav\b.*?</nav>', s, re.S)
    if m:
        nav = m.group(0)
        neuf = re.sub(r'href="/accueil/#realisations"([^>]*)>Portfolio<',
                      r'href="/avocats/"\1>Avocats<', nav)
        if neuf != nav:
            s = s.replace(nav, neuf, 1)
            n += 1
    open(chemin, 'w', encoding='utf-8').write(s)
    if n:
        print('%-28s  navigation corrigee : %d entree(s)' % (page, n))

# ── « Discutons » ─────────────────────────────────────────────────────────
# Le bouton ouvrait le logiciel de messagerie du visiteur. Il mene desormais
# au formulaire, comme « Demarrer un projet ».
for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()
    s, k = re.subn(r'href="mailto:mathieu@biladesigns\.com"(?=[^>]*background: #2743E3[^>]*>Discutons)',
                   'href="%s"' % CIBLE, s)
    if k:
        print('%-28s  bouton « Discutons » -> %s' % (page, CIBLE))
    open(chemin, 'w', encoding='utf-8').write(s)

# ── Les appels a l'action menent au formulaire ────────────────────────────
# « Cadrer mon premier agent », « Donner vie a votre projet », « En parler
# dix minutes » pointaient vers l'ancre #contact de leur propre page. Cette
# ancre mene a un bloc qui affiche une adresse et un numero, pas un
# formulaire : le visiteur arrivait au bout de sa lecture sans rien a
# remplir. Ils menent desormais au formulaire de la page Contact.
# Les ancres #audit ne changent pas : elles pointent deja sur un formulaire.
for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()
    avant = s
    s = re.sub(r'href="#contact"(?=[^>]*>(?:[^<]*)?(?:Donner vie|Parler de votre|Cadrer mon|En parler|Discutons))',
               'href="/contact/#formulaire"', s)
    # le lien « Contact » du pied de page mene a la page, pas a une ancre
    s = s.replace('<a href="#contact" style="font-size: 14px; color: #2C3348;">Contact</a>',
                  '<a href="/contact/" style="font-size: 14px; color: #2C3348;">Contact</a>')
    if s != avant:
        open(chemin, 'w', encoding='utf-8').write(s)
        n = len(re.findall(r'/contact/#formulaire', s))
        print('%-28s  %d lien(s) vers le formulaire' % (page, n))

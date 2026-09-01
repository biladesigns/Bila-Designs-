#!/usr/bin/env python3
"""Cable la page contact : pastilles a choix unique, formulaires postables."""
import re, sys, html

CHEMIN = '/root/bila-site/contact/index.html'
s = open(CHEMIN, encoding='utf-8').read()

# Le style d'une pastille, repris a l'identique de renderVals() dans la maquette.
BASE = ("display: inline-flex; align-items: center; padding: 10px 17px; cursor: pointer; "
        "white-space: nowrap; font-size: 14px; "
        "transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease; ")
ETEINT = "border: 1px solid rgba(16,27,51,0.2); background: transparent; color: #4A5163;"
ALLUME = "border: 1px solid #2743E3; background: #2743E3; color: #FFFFFF;"

GROUPES = {
    'sujets':  ('sujet',  'C’est a propos de quoi',
                ['Un site web', 'Une identite, un logo', "De l'automatisation",
                 'Le tout', 'Je ne sais pas encore'], 'Un site web'),
    'budgets': ('budget', 'Votre budget',
                ['moins de 1 500 €', '1 500 a 3 000 €', '3 000 a 6 000 €',
                 'plus de 6 000 €', 'je ne sais pas'], 'je ne sais pas'),
    'delais':  ('delai',  'Pour quand',
                ['des que possible', 'ce mois-ci', 'dans un a trois mois',
                 'je me renseigne'], 'je me renseigne'),
}


def pastilles(cle):
    champ, _, options, defaut = GROUPES[cle]
    out = []
    for i, opt in enumerate(options):
        coche = ' checked' if opt == defaut else ''
        style = BASE + (ALLUME if opt == defaut else ETEINT)
        out.append(
            '<label class="pastille" style="%s">'
            '<input type="radio" name="%s" value="%s"%s>%s</label>'
            % (style, champ, html.escape(opt, quote=True), coche, html.escape(opt)))
    return '\n              '.join(out)


for cle in GROUPES:
    motif = re.compile(
        r'<sc-for list="\{\{ %s \}\}"[^>]*>\s*'
        r'<span onClick="\{\{ o\.pick \}\}" style="\{\{ o\.style \}\}">\{\{ o\.label \}\}</span>\s*'
        r'</sc-for>' % cle)
    s, n = motif.subn(pastilles(cle), s)
    assert n == 1, 'groupe %s : %d remplacement(s)' % (cle, n)

# Chaque bloc de pastilles devient un groupe repere pour bila-ui.js, et le
# libelle qui le precede devient la legende du groupe.
s = s.replace('<div style="display: flex; flex-wrap: wrap; gap: 10px;">',
              '<div data-pastilles role="radiogroup" style="display: flex; flex-wrap: wrap; gap: 10px;">')

assert s.count('data-pastilles') == 3, 'groupes de pastilles : %d' % s.count('data-pastilles')
open(CHEMIN, 'w', encoding='utf-8').write(s)
print('pastilles cablees : %d groupes' % s.count('data-pastilles'))

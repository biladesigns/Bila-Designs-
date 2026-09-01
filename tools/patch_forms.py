#!/usr/bin/env python3
"""Rend les formulaires reellement postables, sans toucher a leur apparence.

Trois formulaires : la barre d'audit gratuit (accueil, avocats, services,
contact) et le formulaire de contact. Les maquettes n'ont ni nom de champ,
ni validation, ni action : tout est ajoute ici.
"""
import re, os

R = '/root/bila-site/'
PAGES = ['accueil/index.html', 'services/index.html', 'avocats/index.html',
         'contact/index.html', 'automatisations/index.html']

PIEGE = ('<input type="text" name="_honey" tabindex="-1" autocomplete="off" '
         'class="piege" aria-hidden="true">')

# La mention de finalite occupe sa propre ligne : la barre d'audit garde
# ainsi exactement la composition de la maquette (lien, adresse, bouton).
FINALITE = ('<span style="flex: 1 0 100%; margin-top: 4px; font-size: 12px; '
            'line-height: 1.6; color: #8A8F9C;">'
            'Votre adresse ne sert qu’a vous envoyer cet audit. '
            '<a href="/politique-confidentialite/" style="color: #8A8F9C; '
            'text-decoration: underline;">En savoir plus</a>.</span>')

RETOUR = ('<span class="form-retour" role="status" aria-live="polite" '
          'style="flex: 1 0 100%%; %s"></span>')


def champ(bloc, motif, ajouts):
    """Ajoute des attributs a la premiere balise input/textarea qui correspond."""
    m = re.search(motif, bloc)
    assert m, 'champ introuvable : %s' % motif[:60]
    balise = m.group(0)
    return bloc.replace(balise, balise[:-1].rstrip() + ' ' + ajouts + '>', 1)


def cabler_audit(bloc):
    """Barre d'audit : lien du site + adresse, les deux requis."""
    bloc = champ(bloc, r'<input type="url"[^>]*>',
                 'name="site" required aria-label="Adresse de votre site" '
                 'data-libelle="l’adresse de votre site" data-site autocomplete="url" '
                 'inputmode="url" spellcheck="false"')
    # « type=url » impose une adresse complete avec son protocole. Un
    # visiteur tape « moncabinet.fr », pas « https://moncabinet.fr » : le
    # navigateur refusait alors la saisie la plus naturelle. Le champ
    # devient un champ texte, et bila-ui.js complete l'adresse.
    bloc = re.sub(r'(<input )type="url"(?=[^>]*name="site")', r'\1type="text"', bloc)
    bloc = champ(bloc, r'<input type="email"[^>]*>',
                 'name="email" required aria-label="Votre adresse electronique" '
                 'data-libelle="votre adresse electronique" autocomplete="email"')
    ouvre = re.match(r'<form[^>]*>', bloc).group(0)
    neuf = (ouvre[:-1].rstrip() +
            ' data-form data-sujet="Audit gratuit — demande depuis le site"'
            ' data-merci="Bien reçu. Vous recevez l’audit sous vingt-quatre heures."'
            ' method="post" action="https://formsubmit.co/matbila63@gmail.com"'
            ' novalidate>')
    bloc = bloc.replace(ouvre, neuf, 1)
    bloc = bloc.replace('</form>', '  ' + PIEGE + '\n      ' + FINALITE +
                        '\n      ' + (RETOUR % '') + '\n    </form>', 1)
    return bloc


total = {'audit': 0, 'contact': 0}

for page in PAGES:
    chemin = R + page
    s = open(chemin, encoding='utf-8').read()

    # ── Barres d'audit ─────────────────────────────────────────────────────
    def remplacer(m):
        bloc = m.group(0)
        if '<textarea' in bloc or 'data-form' in bloc:
            return bloc
        if 'type="url"' not in bloc or 'type="email"' not in bloc:
            return bloc
        total['audit'] += 1
        return cabler_audit(bloc)

    s = re.sub(r'<form[^>]*>.*?</form>', remplacer, s, flags=re.S)

    # ── Formulaire de contact ──────────────────────────────────────────────
    # La maquette n'a pas de <form> : le bloc interne du cadre lumineux en
    # tient lieu. On le transforme en <form>, styles inchanges.
    if 'id="formulaire"' in s:
        ancre = ('<div style="position: relative; z-index: 1; flex: 1 1 auto; '
                 'box-sizing: border-box; background: #FBFBFA; padding: 44px 40px 40px; '
                 'display: flex; flex-direction: column; gap: 36px;">')
        assert s.count(ancre) == 1, 'bloc de contact introuvable'
        forme = ('<form data-form method="post" '
                 'action="https://formsubmit.co/matbila63@gmail.com" novalidate '
                 'data-sujet="Nouveau projet — message depuis biladesigns.com" '
                 'data-merci="Bien reçu. Je vous reponds sous vingt-quatre heures." '
                 + ancre[len('<div'):])
        s = s.replace(ancre, forme, 1)

        # La fermeture correspondante : le </div> qui precede la fermeture du
        # cadre lumineux, juste apres le bloc du bouton d'envoi.
        fin = ('</span>\n        </div>\n      </div>\n    </div>\n')
        assert s.count(fin) == 1, 'fermeture du formulaire introuvable (%d)' % s.count(fin)
        s = s.replace(fin, '</span>\n        </div>\n      </form>\n    </div>\n', 1)

        s = champ(s, r'<input type="text" placeholder="Prénom Nom"[^>]*>',
                  'name="nom" required data-libelle="votre nom" autocomplete="name"')
        s = champ(s, r'<input type="email" placeholder="vous@exemple\.fr"[^>]*>',
                  'name="email" required data-libelle="votre adresse electronique" '
                  'autocomplete="email"')
        s = champ(s, r'<input type="text" placeholder="Cabinet, société…"[^>]*>',
                  'name="entreprise" autocomplete="organization"')
        s = champ(s, r'<input type="url" placeholder="votre-site\.fr"(?![^>]*name=)[^>]*>',
                  'name="site" data-site autocomplete="url" inputmode="url" spellcheck="false"')
        s = re.sub(r'(<input )type="url"(?=[^>]*name="site")', r'\1type="text"', s)
        s = s.replace('<textarea rows="5"',
                      '<textarea rows="5" name="message" required '
                      'data-libelle="votre message"', 1)
        # Piege a robots et zone de retour, dans le pied du formulaire.
        s = s.replace('<span style="font-size: 13px; line-height: 1.6; color: #8A8F9C;">'
                      'Vos informations ne servent qu\'à vous répondre.</span>',
                      PIEGE + '<span style="font-size: 13px; line-height: 1.6; color: #8A8F9C;">'
                      'Vos informations ne servent qu\'à vous répondre. '
                      '<a href="/politique-confidentialite/" style="color: #8A8F9C; '
                      'text-decoration: underline;">En savoir plus</a>.</span>'
                      + (RETOUR % 'margin-top: 6px;'), 1)
        total['contact'] += 1

    open(chemin, 'w', encoding='utf-8').write(s)

print('barres d’audit cablees : %d' % total['audit'])
print('formulaire de contact  : %d' % total['contact'])
assert total['audit'] == 4 and total['contact'] == 1, 'compte inattendu'

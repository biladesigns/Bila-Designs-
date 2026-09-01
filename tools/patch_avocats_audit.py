#!/usr/bin/env python3
"""Remplace la section de constats de la page Avocats par une accroche simple.

La section « Je commence toujours par regarder » deroulait trois constats
d'audit dans un systeme de jalons cliquables. Mathieu la voulait remplacee
par ce qu'il avait demande des le depart : sous le heros, une phrase et la
barre d'audit, rien de plus.

La barre d'audit elle-meme est conservee : elle etait imbriquee dans cette
section, c'est elle qui recolte les demandes.

Le bloc retire se terminait par la fermeture du conteneur qui portait
les filets verticaux de la section : elle est reecrite, sans quoi la
section suivante se retrouve imbriquee dans celle-ci.
"""
import re, os

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
CHEMIN = R + 'avocats/index.html'
s = open(CHEMIN, encoding='utf-8').read()

debut = s.index('  <div style="position: relative; z-index: 2; padding: 0 var(--gut); display: flex; '
                'flex-direction: column; align-items: flex-start; gap: 20px;">')
fin = s.index('<div id="audit"')

REMPLACEMENT = """  <div style="position: relative; z-index: 2; padding: 0 var(--gut); display: flex; flex-direction: column; align-items: flex-start; gap: 20px;">
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #2743E3;">L'existant d'abord</span>
    <h2 style="margin: 0; max-width: 760px; font-family: 'Fraunces', Georgia, serif; font-weight: 500; font-size: clamp(26px, 16.3px + 2.47vw, 52px); line-height: 1.08; letter-spacing: -0.02em;">Je commence toujours par regarder.</h2>
    <p style="margin: 0; max-width: 620px; font-size: 16px; line-height: 1.7; color: #4A5163; text-wrap: pretty;">J'audite le site avant de proposer quoi que ce soit. Envoyez-moi le lien du votre : vous recevez le relevé sous vingt-quatre heures.</p>
    <span style="font-family: 'Caveat', cursive; font-size: 22px; color: #4A5163; transform: rotate(-1deg); display: inline-block; margin-top: 2px;">sur le dernier cabinet, vingt-six points sont ressortis</span>
  </div>

  <div style="height: 56px;"></div>
  </div>

  """

s = s[:debut] + REMPLACEMENT + s[fin:]

# Les donnees des constats ne servent plus ; celles de la chaine du dossier
# restent necessaires.
import json
m = re.search(r'<script type="application/json" id="donnees-avocats">(.*?)</script>', s, re.S)
if m:
    d = json.loads(m.group(1))
    d.pop('constats', None)
    s = s[:m.start(1)] + json.dumps(d, ensure_ascii=False) + s[m.end(1):]

assert 'data-groupe="constats"' not in s, 'jalons de constats encore presents'
assert 'id="audit"' in s, 'barre d audit perdue'
open(CHEMIN, 'w', encoding='utf-8').write(s)
print('avocats : constats remplaces par l accroche, barre d audit conservee')

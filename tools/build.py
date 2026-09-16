#!/usr/bin/env python3
"""Reconstruit les cinq pages du site a partir des maquettes."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from dc_convert import main

M = '/root/.claude/uploads/f995dfca-f70d-49dc-aa7b-9369b5e2150d/'
R = '/root/bila-site/'

PAGES = [
    dict(src=M + '90932b00-Hero_Bila_Designs.dc.html', out=R + 'accueil/index.html',
         nav_active='accueil', canonical='/accueil/',
         title='Bila Designs — sites web, IA et automatisations',
         desc="Studio indépendant à Lyon. Sites web sur mesure, identité de marque, automatisations et agents IA, conçus avec exigence et accompagnés humainement.",
         preload_hero='/assets/img/hero-arche-crop.webp'),
    dict(src=M + '17727c2e-Sites_web_et_branding.dc.html', out=R + 'services/index.html',
         nav_active='services', canonical='/services/',
         title='Sites web & branding — Bila Designs',
         desc="Notre processus de création : stratégie et identité, interface web, rebranding global. Le référencement est traité dès le cadrage, jamais en option.",
         preload_hero='/assets/img/hero-atelier.webp'),
    dict(src=M + '26ee78d5-Avocats.dc.html', out=R + 'avocats/index.html',
         nav_active='avocats', canonical='/avocats/',
         title="Sites web et agents IA pour cabinets d'avocats — Bila Designs",
         desc="Audit gratuit de votre site, refonte et référencement pour cabinets d'avocats. Cinq sujets où un agent vous enlève du travail, dans le respect de la déontologie.",
         preload_hero='/assets/img/hero-avocats.webp',
         og='og-avocats.png'),
    dict(src=M + 'c4270276-Contact.dc.html', out=R + 'contact/index.html',
         nav_active='contact', canonical='/contact/',
         title='Contact — Bila Designs',
         desc="Parlons de votre projet : site web, identité ou automatisation. Un seul interlocuteur, celui qui fera le travail. Réponse sous vingt-quatre heures."),
    dict(src=M + '7cca7f16-Automatisations.dc.html', out=R + 'automatisations/index.html',
         nav_active='automatisations', canonical='/automatisations/',
         title='Automatisations — Bila Designs',
         desc="Page en cours de refonte. Les automatisations et les agents IA sont présentés sur la page d'accueil.",
         noindex=True),
]


# ── Corrections de maquette ────────────────────────────────────────────────
# Deux maquettes ont une balise <div> non fermee. Ce n'est pas visible dans
# le prototype (le navigateur repare a la volee) mais ca casse la structure
# de la page finale : la section suivante se retrouve imbriquee dans la
# precedente. On referme au bon endroit, sans rien changer d'autre.
CORRECTIONS = [
    # Accueil : le bandeau "Ils nous font confiance". La piste du defilement
    # n'est jamais refermee avant la fin de la section.
    (R + 'accueil/index.html',
     "      </div>\n    </div>\n  </div>\n</section>",
     "      </div>\n    </div>\n  </div>\n</div>\n</section>"),
    # Avocats : le bandeau d'audit gratuit, ouvert en #audit, n'est pas
    # referme avant la fin de la section "Je commence toujours par regarder".
    (R + 'avocats/index.html',
     "      </form>\n    </div>\n\n</section>",
     "      </form>\n    </div>\n  </div>\n\n</section>"),
]


for p in PAGES:
    main(**p)

for chemin, avant, apres in CORRECTIONS:
    s = open(chemin, encoding='utf-8').read()
    n = s.count(avant)
    assert n == 1, 'correction non appliquable (%d occurrences) : %s' % (n, chemin)
    open(chemin, 'w', encoding='utf-8').write(s.replace(avant, apres))
    print('correction        -> %s' % chemin)

#!/usr/bin/env python3
"""Cable les deux systemes interactifs de la page Avocats.

  - les trois constats d'audit (jalons cliquables + panneau de detail)
  - la chaine du dossier en cinq onglets

Le contenu et les styles sont repris mot pour mot de la classe Component
de la maquette (constatData / stepData / renderVals). Rien n'est reformule.
"""
import re, json, html

CHEMIN = '/root/bila-site/avocats/index.html'
s = open(CHEMIN, encoding='utf-8').read()

MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

CONSTATS = [
    {"num": "01", "label": "Domaines", "title": "Aucune page par domaine", "tag": "Structure",
     "body": "Le site annonce douze domaines d'intervention, mais aucun n'a sa propre page. "
             "Quand on cherche « avocat droit du travail », il n'y a rien à proposer.",
     "fix": "Une page par domaine, écrite avec vous, et un maillage qui les relie."},
    {"num": "02", "label": "Fiche", "title": "La fiche d'identité est vide", "tag": "Données locales",
     "body": "Ni adresse, ni téléphone, ni horaires déclarés sous forme exploitable. C'est pourtant "
             "ce sur quoi Google et les assistants s'appuient pour situer un cabinet.",
     "fix": "Données structurées, fiche Google et annuaires alignés sur le même NAP."},
    {"num": "03", "label": "Publications", "title": "Les articles sont invisibles", "tag": "Autorité",
     "body": "Des années de publications, des passages en télévision, des colloques du Barreau, "
             "et pas un lien du site qui y mène.",
     "fix": "Une page presse et publications, reliée depuis chaque domaine concerné."},
]

STEPS = [
    {"label": "Acquisition", "title": "Développer la clientèle",
     "sub": "Acquisition · le bouche-à-oreille ne suffit plus",
     "probleme": "L'essentiel des nouveaux dossiers vient de la recommandation. Chacun publie quand il a le temps, c'est-à-dire rarement, et les quelques heures passées sur les réseaux ne se transforment presque jamais en rendez-vous.",
     "branche": "Un agent de veille suit les évolutions de vos domaines et alimente un agent qui rédige des propositions de publications. Un troisième trie les messages entrants et vous signale ceux qui méritent votre attention. Chaque texte passe un contrôle déontologique avant de vous être soumis.",
     "chips": ["Veille juridique", "Rédaction assistée", "Tri des messages", "Contrôle déontologique"],
     "change": "Vous publiez régulièrement sans y penser, et vous ne lisez que les messages qui valent votre temps. Le temps passé sur les réseaux se compte en minutes, plus en heures.",
     "decide": "Zéro publication automatique. Aucun texte, aucun message ne part sans votre clic. Les règles de communication sont posées avec vous, et vérifiables."},
    {"label": "Ouverture du dossier", "title": "Conflits d'intérêts et déontologie",
     "sub": "Ouverture du dossier · la vérification qui prend une matinée",
     "probleme": "Chaque nouveau dossier demande une vérification manuelle, souvent sur un tableur tenu à la main. C'est long, c'est fastidieux, et un conflit manqué expose le cabinet bien au-delà du désagrément.",
     "branche": "Vos dossiers passés sont mis en base, anonymisés. À chaque nouveau dossier, l'agent croise les parties, les adverses et les bénéficiaires effectifs, puis produit une note d'analyse assortie d'un degré de certitude.",
     "chips": ["Base de dossiers", "Croisement des parties", "Note d'analyse", "Journalisation"],
     "change": "La vérification passe de plusieurs dizaines de minutes à quelques-unes, et la décision d'ouvrir ou non se prend le jour même plutôt qu'en fin de semaine.",
     "decide": "L'agent ne tranche aucune question déontologique. Chaque vérification donne lieu à une décision d'associé, horodatée et journalisée."},
    {"label": "Recherche", "title": "La recherche jurisprudentielle",
     "sub": "Recherche · le poste le plus lourd des collaborateurs",
     "probleme": "Un dossier complexe demande plusieurs heures de recherche, et cette recherche est souvent refaite ailleurs dans le cabinet sans que personne ne le sache. La jurisprudence la plus récente passe régulièrement à côté.",
     "branche": "Un agent interroge vos bases documentaires, hiérarchise les décisions par autorité et rédige une synthèse. Un second vérifie chaque citation contre la base avant qu'elle n'entre dans la note.",
     "chips": ["Bases documentaires", "Hiérarchisation", "Synthèse", "Vérification des citations"],
     "change": "La recherche se fait en une fraction du temps, elle n'est plus dupliquée entre équipes, et la jurisprudence récente cesse d'être oubliée.",
     "decide": "Chaque citation est vérifiée contre la base, ou explicitement marquée « à vérifier ». L'associé relit chaque synthèse avant usage."},
    {"label": "Audience", "title": "Le mémo de plaidoirie",
     "sub": "Audience · la chronologie reconstruite à la main",
     "probleme": "Préparer une audience importante demande une journée, dont une bonne part passée à reconstruire la chronologie à partir de dizaines, parfois de centaines de pièces. Le mémo se termine souvent la veille.",
     "branche": "L'agent lit les pièces du dossier, reconstruit la chronologie des faits, va chercher la jurisprudence utile et propose une première version du mémo, que vous reprenez et affinez.",
     "chips": ["Lecture des pièces", "Chronologie", "Jurisprudence", "Pré-rédaction"],
     "change": "La préparation se concentre sur le raisonnement plutôt que sur la mise en ordre, et le mémo cesse de se boucler dans les dernières heures.",
     "decide": "L'agent ne signe rien, ne dépose rien au greffe, ne parle jamais à un tiers. Vous restez seul signataire."},
    {"label": "Facturation", "title": "Les honoraires jamais saisis",
     "sub": "Facturation · le temps travaillé qui n'arrive pas sur la facture",
     "probleme": "Des heures réellement travaillées ne sont jamais saisies, parce que la fiche se remplit des jours après. Et une part des factures dépasse largement l'échéance sans qu'aucune relance ne parte.",
     "branche": "L'agent lit vos échanges et votre agenda, pré-remplit chaque fiche de temps avec le dossier et son justificatif, et déclenche les relances d'impayés selon le rythme que vous fixez.",
     "chips": ["Agenda et messagerie", "Fiches de temps", "Justificatifs", "Relances échelonnées"],
     "change": "Le temps travaillé se retrouve sur la facture, et les impayés cessent de vieillir en silence.",
     "decide": "Aucune fiche de temps n'est validée automatiquement. Passé un certain retard, aucune relance ne part sans revue de l'associé."},
]


def e(t):
    return html.escape(t, quote=True)


# ── Les trois jalons de constat ───────────────────────────────────────────
def dot(idx, etat):
    """etat : 'actif' | 'avant' (deja parcouru) | 'apres'."""
    bord = '#2743E3' if etat in ('actif', 'avant') else 'rgba(16,27,51,0.22)'
    fond = '#2743E3' if etat == 'actif' else 'transparent'
    return ('flex: 0 0 auto; display: flex; align-items: center; justify-content: center; '
            'width: 34px; height: 34px; border: 1px solid %s; background: %s; '
            'transform: rotate(45deg); cursor: pointer; '
            'transition: background 0.3s ease, border-color 0.3s ease;' % (bord, fond))


def num(etat):
    couleur = '#FFFFFF' if etat == 'actif' else ('#2743E3' if etat == 'avant' else '#8A8F9C')
    return ('transform: rotate(-45deg); font-family: %s; font-size: 11px; color: %s;'
            % (MONO, couleur))


def lien(idx, dernier):
    """Le filet entre deux jalons : bleu tant qu'on n'a pas depasse l'actif."""
    cache = ' display: none;' if dernier else ''
    return ('flex: 1 1 auto; height: 1px; margin: 0 10px; background: %s;' + cache)


def libelle(etat):
    return ('flex: 1 1 0; min-width: 0; min-height: 20px; padding-right: 14px; font-size: 12px; '
            'letter-spacing: 0.14em; text-transform: uppercase; cursor: pointer; color: %s;'
            % ('#101B33' if etat == 'actif' else '#8A8F9C'))


jalons = []
for i, c in enumerate(CONSTATS):
    dernier = i == len(CONSTATS) - 1
    fin = ' display: none;' if dernier else ''
    jalons.append(
        '<div style="display: flex; align-items: center; flex: 1 1 0; min-width: 0;">'
        '<button type="button" data-choix="%d" role="tab" aria-selected="%s" tabindex="%s" '
        'aria-controls="constat-panneau" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" '
        'style="%s">'
        '<span data-choix-enfant="%d" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" '
        'style="%s">%s</span>'
        '<span class="piege">%s</span></button>'
        '<span data-lien="%d" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" style="%s"></span>'
        '</div>'
        % (i, 'true' if i == 0 else 'false', '0' if i == 0 else '-1',
           e(dot(i, 'actif')), e(dot(i, 'avant')), e(dot(i, 'apres')), dot(i, 'actif' if i == 0 else 'apres'),
           i, e(num('actif')), e(num('avant')), e(num('apres')), num('actif' if i == 0 else 'apres'), c['num'],
           e(c['label']),
           i,
           e('flex: 1 1 auto; height: 1px; margin: 0 10px; background: rgba(16,27,51,0.18);' + fin),
           e('flex: 1 1 auto; height: 1px; margin: 0 10px; background: #2743E3;' + fin),
           e('flex: 1 1 auto; height: 1px; margin: 0 10px; background: rgba(16,27,51,0.18);' + fin),
           'flex: 1 1 auto; height: 1px; margin: 0 10px; background: rgba(16,27,51,0.18);' + fin))

etiquettes = []
for i, c in enumerate(CONSTATS):
    etiquettes.append(
        '<span data-choix-enfant="%d" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" '
        'style="%s" aria-hidden="true">%s</span>'
        % (i, e(libelle('actif')), e(libelle('apres')), e(libelle('apres')),
           libelle('actif' if i == 0 else 'apres'), e(c['label'])))

bloc = re.compile(
    r'<sc-for list="\{\{ constats \}\}"[^>]*>\s*'
    r'<div style="display: flex; align-items: center; flex: 1 1 0; min-width: 0;">.*?</div>\s*'
    r'</sc-for>', re.S)
s, n = bloc.subn('\n        '.join(jalons), s)
assert n == 1, 'jalons : %d' % n

bloc = re.compile(
    r'<sc-for list="\{\{ constats \}\}"[^>]*>\s*'
    r'<span onClick="\{\{ c\.select \}\}" style="\{\{ c\.labelStyle \}\}">\{\{ c\.label \}\}</span>\s*'
    r'</sc-for>', re.S)
s, n = bloc.subn('\n        '.join(etiquettes), s)
assert n == 1, 'etiquettes : %d' % n

# ── Les cinq onglets de la chaine du dossier ──────────────────────────────
def onglet(idx, actif):
    st = ('position: relative; flex: 1 1 0; min-width: 0; box-sizing: border-box; display: flex; '
          'flex-direction: column; gap: 10px; padding: 22px 18px 24px; cursor: pointer; '
          'background: transparent;')
    if idx:
        st += ' border-left: 1px solid rgba(16,27,51,0.14);'
    if actif:
        st += ' box-shadow: inset 0 3px 0 0 #2743E3;'
    return st


def onglet_num(actif):
    return ('font-family: %s; font-size: 11px; letter-spacing: 0.14em; color: %s;'
            % (MONO, '#2743E3' if actif else 'rgba(16,27,51,0.35)'))


def onglet_lib(actif):
    return ('font-family: Fraunces, Georgia, serif; font-size: 19px; line-height: 1.2; '
            'letter-spacing: -0.01em; color: %s;'
            % ('#101B33' if actif else 'rgba(16,27,51,0.42)'))


onglets = []
for i, st in enumerate(STEPS):
    onglets.append(
        '<button type="button" data-choix="%d" role="tab" aria-selected="%s" tabindex="%s" '
        'aria-controls="chaine-panneau" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" style="%s">'
        '<span data-choix-enfant="%d" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" style="%s">%02d</span>'
        '<span data-choix-enfant="%d" data-s-actif="%s" data-s-avant="%s" data-s-apres="%s" style="%s">%s</span>'
        '</button>'
        % (i, 'true' if i == 0 else 'false', '0' if i == 0 else '-1',
           e(onglet(i, True)), e(onglet(i, False)), e(onglet(i, False)), onglet(i, i == 0),
           i, e(onglet_num(True)), e(onglet_num(False)), e(onglet_num(False)), onglet_num(i == 0), i + 1,
           i, e(onglet_lib(True)), e(onglet_lib(False)), e(onglet_lib(False)), onglet_lib(i == 0), e(st['label'])))

bloc = re.compile(
    r'<sc-for list="\{\{ steps \}\}"[^>]*>\s*'
    r'<a href="#agents" onClick="\{\{ s\.select \}\}" style="\{\{ s\.tabStyle \}\}">.*?</a>\s*'
    r'</sc-for>', re.S)
s, n = bloc.subn('\n        '.join(onglets), s)
assert n == 1, 'onglets : %d' % n

# Les etiquettes de la carte navy sont reconstruites par le script.
bloc = re.compile(
    r'<sc-for list="\{\{ active\.chips \}\}"[^>]*>\s*'
    r'<span style="([^"]*)">\{\{ chip\.label \}\}</span>\s*'
    r'</sc-for>', re.S)
m = bloc.search(s)
assert m, 'etiquettes de la carte navy introuvables'
s = bloc.sub('<span data-liste="steps.chips" data-style-item="%s"></span>' % e(m.group(1)), s)

# ── Les emplacements de texte pilotes par la selection ────────────────────
for cle in ('num', 'title', 'tag', 'body', 'fix'):
    s = s.replace('{{ activeConstat.%s }}' % cle,
                  '<span data-champ="constats.%s"></span>' % cle)
for cle in ('num', 'title', 'sub', 'probleme', 'branche', 'change', 'decide'):
    s = s.replace('{{ active.%s }}' % cle,
                  '<span data-champ="steps.%s"></span>' % cle)

assert '{{' not in s and '<sc-for' not in s, 'marqueurs restants'

# ── Reperes de groupe + donnees ───────────────────────────────────────────
ancre = '<div style="position: relative; z-index: 2; margin: 60px var(--gut) 0;">'
assert s.count(ancre) == 1
s = s.replace(ancre, '<div data-groupe="constats" data-actif="0"' + ancre[len('<div'):], 1)

ancre = '<div style="position: relative; z-index: 2; margin: 64px var(--gut) 0;">'
assert s.count(ancre) == 1
s = s.replace(ancre, '<div data-groupe="steps" data-actif="0"' + ancre[len('<div'):], 1)

# Les barres d'onglets deviennent de vraies listes d'onglets pour le clavier.
s = s.replace('<div style="display: flex; align-items: center; gap: 0;">',
              '<div role="tablist" aria-label="Constats de l’audit" '
              'style="display: flex; align-items: center; gap: 0;">', 1)
s = s.replace('<div style="display: flex; align-items: stretch; border-top: 1px solid rgba(16,27,51,0.22); '
              'border-bottom: 1px solid rgba(16,27,51,0.14);">',
              '<div role="tablist" aria-label="Chaîne du dossier" '
              'style="display: flex; align-items: stretch; border-top: 1px solid rgba(16,27,51,0.22); '
              'border-bottom: 1px solid rgba(16,27,51,0.14);">', 1)

# Les deux panneaux, reperes pour aria-controls et aria-live.
ancre = ('<div style="margin-top: 40px; border-top: 1px solid rgba(16,27,51,0.22); '
         'display: grid; grid-template-columns: 320px minmax(0, 1fr); gap: 0;" class="g-2">')
assert s.count(ancre) == 1, 'panneau des constats introuvable'
s = s.replace(ancre, ancre[:-1].replace('<div', '<div id="constat-panneau" role="tabpanel" aria-live="polite"', 1) + '>', 1)

ancre = '<div style="margin-top: 48px; display: flex; flex-direction: column; gap: 8px;">'
assert s.count(ancre) == 1, 'panneau de la chaine introuvable'
s = s.replace(ancre, '<div id="chaine-panneau" role="tabpanel" aria-live="polite"' + ancre[len('<div'):], 1)

donnees = json.dumps({'constats': CONSTATS, 'steps': STEPS}, ensure_ascii=False)
s = s.replace('</main>',
              '<script type="application/json" id="donnees-avocats">%s</script>\n</main>' % donnees, 1)

open(CHEMIN, 'w', encoding='utf-8').write(s)
print('avocats : %d constats, %d etapes cables' % (len(CONSTATS), len(STEPS)))

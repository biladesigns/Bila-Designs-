#!/usr/bin/env python3
"""En-tete et pied de page communs, repris a l'identique des maquettes."""

MONO = "ui-monospace, 'SFMono-Regular', Menlo, monospace"

NAV = [
    ('Sites web &amp; branding', '/services/', 'services'),
    ('Automatisations',          '/automatisations/', 'automatisations'),
    ('Avocats',                  '/avocats/', 'avocats'),
]


def marque(corps=28):
    """Le logotype « Deux encres », compose en texte.

    Deux lettres en Fraunces 600 imprimees l'une sur l'autre : le
    recouvrement produit une troisieme encre, et c'est lui qui fait la
    marque. Voir assets/marque/LISEZ-MOI-logo.md."""
    return ('<span class="logo" style="font-size: %dpx;">'
            '<span class="logo-bd" aria-hidden="true">'
            '<span class="logo-b">B</span><span class="logo-d">D</span></span>'
            '<span class="logo-filet" aria-hidden="true"></span>'
            '<span class="logo-nom">Bila Designs</span></span>' % corps)


def entete(actif=None):
    liens = []
    for libelle, href, cle in NAV:
        if cle == actif:
            liens.append('<a href="#" aria-current="page" style="white-space: nowrap; font-size: 14px; '
                         'font-weight: 600; color: #2743E3;">%s</a>' % libelle)
        else:
            liens.append('<a href="%s" style="white-space: nowrap; font-size: 14px; font-weight: 500; '
                         'color: #2C3348;">%s</a>' % (href, libelle))
    return """  <header style="position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between; gap: 40px; padding: 0 var(--gut);">
    <a href="/accueil/" style="flex: 0 0 auto; display: flex; align-items: center; gap: 13px;">
      %s
    </a>
    <nav style="flex: 0 0 auto; display: flex; align-items: center; gap: 26px;">
      %s
      <span style="position: relative; display: inline-flex; flex: 0 0 auto;">
        <span style="position: absolute; inset: -4px; border-radius: 999px; border: 2px solid rgba(39,67,227,0.85); animation: bila-halo 2.4s cubic-bezier(0.22,0.61,0.36,1) infinite; pointer-events: none;"></span>
        <span style="position: absolute; inset: -4px; border-radius: 999px; border: 2px solid rgba(39,67,227,0.55); animation: bila-halo 2.4s cubic-bezier(0.22,0.61,0.36,1) 1.2s infinite; pointer-events: none;"></span>
        <a href="/contact/#formulaire" style="display: inline-flex; align-items: center; padding: 13px 24px; background: #2743E3; color: #FFFFFF; font-size: 14px; font-weight: 600; border-radius: 999px; animation: bila-glow 2.4s ease-in-out infinite;" class="hv-cta">Démarrer un projet</a>
      </span>
    </nav>
  </header>""" % (marque(28), '\n      '.join(liens))


PIED = """  <footer style="position: relative; z-index: 2; padding: 44px var(--gut) 40px; border-top: 1px solid rgba(16,27,51,0.14); display: flex; flex-direction: column; gap: 40px;">
    <div style="display: flex; justify-content: space-between; gap: 56px; flex-wrap: wrap;">
      <div style="display: flex; flex-direction: column; gap: 16px; min-width: 220px; background: #FBFBFA; padding-right: 18px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          %s
        </div>
        <span style="font-size: 13px; line-height: 1.7; color: #6B7280;">Studio indépendant de design et d'automatisation.<br>Basé à Lyon, France.</span>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; background: #FBFBFA; padding: 0 16px;">
        <span style="font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #A0A5B0;">Prestations</span>
        <a href="/services/" style="font-size: 14px; color: #2C3348;">Sites web &amp; référencement</a>
        <a href="/services/" style="font-size: 14px; color: #2C3348;">Rebranding</a>
        <a href="/automatisations/" style="font-size: 14px; color: #2C3348;">Automatisations</a>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; background: #FBFBFA; padding: 0 16px;">
        <span style="font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #A0A5B0;">Studio</span>
        <a href="/accueil/#realisations" style="font-size: 14px; color: #2C3348;">Portfolio</a>
        <a href="/accueil/#audit" style="font-size: 14px; color: #2C3348;">Audit gratuit</a>
        <a href="/contact/" style="font-size: 14px; color: #2C3348;">Contact</a>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; background: #FBFBFA; padding: 0 16px;">
        <span style="font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #A0A5B0;">Réseaux</span>
        <a href="https://www.instagram.com/biladesigns" target="_blank" rel="noopener" style="font-size: 14px; color: #2C3348;">Instagram</a>
        <a href="https://www.linkedin.com/company/biladesigns" target="_blank" rel="noopener" style="font-size: 14px; color: #2C3348;">LinkedIn</a>
      </div>
    </div>
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap; border-top: 1px solid rgba(16,27,51,0.1); padding-top: 22px;">
      <span style="background: #FBFBFA; padding: 0 14px 0 0; font-size: 12px; color: #8A8F9C;">2026 © Bila Designs — Édition</span>
      <div style="display: flex; align-items: center; gap: 24px; flex-wrap: wrap; background: #FBFBFA; padding: 0 14px;">
        <a href="/mentions-legales/" style="font-size: 12px; color: #8A8F9C;">Mentions légales</a>
        <a href="/politique-confidentialite/" style="font-size: 12px; color: #8A8F9C;">Confidentialité</a>
      </div>
    </div>
  </footer>""" % marque(24)

FILETS = """  <div style="position: absolute; inset: 0; overflow: hidden;">
    <div style="position: absolute; left: var(--rail); top: 44px; bottom: 0; width: 1px; background: rgba(16,27,51,0.1);"></div>
    <div style="position: absolute; right: var(--rail); top: 44px; bottom: 0; width: 1px; background: rgba(16,27,51,0.1);"></div>
  </div>"""

STYLE_COMMUN = """  .hv-cta:hover, .hv-cta:focus-visible { background: #101B33 !important; color: #FFFFFF !important; }
  .prose a { color: #2743E3; border-bottom: 1px solid rgba(39,67,227,0.35); }
  .prose a:hover { color: #101B33; border-bottom-color: #101B33; }"""


def document(titre, description, canonique, corps, style_extra='', script_extra='', noindex=False):
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titre)s</title>
<meta name="description" content="%(desc)s">
%(robots)s<link rel="canonical" href="https://www.biladesigns.com%(can)s">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon/favicon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="/favicon/favicon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#101B33">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bila Designs">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="%(titre)s">
<meta property="og:description" content="%(desc)s">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/fraunces-latin.woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/bila.css">
<style>
%(style)s
</style>
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>
<main id="contenu">
%(corps)s
</main>
<script src="/assets/js/bila-motion.js" defer></script>
<script src="/assets/js/bila-ui.js" defer></script>
%(script)s</body>
</html>
""" % dict(titre=titre, desc=description, can=canonique,
           robots='<meta name="robots" content="noindex, follow">\n' if noindex else '',
           style=STYLE_COMMUN + ('\n' + style_extra if style_extra else ''),
           corps=corps, script=(script_extra + '\n') if script_extra else '')

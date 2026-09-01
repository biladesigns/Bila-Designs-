#!/usr/bin/env python3
"""Traduit une maquette Claude Design (.dc.html) en page HTML autonome.

Le runtime de prototypage (support.js, <x-dc>, <helmet>, style-hover, x-import)
n'est pas porte : il est remplace par du HTML/CSS/JS standard. Les valeurs
numeriques des maquettes ne sont jamais modifiees, a deux exceptions pres,
toutes deux reversibles et pilotees par variables CSS :
  - les gouttieres 90px et les filets a 64px deviennent var(--gut) / var(--rail)
  - les corps de police >= 30px deviennent des clamp() qui valent la taille
    d'origine au-dela de 1440px de large.
"""
import re, sys, html, os

GUT, RAIL = 90, 64
CLAMP_MIN_PX = 30

# --- liens : maquette -> routes du site ------------------------------------
ROUTES = {
    "Hero Bila Designs.dc.html": "/accueil/",
    "Sites web et branding.dc.html": "/services/",
    "Avocats.dc.html": "/avocats/",
    "Automatisations.dc.html": "/automatisations/",
    "Contact.dc.html": "/contact/",
}


def route_links(s):
    for src, dst in ROUTES.items():
        s = s.replace('href="%s#' % src, 'href="%s#' % dst)
        s = s.replace('href="%s"' % src, 'href="%s"' % dst)
    return s


def strip_runtime(s):
    """Retire l'echafaudage du prototype et remonte le <helmet> en <head>."""
    s = s.replace('<script src="./support.js"></script>', '')
    s = s.replace('<![CDATA[', '')
    # le <script type="text/x-dc"> final porte la logique : on le recupere a part
    logic = ''
    m = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', s, re.S)
    if m:
        logic = m.group(1)
        s = s[:m.start()] + s[m.end():]
    helmet = ''
    m = re.search(r'<helmet>(.*?)</helmet>', s, re.S)
    if m:
        helmet = m.group(1)
        s = s[:m.start()] + s[m.end():]
    m = re.search(r'<x-dc>(.*?)</x-dc>', s, re.S)
    body = m.group(1) if m else s
    return body.strip(), helmet, logic


def helmet_styles(helmet):
    """Ne garde que les @keyframes/regles maison : les polices sont auto-hebergees."""
    out = []
    for blk in re.findall(r'<style>(.*?)</style>', helmet, re.S):
        for line in blk.splitlines():
            t = line.strip()
            if not t:
                continue
            # body{margin} et a{color} vivent desormais dans bila.css
            if t.startswith('body {') or t.startswith('a {') or t.startswith('a:hover'):
                continue
            out.append(t)
    return '\n  '.join(out)


# --- style-hover -> vraies regles :hover ------------------------------------
def convert_hover(s):
    rules = []
    counter = [0]

    def repl(m):
        decls = html.unescape(m.group(1)).strip().rstrip(';')
        if not decls:
            return ''
        counter[0] += 1
        cls = 'hv-%d' % counter[0]
        # une declaration inline l'emporte sur une classe : !important est requis
        body = '; '.join(d.strip() + ' !important' for d in decls.split(';') if d.strip())
        rules.append('.%s:hover, .%s:focus-visible { %s; }' % (cls, cls, body))
        return ' data-hv="%s"' % cls

    s = re.sub(r'\s+style-hover="([^"]*)"', repl, s)
    s = re.sub(r"\s+style-hover='([^']*)'", repl, s)
    # style-active : meme traitement, sur :active
    def repl_a(m):
        decls = html.unescape(m.group(1)).strip().rstrip(';')
        if not decls:
            return ''
        counter[0] += 1
        cls = 'hv-%d' % counter[0]
        body = '; '.join(d.strip() + ' !important' for d in decls.split(';') if d.strip())
        rules.append('.%s:active { %s; }' % (cls, body))
        return ' data-hv="%s"' % cls
    s = re.sub(r'\s+style-active="([^"]*)"', repl_a, s)

    # data-hv -> class (en fusionnant avec une classe deja presente)
    def merge(m):
        tag = m.group(0)
        cls = re.search(r'data-hv="([^"]+)"', tag).group(1)
        tag = re.sub(r'\s*data-hv="[^"]+"', '', tag)
        if re.search(r'\sclass="', tag):
            tag = re.sub(r'class="([^"]*)"', lambda x: 'class="%s %s"' % (x.group(1), cls), tag, count=1)
        else:
            tag = tag[:-1].rstrip() + ' class="%s">' % cls
        return tag
    s = re.sub(r'<[a-zA-Z][^>]*data-hv="[^"]+"[^>]*>', merge, s)
    return s, rules


# --- gouttieres et filets -> variables CSS ---------------------------------
def variabilise(s):
    s = re.sub(r'padding:\s*0\s+%dpx' % GUT, 'padding: 0 var(--gut)', s)
    s = re.sub(r'padding:\s*(\d+px)\s+%dpx\s+(\d+px)' % GUT, r'padding: \1 var(--gut) \2', s)
    s = re.sub(r'padding:\s*(\d+px)\s+%dpx' % GUT, r'padding: \1 var(--gut)', s)
    s = re.sub(r'margin:\s*0\s+%dpx' % GUT, 'margin: 0 var(--gut)', s)
    s = re.sub(r'margin:\s*(-?\d+px)\s+%dpx\s+(-?\d+px)' % GUT, r'margin: \1 var(--gut) \2', s)
    s = re.sub(r'margin:\s*(-?\d+px)\s+%dpx' % GUT, r'margin: \1 var(--gut)', s)
    s = re.sub(r'padding:\s*0\s+var\(--gut\)\s+(\d+px)', r'padding: 0 var(--gut) \1', s)
    s = s.replace('left: %dpx;' % RAIL, 'left: var(--rail);')
    s = s.replace('right: %dpx;' % RAIL, 'right: var(--rail);')
    s = s.replace('padding: 42px %dpx;' % RAIL, 'padding: 42px var(--rail);')
    s = s.replace('calc(%dpx + (100%% - %dpx)' % (GUT, GUT * 2),
                  'calc(var(--gut) + (100% - var(--gut) * 2)')
    s = s.replace('padding: 0 40px 0 %dpx;' % GUT, 'padding: 0 40px 0 var(--gut);')
    return s


def clamp_sizes(s):
    def repl(m):
        n = int(m.group(1))
        if n < CLAMP_MIN_PX:
            return m.group(0)
        lo = round(n * 0.50, 1)
        base = round(n * 0.3143, 1)
        vw = round(n * 0.0476, 3)
        return 'font-size: clamp(%gpx, %gpx + %gvw, %dpx)' % (lo, base, vw, n)
    return re.sub(r'font-size:\s*(\d+)px(?=\s*[;"])', repl, s)


# --- grilles : classe pour pouvoir les empiler en media query --------------
def tag_grids(s):
    def repl(m):
        tag = m.group(0)
        style = m.group(1)
        gt = re.search(r'grid-template-columns:\s*([^;"]+)', style)
        if not gt:
            return tag
        cols = gt.group(1)
        r = re.match(r'repeat\((\d+),', cols.strip())
        n = int(r.group(1)) if r else (2 if ',' not in cols and cols.count('minmax') + cols.count('px') >= 2 else 0)
        if not n:
            n = len([c for c in re.split(r'\s+(?![^()]*\))', cols.strip()) if c])
        if n < 2:
            return tag
        cls = 'g-%d' % min(n, 4)
        if re.search(r'\sclass="', tag):
            return re.sub(r'class="([^"]*)"', lambda x: 'class="%s %s"' % (x.group(1), cls), tag, count=1)
        return tag[:-1].rstrip() + ' class="%s">' % cls
    return re.sub(r'<[a-zA-Z][a-zA-Z0-9]*[^>]*style="([^"]*grid-template-columns[^"]*)"[^>]*>', repl, s)


# --- x-import BorderGlow -> markup statique + classes ----------------------
def convert_borderglow(s):
    def repl(m):
        attrs = m.group(1)
        inner = m.group(2)
        def a(name, default):
            mm = re.search(r'%s="([^"]*)"' % name, attrs)
            return mm.group(1) if mm else default
        bg = a('background-color', '#FBFBFA')
        glow = a('glow-color', '229 78 52')
        style = a('style', '')
        h, sat, li = (glow.split() + ['78', '52'])[:3]
        vars_ = ['--card-bg: %s' % bg]
        for key, op in [('', 100), ('-60', 60), ('-50', 50), ('-40', 40), ('-30', 30), ('-20', 20), ('-10', 10)]:
            vars_.append('--glow-color%s: hsl(%sdeg %s%% %s%% / %d%%)' % (key, h, sat, li, op))
        pos = ['80% 55%', '69% 34%', '8% 6%', '41% 38%', '86% 85%', '82% 18%', '51% 4%']
        keys = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']
        cmap = [0, 1, 2, 0, 1, 2, 1]
        colors = ['#2743E3', '#5D7EFF', '#101B33']
        for i, k in enumerate(keys):
            vars_.append('--gradient-%s: radial-gradient(at %s, %s 0px, transparent 50%%)' % (k, pos[i], colors[cmap[i]]))
        vars_.append('--gradient-base: linear-gradient(%s 0 100%%)' % colors[0])
        light = ' border-glow-card--light' if bg.upper() in ('#FBFBFA', '#FFFFFF', '#F6F6F3') else ''
        return ('<div class="border-glow-card%s" style="%s; %s">'
                '<span class="edge-light"></span>'
                '<div class="border-glow-inner">%s</div></div>') % (light, style, '; '.join(vars_), inner)
    return re.sub(r'<x-import\s+component="BorderGlow"([^>]*)>(.*?)</x-import>', repl, s, flags=re.S)



# --- rangees en flex : autoriser le retour a la ligne en mobile ------------
def tag_flex(s):
    """Marque les rangees horizontales qui ne savent pas encore passer a la
    ligne. En dessous de 768px elles debordent : la regle .fx-row de
    bila.css leur rend le retour a la ligne, sans toucher au desktop."""
    def repl(m):
        tag, style = m.group(0), m.group(1)
        if 'display: flex' not in style:
            return tag
        for exclu in ('flex-direction: column', 'flex-wrap', 'width: max-content',
                      'position: absolute', 'position: fixed'):
            if exclu in style:
                return tag
        if re.search(r'\sclass="', tag):
            return re.sub(r'class="([^"]*)"', lambda x: 'class="%s fx-row"' % x.group(1), tag, count=1)
        return tag[:-1].rstrip() + ' class="fx-row">'
    return re.sub(r'<(?:div|span|header|nav|footer|form|article|section|label|a|ul)\b[^>]*style="([^"]*)"[^>]*>',
                  repl, s)


# --- plancher de lisibilite pour les tres petits corps ---------------------
def tag_petits(s):
    """Les etiquettes de 9 a 12px sont lisibles sur un ecran d'ordinateur,
    plus du tout sur un telephone. Une classe par taille permet de leur
    donner un plancher en media query, sans toucher au dessin desktop."""
    def repl(m):
        tag = m.group(0)
        n = int(m.group(1))
        cls = 't%d' % n
        if re.search(r'\sclass="', tag):
            return re.sub(r'class="([^"]*)"', lambda x: 'class="%s %s"' % (x.group(1), cls), tag, count=1)
        return tag[:-1].rstrip() + ' class="%s">' % cls
    def repl_corps(m):
        # Le texte courant en 13 ou 14px passe a 15px sur telephone. Les
        # etiquettes en capitales gardent leur taille : leur petitesse est
        # voulue, et elles restent lisibles grace a l'interlettrage.
        tag = m.group(0)
        if 'text-transform: uppercase' in tag:
            return tag
        cls = 't%d' % int(m.group(1))
        if re.search(r'\sclass="', tag):
            return re.sub(r'class="([^"]*)"', lambda x: 'class="%s %s"' % (x.group(1), cls), tag, count=1)
        return tag[:-1].rstrip() + ' class="%s">' % cls

    s = re.sub(r'<[a-zA-Z][a-zA-Z0-9]*\b[^>]*style="[^"]*font-size:\s*(9|10|11|12)px[^"]*"[^>]*>',
               repl, s)
    return re.sub(r'<[a-zA-Z][a-zA-Z0-9]*\b[^>]*style="[^"]*font-size:\s*(13|14)px[^"]*"[^>]*>',
                  repl_corps, s)

def main(src, out, title, desc, canonical, nav_active, extra_css='', extra_js='', noindex=False, preload_hero=None):
    raw = open(src, encoding='utf-8').read()
    body, helmet, logic = strip_runtime(raw)
    body = route_links(body)
    body = convert_borderglow(body)
    body, hover_rules = convert_hover(body)
    body = variabilise(body)
    body = clamp_sizes(body)
    body = tag_grids(body)
    # Les images de DA sont servies en WebP ; les PNG restent au depot
    # comme sources. Voir tools/optimiser_images.py.
    body = re.sub(r'src="assets/([^"]+)\.png"', r'src="/assets/img/\1.webp"', body)
    body = body.replace('src="assets/', 'src="/assets/img/')
    kf = helmet_styles(helmet)

    head_css = ''
    if kf:
        head_css += '  ' + kf + '\n'
    if hover_rules:
        head_css += '  ' + '\n  '.join(hover_rules) + '\n'
    if extra_css:
        head_css += '  ' + extra_css.strip() + '\n'

    preload = ''
    if preload_hero:
        preload = '<link rel="preload" as="image" href="%s" fetchpriority="high">\n' % preload_hero

    doc = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(robots)s<link rel="canonical" href="https://www.biladesigns.com%(canonical)s">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bila Designs">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="https://www.biladesigns.com%(canonical)s">
<meta property="og:image" content="https://www.biladesigns.com/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/fraunces-latin.woff2" crossorigin>
%(preload)s<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/bila.css">
<style>
%(head_css)s</style>
</head>
<body data-nav="%(nav)s">
<a class="skip-link" href="#contenu">Aller au contenu</a>
<main id="contenu">
%(body)s
</main>
<script src="/assets/js/bila-motion.js" defer></script>
<script src="/assets/js/bila-ui.js" defer></script>
%(extra_js)s</body>
</html>
""" % dict(title=html.escape(title), desc=html.escape(desc), canonical=canonical,
           robots='<meta name="robots" content="noindex, follow">\n' if noindex else '',
           preload=preload, head_css=head_css, nav=nav_active, body=body,
           extra_js=(extra_js + '\n') if extra_js else '')

    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)
    print('%-34s -> %-28s  %6d o  (%d :hover)' % (os.path.basename(src), out, len(doc), len(hover_rules)))
    if 'sc-for' in doc or '{{' in doc:
        n = doc.count('<sc-for') + len(re.findall(r'\{\{', doc))
        print('   ! %d marqueurs dynamiques restants a cabler a la main' % n)
    return logic


if __name__ == '__main__':
    main(*sys.argv[1:])

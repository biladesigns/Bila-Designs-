#!/usr/bin/env python3
"""Compose l'image de partage, celle qui s'affiche quand on colle un lien.

Elle etait declaree dans les balises Open Graph mais n'existait pas :
l'apercu etait vide sur LinkedIn, dans les messageries et partout ailleurs.
Elle est composee dans la DA, avec le logotype rendu par le navigateur —
la meme Fraunces, le meme melange d'encres que sur le site.
"""
import subprocess, os, sys, json

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'

GABARIT = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="%(base)sassets/css/fonts.css">
<style>
  * { margin: 0; box-sizing: border-box; }
  body { width: 1200px; height: 630px; background: #FBFBFA;
         font-family: 'Archivo', sans-serif; position: relative; overflow: hidden; }
  .filet { position: absolute; top: 0; bottom: 0; width: 1px; background: rgba(16,27,51,0.12); }
  .contenu { position: absolute; inset: 0; padding: 78px 90px;
             display: flex; flex-direction: column; justify-content: space-between; }
  .logo { display: inline-flex; align-items: center; gap: 18px; font-size: 46px; }
  .bd { display: inline-flex; isolation: isolate; font-family: 'Fraunces', Georgia, serif;
        font-weight: 600; font-size: 1em; line-height: 0.82; letter-spacing: -0.02em; }
  .b { color: #101B33; mix-blend-mode: multiply; }
  .d { margin-left: -0.34em; color: #2743E3; mix-blend-mode: multiply; }
  .rule { width: 1px; align-self: stretch; background: rgba(16,27,51,0.2); }
  .nom { font-weight: 700; font-size: 0.48em; letter-spacing: -0.012em; color: #101B33; }
  h1 { font-family: 'Fraunces', Georgia, serif; font-weight: 600; font-size: 78px;
       line-height: 1.04; letter-spacing: -0.025em; color: #101B33; max-width: 15ch; }
  h1 em { font-style: normal; color: #2743E3; }
  .pied { display: flex; align-items: baseline; gap: 22px; }
  .eyebrow { font-size: 15px; font-weight: 700; letter-spacing: 0.2em;
             text-transform: uppercase; color: #2743E3; }
  .url { font-size: 19px; color: #6B7280; }
  .losange { width: 9px; height: 9px; background: #2743E3; transform: rotate(45deg); }
</style></head><body>
  <div class="filet" style="left: 64px"></div>
  <div class="filet" style="right: 64px"></div>
  <div class="contenu">
    <span class="logo"><span class="bd"><span class="b">B</span><span class="d">D</span></span>
      <span class="rule"></span><span class="nom">Bila Designs</span></span>
    <h1>%(titre)s</h1>
    <div class="pied"><span class="losange"></span><span class="eyebrow">%(eyebrow)s</span>
      <span class="url">biladesigns.com</span></div>
  </div>
</body></html>"""

IMAGES = [
    ('og.png', 'Une présence digitale à la hauteur de <em>votre expertise.</em>',
     'Sites web · IA · Automatisations'),
    ('og-avocats.png', 'Une IA choisit trois cabinets. <em>Pas le vôtre.</em>',
     'Cabinets d’avocats'),
]

for nom, titre, eyebrow in IMAGES:
    html = GABARIT % dict(base='file://' + R, titre=titre, eyebrow=eyebrow)
    tmp = '/tmp/og-source.html'
    open(tmp, 'w', encoding='utf-8').write(html)
    dst = R + 'assets/img/' + nom
    r = subprocess.run(['timeout', '90', 'playwright', 'screenshot',
                        '--viewport-size=1200,630', '--wait-for-timeout=1500',
                        'file://' + tmp, dst], capture_output=True, text=True)
    if not os.path.exists(dst):
        print('ECHEC %s : %s' % (nom, r.stderr[:180]))
        sys.exit(1)
    print('%-18s %6.0f Ko' % (nom, os.path.getsize(dst) / 1024))

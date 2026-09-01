#!/usr/bin/env python3
"""Reconstruit les trois pages annexes dans la nouvelle direction artistique.

Mentions legales, confidentialite et desabonnement n'avaient pas de
maquette : elles gardaient l'en-tete, le pied de page, Tailwind et la
banniere cookies de l'ancien site. On repart de leur texte, et on le
repose dans le systeme du nouveau site.

Le contenu juridique n'est pas reformule, a une exception signalee : la
section cookies de la politique de confidentialite decrivait Google
Analytics et un calendrier de reservation. Le nouveau site n'en pose
aucun, et laisser ecrit qu'on suit les visiteurs alors que c'est faux
serait pire qu'une reecriture.
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annexes_gabarit import entete, PIED, FILETS, document

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'


def liens(t):
    """[[libelle|href]] -> <a>."""
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'<a href="\2">\1</a>', t)


def extraire(fichier):
    s = open(fichier, encoding='utf-8').read()
    m = re.search(r'<main\b[^>]*>(.*?)</main>', s, re.S)
    c = re.sub(r'<script.*?</script>', '', m.group(1), flags=re.S)
    blocs = []
    for mm in re.finditer(r'<(h1|h2|h3|p|li)\b[^>]*>(.*?)</\1>', c, re.S):
        tag, txt = mm.group(1), mm.group(2)
        txt = re.sub(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[[\2|\1]]', txt, flags=re.S)
        txt = re.sub(r'<br\s*/?>', ' ', txt)
        txt = html.unescape(re.sub(r'<[^>]+>', '', txt)).strip()
        txt = re.sub(r'\s+', ' ', txt)
        if txt:
            blocs.append([tag, txt])
    return blocs


# Les deux adresses coexistaient ; le site n'en affiche plus qu'une.
def normaliser(blocs):
    for b in blocs:
        b[1] = b[1].replace('contact@biladesigns.com', 'mathieu@biladesigns.com')
    return blocs


H2 = ('font-family: \'Fraunces\', Georgia, serif; font-weight: 500; '
      'font-size: clamp(21px, 13.2px + 2vw, 30px); line-height: 1.2; '
      'letter-spacing: -0.02em; color: #101B33; margin: 56px 0 18px;')
H3 = ('font-family: \'Fraunces\', Georgia, serif; font-weight: 500; font-size: 20px; '
      'line-height: 1.3; color: #101B33; margin: 32px 0 12px;')
P = ('margin: 0 0 14px; max-width: 62ch; font-size: 16px; line-height: 1.75; '
     'color: #4A5163; text-wrap: pretty;')
LI = ('margin: 0 0 10px; max-width: 62ch; font-size: 16px; line-height: 1.7; color: #4A5163;')


def rendre(blocs, sous_titre):
    """Le h1 devient le hero ; le reste devient la prose."""
    titre = blocs[0][1]
    out = []
    liste_ouverte = False
    for tag, txt in blocs[1:]:
        txt = liens(txt)
        if tag == 'li':
            if not liste_ouverte:
                out.append('<ul style="margin: 0 0 18px; padding-left: 22px; list-style: none;">')
                liste_ouverte = True
            out.append('  <li style="%s position: relative;">'
                       '<span style="position: absolute; left: -22px; top: 9px; width: 6px; height: 6px; '
                       'background: #2743E3; transform: rotate(45deg);"></span>%s</li>' % (LI, txt))
            continue
        if liste_ouverte:
            out.append('</ul>')
            liste_ouverte = False
        if tag == 'h2':
            out.append('<h2 style="%s">%s</h2>' % (H2, txt))
        elif tag == 'h3':
            out.append('<h3 style="%s">%s</h3>' % (H3, txt))
        else:
            out.append('<p style="%s">%s</p>' % (P, txt))
    if liste_ouverte:
        out.append('</ul>')
    return titre, '\n      '.join(out)


def page_prose(source, sortie, actif, titre_onglet, description, canonique, eyebrow, remplacements=None):
    blocs = normaliser(extraire(R + source))
    if remplacements:
        blocs = remplacements(blocs)
    titre, prose = rendre(blocs, eyebrow)

    corps = """<section style="position: relative; background: #FBFBFA; font-family: 'Archivo', Helvetica, Arial, sans-serif; color: #101B33; padding: 34px 0 0; overflow: hidden;">
%(filets)s

%(entete)s

  <div style="position: relative; z-index: 2; margin-top: 88px; padding: 0 var(--gut); display: flex; flex-direction: column; align-items: flex-start; gap: 20px;">
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #2743E3;">%(eyebrow)s</span>
    <h1 style="margin: 0; max-width: 820px; font-family: 'Fraunces', Georgia, serif; font-weight: 600; font-size: clamp(33px, 20.7px + 3.14vw, 66px); line-height: 1.06; letter-spacing: -0.02em;">%(titre)s</h1>
  </div>

  <div class="prose" style="position: relative; z-index: 2; margin-top: 48px; padding: 0 var(--gut) 104px;">
      %(prose)s
  </div>

%(pied)s
</section>""" % dict(filets=FILETS, entete=entete(actif), eyebrow=eyebrow,
                     titre=titre, prose=prose, pied=PIED)

    open(R + sortie, 'w', encoding='utf-8').write(
        document(titre_onglet, description, canonique, corps))
    print('%-30s -> %s' % (source, sortie))


def corriger_cookies(blocs):
    """Le nouveau site ne pose aucun cookie : la section le dit desormais."""
    debut = next(i for i, b in enumerate(blocs) if b[0] == 'h2' and 'Cookies' in b[1])
    fin = next(i for i, b in enumerate(blocs) if b[0] == 'h2' and 'Durée de conservation' in b[1])
    neuf = [
        ['h2', blocs[debut][1]],
        ['p', "Ce site ne depose aucun cookie de mesure d'audience ni de publicite. "
              "Il n'utilise ni Google Analytics, ni outil de suivi comportemental, ni "
              "service tiers embarque. Aucun consentement n'a donc a vous etre demande, "
              "et il n'y a pas de banniere a accepter."],
        ['p', "Les seules donnees qui nous parviennent sont celles que vous nous "
              "transmettez vous-meme, par le formulaire de contact ou la demande "
              "d'audit gratuit."],
    ]
    for b in neuf:
        b[1] = (b[1].replace('depose', 'dépose').replace("d'audience", "d'audience")
                    .replace('embarque', 'embarqué').replace('demande', 'demandé')
                    .replace('banniere', 'bannière').replace('donnees', 'données')
                    .replace('parviennent', 'parviennent').replace('transmettez', 'transmettez')
                    .replace('meme', 'même').replace('gratuit', 'gratuit'))
    return blocs[:debut] + neuf + blocs[fin:]


page_prose('mentions-legales/index.html', 'mentions-legales/index.html', None,
           'Mentions légales — Bila Designs',
           "Mentions légales de biladesigns.com : éditeur, hébergement, propriété "
           "intellectuelle et droit applicable.",
           '/mentions-legales', 'Informations légales')

page_prose('politique-confidentialite/index.html', 'politique-confidentialite/index.html', None,
           'Politique de confidentialité — Bila Designs',
           "Quelles données sont collectées sur biladesigns.com, pourquoi, combien de "
           "temps, et comment exercer vos droits.",
           '/politique-confidentialite', 'Vos données',
           remplacements=corriger_cookies)


# ── Desabonnement ─────────────────────────────────────────────────────────
# Page fonctionnelle : le formulaire, ses identifiants et son comportement
# sont conserves. Deux corrections : FormSubmit repond 200 meme quand il
# refuse, et l'ancien script se fiait a ce 200 pour annoncer un
# desabonnement qui n'avait pas eu lieu ; et l'affichage passait par la
# classe « hidden » de Tailwind, qui n'existe plus.
CHAMP = ("border: none; border-bottom: 1px solid rgba(16,27,51,0.24); background: transparent; "
         "padding: 6px 0 11px; font-family: 'Archivo', Helvetica, Arial, sans-serif; "
         "font-size: 16px; color: #101B33; outline: none; width: 100%; max-width: 420px;")

DESAB_CORPS = """<section style="position: relative; background: #FBFBFA; font-family: 'Archivo', Helvetica, Arial, sans-serif; color: #101B33; padding: 34px 0 0; overflow: hidden;">
%(filets)s

%(entete)s

  <div style="position: relative; z-index: 2; margin-top: 88px; padding: 0 var(--gut) 104px; display: flex; flex-direction: column; align-items: flex-start; gap: 22px;">
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #2743E3;">Liste de diffusion</span>
    <h1 style="margin: 0; max-width: 760px; font-family: 'Fraunces', Georgia, serif; font-weight: 600; font-size: clamp(33px, 20.7px + 3.14vw, 66px); line-height: 1.06; letter-spacing: -0.02em;">Se désabonner.</h1>

    <div id="form-container" style="display: flex; flex-direction: column; align-items: flex-start; gap: 26px; margin-top: 8px;">
      <p style="margin: 0; max-width: 52ch; font-size: 17px; line-height: 1.7; color: #4A5163;">Vous ne souhaitez plus recevoir nos emails ? Entrez votre adresse ci-dessous, et c'est fini.</p>
      <form id="unsubscribe-form" style="display: flex; flex-direction: column; align-items: flex-start; gap: 24px; width: 100%%; max-width: 440px;">
        <label style="display: flex; flex-direction: column; gap: 10px; width: 100%%;">
          <span style="font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #8A8F9C;">Votre adresse électronique</span>
          <input type="email" id="email" name="email" required autocomplete="email" placeholder="vous@exemple.fr" style="%(champ)s">
        </label>
        <span style="position: relative; display: inline-flex; flex: 0 0 auto;">
          <span style="position: absolute; inset: -4px; border-radius: 999px; border: 2px solid rgba(39,67,227,0.85); animation: bila-halo 2.4s cubic-bezier(0.22,0.61,0.36,1) 0.4s infinite; pointer-events: none;"></span>
          <span style="position: absolute; inset: -4px; border-radius: 999px; border: 2px solid rgba(39,67,227,0.55); animation: bila-halo 2.4s cubic-bezier(0.22,0.61,0.36,1) 1.6s infinite; pointer-events: none;"></span>
          <button type="submit" style="display: inline-flex; align-items: center; gap: 10px; padding: 17px 32px; border: none; border-radius: 999px; background: #2743E3; color: #FFFFFF; font-family: 'Archivo', Helvetica, Arial, sans-serif; font-size: 15px; font-weight: 600; cursor: pointer; white-space: nowrap; animation: bila-glow 2.4s ease-in-out infinite;" class="hv-cta">Me désabonner <span style="font-size: 14px;">&rarr;</span></button>
        </span>
        <span id="retour" role="status" aria-live="polite" class="form-retour"></span>
      </form>
      <span style="max-width: 52ch; font-size: 13px; line-height: 1.7; color: #8A8F9C;">Cette action est irréversible. Vous pouvez nous recontacter à tout moment depuis la <a href="/contact/" style="color: #8A8F9C; text-decoration: underline;">page contact</a>.</span>
    </div>

    <div id="success-container" hidden style="display: flex; flex-direction: column; align-items: flex-start; gap: 20px; margin-top: 8px;">
      <span style="display: inline-flex; align-items: center; gap: 12px; font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #2743E3;"><span style="width: 7px; height: 7px; background: #2743E3; transform: rotate(45deg);"></span>Désabonnement confirmé</span>
      <p style="margin: 0; max-width: 52ch; font-family: 'Fraunces', Georgia, serif; font-size: 26px; line-height: 1.3; letter-spacing: -0.01em; color: #101B33;">Vous ne recevrez plus rien de notre part.</p>
      <a href="/accueil/" style="display: inline-flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; color: #101B33; border-bottom: 1px solid #C9CCD4; padding-bottom: 4px;">Retour à l'accueil <span style="font-size: 13px;">&rarr;</span></a>
    </div>

    <div id="error-container" hidden style="display: flex; flex-direction: column; align-items: flex-start; gap: 20px; margin-top: 8px;">
      <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #B3261E;">Une erreur est survenue</span>
      <p id="error-message" style="margin: 0; max-width: 52ch; font-size: 17px; line-height: 1.7; color: #4A5163;">Impossible de traiter votre demande.</p>
      <p style="margin: 0; max-width: 52ch; font-size: 15px; line-height: 1.7; color: #4A5163;">Écrivez-moi directement à <a href="mailto:mathieu@biladesigns.com?subject=Désabonnement" style="color: #2743E3; border-bottom: 1px solid rgba(39,67,227,0.35);">mathieu@biladesigns.com</a> : je vous retire de la liste à la main.</p>
      <button type="button" onclick="location.reload()" style="display: inline-flex; align-items: center; padding: 14px 26px; border: 1px solid rgba(16,27,51,0.2); border-radius: 999px; background: transparent; font-family: 'Archivo', Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #101B33; cursor: pointer;">Réessayer</button>
    </div>
  </div>

%(pied)s
</section>""" % dict(filets=FILETS, entete=entete(None), pied=PIED, champ=CHAMP)

DESAB_SCRIPT = """<script>
(function () {
  var form = document.getElementById('unsubscribe-form');
  var formulaire = document.getElementById('form-container');
  var succes = document.getElementById('success-container');
  var erreur = document.getElementById('error-container');
  var message = document.getElementById('error-message');
  var retour = document.getElementById('retour');
  if (!form) return;

  // Adresse pre-remplie depuis le lien du mail.
  var params = new URLSearchParams(window.location.search);
  var fourni = params.get('email');
  if (fourni) {
    try { document.getElementById('email').value = decodeURIComponent(fourni); } catch (e) {}
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var champ = document.getElementById('email');
    var adresse = champ.value.trim().toLowerCase();
    if (!champ.checkValidity() || !adresse) {
      champ.classList.add('champ-erreur');
      champ.focus();
      retour.textContent = 'Cette adresse ne semble pas valide.';
      retour.setAttribute('data-etat', 'erreur');
      return;
    }
    champ.classList.remove('champ-erreur');

    var bouton = form.querySelector('button[type="submit"]');
    var texte = bouton.innerHTML;
    bouton.disabled = true;
    bouton.textContent = 'Traitement…';
    retour.textContent = 'Envoi en cours…';
    retour.setAttribute('data-etat', '');

    var donnees = new FormData();
    donnees.append('email', adresse);
    donnees.append('_subject', 'Demande de desabonnement — ' + adresse);
    donnees.append('message', 'Demande de desabonnement pour : ' + adresse);
    donnees.append('_captcha', 'false');

    fetch('https://formsubmit.co/ajax/matbila63@gmail.com', {
      method: 'POST', body: donnees, headers: { 'Accept': 'application/json' }
    }).then(function (rep) {
      if (!rep.ok) throw new Error(rep.status);
      return rep.json();
    }).then(function (data) {
      // FormSubmit repond 200 meme lorsqu'il refuse. Confirmer un
      // desabonnement qui n'a pas eu lieu serait le pire des resultats :
      // on ne le confirme que si le service dit l'avoir accepte.
      if (data && String(data.success) === 'false') throw new Error(data.message || 'refus');
      try {
        var liste = JSON.parse(localStorage.getItem('unsubscribed_emails') || '[]');
        if (liste.indexOf(adresse) === -1) {
          liste.push(adresse);
          localStorage.setItem('unsubscribed_emails', JSON.stringify(liste));
        }
      } catch (err) {}
      formulaire.hidden = true;
      succes.hidden = false;
    }).catch(function () {
      formulaire.hidden = true;
      erreur.hidden = false;
      message.textContent = 'Votre demande n’a pas pu etre enregistree automatiquement.';
    }).then(function () {
      bouton.disabled = false;
      bouton.innerHTML = texte;
    });
  });
})();
</script>"""

open(R + 'desabonnement/index.html', 'w', encoding='utf-8').write(
    document('Se désabonner — Bila Designs',
             "Retirez votre adresse de la liste de diffusion de Bila Designs.",
             '/desabonnement', DESAB_CORPS, script_extra=DESAB_SCRIPT, noindex=True))
print('%-30s -> %s' % ('desabonnement', 'desabonnement/index.html'))

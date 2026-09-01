/* =========================================================================
   Bila Designs — comportements d'interface
   Remplace le runtime du prototype : onglets, pastilles, cartes
   retournables, cadre lumineux, formulaires.
   Sans dependance, charge en defer sur toutes les pages.
   ========================================================================= */
(function () {
  'use strict';

  var ENDPOINT = 'https://formsubmit.co/ajax/matbila63@gmail.com';

  /* ── Onglets ────────────────────────────────────────────────────────────
     Un groupe [data-onglets] contient des [data-onglet="cle"] et des
     panneaux [data-panneau="cle"]. Le style actif est porte par des
     attributs data-* pour rester lisible dans le HTML des maquettes. */
  function initOnglets() {
    var groupes = document.querySelectorAll('[data-onglets]');
    for (var g = 0; g < groupes.length; g++) {
      (function (groupe) {
        if (groupe.__bilaTabs) return;
        groupe.__bilaTabs = true;
        var boutons = groupe.querySelectorAll('[data-onglet]');

        function activer(cle, focus) {
          for (var i = 0; i < boutons.length; i++) {
            var actif = boutons[i].getAttribute('data-onglet') === cle;
            boutons[i].setAttribute('aria-selected', actif ? 'true' : 'false');
            boutons[i].setAttribute('tabindex', actif ? '0' : '-1');
            if (actif && focus) boutons[i].focus();
          }
          var pans = groupe.querySelectorAll('[data-panneau]');
          for (var j = 0; j < pans.length; j++) {
            var on = pans[j].getAttribute('data-panneau') === cle;
            pans[j].hidden = !on;
          }
          // Les compteurs "02 / 05" et autres libelles qui suivent l'onglet.
          var suivis = groupe.querySelectorAll('[data-suit-onglet]');
          for (var k = 0; k < suivis.length; k++) {
            suivis[k].textContent = suivis[k].getAttribute('data-' + cle) || suivis[k].textContent;
          }
        }

        for (var b = 0; b < boutons.length; b++) {
          (function (bouton, index) {
            bouton.addEventListener('click', function (e) {
              e.preventDefault();
              activer(bouton.getAttribute('data-onglet'), false);
            });
            bouton.addEventListener('keydown', function (e) {
              var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
                    : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
              if (!d) return;
              e.preventDefault();
              var n = (index + d + boutons.length) % boutons.length;
              activer(boutons[n].getAttribute('data-onglet'), true);
            });
          })(boutons[b], b);
        }

        var depart = groupe.querySelector('[data-onglet][aria-selected="true"]') || boutons[0];
        if (depart) activer(depart.getAttribute('data-onglet'), false);
      })(groupes[g]);
    }
  }

  /* ── Pastilles a choix unique (page contact) ────────────────────────────
     De vraies radios : la navigation clavier et la restitution vocale sont
     celles du navigateur, seule l'apparence est reprise de la maquette. */
  function initPastilles() {
    var lots = document.querySelectorAll('[data-pastilles]');
    for (var i = 0; i < lots.length; i++) {
      (function (lot) {
        if (lot.__bilaChips) return;
        lot.__bilaChips = true;
        function peindre() {
          var labels = lot.querySelectorAll('.pastille');
          for (var j = 0; j < labels.length; j++) {
            var input = labels[j].querySelector('input');
            var on = input && input.checked;
            labels[j].style.border = '1px solid ' + (on ? '#2743E3' : 'rgba(16,27,51,0.2)');
            labels[j].style.background = on ? '#2743E3' : 'transparent';
            labels[j].style.color = on ? '#FFFFFF' : '#4A5163';
          }
        }
        lot.addEventListener('change', peindre);
        peindre();
      })(lots[i]);
    }
  }

  /* ── Cadre lumineux ─────────────────────────────────────────────────────
     Le composant React de la maquette, ramene a son seul effet : suivre le
     curseur pour orienter le halo. Le reste est deja dans la feuille CSS. */
  function initCadres() {
    var cartes = document.querySelectorAll('.border-glow-card');
    for (var i = 0; i < cartes.length; i++) {
      (function (carte) {
        if (carte.__bilaGlow) return;
        carte.__bilaGlow = true;
        carte.addEventListener('pointermove', function (e) {
          var r = carte.getBoundingClientRect();
          var cx = r.width / 2, cy = r.height / 2;
          var dx = e.clientX - r.left - cx, dy = e.clientY - r.top - cy;
          var kx = dx ? cx / Math.abs(dx) : Infinity;
          var ky = dy ? cy / Math.abs(dy) : Infinity;
          var bord = Math.min(Math.max(1 / Math.min(kx, ky), 0), 1);
          var deg = 0;
          if (dx || dy) {
            deg = Math.atan2(dy, dx) * (180 / Math.PI) + 90;
            if (deg < 0) deg += 360;
          }
          carte.style.setProperty('--edge-proximity', (bord * 100).toFixed(2));
          carte.style.setProperty('--cursor-angle', deg.toFixed(2) + 'deg');
        });
      })(cartes[i]);
    }
  }

  /* ── Cartes retournables ────────────────────────────────────────────────
     bila-motion.js gere deja le clic ; on ajoute ici le clavier et l'etat
     annonce, qui lui manquent. */
  function initRetournables() {
    var cartes = document.querySelectorAll('[data-flip]');
    for (var i = 0; i < cartes.length; i++) {
      (function (carte) {
        if (carte.__bilaFlipA11y) return;
        carte.__bilaFlipA11y = true;
        var interne = carte.querySelector('[data-flip-inner]');
        if (!interne) return;
        carte.setAttribute('role', 'button');
        carte.setAttribute('tabindex', '0');
        carte.setAttribute('aria-expanded', 'false');
        var faces = interne.children;
        if (faces[1]) faces[1].setAttribute('aria-hidden', 'true');

        function bascule() {
          var on = interne.getAttribute('data-on') === '1';
          interne.setAttribute('data-on', on ? '0' : '1');
          interne.style.transform = on ? 'rotateY(0deg)' : 'rotateY(180deg)';
          carte.setAttribute('aria-expanded', on ? 'false' : 'true');
          if (faces[0]) faces[0].setAttribute('aria-hidden', on ? 'false' : 'true');
          if (faces[1]) faces[1].setAttribute('aria-hidden', on ? 'true' : 'false');
        }
        carte.addEventListener('keydown', function (e) {
          if (e.key !== 'Enter' && e.key !== ' ') return;
          e.preventDefault();
          bascule();
        });
        // Le clic passe par bila-motion.js : on se contente de suivre l'etat.
        carte.addEventListener('click', function () {
          var on = interne.getAttribute('data-on') === '1';
          carte.setAttribute('aria-expanded', on ? 'true' : 'false');
          if (faces[0]) faces[0].setAttribute('aria-hidden', on ? 'true' : 'false');
          if (faces[1]) faces[1].setAttribute('aria-hidden', on ? 'false' : 'true');
        });
      })(cartes[i]);
    }
  }

  /* ── Formulaires ────────────────────────────────────────────────────────
     Validation cote client, piege a robots + horodatage, envoi en arriere-
     plan, etats explicites annonces par aria-live. */
  function initFormulaires() {
    var formulaires = document.querySelectorAll('form[data-form]');
    for (var i = 0; i < formulaires.length; i++) {
      (function (form) {
        if (form.__bilaForm) return;
        form.__bilaForm = true;

        var ouvert = Date.now();
        var bouton = form.querySelector('button[type="submit"]');
        var retour = form.querySelector('.form-retour');
        if (!retour) {
          retour = document.createElement('span');
          retour.className = 'form-retour';
          retour.setAttribute('role', 'status');
          retour.setAttribute('aria-live', 'polite');
          form.appendChild(retour);
        }

        function dire(texte, etat) {
          retour.textContent = texte;
          retour.setAttribute('data-etat', etat || '');
        }

        form.addEventListener('submit', function (e) {
          e.preventDefault();
          dire('', '');

          // Champs requis : on signale le premier fautif et on s'y arrete.
          var requis = form.querySelectorAll('[required]');
          for (var r = 0; r < requis.length; r++) {
            requis[r].classList.remove('champ-erreur');
          }
          for (var q = 0; q < requis.length; q++) {
            if (!requis[q].checkValidity()) {
              requis[q].classList.add('champ-erreur');
              requis[q].focus();
              dire(requis[q].validity.valueMissing
                ? 'Il manque ' + (requis[q].getAttribute('data-libelle') || 'un champ') + '.'
                : 'Cette valeur ne semble pas valide.', 'erreur');
              return;
            }
          }

          // Piege a robots : un champ que personne ne voit, plus un delai
          // minimal de remplissage. Aucun CAPTCHA a subir pour l'humain.
          var piege = form.querySelector('input[name="_honey"]');
          if ((piege && piege.value) || Date.now() - ouvert < 2500) {
            dire('Message envoye. Je vous reponds sous vingt-quatre heures.', 'ok');
            form.reset();
            return;
          }

          if (bouton) {
            bouton.disabled = true;
            bouton.__texte = bouton.innerHTML;
            bouton.textContent = 'Envoi…';
          }
          dire('Envoi en cours…', '');

          var donnees = new FormData(form);
          donnees.append('_subject', form.getAttribute('data-sujet') || 'Message depuis biladesigns.com');
          donnees.append('_template', 'table');
          donnees.append('_captcha', 'false');

          fetch(ENDPOINT, {
            method: 'POST',
            body: donnees,
            headers: { 'Accept': 'application/json' }
          }).then(function (rep) {
            if (!rep.ok) throw new Error(rep.status);
            return rep.json();
          }).then(function (data) {
            // FormSubmit repond 200 meme quand il refuse l'envoi (formulaire
            // non active, adresse bloquee). Le seul signal fiable est le
            // champ success du corps de reponse : sans ce controle, la page
            // annonce un envoi qui n'a jamais eu lieu.
            if (data && String(data.success) === 'false') {
              throw new Error(data.message || 'refus');
            }
            form.reset();
            dire(form.getAttribute('data-merci') ||
                 'Bien recu. Je vous reponds sous vingt-quatre heures.', 'ok');
          }).catch(function () {
            // Les donnees saisies restent en place : l'envoi peut etre repris.
            dire('L’envoi a echoue. Ecrivez-moi directement a mathieu@biladesigns.com.', 'erreur');
          }).then(function () {
            if (bouton) {
              bouton.disabled = false;
              bouton.innerHTML = bouton.__texte;
            }
          });
        });
      })(formulaires[i]);
    }
  }


  /* ── Groupes a selection (page Avocats) ─────────────────────────────────
     Deux systemes partagent la meme mecanique : les trois constats d'audit
     et les cinq etapes de la chaine du dossier. Chaque element stylable
     porte ses trois variantes (data-s-avant / data-s-actif / data-s-apres),
     exactement celles calculees par renderVals() dans la maquette ; le
     script se contente de choisir laquelle appliquer. Les textes du
     panneau viennent du bloc JSON en fin de page. */
  function initGroupes() {
    var source = document.getElementById('donnees-avocats');
    var donnees = {};
    if (source) {
      try { donnees = JSON.parse(source.textContent); } catch (e) { donnees = {}; }
    }

    var groupes = document.querySelectorAll('[data-groupe]');
    for (var g = 0; g < groupes.length; g++) {
      (function (groupe) {
        if (groupe.__bilaGroupe) return;
        groupe.__bilaGroupe = true;

        var nom = groupe.getAttribute('data-groupe');
        var lignes = donnees[nom] || [];
        var boutons = groupe.querySelectorAll('[data-choix]');

        function peindre(el, idx, actif) {
          var etat = idx === actif ? 'actif' : (idx < actif ? 'avant' : 'apres');
          var st = el.getAttribute('data-s-' + etat);
          if (st) el.style.cssText = st;
        }

        function remplir(ligne) {
          var champs = groupe.querySelectorAll('[data-champ]');
          for (var i = 0; i < champs.length; i++) {
            var cle = champs[i].getAttribute('data-champ').split('.')[1];
            var v = ligne[cle];
            champs[i].textContent = v === undefined ? '' : v;
          }
          var listes = groupe.querySelectorAll('[data-liste]');
          for (var j = 0; j < listes.length; j++) {
            var cle2 = listes[j].getAttribute('data-liste').split('.')[1];
            var items = ligne[cle2] || [];
            var style = listes[j].getAttribute('data-style-item') || '';
            listes[j].textContent = '';
            for (var k = 0; k < items.length; k++) {
              var sp = document.createElement('span');
              sp.className = 'puce-agent';
              sp.style.cssText = style;
              sp.textContent = items[k];
              listes[j].appendChild(sp);
              if (k < items.length - 1) listes[j].appendChild(document.createTextNode(' '));
            }
          }
        }

        function choisir(actif, focus) {
          groupe.setAttribute('data-actif', String(actif));
          var stylables = groupe.querySelectorAll('[data-s-actif]');
          for (var i = 0; i < stylables.length; i++) {
            var el = stylables[i];
            var brut = el.getAttribute('data-choix');
            if (brut === null) brut = el.getAttribute('data-choix-enfant');
            if (brut === null) brut = el.getAttribute('data-lien');
            if (brut === null) continue;
            peindre(el, parseInt(brut, 10), actif);
          }
          for (var b = 0; b < boutons.length; b++) {
            var on = parseInt(boutons[b].getAttribute('data-choix'), 10) === actif;
            boutons[b].setAttribute('aria-selected', on ? 'true' : 'false');
            boutons[b].setAttribute('tabindex', on ? '0' : '-1');
            if (on && focus) boutons[b].focus();
          }
          if (lignes[actif]) {
            var ligne = lignes[actif];
            // Le compteur "02 / 05" affiche le rang, pas un champ de donnees.
            var copie = {};
            for (var c in ligne) copie[c] = ligne[c];
            if (copie.num === undefined) {
              copie.num = (actif + 1 < 10 ? '0' : '') + (actif + 1);
            }
            remplir(copie);
          }
        }

        for (var b2 = 0; b2 < boutons.length; b2++) {
          (function (bouton, index) {
            bouton.addEventListener('click', function (e) {
              e.preventDefault();
              choisir(index, false);
            });
            bouton.addEventListener('keydown', function (e) {
              var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
                    : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
              if (!d) return;
              e.preventDefault();
              choisir((index + d + boutons.length) % boutons.length, true);
            });
          })(boutons[b2], parseInt(boutons[b2].getAttribute('data-choix'), 10));
        }

        choisir(parseInt(groupe.getAttribute('data-actif') || '0', 10), false);
      })(groupes[g]);
    }
  }

  function demarrer() {
    initOnglets();
    initGroupes();
    initPastilles();
    initCadres();
    initRetournables();
    initFormulaires();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', demarrer);
  } else {
    demarrer();
  }
})();

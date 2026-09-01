/* Audit responsive : debordement, filets sur du texte, cibles tactiles,
   lisibilite, elements plus larges que l'ecran. */
const { chromium, PAGES, LARGEURS, ouvrir } = require('./harnais');

(async () => {
  const nav = await chromium.launch();
  const soucis = [];

  for (const largeur of LARGEURS) {
    for (const page of PAGES) {
      const { ctx, pg, journal } = await ouvrir(nav, page, largeur);
      const r = await pg.evaluate((largeur) => {
        const out = { debordement: 0, filets: 0, croisements: [], coupables: [], petites: [], minuscule: [] };
        out.debordement = document.documentElement.scrollWidth - window.innerWidth;

        // elements qui depassent la fenetre
        if (out.debordement > 1) {
          for (const el of document.querySelectorAll('body *')) {
            const b = el.getBoundingClientRect();
            if (b.width === 0 || b.height === 0) continue;
            if (b.right > window.innerWidth + 1 || b.left < -1) {
              const cs = getComputedStyle(el);
              if (cs.position === 'fixed') continue;
              out.coupables.push({
                tag: el.tagName,
                cls: (el.className || '').toString().slice(0, 30),
                style: (el.getAttribute('style') || '').slice(0, 70),
                boite: Math.round(b.left) + '..' + Math.round(b.right),
              });
              if (out.coupables.length > 6) break;
            }
          }
        }

        // filets verticaux contre le texte rendu
        const filets = [];
        for (const el of document.querySelectorAll('div, span')) {
          const b = el.getBoundingClientRect();
          if (b.width > 0 && b.width <= 2.5 && b.height >= 100) filets.push(b);
        }
        out.filets = filets.length;
        const boites = [];
        const it = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = it.nextNode())) {
          if (!n.nodeValue.trim()) continue;
          const p = n.parentElement;
          if (!p || getComputedStyle(p).visibility === 'hidden') continue;
          const rg = document.createRange(); rg.selectNodeContents(n);
          for (const rr of rg.getClientRects()) if (rr.width > 2 && rr.height > 2) boites.push(rr);
        }
        for (const f of filets) {
          for (const t of boites) {
            if (f.left < t.right - 1 && f.right > t.left + 1 && f.top < t.bottom - 1 && f.bottom > t.top + 1) {
              out.croisements.push(Math.round(f.left)); break;
            }
          }
        }

        // cibles tactiles trop petites (mobile seulement)
        if (largeur <= 768) {
          // La zone cliquable n'est pas la boite de l'element : une zone
          // etendue par ::after ne compte pas dans getBoundingClientRect.
          // On teste donc au point, comme le fait un doigt.
          const atteint = (el, x, y) => {
            const cible = document.elementFromPoint(x, y);
            return cible && (cible === el || el.contains(cible) || cible.parentElement === el);
          };
          for (const el of document.querySelectorAll('a, button, input, [role="tab"], label.pastille')) {
            const b = el.getBoundingClientRect();
            if (b.width === 0 || b.height === 0) continue;
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            if (el.classList.contains('piege') || el.classList.contains('skip-link')) continue;
            const cx = Math.min(Math.max(b.left + b.width / 2, 1), window.innerWidth - 1);
            const cy = b.top + b.height / 2;
            // hauteur atteignable : on remonte et on descend par pas de 2px
            let haut = cy, bas = cy;
            for (let d = 2; d <= 24; d += 2) {
              if (cy - d > 0 && atteint(el, cx, cy - d)) haut = cy - d; else break;
            }
            for (let d = 2; d <= 24; d += 2) {
              if (cy + d < window.innerHeight && atteint(el, cx, cy + d)) bas = cy + d; else break;
            }
            const utile = Math.max(b.height, bas - haut);
            if (utile < 40) {
              const nom = (el.textContent || '').trim() || (el.name || el.type || el.tagName);
              out.petites.push(nom.slice(0, 26) + ' h=' + Math.round(utile));
            }
          }
          // texte courant trop petit
          for (const el of document.querySelectorAll('p, li, span, a, input, textarea, button')) {
            const t = (el.textContent || '').trim();
            if (t.length < 12) continue;
            if (el.querySelector('*')) continue;
            const px = parseFloat(getComputedStyle(el).fontSize);
            // .piege : etiquette lue par les lecteurs d'ecran, jamais affichee
            if (el.closest('.skip-link') || el.closest('.piege') || el.classList.contains('piege')) continue;
            const cs2 = getComputedStyle(el);
            // Trois planchers, selon le role du texte : etiquette en
            // capitales, mention secondaire (gris clair), texte courant.
            const par = el.parentElement ? getComputedStyle(el.parentElement) : cs2;
            const etiquette = cs2.textTransform === 'uppercase' || par.textTransform === 'uppercase'
                           || parseFloat(cs2.letterSpacing) > 0.8 || parseFloat(par.letterSpacing) > 0.8;
            // gris de mention secondaire, sur fond clair comme sur fond navy
            const secondaire = /rgb\((138|160|107|139)/.test(cs2.color)
                            || /rgba\(255, 255, 255, 0\.[0-5]/.test(cs2.color);
            const plancher = etiquette ? 11 : (secondaire ? 12 : 15);
            if (px < plancher) out.minuscule.push(t.slice(0, 26) + ' ' + px + 'px' + (etiquette ? ' (etiquette)' : ''));
          }
        }
        return out;
      }, largeur);

      const lignes = [];
      if (r.debordement > 1) lignes.push(`deborde +${r.debordement}px ` + JSON.stringify(r.coupables.slice(0, 3)));
      if (r.croisements.length) lignes.push(`${r.croisements.length} filet(s) sur du texte @x=${[...new Set(r.croisements)].join(',')}`);
      if (r.petites.length) lignes.push(`${r.petites.length} cible(s) < 40px : ${[...new Set(r.petites)].slice(0, 4).join(' | ')}`);
      if (r.minuscule.length) lignes.push(`${r.minuscule.length} texte(s) sous le plancher : ${[...new Set(r.minuscule)].slice(0, 3).join(' | ')}`);
      if (journal.length) lignes.push('erreurs: ' + journal.slice(0, 3).join(' ; '));

      if (lignes.length) {
        soucis.push({ largeur, page, lignes });
        console.log(`${String(largeur).padEnd(5)} ${page.padEnd(26)} ${lignes.join('\n' + ' '.repeat(33))}`);
      }
      await ctx.close();
    }
  }

  console.log('\n' + '='.repeat(70));
  console.log(soucis.length ? `${soucis.length} combinaison(s) largeur/page a corriger`
                            : `aucun souci sur ${LARGEURS.length} largeurs x ${PAGES.length} pages`);
  await nav.close();
  process.exit(soucis.length ? 1 : 0);
})();

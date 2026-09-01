/* Harnais de tests navigateur.
   Attention : en JavaScript l'option Playwright est « viewport », pas
   « viewportSize » (qui est la forme Python). Mal nommee, elle est ignoree
   sans erreur et toutes les mesures se font a 1280 px. */
const { chromium } = require('/usr/lib/node_modules/playwright');

const BASE = process.env.BASE || 'http://127.0.0.1:8899';

const PAGES = ['accueil', 'services', 'avocats', 'contact', 'automatisations',
               'mentions-legales', 'politique-confidentialite', 'desabonnement'];

const LARGEURS = [360, 390, 430, 600, 768, 834, 1024, 1180, 1280, 1440, 1920];

async function ouvrir(navigateur, page, largeur, hauteur = 900) {
  const ctx = await navigateur.newContext({
    viewport: { width: largeur, height: hauteur },
    deviceScaleFactor: 1,
  });
  const pg = await ctx.newPage();
  const journal = [];
  pg.on('pageerror', e => journal.push('JS: ' + e.message));
  pg.on('requestfailed', r => journal.push('requete: ' + r.url()));
  pg.on('response', r => { if (r.status() >= 400) journal.push(r.status() + ' ' + r.url()); });
  await pg.goto(`${BASE}/${page}/`, { waitUntil: 'networkidle' });
  // forcer le chargement differe puis revenir en haut
  await pg.evaluate(() => new Promise(r => {
    let y = 0;
    const pas = () => {
      window.scrollTo(0, y); y += 500;
      if (y < document.body.scrollHeight) setTimeout(pas, 25);
      else { window.scrollTo(0, 0); setTimeout(r, 500); }
    };
    pas();
  }));
  // verifier que la largeur est bien celle demandee
  const reelle = await pg.evaluate(() => window.innerWidth);
  if (reelle !== largeur) throw new Error(`largeur demandee ${largeur}, obtenue ${reelle}`);
  return { ctx, pg, journal };
}

module.exports = { chromium, BASE, PAGES, LARGEURS, ouvrir };

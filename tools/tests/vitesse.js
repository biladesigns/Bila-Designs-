/* Mesure du poids et des metriques de rendu, en conditions telephone. */
const { chromium } = require('/usr/lib/node_modules/playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8899';
const PAGES = ['accueil', 'services', 'avocats', 'contact', 'automatisations'];

(async () => {
  const nav = await chromium.launch();
  for (const page of PAGES) {
    const ctx = await nav.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    const pg = await ctx.newPage();
    const poids = {};
    let total = 0, bloquant = 0;
    pg.on('response', async r => {
      try {
        const b = (await r.body()).length;
        const t = (r.headers()['content-type'] || '').split(';')[0];
        poids[t] = (poids[t] || 0) + b;
        total += b;
        const u = r.url();
        if (/\.css$/.test(u)) bloquant += b;
      } catch (e) {}
    });
    await pg.goto(`${BASE}/${page}/`, { waitUntil: 'load' });
    const m = await pg.evaluate(() => new Promise(res => {
      let lcp = 0;
      new PerformanceObserver(l => { for (const e of l.getEntries()) lcp = e.startTime; })
        .observe({ type: 'largest-contentful-paint', buffered: true });
      let cls = 0;
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; })
        .observe({ type: 'layout-shift', buffered: true });
      setTimeout(() => {
        const n = performance.getEntriesByType('navigation')[0] || {};
        const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0;
        res({ lcp: Math.round(lcp), cls: +cls.toFixed(4), fcp: Math.round(fcp),
              dcl: Math.round(n.domContentLoadedEventEnd || 0),
              elements: document.querySelectorAll('*').length });
      }, 2500);
    }));
    const parType = Object.entries(poids).sort((a,b)=>b[1]-a[1])
      .map(([t,b]) => `${t.replace('application/','').replace('text/','')} ${(b/1024).toFixed(0)}Ko`).join('  ');
    console.log(`${page.padEnd(16)} total ${(total/1024).toFixed(0).padStart(4)} Ko   FCP ${String(m.fcp).padStart(4)}ms   LCP ${String(m.lcp).padStart(4)}ms   CLS ${m.cls}   noeuds ${m.elements}`);
    console.log(`${''.padEnd(16)} ${parType}`);
    await ctx.close();
  }
  await nav.close();
})();

(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ACCENT = '39,67,227';

  var marquees = [];
  var halos = [];
  var glows = [];
  var guides = [];
  var breathers = [];
  var branches = [];
  var counters = [];
  var bursts = [];
  var burstLayer = null;
  var nav = null;

  function initNav() {
    if (nav) return;
    var host = document.querySelector('header nav');
    if (!host) return;
    var stale = document.querySelectorAll('[data-bila-navmark]');
    for (var s = 0; s < stale.length; s++) stale[s].remove();
    var links = [];
    var all = host.querySelectorAll('a');
    for (var i = 0; i < all.length; i++) {
      var bg = getComputedStyle(all[i]).backgroundColor || '';
      if (bg.indexOf('39, 67, 227') !== -1) continue;
      links.push(all[i]);
    }
    if (links.length < 2) return;

    var mark = document.createElement('div');
    mark.setAttribute('data-bila-navmark', '1');
    mark.style.cssText = 'position:fixed;left:0;top:0;height:9px;width:0;opacity:0;pointer-events:none;z-index:40;';
    mark.innerHTML =
      '<span style="position:absolute;left:0;right:0;top:8px;height:1px;background:#2743E3;"></span>' +
      '<span style="position:absolute;left:0;top:2px;width:1px;height:7px;background:#2743E3;"></span>' +
      '<span style="position:absolute;right:0;top:2px;width:1px;height:7px;background:#2743E3;"></span>';
    document.body.appendChild(mark);

    var active = -1;
    for (var k = 0; k < links.length; k++) {
      var col = getComputedStyle(links[k]).color || '';
      if (col.indexOf('39, 67, 227') !== -1) active = k;
    }
    if (active === -1) { mark.remove(); return; }

    var r0 = links[active].getBoundingClientRect();
    if (!r0.width) { mark.remove(); return; }
    mark.style.width = r0.width.toFixed(1) + 'px';
    mark.style.transform = 'translate3d(' + r0.left.toFixed(1) + 'px,' + (r0.bottom + 6).toFixed(1) + 'px,0)';
    mark.style.opacity = '1';

    nav = { links: links, mark: mark, from: null, to: active, active: active, start: -1 };

    links.forEach(function (link, idx) {
      link.addEventListener('click', function (e) {
        if (!nav || nav.active === idx) return;
        var rp = nav.links[nav.active].getBoundingClientRect();
        nav.from = { x: rp.left, w: rp.width };
        nav.active = idx;
        nav.start = lastT;
        var r1 = link.getBoundingClientRect();
        nav.mark.style.width = r1.width.toFixed(1) + 'px';
        nav.mark.style.transform = 'translate3d(' + r1.left.toFixed(1) + 'px,' + (r1.bottom + 6).toFixed(1) + 'px,0)';
        burstAt(r1.left + r1.width / 2, r1.bottom + 4, true);
      });
    });
  }

  function burstAt(x, y, dark) {
    if (reduce) return;
    if (!burstLayer) {
      burstLayer = document.createElement('div');
      burstLayer.style.cssText = 'position:fixed;left:0;top:0;width:0;height:0;overflow:visible;pointer-events:none;z-index:2147483000;';
      document.body.appendChild(burstLayer);
    }
    var n = 16;
    var now0 = performance.now();
    for (var i = 0; i < n; i++) {
      var el = document.createElement('span');
      var size = 3 + Math.random() * 4;
      el.style.cssText = 'position:fixed;left:0;top:0;width:' + size.toFixed(1) + 'px;height:' + size.toFixed(1) +
        'px;background:' + (dark ? '#2743E3' : '#FFFFFF') + ';will-change:transform,opacity;opacity:1;' +
        'transform:translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0) rotate(45deg);';
      burstLayer.appendChild(el);
      var a = (Math.PI * 2 * i) / n + (Math.random() - 0.5) * 0.35;
      var life = 0.52 + Math.random() * 0.28;
      var p = {
        el: el, x: x, y: y,
        vx: Math.cos(a) * (46 + Math.random() * 54),
        vy: Math.sin(a) * (46 + Math.random() * 54),
        spin: (Math.random() - 0.5) * 420,
        life: life,
        born: (now0 - (t0 || now0)) / 1000
      };
      bursts.push(p);
      (function (particle) {
        setTimeout(function () {
          var at = bursts.indexOf(particle);
          if (at !== -1) bursts.splice(at, 1);
          if (particle.el.parentNode) particle.el.remove();
        }, life * 1000 + 200);
      })(p);
    }
  }

  if (!window.__bilaClickBound) {
    window.__bilaClickBound = true;
    document.addEventListener('click', function (e) {
    var flip = e.target;
    while (flip && flip !== document.body && !flip.hasAttribute('data-flip')) flip = flip.parentElement;
    if (flip && flip !== document.body && flip.hasAttribute('data-flip')) {
      var inner = flip.querySelector('[data-flip-inner]');
      if (inner) {
        var on = inner.getAttribute('data-on') === '1';
        inner.setAttribute('data-on', on ? '0' : '1');
        inner.style.transform = on ? 'rotateY(0deg)' : 'rotateY(180deg)';
      }
      return;
    }
    var node = e.target;
    while (node && node !== document.body) {
      if (node.tagName === 'A' || node.tagName === 'BUTTON') break;
      node = node.parentElement;
    }
    if (!node || node === document.body) return;
    var cs = getComputedStyle(node);
    var bg = cs.backgroundColor || '';
    var isAccent = bg.indexOf('39, 67, 227') !== -1;
    var isLight = bg.indexOf('255, 255, 255') !== -1 && (cs.borderRadius || '').indexOf('999') !== -1;
    if (!isAccent && !isLight) return;
    var r = node.getBoundingClientRect();
    burstAt(r.left + r.width / 2, r.top + r.height / 2, isAccent);
    }, true);
  }

  function initCounters() {
    var cells = document.querySelectorAll('[data-rise]');
    if (!cells.length) return;
    if (!window.__bilaStatSheet) {
      var st = document.createElement('style');
      st.id = 'bila-stat-sheet';
      document.head.appendChild(st);
      window.__bilaStatSheet = st;
    }
    if (counters.length === cells.length) return;
    counters = [];
    for (var i = 0; i < cells.length; i++) {
      var key = cells[i].getAttribute('data-rise');
      if (!key) { key = 'r' + i; cells[i].setAttribute('data-rise', key); }
      counters.push({ key: key, seen: -1, order: i });
    }
  }

  function initDiagram() {
    var groups = document.querySelectorAll('svg g[id^="branch-"]');
    for (var i = 0; i < groups.length; i++) {
      var g = groups[i];
      if (g.__bilaBranch) continue;
      g.__bilaBranch = true;
      var path = g.querySelector('path');
      if (!path || !path.getTotalLength) continue;
      var len = path.getTotalLength();
      if (!len) continue;
      path.style.strokeDasharray = len + ' ' + len;
      path.style.strokeDashoffset = len;
      var dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('r', '2.8');
      dot.setAttribute('fill', '#5D7EFF');
      dot.setAttribute('opacity', '0');
      g.appendChild(dot);
      branches.push({ path: path, len: len, dot: dot, order: i });

      // the underline is a real dimension: it spans exactly from the label ink to the branch
      try {
        var title = g.querySelector('text');
        var rule = g.querySelector('line[data-rule]');
        if (title && rule && title.getBBox) {
          var tb = title.getBBox();
          if (tb.width) {
            if (rule.getAttribute('data-rule') === 'l') rule.setAttribute('x1', (tb.x - 8).toFixed(1));
            else rule.setAttribute('x2', (tb.x + tb.width + 8).toFixed(1));
            rule.setAttribute('data-rule', 'done');
          } else {
            g.__bilaBranch = false;
          }
        }
      } catch (err) {
        g.__bilaBranch = false;
      }
    }
  }

  function collect() {
    var all = document.querySelectorAll('div, span, a, button, img');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el.__bilaSeen) continue;
      var cs = getComputedStyle(el);
      var name = cs.animationName || '';

      if (name.indexOf('bila-marquee') !== -1) {
        el.__bilaSeen = true;
        el.style.animation = 'none';
        el.style.willChange = 'transform';
        marquees.push(el);
        continue;
      }
      if (name.indexOf('bila-halo') !== -1) {
        el.__bilaSeen = true;
        el.style.animation = 'none';
        el.style.opacity = '0';
        el.style.transform = 'none';
        el.style.borderColor = 'rgba(255,255,255,0.9)';
        halos.push({ el: el, delay: parseFloat(cs.animationDelay) || 0 });
        continue;
      }
      if (name.indexOf('bila-glow') !== -1) {
        el.__bilaSeen = true;
        el.style.animation = 'none';
        glows.push(el);
        continue;
      }
      if (name.indexOf('bila-breathe') !== -1) {
        el.__bilaSeen = true;
        el.style.animation = 'none';
        breathers.push(el);
        continue;
      }

      // background guide rules: 1px-wide absolute hairlines in a section's background layer only
      if (el.tagName === 'DIV' && cs.position === 'absolute' && !el.firstElementChild) {
        var host = el.parentElement;
        var isBgLayer = host && host.parentElement && host.parentElement.tagName === 'SECTION';
        if (!isBgLayer || el.closest('.border-glow-card')) continue;
        var r = el.getBoundingClientRect();
        if (r.width > 0 && r.width <= 2.5 && r.height >= 220) {
          el.__bilaSeen = true;
          el.style.overflow = 'hidden';
          var seg = document.createElement('span');
          seg.style.cssText = 'position:absolute;left:-1px;width:3px;height:210px;top:0;pointer-events:none;' +
            'background:linear-gradient(to bottom, rgba(' + ACCENT + ',0) 0%, rgba(' + ACCENT + ',0.85) 45%, rgba(' + ACCENT + ',0.95) 55%, rgba(' + ACCENT + ',0) 100%);' +
            'filter:blur(0.4px);box-shadow:0 0 14px 1px rgba(' + ACCENT + ',0.5);opacity:0;will-change:transform,opacity;';
          el.appendChild(seg);
          guides.push({ host: el, seg: seg, phase: Math.random(), speed: 7.5 + Math.random() * 5 });
        }
      }
    }
  }

  var t0 = 0;
  var lastT = 0;
  var lastFrame = 0;
  var frames = 0;

  function forceVisible() {
    if (window.__bilaStatSheet) window.__bilaStatSheet.textContent = '';
    for (var i = 0; i < counters.length; i++) counters[i].seen = -2;
    for (var d = 0; d < branches.length; d++) {
      branches[d].path.style.strokeDasharray = 'none';
      branches[d].path.style.strokeDashoffset = '0';
    }
  }

  function frame(now) {
    if (!t0) t0 = now;
    lastFrame = now;
    frames++;
    var t = (now - t0) / 1000;
    lastT = t;

    for (var i = 0; i < marquees.length; i++) {
      var track = marquees[i];
      var half = track.__half;
      if (!half) {
        var first = track.firstElementChild;
        half = first ? first.getBoundingClientRect().width : 0;
        track.__half = half;
      }
      if (half) {
        var x = (t * 42) % half;
        track.style.transform = 'translate3d(' + (0 - x).toFixed(1) + 'px,0,0)';
      }
    }

    for (var h = 0; h < halos.length; h++) {
      var ha = halos[h];
      var p = ((t - ha.delay) % 2.4) / 2.4;
      if (p < 0) p += 1;
      if (p < 0.65) {
        var k = p / 0.65;
        ha.el.style.inset = (1 + 11 * k).toFixed(1) + 'px';
        ha.el.style.opacity = (0.85 * (1 - k)).toFixed(3);
      } else {
        ha.el.style.opacity = '0';
      }
    }

    var s = 0.5 - 0.5 * Math.cos((t / 2.4) * Math.PI * 2);
    for (var g = 0; g < glows.length; g++) {
      glows[g].style.boxShadow =
        '0 0 0 ' + (9 * s).toFixed(1) + 'px rgba(' + ACCENT + ',' + (0.3 * (1 - s)).toFixed(2) + '), ' +
        '0 ' + (8 + 4 * s).toFixed(1) + 'px ' + (22 + 9 * s).toFixed(1) + 'px rgba(' + ACCENT + ',' + (0.28 + 0.16 * s).toFixed(2) + ')';
    }

    for (var b = 0; b < breathers.length; b++) {
      var bs = 0.5 - 0.5 * Math.cos((t / 9) * Math.PI * 2);
      breathers[b].style.filter = 'contrast(' + (1.04 + 0.02 * bs).toFixed(3) + ') saturate(' + (1.02 + 0.14 * bs).toFixed(3) + ')';
    }

    for (var q = 0; q < guides.length; q++) {
      var gu = guides[q];
      var hr = gu.host.getBoundingClientRect();
      if (hr.height < 80) { gu.seg.style.opacity = '0'; continue; }
      var segH = Math.min(210, Math.max(60, hr.height * 0.42));
      if (gu.segH !== segH) { gu.segH = segH; gu.seg.style.height = segH.toFixed(0) + 'px'; }
      var pp = ((t / gu.speed) + gu.phase) % 1;
      var span = hr.height - segH;
      gu.seg.style.transform = 'translate3d(0,' + (pp * span).toFixed(1) + 'px,0)';
      var fade = pp < 0.12 ? pp / 0.12 : (pp > 0.88 ? (1 - pp) / 0.12 : 1);
      gu.seg.style.opacity = (fade * 0.85).toFixed(3);
    }

    for (var d = 0; d < branches.length; d++) {
      var br = branches[d];
      var start = 0.35 + br.order * 0.22;
      var draw = Math.max(0, Math.min((t - start) / 1.1, 1));
      br.path.style.strokeDashoffset = (br.len * (1 - draw)).toFixed(1);
      if (draw >= 1) {
        var cyc = ((t - start - 1.1) / 4.8 + br.order * 0.09) % 1;
        if (cyc < 0) cyc += 1;
        var pt = br.path.getPointAtLength(br.len * (1 - cyc));
        br.dot.setAttribute('cx', pt.x.toFixed(1));
        br.dot.setAttribute('cy', pt.y.toFixed(1));
        var f2 = cyc < 0.1 ? cyc / 0.1 : (cyc > 0.72 ? Math.max(0, (0.88 - cyc) / 0.16) : 1);
        br.dot.setAttribute('opacity', f2.toFixed(2));
      }
    }

    if (counters.length && window.__bilaStatSheet) {
      var css = '';
      var vh = window.innerHeight;
      for (var c = 0; c < counters.length; c++) {
        var ct = counters[c];
        if (ct.seen === -2) continue;
        var live = document.querySelector('[data-rise="' + ct.key + '"]');
        if (!live) continue;
        if (ct.seen < 0) {
          var rr = live.getBoundingClientRect();
          if (!rr.height) continue;
          if (rr.top < vh * 0.88 && rr.bottom > 0) ct.seen = t;
          else if (frames > 2 && (performance.now() - lastFrame) < 300) { css += '[data-rise="' + ct.key + '"]{opacity:0;transform:translate3d(0,20px,0);}'; continue; }
          else continue;
        }
        var p2 = Math.max(0, Math.min((t - ct.seen) / 0.9, 1));
        var eased = 1 - Math.pow(1 - p2, 3);
        if (p2 >= 1) continue;
        css += '[data-rise="' + ct.key + '"]{opacity:' + Math.min(1, eased * 1.15).toFixed(3) +
               ';transform:translate3d(0,' + (20 * (1 - eased)).toFixed(1) + 'px,0);}';
      }
      window.__bilaStatSheet.textContent = css;
    }

    if (nav) {
      var target = nav.links[nav.active].getBoundingClientRect();
      var x = target.left, w = target.width;
      if (nav.from && nav.start >= 0) {
        var pn = Math.max(0, Math.min((t - nav.start) / 0.42, 1));
        var en = 1 - Math.pow(1 - pn, 3);
        x = nav.from.x + (target.left - nav.from.x) * en;
        w = nav.from.w + (target.width - nav.from.w) * en;
        if (pn >= 1) { nav.from = null; nav.start = -1; }
      }
      nav.mark.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + (target.bottom + 6).toFixed(1) + 'px,0)';
      nav.mark.style.width = w.toFixed(1) + 'px';
      nav.mark.style.opacity = target.width ? '1' : '0';
    }

    for (var k = bursts.length - 1; k >= 0; k--) {
      var bp = bursts[k];
      var age = (t - bp.born) / bp.life;
      if (age >= 1) { bp.el.remove(); bursts.splice(k, 1); continue; }
      var ez = 1 - Math.pow(1 - age, 2.4);
      bp.el.style.transform = 'translate3d(' + (bp.x + bp.vx * ez).toFixed(1) + 'px,' +
        (bp.y + bp.vy * ez + 26 * age * age).toFixed(1) + 'px,0) rotate(' + (45 + bp.spin * ez).toFixed(0) + 'deg)';
      bp.el.style.opacity = (1 - age * age).toFixed(3);
    }

    requestAnimationFrame(frame);
  }

  function initFirms() {
    var rows = document.querySelectorAll('[data-firm]');
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      if (row.__bilaFirm) continue;
      row.__bilaFirm = true;
      (function (r) {
        var card = r.querySelector('[data-firm-card]');
        if (!card) return;
        r.addEventListener('mousemove', function (e) {
          var rect = r.getBoundingClientRect();
          var x = e.clientX - rect.left - rect.width / 2;
          card.style.transform = 'translate3d(' + (x * 0.35).toFixed(1) + 'px,0,0)';
        });
        r.addEventListener('mouseenter', function () {
          card.style.opacity = '1';
          var sibs = document.querySelectorAll('[data-firm]');
          for (var k = 0; k < sibs.length; k++) if (sibs[k] !== r) sibs[k].style.opacity = '0.35';
        });
        r.addEventListener('mouseleave', function () {
          card.style.opacity = '0';
          var sibs = document.querySelectorAll('[data-firm]');
          for (var k = 0; k < sibs.length; k++) sibs[k].style.opacity = '1';
        });
      })(row);
    }
  }

  function syncNav() {
    if (!nav || !nav.mark || nav.from) return;
    var r = nav.links[nav.active].getBoundingClientRect();
    if (!r.width) return;
    if (Math.abs(r.left - nav.mark.getBoundingClientRect().left) > 1) {
      nav.mark.style.width = r.width.toFixed(1) + 'px';
      nav.mark.style.transform = 'translate3d(' + r.left.toFixed(1) + 'px,' + (r.bottom + 6).toFixed(1) + 'px,0)';
    }
  }

  function boot() {
    collect();
    initCounters();
    initNav();
    initFirms();
    try { initDiagram(); } catch (e) {}
    if (reduce) {
      if (window.__bilaStatSheet) window.__bilaStatSheet.textContent = '';
      for (var d = 0; d < branches.length; d++) { branches[d].path.style.strokeDasharray = 'none'; branches[d].path.style.strokeDashoffset = '0'; }
      for (var i = 0; i < guides.length; i++) guides[i].seg.style.display = 'none';
      for (var h = 0; h < halos.length; h++) halos[h].el.style.display = 'none';
      return;
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(syncNav);
    window.addEventListener('resize', syncNav);
    requestAnimationFrame(frame);
    setInterval(function () {
      var now = performance.now();
      var stale = now - lastFrame;
      if (stale > 900) forceVisible();
      else if (stale > 220) frame(now);
    }, 180);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) forceVisible();
    });
    var ticks = 0;
    var again = setInterval(function () {
      collect();
      initCounters();
      initNav();
      syncNav();
      initFirms();
      try { initDiagram(); } catch (e) {}
      if (++ticks > 40) clearInterval(again);
    }, 200);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

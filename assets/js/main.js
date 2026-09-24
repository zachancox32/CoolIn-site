/* ============================================================
   CoolIn interactions
   GSAP + ScrollTrigger. Short, quiet movements only.
   ============================================================ */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof gsap !== 'undefined';

  if (!hasGsap || reduced) {
    document.querySelectorAll('.js-hero,.js-up,.js-card,.js-step').forEach(function (el) {
      el.style.opacity = 1;
    });
    document.querySelectorAll('.step').forEach(function (el) { el.classList.add('is-on'); });
  }

  /* ---------- in page links without the #fragment in the address ----------
     A plain <a href="#calculator"> leaves /page#calculator in the address bar,
     which then gets copied and shared. This does the same jump, keeps the
     address clean, and moves focus to the target the way the browser would, so
     keyboard and screen reader users land in the same place. The scroll itself
     is unchanged: scrollIntoView follows the CSS smooth setting, and that
     already drops to instant under reduced motion. Links into another page,
     such as contact#quote, are left alone. */
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = decodeURIComponent(a.getAttribute('href').slice(1));
    var target = id && document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ block: 'start' });
    if (!target.hasAttribute('tabindex') && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(target.tagName)) {
      target.setAttribute('tabindex', '-1');
    }
    target.focus({ preventScroll: true });
    // arriving on a shared /page#section and then jumping elsewhere should not
    // leave the old fragment sitting there either
    if (location.hash) history.replaceState(null, '', location.pathname + location.search);
  });

  /* ---------- rough size calculator ---------- */
  (function () {
    var els = {
      w: document.getElementById('cW'), l: document.getElementById('cL'),
      h: document.getElementById('cH'), g: document.getElementById('cG'),
      pp: document.getElementById('cP'), t: document.getElementById('cT'),
      roof: document.getElementById('cR'),
      kw: document.getElementById('calcKw'), unit: document.getElementById('calcUnit'),
      price: document.getElementById('calcPrice'),
      // optional: only the standalone calculator page has these two
      btu: document.getElementById('calcBtu'), steps: document.getElementById('calcWork')
    };
    if (!els.w || !els.kw) return;

    // standard indoor unit sizes and our installed prices for a single wall unit
    var SIZES = [
      { kw: 2.0, price: 1850 }, { kw: 2.5, price: 1850 }, { kw: 3.5, price: 1995 },
      { kw: 5.0, price: 2280 }, { kw: 6.0, price: 2650 }, { kw: 7.1, price: 2950 }
    ];

    function num(el, fallback) {
      var v = parseFloat(el.value);
      return isNaN(v) || v <= 0 ? fallback : v;
    }

    // Each step is recorded as it is applied, so a page can show the working.
    // The arithmetic is unchanged from when this only returned the total.
    var trail = [];
    function picked(el) { return el.options[el.selectedIndex].text; }

    function work() {
      var w = num(els.w, 3.5), l = num(els.l, 4.5), area = w * l;
      var load = area * 0.155;                       // 155W per m2, matching the sizing table
      trail = [['Floor area', w + 'm \u00d7 ' + l + 'm = ' + area.toFixed(1) + ' m\u00b2', null],
               ['Starting load at 155W per m\u00b2', area.toFixed(1) + ' \u00d7 0.155', load]];
      load *= parseFloat(els.h.value);               // ceiling height
      trail.push(['Ceiling: ' + picked(els.h), '\u00d7 ' + parseFloat(els.h.value).toFixed(2), load]);
      load *= parseFloat(els.g.value);               // aspect and glazing
      trail.push(['Windows: ' + picked(els.g), '\u00d7 ' + parseFloat(els.g.value).toFixed(2), load]);
      if (els.roof.checked) {
        load *= 1.2;                                 // roof rooms gain from above all day
        trail.push(['Room in the roof', '\u00d7 1.20', load]);
      }
      var extra = Math.max(0, num(els.pp, 2) - 2);
      load += extra * 0.1;                           // bodies in the room
      trail.push(['People beyond the first two', extra + ' \u00d7 0.1 kW', load]);
      load += parseFloat(els.t.value);               // appliances and kit
      trail.push(['Room use: ' + picked(els.t), '+ ' + parseFloat(els.t.value).toFixed(1) + ' kW', load]);
      return load;
    }

    function showWorking(load, pick) {
      if (els.btu) {
        els.btu.textContent = (Math.round(load * 3412.14 / 100) * 100).toLocaleString('en-GB') + ' BTU/h';
      }
      if (!els.steps) return;
      els.steps.textContent = '';
      trail.concat([['Next standard size up', pick ? pick.kw.toFixed(1) + ' kW unit' : 'More than one unit', null]])
        .forEach(function (row) {
          var li = document.createElement('li');
          [row[0], row[1], row[2] === null ? '' : row[2].toFixed(2) + ' kW'].forEach(function (t, i) {
            var span = document.createElement('span');
            span.className = 'working__' + ['label', 'op', 'total'][i];
            span.textContent = t;
            li.appendChild(span);
          });
          els.steps.appendChild(li);
        });
    }

    function render(animate) {
      var load = work();
      var pick = null;
      for (var i = 0; i < SIZES.length; i++) {
        if (SIZES[i].kw >= load) { pick = SIZES[i]; break; }
      }

      var shown = Math.round(load * 10) / 10;
      if (animate && !reduced && typeof gsap !== 'undefined') {
        var from = parseFloat(els.kw.textContent) || 0;
        gsap.to({ v: from }, {
          v: shown, duration: .5, ease: 'power2.out',
          onUpdate: function () { els.kw.textContent = this.targets()[0].v.toFixed(1); }
        });
      } else {
        els.kw.textContent = shown.toFixed(1);
      }

      if (!pick) {
        els.unit.textContent = 'Past what one indoor unit will do comfortably';
        els.price.textContent = 'Two units or a ducted system, priced at survey';
      } else {
        els.unit.textContent = 'Points at a ' + pick.kw.toFixed(1).replace('.0', '') + 'kW wall unit';
        els.price.textContent = 'from £' + pick.price.toLocaleString('en-GB') + ' fitted, 0% VAT';
      }
      showWorking(load, pick);
    }

    ['input', 'change'].forEach(function (ev) {
      Object.keys(els).forEach(function (k) {
        if (els[k] && els[k].tagName && /INPUT|SELECT/.test(els[k].tagName)) {
          els[k].addEventListener(ev, function () { render(true); });
        }
      });
    });

    render(false);
  })();

  /* ---------- heating cost against a gas boiler ---------- */
  (function () {
    var g = function (id) { return document.getElementById(id); };
    var area = g('vArea'), hrs = g('vHrs'), ins = g('vIns'), scope = g('vScope'),
        elec = g('vElec'), gas = g('vGas'), mon = g('vMon');
    if (!area) return;

    var SCOP = 4.5;        // seasonal efficiency of a current A+++ wall unit
    var BOILER = 0.88;     // seasonal efficiency of a gas boiler in the real world
    var DUTY = 0.6;        // average call on peak heat loss across a season

    function n(el, d) { var v = parseFloat(el.value); return isNaN(v) || v <= 0 ? d : v; }
    function money(v) {
      return '£' + Math.round(v).toLocaleString('en-GB');
    }

    function calc() {
      var days = parseFloat(mon.value) * 30.4;
      var heat = n(area, 20) * (parseFloat(ins.value) / 1000) * n(hrs, 6) * DUTY; // kWh a day
      var hp = heat / SCOP * (n(elec, 25) / 100) * days;
      var likeForLike = heat / BOILER * (n(gas, 6.5) / 100) * days;
      var boiler = likeForLike * parseFloat(scope.value);
      return { hp: hp, boiler: boiler, like: likeForLike, save: boiler - hp };
    }

    var bars = { hp: g('vHpBar'), gas: g('vGasBar') };
    function paint() {
      var r = calc();
      var max = Math.max(r.hp, r.boiler, 1);
      var pct = r.save > 0 ? Math.round(r.save / r.boiler * 100) : 0;

      g('vHpCost').textContent = money(r.hp);
      g('vGasCost').textContent = money(r.boiler);
      g('vSave').textContent = money(Math.abs(r.save));
      var SCOPE_LABEL = { '1': 'this room only', '2.4': 'this room and the rest of the floor', '4': 'the whole house' };
      g('vGasLabel').firstChild.nodeValue = 'Gas central heating, ' + (SCOPE_LABEL[scope.value] || 'the whole house');

      if (r.save > 0) {
        g('vPct').textContent = 'That is ' + pct + '% off what the same comfort costs you now';
        document.querySelector('.vs__save').lastChild.nodeValue = ' cheaper';
      } else {
        g('vPct').textContent = 'On these figures the boiler is ahead. Check the tariffs you have typed in.';
        document.querySelector('.vs__save').lastChild.nodeValue = ' dearer';
      }

      g('vLike').textContent = 'Like for like on exactly the same heat, gas costs ' + money(r.like) +
        ' and the heat pump ' + money(r.hp) + '. The rest of the gap is the rooms you are not sitting in.';

      var wHp = Math.max(4, r.hp / max * 100), wGas = Math.max(4, r.boiler / max * 100);
      if (typeof gsap !== 'undefined' && !reduced) {
        gsap.to(bars.hp, { width: wHp + '%', duration: .6, ease: 'power2.out' });
        gsap.to(bars.gas, { width: wGas + '%', duration: .6, ease: 'power2.out' });
      } else {
        bars.hp.style.width = wHp + '%';
        bars.gas.style.width = wGas + '%';
      }
    }

    [area, hrs, ins, scope, elec, gas, mon].forEach(function (el) {
      el.addEventListener('input', paint);
      el.addEventListener('change', paint);
    });
    paint();
  })();

  /* ---------- header ---------- */
  var header = document.getElementById('header');
  function onScroll() {
    header.classList.toggle('is-stuck', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      nav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });
  }

  /* ---------- quote form ---------- */
  var form = document.getElementById('quoteForm');
  var done = document.getElementById('formDone');
  var isLocal = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname) || location.protocol === 'file:';
  if (form) {
  form.addEventListener('submit', function (e) {
    // On a real host the form posts to Netlify and lands on thanks.html.
    // Locally there is no handler, so show the confirmation panel instead.
    if (!isLocal) return;
    e.preventDefault();
    var required = form.querySelectorAll('[required]');
    for (var i = 0; i < required.length; i++) {
      if (!required[i].value.trim()) { required[i].focus(); return; }
    }
    done.hidden = false;
    if (hasGsap && !reduced) {
      gsap.fromTo(done, { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: .45, ease: 'power2.out' });
    }
  });
  }

  if (!hasGsap || reduced) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- hero entrance ---------- */
  var tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
  if (document.getElementById('scene')) {
    tl.from('#scene', { autoAlpha: 0, duration: 1.6, ease: 'power1.out' });
  }
  tl.fromTo('.js-hero', { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: .9, stagger: .11 }, .15);
  if (document.querySelector('.hero__scroll')) {
    tl.from('.hero__scroll', { autoAlpha: 0, duration: .8 }, '-=.3');
  }

  /* ---------- generic reveals ---------- */
  gsap.utils.toArray('.js-up').forEach(function (el) {
    gsap.fromTo(el, { opacity: 0, y: 26 }, {
      opacity: 1, y: 0, duration: .8, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 88%' }
    });
  });

  ScrollTrigger.batch('.js-card', {
    start: 'top 86%',
    onEnter: function (batch) {
      gsap.fromTo(batch, { opacity: 0, y: 34 }, {
        opacity: 1, y: 0, duration: .85, ease: 'power3.out', stagger: .09, overwrite: true
      });
    }
  });

  /* ---------- process steps ---------- */
  gsap.utils.toArray('.js-step').forEach(function (el, i) {
    gsap.fromTo(el, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: .8, delay: i * 0.06, ease: 'power3.out',
      scrollTrigger: {
        trigger: el, start: 'top 85%',
        onEnter: function () { el.classList.add('is-on'); }
      }
    });
  });

  var fill = document.getElementById('stepsFill');
  if (fill) {
    gsap.to(fill, {
      width: '100%', ease: 'none',
      scrollTrigger: { trigger: '#steps', start: 'top 72%', end: 'bottom 72%', scrub: .6 }
    });
  }

  /* ---------- counters ---------- */
  gsap.utils.toArray('.stat__n').forEach(function (el) {
    var target = parseFloat(el.dataset.count);
    var dec = parseInt(el.dataset.dec || '0', 10);
    var suffix = el.dataset.suffix || '';
    var obj = { v: 0 };
    gsap.to(obj, {
      v: target, duration: 1.8, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 90%' },
      onUpdate: function () {
        var n = dec ? obj.v.toFixed(dec) : Math.round(obj.v).toLocaleString('en-GB');
        el.textContent = n + suffix;
      }
    });
  });

  /* ---------- brand marquee ---------- */
  var row = document.querySelector('.marquee__row');
  if (row) {
    row.insertAdjacentHTML('beforeend',
      '<span class="marquee__dup" aria-hidden="true">' + row.innerHTML + '</span>');
    var half = row.scrollWidth / 2;
    var loop = gsap.to(row, { x: -half, duration: 34, ease: 'none', repeat: -1 });
    row.parentElement.addEventListener('pointerenter', function () { loop.timeScale(0.25); });
    row.parentElement.addEventListener('pointerleave', function () { loop.timeScale(1); });
    window.addEventListener('resize', function () {
      half = row.scrollWidth / 2;
      loop.vars.x = -half;
      loop.invalidate();
    });
  }

  /* ---------- accordion ---------- */
  document.querySelectorAll('.acc__item').forEach(function (item) {
    var body = item.querySelector('.acc__body');
    item.addEventListener('toggle', function () {
      if (item.open) {
        gsap.fromTo(body, { height: 0, opacity: 0 }, {
          height: 'auto', opacity: 1, duration: .4, ease: 'power2.out',
          onComplete: function () { ScrollTrigger.refresh(); }
        });
      }
    });
    item.querySelector('summary').addEventListener('click', function (e) {
      if (!item.open) return;
      e.preventDefault();
      gsap.to(body, {
        height: 0, opacity: 0, duration: .3, ease: 'power2.in',
        onComplete: function () { item.open = false; gsap.set(body, { clearProps: 'height,opacity' }); }
      });
    });
  });

  /* ---------- gentle parallax on the panel ---------- */
  if (document.querySelector('.panel')) {
    gsap.to('.panel', {
      y: -26, ease: 'none',
      scrollTrigger: { trigger: '.split', start: 'top bottom', end: 'bottom top', scrub: 1 }
    });
  }

  /* ---------- sub navigation active state ---------- */
  (function () {
    var bar = document.getElementById('subnav');
    if (!bar) return;
    var links = [].slice.call(bar.querySelectorAll('a'));
    links.forEach(function (a) {
      var target = document.querySelector(a.getAttribute('href'));
      if (!target) return;
      ScrollTrigger.create({
        trigger: target, start: 'top 40%', end: 'bottom 40%',
        onToggle: function (self) {
          if (!self.isActive) return;
          links.forEach(function (l) { l.classList.remove('is-active'); });
          a.classList.add('is-active');
        }
      });
    });
  })();

  /* WhatsApp deep link, prefilled with what the page is about so the
     enquiry arrives with context instead of a bare "hi". */
  (function () {
    var links = document.querySelectorAll('[data-wa]');
    if (!links.length) return;
    var SMALL = { under: 1, upon: 1, on: 1, in: 1 };
    var page = location.pathname.replace(/^\//, '').replace(/\.html$/, '') || 'index';
    var town = page.match(/^air-conditioning-(.+)$/);
    var ctx = 'air conditioning';
    if (town) {
      ctx = 'air conditioning in ' + town[1].split('-').map(function (w, i) {
        return (i && SMALL[w]) ? w : w.charAt(0).toUpperCase() + w.slice(1);
      }).join(' ');
    } else if (page === 'domestic') ctx = 'air conditioning at home';
    else if (page === 'commercial') ctx = 'commercial air conditioning';
    else if (page === 'servicing') ctx = 'a service';
    else if (page === 'repairs') ctx = 'a repair';
    else if (page === 'heat-pumps') ctx = 'an air source heat pump';
    else if (page === 'ventilation') ctx = 'ventilation';
    var text = '?text=' + encodeURIComponent('Hi CoolIn, I would like a quote for ' + ctx + '.');
    Array.prototype.forEach.call(links, function (a) {
      a.href = a.href.split('?')[0] + text;
    });
  })();

  ScrollTrigger.refresh();
})();

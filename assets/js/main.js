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

  /* ---------- rough size calculator ---------- */
  (function () {
    var els = {
      w: document.getElementById('cW'), l: document.getElementById('cL'),
      h: document.getElementById('cH'), g: document.getElementById('cG'),
      pp: document.getElementById('cP'), t: document.getElementById('cT'),
      roof: document.getElementById('cR'),
      kw: document.getElementById('calcKw'), unit: document.getElementById('calcUnit'),
      price: document.getElementById('calcPrice')
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

    function work() {
      var area = num(els.w, 3.5) * num(els.l, 4.5);
      var load = area * 0.155;                       // 155W per m2, matching the sizing table
      load *= parseFloat(els.h.value);               // ceiling height
      load *= parseFloat(els.g.value);               // aspect and glazing
      if (els.roof.checked) load *= 1.2;             // roof rooms gain from above all day
      load += Math.max(0, num(els.pp, 2) - 2) * 0.1; // bodies in the room
      load += parseFloat(els.t.value);               // appliances and kit
      return load;
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

  ScrollTrigger.refresh();
})();

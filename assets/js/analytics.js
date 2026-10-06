/* ============================================================
   CoolIn analytics: Google Analytics 4, only with consent.

   Nothing from Google loads until the visitor presses Accept. Until
   then there is no gtag.js, no cookie and no request to Google. The
   choice is kept in localStorage under coolin-consent, which is not a
   cookie and is needed to remember the answer, and it can be changed
   from the cookie policy page.

   With consent it also records enquiries: a completed form, counted when
   the thank you page loads (which form, from which page, never what was
   typed), phone link clicks and WhatsApp clicks, so it is possible to see
   which pages lead to work.
   ============================================================ */
(function () {
  var ID = 'G-4MGYWZ7WMD';
  var KEY = 'coolin-consent';
  var loaded = false;

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  function load() {
    if (loaded) return;
    loaded = true;
    gtag('consent', 'default', {
      analytics_storage: 'granted',
      ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'
    });
    gtag('js', new Date());
    gtag('config', ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(s);
  }

  function track(name, params) {
    if (!loaded) return;
    params = params || {};
    params.page_path = location.pathname;
    params.transport_type = 'beacon';
    gtag('event', name, params);
  }

  /* ---------- banner ---------- */
  function hideBanner() {
    var b = document.getElementById('consent');
    if (b) b.parentNode.removeChild(b);
  }

  function showBanner() {
    if (document.getElementById('consent')) return;
    var b = document.createElement('div');
    b.id = 'consent';
    b.className = 'consent';
    b.setAttribute('role', 'region');
    b.setAttribute('aria-label', 'Cookie choice');
    b.innerHTML =
      '<p class="consent__text">Can we use analytics cookies to see which pages are useful? ' +
      'Nothing is shared for advertising. <a href="/cookies">Cookie policy</a></p>' +
      '<div class="consent__btns">' +
      '<button type="button" class="btn btn--primary consent__btn" data-consent="granted">Accept</button>' +
      '<button type="button" class="btn btn--ghost consent__btn" data-consent="denied">Reject</button>' +
      '</div>';
    document.body.appendChild(b);
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-consent],[data-consent-reset],a[href^="tel:"],a[data-wa],a[data-save-contact],a[data-system]');
    if (!t) return;

    if (t.hasAttribute('data-consent')) {
      var v = t.getAttribute('data-consent');
      remember(v);
      hideBanner();
      if (v === 'granted') load();
      return;
    }
    if (t.hasAttribute('data-consent-reset')) {
      // Forget the answer and ask again. Cookies already set by an earlier
      // Accept are left to expire; the page says how to clear them sooner.
      try { localStorage.removeItem(KEY); } catch (err) {}
      showBanner();
      return;
    }
    if (t.matches('a[href^="tel:"]')) track('click_to_call');
    else if (t.hasAttribute('data-save-contact')) track('save_contact');
    else if (t.hasAttribute('data-system')) track('choose_system', { system: t.getAttribute('data-system') });
    else track('click_whatsapp');
  });

  /* ---------- enquiries ----------
     The lead is counted when the thank you page loads after a real
     submission, not when the button is pressed, so a submission that fails
     never counts. On submit the form name and page are noted for this tab
     only; /thanks reads the note once, sends generate_lead and clears it,
     so a refresh or a direct visit to /thanks does not count again. */
  var LEAD = 'coolin-lead';
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!loaded || !f || !f.hasAttribute || !f.hasAttribute('data-netlify')) return;
    try {
      sessionStorage.setItem(LEAD, JSON.stringify({ form: f.getAttribute('name') || 'form', page: location.pathname }));
    } catch (err) {}
  });

  function countLead() {
    if (!/^\/thanks(\.html)?$/.test(location.pathname)) return;
    var raw = null;
    try { raw = sessionStorage.getItem(LEAD); sessionStorage.removeItem(LEAD); } catch (err) {}
    if (!raw) return;
    var d = {};
    try { d = JSON.parse(raw) || {}; } catch (err) {}
    track('generate_lead', { form_name: d.form || 'form', form_page: d.page || '' });
  }

  /* ---------- start ---------- */
  var choice = stored();
  if (choice === 'granted') { load(); countLead(); }
  else if (choice !== 'denied') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showBanner);
    else showBanner();
  }
})();

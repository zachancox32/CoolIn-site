#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the six commercial sector pages from tools/_sectors_data.py.

Each sector was previously one H3 card on commercial.html. Six buyers with six
different problems were sharing one page, so only one of them could ever rank.
These are separate pages now, each hung off the commercial hub.

The shell (utility bar, header, footer, scripts) is lifted from index.html and
the quote form from commercial.html, exactly as the town pages do, so a change
to the shell reaches these pages through tools/sync-shell.py rather than being
maintained twice.

    python3 tools/build-sectors.py
"""
import re, json, html, os, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, 'tools')
from _sectors_data import SECTORS

IDX  = open('index.html', encoding='utf-8').read()
COMM = open('commercial.html', encoding='utf-8').read()
BASE = re.search(r'rel="canonical" href="(https://[^/]+)', IDX).group(1)
CSS_V = re.search(r'style\.css\?v=([A-Za-z0-9]+)', IDX).group(1)


def shell(name):
    return re.search(r'<!-- SHELL:%s:START -->.*?<!-- SHELL:%s:END -->' % (name, name),
                     IDX, re.S).group(0)

UTILITY = shell('UTILITY')
HEADER  = (shell('HEADER')
           # The shell comes from the homepage, where the logo is a self anchor.
           # On an inner page it has to be a link back to the homepage.
           .replace('<a class="logo" href="#top"', '<a class="logo" href="/"')
           .replace(' class="is-current" aria-current="page"', '')
           # Same shape sync-shell.py writes, so the two never disagree.
           .replace('<a href="commercial">',
                    '<a href="commercial" class="is-current" aria-current="page">', 1))
TAIL    = shell('FOOTER') + '\n</body>\n</html>\n'
QUOTE   = re.search(r'<section class="quote-sec" id="quote">.*?\n</section>\n', COMM, re.S).group(0)


def photo_srcset(ph):
    return ', '.join(f"assets/img/photos/{ph['name']}-{w}.jpg {w}w" for w in ph['widths'])


def head(s, slug):
    """The whole <head>, mirroring commercial.html so nothing drifts between them."""
    t, d, url = s['title'], s['desc'], f'{BASE}/{slug}'
    ph = s.get('photo')
    preload = (f'<link rel="preload" as="image" imagesrcset="{photo_srcset(ph)}" imagesizes="100vw" fetchpriority="high">\n'
               if ph else '')
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="CoolIn">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{BASE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CoolIn, air conditioning across the North West">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/img/og-image.png">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="geo.region" content="GB-MAN">
<meta name="geo.placename" content="Manchester">
<link rel="preload" href="assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="assets/css/style.css?v={CSS_V}">
<noscript><style>.js-hero,.js-up,.js-card,.js-step{{opacity:1!important}}</style></noscript>
__JSONLD__
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>

'''


def faq_entities(markup):
    """Pull the questions straight back out of the rendered FAQ so the schema can
    never say something different from the page. Same approach as the town pages."""
    out = []
    for m in re.finditer(r'<summary>(.*?)</summary>\s*<div class="acc__body">(.*?)</div>\s*</details>',
                         markup, re.S):
        q = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        a = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()
        out.append({"@type": "Question", "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}})
    return out


def build(s, others):
    slug = s['slug'] + '.html'

    trust = ''.join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in s['trust'])
    kf = '\n'.join(f'        <div class="kf__item"><dt>{k}</dt><dd>{v}</dd></div>'
                   for k, v in s['kf'])

    challenges = '\n'.join(f'''      <article class="sector js-card">
        <h3>{h}</h3>
        <p>{p}</p>
        <span class="sector__meta">{meta}</span>
      </article>''' for h, p, meta in s['challenges'])

    systems = '\n'.join(f'''      <article class="truth js-card"><span class="truth__n">{i:02d}</span>'''
                        f'''<h3>{h}</h3><p>{p}</p></article>'''
                        for i, (h, p) in enumerate(s['systems'], 1))

    # Optional "which suits your building" guide: situation, the recommended
    # system, and why. Plain HTML so it reads without script and can be quoted.
    chooser = ''
    if s.get('chooser'):
        rows = '\n'.join(f'''      <li class="chooser__row js-card">
        <p class="chooser__if"><span>If</span>{a}</p>
        <p class="chooser__pick"><strong>{b}</strong><span>{c}</span></p>
      </li>''' for a, b, c in s['chooser']['rows'])
        chooser = f'''
<!-- ============ CHOOSER ============ -->
<section class="section chooser" id="chooser">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Which suits you</p>
      <h2 class="js-up">{s['chooser']['h2']}</h2>
      <p class="sec-head__sub js-up">{s['chooser']['sub']}</p>
    </header>
    <ul class="chooser__list">
{rows}
    </ul>
  </div>
</section>
'''

    prices = '\n'.join('''      <div class="price-card js-card">
        <h3>{h}</h3>
        <p class="price-card__sub">{sub}. Installed prices, plus VAT</p>
        <ul class="price-list">
{rows}
        </ul>
      </div>'''.format(h=h, sub=sub, rows='\n'.join(
            f'          <li><span>{a}</span><strong>{b}</strong></li>' for a, b in rows))
        for h, sub, rows in s['prices'])

    # A page can show one "from" price instead of the per unit grid, for
    # buyers where the number of variables makes a list misleading.
    pf = s.get('price_from')
    if pf:
        incl = ''.join(f'<li>{x}</li>' for x in pf['includes'])
        price_block = f'''    <div class="price-from js-up">
      <div class="price-from__fig">
        <p class="price-from__label">{pf['label']}</p>
        <p class="price-from__n">from {pf['figure']}<span class="price-from__vat">plus VAT</span></p>
        <p class="price-from__sub">{pf['sub']}</p>
        <a class="btn btn--primary" href="#quote">Get a fixed price for your building</a>
      </div>
      <div class="price-from__inc">
        <p class="price-from__h">Every fixed price includes</p>
        <ul>{incl}</ul>
      </div>
    </div>'''
    else:
        price_block = f'''    <p class="price-caption js-up">Guide prices, installed, plus VAT. Confirmed at site survey.</p>
    <div class="price-grid">
{prices}
    </div>'''

    duties = '\n'.join('''      <article class="comp js-up">
        <h3>{h}</h3>
{body}
        <p class="comp__note">{note}</p>
      </article>'''.format(h=h, note=note,
                           body='\n'.join(f'        <p>{p}</p>' for p in paras))
        for h, paras, note in s['duties'])

    faq_block = '''<!-- ============ FAQ ============ -->
<section class="section section--tint" id="faq">
  <div class="wrap faq">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Questions</p>
      <h2 class="js-up">What {crumb} customers ask first</h2>
    </header>
    <div class="acc">
{items}
    </div>
  </div>
</section>

'''.format(crumb=s['crumb'].lower(), items='\n'.join(
        f'''      <details class="acc__item js-up">
        <summary>{q}</summary>
        <div class="acc__body"><p>{a}</p></div>
      </details>''' for q, a in s['faqs']))

    siblings = '\n'.join(f'<li><a href="{o["slug"]}">{o["nav"]}</a></li>' for o in others)

    ph = s.get('photo')
    if ph:
        # Decorative, so empty alt: it sets the scene and is not CoolIn's own work.
        backdrop = (f'<img class="hero__photo" src="assets/img/photos/{ph["name"]}-{ph["widths"][1]}.jpg" '
                    f'srcset="{photo_srcset(ph)}" sizes="100vw" alt="" '
                    f'style="object-position:{ph["position"]}" fetchpriority="high" decoding="async">')
        hero_cls = 'hero hero--inner hero--photo'
    else:
        backdrop = '<canvas id="scene" class="hero__canvas" aria-hidden="true"></canvas>'
        hero_cls = 'hero hero--inner'

    body = f'''<!-- ============ HERO ============ -->
<section class="{hero_cls}" id="hero">
  {backdrop}
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <nav class="crumbs js-hero" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><a href="commercial">For your business</a><span aria-hidden="true">/</span><span aria-current="page">{s['crumb']}</span>
      </nav>
      <p class="eyebrow js-hero"><span class="eyebrow__mark"></span>{s['eyebrow']}</p>
      <h1 class="js-hero">{s['h1a']}<br><span class="grad">{s['h1b']}</span></h1>
      <p class="lede js-hero">{s['lede']}</p>
      <div class="hero__btns js-hero">
        <a class="btn btn--primary btn--lg" href="#quote">Book a site survey</a>
        <a class="btn btn--line btn--lg" href="#costs">{'See the starting price' if s.get('price_from') else 'See guide prices'}</a>
      </div>
      <ul class="hero__trust js-hero">{trust}</ul>
    </div>
  </div>
</section>

<!-- ============ SUBNAV ============ -->
<nav class="subnav" id="subnav" aria-label="On this page">
  <div class="wrap">
    <ul>
      <li><a href="#key-facts">In short</a></li>
      <li><a href="#challenges">The problem</a></li>
      <li><a href="#systems">Systems</a></li>
      <li><a href="#costs">Budget</a></li>
      <li><a href="#duties">{s['du_nav']}</a></li>
      <li><a href="#faq">FAQs</a></li>
    </ul>
  </div>
</nav>

<!-- ============ KEY FACTS ============ -->
<section class="keyfacts" id="key-facts" aria-labelledby="kf-title">
  <div class="wrap">
    <div class="kf">
      <div class="kf__lead">
        <h2 id="kf-title">In short</h2>
        <p>{s['kf_lead']}</p>
      </div>
      <dl class="kf__grid">
{kf}
      </dl>
    </div>
  </div>
</section>

<!-- ============ CHALLENGES ============ -->
<section class="section" id="challenges">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>{s['ch_eyebrow']}</p>
      <h2 class="js-up">{s['ch_h2']}</h2>
      <p class="sec-head__sub js-up">{s['ch_sub']}</p>
    </header>
    <div class="sectors">
{challenges}
    </div>
  </div>
</section>

<!-- ============ SYSTEMS ============ -->
<section class="section section--dark" id="systems">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>The options</p>
      <h2 class="js-up">{s['sy_h2']}</h2>
      <p class="sec-head__sub js-up">{s['sy_sub']}</p>
    </header>
    <div class="truths">
{systems}
    </div>
  </div>
</section>
{chooser}
<!-- ============ COSTS ============ -->
<section class="section" id="costs">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Budget</p>
      <h2 class="js-up">{s['co_h2']}</h2>
      <p class="sec-head__sub js-up">{s['co_sub']}</p>
    </header>

{price_block}

    <p class="price-note js-up">{s['price_note']}</p>
  </div>
</section>

<!-- ============ DUTIES ============ -->
<section class="section section--tint" id="duties">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>{s['du_eyebrow']}</p>
      <h2 class="js-up">{s['du_h2']}</h2>
      <p class="sec-head__sub js-up">{s['du_sub']}</p>
    </header>
    <div class="compliance">
{duties}
    </div>
  </div>
</section>

<!-- ============ HOW IT RUNS ============ -->
<section class="section" id="process">
  <div class="wrap">
    <header class="sec-head sec-head--center">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>How it works</p>
      <h2 class="js-up">Survey, fixed quote, fitted around you</h2>
      <p class="sec-head__sub js-up">A free survey, a written price with the heat load working shown, and a programme set around your hours. The four stages are the same on every commercial job and are set out in full on the <a href="commercial#process">commercial page</a>, along with <a href="servicing">servicing plans</a> and what to do about <a href="repairs">breakdowns</a>. Guide prices for every type of system are in our guide to <a href="guides/air-conditioning-cost-manchester">what air conditioning costs in Manchester</a>, and contractors letting the package can see <a href="hvac-contractors">HVAC packages for contractors</a>.</p>
    </header>
  </div>
</section>

<!-- ============ WHERE WE WORK ============ -->
<section class="areas-strip" aria-label="Areas covered">
  <div class="wrap">
    <p class="js-up">{s['areas_line']}, including <a href="air-conditioning-manchester">Manchester</a>, <a href="air-conditioning-salford">Salford</a>, <a href="air-conditioning-stockport">Stockport</a>, <a href="air-conditioning-warrington">Warrington</a> and <a href="air-conditioning-liverpool">Liverpool</a>. <a href="areas">See every town we cover</a>.</p>
  </div>
</section>

<!-- ============ OTHER SECTORS ============ -->
<section class="section section--tint" id="sectors">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Other business types</p>
      <h2 class="js-up">We work in these too</h2>
      <p class="sec-head__sub js-up">Each sector has its own page, because a server room and a hair salon are genuinely different jobs. The <a href="commercial">commercial overview</a> covers what applies to all of them.</p>
    </header>
    <ul class="nearby js-up">{siblings}</ul>
  </div>
</section>

''' + faq_block + QUOTE

    ld = [
        {"@type": "Service",
         "name": s['service_type'],
         "serviceType": s['service_type'],
         "provider": {"@id": f"{BASE}/#business"},
         "areaServed": [{"@type": "City", "name": "Manchester"},
                        {"@type": "AdministrativeArea", "name": "North West England"}],
         "url": f"{BASE}/{s['slug']}",
         "description": s['ld_desc']},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "For your business",
             "item": f"{BASE}/commercial"},
            {"@type": "ListItem", "position": 3, "name": s['crumb'],
             "item": f"{BASE}/{s['slug']}"}]},
        {"@type": "FAQPage", "mainEntity": faq_entities(faq_block)},
    ]
    jsonld = ('<script type="application/ld+json">\n'
              + json.dumps({"@context": "https://schema.org", "@graph": ld},
                           ensure_ascii=False, indent=2)
              + '\n</script>')

    out = head(s, s['slug']).replace('__JSONLD__', jsonld)
    out += UTILITY + '\n' + HEADER + '\n\n<main id="main">\n\n' + body + '\n</main>\n\n' + TAIL
    open(slug, 'w', encoding='utf-8').write(out)
    return slug, len(re.sub(r'<[^>]+>', ' ', body).split())


# The label a sector is given when another sector links to it.
NAV = {'office-air-conditioning':    'Office air conditioning',
       'retail-air-conditioning':    'Shops and salons',
       'restaurant-air-conditioning': 'Restaurants, bars and kitchens',
       'gym-air-conditioning':       'Gyms and studios',
       'server-room-cooling':        'Server and comms rooms',
       'warehouse-air-conditioning': 'Warehouse and industrial',
       'modular-building-air-conditioning': 'Modular buildings and cabins'}

if __name__ == '__main__':
    for s in SECTORS:
        others = [{'slug': o['slug'], 'nav': NAV[o['slug']]}
                  for o in SECTORS if o['slug'] != s['slug']]
        name, words = build(s, others)
        print(f'  {name:34} {words:5} words')
    print(f'  {len(SECTORS)} sector page(s)')

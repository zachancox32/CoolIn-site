# -*- coding: utf-8 -*-
"""Builds a town page from the shared shell plus per town content.
Content lives in _towns_data.py. Nothing here is templated prose: every
town supplies its own intro, local knowledge cards and FAQs."""
import re, json, html, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

IDX = open('index.html').read()
SRC = open('air-conditioning-manchester.html').read()
BASE = 'https://www.cool-in.co.uk'
CSS_V = re.search(r'style\.css\?v=([A-Za-z0-9]+)', IDX).group(1)
JS_V  = re.search(r'main\.js\?v=(\d+)', IDX).group(1)
SCENE_V = re.search(r'scene\.js\?v=(\d+)', IDX).group(1)

def shell(name):
    return re.search(r'<!-- SHELL:%s:START -->.*?<!-- SHELL:%s:END -->' % (name, name), IDX, re.S).group(0)

UTILITY = shell('UTILITY')
HEADER  = (shell('HEADER')
           .replace('<a class="logo" href="#top"', '<a class="logo" href="index.html"')
           .replace(' class="is-current" aria-current="page"', ''))
FOOTER_BLOCK = shell('FOOTER')
TAIL = FOOTER_BLOCK + '\n</body>\n</html>\n'
QUOTE = re.search(r'<!-- ============ QUOTE / CONTACT ============ -->.*?\n</section>\n', SRC, re.S).group(0)

def head(title, desc, slug):
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}/{slug}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/{slug}">
<meta property="og:site_name" content="CoolIn">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{BASE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CoolIn, air conditioning across the North West">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/img/og-image.png">
<meta name="geo.region" content="GB-MAN">
<meta name="geo.placename" content="Manchester">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={CSS_V}">
<noscript><style>.js-hero,.js-up,.js-card,.js-step{{opacity:1!important}}</style></noscript>
__JSONLD__
</head>
<body id="top">

<a class="skip" href="#main">Skip to content</a>

'''

def faq_entities(markup):
    out=[]
    for m in re.finditer(r'<summary>(.*?)</summary>\s*<div class="acc__body">(.*?)</div>\s*</details>', markup, re.S):
        q = html.unescape(re.sub(r'<[^>]+>','',m.group(1))).strip()
        a = html.unescape(re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ',m.group(2)))).strip()
        out.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    return out

def build(t, neighbours):
    slug = t['slug'] + '.html'
    town, county = t['town'], t['county']

    cards = '\n'.join(f'''      <article class="sector js-card">
        <h3>{h}</h3>
        <p>{p}</p>
      </article>''' for h, p in t['local'])

    faqs = '\n'.join(f'''      <details class="acc__item js-up">
        <summary>{q}</summary>
        <div class="acc__body"><p>{a}</p></div>
      </details>''' for q, a in t['faqs'])

    faq_block = f'''<!-- ============ FAQ ============ -->
<section class="section section--tint" id="faq">
  <div class="wrap faq">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Local questions</p>
      <h2 class="js-up">Asked most often in {town}</h2>
    </header>
    <div class="acc">
{faqs}
    </div>
  </div>
</section>

'''
    near = '\n'.join(f'<li><a href="{h}">Air conditioning in {n}</a></li>' for n, h in neighbours)

    kf = '\n'.join(f'        <div class="kf__item"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [
        ('Town', town), ('County', county), ('Postcodes', t['postcodes']),
        ('Travel time', f"About {t['drive']} from our Manchester base"),
        ('Domestic from', '£1,850 fitted, zero rated for VAT until 31 March 2027'),
        ('Services', 'Installation, servicing, repairs, heat pumps, ventilation')])

    body = f'''<!-- ============ HERO ============ -->
<section class="hero hero--inner" id="hero">
  <canvas id="scene" class="hero__canvas" aria-hidden="true"></canvas>
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <nav class="crumbs js-hero" aria-label="Breadcrumb">
        <a href="index.html">CoolIn</a><span aria-hidden="true">/</span><a href="areas.html">Areas covered</a><span aria-hidden="true">/</span><span aria-current="page">{town}</span>
      </nav>
      <p class="eyebrow js-hero"><span class="eyebrow__mark"></span>{town} and {county}</p>
      <h1 class="js-hero">Air conditioning in<br><span class="grad">{town}</span></h1>
      <p class="lede js-hero">{t['intro']}</p>
      <div class="hero__btns js-hero">
        <a class="btn btn--primary btn--lg" href="#quote">Book a free survey</a>
        <a class="btn btn--line btn--lg" href="domestic.html#prices">See prices</a>
      </div>
      <ul class="hero__trust js-hero">
        <li><strong>{t['drive']}</strong><span>from our base</span></li>
        <li><strong>£1,850</strong><span>one room, fitted</span></li>
        <li><strong>0% VAT</strong><span>on domestic work</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- ============ KEY FACTS ============ -->
<section class="keyfacts" id="key-facts" aria-labelledby="kf-title">
  <div class="wrap">
    <div class="kf">
      <div class="kf__lead">
        <h2 id="kf-title">In short</h2>
        <p>CoolIn installs, services and repairs air conditioning throughout {town} and the wider {county} area, covering {t['postcodes']}. We are about {t['drive']} away, which is close enough to attend a breakdown in the same week rather than the same month.</p>
      </div>
      <dl class="kf__grid">
{kf}
      </dl>
    </div>
  </div>
</section>

<!-- ============ LOCAL ============ -->
<section class="section" id="local">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Local knowledge</p>
      <h2 class="js-up">What the buildings in {town} tend to need</h2>
      <p class="sec-head__sub js-up">{t['stock']}</p>
    </header>
    <div class="sectors">
{cards}
    </div>
  </div>
</section>

<!-- ============ SERVICES LINKS ============ -->
<section class="section section--dark" id="services">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>What we do in {town}</p>
      <h2 class="js-up">Everything from one bedroom unit to a full fit out</h2>
    </header>
    <div class="truths">
      <article class="truth js-card"><span class="truth__n">01</span><h3><a href="domestic.html">Home air conditioning</a></h3><p>Wall units, multi splits and ducted systems for houses and flats, from £1,850 fitted with no VAT to add.</p></article>
      <article class="truth js-card"><span class="truth__n">02</span><h3><a href="commercial.html">Commercial installation</a></h3><p>Offices, shops, kitchens, gyms and server rooms, designed around your heat load and fitted around your trading hours.</p></article>
      <article class="truth js-card"><span class="truth__n">03</span><h3><a href="servicing.html">Servicing and maintenance</a></h3><p>Plans from £89 per unit a year, keeping the manufacturer warranty valid and the running costs down.</p></article>
      <article class="truth js-card"><span class="truth__n">04</span><h3><a href="repairs.html">Repairs and callouts</a></h3><p>All makes and models, £95 for the first hour, with the common parts carried on the van.</p></article>
      <article class="truth js-card"><span class="truth__n">05</span><h3><a href="heat-pumps.html">Air source heat pumps</a></h3><p>Air to air heat pumps giving around 4.5kWh of heat per kWh of electricity, heating and cooling from one unit.</p></article>
      <article class="truth js-card"><span class="truth__n">06</span><h3><a href="ventilation.html">Ventilation</a></h3><p>Heat recovery, kitchen extract and make up air, and filtration where cooling alone will not fix the problem.</p></article>
    </div>
  </div>
</section>

<!-- ============ NEARBY ============ -->
<section class="section section--tint" id="nearby">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Nearby</p>
      <h2 class="js-up">We cover these too</h2>
      <p class="sec-head__sub js-up">Each town has its own page, because the housing stock and the planning rules genuinely differ. The <a href="areas.html">full coverage area</a> lists everywhere else we work.</p>
    </header>
    <ul class="nearby js-up">{near}</ul>
  </div>
</section>

''' + faq_block + QUOTE

    ld = [
      {"@type":"Service","serviceType":f"Air conditioning installation in {town}",
       "provider":{"@id":f"{BASE}/#business"},
       "areaServed":{"@type":"City","name":town,
                     "containedInPlace":{"@type":"AdministrativeArea","name":county}},
       "description":f"Air conditioning installation, servicing and repair throughout {town} and {county}, covering {t['postcodes']}."},
      {"@type":"Place","name":town,
       "geo":{"@type":"GeoCoordinates","latitude":t['lat'],"longitude":t['lon']}},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"CoolIn","item":f"{BASE}/"},
        {"@type":"ListItem","position":2,"name":"Areas covered","item":f"{BASE}/areas.html"},
        {"@type":"ListItem","position":3,"name":f"Air conditioning in {town}","item":f"{BASE}/{slug}"}]},
      {"@type":"FAQPage","mainEntity":faq_entities(faq_block)},
    ]
    jsonld = '<script type="application/ld+json">\n' + json.dumps(
        {"@context":"https://schema.org","@graph":ld}, ensure_ascii=False, indent=2) + '\n</script>'

    out = head(t['title'], t['desc'], slug).replace('__JSONLD__', jsonld)
    out += UTILITY + '\n' + HEADER + '\n\n<main id="main">\n\n' + body + '\n</main>\n\n' + TAIL
    open(slug, 'w').write(out)
    return slug, len(re.sub(r'<[^>]+>', ' ', body).split())

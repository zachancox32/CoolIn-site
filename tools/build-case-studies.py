#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds case studies from case-studies/projects/*.md into flat HTML pages.

Same approach as build-blog.py: reuses the shell out of index.html so there is
only ever one copy of the header, footer and nav to keep in step.

Everything a case study needs is a frontmatter field, so the whole thing is
fillable from the CMS with no markup.

    python3 tools/build-case-studies.py
"""
import os, re, sys, json, glob, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _md import render, frontmatter

IDX = open('index.html').read()
BASE = re.search(r'rel="canonical" href="(https://[^/]+)', IDX).group(1)
CSS_V = re.search(r'style\.css\?v=([A-Za-z0-9]+)', IDX).group(1)

def shell(name):
    m = re.search(r'<!-- SHELL:%s:START -->.*?<!-- SHELL:%s:END -->' % (name, name), IDX, re.S)
    return m.group(0)

UTILITY = shell('UTILITY')
HEADER  = (shell('HEADER')
           .replace('<a class="logo" href="#top"', '<a class="logo" href="/"')
           .replace(' class="is-current" aria-current="page"', ''))
FOOTER  = shell('FOOTER') + '\n</body>\n</html>\n'

MONTHS = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
def pretty(d):
    y, m, dd = d.split('-')
    return f'{int(dd)} {MONTHS[int(m)-1]} {y}'

# town name -> town page, built from the pages that actually exist
TOWNS = {}
for f in glob.glob('air-conditioning-*.html'):
    slug = os.path.basename(f)[len('air-conditioning-'):-5]
    TOWNS[slug.replace('-', ' ').title()] = f
    TOWNS[slug] = f

def town_link(name):
    if not name:
        return ''
    f = TOWNS.get(name) or TOWNS.get(name.strip().lower().replace(' ', '-'))
    return f'/{f}' if f else ''

def rootify(block):
    # shell links are now extensionless, so match the bare slug up to the
    # closing quote or a fragment
    block = re.sub(r'href="(?!https?:|tel:|mailto:|/|#)([a-z0-9\-]+)(?=["#])', r'href="/\1', block)
    block = block.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    return block

def head(title, desc, url, jsonld, robots=''):
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | CoolIn</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{robots}<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="CoolIn">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{BASE}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}/assets/img/og-image.png">
<meta name="geo.region" content="GB-MAN">
<meta name="geo.placename" content="Manchester">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={CSS_V}">
<noscript><style>.js-hero,.js-up,.js-card,.js-step{{opacity:1!important}}</style></noscript>
{jsonld}
</head>
<body id="top">

<a class="skip" href="#main">Skip to content</a>

'''

def img(src, alt, cls=''):
    if not src:
        return ''
    if not src.startswith(('http', '/')):
        src = '/' + src.lstrip('/')
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy" decoding="async">'

def section(heading, md):
    if not (md or '').strip():
        return ''
    return f'<h2>{html.escape(heading)}</h2>\n{render(md)}'

def build_one(path):
    fm, body = frontmatter(open(path).read())
    slug = fm.get('slug') or os.path.basename(path)[:-3]
    url = f'{BASE}/case-studies/{slug}'
    title = fm['title']
    desc  = fm.get('description', '')
    date  = (fm.get('date', '') or '')[:10]
    town  = fm.get('town', '')
    ptype = fm.get('property_type', '')
    seo_title = fm.get('seo_title') or title

    # spec strip, only the rows that were filled in
    spec = [('Location', town), ('Property', ptype), ('System', fm.get('system', '')),
            ('Rooms', fm.get('rooms', '')), ('Time on site', fm.get('duration', '')),
            ('Guide price', fm.get('guide_price', ''))]
    kf = ''.join(f'<div class="kf"><span class="kf__k">{html.escape(k)}</span>'
                 f'<span class="kf__v">{html.escape(str(v))}</span></div>'
                 for k, v in spec if str(v or '').strip())

    gallery = [g for g in (fm.get('gallery') or []) if g]
    gal_html = ''
    if gallery:
        gal_html = ('<div class="cs-gallery">'
                    + ''.join(img(g, f'{title}, photo {n+1}') for n, g in enumerate(gallery))
                    + '</div>')

    quote_html = ''
    if (fm.get('customer_quote') or '').strip():
        who = fm.get('customer_name', '')
        cite = f'<cite>{html.escape(who)}</cite>' if who.strip() else ''
        quote_html = (f'<blockquote class="cs-quote"><p>{html.escape(fm["customer_quote"])}</p>'
                      f'{cite}</blockquote>')

    tl = town_link(town)
    service = '/commercial.html' if 'commercial' in ptype.lower() else '/domestic.html'
    service_label = 'commercial air conditioning' if 'commercial' in ptype.lower() else 'home air conditioning'
    nearby = ''
    if tl:
        nearby = (f'<p class="cs-next">More on <a href="{tl}">air conditioning in '
                  f'{html.escape(town)}</a>, or what is involved in a '
                  f'<a href="{service}">{service_label}</a> installation.</p>')

    article = {"@type": "Article", "headline": title, "description": desc,
               "datePublished": date, "dateModified": fm.get('updated', date),
               "author": {"@id": f"{BASE}/#business"},
               "publisher": {"@id": f"{BASE}/#business"},
               "mainEntityOfPage": {"@type": "WebPage", "@id": url},
               "image": (fm.get('image') and f'{BASE}/{fm["image"].lstrip("/")}') or f'{BASE}/assets/img/og-image.png',
               "inLanguage": "en-GB"}
    if town:
        article["contentLocation"] = {"@type": "Place", "name": town}

    ld = {"@context": "https://schema.org", "@graph": [article,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Case studies", "item": f"{BASE}/case-studies"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'

    content = f'''<!-- ============ CASE STUDY ============ -->
<article class="post">
  <header class="post__head">
    <div class="wrap post__wrap">
      <nav class="crumbs crumbs--light js-up" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><a href="/case-studies">Case studies</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(title)}</span>
      </nav>
      <h1 class="js-up">{html.escape(title)}</h1>
      {f'<p class="lede js-up">{html.escape(desc)}</p>' if desc else ''}
      {f'<p class="post__meta js-up"><time datetime="{date}">{pretty(date)}</time></p>' if date else ''}
    </div>
  </header>
  <div class="wrap post__wrap">
    {f'<div class="keyfacts js-up">{kf}</div>' if kf else ''}
    {f'<p class="cs-hero-img js-up">{img(fm.get("image",""), title)}</p>' if fm.get('image') else ''}
    <div class="prose js-up">
{section('The brief', fm.get('brief',''))}
{section('What we did', fm.get('work',''))}
{section('The result', fm.get('result',''))}
{render(body) if body.strip() else ''}
    </div>
    {gal_html}
    {quote_html}
    {nearby}
    <p class="post__back"><a href="/case-studies">All case studies</a></p>
  </div>
</article>

'''
    out = head(seo_title, desc, url, jsonld) + rootify(UTILITY) + rootify(HEADER) \
        + '\n<main id="main">\n\n' + content + '\n</main>\n\n' + rootify(FOOTER)
    open(f'case-studies/{slug}.html', 'w').write(out)
    if len(seo_title) + 9 > 60:
        print(f'    WARNING {slug}: title is {len(seo_title)+9} chars, over the 60 that fit a search result')
    if desc and len(desc) > 160:
        print(f'    WARNING {slug}: description is {len(desc)} chars, over 160')
    if not desc:
        print(f'    WARNING {slug}: no description, so Google will invent the search snippet')
    return dict(slug=slug, title=title, desc=desc, date=date, url=url, town=town,
                ptype=ptype, image=fm.get('image', ''))

def build_index(items):
    if True:
        cards = '\n'.join(f'''      <article class="post-card js-card">
        <p class="post-card__date">{html.escape(' / '.join(x for x in [i['town'], i['ptype']] if x)) or '&nbsp;'}</p>
        <h2><a href="/case-studies/{i['slug']}">{html.escape(i['title'])}</a></h2>
        <p>{html.escape(i['desc'])}</p>
        <span class="post-card__go">See the job</span>
      </article>''' for i in items)
        grid = f'<div class="post-grid">\n{cards}\n    </div>'
        robots = ''

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "CoolIn case studies",
         "description": "Air conditioning installations across the North West, with the system, the property and what the job involved.",
         "url": f"{BASE}/case-studies",
         "isPartOf": {"@id": f"{BASE}/#business"},
         "hasPart": [{"@type": "Article", "headline": i['title'], "url": i['url'],
                      "datePublished": i['date']} for i in items]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Case studies", "item": f"{BASE}/case-studies"}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'

    body = f'''<!-- ============ HERO ============ -->
<section class="hero hero--inner" id="hero">
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <nav class="crumbs js-hero" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><span aria-current="page">Case studies</span>
      </nav>
      <p class="eyebrow js-hero"><span class="eyebrow__mark"></span>Our work</p>
      <h1 class="js-hero">Air conditioning jobs,<br><span class="grad">start to finish</span></h1>
      <p class="lede js-hero">Real installations across the North West. The property, the system we fitted, what made the job awkward and how long it took.</p>
    </div>
  </div>
</section>

<!-- ============ CASE STUDIES ============ -->
<section class="section" id="work">
  <div class="wrap">
    {grid}
  </div>
</section>

'''
    quote = re.search(r'<!-- ============ QUOTE / CONTACT ============ -->.*?\n</section>\n',
                      open('domestic.html').read(), re.S).group(0)
    out = head('Case studies',
               'Air conditioning installations across the North West. The property, the system fitted, what the job involved and how long it took.',
               f'{BASE}/case-studies.html', jsonld, robots)
    out += UTILITY + HEADER + '\n<main id="main">\n\n' + body + quote + '\n</main>\n\n' + FOOTER
    open('case-studies.html', 'w').write(out)

MARKER = '<!-- CASE-STUDIES-LINK -->'

def set_footer_link(show):
    """The footer link only exists while there is something to link to."""
    changed = 0
    for f in glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('case-studies/*.html'):
        s = open(f, encoding='utf-8').read()
        href = '/case-studies.html' if '/' in f else 'case-studies.html'
        link = f'<li><a href="{href}">Case studies</a></li>'
        n = s.replace(link, MARKER) if not show else s.replace(MARKER, link)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); changed += 1
    return changed

items = sorted((build_one(p) for p in glob.glob('case-studies/projects/*.md')),
               key=lambda i: i['date'], reverse=True)

if items:
    build_index(items)
    set_footer_link(True)
    for i in items:
        print(f"  case-studies/{i['slug']+'.html':44s} {i['town']}")
    print(f"  case-studies.html  listing {len(items)} case stud{'y' if len(items)==1 else 'ies'}")
else:
    # Nothing to show yet, so the page is not built and nothing links to it.
    if os.path.exists('case-studies.html'):
        os.remove('case-studies.html')
    set_footer_link(False)
    print('  case-studies: none yet, page not built and footer link hidden')

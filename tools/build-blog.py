#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the blog from blog/posts/*.md into flat HTML pages.

Runs on Netlify (python3 is in the build image) and locally, so a post can
be checked before it goes live. Reuses the site shell from index.html, so
posts inherit the real header, footer, nav and styling with no second copy
of the template to keep in step.

    python3 tools/build-blog.py
"""
import os, re, sys, json, glob, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _md import render, frontmatter

CRYSTAL = '<svg class="post__mark" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M12 2v20"/><path d="M3.3 7 20.7 17"/><path d="M20.7 7 3.3 17"/><path d="M12 6 9.4 3.4M12 6l2.6-2.6M12 18l-2.6 2.6M12 18l2.6 2.6"/><path d="m17.1 9 3.2-.9M17.1 9l.9 3.2M6.9 15l-3.2.9M6.9 15 6 11.8"/><path d="m17.1 15 3.2.9M17.1 15l.9-3.2M6.9 9l-3.2-.9M6.9 9 6 12.2"/></g></svg>'
CRYSTAL_CARD = CRYSTAL.replace('post__mark', 'post-card__mark')

IDX = open('index.html').read()
BASE = re.search(r'rel="canonical" href="(https://[^/]+)', IDX).group(1)
CSS_V = re.search(r'style\.css\?v=([A-Za-z0-9]+)', IDX).group(1)

def shell(name):
    m = re.search(r'<!-- SHELL:%s:START -->.*?<!-- SHELL:%s:END -->' % (name, name), IDX, re.S)
    return m.group(0)

UTILITY = shell('UTILITY')
HEADER  = (shell('HEADER')
           .replace('<a class="logo" href="#top"', '<a class="logo" href="/"')
           .replace(' class="is-current" aria-current="page"', '')
           .replace('<a href="blog">', '<a href="blog" class="is-current" aria-current="page">'))
FOOTER  = shell('FOOTER') + '\n</body>\n</html>\n'

MONTHS = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
def pretty(d):
    y, m, dd = d.split('-')
    return f'{int(dd)} {MONTHS[int(m)-1]} {y}'

def authors():
    out = {}
    for f in glob.glob('blog/authors/*.json'):
        a = json.load(open(f))
        out[a.get('id') or os.path.basename(f)[:-5]] = a
    return out
AUTHORS = authors()

def head(title, desc, url, jsonld, extra=''):
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | CoolIn</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
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
{extra}{jsonld}
</head>
<body id="top">

<a class="skip" href="#main">Skip to content</a>

'''

def rootify(block):
    """Posts live at /blog/<slug>, so shell links need a leading slash."""
    # shell links are now extensionless, so match the bare slug up to the
    # closing quote or a fragment
    block = re.sub(r'href="(?!https?:|tel:|mailto:|/|#)([a-z0-9\-]+)(?=["#])', r'href="/\1', block)
    block = block.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    block = block.replace('src="/assets/js/', 'src="/assets/js/')
    return block

def author_block(post):
    a = AUTHORS.get(post.get('author', ''), None)
    if not a:
        return ('<p class="post__by">By the CoolIn team</p>', {"@type": "Organization", "name": "CoolIn",
      "alternateName": "CoolIn Air Conditioning Specialists"})
    creds = a.get('credentials') or []
    cred_html = ''.join(f'<li>{html.escape(c)}</li>' for c in creds)
    card = f'''
    <aside class="author-card">
      <div>
        <p class="author-card__name">{html.escape(a.get("name",""))}</p>
        <p class="author-card__role">{html.escape(a.get("role",""))}</p>
        <p class="author-card__bio">{html.escape(a.get("bio",""))}</p>
        {f'<ul class="author-card__creds">{cred_html}</ul>' if creds else ''}
      </div>
    </aside>'''
    schema = {"@type": "Person", "name": a.get("name", ""), "jobTitle": a.get("role", "")}
    if a.get('linkedin'):
        schema['sameAs'] = [a['linkedin']]
    return (f'<p class="post__by">By {html.escape(a.get("name",""))}, {html.escape(a.get("role",""))}</p>', schema), card

def scan(path):
    """Frontmatter and length only, so related links can be worked out before
    any page is written."""
    fm, body = frontmatter(open(path).read())
    words = len(re.sub(r'<[^>]+>', ' ', render(body)).split())
    return dict(slug=fm.get('slug') or os.path.basename(path)[:-3],
                title=fm['title'], desc=fm.get('description', ''),
                date=(fm.get('date', '') or '')[:10],
                category=fm.get('category') or 'Advice',
                mins=max(1, round(words / 200)))


def related(me, all_posts, n=3):
    """Same category first, then most recent. Never the post you are reading."""
    others = [p for p in all_posts if p['slug'] != me['slug']]
    same = [p for p in others if p['category'] == me['category']]
    rest = [p for p in others if p['category'] != me['category']]
    return (same + rest)[:n]


def build_post(path, siblings=()):
    fm, body = frontmatter(open(path).read())
    slug = fm.get('slug') or os.path.basename(path)[:-3]
    url = f'{BASE}/blog/{slug}'
    title, desc, date = fm['title'], fm.get('description', ''), fm.get('date', '')[:10]
    # the <title> tag has to fit in a search result; the h1 does not.
    seo_title = fm.get('seo_title') or title
    words = len(re.sub(r'<[^>]+>', ' ', render(body)).split())
    mins = max(1, round(words / 200))
    ab = author_block(fm)
    byline, aschema, card = (ab[0][0], ab[0][1], ab[1]) if isinstance(ab[0], tuple) else (ab[0], ab[1], '')

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": title, "description": desc,
         "datePublished": date, "dateModified": fm.get('updated', date),
         "author": aschema,
         "publisher": {"@id": f"{BASE}/#business"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "image": f"{BASE}/assets/img/og-image.png",
         "inLanguage": "en-GB"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'

    me = dict(slug=slug, title=title, category=fm.get('category') or 'Advice')
    near = related(me, siblings)
    more = ''
    if near:
        cards = '\n'.join(f'''        <article class="post-card js-card">
          <div class="post-card__panel">
            <span class="post-card__cat">{html.escape(o['category'])}</span>
            <h2><a href="/blog/{o['slug']}">{html.escape(o['title'])}</a></h2>
          </div>
          <div class="post-card__body">
            <p>{html.escape(o['desc'])}</p>
            <p class="post-card__meta"><time datetime="{o['date']}">{pretty(o['date'])}</time>
              <span aria-hidden="true">&middot;</span>{o['mins']} min read</p>
            <span class="post-card__go">Read it</span>
          </div>
        </article>''' for o in near)
        more = f'''
  <section class="post-more">
    <div class="wrap">
      <h2 class="post-more__title js-up">Keep reading</h2>
      <div class="post-grid">
{cards}
      </div>
    </div>
  </section>
'''

    content = f'''<!-- ============ POST ============ -->
<article class="post">
  <header class="post__head">
    {CRYSTAL}
    <div class="wrap post__wrap">
      <nav class="crumbs crumbs--light js-up" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><a href="/blog">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(title)}</span>
      </nav>
      <p class="post__cat js-up">{html.escape(fm.get('category') or 'Advice')}</p>
      <h1 class="js-up">{html.escape(title)}</h1>
      <p class="post__meta js-up"><time datetime="{date}">{pretty(date)}</time>
        <span aria-hidden="true">&middot;</span> {mins} min read{byline.replace('<p class="post__by">', ' &middot; ').replace('</p>','')}</p>
    </div>
  </header>
  <div class="wrap post__wrap">
    <div class="prose js-up">
{render(body)}
    </div>
{card}
    <aside class="post-cta js-up">
      <div>
        <h2>Thinking about it for your own place?</h2>
        <p>Free survey, a written price within 48 hours, and no sales visit. Tell us the rooms and we will do the rest.</p>
      </div>
      <div class="post-cta__act">
        <a class="btn btn--primary" href="/contact">Book a free survey</a>
        <a class="post-cta__tel" href="tel:+447391523255">or call 07391 523255</a>
      </div>
    </aside>
    <p class="post__back"><a href="/blog">All articles</a></p>
  </div>
</article>
{more}
'''

    out = head(seo_title, desc, url, jsonld) + rootify(UTILITY) + rootify(HEADER) \
        + '\n<main id="main">\n\n' + content + '\n</main>\n\n' + rootify(FOOTER)
    open(f'blog/{slug}.html', 'w').write(out)
    if len(seo_title) + 9 > 60:
        print(f'    WARNING {slug}: title is {len(seo_title)+9} chars, over the 60 that fit a search result')
    if len(desc) > 160:
        print(f'    WARNING {slug}: description is {len(desc)} chars, over 160')
    return dict(slug=slug, title=title, desc=desc, date=date, url=url,
                author=fm.get('author', ''), words=words,
                category=fm.get('category') or 'Advice',
                mins=max(1, round(words / 200)))

def build_index(posts):
    cards = '\n'.join(f'''      <article class="post-card js-card">
        <div class="post-card__panel">
          <span class="post-card__cat">{html.escape(p['category'])}</span>
          <h2><a href="/blog/{p['slug']}">{html.escape(p['title'])}</a></h2>
        </div>
        <div class="post-card__body">
          <p>{html.escape(p['desc'])}</p>
          <p class="post-card__meta">
            <time datetime="{p['date']}">{pretty(p['date'])}</time>
            <span aria-hidden="true">&middot;</span>{p['mins']} min read
          </p>
          <span class="post-card__go">Read it</span>
        </div>
      </article>''' for p in posts)

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "name": "CoolIn air conditioning advice",
         "description": "Straight answers to the questions people actually ask about air conditioning: what it costs, what the rules are, and what the equipment really does.",
         "publisher": {"@id": f"{BASE}/#business"}, "url": f"{BASE}/blog",
         "blogPost": [{"@type": "BlogPosting", "headline": p['title'],
                       "url": p['url'], "datePublished": p['date']} for p in posts]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog"}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'

    body = f'''<!-- ============ HERO ============ -->
<section class="hero hero--inner" id="hero">
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <nav class="crumbs js-hero" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><span aria-current="page">Blog</span>
      </nav>
      <p class="eyebrow js-hero"><span class="eyebrow__mark"></span>Advice</p>
      <h1 class="js-hero">Air conditioning,<br><span class="grad">explained properly</span></h1>
      <p class="lede js-hero">Straight answers to the questions we get asked on the phone. What it costs to run, what the rules actually say, and what the equipment does when nobody is selling you anything.</p>
    </div>
  </div>
</section>

<!-- ============ POSTS ============ -->
<section class="section" id="posts">
  <div class="wrap">
    <div class="post-grid">
{cards}
    </div>
  </div>
</section>

'''
    quote = re.search(r'<!-- ============ QUOTE / CONTACT ============ -->.*?\n</section>\n',
                      open('domestic.html').read(), re.S).group(0)
    out = head('Air conditioning advice',
               'Straight answers on air conditioning: running costs, planning permission, heating with a heat pump, and what the equipment actually does.',
               f'{BASE}/blog', jsonld)
    out += UTILITY + HEADER + '\n<main id="main">\n\n' + body + quote + '\n</main>\n\n' + FOOTER
    open('blog.html', 'w').write(out)

# Guarded so build-guides.py can import head, rootify and author_block from
# here without rebuilding the blog as a side effect.
if __name__ == '__main__':
    paths = sorted(glob.glob('blog/posts/*.md'))
    siblings = sorted((scan(p) for p in paths), key=lambda p: p['date'], reverse=True)
    posts = sorted((build_post(p, siblings) for p in paths), key=lambda p: p['date'], reverse=True)
    if posts:
        build_index(posts)
    for p in posts:
        print(f"  blog/{p['slug']+'.html':44s} {p['words']:5d} words  {p['date']}")
    print(f"  blog.html  listing {len(posts)} post(s)")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds guides from guides/source/*.md into /guides/<slug> and a /guides hub.

A guide is a permanent answer to one question people ask Google or an AI
assistant, such as "Can I install air conditioning in a terraced house?". Unlike
a blog post it carries no date on the page, lives at an address that never
changes, and is listed on the service page it relates to, so it inherits that
page's internal link weight instead of sitting deep in /blog.

The page is ordered the way answer engines read: the question as the h1, a
short answer that stands on its own, key facts, then the full answer and the
follow up questions, all carried in Article and FAQPage markup.

Everything a guide needs is a frontmatter field, so it is written in the CMS:

    title        the question, word for word
    answer       40 to 60 words, answering it in the first sentence
    key_facts    optional list of one line facts
    service      domestic, commercial, servicing, repairs, heat-pumps, ventilation
    seo_title    optional, shorter <title>
    description  optional, otherwise the short answer is used
    author       an id from blog/authors
    updated      when the answer was last checked, never shown on the page
    faqs         optional list of {question, answer}

With no guides the hub is not built, the footer link is hidden and the service
page slots are empty, the same way case studies behave.

    python3 tools/build-guides.py
"""
import os, re, sys, json, glob, html, importlib.util, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.join(HERE, '..'))
from _md import render, frontmatter

# head(), rootify() and author_block() come from the blog builder, which is
# guarded so importing it does not rebuild the blog.
_spec = importlib.util.spec_from_file_location('build_blog', os.path.join(HERE, 'build-blog.py'))
blog = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(blog)
BASE, CRYSTAL, head, rootify, author_block = blog.BASE, blog.CRYSTAL, blog.head, blog.rootify, blog.author_block
UTILITY, FOOTER = blog.UTILITY, blog.FOOTER
HEADER = (blog.shell('HEADER')
          .replace('<a class="logo" href="#top"', '<a class="logo" href="/"')
          .replace(' class="is-current" aria-current="page"', ''))

SRC = 'guides/source'
SERVICES = {                      # CMS value -> (page, how the page is named)
    'domestic':    ('domestic',    'Home air conditioning'),
    'commercial':  ('commercial',  'Commercial air conditioning'),
    'servicing':   ('servicing',   'Air conditioning servicing'),
    'repairs':     ('repairs',     'Air conditioning repairs'),
    'heat-pumps':  ('heat-pumps',  'Air source heat pumps'),
    'ventilation': ('ventilation', 'Ventilation'),
}
QUOTE = re.search(r'<!-- ============ QUOTE / CONTACT ============ -->.*?\n</section>\n',
                  open('domestic.html', encoding='utf-8').read(), re.S).group(0)


def clip(text, n=158):
    """A meta description from the short answer, cut at a word boundary."""
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip(',;:')
    return cut + '.' if not cut.endswith('.') else cut


def load(path):
    fm, body = frontmatter(open(path, encoding='utf-8').read())
    slug = os.path.basename(path)[:-3]
    for need in ('title', 'answer'):
        if not str(fm.get(need, '')).strip():
            sys.exit(f'  build-guides: {path} has no {need}, and a guide cannot work without it')
    svc = fm.get('service') or 'domestic'
    if svc not in SERVICES:
        sys.exit(f'  build-guides: {path} names service "{svc}", which is not one of {", ".join(SERVICES)}')
    facts = fm.get('key_facts') or []
    faqs = [f for f in (fm.get('faqs') or []) if isinstance(f, dict) and f.get('question') and f.get('answer')]
    updated = str(fm.get('updated') or '')[:10] or time.strftime('%Y-%m-%d')
    return dict(slug=slug, fm=fm, body=body, title=fm['title'].strip(), answer=fm['answer'].strip(),
                facts=facts if isinstance(facts, list) else [], faqs=faqs, service=svc,
                updated=updated, url=f'{BASE}/guides/{slug}',
                desc=(fm.get('description') or '').strip() or clip(fm['answer']),
                seo_title=(fm.get('seo_title') or '').strip() or fm['title'].strip())


def related(g, guides, n=3):
    """Same service first, then the rest, never itself."""
    same = [o for o in guides if o['slug'] != g['slug'] and o['service'] == g['service']]
    rest = [o for o in guides if o['slug'] != g['slug'] and o['service'] != g['service']]
    return (same + rest)[:n]


def card(o):
    return f'''        <article class="post-card js-card">
          <div class="post-card__panel">
            <span class="post-card__cat">{html.escape(SERVICES[o['service']][1])}</span>
            <h2><a href="/guides/{o['slug']}">{html.escape(o['title'])}</a></h2>
          </div>
          <div class="post-card__body">
            <p>{html.escape(clip(o['answer'], 150))}</p>
            <span class="post-card__go">Read the answer</span>
          </div>
        </article>'''


def build_one(g, guides):
    page, service_name = SERVICES[g['service']]
    ab = author_block(g['fm'])
    byline, aschema, author_card = (ab[0][0], ab[0][1], ab[1]) if isinstance(ab[0], tuple) else (ab[0], ab[1], '')
    byline = re.sub(r'</?p[^>]*>', '', byline)

    facts = ''
    if g['facts']:
        facts = '\n        <ul class="answer__facts">\n' + '\n'.join(
            f'          <li>{html.escape(str(f))}</li>' for f in g['facts']) + '\n        </ul>'

    faq_html = ''
    if g['faqs']:
        faq_html = '''
    <section class="guide-faq js-up" aria-labelledby="next-q">
      <h2 id="next-q">Questions people ask next</h2>
      <div class="acc">
''' + '\n'.join(f'''        <details class="acc__item">
          <summary>{html.escape(f['question'])}</summary>
          <div class="acc__body"><p>{html.escape(f['answer'])}</p></div>
        </details>''' for f in g['faqs']) + '''
      </div>
    </section>'''

    near = related(g, guides)
    more = ''
    if near:
        more = f'''
  <section class="post-more">
    <div class="wrap">
      <h2 class="post-more__title js-up">More questions answered</h2>
      <div class="post-grid">
{chr(10).join(card(o) for o in near)}
      </div>
    </div>
  </section>
'''

    content = f'''<!-- ============ GUIDE ============ -->
<article class="post guide">
  <header class="post__head">
    {CRYSTAL}
    <div class="wrap post__wrap">
      <nav class="crumbs crumbs--light js-up" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><a href="/guides">Guides</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(g['title'])}</span>
      </nav>
      <p class="post__cat js-up">{html.escape(service_name)}</p>
      <h1 class="js-up">{html.escape(g['title'])}</h1>
      <p class="post__meta js-up">{byline}</p>
    </div>
  </header>
  <div class="wrap post__wrap">
    <section class="answer js-up" aria-labelledby="short-answer">
      <h2 class="answer__label" id="short-answer">The short answer</h2>
      <p class="answer__text">{html.escape(g['answer'])}</p>{facts}
    </section>
    <div class="prose js-up">
{rootify(render(g['body']))}
    </div>{faq_html}
{author_card}
    <aside class="post-cta js-up">
      <div>
        <h2>Want it answered for your own place?</h2>
        <p>A free survey settles it: where the units can go, what size, and a fixed written price within 48 hours.</p>
      </div>
      <div class="post-cta__act">
        <a class="btn btn--primary" href="/contact">Book a free survey</a>
        <a class="post-cta__tel" href="/{page}">See {html.escape(service_name.lower())}</a>
      </div>
    </aside>
    <p class="post__back"><a href="/guides">All guides</a></p>
  </div>
</article>
{more}'''

    # The page answers its own question, so that goes first in the FAQ markup,
    # followed by the questions people ask next.
    qa = [{"@type": "Question", "name": g['title'],
           "acceptedAnswer": {"@type": "Answer", "text": g['answer']}}]
    qa += [{"@type": "Question", "name": f['question'],
            "acceptedAnswer": {"@type": "Answer", "text": f['answer']}} for f in g['faqs']]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g['title'], "description": g['desc'],
         "datePublished": str(g['fm'].get('published') or g['updated'])[:10],
         "dateModified": g['updated'], "author": aschema,
         "publisher": {"@id": f"{BASE}/#business"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": g['url']},
         "about": {"@type": "Service", "name": service_name, "url": f"{BASE}/{page}"},
         "image": f"{BASE}/assets/img/og-image.png", "inLanguage": "en-GB"},
        {"@type": "FAQPage", "mainEntity": qa},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{BASE}/guides"},
            {"@type": "ListItem", "position": 3, "name": g['title'], "item": g['url']}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'

    out = head(g['seo_title'], g['desc'], g['url'], jsonld) + rootify(UTILITY) + rootify(HEADER) \
        + '\n<main id="main">\n\n' + content + '\n</main>\n\n' + rootify(FOOTER)
    open(f"guides/{g['slug']}.html", 'w', encoding='utf-8').write(out)

    words = len(g['answer'].split())
    if len(g['seo_title']) + 9 > 60:
        print(f"    WARNING {g['slug']}: title is {len(g['seo_title']) + 9} chars, over the 60 that fit a search result")
    if not 30 <= words <= 80:
        print(f"    WARNING {g['slug']}: short answer is {words} words, aim for 40 to 60")


def build_hub(guides):
    cards = '\n'.join(card(o) for o in guides)
    body = f'''<!-- ============ HERO ============ -->
<section class="hero hero--inner" id="hero">
  <canvas id="scene" class="hero__canvas" aria-hidden="true"></canvas>
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <nav class="crumbs js-hero" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><span aria-current="page">Guides</span>
      </nav>
      <p class="eyebrow js-hero"><span class="eyebrow__mark"></span>Guides</p>
      <h1 class="js-hero">Air conditioning questions,<br><span class="grad">answered straight</span></h1>
      <p class="lede js-hero">The questions people ask before they get in touch, each answered on its own page: the short answer first, then the detail, the rules and the figures.</p>
    </div>
  </div>
</section>

<!-- ============ GUIDES ============ -->
<section class="section" id="guides">
  <div class="wrap">
    <div class="post-grid">
{cards}
    </div>
  </div>
</section>

'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Air conditioning guides", "url": f"{BASE}/guides",
         "publisher": {"@id": f"{BASE}/#business"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i, "name": o['title'], "url": o['url']}
             for i, o in enumerate(guides, 1)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{BASE}/guides"}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'
    out = head('Air conditioning questions answered',
               'Straight answers to the questions people ask about air conditioning: where it can go, '
               'what it costs, what the rules say, and what it needs to keep working.',
               f'{BASE}/guides', jsonld)
    out = out.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    out += UTILITY + HEADER + '\n<main id="main">\n\n' + body + QUOTE + '\n</main>\n\n' + FOOTER
    open('guides.html', 'w', encoding='utf-8').write(out)


SLOT = re.compile(r'<!-- GUIDES:START -->.*?<!-- GUIDES:END -->', re.S)

def fill_service_pages(guides):
    """Each service page lists the guides that relate to it, above its FAQ."""
    for key, (page, name) in SERVICES.items():
        f = page + '.html'
        s = open(f, encoding='utf-8').read()
        mine = [g for g in guides if g['service'] == key]
        inner = ''
        if mine:
            links = ''.join(f'<li><a href="/guides/{g["slug"]}">{html.escape(g["title"])}</a></li>' for g in mine)
            inner = f'''
<section class="section guides-list" id="guides">
  <div class="wrap">
    <header class="sec-head">
      <p class="eyebrow js-up"><span class="eyebrow__mark"></span>Guides</p>
      <h2 class="js-up">Questions answered in full</h2>
    </header>
    <ul class="nearby js-up">{links}</ul>
  </div>
</section>
'''
        n = SLOT.sub(lambda m: '<!-- GUIDES:START -->' + inner + '<!-- GUIDES:END -->', s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n)


MARKER = '<!-- GUIDES-LINK -->'

def set_footer_link(show):
    """The footer link only exists while there is something to link to."""
    for f in glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('case-studies/*.html') + glob.glob('guides/*.html'):
        s = open(f, encoding='utf-8').read()
        link = f'<li><a href="{"/guides" if "/" in f else "guides"}">Guides</a></li>'
        n = s.replace(link, MARKER) if not show else s.replace(MARKER, link)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n)


if __name__ == '__main__':
    os.makedirs('guides', exist_ok=True)
    guides = sorted((load(p) for p in glob.glob(f'{SRC}/*.md')),
                    key=lambda g: (list(SERVICES).index(g['service']), g['title'].lower()))

    # A guide deleted in the CMS must not leave its page behind.
    live = {f"guides/{g['slug']}.html" for g in guides}
    for stale in set(glob.glob('guides/*.html')) - live:
        os.remove(stale)
        print(f'  removed {stale}, its source is gone')

    for g in guides:
        build_one(g, guides)
    fill_service_pages(guides)
    if guides:
        build_hub(guides)
        set_footer_link(True)
        for g in guides:
            print(f"  guides/{g['slug'] + '.html':52s} {g['service']}")
        print(f"  guides.html  listing {len(guides)} guide{'' if len(guides) == 1 else 's'}")
    else:
        if os.path.exists('guides.html'):
            os.remove('guides.html')
        set_footer_link(False)
        print('  guides: none yet, hub not built and footer link hidden')

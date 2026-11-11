#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep check of how the site hangs together: links, anchors, depth and files.

Run it after adding or moving pages. It reads the built HTML, so run the
build first. Nothing here changes a file; it reports, and exits non zero if
anything is broken (a broken link, anchor or file). Weak linking and depth
are reported as advice.

    python3 tools/audit-site.py            internal checks
    python3 tools/audit-site.py --external also checks every outside link
"""
import glob, html, os, re, sys, urllib.request, urllib.error
from collections import defaultdict, deque

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BASE = re.search(r'rel="canonical" href="(https://[^/]+)', open('index.html').read()).group(1)

PAGES = sorted(f for f in glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('guides/*.html')
               + glob.glob('case-studies/*.html') if not f.startswith('_'))

def url_of(f):
    return '/' if f == 'index.html' else '/' + f[:-5]

def file_of(u):
    u = u.rstrip('/') or '/'
    return 'index.html' if u == '/' else u.lstrip('/') + '.html'

SRC = {f: open(f, encoding='utf-8').read() for f in PAGES}
NOINDEX = {f for f, s in SRC.items() if re.search(r'<meta name="robots" content="[^"]*noindex', s)}
INDEXABLE = [f for f in PAGES if f not in NOINDEX and f != '404.html']
IDS = {f: set(re.findall(r'\bid="([^"]+)"', s)) for f, s in SRC.items()}

def body(s):
    """Page content without the shared header, footer and utility bar."""
    s = re.sub(r'<!-- SHELL:(\w+):START -->.*?<!-- SHELL:\1:END -->', '', s, flags=re.S)
    return re.sub(r'<script.*?</script>', '', s, flags=re.S)

def resolve(href, page):
    """(kind, target, anchor): kind is internal, external or skip."""
    href = html.unescape(href.strip())
    if href.startswith(('tel:', 'mailto:', 'javascript:', 'data:')) or href == '':
        return 'skip', None, None
    if href.startswith(BASE):
        href = href[len(BASE):] or '/'
    if href.startswith(('http://', 'https://', '//')):
        return 'external', href, None
    path, _, anchor = href.partition('#')
    path = path.split('?')[0]
    if path == '':
        return 'internal', '/' + page[:-5] if page != 'index.html' else '/', anchor or None
    if not path.startswith('/'):
        d = os.path.dirname(page)
        path = os.path.normpath(os.path.join('/', d, path))
    return 'internal', path, anchor or None

problems = defaultdict(list)
inbound_body = defaultdict(set)
graph = defaultdict(set)
external = defaultdict(set)
anchor_text = defaultdict(set)

for f in PAGES:
    s = SRC[f]
    b = body(s)
    for m in re.finditer(r'<a\b[^>]*\bhref="([^"]*)"[^>]*>(.*?)</a>', s, re.S):
        href, text = m.group(1), html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        kind, target, anchor = resolve(href, f)
        if kind == 'skip':
            continue
        if kind == 'external':
            external[target].add(f)
            continue
        in_body = m.group(0) in b
        if target.endswith('.html'):
            problems['links to an old .html address'].append(f'{f} -> {href}')
            target = target[:-5]
        # files that are not pages: assets, downloads
        if re.search(r'\.(png|jpe?g|svg|webp|csv|vcf|pdf|xml|txt|json|ico)$', target):
            if not os.path.exists(target.lstrip('/')):
                problems['link to a missing file'].append(f'{f} -> {href}')
            continue
        tf = f if target == f else file_of(target)
        if not os.path.exists(tf):
            problems['broken internal link'].append(f'{f} -> {href}')
            continue
        if anchor and anchor not in IDS.get(tf, set()):
            problems['broken anchor (#section does not exist)'].append(f'{f} -> {href}')
        if tf == f and not anchor and f != 'index.html' and in_body:
            problems['links to itself'].append(f'{f}: "{text[:40]}"')
        if tf in NOINDEX and f not in NOINDEX and tf not in ('thanks.html',):
            problems['indexable page links to a noindex page'].append(f'{f} -> {href}')
        if tf != f:
            graph[f].add(tf)
            if in_body:
                inbound_body[tf].add(f)
                anchor_text[tf].add(text.lower())
        if text.lower() in ('click here', 'here', 'read more', 'more', 'this page', 'link') and in_body:
            problems['vague link text'].append(f'{f}: "{text}" -> {href}')

# images, scripts and stylesheets
for f, s in SRC.items():
    for ref in re.findall(r'(?:src|href)="([^"]+\.(?:png|jpe?g|svg|webp|css|js|woff2|ico))(?:\?[^"]*)?"', s):
        if ref.startswith(('http', '//', 'data:')):
            continue
        p = ref if ref.startswith('/') else '/' + os.path.normpath(os.path.join(os.path.dirname(f), ref))
        if not os.path.exists(p.lstrip('/')):
            problems['missing image, script or stylesheet'].append(f'{f} -> {ref}')
    for tag in re.findall(r'<img\b[^>]*>', s):
        if not re.search(r'\balt="', tag):
            problems['image without alt text'].append(f'{f}: {tag[:80]}')

# canonical, sitemap
sitemap = set(re.findall(r'<loc>([^<]+)</loc>', open('sitemap.xml').read()))
for f in INDEXABLE:
    s = SRC[f]
    c = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    want = BASE + url_of(f)
    if not c:
        problems['missing canonical'].append(f)
    elif c.group(1).rstrip('/') != want.rstrip('/'):
        problems['canonical points elsewhere'].append(f'{f}: {c.group(1)}')
    if want not in sitemap and want.rstrip('/') not in {u.rstrip('/') for u in sitemap}:
        problems['indexable page missing from sitemap'].append(f)
for u in sitemap:
    f = file_of(u[len(BASE):] or '/')
    if not os.path.exists(f):
        problems['sitemap lists a page that does not exist'].append(u)
    elif f in NOINDEX:
        problems['sitemap lists a noindex page'].append(u)

# click depth from the homepage, following every link a crawler would
depth = {'index.html': 0}
q = deque(['index.html'])
while q:
    p = q.popleft()
    for t in graph[p]:
        if t not in depth:
            depth[t] = depth[p] + 1
            q.append(t)
for f in INDEXABLE:
    if f not in depth:
        problems['unreachable from the homepage'].append(f)

# external links
if '--external' in sys.argv:
    for u, where in sorted(external.items()):
        if 'wa.me' in u:
            continue
        try:
            req = urllib.request.Request(u, method='GET', headers={'User-Agent': 'Mozilla/5.0 (CoolIn link check)'})
            code = urllib.request.urlopen(req, timeout=15).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = type(e).__name__
        if code not in (200, 301, 302, 303, 307, 308, 403, 405, 429, 999):
            problems['outside link not working'].append(f'{code}  {u}  (on {", ".join(sorted(where))[:80]})')

# report
broken_kinds = {'broken internal link', 'broken anchor (#section does not exist)', 'link to a missing file',
                'missing image, script or stylesheet', 'sitemap lists a page that does not exist',
                'unreachable from the homepage', 'outside link not working', 'links to an old .html address'}
print(f'  audit-site  {len(PAGES)} pages, {len(INDEXABLE)} indexable, {sum(len(v) for v in graph.values())} internal links')
for kind, items in sorted(problems.items(), key=lambda kv: (kv[0] not in broken_kinds, kv[0])):
    flag = 'BROKEN' if kind in broken_kinds else 'note  '
    print(f'  {flag} {kind}: {len(items)}')
    for i in items[:25]:
        print(f'           {i}')
deep = sorted((d, f) for f, d in depth.items() if f in INDEXABLE and d >= 3)
print(f'  click depth: ' + ', '.join(f'{n} page(s) at {d}' for d, n in sorted({d: sum(1 for x in depth.values() if x == d) for d in set(depth.values())}.items())))
for d, f in deep:
    print(f'           {d} clicks: {url_of(f)}')
weak = sorted((len(inbound_body[f]), url_of(f)) for f in INDEXABLE if f not in ('privacy.html', 'terms.html', 'cookies.html'))
print('  fewest body links in (excluding legal pages):')
for n, u in weak[:8]:
    print(f'           {n:3d}  {u}')
same_text = {f: t for f, t in anchor_text.items() if len(t) == 1 and len(inbound_body[f]) >= 4}
if same_text:
    print('  pages always linked with identical text (vary it a little):')
    for f, t in same_text.items():
        print(f'           {url_of(f)}: "{next(iter(t))}"')
sys.exit(1 if any(k in broken_kinds for k in problems) else 0)

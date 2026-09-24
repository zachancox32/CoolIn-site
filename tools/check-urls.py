#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fails the build if any page states a .html address about itself or its links.

Every page is served at its clean address and the .html form 301s to it, so a
.html link is a redirect hop that leaks into Google's index and splits the
signals for that page. This used to be a thing you had to remember. Now it is
a build step: run last, after everything has been generated, and exit non zero
so the Netlify chain stops rather than deploying the problem.

    python3 tools/check-urls.py
"""
import re, os, sys, glob

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# The only .html addresses allowed to appear anywhere in a page.
#   admin/index.html  the CMS entry point, which is not a site page
ALLOW = ('admin/index.html', '/admin/index.html')

PAGES = sorted(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('case-studies/*.html') + glob.glob('guides/*.html'))

# href/src pointing at a .html address, relative or root relative but not external.
LINK = re.compile(r'(?:href|src)="(?!https?:|//|tel:|mailto:|data:)([^"]*\.html(?:[#?][^"]*)?)"')
# The page's own stated addresses.
SELF = re.compile(r'(?:rel="canonical" href|property="og:url" content)="([^"]*\.html[^"]*)"')
# Anything a crawler reads as a URL inside structured data.
LD   = re.compile(r'"(?:item|url|@id)"\s*:\s*"([^"]*\.html[^"]*)"')

bad = []
for p in PAGES:
    s = open(p, encoding='utf-8').read()
    for label, rx in (('link', LINK), ('canonical/og:url', SELF), ('structured data', LD)):
        for hit in rx.findall(s):
            if hit in ALLOW:
                continue
            bad.append(f'  {p}: {label} -> {hit}')

sm = 'sitemap.xml'
if os.path.exists(sm):
    for loc in re.findall(r'<loc>([^<]*\.html[^<]*)</loc>', open(sm, encoding='utf-8').read()):
        bad.append(f'  {sm}: <loc> -> {loc}')

# The model files are read by answer engines and cited back, so a .html address
# in one of them is the same leak by another route.
for f in ('llms.txt', 'llms-full.txt'):
    if not os.path.exists(f):
        continue
    for u in re.findall(r'(https://[^\s)\]]*\.html[^\s)\]]*)', open(f, encoding='utf-8').read()):
        bad.append(f'  {f}: {u}')

if bad:
    print(f'  check-urls  FAILED, {len(bad)} .html address(es) that should be clean:')
    print('\n'.join(bad))
    sys.exit(1)

print(f'  check-urls  {len(PAGES)} page(s), no .html addresses')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Points the whole site at one domain: canonicals, Open Graph URLs, structured
data, sitemap.xml, robots.txt and llms.txt.

    python3 tools/set-domain.py https://www.coolin.co.uk

Run it the moment a real domain goes live. A canonical tag pointing at a domain
that does not resolve stops Google indexing the site at all.
"""
import sys, re, glob, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if len(sys.argv) < 2:
    sys.exit('usage: set-domain.py https://example.co.uk')
new = sys.argv[1].rstrip('/')
if not new.startswith('http'):
    sys.exit('give the full origin, including https://')

# Any host this site has ever used, with or without www. Kept as one pattern
# so adding a domain later cannot leave half the files pointing at the old one.
pat = re.compile(r'https://(?:www\.)?(?:cool-?in\.co\.uk|cool-in\.netlify\.app)')

changed = 0
for f in glob.glob('*.html') + ['sitemap.xml', 'robots.txt', 'llms.txt', 'llms-full.txt']:
    if not os.path.exists(f):
        continue
    s = open(f).read()
    out = pat.sub(new, s)
    if out != s:
        open(f, 'w').write(out)
        changed += 1
print(f'{changed} files now point at {new}')
print('remember to re-run tools/build-llms-full.py if page content changed')

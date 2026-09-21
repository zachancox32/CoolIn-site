#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copies the shared chrome (utility bar, header, footer) from index.html into
every other page, so a nav or phone number change is made once.

Only the regions between the SHELL markers are touched. Page content is never
read or written. The nav link for the current page is re-marked per file.

    python3 tools/sync-shell.py            check only, changes nothing
    python3 tools/sync-shell.py --write    apply
"""
import re, glob, os, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
WRITE = '--write' in sys.argv

# which nav item is current on which page
CURRENT = {
    'domestic.html': 'domestic.html',
    'commercial.html': 'commercial.html',
    'servicing.html': 'servicing.html',
    'repairs.html': 'servicing.html',
    'heat-pumps.html': 'servicing.html',
    'ventilation.html': 'servicing.html',
    'about.html': 'about.html',
    'contact.html': 'contact',
    'blog.html': 'blog.html',
}

BLOCKS = ['UTILITY', 'HEADER', 'FOOTER']

def grab(src, name):
    m = re.search(r'<!-- SHELL:%s:START -->.*?<!-- SHELL:%s:END -->' % (name, name), src, re.S)
    if not m:
        sys.exit(f'index.html is missing the SHELL:{name} markers')
    return m.group(0)

src = open('index.html').read()
shell = {n: grab(src, n) for n in BLOCKS}

changed, checked = [], 0
for f in sorted(glob.glob('*.html')):
    if f == 'index.html':
        continue
    s = open(f).read()
    if '<!-- SHELL:HEADER:START -->' not in s:
        continue
    checked += 1
    out = s
    for n in BLOCKS:
        block = shell[n]
        if n == 'HEADER':
            # point the logo at the homepage and mark the current nav item
            # point at the canonical homepage URL, not /index.html, which is a
            # duplicate that all internal links used to flow to by mistake
            block = block.replace('<a class="logo" href="#top"', '<a class="logo" href="/"')
            block = re.sub(r' class="is-current" aria-current="page"', '', block)
            cur = CURRENT.get(f)
            if cur:
                block = block.replace(f'<a href="{cur}">',
                                      f'<a href="{cur}" class="is-current" aria-current="page">', 1)
            # pages with no enquiry form send the header CTA to the contact page
            if 'id="quote"' not in s:
                block = block.replace('href="#quote">Free survey', 'href="contact#quote">Free survey')
        out = re.sub(r'<!-- SHELL:%s:START -->.*?<!-- SHELL:%s:END -->' % (n, n),
                     lambda m: block, out, flags=re.S)
    if out != s:
        changed.append(f)
        if WRITE:
            open(f, 'w').write(out)

print(f'checked {checked} pages')
if not changed:
    print('shell is in sync')
elif WRITE:
    print('updated: ' + ', '.join(changed))
else:
    print('out of sync: ' + ', '.join(changed))
    print('run with --write to apply')

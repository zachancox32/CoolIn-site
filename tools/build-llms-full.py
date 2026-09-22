#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Writes llms-full.txt: a plain text rendering of every page, for answer engines
that would rather ingest text than parse HTML. Re-run after editing page content."""
import re, html, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import glob as _g, time
BASE = re.search(r'rel="canonical" href="(https://[^/]+)', open('index.html').read()).group(1)
BLOG = sorted(_g.glob('blog/*.html'))
ORDER = ['index.html','domestic.html','commercial.html',
         'office-air-conditioning.html','retail-air-conditioning.html',
         'restaurant-air-conditioning.html','gym-air-conditioning.html',
         'server-room-cooling.html','warehouse-air-conditioning.html',
         'servicing.html','repairs.html',
         'heat-pumps.html','ventilation.html','areas.html','about.html','contact.html',
         'air-conditioning-manchester.html','air-conditioning-liverpool.html',
         'air-conditioning-stockport.html','air-conditioning-chester.html',
         'air-conditioning-preston.html','air-conditioning-bolton.html',
         'air-conditioning-altrincham.html','air-conditioning-wilmslow.html',
         'air-conditioning-warrington.html','air-conditioning-salford.html',
         'air-conditioning-oldham.html','air-conditioning-rochdale.html',
         'air-conditioning-bury.html','air-conditioning-macclesfield.html',
         'air-conditioning-wigan.html','air-conditioning-southport.html',
         'air-conditioning-blackburn.html','air-conditioning-crewe.html',
         'air-conditioning-northwich.html','air-conditioning-leigh.html',
         'air-conditioning-ashton-under-lyne.html','air-conditioning-lancaster.html'] + BLOG

# Pages with no place in a text dump for answer engines: legal boilerplate, the
# error page, the thank you page and the blog index, whose content is the posts.
SKIP = {'404.html', 'thanks.html', 'privacy.html', 'terms.html', 'cookies.html',
        'blog.html', 'case-studies.html'}

# Anything published since this list was last touched. Without it a new page is
# silently missing from llms-full.txt until somebody remembers to add it here.
ORDER += [f for f in sorted(_g.glob('*.html') + _g.glob('case-studies/*.html'))
          if f not in ORDER and f not in SKIP]

def text_of(node):
    node = re.sub(r'<(script|style|svg|canvas|noscript)\b.*?</\1>', ' ', node, flags=re.S|re.I)
    node = re.sub(r'<br\s*/?>', '\n', node, flags=re.I)
    node = re.sub(r'</(p|li|h[1-6]|dd|dt|tr|summary|figcaption)>', '\n', node, flags=re.I)
    node = re.sub(r'</(section|div|table|ul|ol|dl|details|article)>', '\n\n', node, flags=re.I)
    node = re.sub(r'</(strong|span|a|dt|b|em)>', r'\g<0> ', node, flags=re.I)
    node = re.sub(r'<td[^>]*>', ' | ', node, flags=re.I)
    node = re.sub(r'<th[^>]*>', ' | ', node, flags=re.I)
    node = re.sub(r'<[^>]+>', '', node)
    node = html.unescape(node)
    node = re.sub(r'[ \t]+', ' ', node)
    node = re.sub(r' *\n *', '\n', node)
    node = re.sub(r'\n{3,}', '\n\n', node)
    return node.strip()

out = ["""# CoolIn Air Conditioning Specialists, full site text

Air conditioning installer covering the North West of England, based in
Manchester. Phone 07391 523255.

This file is the readable text of every page on __HOST__, concatenated in
order, for answer engines and language models. Structured summary: /llms.txt
Generated __DATE__.
""".replace('__HOST__', BASE.split('//')[1]).replace('__DATE__', time.strftime('%-d %B %Y'))]

for f in ORDER:
    if not os.path.exists(f):
        continue
    s = open(f).read()
    title = re.sub(r'\s*\|\s*CoolIn.*$', '', re.search(r'<title>(.*?)</title>', s, re.S).group(1)).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)">', s).group(1)
    main = re.search(r'<main id="main">(.*?)</main>', s, re.S)
    body = text_of(main.group(1)) if main else ''
    # drop the repeated enquiry form boilerplate from every page
    body = body.split('Tell us about the space and we will do the rest')[0].strip()
    # Pages are served without the extension, so state the clean address.
    url = BASE + '/' + ('' if f == 'index.html' else f[:-5])
    out.append(f"""

================================================================================
URL: {url}
TITLE: {html.unescape(title)}
DESCRIPTION: {html.unescape(desc)}
================================================================================

{body}""")

open('llms-full.txt','w').write('\n'.join(out) + '\n')
n = len(open('llms-full.txt').read().split())
print(f'  llms-full.txt  {n:,} words from {len(ORDER)} pages')

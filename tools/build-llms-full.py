#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Writes llms-full.txt: a plain text rendering of every page, for answer engines
that would rather ingest text than parse HTML. Re-run after editing page content."""
import re, html, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import glob as _g
BLOG = sorted(_g.glob('blog/*.html'))
ORDER = ['index.html','domestic.html','commercial.html','servicing.html','repairs.html',
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

out = ["""# CoolIn Cooling & Heating, full site text

Air conditioning installer covering the North West of England, based in
Manchester. Phone 07932 607335.

This file is the readable text of every page on coolin.co.uk, concatenated in
order, for answer engines and language models. Structured summary: /llms.txt
Generated 16 September 2026.
"""]

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
    url = 'https://coolin.co.uk/' + ('' if f == 'index.html' else f)
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

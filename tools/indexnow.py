#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keeps the IndexNow key file in place for Bing and the other IndexNow engines.

IndexNow is a push protocol: rather than waiting to be crawled, the site says
"these URLs changed". Bing, Yandex, Seznam and Naver consume it. Google does
not, so this complements Search Console rather than replacing it.

The submission itself happens in netlify/functions/deploy-succeeded.js, which
Netlify runs once a deploy is live. Submitting from the build, as this script
used to, told the engines about pages before they could be fetched, and Bing
refused the key.

This script only makes sure the key file is at the site root, where the
engines check it, and that the key in the function matches. A mismatch fails
the build, because every submission would then be refused without anyone
noticing.

    python3 tools/indexnow.py
"""
import os, re, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

KEY_FILE = 'tools/indexnow-key.txt'
FUNCTION = 'netlify/functions/deploy-succeeded.js'

key = open(KEY_FILE).read().strip()
if not re.fullmatch(r'[0-9a-f]{8,128}', key):
    sys.exit('  indexnow: the key is not 8 to 128 hex characters')

m = re.search(r"const KEY = '([0-9a-f]+)'", open(FUNCTION).read())
if not m or m.group(1) != key:
    sys.exit(f'  indexnow: the key in {FUNCTION} does not match {KEY_FILE}')

# the key has to be fetchable at the root for submissions to be trusted
with open(f'{key}.txt', 'w') as f:
    f.write(key)
for stale in (f for f in os.listdir('.') if re.fullmatch(r'[0-9a-f]{32}\.txt', f) and f != f'{key}.txt'):
    os.remove(stale)
    print(f'  indexnow: removed old key file {stale}')
print('  indexnow: key file in place, submission runs after the deploy goes live')

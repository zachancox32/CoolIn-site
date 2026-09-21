#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tells Bing and the other IndexNow engines which pages exist, on every deploy.

IndexNow is a push protocol: rather than waiting to be crawled, the site says
"these URLs changed". Bing, Yandex, Seznam and Naver consume it. Google does
not, so this complements Search Console rather than replacing it.

It needs no account. The only requirement is that a key file is reachable at
the site root, which is why the key is committed: it is public by design and
proves the submitter controls the domain.

Only runs on a production deploy, and never fails the build. A search engine
being unreachable is not a reason to stop shipping a website.

    python3 tools/indexnow.py
"""
import json, os, re, sys, urllib.error, urllib.request

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

KEY_FILE = 'tools/indexnow-key.txt'
ENDPOINT = 'https://api.indexnow.org/indexnow'

def main():
    if not os.path.exists('sitemap.xml'):
        print('  indexnow: no sitemap, skipped'); return
    if not os.path.exists(KEY_FILE):
        print(f'  indexnow: no key at {KEY_FILE}, skipped'); return

    key = open(KEY_FILE).read().strip()
    if not re.fullmatch(r'[0-9a-f]{8,128}', key):
        print('  indexnow: key is not 8 to 128 hex characters, skipped'); return

    urls = re.findall(r'<loc>([^<]+)</loc>', open('sitemap.xml', encoding='utf-8').read())
    if not urls:
        print('  indexnow: sitemap has no urls, skipped'); return
    host = re.match(r'https?://([^/]+)', urls[0]).group(1)

    # the key has to be fetchable at the root for the submission to be trusted
    with open(f'{key}.txt', 'w') as f:
        f.write(key)

    context = os.environ.get('CONTEXT', 'local')
    if context != 'production':
        print(f'  indexnow: key file written, submission skipped on "{context}"'); return

    body = json.dumps({
        'host': host,
        'key': key,
        'keyLocation': f'https://{host}/{key}.txt',
        'urlList': urls[:10000],
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=body,
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f'  indexnow: submitted {len(urls)} urls, {r.status}')
    except urllib.error.HTTPError as e:
        print(f'  indexnow: {e.code} from the endpoint, continuing')
    except Exception as e:
        print(f'  indexnow: {type(e).__name__}, continuing')

try:
    main()
except Exception as e:
    print(f'  indexnow: {type(e).__name__}, continuing')
sys.exit(0)

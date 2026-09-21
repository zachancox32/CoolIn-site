#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stamps the asset query strings with a hash of the file contents.

Netlify serves /assets/* with Cache-Control: immutable, so a browser that has
style.css?v=22 will never ask for it again. Hand-numbering that version means
one forgotten bump ships a stylesheet nobody receives.

This derives the version from the bytes instead, so it changes exactly when
the file changes and never when it does not.

    python3 tools/bust-cache.py
"""
import glob, hashlib, io, os, re

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

ASSETS = {
    'assets/css/style.css': r'(assets/css/style\.css\?v=)([A-Za-z0-9]+)',
    'assets/js/main.js':    r'(assets/js/main\.js\?v=)([A-Za-z0-9]+)',
    'assets/js/scene.js':   r'(assets/js/scene\.js\?v=)([A-Za-z0-9]+)',
}

stamps = {}
for path, pattern in ASSETS.items():
    if os.path.exists(path):
        stamps[pattern] = hashlib.sha1(open(path, 'rb').read()).hexdigest()[:8]

changed = 0
for f in glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('case-studies/*.html'):
    s = io.open(f, encoding='utf-8').read()
    out = s
    for pattern, stamp in stamps.items():
        out = re.sub(pattern, lambda m: m.group(1) + stamp, out)
    if out != s:
        io.open(f, 'w', encoding='utf-8').write(out)
        changed += 1

for path, pattern in ASSETS.items():
    if pattern in stamps:
        print(f'  {os.path.basename(path):12s} -> v={stamps[pattern]}')
print(f'  stamped {changed} page(s)')

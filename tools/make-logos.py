#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepares the brand logo files for the web.

The brand pack ships 1200px and 4000px rasters of every lockup, already
rendered from the vector with real Archivo, so nothing here needs a font or a
renderer. This just box-filters them down and keeps the alpha channel, which
matters: the transparent lockups sit on the translucent header and on the
footer navy without carrying a background of their own.

Source PNGs live in the zip the brand pack came in; the 4000px masters are
kept in assets/img/brand/print. Standard library only.

    python3 tools/make-logos.py
"""
import io, os, struct, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _png import read_png, write_png, resize

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SRC = 'assets/img/brand/print'
BRAND = 'assets/img/brand'
FONT = 'assets/fonts/archivo-latin.woff2'

# svg name -> output, and whether to drop the ground rect so it sits on any colour
SVG_JOBS = [
    ('coolin-logo-18b-primary.svg', 'assets/img/logo.svg',         False),
    ('coolin-logo-18b-reverse.svg', 'assets/img/logo-reverse.svg', True),
]
PNG_JOBS = [
    ('coolin-logo-18b-primary-4000w.png', 'assets/img/logo-email.png', 520),
    # Google picks one favicon and wants a square that is a multiple of 48
    ('coolin-icon-14a-4000w.png',         'assets/img/favicon.png',    192),
]
# Straight copies, no font to embed. The favicon SVG has to be the vector of
# the same mark the PNG is rasterised from, or browsers show one icon and
# Google shows another. It used to be coolin-favicon.svg, which is a simplified
# version without the pill, so the two did not match.
COPY_JOBS = [
    ('coolin-icon-14a.svg', 'assets/img/favicon.svg'),
]

def build_svgs():
    import base64, re
    font = base64.b64encode(open(FONT, 'rb').read()).decode()
    face = ("<style>@font-face{font-family:'Archivo';"
            f"src:url(data:font/woff2;base64,{font}) format('woff2');"
            "font-weight:100 900;font-style:normal}</style>")
    for name, out, drop_ground in SVG_JOBS:
        art = io.open(os.path.join(BRAND, name), encoding='utf-8').read()
        if drop_ground:
            art = re.sub(r'<rect width="320" height="140"[^>]*></rect>\s*', '', art)
        i = art.index('>') + 1
        io.open(out, 'w', encoding='utf-8').write(art[:i] + face + art[i:])
        print(f'  {out:34s} {os.path.getsize(out)//1024}kb  vector, font embedded')

build_svgs()

for name, out in COPY_JOBS:
    art = io.open(os.path.join(BRAND, name), encoding='utf-8').read()
    io.open(out, 'w', encoding='utf-8').write(art)
    print(f'  {out:34s} {os.path.getsize(out)}b  vector, copied as is')

for name, out, width in PNG_JOBS:
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        sys.exit(f'missing master: {path}')
    w, h, rows, ch = read_png(path)
    ow, oh, orows = resize(w, h, rows, ch, width)
    size = write_png(out, ow, oh, orows, ch)
    print(f'  {out:34s} {ow}x{oh}  {size//1024}kb  {"transparent" if ch == 4 else "opaque"}')

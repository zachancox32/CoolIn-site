#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Writes /favicon.ico at the site root from assets/img/favicon.png.

The <link> tags in the page head are what Google reads first, but /favicon.ico
is its documented fallback, and it is the address browsers, Bing, Slack and
most directory sites request directly without reading any HTML. Ours returned
404, so every one of those fell back to a generic icon.

The container holds 16, 32 and 48 pixel versions, each stored as PNG, which
every browser and crawler that matters has read since Windows Vista. 48 is in
there because Google wants a size that is a multiple of 48.

Run after changing the logo, then commit the result:

    python3 tools/make-favicon-ico.py
"""
import os, sys, struct, zlib

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, 'tools')
from _png import read_png, resize

SRC, OUT, SIZES = 'assets/img/favicon.png', 'favicon.ico', (16, 32, 48)


def png_bytes(w, h, rows, ch):
    """write_png without the file, because an ICO carries the PNG inline."""
    raw = bytearray()
    for r in rows:
        raw.append(0)
        raw += r

    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6 if ch == 4 else 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))


w, h, rows, ch = read_png(SRC)
assert w == h, f'{SRC} is {w}x{h}, and a favicon has to be square'

images = []
for s in SIZES:
    if s == w:
        images.append((s, png_bytes(w, h, rows, ch)))
    else:
        ow, oh, orows = resize(w, h, rows, ch, s)
        images.append((s, png_bytes(ow, oh, orows, ch)))

# ICONDIR, then one ICONDIRENTRY each, then the image data they point at.
offset = 6 + 16 * len(images)
blob = struct.pack('<HHH', 0, 1, len(images))
entries, data = b'', b''
for s, png in images:
    entries += struct.pack('<BBBBHHII', s, s, 0, 0, 1, 32, len(png), offset)
    data += png
    offset += len(png)

out = blob + entries + data
open(OUT, 'wb').write(out)
print(f'  {OUT}  {", ".join(f"{s}x{s}" for s, _ in images)}, {len(out):,} bytes')

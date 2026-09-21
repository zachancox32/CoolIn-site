#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resizes the brand PNGs down to the sizes the site actually uses.

The brand pack ships 1200px and 4000px rasters of every lockup, already
rendered from the vector with real Archivo, so nothing here needs a font or a
renderer. This just box-filters them down and keeps the alpha channel, which
matters: the transparent lockups sit on the translucent header and on the
footer navy without carrying a background of their own.

Source PNGs live in the zip the brand pack came in; the 4000px masters are
kept in assets/img/brand/print. Standard library only.

    python3 tools/make-logos.py
"""
import os, struct, sys, zlib

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SRC = 'assets/img/brand/print'
JOBS = [
    ('coolin-logo-18b-primary-4000w.png', 'assets/img/logo.png',         440),
    ('coolin-logo-18b-reverse-4000w.png', 'assets/img/logo-reverse.png', 440),
    ('coolin-logo-18b-primary-4000w.png', 'assets/img/logo-email.png',   520),
]

def read_png(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', 'not a png'
    i, idat = 8, b''
    while i < len(d):
        ln = struct.unpack('>I', d[i:i+4])[0]
        tag = d[i+4:i+8]
        body = d[i+8:i+8+ln]
        if tag == b'IHDR':
            w, h, depth, ctype, _, _, interlace = struct.unpack('>IIBBBBB', body)
            assert depth == 8 and ctype in (2, 6) and interlace == 0, 'unsupported png'
        elif tag == b'IDAT':
            idat += body
        elif tag == b'IEND':
            break
        i += 12 + ln
    ch = 3 if ctype == 2 else 4
    raw = zlib.decompress(idat)
    stride = w * ch
    rows, prev, p = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p+stride]); p += stride
        for x in range(stride):
            a = line[x-ch] if x >= ch else 0
            b = prev[x]
            c = prev[x-ch] if x >= ch else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        rows.append(line); prev = line
    return w, h, rows, ch

def write_png(path, w, h, rows, ch):
    raw = bytearray()
    for r in rows:
        raw.append(0); raw += r
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    ctype = 6 if ch == 4 else 2
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, ctype, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(png)
    return len(png)

def resize(w, h, rows, ch, out_w):
    """Box filter, premultiplying alpha so edges do not pick up a dark fringe."""
    out_h = max(1, round(h * out_w / w))
    xs = [(x * w // out_w, max(x * w // out_w + 1, (x + 1) * w // out_w)) for x in range(out_w)]
    ys = [(y * h // out_h, max(y * h // out_h + 1, (y + 1) * h // out_h)) for y in range(out_h)]
    out = []
    for y0, y1 in ys:
        line = bytearray()
        for x0, x1 in xs:
            acc = [0, 0, 0, 0]; n = 0
            for yy in range(y0, y1):
                r = rows[yy]
                for xx in range(x0, x1):
                    i = xx * ch
                    a = r[i+3] if ch == 4 else 255
                    acc[0] += r[i] * a; acc[1] += r[i+1] * a; acc[2] += r[i+2] * a
                    acc[3] += a; n += 1
            if ch == 4:
                a = acc[3] // n
                if a == 0:
                    line += bytes((0, 0, 0, 0))
                else:
                    line += bytes((min(255, acc[0] // acc[3]), min(255, acc[1] // acc[3]),
                                   min(255, acc[2] // acc[3]), a))
            else:
                line += bytes((acc[0] // (n * 255), acc[1] // (n * 255), acc[2] // (n * 255)))
        out.append(line)
    return out_w, out_h, out

for name, out, width in JOBS:
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        sys.exit(f'missing master: {path}')
    w, h, rows, ch = read_png(path)
    ow, oh, orows = resize(w, h, rows, ch, width)
    size = write_png(out, ow, oh, orows, ch)
    print(f'  {out:34s} {ow}x{oh}  {size//1024}kb  {"transparent" if ch == 4 else "opaque"}')

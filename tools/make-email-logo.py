#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renders assets/img/logo-email.png from the real site logo.

The logo only exists as code: HTML text in Archivo plus two inline SVGs. Email
clients strip SVG and cannot load a self hosted webfont, so it has to become a
raster image.

This rebuilds the logo as one standalone SVG with the Archivo woff2 embedded,
hands it to Quick Look (WebKit) to rasterise, then crops to the artwork and
writes the PNG. Same engine the site renders in, so the letterforms are exact.

macOS only, because it uses qlmanage. It is a local tool, not part of the
Netlify build: the PNG it produces is committed as an asset.

    python3 tools/make-email-logo.py
"""
import base64, io, os, struct, subprocess, sys, tempfile, zlib

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = 'assets/img/logo-email.png'
SCALE = 704                 # render size; the logo is cropped out of this
PAD = 6                     # white margin left around the artwork, in px


def build_svg():
    """The real brand lockup, with Archivo embedded so WebKit can set the type.

    assets/img/brand/coolin-logo-primary.svg references Archivo by name, which
    only works on a machine with the font installed. Embedding the site's own
    woff2 makes the render match the site exactly.
    """
    font = base64.b64encode(open('assets/fonts/archivo-latin.woff2', 'rb').read()).decode()
    art = io.open('assets/img/brand/coolin-logo-primary.svg', encoding='utf-8').read()
    face = ("<style>@font-face{font-family:'Archivo';"
            f"src:url(data:font/woff2;base64,{font}) format('woff2');"
            "font-weight:100 900;font-style:normal}</style>"
            '<rect width="280" height="104" fill="#ffffff"/>')
    # drop it in right after the opening tag, behind the artwork
    i = art.index('>') + 1
    return art[:i] + face + art[i:]

def read_png(path):
    """Minimal PNG reader: 8 bit RGB or RGBA, no interlace. Returns (w, h, rows)."""
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', 'not a png'
    i, idat, w = 8, b'', None
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

def write_png(path, w, h, rows):
    raw = bytearray()
    for r in rows:
        raw.append(0); raw += r
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(png)
    return len(png)

tmp = tempfile.mkdtemp()
svg_path = os.path.join(tmp, 'logo.svg')
io.open(svg_path, 'w', encoding='utf-8').write(build_svg())
subprocess.run(['qlmanage', '-t', '-s', str(SCALE), '-o', tmp, svg_path],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
shot = os.path.join(tmp, 'logo.svg.png')
if not os.path.exists(shot):
    sys.exit('qlmanage produced nothing. This tool needs macOS.')

w, h, rows, ch = read_png(shot)

# crop to the artwork: anything that is not near white
x0, y0, x1, y1 = w, h, 0, 0
for y in range(h):
    r = rows[y]
    for x in range(w):
        i = x * ch
        if r[i] < 245 or r[i+1] < 245 or r[i+2] < 245:
            if x < x0: x0 = x
            if x > x1: x1 = x
            if y < y0: y0 = y
            if y > y1: y1 = y
if x1 <= x0:
    sys.exit('nothing drawn, the font or Quick Look failed')

x0 = max(0, x0 - PAD); y0 = max(0, y0 - PAD)
x1 = min(w - 1, x1 + PAD); y1 = min(h - 1, y1 + PAD)
cw, chh = x1 - x0 + 1, y1 - y0 + 1

out_rows = []
for y in range(y0, y1 + 1):
    src, line = rows[y], bytearray()
    for x in range(x0, x1 + 1):
        i = x * ch
        line += src[i:i+3]
    out_rows.append(line)

size = write_png(OUT, cw, chh, out_rows)
print(f'  {OUT}  {cw}x{chh}  {size//1024}kb  (shows at {cw//4}px wide)')

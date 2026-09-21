#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renders the logo PNGs from the real brand SVGs.

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
SCALE = 704                 # render size; the logo is cropped out of this



# what to render: brand svg -> output png, at this pixel width
# brand svg -> output png, pixel width, and an optional ground override.
# The reverse lockup ships on #0D2B38 but the site footer is #08222F, so it is
# re-grounded to match exactly. Without that the logo reads as a lighter box.
JOBS = [
    ('coolin-logo-primary.svg', 'assets/img/logo.png',         560, None),
    ('coolin-logo-reverse.svg', 'assets/img/logo-reverse.png', 560, '#08222F'),
    ('coolin-logo-primary.svg', 'assets/img/logo-email.png',   640, None),
]

def build_svg(name, ground=None):
    """The real brand lockup with Archivo embedded, so WebKit sets the type.

    The brand SVGs name Archivo rather than outlining it, which only works on
    a machine with the font. Embedding the site's own woff2 makes the render
    match the artwork exactly.
    """
    font = base64.b64encode(open('assets/fonts/archivo-latin.woff2', 'rb').read()).decode()
    art = io.open(f'assets/img/brand/{name}', encoding='utf-8').read()
    face = ("<style>@font-face{font-family:'Archivo';"
            f"src:url(data:font/woff2;base64,{font}) format('woff2');"
            "font-weight:100 900;font-style:normal}</style>")
    if ground:
        art = art.replace('<rect width="280" height="104" fill="#0D2B38">',
                          f'<rect width="280" height="104" fill="{ground}">')
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


for art_name, out, width, ground in JOBS:
    tmp = tempfile.mkdtemp()
    svg_path = os.path.join(tmp, 'logo.svg')
    io.open(svg_path, 'w', encoding='utf-8').write(build_svg(art_name, ground))
    subprocess.run(['qlmanage', '-t', '-s', str(width * 2), '-o', tmp, svg_path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shot = os.path.join(tmp, 'logo.svg.png')
    if not os.path.exists(shot):
        sys.exit('qlmanage produced nothing. This tool needs macOS.')

    w, h, rows, ch = read_png(shot)

    def px(x, y):
        i = (x * ch)
        return rows[y][i], rows[y][i+1], rows[y][i+2]

    def near(a, b, tol=10):
        return all(abs(a[k] - b[k]) <= tol for k in range(3))

    canvas = px(w - 1, h - 1)          # bottom right is always outside the artwork
    art = io.open(f'assets/img/brand/{art_name}', encoding='utf-8').read()
    has_ground = '<rect width="280" height="104"' in art

    if has_ground:
        # the lockup paints its own ground, so its edge is where the canvas ends
        target, tol, pad = canvas, 10, 0
        hit = lambda c: not near(c, target, tol)
    else:
        # transparent lockup: bound the ink, then leave a little breathing room
        target, tol, pad = canvas, 10, 10
        hit = lambda c: not near(c, target, tol)

    x0, y0, x1, y1 = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            if hit(px(x, y)):
                x0 = min(x0, x); x1 = max(x1, x)
                y0 = min(y0, y); y1 = max(y1, y)
    if x1 <= x0:
        sys.exit(f'nothing drawn for {art_name}')
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(w - 1, x1 + pad); y1 = min(h - 1, y1 + pad)

    out_rows = []
    for y in range(y0, y1 + 1):
        s_, line = rows[y], bytearray()
        for x in range(x0, x1 + 1):
            i = x * ch
            line += s_[i:i+3]
        out_rows.append(line)
    size = write_png(out, x1-x0+1, y1-y0+1, out_rows)
    print(f'  {out:34s} {x1-x0+1}x{y1-y0+1}  {size//1024}kb')

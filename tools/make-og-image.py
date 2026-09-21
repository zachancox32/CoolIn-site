#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws assets/img/og-image.png, the 1200x630 card shown when the site is
shared on social, in chat apps and in some AI answer panels.

Pure standard library: raw pixels plus zlib into a PNG. No design tools needed,
so the card can be regenerated whenever the brand colours change.
"""
import zlib, struct, math, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

W, H = 1200, 630
NAVY  = (0x0D, 0x2B, 0x38)
ICE   = (0x5E, 0xC3, 0xE0)
ORANGE= (0xE2, 0x67, 0x3B)
WHITE = (0xFF, 0xFF, 0xFF)
GREY  = (0x9E, 0xBD, 0xCA)

buf = bytearray()
for _ in range(W * H):
    buf += bytes(NAVY)

def px(x, y, c, a=1.0):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        if a >= 1.0:
            buf[i:i+3] = bytes(c)
        else:
            for k in range(3):
                buf[i+k] = int(buf[i+k] * (1 - a) + c[k] * a)

def disc(cx, cy, r, c, a=1.0):
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                px(x, y, c, a)

# soft glow top right, echoing the hero
for y in range(0, 420):
    for x in range(700, W):
        d = math.hypot(x - 1150, y - 40)
        if d < 430:
            px(x, y, ICE, 0.10 * (1 - d / 430))

# 5x7 block font, only the glyphs this card needs
F = {
 'A':('01110','10001','10001','11111','10001','10001','10001'),
 'C':('01110','10001','10000','10000','10000','10001','01110'),
 'D':('11110','10001','10001','10001','10001','10001','11110'),
 'E':('11111','10000','10000','11110','10000','10000','11111'),
 'G':('01110','10001','10000','10111','10001','10001','01111'),
 'H':('10001','10001','10001','11111','10001','10001','10001'),
 'I':('11111','00100','00100','00100','00100','00100','11111'),
 'L':('10000','10000','10000','10000','10000','10000','11111'),
 'N':('10001','11001','10101','10011','10001','10001','10001'),
 'O':('01110','10001','10001','10001','10001','10001','01110'),
 'R':('11110','10001','10001','11110','10100','10010','10001'),
 'S':('01111','10000','10000','01110','00001','00001','11110'),
 'T':('11111','00100','00100','00100','00100','00100','00100'),
 'W':('10001','10001','10001','10101','10101','11011','10001'),
 ' ':('00000','00000','00000','00000','00000','00000','00000'),
}

def text(s, x, y, scale, colour, gap=1):
    cx = x
    for ch in s:
        g = F.get(ch)
        if g is None:
            cx += (5 + gap) * scale; continue
        for ry, row in enumerate(g):
            for rx, bit in enumerate(row):
                if bit == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            px(cx + rx * scale + dx, y + ry * scale + dy, colour)
        cx += (5 + gap) * scale
    return cx

def width_of(s, scale, gap=1):
    return len(s) * (5 + gap) * scale

# wordmark: COOL in white, IN in ice
S = 20
x = 96
x = text('COOL', x, 150, S, WHITE)
x = text('IN', x, 150, S, ICE)

# snowflake mark, six spokes
sx, sy, r = x + 72, 150 + 22, 22
for k in range(6):
    a = math.radians(k * 60)
    for t in range(r):
        px(int(sx + math.cos(a) * t), int(sy + math.sin(a) * t), ICE)
        px(int(sx + math.cos(a) * t) + 1, int(sy + math.sin(a) * t), ICE)
    for s2 in (-1, 1):
        b = a + math.radians(40 * s2)
        for t in range(9):
            bx, by = sx + math.cos(a) * (r - 9), sy + math.sin(a) * (r - 9)
            px(int(bx + math.cos(b) * t), int(by + math.sin(b) * t), ICE)

# the two waves from the logo
for wave, (col, off) in enumerate([(ICE, 0), (ORANGE, 46)]):
    for x in range(96, 1104):
        y = 330 + off + math.sin((x - 96) / 118.0) * 26
        for t in range(9):
            px(x, int(y) + t, col)

# strapline
text('AIR CONDITIONING', 96, 470, 6, GREY)
text('NORTH WEST', 96, 530, 6, ICE)

# orange rule bottom right
for x in range(W - 300, W - 96):
    for t in range(6):
        px(x, 560 + t, ORANGE)

raw = bytearray()
for y in range(H):
    raw.append(0)
    raw += buf[y * W * 3:(y + 1) * W * 3]

def chunk(tag, data):
    c = struct.pack('>I', len(data)) + tag + data
    return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
       + chunk(b'IEND', b''))

open('assets/img/og-image.png', 'wb').write(png)
print(f'  assets/img/og-image.png  {W}x{H}  {len(png)//1024}kb')

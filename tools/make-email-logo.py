#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws assets/img/logo-email.png, the snowflake mark used in emails.

The site logo is inline SVG, which Gmail and Outlook strip, so email needs a
raster copy. Only the mark is drawn here: the wordmark is set as real HTML
text in the email, which stays crisp at any size and still shows when a
client blocks images.

Same approach as make-og-image.py: raw pixels plus zlib, no design tools and
no dependency to install. Drawn at 4x and averaged down for smooth edges.
"""
import zlib, struct, math, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SS = 4                      # supersample factor
W, H = 96, 96               # final size, shown at 48px for retina
BW, BH = W * SS, H * SS

NAVY   = (0x0C, 0x2A, 0x39)
BLUE   = (0x1A, 0x7C, 0xA4)
ICE    = (0x5C, 0xB8, 0xDC)
ORANGE = (0xE4, 0x63, 0x2C)
GREY   = (0x6E, 0x85, 0x92)
WHITE  = (0xFF, 0xFF, 0xFF)

buf = bytearray()
for _ in range(BW * BH):
    buf += bytes(WHITE)

def px(x, y, c):
    x, y = int(x), int(y)
    if 0 <= x < BW and 0 <= y < BH:
        i = (y * BW + x) * 3
        buf[i:i+3] = bytes(c)

def stroke(x, y, c, w):
    """A round dot of width w, so lines have thickness without gaps."""
    r = w / 2.0
    for dy in range(int(-r) - 1, int(r) + 2):
        for dx in range(int(-r) - 1, int(r) + 2):
            if dx * dx + dy * dy <= r * r:
                px(x + dx, y + dy, c)

# ---- snowflake, six spokes with barbs, centred ----
sx = sy = (W * SS) / 2.0
r = 40 * SS
for k in range(6):
    a = math.radians(k * 60)
    for t in range(r):
        stroke(sx + math.cos(a) * t, sy + math.sin(a) * t, BLUE, 2.6 * SS)
    for s2 in (-1, 1):
        b = a + math.radians(42 * s2)
        bx, by = sx + math.cos(a) * (r - 15 * SS), sy + math.sin(a) * (r - 15 * SS)
        for t in range(15 * SS):
            stroke(bx + math.cos(b) * t, by + math.sin(b) * t, BLUE, 2.2 * SS)

# ---- average the supersampled buffer down ----
out = bytearray()
for y in range(H):
    out.append(0)
    for x in range(W):
        r_ = g_ = b_ = 0
        for dy in range(SS):
            for dx in range(SS):
                i = ((y * SS + dy) * BW + (x * SS + dx)) * 3
                r_ += buf[i]; g_ += buf[i+1]; b_ += buf[i+2]
        n = SS * SS
        out += bytes((r_ // n, g_ // n, b_ // n))

def chunk(tag, data):
    c = struct.pack('>I', len(data)) + tag + data
    return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(bytes(out), 9))
       + chunk(b'IEND', b''))
open('assets/img/logo-email.png', 'wb').write(png)
print(f'  assets/img/logo-email.png  {W}x{H}  {len(png)//1024}kb')

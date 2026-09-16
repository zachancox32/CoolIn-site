# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _towngen import build
import _towns_data, _towns_data2

ALL = _towns_data.TOWNS + _towns_data2.TOWNS

# the six that already exist, so neighbours can point at them too
EXISTING = [('Manchester','air-conditioning-manchester.html'),
            ('Liverpool','air-conditioning-liverpool.html'),
            ('Stockport','air-conditioning-stockport.html'),
            ('Chester','air-conditioning-chester.html'),
            ('Preston','air-conditioning-preston.html'),
            ('Bolton','air-conditioning-bolton.html')]

# geographic neighbours, so the cross links are useful rather than arbitrary
NEAR = {
 'Altrincham': ['Wilmslow','Manchester','Warrington','Stockport','Salford'],
 'Wilmslow':   ['Altrincham','Macclesfield','Stockport','Manchester','Northwich'],
 'Warrington': ['Altrincham','Wigan','Liverpool','Northwich','Leigh'],
 'Salford':    ['Manchester','Bolton','Bury','Altrincham','Wigan'],
 'Oldham':     ['Rochdale','Ashton under Lyne','Bury','Manchester','Stockport'],
 'Rochdale':   ['Oldham','Bury','Bolton','Manchester','Ashton under Lyne'],
 'Bury':       ['Bolton','Rochdale','Salford','Oldham','Manchester'],
 'Macclesfield':['Wilmslow','Stockport','Northwich','Crewe','Manchester'],
 'Wigan':      ['Leigh','Bolton','Warrington','Salford','Southport'],
 'Southport':  ['Liverpool','Preston','Wigan','Blackburn','Warrington'],
 'Blackburn':  ['Preston','Bolton','Bury','Rochdale','Lancaster'],
 'Crewe':      ['Northwich','Macclesfield','Chester','Wilmslow','Warrington'],
 'Northwich':  ['Warrington','Chester','Wilmslow','Crewe','Macclesfield'],
 'Leigh':      ['Wigan','Bolton','Salford','Warrington','Manchester'],
 'Ashton under Lyne':['Oldham','Stockport','Manchester','Rochdale','Bury'],
 'Lancaster':  ['Preston','Blackburn','Southport','Bolton','Liverpool'],
}

LOOKUP = dict(EXISTING)
for t in ALL:
    LOOKUP[t['town']] = t['slug'] + '.html'

total = 0
for t in ALL:
    names = NEAR[t['town']]
    nb = [(n, LOOKUP[n]) for n in names if n in LOOKUP]
    slug, words = build(t, nb)
    total += words
    print(f"  {slug:42s} {words:4d} words")
print(f"\n  {len(ALL)} pages, {total:,} words of town specific content")

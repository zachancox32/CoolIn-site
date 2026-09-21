#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The domestic system diagrams, as data rather than markup.

Kept here so the geometry lives in one place: the cards in domestic.html are
generated from it, and a change to a pipe run is a change to one line.

The four domestic system diagrams. One shared visual language: same house
shell, same unit shapes, only the arrangement changes, so the cards read as a
set rather than four unrelated drawings."""

SHELL = ('<path class="d-ground" d="M4 128h232"/>'
         '<path class="d-shell" d="M90 14 20 54v74h140V54z"/>'
         '<path class="d-floor" d="M20 90h140"/>')

def air(paths):
    return ''.join(f'<path class="d-air" d="{p}"/>' for p in paths)

def pipe(*runs):
    """Solid run plus a dashed overlay that travels it, so the circuit reads as
    connected rather than merely drawn. Paths are authored indoor to outdoor,
    which is the direction the dashes move."""
    return (''.join(f'<path class="d-pipe" d="{d}"/>' for d in runs)
            + ''.join(f'<path class="d-flow" d="{d}"/>' for d in runs))

def fan(x, y, n=3, spread=8):
    """A fan of airflow arcs leaving an indoor unit, long enough that the dashes
    visibly travel rather than sitting as stubs."""
    return air([f'M{x + i*spread} {y}q9 15 -2 27' for i in range(n)])

IN_UNIT  = '<rect class="d-unit" x="{x}" y="{y}" width="26" height="9" rx="3"/>'
GRILLE   = '<rect class="d-grille" x="{x}" y="{y}" width="20" height="4" rx="2"/>'
OUT_UNIT = ('<g class="d-out"><rect x="{x}" y="{y}" width="34" height="26" rx="4"/>'
            '<circle cx="{cx}" cy="{cy}" r="7"/><circle class="d-hub" cx="{cx}" cy="{cy}" r="1.8"/></g>')
CONDENSER = OUT_UNIT.format(x=180, y=98, cx=197, cy=111)

DIAGRAMS = {
 'wall': dict(
   caption='One indoor unit, one outdoor unit, surface trunking',
   body = SHELL
     + '<rect class="d-room" x="32" y="60" width="52" height="26" rx="2"/>'
     + IN_UNIT.format(x=38, y=64)
     + pipe('M64 69h76v42h40')
     + CONDENSER
     + fan(42, 76)),

 'multi': dict(
   caption='Two to five indoor units sharing one outdoor unit',
   body = SHELL
     + '<rect class="d-room" x="32" y="60" width="44" height="26" rx="2"/>'
     + '<rect class="d-room" x="88" y="60" width="44" height="26" rx="2"/>'
     + IN_UNIT.format(x=36, y=64) + IN_UNIT.format(x=92, y=64)
     + IN_UNIT.format(x=36, y=100)
     + pipe('M62 69h80M118 69h24v42M62 105h80', 'M142 111h38')
     + CONDENSER
     + fan(40, 76, n=2) + fan(96, 76, n=2) + fan(40, 112, n=2)),

 'ducted': dict(
   caption='Unit in the loft, ducted down to grilles in each room',
   body = SHELL
     + '<path class="d-void" d="M20 54h140v13H20z"/>'
     + '<rect class="d-unit" x="74" y="56" width="30" height="9" rx="3"/>'
     + pipe('M74 60H44v7M104 60h32v7', 'M136 60h14v51h30')
     + GRILLE.format(x=34, y=67) + GRILLE.format(x=126, y=67)
     + CONDENSER
     + fan(38, 72, n=2, spread=7) + fan(130, 72, n=2, spread=7)),

 'console': dict(
   caption='Low level unit downstairs, sits where a radiator would',
   body = SHELL
     + '<rect class="d-room" x="34" y="96" width="46" height="20" rx="2"/>'
     + '<rect class="d-unit" x="38" y="114" width="32" height="11" rx="3"/>'
     + pipe('M70 119h72v-8h38')
     + CONDENSER
     + air(['M44 112q3-16 16-21', 'M52 112q3-16 16-21', 'M60 112q3-16 16-21'])),
}

def svg(key):
    d = DIAGRAMS[key]
    return (f'<figure class="sys__dia">'
            f'<svg viewBox="0 0 240 136" role="img" aria-label="{d["caption"]}">{d["body"]}</svg>'
            f'<figcaption>{d["caption"]}</figcaption></figure>')


ROOM = ('<path class="d-ground" d="M4 128h232"/>'
        '<path class="d-shell" d="M24 34h150v94H24z"/>'
        '<path class="d-void" d="M24 34h150v15H24z"/>')

BLD  = ('<path class="d-ground" d="M4 128h232"/>'
        '<path class="d-shell" d="M24 24h150v104H24z"/>'
        '<path class="d-floor" d="M24 58h150M24 92h150"/>')

CASSETTE = '<rect class="d-unit" x="{x}" y="{y}" width="38" height="8" rx="2"/>'
RACK     = ('<g class="d-out"><rect x="{x}" y="{y}" width="24" height="46" rx="2"/>'
            '<path d="M{x1} {y1}h14M{x1} {y2}h14M{x1} {y3}h14"/></g>')

COMMERCIAL = {
 'cassette': dict(
   caption='Recessed flush in the ceiling, blows four ways',
   body = ROOM
     + CASSETTE.format(x=80, y=42)
     + pipe('M118 46h48v58h26')
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M84 52q-12 10-16 24', 'M94 52v26', 'M110 52v26', 'M118 52q12 10 16 24'])),

 'ducted-c': dict(
   caption='Unit in the service void, ducted to grilles',
   body = ROOM
     + '<rect class="d-unit" x="86" y="37" width="30" height="10" rx="3"/>'
     + pipe('M86 42H50v7M116 42h34v7')
     + GRILLE.format(x=40, y=49) + GRILLE.format(x=92, y=49) + GRILLE.format(x=140, y=49)
     + pipe('M150 42h22v62h20')
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M46 56q6 10 0 18', 'M98 56q6 10 0 18', 'M146 56q6 10 0 18'])),

 'vrf': dict(
   caption='Mixed unit types on one riser, modular plant on the roof',
   body = BLD
     + CASSETTE.format(x=44, y=28)
     + IN_UNIT.format(x=48, y=64) + GRILLE.format(x=48, y=98)
     + pipe('M82 32h44M74 68h52M68 100h58M126 32v76')
     + pipe('M126 20v12M126 20h30')
     + OUT_UNIT.format(x=156, y=8, cx=173, cy=21)
     + OUT_UNIT.format(x=194, y=8, cx=211, cy=21)
     + pipe('M190 21h4')
     + air(['M50 38v14', 'M74 38v14', 'M52 76v12', 'M52 108v10'])),

 'wall-c': dict(
   caption='One unit, one condenser, the same as a home install',
   body = ROOM
     + IN_UNIT.format(x=44, y=56)
     + pipe('M70 61h96v43h26')
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M48 70q9 7 1 14', 'M56 70q9 7 1 14', 'M64 70q9 7 1 14'])),

 'close': dict(
   caption='Precision cooling aimed at the racks, not the room',
   body = ROOM
     + RACK.format(x=52, y=66, x1=57, y1=78, y2=88, y3=98)
     + RACK.format(x=84, y=66, x1=89, y1=78, y2=88, y3=98)
     + '<rect class="d-unit" x=" 124" y="62" width="22" height="50" rx="3"/>'
     + pipe('M146 70h20v34h26')
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M124 74q-14 0-20 8', 'M124 88q-14 0-20 6', 'M124 100q-14 2-20 6'])),

 'hrv': dict(
   caption='Stale air out, fresh air in, heat kept back',
   body = ROOM
     + '<rect class="d-unit" x="96" y="36" width="34" height="12" rx="3"/>'
     + pipe('M96 42H54v8M130 42h40')
     + GRILLE.format(x=44, y=50) + GRILLE.format(x=104, y=50)
     + pipe('M113 48v2')
     + '<path class="d-warm" d="M170 42h22"/>'
     + OUT_UNIT.format(x=192, y=30, cx=209, cy=43)
     + air(['M50 58q6 10 0 18', 'M110 58q6 10 0 18'])
     + '<path class="d-warm d-air" d="M140 36q14-8 28-4"/>'),
}

def commercial_svg(key):
    d = COMMERCIAL[key]
    return (f'<figure class="sys__dia">'
            f'<svg viewBox="0 0 240 136" role="img" aria-label="{d["caption"]}">{d["body"]}</svg>'
            f'<figcaption>{d["caption"]}</figcaption></figure>')

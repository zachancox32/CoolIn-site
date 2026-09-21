#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The domestic system diagrams, as data rather than markup.

Kept here so the geometry lives in one place: the cards in domestic.html are
generated from it, and a change to a pipe run is a change to one line.

The four domestic system diagrams. One shared visual language: same house
shell, same unit shapes, only the arrangement changes, so the cards read as a
set rather than four unrelated drawings."""

SHELL = ('<path class="d-ground" d="M4 128h232"/>'
         '<path class="d-shell" d="M120 22 30 62v66h180V62z"/>')

def air(paths):
    return ''.join(f'<path class="d-air" d="{p}"/>' for p in paths)

IN_UNIT  = '<rect class="d-unit" x="{x}" y="{y}" width="26" height="9" rx="3"/>'
GRILLE   = '<rect class="d-grille" x="{x}" y="{y}" width="20" height="4" rx="2"/>'
OUT_UNIT = ('<g class="d-out"><rect x="{x}" y="{y}" width="34" height="26" rx="4"/>'
            '<circle cx="{cx}" cy="{cy}" r="7"/><circle class="d-hub" cx="{cx}" cy="{cy}" r="1.8"/></g>')

DIAGRAMS = {
 'wall': dict(
   caption='One indoor unit, one outdoor unit, surface trunking',
   body = SHELL
     + '<rect class="d-room" x="44" y="72" width="60" height="48" rx="2"/>'
     + '<rect class="d-room" x="132" y="72" width="60" height="48" rx="2"/>'
     + IN_UNIT.format(x=52, y=78)
     + '<path class="d-pipe" d="M78 87h62v28"/>'
     + OUT_UNIT.format(x=192, y=98, cx=209, cy=111)
     + '<path class="d-pipe" d="M140 111h52"/>'
     + air(['M56 92q10 7 2 15', 'M64 92q10 7 2 15', 'M72 92q10 7 2 15'])),

 'multi': dict(
   caption='Two to five indoor units sharing one outdoor unit',
   body = SHELL
     + '<path class="d-floor" d="M30 94h180"/>'
     + IN_UNIT.format(x=46, y=70) + IN_UNIT.format(x=104, y=70)
     + IN_UNIT.format(x=46, y=102)
     + '<path class="d-pipe" d="M72 74h58M130 74h28v38M72 106h86"/>'
     + '<path class="d-pipe" d="M158 112h34"/>'
     + OUT_UNIT.format(x=192, y=99, cx=209, cy=112)
     + air(['M50 84q8 6 1 11', 'M108 84q8 6 1 11', 'M50 116q8 6 1 9'])),

 'ducted': dict(
   caption='Unit hidden in the ceiling void, only grilles on show',
   body = SHELL
     + '<path class="d-void" d="M30 62h180v14H30z"/>'
     + '<rect class="d-unit" x="98" y="64" width="30" height="10" rx="3"/>'
     + '<path class="d-pipe" d="M98 69H62v7M128 69h36v7"/>'
     + GRILLE.format(x=52, y=76) + GRILLE.format(x=104, y=76) + GRILLE.format(x=154, y=76)
     + '<path class="d-pipe" d="M128 69h50v44h14"/>'
     + OUT_UNIT.format(x=192, y=100, cx=209, cy=113)
     + air(['M58 84q6 8 0 14', 'M110 84q6 8 0 14', 'M160 84q6 8 0 14'])),

 'console': dict(
   caption='Low level unit, sits where a radiator would',
   body = SHELL
     + '<rect class="d-room" x="52" y="66" width="52" height="30" rx="2"/>'
     + '<rect class="d-unit" x="60" y="108" width="34" height="12" rx="3"/>'
     + '<path class="d-pipe" d="M94 114h98"/>'
     + OUT_UNIT.format(x=192, y=99, cx=209, cy=112)
     + air(['M66 104q4-10 12-14', 'M76 104q4-10 12-14', 'M86 104q4-10 12-14'])),
}

def svg(key):
    d = DIAGRAMS[key]
    return (f'<figure class="sys__dia">'
            f'<svg viewBox="0 0 240 136" role="img" aria-label="{d["caption"]}">{d["body"]}</svg>'
            f'<figcaption>{d["caption"]}</figcaption></figure>')


# ---------- commercial ----------
# Same language, different shell: a flat ceiling with a service void instead of
# a pitched roof, because that is what the kit actually sits in.

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
     + '<path class="d-pipe" d="M118 46h48v58h26"/>'
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M84 52q-12 10-16 24', 'M94 52v26', 'M110 52v26', 'M118 52q12 10 16 24'])),

 'ducted-c': dict(
   caption='Unit in the service void, ducted to grilles',
   body = ROOM
     + '<rect class="d-unit" x="86" y="37" width="30" height="10" rx="3"/>'
     + '<path class="d-pipe" d="M86 42H50v7M116 42h34v7"/>'
     + GRILLE.format(x=40, y=49) + GRILLE.format(x=92, y=49) + GRILLE.format(x=140, y=49)
     + '<path class="d-pipe" d="M150 42h22v62h20"/>'
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M46 56q6 10 0 18', 'M98 56q6 10 0 18', 'M146 56q6 10 0 18'])),

 'vrf': dict(
   caption='Mixed unit types on one riser, modular plant on the roof',
   body = BLD
     + CASSETTE.format(x=44, y=28)
     + IN_UNIT.format(x=48, y=64) + GRILLE.format(x=48, y=98)
     + '<path class="d-pipe" d="M82 32h44M74 68h52M68 100h58M126 32v76"/>'
     + '<path class="d-pipe" d="M126 20v12M126 20h30"/>'
     + OUT_UNIT.format(x=156, y=8, cx=173, cy=21)
     + OUT_UNIT.format(x=194, y=8, cx=211, cy=21)
     + '<path class="d-pipe" d="M190 21h4"/>'
     + air(['M50 38v14', 'M74 38v14', 'M52 76v12', 'M52 108v10'])),

 'wall-c': dict(
   caption='One unit, one condenser, the same as a home install',
   body = ROOM
     + IN_UNIT.format(x=44, y=56)
     + '<path class="d-pipe" d="M70 61h96v43h26"/>'
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M48 70q9 7 1 14', 'M56 70q9 7 1 14', 'M64 70q9 7 1 14'])),

 'close': dict(
   caption='Precision cooling aimed at the racks, not the room',
   body = ROOM
     + RACK.format(x=52, y=66, x1=57, y1=78, y2=88, y3=98)
     + RACK.format(x=84, y=66, x1=89, y1=78, y2=88, y3=98)
     + '<rect class="d-unit" x=" 124" y="62" width="22" height="50" rx="3"/>'
     + '<path class="d-pipe" d="M146 70h20v34h26"/>'
     + OUT_UNIT.format(x=192, y=91, cx=209, cy=104)
     + air(['M124 74q-14 0-20 8', 'M124 88q-14 0-20 6', 'M124 100q-14 2-20 6'])),

 'hrv': dict(
   caption='Stale air out, fresh air in, heat kept back',
   body = ROOM
     + '<rect class="d-unit" x="96" y="36" width="34" height="12" rx="3"/>'
     + '<path class="d-pipe" d="M96 42H54v8M130 42h40"/>'
     + GRILLE.format(x=44, y=50) + GRILLE.format(x=104, y=50)
     + '<path class="d-pipe" d="M113 48v2"/>'
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

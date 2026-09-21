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

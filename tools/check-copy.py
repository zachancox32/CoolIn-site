#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flags phrasing that makes copy read as if a machine wrote it.

Readers and Google both notice the same habits: announcing your own honesty
("two honest caveats"), setting up a point instead of making it ("here's
why"), labelling and counting ("the short version", "one catch"), the
"it's not just X, it's Y" turn, and a small vocabulary of words that turn up
far more in generated text than in anything a tradesman would say.

It reads the sources people actually edit: guides and blog markdown, the
page generators' data, and the hand made HTML pages. It reports every hit
with its file and line. Dashes (em and en) fail the build, because the house
style bans them outright; everything else is a warning to fix by rewriting
the sentence, not by swapping one word for another.

    python3 tools/check-copy.py          warnings, fails only on dashes
    python3 tools/check-copy.py --strict fails on any hit
"""
import glob, html, os, re, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

PATTERNS = [
    # honesty and candour signposting
    (r"\b(honest|honestly|to be honest|in all honesty|if we'?re honest|candidly|frankly)\b", 'announces its own honesty'),
    (r"\b(let'?s be (clear|straight|honest)|to be (clear|straight)|straight with you|the truth is|the reality is)\b", 'announces its own honesty'),
    # setting up a point instead of making it
    (r"\bhere'?s (the thing|why|how|what|the catch|the deal|the version|the kicker|the short|the sum)\b", 'sets up the point instead of making it'),
    (r"\b(the (short|long) (answer|version)|in short|in summary|to sum up|the bottom line|the takeaway|key takeaways?)\b", 'labels the answer instead of giving it'),
    (r"\b(one|two|three|a few) (honest |important |key )?(caveats?|catch(es)?|things to know|points to note)\b", 'counts and labels instead of saying it'),
    (r"\bthe catch\?|\bthe answer\?|\bthe result\?", 'rhetorical question set up'),
    (r"\b(isn'?t|is not|aren'?t|are not) just (a|an|about)\b", '"it\'s not just X" construction'),
    (r"\bnot only\b.{0,60}\bbut also\b", '"not only... but also" construction'),
    # filler and hedges
    (r"\b(it'?s worth noting|worth noting|it'?s important to (note|remember)|notably|importantly|crucially|essentially|ultimately|at the end of the day)\b", 'filler'),
    (r"\b(rest assured|peace of mind|hassle[- ]free|look no further|whether you'?re a)\b", 'stock marketing phrase'),
    # vocabulary that generated text overuses
    (r"\b(delve|delves|delving|seamless(ly)?|elevate|unlock|unleash|game[- ]changer|robust|leverage|streamline|empower|myriad|plethora|realm|tapestry|testament|nestled|bustling|journey|landscape|navigate|navigating|comprehensive|cutting[- ]edge|state[- ]of[- ]the[- ]art|optimal|optimise|enhance|ensure|crucial|vital|pivotal|paramount|meticulous(ly)?|holistic|synergy|boasts?)\b", 'generated text vocabulary'),
    (r"\bin today'?s (world|climate|market|fast)", 'stock opener'),
    (r"\b(genuinely|truly|really) (the )?(best|most|great)\b", 'empty intensifier'),
]
DASH = re.compile('[\u2013\u2014]')

# Hits checked by hand and kept on purpose: (file, text on the line).
ALLOW = [
    ('tools/_sectors_data.py', 'Is cooling the answer?'),        # a customer's own question
    ('tools/build-stats.py', "in today's climate"),              # the Met Office's wording
    ('areas.html', 'justifies the journey'),                     # actual travel
    ('tools/build-guides.py', 'short answer'),                   # the answer box label and code notes
]

FILES = (sorted(glob.glob('guides/source/*.md')) + sorted(glob.glob('blog/posts/*.md')) +
         ['tools/_sectors_data.py', 'tools/_towns_data.py', 'tools/_towns_data2.py', 'tools/build-stats.py',
          'tools/build-guides.py', 'tools/_towngen.py'] +
         [f for f in ['index.html', 'domestic.html', 'commercial.html', 'servicing.html', 'repairs.html',
                      'heat-pumps.html', 'ventilation.html', 'about.html', 'contact.html', 'areas.html',
                      'hvac-contractors.html', 'air-conditioning-size-calculator.html', 'thanks.html',
                      'home-air-conditioning-quote.html', 'air-conditioning-manchester.html',
                      'air-conditioning-liverpool.html', 'air-conditioning-bolton.html',
                      'air-conditioning-stockport.html', 'air-conditioning-chester.html',
                      'air-conditioning-preston.html', '404.html'] if os.path.exists(f)])

def visible(line, path):
    """The words a reader sees on this line: tags, code and comments removed."""
    if path.endswith('.py') and line.lstrip().startswith('#'):
        return ''
    # descriptions and titles are read in search results, so they count too
    extra = ' '.join(re.findall(r'<meta (?:name|property)="(?:description|og:description|twitter:description)" content="([^"]*)"', line))
    line = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', line)
    line = extra + ' ' + line
    line = re.sub(r'<[^>]+>', ' ', line)
    line = re.sub(r'\]\([^)]*\)', ']', line)            # markdown link targets
    return html.unescape(line)

def main():
    strict = '--strict' in sys.argv
    hits, dashes = [], []
    for f in FILES:
        in_script = False
        for n, raw in enumerate(open(f, encoding='utf-8'), 1):
            if '<script' in raw and 'ld+json' not in raw:
                in_script = True
            if in_script:
                if '</script>' in raw:
                    in_script = False
                continue
            t = visible(raw, f)
            if any(f == af and a in raw for af, a in ALLOW):
                continue
            if DASH.search(t):
                dashes.append((f, n, t.strip()[:120]))
            for rx, why in PATTERNS:
                for m in re.finditer(rx, t, re.I):
                    s = max(0, m.start() - 50)
                    hits.append((f, n, why, '...' + t[s:m.end() + 40].strip().replace('\n', ' ') + '...'))
    for f, n, t in dashes:
        print(f'  DASH  {f}:{n}  {t}')
    for f, n, why, ctx in hits:
        print(f'  {f}:{n}  [{why}]  {ctx}')
    print(f'  check-copy  {len(hits)} phrasing warning(s), {len(dashes)} dash(es) in {len(FILES)} files')
    if dashes or (strict and hits):
        sys.exit(1)

if __name__ == '__main__':
    main()

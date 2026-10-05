#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws a PNG of every chart in assets/img/stats, for journalists whose
content systems will not take an SVG.

Run on a Mac after tools/build-stats.py, and commit the PNGs. It uses the
installed Google Chrome to render each SVG, so it is not part of the Netlify
build. Drawn at twice the size for sharp text, and each PNG is recorded in
png-manifest.json against the SVG it came from, so build-stats.py only shows
a PNG while it still matches the figures.

    python3 tools/make-stats-png.py
"""
import os, re, glob, json, hashlib, subprocess, sys, tempfile, time

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
if not os.path.exists(CHROME):
    sys.exit('  make-stats-png: Google Chrome is not installed where expected')

profile = tempfile.mkdtemp(prefix='stats-png-')
manifest = {}
for svg in sorted(glob.glob('assets/img/stats/*.svg')):
    text = open(svg, encoding='utf-8').read()
    w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', text).groups())
    png = svg[:-4] + '.png'
    if os.path.exists(png):
        os.remove(png)
    # Headless Chrome sometimes writes the screenshot and then fails to exit,
    # so wait for the file rather than for the process.
    proc = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2', f'--user-data-dir={profile}',
                             f'--window-size={w},{h}', f'--screenshot={os.path.abspath(png)}',
                             'file://' + os.path.abspath(svg)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if os.path.exists(png) and os.path.getsize(png) > 0:
            time.sleep(0.5)
            break
        time.sleep(0.5)
    proc.kill()
    if not os.path.exists(png):
        sys.exit(f'  make-stats-png: Chrome did not draw {svg}')
    manifest[os.path.basename(svg)[:-4]] = hashlib.sha1(text.encode('utf-8')).hexdigest()[:16]
    print(f'  {png}  {w * 2}x{h * 2}, {os.path.getsize(png) // 1024}KB')

json.dump(manifest, open('assets/img/stats/png-manifest.json', 'w'), indent=1, sort_keys=True)

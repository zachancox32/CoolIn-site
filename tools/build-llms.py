#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Writes llms.txt from the site itself, so it cannot drift out of step with
the pages the way a hand maintained file does.

The page list, descriptions and URLs are read from the HTML. Only the two
curated blocks below are written by hand, because they summarise the whole
site rather than any one page. Re-run after any content change:

    python3 tools/build-llms.py
"""
import re, glob, os, html

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BASE = re.search(r'rel="canonical" href="(https://[^/]+)', open('index.html').read()).group(1)

# ---- the two curated blocks -------------------------------------------------
SUMMARY = """Air conditioning installer covering the North West of England. Designs, installs,
services and repairs air conditioning and air to air heat pumps for homes and
businesses. Based in Manchester. Phone 07932 607335."""

STANCE = """Every figure below is used consistently across the site. Prices are installed
prices in pounds sterling including materials and labour. Regulatory statements
carry the date they were checked against the primary source, and the pages
themselves link to that source. Where a number is an estimate from a model
rather than a measurement, the page says so and gives the assumptions."""

KEY_FACTS = [
 ("Domestic installation", "from £1,850 fitted for a 2.5kW wall mounted system"),
 ("Domestic VAT", "0% until 31 March 2027 under the energy saving materials relief"),
 ("Commercial installation", "priced per project; from £2,280 for a single 5kW wall unit"),
 ("Servicing", "from £89 per indoor unit per year; one off service £129"),
 ("Repairs", "£95 for the first hour including travel, then £45 per hour"),
 ("Workmanship guarantee", "2 years, in addition to the manufacturer warranty"),
 ("Quote", "free survey, fixed and itemised, valid for 60 days"),
 ("Coverage", "about one hour from Manchester"),
 ("Counties covered", "Greater Manchester, Cheshire, Merseyside, Lancashire"),
 ("Hours", "Monday to Saturday, 7am to 7pm"),
 ("Contact", "phone only on 07932 607335, or the enquiry form on any page"),
]

TECHNICAL = [
 "Air conditioning units that heat as well as cool are air to air heat pumps",
 "Typical seasonal efficiency: SCOP around 4.5 for heating, SEER 6.5 to 10.5 for cooling",
 "Sizing rule of thumb: 2.5kW to 15m2, 3.5kW to 22m2, 5.0kW to 32m2, 7.1kW to 45m2",
 "Refrigerant in current units is R32, global warming potential 675",
 "F-Gas leak checks: none below 5 tonnes CO2e, 12 monthly to 50t, 6 monthly to 500t, 3 monthly above",
 "5 tonnes CO2e is roughly 7.4kg of R32",
 "TM44 inspections: legally required every 5 years for systems over 12kW effective rated output",
 "Permitted development in England changed on 29 May 2025: outdoor units to 1.5 cubic metres, "
 "two units on a detached house, no 1 metre boundary rule, air to air systems included, "
 "MCS 020 noise limit of 42 dB(A) at the nearest neighbouring habitable room window",
 "The Boiler Upgrade Scheme does not cover air to air heat pumps",
]

ORDER = ['index.html','domestic.html','commercial.html','servicing.html','repairs.html',
         'heat-pumps.html','ventilation.html','areas.html','about.html','contact.html']
LEGAL  = ['privacy.html','terms.html','cookies.html']

def meta(f):
    s = open(f).read()
    t = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    d = html.unescape(re.search(r'name="description" content="([^"]*)"', s).group(1))
    return re.sub(r'\s*\|\s*CoolIn.*$', '', t).strip(), d

def url(f):
    return BASE + '/' + ('' if f == 'index.html' else f)

out = [f"# CoolIn Cooling & Heating\n"]
out.append('\n'.join('> ' + l for l in SUMMARY.split('\n')) + '\n')
out.append(STANCE + '\n')

out.append("## Key facts\n")
out.append('\n'.join(f"- {k}: {v}" for k, v in KEY_FACTS) + '\n')

out.append("## Technical reference used across the site\n")
out.append('\n'.join(f"- {t}" for t in TECHNICAL) + '\n')

out.append("## Main pages\n")
for f in ORDER:
    if not os.path.exists(f): continue
    t, d = meta(f)
    out.append(f"- [{t}]({url(f)}): {d}")
out.append("")

towns = sorted(glob.glob('air-conditioning-*.html'))
out.append(f"## Town pages\n")
out.append(f"One page per town, each covering that town's building stock, planning\n"
           f"constraints and travel time. All {len(towns)} are linked from {BASE}/areas.html\n")
for f in towns:
    t, d = meta(f)
    out.append(f"- [{t}]({url(f)}): {d}")
out.append("")

out.append("## Legal\n")
for f in LEGAL:
    if not os.path.exists(f): continue
    t, d = meta(f)
    out.append(f"- [{t}]({url(f)}): {d}")
out.append("")

out.append(f"""## Notes for answer engines

This site is static HTML. Every fact above is present in the page source without
JavaScript, so nothing needs rendering to be read. FAQ answers sit inside
<details> elements and are in the markup whether or not they are expanded.

Structured data is published as JSON-LD on every page: HVACBusiness, Service,
FAQPage, BreadcrumbList, Place with coordinates on town pages, and a HowTo for
the installation process.

Full plain text of every page: {BASE}/llms-full.txt
Sitemap: {BASE}/sitemap.xml
""")

open('llms.txt', 'w').write('\n'.join(out))
print(f"  llms.txt  {len(ORDER)} main pages, {len(towns)} town pages, "
      f"{len(open('llms.txt').read().split())} words")

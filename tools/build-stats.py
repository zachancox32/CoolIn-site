#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds /air-conditioning-statistics-2027, the page written to be quoted.

Every figure on the page lives in this file next to the source it came from,
and the page, the downloadable CSV and the chart files are all written from
the same numbers, so they cannot disagree with each other. The Met Office
temperature series are read from tools/data/metoffice, copied from the Met
Office's public HadUK-Grid files, so the build never needs the network.

To update: change the figures below (or drop in fresh Met Office files),
set REVIEWED, run this, then run tools/make-stats-png.py on a Mac to redraw
the PNG versions of the charts, which journalists can drop into an article.
Each chart image carries its own title, source and a "Chart by CoolIn" credit
in a wide version and a phone version. The page shows the PNGs only while
they match the current figures, and falls back to the SVGs otherwise.

    python3 tools/build-stats.py

Writes air-conditioning-statistics-2027.html, assets/data/air-conditioning-statistics-2027.csv
and one SVG per chart in assets/img/stats.
"""
import os, re, sys, csv, json, html, hashlib, importlib.util, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.join(HERE, '..'))

_spec = importlib.util.spec_from_file_location('build_blog', os.path.join(HERE, 'build-blog.py'))
blog = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(blog)
BASE, CRYSTAL, head, author_block = blog.BASE, blog.CRYSTAL, blog.head, blog.author_block
UTILITY, FOOTER = blog.UTILITY, blog.FOOTER
HEADER = (blog.shell('HEADER')
          .replace('<a class="logo" href="#top"', '<a class="logo" href="/"')
          .replace(' class="is-current" aria-current="page"', '')
          .replace('href="#quote">Free survey', 'href="contact#quote">Free survey'))
# The page sits at the root like the hand made pages, so the shell is used
# exactly as sync-shell.py writes it, unrooted, and the two never disagree.

SLUG = 'air-conditioning-statistics-2027'
URL = f'{BASE}/{SLUG}'
SHORT = URL.replace('https://', '')
REVIEWED = '2026-10-05'
PUBLISHED = '2026-10-05'
TITLE = 'Air conditioning statistics 2027: the UK, Manchester and the North West'
SEO_TITLE = 'UK & Manchester Air Conditioning Statistics 2027'
DESC = ('How many UK homes have air conditioning, how Manchester and the North West compare, '
        'who overheats, running costs and what changes in 2027. Sourced, with free charts.')

# ------------------------------------------------------------------ sources
# Numbered in the order they first matter on the page. Charts and findings
# refer to them by key.
SOURCES = {
    'edrc': ('Jones, Fuertes and Charles, Socio-technical drivers of air conditioning adoption and use in UK homes, '
             'Energy Demand Research Centre, June 2026. Analysis of the English Housing Survey 2023-24, 15,846 households',
             'https://www.edrc.ac.uk/publications/socio-technical-drivers-of-air-conditioning-adoption-and-use-in-uk-homes/'),
    'reading': ('University of Reading, The most at risk from heat have the least air con, June 2026',
                'https://www.reading.ac.uk/news/2026/Research-News/The-most-at-risk-from-heat-have-the-least-air-con'),
    'ehs': ('Ministry of Housing, Communities and Local Government, English Housing Survey 2024 to 2025: '
            'weather resilient homes fact sheet, 9 July 2026',
            'https://www.gov.uk/government/statistics/english-housing-survey-2024-to-2025-weather-resilience-in-housing-fact-sheet/english-housing-survey-2024-to-2025-weather-resilient-homes-fact-sheet'),
    'census': ('Office for National Statistics, Census 2021, number of households (TS041). North West: 3,153,403',
               'https://www.ons.gov.uk/datasets/TS041/editions/2021/versions/3'),
    'metgrid': ('Met Office, HadUK-Grid areal series, mean air temperature for England NW and N Wales and for the UK, '
                'last updated 1 October 2026',
                'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/England_NW_and_N_Wales.txt'),
    'metdays': ('Met Office, How exceptional were UK summer 2026 daily temperatures?, 2 September 2026',
                'https://www.metoffice.gov.uk/blog/2026/how-exceptional-were-uk-summer-2026-daily-temperatures'),
    'met40': ('Met Office, Met Office report details rising likelihood of UK hot days, June 2025',
              'https://www.metoffice.gov.uk/about-us/news-and-media/media-centre/weather-and-climate-news/2025/met-office-report-details-rising-likelihood-of-uk-hot-days'),
    'ofgem': ('Ofgem, Energy price cap unit rates and standing charges, 1 October to 31 December 2026',
              'https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges'),
    'ucl': ('Simpson, Halai, Price, Petrou, Heaviside and Davies, Air conditioning and the future electricity system '
            'in Great Britain, Energy Research and Social Science, 2026',
            'https://pmc.ncbi.nlm.nih.gov/articles/PMC7619388/'),
    'fgas': ('Cooling Post, DEFRA delays GB F-gas phase down, 16 May 2026',
             'https://www.coolingpost.com/uk-news/defra-delays-gb-f-gas-phase-down/'),
    'daikin': ('Daikin UK, Air to air heat pump and air conditioner bans of the EU F-gas regulation',
               'https://www.daikin.co.uk/en_gb/knowledge-center/f-gas-regulation/air-to-air-heat-pumps-air-conditioners.html'),
    'fhs': ('UK Parliament, written statement HCWS1445 on the Future Homes and Buildings Standards, 24 March 2026',
            'https://questions-statements.parliament.uk/written-statements/detail/2026-03-24/hcws1445'),
    'vat': ('HM Revenue and Customs, VAT on energy-saving materials and heating equipment (VAT Notice 708/6)',
            'https://www.gov.uk/guidance/vat-on-energy-saving-materials-and-heating-equipment-notice-7086'),
    'partO': ('Home Energy Model, Full Part O overheating review confirmed, 9 April 2026',
              'https://home-energy-model.co.uk/news/2026-04-09-part-o-overheating-review/'),
}
ORDER = list(SOURCES)
def ref(key):
    n = ORDER.index(key) + 1
    return f'<a class="ref" href="#source-{n}" aria-label="Source {n}">[{n}]</a>'

# ------------------------------------------------------------------ figures
ENGLAND_SHARE = 4.3                 # % of households using AC to keep cool, 2023-24 [edrc]
ENGLAND_HOMES = 1.06e6              # the same, as homes [edrc]
NW_SHARE, LONDON_SHARE = 2.5, 6.5   # [edrc]
NW_HOUSEHOLDS = 3153403             # [census]
OVERHEAT_2019, OVERHEAT_2024 = 1.7e6, 3.0e6   # homes reporting overheating [ehs]
INSTALLS_PER_YEAR = 83000           # extra homes with AC each year, 2013 to 2020, BEIS from BSRIA sales [edrc]
UNIT_RATE = 26.32                   # p per kWh, price cap October to December 2026, no VAT [ofgem]

# The survey ran April 2023 to March 2024, so its middle is about October
# 2023. The projection runs from there to July 2027, the height of summer.
YEARS_TO_2027 = 3.75
LOW_2027 = ENGLAND_HOMES + INSTALLS_PER_YEAR * YEARS_TO_2027
HIGH_2027 = ENGLAND_HOMES + 2 * INSTALLS_PER_YEAR * YEARS_TO_2027
HOUSEHOLDS = ENGLAND_HOMES / (ENGLAND_SHARE / 100)          # about 24.7 million
OVERHEAT_2027 = OVERHEAT_2024 + (OVERHEAT_2024 - OVERHEAT_2019) / 5 * 3

NW_HOMES = NW_SHARE / 100 * NW_HOUSEHOLDS
NW_GAP = (LONDON_SHARE - NW_SHARE) / 100 * NW_HOUSEHOLDS

# Typical power drawn, in kW. The split figures are the ones used across the
# site; the rest are typical label figures for each kind of appliance.
APPLIANCES = [
    ('Portable air conditioner', 1.0),
    ('Split system, cooling a hot room down', 0.65),
    ('Split system, holding the room at temperature', 0.3),
    ('Evaporative air cooler', 0.07),
    ('Electric fan', 0.04),
]


def load_summers(path):
    """June to August mean temperature by year from a HadUK-Grid areal file.

    The files are fixed width, with values right aligned under their column
    names, and the current year leaves the months to come blank. So the
    summer value is read from the slice that ends where "sum" ends in the
    header, rather than by counting values, which goes wrong mid year."""
    lines = open(path, encoding='utf-8').read().splitlines()
    hdr = next(l for l in lines if l.startswith('year'))
    end = hdr.index(' sum') + len(' sum')
    start = hdr.index(' spr') + len(' spr')
    out = {}
    for line in lines:
        if not line[:4].isdigit():
            continue
        cell = line[start:end].strip()
        if cell and cell != '---':
            out[int(line[:4])] = float(cell)
    return out

NW = load_summers('tools/data/metoffice/tmean-england-nw-and-n-wales.txt')
UK = load_summers('tools/data/metoffice/tmean-uk.txt')
LATEST = max(NW)
def avg(series, a, b):
    return statistics.mean(v for y, v in series.items() if a <= y <= b)
NW_BASE = avg(NW, 1961, 1990)
NW_RECENT = avg(NW, LATEST - 9, LATEST)
NW_TOP = sorted(NW.items(), key=lambda x: -x[1])[:10]
NW_TOP_RECENT = sum(1 for y, _ in NW_TOP if y >= 2003)
UK_TOP = sorted(UK.items(), key=lambda x: -x[1])[:10]
assert NW_TOP[0][0] == LATEST == UK_TOP[0][0], 'the copy says the latest summer is the hottest on record; check it'


def m(v, dp=2):
    """1371250 -> 1.37 million"""
    s = f'{v / 1e6:.{dp}f}'
    return (s.rstrip('0').rstrip('.') if '.' in s else s) + ' million'

def thou(v, to=1000):
    return f'{round(v / to) * to:,}'

def pence(kw):
    return kw * UNIT_RATE

def one_in(share):
    return round(100 / share)


# ------------------------------------------------------------------ charts
# A chart is a dict: id, title, sub, unit, rows, source keys, note. A row is
# (label, value, shown, kind) where kind is '', 'hi' (the point of the chart),
# 'ref' (a reference line such as the England average) or 'proj' (a
# projection, drawn hatched). A row whose value is None is a group heading.

def R(label, value, shown=None, kind=''):
    if shown is None:
        # survey figures keep their decimal place, so 5.0% does not become 5%
        shown = '' if value is None else (f'{value:.1f}%' if isinstance(value, float) else f'{value}%')
    return (label, value, shown, kind)

CHARTS = {
    'region': dict(
        title='Homes using air conditioning, by region',
        sub='Share of households in each English region using air conditioning to keep cool in summer, 2023-24',
        rows=[R('London', 6.5), R('East of England', 6.5), R('East Midlands', 5.5), R('South East', 5.4),
              R('England', 4.3, kind='ref'), R('West Midlands', 3.5), R('South West', 2.8),
              R('North West', 2.5, kind='hi'), R('Yorkshire and the Humber', 1.7), R('North East', 1.5)],
        src=['edrc']),
    'income': dict(
        title='Air conditioning rises with income',
        sub='Share of households using air conditioning in summer, by household income, England 2023-24',
        rows=[R('Highest fifth', 8.2, kind='hi'), R('Fourth fifth', 5.1), R('Middle fifth', 3.6),
              R('Second fifth', 2.2), R('Lowest fifth', 2.5)],
        src=['edrc']),
    'people': dict(
        title='Those most at risk from heat are least likely to have it',
        sub='Share of households using air conditioning in summer, by who lives there, England 2023-24',
        rows=[R('Child under 5', 6.1), R('Baby under 1', 5.8), R('Someone with a long term illness or disability', 5.0),
              R('All households', 4.3, kind='ref'), R('Someone over 65', 3.7), R('Lone parent with children', 2.9),
              R('Someone over 75', 3.0, kind='hi')],
        src=['edrc']),
    'wfh': dict(
        title='Working from home goes with air conditioning',
        sub='Share of households using air conditioning in summer, by how often someone works from home, England 2023-24',
        rows=[R('Four or more days a week', 6.9, kind='hi'), R('Two or three days a week', 6.3),
              R('Once a week', 5.6), R('Less than once a week', 1.3), R('Never', 3.2)],
        src=['edrc']),
    'home': dict(
        title='Which homes have air conditioning',
        sub='Share of households using air conditioning in summer, by home type, age and tenure, England 2023-24',
        rows=[R('By type', None), R('Detached or bungalow', 6.2), R('Semi detached', 3.9), R('Flat', 3.7), R('Terraced', 3.6),
              R('By age', None), R('Built since 2000', 6.6, kind='hi'), R('Built before 1930', 4.3),
              R('Built 1930 to 1964', 3.7), R('Built 1965 to 1999', 3.6),
              R('By tenure', None), R('Owner occupied', 5.0), R('Private rented', 3.3),
              R('Council', 3.2), R('Housing association', 2.6)],
        src=['edrc']),
    'overheat': dict(
        title='Homes reporting overheating in England',
        sub='Homes where the household reported the home getting uncomfortably hot, millions',
        rows=[R('2019', 1.7, '1.7 million (7%)'), R('2024', 3.0, '3.0 million (12%)', 'hi'),
              R('2027 if the trend continues', round(OVERHEAT_2027 / 1e6, 2), f'about {m(OVERHEAT_2027, 1)}', 'proj')],
        src=['ehs'], note='The 2027 bar is our straight line projection of the 2019 to 2024 rise, not an official figure. Overheating also depends on how hot a given summer is.'),
    'overheat-type': dict(
        title='Which homes overheat',
        sub='Share of homes in England reported as overheating in 2024, by type of home',
        rows=[R('Detached house', 15, kind='hi'), R('Bungalow', 14), R('Semi detached house', 12),
              R('Terraced house', 11), R('Purpose built flat', 9.5, '9 to 10%')],
        src=['ehs']),
    'cooling': dict(
        title='How people cooled down when their home overheated',
        sub='Methods used by the 3 million households in England whose home got uncomfortably hot, 2024-25',
        rows=[R('Opened windows', 90), R('Closed curtains, blinds or shutters', 75), R('Switched on a fan', 59),
              R('Used air conditioning', 7, kind='hi'), R('Put out an awning or canopy', 3)],
        src=['ehs']),
    'cost': dict(
        title='What it costs to keep cool, per hour',
        sub=f'Running cost per hour at the October to December 2026 price cap of {UNIT_RATE}p per kWh',
        rows=[R(n, round(pence(kw), 1), f'{pence(kw):.1f}p', 'hi' if 'holding' in n else '') for n, kw in APPLIANCES],
        src=['ofgem'], unit='p',
        note='Power figures are typical: 0.3 and 0.65kW for a 2.5kW split system, about 1kW for a portable unit, 70W for an air cooler and 40W for a fan. Check the label on your own appliance.'),
    'outlook': dict(
        title='Homes using air conditioning in England by summer 2027',
        sub='Measured in 2023-24, and two projections for July 2027, millions of homes',
        rows=[R('2023-24, measured', 1.06, f'1.06 million ({ENGLAND_SHARE:g}%)'),
              R('2027 at the pre 2020 pace', round(LOW_2027 / 1e6, 2),
                f'{m(LOW_2027)} ({LOW_2027 / HOUSEHOLDS * 100:.1f}%)', 'proj'),
              R('2027 at twice that pace', round(HIGH_2027 / 1e6, 2),
                f'{m(HIGH_2027)} ({HIGH_2027 / HOUSEHOLDS * 100:.1f}%)', 'proj')],
        src=['edrc'], note="Projections are CoolIn's, built from the measured figure and the 2013 to 2020 installation rate. The full method is on the page."),
    'nw-summers': dict(
        title=f'North West England summers, {min(NW)} to {LATEST}',
        sub='Mean temperature, June to August, England NW and North Wales. Orange summers were warmer than the 1961 to 1990 average, blue were cooler',
        series=NW, base=NW_BASE, src=['metgrid'],
        alt_data=(f'Summer {LATEST} was the warmest on record at {NW[LATEST]:.1f}°C, against a 1961 to 1990 average of '
                  f'{NW_BASE:.1f}°C. Seven of the ten warmest summers came in 2003 or later')),
}


# Each chart is drawn twice as a self contained image: a wide one for articles
# and desktop, and a narrow one with larger text for phones. Both carry the
# title, the source and a "Chart by CoolIn" credit with the address, so the
# image still names us wherever it ends up. No logo: the credit line does it.
INK, BODY, GREY, LINE, BLUE, ORANGE, REF, ICE, NAVY = ('#12262F', '#41606E', '#6E8592', '#E1EAEF', '#0E6E96',
                                                       '#E2673B', '#9FB3BE', '#D7EDF7', '#0D2B38')
FONT = "Arial, Helvetica, sans-serif"
WIDE, NARROW = 1200, 600
CREDIT = f'Chart by CoolIn, {SHORT}'


def wrap(text, size, width):
    """Greedy line breaks, using an average Arial character width."""
    per = max(int(width / (size * 0.53)), 10)
    lines, cur = [], ''
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > per:
            lines.append(cur)
            cur = word
        else:
            cur = f'{cur} {word}'.strip()
    return lines + ([cur] if cur else [])


def tspans(lines, x, y, size, lead, **attrs):
    a = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return ''.join(f'<text x="{x}" y="{y + i * size * lead:.0f}" font-size="{size}" {a}>{html.escape(t)}</text>'
                   for i, t in enumerate(lines))


def frame(W, c, body, body_h):
    narrow = W == NARROW
    pad = 32 if narrow else 48
    ts, ss, fs = (30, 19, 17) if narrow else (34, 19, 16)
    title = wrap(c['title'], ts, W - 2 * pad)
    sub = wrap(c['sub'], ss, W - 2 * pad)
    y = 8 + 26 + ts
    head = tspans(title, pad, y, ts, 1.18, font_weight='700', fill=INK)
    y += (len(title) - 1) * ts * 1.18 + ss * 1.7
    head += tspans(sub, pad, y, ss, 1.35, fill=BODY)
    y += (len(sub) - 1) * ss * 1.35 + 30
    out = [head, f'<g transform="translate(0,{y:.0f})">{body}</g>']
    y += body_h
    if c.get('note'):
        note = wrap(c['note'], fs, W - 2 * pad)
        y += 10
        out.append(tspans(note, pad, y + fs, fs, 1.4, fill=GREY))
        y += len(note) * fs * 1.4
    y += 22
    out.append(f'<line x1="{pad}" y1="{y:.0f}" x2="{W - pad}" y2="{y:.0f}" stroke="{LINE}" stroke-width="2"/>')
    text_w = W - 2 * pad
    src = wrap('Source: ' + (c.get('src_line') or src_text(c['src'])), fs, text_w)
    y += 14 + fs
    out.append(tspans(src, pad, y, fs, 1.4, fill=GREY))
    y += len(src) * fs * 1.4
    credit = wrap(CREDIT, fs, text_w)
    out.append(tspans(credit, pad, y, fs, 1.4, font_weight='700', fill=BLUE))
    y += (len(credit) - 1) * fs * 1.4
    h = int(y + 26)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" font-family="{FONT}">\n'
           f'<title>{html.escape(c["title"])}. {html.escape(CREDIT)}</title>\n'
           f'<rect width="{W}" height="{h}" fill="#FFFFFF"/><rect width="{W}" height="8" fill="{BLUE}"/>\n'
           + '\n'.join(out) + '\n</svg>\n')
    return svg, h


def bars_body(c, W):
    narrow = W == NARROW
    pad = 32 if narrow else 48
    fs = 20 if narrow else 19
    rows = c['rows']
    top = max(r[1] for r in rows if r[1] is not None)
    room = max(len(r[2]) for r in rows if r[1] is not None) * fs * 0.56 + 16
    x0 = pad if narrow else 470
    x1 = W - pad - room
    p = [f'<defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<rect width="10" height="10" fill="#FBE7DC"/><line x1="0" y1="0" x2="0" y2="10" stroke="{ORANGE}" stroke-width="4"/></pattern></defs>']
    y = 0
    for label, value, shown, kind in rows:
        if value is None:
            p.append(f'<text x="{pad}" y="{y + 26}" font-size="{fs - 4}" font-weight="700" letter-spacing="2" fill="{GREY}">{html.escape(label.upper())}</text>')
            y += 42
            continue
        w = value / top * (x1 - x0)
        fill = {'hi': ORANGE, 'ref': REF, 'proj': 'url(#hatch)'}.get(kind, BLUE)
        weight = '700' if kind in ('hi', 'ref') else '400'
        stroke = f' stroke="{ORANGE}" stroke-width="2"' if kind == 'proj' else ''
        if narrow:
            p.append(f'<text x="{x0}" y="{y + fs}" font-size="{fs}" font-weight="{weight}" fill="{INK}">{html.escape(label)}</text>')
            by = y + fs + 10
        else:
            p.append(f'<text x="{x0 - 16}" y="{y + 25}" font-size="{fs}" font-weight="{weight}" fill="{INK}" text-anchor="end">{html.escape(label)}</text>')
            by = y + 6
        p.append(f'<rect x="{x0}" y="{by}" width="{x1 - x0:.1f}" height="26" rx="4" fill="{ICE}" opacity=".45"/>')
        p.append(f'<rect x="{x0}" y="{by}" width="{w:.1f}" height="26" rx="4" fill="{fill}"{stroke}/>')
        p.append(f'<text x="{x0 + w + 12:.1f}" y="{by + 20}" font-size="{fs}" font-weight="700" fill="{INK}">{html.escape(shown)}</text>')
        y = by + 26 + (22 if narrow else 14)
    return '\n'.join(p), y


def stripes_body(c, W):
    """Summer temperature by year as columns, warm years orange, cool years blue."""
    narrow = W == NARROW
    series, base = c['series'], c['base']
    years = sorted(series)
    pad = 32 if narrow else 48
    fs = 18 if narrow else 15
    L, Rt, T, B = (50 if narrow else 44), (8 if narrow else 64), 30, 34
    H = 330 if narrow else 340
    pw, ph = W - 2 * pad - L - Rt, H - T - B
    lo, hi = 12.0, 17.0
    bw = pw / len(years)
    def X(i): return pad + L + i * bw
    def Y(v): return T + (hi - v) / (hi - lo) * ph
    halo = 'stroke="#FFFFFF" stroke-width="4" paint-order="stroke" stroke-linejoin="round"'
    p = []
    for t in range(12, 18):
        p.append(f'<line x1="{pad + L}" x2="{pad + L + pw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{LINE}"/>')
        p.append(f'<text x="{pad + L - 8}" y="{Y(t) + 5:.1f}" text-anchor="end" font-size="{fs}" fill="{GREY}">{t}°C</text>')
    for i, yr in enumerate(years):
        v = series[yr]
        a = v - base
        op = 0.22 + 0.78 * min(abs(a) / 2.2, 1)
        y0, y1 = Y(max(v, lo)), Y(lo)
        p.append(f'<rect x="{X(i) + 0.3:.2f}" y="{y0:.1f}" width="{max(bw - 0.6, 0.6):.2f}" height="{y1 - y0:.1f}" '
                 f'fill="{ORANGE if a > 0 else BLUE}" fill-opacity="{op:.2f}"/>')
    by = Y(base)
    p.append(f'<line x1="{pad + L}" x2="{pad + L + pw}" y1="{by:.1f}" y2="{by:.1f}" stroke-dasharray="5 4" stroke="{INK}" stroke-width="1.4"/>')
    p.append(f'<text x="{pad + L + 6}" y="{by + fs + 6:.1f}" font-size="{fs}" fill="{INK}" {halo}>1961 to 1990 average, {base:.1f}°C</text>')
    ticks = (1900, 1950, 2000) if narrow else (1900, 1925, 1950, 1975, 2000, 2025)
    for yr in ticks:
        i = years.index(yr)
        p.append(f'<text x="{X(i) + bw / 2:.1f}" y="{T + ph + fs + 8}" text-anchor="middle" font-size="{fs}" fill="{GREY}">{yr}</text>')
    for yr, anchor in ((1976, 'middle'), (years[-1], 'end')):
        i = years.index(yr)
        p.append(f'<text x="{X(i) + bw:.1f}" y="{Y(series[yr]) - 9:.1f}" text-anchor="{anchor}" font-size="{fs + 1}" '
                 f'font-weight="700" fill="{INK}" {halo}>{yr}: {series[yr]:.1f}°C</text>')
    return '\n'.join(p), H


def findings_body(c, W):
    """The headline findings as one grid: a big figure and a line under it."""
    narrow = W == NARROW
    pad = 32 if narrow else 48
    cols = 2 if narrow else 4
    ns, fs = (44, 18) if narrow else (52, 18)
    cw = (W - 2 * pad) / cols
    cells = [(big, wrap(line, fs, cw - 28)) for _, big, line, _, _ in FINDINGS]
    p = []
    y = 0
    for r in range(0, len(cells), cols):
        row = cells[r:r + cols]
        h = ns + 18 + max(len(t) for _, t in row) * fs * 1.38 + 30
        if r:
            p.append(f'<line x1="{pad}" x2="{W - pad}" y1="{y:.0f}" y2="{y:.0f}" stroke="{LINE}" stroke-width="2"/>')
        for i, (big, lines) in enumerate(row):
            x = pad + i * cw + (0 if i == 0 else 22)
            if i:
                p.append(f'<line x1="{pad + i * cw:.0f}" x2="{pad + i * cw:.0f}" y1="{y + 18:.0f}" y2="{y + h - 14:.0f}" stroke="{LINE}" stroke-width="2"/>')
            colour = ORANGE if r + i == 0 else NAVY
            p.append(f'<text x="{x:.0f}" y="{y + 22 + ns * 0.8:.0f}" font-size="{ns}" font-weight="700" letter-spacing="-1" fill="{colour}">{html.escape(big)}</text>')
            p.append(tspans(lines, round(x), y + 22 + ns * 0.8 + 16 + fs, fs, 1.38, fill=BODY))
        y += h
    return '\n'.join(p), y


def draw(c, W):
    kind = 'findings' if c.get('kind') == 'findings' else 'stripes' if c.get('series') else 'bars'
    body, h = {'findings': findings_body, 'stripes': stripes_body, 'bars': bars_body}[kind](c, W)
    return frame(W, c, body, h)


def alt_text(c):
    if c.get('alt_data'):
        data = c['alt_data']
    else:
        data = '; '.join(f'{label} {shown}' for label, value, shown, kind in c['rows'] if value is not None)
    return f"{c['title']}. {c['sub']}. {data} Source: {c.get('src_line') or src_text(c['src'])}. {CREDIT}."


def src_text(keys):
    names = {'edrc': 'EDRC analysis of the English Housing Survey 2023-24',
             'ehs': 'English Housing Survey 2024 to 2025, MHCLG',
             'ofgem': 'Ofgem price cap, October 2026; CoolIn calculation',
             'metgrid': 'Met Office HadUK-Grid'}
    return '; '.join(names.get(k, SOURCES[k][0]) for k in keys)


STATS_DIR = 'assets/img/stats'
MANIFEST = f'{STATS_DIR}/png-manifest.json'

def digest(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:16]

def png_current(name, svg_text):
    """A PNG is shown only if it was drawn from the SVG as it is now, so a
    figure changed without re-running make-stats-png.py falls back to the SVG
    instead of showing an out of date picture."""
    try:
        made = json.load(open(MANIFEST))
    except (OSError, ValueError):
        return False
    return made.get(name) == digest(svg_text) and os.path.exists(f'{STATS_DIR}/{name}.png')


def figure(cid, c, first=False):
    e = html.escape
    os.makedirs(STATS_DIR, exist_ok=True)
    wide, wh = draw(c, WIDE)
    narrow, nh = draw(c, NARROW)
    open(f'{STATS_DIR}/{cid}.svg', 'w', encoding='utf-8').write(wide)
    open(f'{STATS_DIR}/{cid}-mobile.svg', 'w', encoding='utf-8').write(narrow)
    has_png = png_current(cid, wide)
    ext_w = 'png' if has_png else 'svg'
    ext_n = 'png' if png_current(f'{cid}-mobile', narrow) else 'svg'
    alt = alt_text(c)
    img_url = f'{BASE}/{STATS_DIR}/{cid}.{ext_w}'
    embed = (f'<figure><a href="{URL}#chart-{cid}"><img src="{img_url}" alt="{e(alt)}" width="{WIDE}" height="{wh}" '
             f'style="max-width:100%;height:auto"></a><figcaption>Chart: <a href="{URL}">CoolIn, UK air conditioning '
             f'statistics</a></figcaption></figure>')
    dl = ((f'<a class="chart__dl" href="/{STATS_DIR}/{cid}.png" download="coolin-{cid}.png">Download PNG</a>' if has_png else '')
          + f'<a class="chart__dl" href="/{STATS_DIR}/{cid}.svg" download="coolin-{cid}.svg">SVG</a>')
    load = '' if first else ' loading="lazy"'
    return f'''
    <figure class="chart js-up" id="chart-{cid}">
      <picture>
        <source media="(max-width:640px)" srcset="/{STATS_DIR}/{cid}-mobile.{ext_n}" width="{NARROW}" height="{nh}">
        <img class="chart__img" src="/{STATS_DIR}/{cid}.{ext_w}" width="{WIDE}" height="{wh}" alt="{e(alt)}"{load} decoding="async">
      </picture>
      <figcaption class="chart__foot">
        <p class="chart__src">Free to use with credit to CoolIn. Data: {e(c.get('src_line') or src_text(c['src']))} {' '.join(ref(k) for k in c['src'])}</p>
        <div class="chart__tools">{dl}<button type="button" class="chart__dl chart__embed" data-copy="{e(embed)}" data-done="Embed code copied. Paste it into your article's HTML">Embed</button></div>
      </figcaption>
    </figure>'''


# ------------------------------------------------------------------ copy
LOW_PC, HIGH_PC = LOW_2027 / HOUSEHOLDS * 100, HIGH_2027 / HOUSEHOLDS * 100

WORDS = ['None', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']

# The findings band at the top of the page. Each is (id, the big figure, the
# line beside it, the full sentence that is copied, source keys). The first
# is the figure people search for and leads; the rest are the ones only this
# page has. Keep the list short: every extra line makes the others weaker.
FINDINGS = [
    ('homes', f'{ENGLAND_SHARE:g}%', f'of homes in England use air conditioning. About {m(ENGLAND_HOMES)}.',
     f'Only {ENGLAND_SHARE:g}% of homes in England use air conditioning to keep cool in summer, about {m(ENGLAND_HOMES)} homes.',
     ['edrc']),
    ('north-west', f'{NW_SHARE:g}%', f'in the North West, including Manchester. Roughly {thou(NW_HOMES, 10000)} homes. London: {LONDON_SHARE:g}%.',
     f'In the North West, which includes Manchester, {NW_SHARE:g}% of homes use air conditioning, roughly {thou(NW_HOMES, 10000)} homes, against {LONDON_SHARE:g}% in London and the East of England.',
     ['edrc', 'census']),
    ('gap', thou(NW_GAP, 5000), 'more North West homes would have it at London\'s rate.',
     f'If the North West used air conditioning at London\'s rate, around {thou(NW_GAP, 5000)} more homes in the region would have it.',
     ['edrc', 'census']),
    ('seven', f'{NW_TOP_RECENT} in 10', 'of the North West\'s warmest summers since 1884 came in 2003 or later.',
     f'{WORDS[NW_TOP_RECENT]} of the North West\'s ten warmest summers since 1884 have come in 2003 or later.',
     ['metgrid']),
    ('windows', '7%', 'of households whose home overheated used air conditioning. 90% opened a window.',
     'When their home overheated, 90% of households in England opened the windows and 7% used air conditioning.',
     ['ehs']),
    ('income', '3x', 'as likely to have it in the richest fifth of homes as the poorest: 8.2% against 2.5%.',
     'The highest earning fifth of households are more than three times as likely to use air conditioning as the lowest earning fifth: 8.2% against 2.5%.',
     ['edrc']),
    ('2027', f'{HIGH_2027 / 1e6:.2f}m', f'homes in England could be using it by summer 2027. Up to 1 in {one_in(HIGH_PC)}.',
     f'By summer 2027, between {m(LOW_2027)} and {m(HIGH_2027)} homes in England could be using air conditioning, about 1 in {one_in(LOW_PC)} to 1 in {one_in(HIGH_PC)}.',
     ['edrc']),
    ('ban', 'No ban', 'on air conditioning in Great Britain in 2027. The EU\'s applies in the EU and Northern Ireland only.',
     'No new air conditioning ban arrives in Great Britain in 2027. The EU\'s ban on small split systems using higher warming refrigerants starts in the EU and Northern Ireland on 1 January 2027, but not in England, Scotland or Wales.',
     ['fgas', 'daikin']),
]
assert NW_TOP_RECENT == 7 and len(FINDINGS) == 8, 'the findings band is laid out for eight cards with seven of ten; check it'


FINDINGS_CHART = dict(
    kind='findings', title='UK air conditioning in numbers, 2027',
    sub='Who has it, who goes without, and what changes next year',
    src=list(dict.fromkeys(k for f in FINDINGS for k in f[4])),
    src_line='EDRC analysis of the English Housing Survey 2023-24; English Housing Survey 2024 to 2025; '
             'Met Office HadUK-Grid; ONS Census 2021; DEFRA; CoolIn projection',
    alt_data=' '.join(f[3] for f in FINDINGS))


RECENT = ' class="is-recent"'

def top10_table():
    rows = ''.join(
        f'<tr{RECENT if y >= 2003 else ""}><td>{i}</td><td>{y}</td><td>{v:.1f}°C</td>'
        f'<td>{v - NW_BASE:+.1f}°C</td></tr>'
        for i, (y, v) in enumerate(NW_TOP, 1))
    return f'''<div class="prose__table stats-table js-up">
      <table>
        <caption>The ten warmest summers in North West England and North Wales since 1884, by mean temperature, June to August. Years from 2003 on are highlighted. {ref('metgrid')}</caption>
        <thead><tr><th scope="col">Rank</th><th scope="col">Year</th><th scope="col">Mean</th><th scope="col">Against 1961 to 1990</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>'''


TIMELINE = [
    ('1 January 2027', 'The HFC quota steps down in Great Britain, as already scheduled',
     'DEFRA confirmed in May 2026 that it will not change the 2027 phase down step. Unlike the EU and Northern Ireland, '
     'Great Britain brings in no ban on new split systems in 2027.', ['fgas']),
    ('1 January 2027', 'The EU bans small split systems using higher warming refrigerants',
     'New split air conditioners and heat pumps under 12kW using refrigerant with a global warming potential of 150 or more '
     'cannot be placed on the market in the EU or Northern Ireland.', ['daikin']),
    ('January, April, July and October 2027', 'The energy price cap changes four times',
     'Each change moves the running cost of every appliance in the table above. We update this page when it does.', ['ofgem']),
    ('24 March 2027', 'The Future Homes Standard comes into force in England',
     'New homes have to be more airtight and better insulated. The overheating rule for new homes, Part O, is under '
     'a separate full review.', ['fhs', 'partO']),
    ('31 March 2027', 'Zero rate VAT on home installations ends',
     'Installing energy saving materials in homes, including heat pumps, is zero rated until 31 March 2027, then 5% from '
     '1 April. HMRC says most air conditioning units are air source heat pumps.', ['vat']),
    ('31 March 2027', 'No VAT on household electricity runs until this date',
     'Ofgem\'s price cap shows no VAT on electricity from 1 October 2026 to 31 March 2027.', ['ofgem']),
]


def timeline_html():
    return '\n'.join(f'''        <li class="tl__item">
          <p class="tl__date">{html.escape(d)}</p>
          <h4 class="tl__title">{html.escape(t)}</h4>
          <p class="tl__text">{html.escape(x)} {' '.join(ref(k) for k in keys)}</p>
        </li>''' for d, t, x, keys in TIMELINE)


FAQS = [
    ('What percentage of UK homes have air conditioning?',
     f'The most reliable recent figure is {ENGLAND_SHARE:g}% of homes in England, about {m(ENGLAND_HOMES)}, from the English Housing Survey 2023-24. '
     'The national grid operator, NESO, uses about 3% for the UK, and private surveys have given figures from 8% to 19%. '
     'The surveys ask different questions, which is most of the difference.'),
    ('Which part of England has the most air conditioning?',
     f'London and the East of England, both at {LONDON_SHARE:g}% of homes. The lowest are the North East at 1.5%, '
     f'Yorkshire and the Humber at 1.7% and the North West at {NW_SHARE:g}%.'),
    ('How common is air conditioning in Manchester?',
     f'There is no official figure for Manchester on its own. Manchester is in the North West, where {NW_SHARE:g}% of households '
     f'use air conditioning, roughly {thou(NW_HOMES, 10000)} homes, against {ENGLAND_SHARE:g}% across England and {LONDON_SHARE:g}% in London. '
     'That makes the North West one of the three least air conditioned regions in England.'),
    ('How many homes in England overheat?',
     'About 3 million in 2024, or 12% of occupied homes, up from 1.7 million, or 7%, in 2019. Detached houses were the most likely to overheat, at 15%.'),
    ('Will air conditioning be banned in the UK in 2027?',
     'No. The EU bans new small split systems that use refrigerant with a global warming potential of 150 or more from 1 January 2027, '
     'and that applies in Northern Ireland, but Great Britain has not adopted it. Systems already installed are not affected either way.'),
    ('How much does air conditioning cost to run per hour?',
     f'At the October 2026 price cap of {UNIT_RATE}p per kWh, a 2.5kW split system costs about {pence(0.3):.0f}p an hour holding a room '
     f'at temperature and about {pence(0.65):.0f}p cooling a hot room down. A portable unit costs about {pence(1.0):.0f}p an hour.'),
    ('Can I use these statistics and charts?',
     'Yes. Quote the figures, embed or download the charts, and use the CSV, with credit to CoolIn and a link to this page. '
     'The underlying data belongs to the sources listed, so cite them too where you can.'),
]


def page():
    e = html.escape
    ab = author_block({'author': 'zac-hancox'})
    byline, aschema = (ab[0][0], ab[0][1]) if isinstance(ab[0], tuple) else (ab[0], ab[1])
    byline = re.sub(r'</?p[^>]*>', '', byline)
    y, mo, _ = REVIEWED.split('-')
    byline = re.sub(r'^By ', f'<time datetime="{REVIEWED}">Updated {blog.MONTHS[int(mo) - 1]} {y}</time> by ', byline)

    sources = '\n'.join(f'        <li id="source-{i}"><a href="{u}" rel="noopener">{e(t)}</a></li>'
                        for i, (t, u) in enumerate(SOURCES.values(), 1))

    def night(kw):
        p = pence(kw) * 8
        return f'£{p / 100:.2f}' if p >= 100 else f'{p:.0f}p'
    cost_rows = ''.join(f'<tr><td>{e(n)}</td><td>{kw * 1000:.0f}W</td><td>{pence(kw):.1f}p</td><td>{night(kw)}</td></tr>'
                        for n, kw in APPLIANCES)

    toc = [('findings', 'At a glance'), ('who', 'Who has air conditioning'),
           ('north-west', 'Manchester and the North West'), ('overheating', 'Homes that overheat'), ('summers', 'Hotter summers'),
           ('running-costs', 'Running costs'), ('2027', 'What 2027 brings'), ('estimates', 'Why estimates differ'),
           ('method', 'How we worked these out'), ('use', 'Use these figures'), ('sources', 'Sources')]
    toc_html = ''.join(f'<li><a href="#{a}">{e(t)}</a></li>' for a, t in toc)

    content = f'''<!-- ============ STATISTICS ============ -->
<article class="post statpage">
  <header class="post__head">
    {CRYSTAL}
    <div class="wrap post__wrap stats__wrap">
      <nav class="crumbs crumbs--light js-up" aria-label="Breadcrumb">
        <a href="/">CoolIn</a><span aria-hidden="true">/</span><span aria-current="page">Air conditioning statistics</span>
      </nav>
      <p class="post__cat js-up">Data, updated quarterly</p>
      <h1 class="js-up">{e(TITLE)}</h1>
      <p class="stats__lede js-up">How many homes have air conditioning, how Manchester and the North West compare, who has it, how many overheat, what it costs to run, and what changes in 2027. Every figure links to its source, and every chart is free to use.</p>
      <p class="post__meta js-up">{byline}</p>
    </div>
  </header>

  <div class="wrap stats__wrap">
    <section class="stats__sec" id="findings" aria-labelledby="h-findings">
      <h2 id="h-findings">UK air conditioning statistics at a glance</h2>
{figure('findings', FINDINGS_CHART, first=True)}
      <p class="sr-only" role="status"></p>
    </section>

    <nav class="stats__toc js-up" aria-label="On this page"><p class="stats__toc-h">On this page</p><ul>{toc_html}</ul></nav>

    <section class="stats__sec" id="who" aria-labelledby="h-who">
      <h2 id="h-who">How many UK homes have air conditioning?</h2>
      <div class="prose">
        <p>The best measure of air conditioning in English homes is the English Housing Survey, which asked 15,846 households in 2023-24 how they keep cool in summer. Researchers at the Energy Demand Research Centre and the University of Reading analysed the answers and found that {ENGLAND_SHARE:g}% used air conditioning, about {m(ENGLAND_HOMES)} homes. {ref('edrc')}</p>
        <p>It is not spread evenly. It follows money, the age of the home, where in the country you live, and whether anyone works from home. The households the researchers flag as most at risk from heat, older people and lone parents among them, are among the least likely to have it. {ref('reading')}</p>
      </div>
{figure('region', CHARTS['region'])}
{figure('income', CHARTS['income'])}
{figure('people', CHARTS['people'])}
{figure('home', CHARTS['home'])}
{figure('wfh', CHARTS['wfh'])}
      <div class="prose">
        <p>Two patterns stand out. Homes built since 2000 are the most likely of any age to have air conditioning, at 6.6%, which fits with modern homes being more airtight and better insulated, so they hold heat in summer as well as in winter. And working from home matters: once someone is home four or more days a week, use rises to 6.9%. After allowing for income, home type and region together, households where someone works from home two or more days a week had 42% higher odds of using air conditioning. {ref('edrc')}</p>
      </div>
    </section>

    <section class="stats__sec" id="north-west" aria-labelledby="h-nw">
      <h2 id="h-nw">Air conditioning in Manchester and the North West</h2>
      <div class="prose">
        <p>The North West, which takes in Manchester and the rest of Greater Manchester, has some of the lowest air conditioning use in England. {NW_SHARE:g}% of households use it, which across the region's {NW_HOUSEHOLDS:,} households is roughly {thou(NW_HOMES, 10000)} homes. {ref('edrc')} {ref('census')}</p>
        <p>At London's rate of {LONDON_SHARE:g}%, around {thou(NW_GAP, 5000)} more North West homes would have it. Even allowing for income, home type and the other differences between households, a North West household had 69% lower odds of using air conditioning than one in London. {ref('edrc')}</p>
        <p>The survey does not publish figures for individual cities, so these regional numbers are the closest available for Manchester. In Manchester, the homes most prone to overheating tend to be top floor flats, glass fronted apartments in the city centre and Salford Quays, and offices with south facing windows. The <a href="/air-conditioning-manchester">Manchester page</a> covers what installation involves in the city's mills, terraces and towers.</p>
        <p>The summers are not standing still while that gap stays open. Summer {LATEST} was the warmest in the Met Office record for North West England and North Wales, which goes back to 1884, at a mean of {NW[LATEST]:.1f}°C. Summer {LATEST - 1} was the second warmest. {WORDS[NW_TOP_RECENT]} of the ten warmest have come in 2003 or later, and the last ten summers averaged {NW_RECENT - NW_BASE:.1f}°C warmer than the 1961 to 1990 average. {ref('metgrid')}</p>
      </div>
{figure('nw-summers', CHARTS['nw-summers'])}
{top10_table()}
    </section>

    <section class="stats__sec" id="overheating" aria-labelledby="h-over">
      <h2 id="h-over">How many homes overheat in summer?</h2>
      <div class="prose">
        <p>In 2024, households in about 3 million homes in England said their home got uncomfortably hot, 12% of occupied homes. In 2019 it was 1.7 million, or 7%. Owner occupied homes were the most affected at 13%, against 11% for both private and social renters. {ref('ehs')}</p>
      </div>
{figure('overheat', CHARTS['overheat'])}
{figure('overheat-type', CHARTS['overheat-type'])}
{figure('cooling', CHARTS['cooling'])}
      <div class="prose">
        <p>Air conditioning is still the exception even in homes that overheat. Among those 3 million households, 7% used it: 9% of owner occupiers, 6% of social renters and 4% of private renters. {ref('ehs')} Renters usually need their landlord's permission to fit anything, which goes some way to explaining the gap. The guide to <a href="/guides/air-conditioning-flat-or-apartment">air conditioning in a flat or apartment</a> covers what that involves.</p>
      </div>
    </section>

    <section class="stats__sec" id="summers" aria-labelledby="h-summers">
      <h2 id="h-summers">Hotter summers in the UK and the North West</h2>
      <div class="prose">
        <p>Summer {LATEST} was the hottest on record for the UK as a whole, with a mean of {UK[LATEST]:.1f}°C, ahead of {LATEST - 1} at {UK[LATEST - 1]:.1f}°C. {ref('metgrid')} There were 55 days above 28°C, beating the previous record of 41 days set in 1976 and again in 1995, and 9 days above 35°C, almost double the previous record of 5 in 2020. The Met Office puts a summer with that many days over 35°C at about a 1 in 100 chance in today's climate. {ref('metdays')}</p>
        <p>The UK first passed 40°C in July 2022, when Coningsby in Lincolnshire reached 40.3°C. The Met Office estimates a 50-50 chance of another 40°C day within 12 years of its 2025 study, and says the chance of exceeding 40°C is now over 20 times what it was in the 1960s. {ref('met40')}</p>
      </div>
    </section>

    <section class="stats__sec" id="running-costs" aria-labelledby="h-cost">
      <h2 id="h-cost">How much does air conditioning cost to run?</h2>
      <div class="prose">
        <p>A 2.5kW split system does not draw 2.5kW of electricity. That figure is the heat it moves. Once the room is down to temperature it throttles back to roughly 0.3kW. At the price cap for October to December 2026, {UNIT_RATE}p per kWh with no VAT on electricity until 31 March 2027, that is about {pence(0.3):.0f}p an hour. {ref('ofgem')} The <a href="/blog/air-conditioning-running-costs">running costs article</a> goes through heating costs as well.</p>
      </div>
{figure('cost', CHARTS['cost'])}
      <div class="prose__table stats-table js-up">
        <table>
          <caption>Running cost at {UNIT_RATE}p per kWh, per hour and for an eight hour night</caption>
          <thead><tr><th scope="col">Appliance</th><th scope="col">Typical draw</th><th scope="col">Per hour</th><th scope="col">Eight hours</th></tr></thead>
          <tbody>{cost_rows}</tbody>
        </table>
      </div>
      <div class="prose">
        <p>A fan and an air cooler are far cheaper to run because they do not lower the temperature of the room. A fan moves air across your skin, and an evaporative cooler adds moisture, which helps less in humid weather. A portable air conditioner does cool, but a single hose unit pushes the room air it has just cooled out of the window, so it draws the most power for the least effect.</p>
      </div>
    </section>

    <section class="stats__sec" id="2027" aria-labelledby="h-2027">
      <h2 id="h-2027">Air conditioning in 2027: what changes</h2>
      <div class="prose">
        <p>Some of 2027 is already fixed in law or policy. Some of it is a projection, which we show with its working. And one part nobody can tell you: how hot summer 2027 will be. Seasonal forecasts do not reach that far ahead, so anyone quoting a forecast for next summer's weather today is guessing.</p>
        <h3>What is already decided</h3>
      </div>
      <ol class="tl js-up">
{timeline_html()}
      </ol>
      <div class="prose">
        <h3>What the trend points to</h3>
        <p>If homes in England took up air conditioning at the pace measured from 2013 to 2020, about 83,000 more a year, {m(LOW_2027)} homes would be using it by July 2027, {LOW_PC:.1f}% of households. {ref('edrc')} That pace came before the record summers of 2022, 2025 and 2026, so it is a floor more than a forecast. At twice the pace, it would be {m(HIGH_2027)}, or {HIGH_PC:.1f}%: about 1 in {one_in(HIGH_PC)} homes.</p>
      </div>
{figure('outlook', CHARTS['outlook'])}
      <div class="prose">
        <p>Overheating is moving faster. If the 2019 to 2024 rise carries on in a straight line, about {m(OVERHEAT_2027, 1)} homes in England would report overheating in 2027. {ref('ehs')} Further out, NESO's scenarios have between 10% and 40% of UK homes using air conditioning by 2050, depending on the path the energy system takes. {ref('edrc')} Researchers at UCL have argued that home air conditioning may already be more common than every one of NESO's 2024 scenarios assumed for 2030. {ref('ucl')}</p>
      </div>
    </section>

    <section class="stats__sec" id="estimates" aria-labelledby="h-est">
      <h2 id="h-est">Why air conditioning estimates differ</h2>
      <div class="prose">
        <p>Published figures for UK homes with air conditioning run from about 3% to 19%. They are mostly answering different questions.</p>
      </div>
      <div class="prose__table stats-table js-up">
        <table>
          <thead><tr><th scope="col">Estimate</th><th scope="col">Figure</th><th scope="col">What it measures</th></tr></thead>
          <tbody>
            <tr><td>English Housing Survey 2023-24 {ref('edrc')}</td><td>4.3%</td><td>Households in England that use air conditioning to keep cool in summer. A large official survey, 15,846 households</td></tr>
            <tr><td>NESO {ref('edrc')}</td><td>About 3%</td><td>UK homes with air conditioning, used for planning the electricity grid</td></tr>
            <tr><td>Official survey, 2021-22 {ref('ucl')}</td><td>3.1%</td><td>UK households, as cited by UCL researchers</td></tr>
            <tr><td>Private surveys, 2023 and 2024 {ref('ucl')}</td><td>19% and 8%</td><td>Smaller online polls, as cited by UCL researchers. Likely to count portable units and to over represent people interested in the subject</td></tr>
          </tbody>
        </table>
      </div>
      <div class="prose">
        <p>For a single number, use the English Housing Survey figure: it is the largest, the most recent official measure, and it is the one the research on this page is built on.</p>
      </div>
    </section>

    <section class="stats__sec" id="method" aria-labelledby="h-method">
      <h2 id="h-method">How we worked these out</h2>
      <div class="prose">
        <p>Most figures on this page are quoted straight from the sources listed below. These are the ones we calculated ourselves:</p>
        <ul>
          <li><strong>North West homes.</strong> {NW_SHARE:g}% of the region's {NW_HOUSEHOLDS:,} households at the 2021 Census is {NW_HOMES:,.0f}, which we round to {thou(NW_HOMES, 10000)}. At London's {LONDON_SHARE:g}%, the difference is {NW_GAP:,.0f}, which we round to {thou(NW_GAP, 5000)}.</li>
          <li><strong>Summer temperatures.</strong> The Met Office's HadUK-Grid mean temperature series for England NW and North Wales and for the UK, June to August, {min(NW)} to {LATEST}, last updated by the Met Office on 1 October 2026. The averages and rankings are ours. The regional series includes North Wales.</li>
          <li><strong>Running costs.</strong> Power drawn multiplied by {UNIT_RATE}p per kWh. The power figures are typical for each kind of appliance, not measured on a particular model.</li>
          <li><strong>The 2027 projection.</strong> We start from {m(ENGLAND_HOMES)} homes at the middle of the survey, October 2023, and add 83,000 homes a year, the rate the government estimated from sales data for 2013 to 2020, for the {YEARS_TO_2027:g} years to July 2027. The higher figure doubles that rate. Percentages hold the number of households at the survey's {HOUSEHOLDS / 1e6:.1f} million. The 83,000 figure covers the UK, so applying it to England alone slightly flatters the lower figure.</li>
          <li><strong>Overheating in 2027.</strong> The rise from {m(OVERHEAT_2019)} homes in 2019 to {m(OVERHEAT_2024)} in 2024 is about 260,000 a year. Carried on for three more years, that gives about {m(OVERHEAT_2027, 1)}. A cool summer would bring the real figure in lower.</li>
        </ul>
        <p>We will update this page when new data is published, and each quarter when the price cap changes. The date at the top shows when it was last checked.</p>
      </div>
    </section>

    <section class="stats__sec" id="use" aria-labelledby="h-use">
      <div class="cite js-up">
        <svg class="cite__mark" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M12 2v20"/><path d="M3.3 7 20.7 17"/><path d="M20.7 7 3.3 17"/><path d="M12 6 9.4 3.4M12 6l2.6-2.6M12 18l-2.6 2.6M12 18l2.6 2.6"/><path d="m17.1 9 3.2-.9M17.1 9l.9 3.2M6.9 15l-3.2.9M6.9 15 6 11.8"/><path d="m17.1 15 3.2.9M17.1 15l.9-3.2M6.9 9l-3.2-.9M6.9 9 6 12.2"/></g></svg>
        <div class="cite__intro">
          <p class="eyebrow"><span class="eyebrow__mark"></span>Free to use</p>
          <h2 id="h-use">Writing about air conditioning?</h2>
          <p>Quote any figure, embed or download any chart, and take the full dataset as a spreadsheet. All we ask is credit to CoolIn and a link to this page.</p>
        </div>
        <div class="cite__tools">
          <p class="cite__label" id="cite-label">Link to this page</p>
          <div class="cite__field">
            <span class="cite__url" aria-labelledby="cite-label">{e(SHORT)}</span>
            <button type="button" class="btn btn--primary cite__copy" data-copy="{URL}" data-done="Link copied to your clipboard">Copy link</button>
          </div>
          <div class="cite__alt">
            <button type="button" class="btn btn--ghost cite__copy" data-copy="{e(f'<a href="{URL}">UK air conditioning statistics</a>')}" data-done="HTML link copied to your clipboard">Copy as HTML</button>
            <a class="btn btn--ghost" href="/assets/data/{SLUG}.csv" download>Download the data (CSV)</a>
          </div>
          <p class="cite__status" role="status"></p>
        </div>
      </div>
    </section>

    <section class="stats__sec guide-faq" aria-labelledby="h-faq">
      <h2 id="h-faq">Questions people ask</h2>
      <div class="acc">
{chr(10).join(f"""        <details class="acc__item">
          <summary>{e(q)}</summary>
          <div class="acc__body"><p>{e(a)}</p></div>
        </details>""" for q, a in FAQS)}
      </div>
    </section>

    <section class="stats__sec" id="sources" aria-labelledby="h-sources">
      <h2 id="h-sources">Sources</h2>
      <ol class="sources">
{sources}
      </ol>
    </section>

    <aside class="post-cta js-up">
      <div>
        <h2>Thinking about air conditioning in Manchester?</h2>
        <p>We fit air conditioning across Manchester and the North West. A free survey settles where the units go, what size you need, and a fixed written price within 48 hours.</p>
      </div>
      <div class="post-cta__act">
        <a class="btn btn--primary" href="/contact">Book a free survey</a>
        <a class="post-cta__tel" href="/guides/air-conditioning-cost-manchester">See what it costs</a>
      </div>
    </aside>
  </div>
</article>
'''

    qa = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": TITLE, "description": DESC,
         "datePublished": PUBLISHED, "dateModified": REVIEWED, "author": aschema,
         "publisher": {"@id": f"{BASE}/#business"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
         "image": f"{BASE}/assets/img/og-image.png", "inLanguage": "en-GB"},
        {"@type": "Dataset", "name": "UK air conditioning statistics",
         "description": ('Air conditioning use in English homes by region, income, household and home type; homes '
                         'reporting overheating; North West England summer temperatures since 1884; running costs at '
                         'the current price cap; and projections for 2027, compiled from official sources.'),
         "url": URL, "creator": {"@id": f"{BASE}/#business"}, "dateModified": REVIEWED,
         "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/",
         "spatialCoverage": "England, United Kingdom, including North West England and Manchester", "temporalCoverage": f"{min(NW)}/2027",
         "keywords": ["air conditioning", "overheating", "heatwave", "housing", "energy", "North West England"],
         "citation": [u for _, u in SOURCES.values()],
         "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv",
                           "contentUrl": f"{BASE}/assets/data/{SLUG}.csv"}]},
        {"@type": "FAQPage", "mainEntity": qa},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CoolIn", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Air conditioning statistics", "item": URL}]}]}
    jsonld = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'
    return head(SEO_TITLE, DESC, URL, jsonld) + UTILITY + HEADER \
        + '\n<main id="main">\n\n' + content + '\n</main>\n\n' + FOOTER


def write_csv():
    rows = [('metric', 'group', 'value', 'unit', 'period', 'area', 'source', 'source_url', 'note')]
    src_of = {'region': 'edrc', 'income': 'edrc', 'people': 'edrc', 'wfh': 'edrc', 'home': 'edrc',
              'overheat': 'ehs', 'overheat-type': 'ehs', 'cooling': 'ehs', 'cost': 'ofgem', 'outlook': 'edrc'}
    for cid, c in CHARTS.items():
        if c.get('series'):
            continue
        group_prefix = ''
        for label, value, shown, kind in c['rows']:
            if value is None:
                group_prefix = label + ': '
                continue
            s = SOURCES[src_of[cid]]
            note = 'CoolIn projection' if kind == 'proj' else ''
            unit = 'pence per hour' if cid == 'cost' else ('million homes' if cid in ('overheat', 'outlook') else '% of households')
            rows.append((c['title'], group_prefix + label, value, unit, c['sub'], 'England' if cid != 'cost' else 'Great Britain',
                         s[0].split(',')[0] if cid != 'cost' else 'Ofgem; CoolIn', s[1], note))
    for y in sorted(NW):
        rows.append(('Mean summer temperature, June to August', 'England NW and North Wales', f'{NW[y]:.2f}', '°C', str(y),
                     'England NW and North Wales', 'Met Office HadUK-Grid', SOURCES['metgrid'][1], ''))
    for y in sorted(UK):
        rows.append(('Mean summer temperature, June to August', 'United Kingdom', f'{UK[y]:.2f}', '°C', str(y),
                     'United Kingdom', 'Met Office HadUK-Grid',
                     'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/UK.txt', ''))
    os.makedirs('assets/data', exist_ok=True)
    with open(f'assets/data/{SLUG}.csv', 'w', newline='', encoding='utf-8') as f:
        f.write(f'# UK air conditioning statistics, compiled by CoolIn, {URL}, updated {REVIEWED}. Free to use with credit and a link.\n')
        csv.writer(f).writerows(rows)


if __name__ == '__main__':
    write_csv()
    out = page()
    for bad in ('–', '—'):
        if bad in out:
            sys.exit(f'  build-stats: the page contains a {"en" if bad == chr(0x2013) else "em"} dash, which the house style does not use')
    open(f'{SLUG}.html', 'w', encoding='utf-8').write(out)
    print(f'  {SLUG}.html  {len(CHARTS)} charts, {len(FINDINGS)} findings, {len(SOURCES)} sources')

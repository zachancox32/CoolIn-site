#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Writes tools/coolin-sizing.xlsx, the room sizing calculator.

An xlsx is a zip of XML, so it is written here directly rather than pulling in
a spreadsheet library. Standard library only, same as everything else in here.

The arithmetic is the same as the calculator on domestic.html, so the sheet and
the website can never quote different numbers for the same room. Formulas use
nested IF rather than IFS or FILTER, which keeps the file working in older
Excel, LibreOffice and Numbers as well as 365 and Google Sheets.

    python3 tools/make-sizing-xlsx.py
"""
import os, zipfile
from xml.sax.saxutils import escape

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = 'tools/coolin-sizing.xlsx'
SIZES = [(2.0, 1850), (2.5, 1850), (3.5, 1995), (5.0, 2280), (6.0, 2650), (7.1, 2950)]

def ceil_f(c):  return f'IF({c}="High",1.12,IF({c}="Vaulted",1.26,1))'
def glaz_f(g):  return f'IF({g}="Shaded",0.95,IF({g}="Sunny",1.2,IF({g}="Bifolds",1.35,1)))'
def use_f(u):   return (f'IF({u}="Kitchen",0.5,IF({u}="Office",0.4,'
                        f'IF({u}="Gym",0.9,IF({u}="Server",1.4,0))))')

def load_f(w, l, c, g, rf, p, u):
    return (f'ROUND(({w}*{l}*0.155)*{ceil_f(c)}*{glaz_f(g)}'
            f'*IF(LOWER({rf})="y",1.2,1)+MAX(0,{p}-2)*0.1+{use_f(u)},2)')

def ladder(ref, values, last):
    """Smallest unit that covers the load. Nested IF so it works everywhere."""
    out = last
    for kw, v in reversed(values):
        out = f'IF({ref}<={kw},{v},{out})'
    return out

def unit_f(ref):  return ladder(ref, [(kw, kw) for kw, _ in SIZES], '"two units"')
def price_f(ref): return ladder(ref, [(kw, p) for kw, p in SIZES], '""')

# style ids: 0 plain, 1 bold, 2 white on navy, 3 input, 4 big result, 5 muted, 6 money
S_PLAIN, S_BOLD, S_HEAD, S_INPUT, S_BIG, S_MUTED, S_MONEY = range(7)

rows = []          # (style, [(style_override|None, value_or_formula), ...])
def row(cells): rows.append(cells); return len(rows)

def t(v, s=S_PLAIN): return ('s', v, s)     # text
def n(v, s=S_PLAIN): return ('n', v, s)     # number
def f(v, s=S_PLAIN): return ('f', v, s)     # formula
def blank():         return None

row([t('CoolIn rough sizing', S_BOLD)])
row([t('Same arithmetic as the calculator on cool-in.co.uk. Rough only, the survey decides.', S_MUTED)])
row([])
row([t('ONE ROOM', S_HEAD), t('', S_HEAD), t('change the middle column', S_HEAD)])
r_w = row([t('Width m', S_BOLD),   n(3.6, S_INPUT)])
r_l = row([t('Length m', S_BOLD),  n(4.2, S_INPUT)])
r_c = row([t('Ceiling', S_BOLD),   t('Standard', S_INPUT), t('Standard / High / Vaulted', S_MUTED)])
r_g = row([t('Glazing', S_BOLD),   t('Average', S_INPUT),  t('Average / Shaded / Sunny / Bifolds', S_MUTED)])
r_r = row([t('Roof room', S_BOLD), t('n', S_INPUT),        t('y or n', S_MUTED)])
r_p = row([t('People', S_BOLD),    n(2, S_INPUT)])
r_u = row([t('Room use', S_BOLD),  t('Bedroom', S_INPUT),  t('Bedroom / Kitchen / Office / Gym / Server', S_MUTED)])
r_load = row([t('Load kW', S_BOLD),
              f(load_f(f'B{r_w}', f'B{r_l}', f'B{r_c}', f'B{r_g}', f'B{r_r}', f'B{r_p}', f'B{r_u}'))])
row([t('FIT THIS UNIT', S_BOLD), f(unit_f(f'B{r_load}'), S_BIG), t('kW', S_MUTED)])
row([t('Guide price', S_BOLD), f(price_f(f'B{r_load}'), S_MONEY), t('installed, one room', S_MUTED)])
row([])
row([t('WHOLE HOUSE', S_HEAD)] + [t('', S_HEAD) for _ in range(11)])
row([t(x, S_BOLD) for x in ['Room','Width m','Length m','Ceiling','Glazing','Roof room','People',
                            'Room use','Area m2','Load kW','Unit kW','Guide GBP']])
EX = [['Main bedroom',3.6,4.2,'Standard','Average','n',2,'Bedroom'],
      ['Lounge',4.2,5.4,'High','Sunny','n',4,'Bedroom'],
      ['Loft office',3.0,3.8,'Vaulted','Average','y',1,'Office']]
first = None
for i in range(12):
    r = len(rows) + 1
    if first is None: first = r
    e = EX[i] if i < len(EX) else ['', '', '', '', '', '', '', '']
    cells = [t(e[0], S_INPUT), n(e[1], S_INPUT) if e[1] != '' else t('', S_INPUT),
             n(e[2], S_INPUT) if e[2] != '' else t('', S_INPUT)] + \
            [t(e[k], S_INPUT) for k in (3, 4, 5)] + \
            [n(e[6], S_INPUT) if e[6] != '' else t('', S_INPUT), t(e[7], S_INPUT)]
    ld = f'J{r}'
    cells += [f(f'IF(B{r}="","",ROUND(B{r}*C{r},1))'),
              f(f'IF(B{r}="","",{load_f(f"B{r}", f"C{r}", f"D{r}", f"E{r}", f"F{r}", f"G{r}", f"H{r}")})'),
              f(f'IF({ld}="","",{unit_f(ld)})'),
              f(f'IF({ld}="","",{price_f(ld)})', S_MONEY)]
    row(cells)
last = len(rows)
row([t('')]*7 + [t('Total load', S_BOLD),
                 f(f'IF(COUNT(J{first}:J{last})=0,"",ROUND(SUM(J{first}:J{last}),1))', S_BOLD),
                 t('kW', S_MUTED)])
row([])
row([t('Careful with the money column', S_BOLD)])
row([t('Guide prices are one wall unit installed in one room.', S_MUTED)])
row([t('Do not add them up for a house. Several rooms on one condenser is a multi split,', S_MUTED)])
row([t('which starts at 3450 and is priced after a survey.', S_MUTED)])
row([t('Total load is the figure that matters there, for sizing the condenser.', S_MUTED)])

def col(i): return chr(65 + i)

def sheet_xml():
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
           '<cols>',
           '<col min="1" max="1" width="17" customWidth="1"/>',
           '<col min="2" max="2" width="15" customWidth="1"/>',
           '<col min="3" max="3" width="34" customWidth="1"/>',
           '<col min="4" max="8" width="12" customWidth="1"/>',
           '<col min="9" max="12" width="12" customWidth="1"/>',
           '</cols>', '<sheetData>']
    for ri, cells in enumerate(rows, 1):
        if not cells:
            out.append(f'<row r="{ri}"/>'); continue
        parts = [f'<row r="{ri}">']
        for ci, cell in enumerate(cells):
            if cell is None: continue
            kind, val, st = cell
            ref = f'{col(ci)}{ri}'
            if kind == 'f':
                parts.append(f'<c r="{ref}" s="{st}"><f>{escape(str(val))}</f></c>')
            elif kind == 'n':
                parts.append(f'<c r="{ref}" s="{st}"><v>{val}</v></c>')
            elif val == '':
                parts.append(f'<c r="{ref}" s="{st}"/>')
            else:
                parts.append(f'<c r="{ref}" s="{st}" t="inlineStr"><is><t>{escape(str(val))}</t></is></c>')
        parts.append('</row>')
        out.append(''.join(parts))
    out += ['</sheetData>', '</worksheet>']
    return ''.join(out)

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="1"><numFmt numFmtId="164" formatCode="&quot;GBP &quot;#,##0"/></numFmts>
<fonts count="6">
<font><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><b/><sz val="18"/><color rgb="FF0E6E96"/><name val="Calibri"/></font>
<font><sz val="10"/><color rgb="FF5A7080"/><name val="Calibri"/></font>
<font><b/><sz val="12"/><color rgb="FF0D2B38"/><name val="Calibri"/></font>
</fonts>
<fills count="4">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF0D2B38"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFFF4D6"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2">
<border><left/><right/><top/><bottom/><diagonal/></border>
<border><left/><right/><top/><bottom style="thin"><color rgb="FFD6E1E8"/></bottom><diagonal/></border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="7">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="2" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>
<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="164" fontId="5" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1"/>
</cellXfs>
</styleSheet>'''

PARTS = {
 '[Content_Types].xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>''',
 '_rels/.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''',
 'xl/workbook.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Sizing" sheetId="1" r:id="rId1"/></sheets>
<calcPr calcId="0" fullCalcOnLoad="1"/>
</workbook>''',
 'xl/_rels/workbook.xml.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',
 'xl/styles.xml': STYLES,
 'xl/worksheets/sheet1.xml': sheet_xml(),
}

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, body in PARTS.items():
        z.writestr(name, body)
print(f'  {OUT}  {os.path.getsize(OUT):,} bytes, {len(rows)} rows')

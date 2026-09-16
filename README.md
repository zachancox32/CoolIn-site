# CoolIn Cooling & Heating, website

Static site, 21 pages. No build step and no dependencies to install.

## Run it

```
python3 -m http.server 4322
```

Then open http://localhost:4322/index.html

## Pages

| File | Purpose |
|---|---|
| `index.html` | Hub. Routes to domestic or commercial within one screen of the hero |
| `domestic.html` | Homes: systems, sizing calculator, prices, gas comparison, running costs |
| `commercial.html` | Business: sectors, systems, budgets, compliance, maintenance |
| `servicing.html` | Service plans, F-Gas leak checks, TM44, how warranties work |
| `repairs.html` | Common faults, callout costs, response times, repair or replace |
| `heat-pumps.html` | Air to air against air to water, grants, efficiency, suitability |
| `ventilation.html` | MVHR, kitchen extract and make up air, filtration |
| `areas.html` | Coverage hub, linking the six town pages |
| `about.html` | Who CoolIn are and the guarantees offered in place of a history |
| `contact.html` | Phone, email, address, coverage, form |
| `air-conditioning-<town>.html` | Six town pages: Manchester, Liverpool, Stockport, Chester, Preston, Bolton |
| `privacy.html` `terms.html` `cookies.html` | Legal. Templates, not reviewed by a solicitor |
| `thanks.html` `404.html` | Form confirmation and not found. Both noindex |

```
assets/css/style.css    all styling, light theme, tokens at the top
assets/js/scene.js      three.js hero, loaded conditionally (see performance)
assets/js/main.js       GSAP, size calculator, gas comparison, sub nav, form
assets/img/brands/      manufacturer logos
sitemap.xml robots.txt  technical SEO
llms.txt llms-full.txt  for answer engines and language models
tools/                  two maintenance scripts, see below
```

## Maintenance

The flat HTML files are the source of truth. Two scripts keep the repetitive parts honest:

```bash
python3 tools/sync-shell.py          # check the shared chrome is in step
python3 tools/sync-shell.py --write  # push index.html's header and footer everywhere
python3 tools/build-llms-full.py     # regenerate llms-full.txt from the pages
```

`sync-shell.py` only touches the regions between the `SHELL:` marker comments, and it
re-marks the current nav item per page. Page content is never read or written. Change the
phone number or a nav item in `index.html`, run it with `--write`, and all 20 other pages
follow. Run `build-llms-full.py` after any content edit.

## Search and answer engines

Built for both from the start rather than retrofitted.

**Technical**
- One `<h1>` per page, headings in order, semantic sections
- Unique title (under 60 characters) and description (120 to 160) on every page
- Canonical URL, Open Graph, Twitter card and geo meta on every page
- `sitemap.xml` with 19 indexable URLs, `robots.txt` naming the answer engine crawlers explicitly
- No page duplicates another page's FAQ, so they do not compete with each other

**Structured data**, one JSON-LD graph per page:
- `HVACBusiness` with address, hours, area served and services on the homepage
- `Service` plus `BreadcrumbList` on every service page
- `Service` plus `Place` with coordinates plus `BreadcrumbList` on every town page
- `FAQPage` on all eleven pages that carry questions, generated from the visible markup
  so the two can never drift apart

**For language models and chatbots**
- `llms.txt` at the root: what the company is, hard numbers, the technical reference used
  across the site, and a described link to every page
- `llms-full.txt`: the readable text of all 16 content pages, 18,000 words, regenerated
  by `tools/build-llms-full.py`
- An "In short" key facts block near the top of every substantial page. It opens with a
  self contained definition sentence and follows with a labelled grid of hard numbers,
  which is the shape a model needs to quote something accurately
- Facts carry their units, their date and their source. Regulatory claims say when they
  were checked and when they expire
- Estimates are labelled as estimates, with the assumptions printed next to them

**Performance**, because Core Web Vitals feed rankings
- three.js is 600kb, so `scene.js` only fetches it on a viewport of 900px or wider, with
  motion allowed and Save Data off, and then only during browser idle time. Phones never
  download it and the hero falls back to the CSS gradient
- GSAP and the page scripts are deferred
- No images, no web fonts beyond two Google families, no analytics, no cookie banner

## What is still placeholder

## Copy stance

The site makes no claim about history, review scores or numbers of installs, because
CoolIn is new and none of that would be true. Trust is carried by things a new firm can
actually commit to: a free survey, a fixed written price, a workmanship guarantee, one
point of contact, certification for the work itself, and being straight about how the
equipment behaves.

The site does not claim the work is done without subcontractors, because it will be.
The line it takes instead is that CoolIn holds the contract and the guarantee whoever is
on site, everyone doing refrigerant work is F-Gas certified, and the customer is told who
is coming before the day. If that changes, the FAQ "Who will actually be doing the work?"
on the homepage and point 01 in the Why section are the two places to edit.

Two sections handle the age of the business head on:

- **Why trust a new name with the job** admits the business is new, then answers it.
- **Our promise** replaces testimonials. Swap it for real reviews once you have them.
  The `.quote` markup still holds a quote, a name and a location, so it drops straight
  back in. Delete the `.quote__ico` block and put `<div class="stars">★★★★★</div>` back.

## Facts on the page, and where they came from

These were checked against primary sources rather than copied from competitors. They do
change, so re-check before a rewrite.

| Claim | Source | Watch for |
|---|---|---|
| 0% VAT on domestic installs, 1 May 2023 to 31 March 2027, reverting to 5% | HMRC VAT Notice 708/6 | The 2027 end date, and any Budget change |
| HMRC treats most air conditioning as an air source heat pump | VAT Notice 708/6, section 2.15 | Applies to units that heat, not cooling only |
| Permitted development widened on 29 May 2025: 1.5m³ unit, two units on a detached house, no 1m boundary rule, air to air included | Planning Portal, GPDO Part 14 Class G | MCS 020 becomes the sole scheme from 28 May 2026 |
| MCS 020 noise limit, 42 dB(A) at the neighbour's window | MCS Planning Standards | |
| F-Gas leak checks: none under 5t CO2e, 12 months to 50t, 6 months to 500t, 3 months above | gov.uk, checking F gas equipment for leaks | Hermetically sealed under 10t CO2e are exempt |
| TM44 inspection every 5 years for systems over 12kW | Energy Performance of Buildings Directive | Duty sits with the building operator |
| R32 global warming potential roughly a third of R410A | Manufacturer data | |

## Numbers you must set yourself

Every price on the page is indicative and needs replacing with yours.

- Price guide: one room £1,850 to £2,950, multi split £3,450 to £8,200, console £2,150,
  cassette £2,450, ducted £3,500
- The typical install panel in the Why section, currently £1,850
- Service plans: £89, £149 and £229 per unit per year, and £129 for a one off service
- Repair rates: £95 for the first hour, £45 an hour after that
- Commercial bands on commercial.html, £2,280 up to £14,000 and the per project lines
- Ventilation prices: £450 extract, £5,200 MVHR, £6,500 kitchen extract
- Running cost section assumes 25p per kWh electricity and 6.5p per kWh gas. Both are in
  the copy so they are easy to update, and the comparison holds even when rates move.
- The four commitments in the band: 48 hour quote, 2 year workmanship guarantee, no
  extras after acceptance, one point of contact

## The size calculator

Lives at the bottom of `assets/js/main.js`. It starts from 155W per square metre, which
is what makes it agree with the sizing table above it, then applies multipliers for
ceiling height, aspect and glazing, roof rooms, occupancy and room use.

Unit sizes and prices are in the `SIZES` array. Change a price there and change it in the
price guide too, or the page contradicts itself.

## The gas boiler comparison

Also in `assets/js/main.js`, on the domestic page. Every input is on the page so a visitor
can put their own tariff in, and the three constants sit at the top of that function:

| Constant | Value | What it is |
|---|---|---|
| `SCOP` | 4.5 | Seasonal heating efficiency of a current A+++ wall unit |
| `BOILER` | 0.88 | Gas boiler efficiency across a real season, not the badge figure |
| `DUTY` | 0.6 | Share of peak heat loss the room actually calls for on average |

The model is: heat needed a day = room area x watts per m2 x hours x duty. The heat pump
divides that by SCOP and multiplies by the electricity price. The boiler divides by 0.88,
multiplies by the gas price, then multiplies again by how much of the house the boiler
warms to heat that one room.

On the defaults, 20m² heated 6 hours a day for six months, it shows £55 for the heat pump
against £291 for gas central heating warming the whole house, a saving of £236. The panel
also prints the like for like figure, £73 against £55, so the honest 25% efficiency gain is
visible and the rest of the gap is clearly attributed to heating empty rooms.

If a visitor enters a tariff where gas wins, it says so rather than showing a negative
saving.

## Other placeholders

- Phone `0161 000 0000`, email `hello@coolin.co.uk`, address Unit 14 Trafford Park
- Company number and VAT number in the footer
- Accreditation badges. F-Gas, Fully insured and Part P are listed. REFCOM, MCS and
  TrustMark are commented out in the HTML, ready to add once you are registered.
- The heat pump service card avoids claiming Boiler Upgrade Scheme grants, which need MCS
  certification. There is a comment in the card explaining what to add back.
- Areas covered assumes a Trafford Park base and an hour radius
- The JSON-LD in every `<head>` carries the business details. Update the address, phone
  and domain there, in `llms.txt`, in `sitemap.xml` and in the visible markup together.
- The domain `coolin.co.uk` is assumed throughout, in canonicals, sitemap, robots and
  llms.txt. Change it everywhere at once if the real domain differs.
- Legal pages are templates. A solicitor should read the terms before they go live, and
  the cookie policy becomes wrong the moment analytics is added.

## Brand logos

`assets/img/brands/` holds the manufacturers' own SVG marks, taken from Simple Icons in
their official brand colours, with the viewBox cropped to the artwork so they line up.

Three are approximations and should be swapped for official artwork from each
manufacturer's brand pack:

- **Daikin** is set as text in Daikin blue, because no clean SVG was available
- **Mitsubishi Electric** is the diamond mark with the name set in our typeface
- **Fujitsu** is the infinity mark with the name set in our typeface

Panasonic, Toshiba, Samsung, LG and Hitachi are the real wordmarks.

## Not built yet

- The quote form is wired for Netlify Forms: `data-netlify`, a honeypot field and
  `action="/thanks.html"`. Deploy to Netlify and it works with no further setup. Run it
  anywhere else and you need your own handler. Locally the JavaScript intercepts the
  submit and shows the confirmation panel instead, so the demo still behaves.
- Six town pages exist. Altrincham, Warrington, Wigan, Wilmslow and Macclesfield are the
  obvious next ones, but only write them if you can say something genuinely different
  about each. Thin duplicated location pages do more harm than no page at all.
- No blog. Regular articles answering real customer questions are the single biggest
  remaining lever for both search rankings and being cited by chatbots.
- No images anywhere. Photographs of real installations are the biggest single
  improvement available, for trust and for search. Every card that uses a CSS gradient or
  an icon is a place a photograph belongs. Give each one a descriptive alt attribute.
- No Google Business Profile. For local search that matters as much as the whole site.

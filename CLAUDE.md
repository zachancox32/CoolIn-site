# CoolIn website

Air conditioning installer based in Manchester, covering the North West. Live at
https://cool-in.co.uk on Netlify, deployed from `main` on GitHub. The owner pushes;
commit, but don't push or deploy unless asked.

## Copy rules (hard rules, the owner has corrected drift before)

- Never claim to hold F-Gas, insurance, Part P, MCS, REFCOM or TrustMark. Describe the
  duty ("must be done by an F-Gas certified technician"), never claim the ticket.
- Legal entity: CoolIn Limited, company number 17501944, registered in England and Wales,
  registered office Lloyds House, 18-22 Lloyd Street, Manchester M2 5WA. Show it only in
  legal places (footer, terms, privacy, contact, schema legalName, email footer).
  Everyday copy says "CoolIn".
- No false history or implied track record: no "since", "years of experience", founded
  dates, "our clients", "the most common call we get", "most of our work". Never use the
  incorporation date as trading history.
- Don't mention subcontracting on the site, and don't deny it either.
- All prices are guide prices, installed. Home installations are 0% VAT until
  31 March 2027 (then 5%). Every commercial (business) price is shown "plus VAT".
  No VAT number on the site until the owner supplies one.
- No em dashes or en dashes anywhere. Avoid AI tells (optimal, enhance, ensure, seamless,
  crucial, leading, experienced).
- Body copy uses natural contractions (it's, don't, you're, can't). Headings, page
  titles, meta descriptions, FAQ questions and legal pages stay uncontracted. Never
  contract at the end of a clause.
- Write like a person, not a machine. Before committing any copy, run
  `python3 tools/check-copy.py` and rewrite every hit. It flags announcing your own
  honesty ("two honest caveats", "the honest answer"), set ups ("here's how", "here's
  why"), labels instead of answers ("the short version", "in short", "one catch"),
  "it's not just X, it's Y", filler ("it's worth noting", "ultimately") and words that
  generated text overuses (delve, seamless, robust, journey, ensure, enhance). Fix by
  rewriting the sentence, not swapping a synonym. Dashes fail the Netlify build.
- Plain language for homeowners: "fitted" or "wall mounted" air conditioning, not
  "split system" (explain the trade term once if needed).
- Don't name competitors on the site.
- Stock photos only from free licences (Unsplash, Pexels), no readable branding, no
  recognisable faces, logged in assets/img/photos/CREDITS.md. Never present stock as
  CoolIn's own work.
- Never put secrets, API keys or tokens in the repo or in chat.

## How the site is built

Static HTML, no framework, no Node. Netlify runs the Python build chain in
`netlify.toml`: blog, sectors, case studies, guides, stats, cache busting, redirects,
sitemap, llms.txt, llms-full.txt, then `tools/check-urls.py` (fails the build on any
`.html` address; all links are clean URLs) and `tools/indexnow.py` (only places the key
file; submission happens in `netlify/functions/deploy-succeeded.js` after a live deploy).

- Shared header, footer and utility bar live in `index.html` between `SHELL` markers.
  Run `python3 tools/sync-shell.py --write` after changing them; nav highlighting is
  the `CURRENT` map in that script.
- Generated pages: edit the source, not the HTML.
  - Town pages: `tools/_towns_data.py`, `tools/_towns_data2.py`, `tools/_towngen.py`,
    run `tools/_build_towns.py`. Manchester, Liverpool, Bolton, Stockport, Chester and
    Preston are hand maintained HTML.
  - Commercial sector pages: `tools/_sectors_data.py` + `tools/build-sectors.py`
    (optional `photo`, `chooser` and `price_from` fields).
  - Guides: `guides/source/*.md` + `tools/build-guides.py`. Blog: `blog/posts/*.md` +
    `tools/build-blog.py`. Both editable in the Sveltia CMS at /admin.
  - Statistics page `/air-conditioning-statistics-2027`: `tools/build-stats.py` holds
    every figure beside its source. Chart PNGs need `tools/make-stats-png.py`, which uses
    a local Google Chrome (not part of the Netlify build); the page falls back to SVG
    when PNGs are stale.
- Hand maintained pages: index, domestic, commercial, servicing, repairs, heat-pumps,
  ventilation, about, contact, areas, hvac-contractors, the size calculator, thanks,
  and the paid search landing page `/home-air-conditioning-quote` (noindex, out of the
  sitemap and llms files on purpose).
- Forms are Netlify Forms (`quote`, `get-in-touch`, `contractor`, `home-quote`).
  `netlify/functions/submission-created.js` emails leads through Resend; keys are
  Netlify environment variables, never in the repo.
- Analytics: GA4 G-4MGYWZ7WMD in `assets/js/analytics.js`, loaded only after cookie
  consent. Leads are counted as `generate_lead` when /thanks loads after a real submit.

Run the whole build locally before committing a content change:

```
python3 tools/build-blog.py && python3 tools/build-sectors.py && python3 tools/build-case-studies.py && python3 tools/build-guides.py && python3 tools/build-stats.py && python3 tools/bust-cache.py && python3 tools/build-redirects.py && python3 tools/build-sitemap.py && python3 tools/build-llms.py && python3 tools/build-llms-full.py && python3 tools/check-urls.py && python3 tools/sync-shell.py
```

## Business facts used across the site

Phone 07391 523255. Hours Mon to Sat, 7am to 7pm. Home installs from £1,650 (2.0 or 2.5kW),
£1,850 (3.5kW), £2,150 (5.0kW), £2,450 (6.0kW), £2,750 (7.1kW), two to five rooms from
£3,450. Commercial from £2,280 plus VAT for a 5kW wall unit. Servicing from £89 per indoor
unit per year. Brands fitted most: Daikin, Mitsubishi Electric, Samsung.
Google Business Profile CID 14475175223730434639.

## Open and parked items

- No reviews or real job photos yet; add a reviews strip and real photos when they exist.
- Case studies are built but hidden until there are real jobs.
- Some lines imply a track record (Altrincham, Liverpool and Rochdale town pages, repairs
  page, gas boiler article) and should be reworded as general facts.
- Parked: glossary page, press page for heatwave PR (before May 2027), a time limited
  offer on the landing page, home servicing and repair prices once VAT registered.
- Update the statistics page at each Ofgem price cap change (Jan, Apr, Jul, Oct).

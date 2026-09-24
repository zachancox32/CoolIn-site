# -*- coding: utf-8 -*-
"""What kind of page a file is, decided in one place.

Town pages used to be found with glob('air-conditioning-*.html'). That held
until air-conditioning-size-calculator.html arrived and was counted as a town.
A town page is now identified by what it is rather than what it is called: its
breadcrumb runs through Areas covered. No other page's breadcrumb does.
"""
import glob

_TOWN_CRUMB = '<a href="areas">Areas covered</a><span aria-hidden="true">/</span>'


def town_pages():
    """Every town page file, sorted, e.g. ['air-conditioning-altrincham.html', ...]."""
    return sorted(f for f in glob.glob('air-conditioning-*.html')
                  if _TOWN_CRUMB in open(f, encoding='utf-8').read())

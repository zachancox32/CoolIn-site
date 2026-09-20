# -*- coding: utf-8 -*-
"""A small markdown subset, standard library only.

Deliberately not a full implementation. It covers what trade blog posts
actually use, and nothing else, so there is no dependency to install on
Netlify and the build cannot break because a package moved.

Supports: # headings, paragraphs, **bold**, *italic*, `code`, [links](url),
bullet and numbered lists, > blockquotes, --- rules, and pipe tables.

A block that starts with an HTML tag is passed through untouched, so a post
can be authored as raw HTML instead of markdown. Posts come from the CMS,
which only repo collaborators can write to, so the HTML is trusted.
"""
import re, html as _html

def _inline(t):
    t = _html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    return t

_RAW_HTML = re.compile(r'^</?[A-Za-z][A-Za-z0-9-]*(\s|/?>|$)')

def render(md):
    lines = md.replace('\r\n', '\n').split('\n')
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1; continue

        if _RAW_HTML.match(s):                          # raw HTML block, verbatim
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i].rstrip()); i += 1
            out.append('\n'.join(buf)); continue

        if s.startswith('---') and set(s) == {'-'} and len(s) >= 3:
            out.append('<hr>'); i += 1; continue

        m = re.match(r'^(#{2,4})\s+(.*)$', s)          # h1 is the page title
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{_inline(m.group(2))}</h{lvl}>'); i += 1; continue

        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip()); i += 1
            out.append('<blockquote><p>' + _inline(' '.join(buf)) + '</p></blockquote>'); continue

        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:\-|]+\|$', lines[i+1].strip()):
            head = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            th = ''.join(f'<th scope="col">{_inline(c)}</th>' for c in head)
            tb = ''.join('<tr>' + ''.join(f'<td>{_inline(c)}</td>' for c in r) + '</tr>' for r in rows)
            out.append(f'<div class="prose__table"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            continue

        if re.match(r'^[-*]\s+', s):
            items = []
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i].strip()):
                items.append(_inline(re.sub(r'^[-*]\s+', '', lines[i].strip()))); i += 1
            out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'); continue

        if re.match(r'^\d+[.)]\s+', s):
            items = []
            while i < len(lines) and re.match(r'^\d+[.)]\s+', lines[i].strip()):
                items.append(_inline(re.sub(r'^\d+[.)]\s+', '', lines[i].strip()))); i += 1
            out.append('<ol>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'); continue

        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{2,4}\s|[-*]\s|\d+[.)]\s|>|\||---)', lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        out.append('<p>' + _inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)

def frontmatter(text):
    """Parse the --- block at the top. Handles key: value and key: [a, b]."""
    if not text.startswith('---'):
        return {}, text
    end = text.index('\n---', 3)
    raw, body = text[3:end], text[end + 4:]
    data = {}
    for line in raw.split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or ':' not in line:
            continue
        k, v = line.split(':', 1)
        v = v.strip().strip('"').strip("'")
        if v.startswith('[') and v.endswith(']'):
            v = [x.strip().strip('"').strip("'") for x in v[1:-1].split(',') if x.strip()]
        data[k.strip()] = v
    return data, body.lstrip('\n')

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
        if not buf:
            # A line no branch above claimed, e.g. a stray '|' that is not a
            # table. Take it as plain text. Without this the index never moves
            # and the build hangs instead of failing.
            buf.append(s); i += 1
        out.append('<p>' + _inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)

def frontmatter(text):
    """Parse the --- block at the top.

    Handles `key: value`, inline `key: [a, b]`, block lists, and the `|` and
    `>` block scalars the CMS writes for any multi-line field.
    """
    if not text.startswith('---'):
        return {}, text
    end = text.index('\n---', 3)
    raw, body = text[3:end], text[end + 4:]
    lines = raw.split('\n')
    data, i = {}, 0

    def indent(ln):
        return len(ln) - len(ln.lstrip(' '))

    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith('#') or ':' not in line.split('#')[0]:
            i += 1; continue
        base = indent(line)
        k, v = line.split(':', 1)
        k, v = k.strip(), v.strip()
        i += 1

        if v in ('|', '|-', '>', '>-'):                     # block scalar
            buf = []
            while i < len(lines) and (not lines[i].strip() or indent(lines[i]) > base):
                buf.append(lines[i][base + 2:] if len(lines[i]) > base + 2 else '')
                i += 1
            while buf and not buf[-1].strip():
                buf.pop()
            sep = '\n' if v.startswith('|') else ' '
            data[k] = sep.join(buf)
            continue

        if v == '':                                          # maybe a block list
            items = []
            while i < len(lines) and lines[i].strip().startswith('- ') and indent(lines[i]) > base:
                items.append(lines[i].strip()[2:].strip().strip('"').strip("'")); i += 1
            data[k] = items if items else ''
            continue

        v = v.strip('"').strip("'")
        if v.startswith('[') and v.endswith(']'):
            v = [x.strip().strip('"').strip("'") for x in v[1:-1].split(',') if x.strip()]
        data[k] = v
    return data, body.lstrip('\n')

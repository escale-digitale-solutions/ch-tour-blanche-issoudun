"""Passages documentaires générés depuis le HTML réellement publié, sans dépendance.

build_assistant_index(docs, metadata) retourne (docs avec ancres, index JSON).
Les liens de documents sont indexés comme intitulés ; les PDF externes ne sont
pas lus. Aucun texte n'est inventé ou rédigé par un modèle.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import re

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
BLOCK = {'p', 'div', 'section', 'article', 'li', 'dt', 'dd', 'h1', 'h2', 'h3', 'h4', 'figcaption', 'address'}


def clean(text):
    text = re.sub(r'\s+', ' ', text.replace('\xa0', ' ')).strip()
    text = re.sub(r'\s+([.,])', r'\1', text)
    return text


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()[:14]


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    position: int = 0
    children: list = field(default_factory=list)
    parent: 'Node | None' = None

    @property
    def classes(self):
        return set(self.attrs.get('class', '').split())

    def text(self):
        if self.tag == 'br':
            return ' '
        if self.tag in {'script', 'style', 'button', 'svg', 'input', 'select', 'textarea'}:
            return ''
        pieces = []
        for child in self.children:
            if isinstance(child, str):
                pieces.append(child)
            else:
                value = child.text()
                pieces.append((' ' + value + ' ') if child.tag in BLOCK | {'a', 'time'} else value)
        return ''.join(pieces)

    def nodes(self, tag=None):
        for child in self.children:
            if isinstance(child, Node):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.nodes(tag)


class Tree(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.offsets = [0]
        self.offsets += [m.end() for m in re.finditer('\n', source)]
        self.root = Node('root')
        self.stack = [self.root]
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        line, col = self.getpos()
        node = Node(tag, dict(attrs), self.offsets[line - 1] + col, parent=self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def split_text(text, limit=500):
    """Conserve les phrases et leurs négations ; coupe sur un mot si nécessaire."""
    text = clean(text)
    if not text:
        return []
    # Protéger les abréviations de personnes et les nombres décimaux.
    protected = re.sub(r'\b(Dr|Mme|M|Pr|Dre|Mlle)\.', lambda m: m.group(0).replace('.', '\u2024'), text)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ«])', protected)
    result, current = [], ''
    for sentence in sentences:
        sentence = sentence.replace('\u2024', '.')
        while len(sentence) > limit:
            if current:
                result.append(current)
                current = ''
            split = sentence.rfind(' ', 0, limit + 1)
            if split < 1:
                split = limit
            result.append(sentence[:split].rstrip())
            sentence = sentence[split:].lstrip()
        if current and len(current) + 1 + len(sentence) > limit:
            result.append(current)
            current = sentence
        else:
            current = (current + ' ' + sentence).strip()
    if current:
        result.append(current)
    return result


class Extractor:
    def __init__(self, path, source, metadata):
        self.path = path
        self.source = source
        self.meta = metadata
        self.tree = Tree(source)
        self.headings = {}
        self.passages = []
        self.insertions = {}
        self.seen = set()
        self.ids = {n.attrs['id'] for n in self.tree.root.nodes() if n.attrs.get('id')}

    def section(self):
        return ' › '.join(self.headings[k] for k in sorted(self.headings) if k > 1)

    def anchor(self, node, context):
        if node.attrs.get('id'):
            return node.attrs['id']
        if node.position in self.insertions:
            return self.insertions[node.position]
        anchor = 'assistant-' + digest(self.path + '|' + context)
        suffix = 1
        base = anchor
        while anchor in self.ids:
            suffix += 1
            anchor = base + '-' + str(suffix)
        self.ids.add(anchor)
        self.insertions[node.position] = anchor
        return anchor

    def add(self, node, text, kind='paragraph', section=None):
        text = clean(text)
        section = self.section() if section is None else section
        if len(text) < 3:
            return
        anchor = self.anchor(node, kind + '|' + section + '|' + text)
        for part in split_text(text):
            signature = (section, part, kind)
            if signature in self.seen:
                continue
            self.seen.add(signature)
            self.passages.append({
                'id': digest(self.path + '|' + section + '|' + kind + '|' + part),
                'page': self.path,
                'title': self.meta.get('t') or self.headings.get(1, self.path),
                'section': section,
                'text': part,
                'kind': kind,
                'url': self.path + '#' + anchor,
                'keywords': self.meta.get('k', ''),
            })

    def links_only(self, node):
        all_text = clean(node.text())
        links = [clean(n.text()) for n in node.nodes('a') if clean(n.text())]
        # Telephone links are genuine facts when paired with labels.
        if any(n.attrs.get('href', '').startswith(('tel:', 'mailto:')) for n in node.nodes('a')):
            return False
        return bool(links) and len(' '.join(links)) >= max(1, len(all_text) * .72)

    def table(self, node):
        headers, group = [], ''
        for row in node.nodes('tr'):
            cells = [c for c in row.children if isinstance(c, Node) and c.tag in {'th', 'td'}]
            if not cells:
                continue
            values = [clean(c.text()) for c in cells]
            if all(c.tag == 'th' and c.attrs.get('scope') == 'col' for c in cells):
                headers = values
                continue
            if len(cells) == 1 and (cells[0].attrs.get('colspan') or cells[0].attrs.get('scope') == 'colgroup'):
                group = values[0]
                continue
            if headers and len(headers) == len(values):
                text = ' ; '.join(f'{h} : {v}' if h else v for h, v in zip(headers, values) if v)
            else:
                text = ' : '.join(values[:2])
                if len(values) > 2:
                    text += ' ; ' + ' ; '.join(values[2:])
            section = ' › '.join(s for s in [self.section(), group] if s)
            self.add(row, text, 'table', section)

    def definition_list(self, node):
        term = ''
        for item in node.nodes():
            if item.tag == 'dt':
                term = clean(item.text())
            elif item.tag == 'dd':
                if item.classes & {'empty', 'result'}:
                    continue
                kind = 'document' if any('docs' in n.classes for n in item.nodes()) else 'definition'
                if term == 'Documents':
                    for child in item.children:
                        if isinstance(child, Node):
                            self.walk(child)
                else:
                    self.add(item, (term + ' : ' if term else '') + clean(item.text()), kind,
                             ' › '.join(s for s in [self.section(), term] if s))

    def listing(self, node):
        items = [c for c in node.children if isinstance(c, Node) and c.tag == 'li']
        if not items:
            return
        floor = node.parent if node.parent and 'floor' in node.parent.classes else None
        if floor:
            label = next(floor.nodes('small'), None)
            level = clean(label.text()) if label else ''
            for item in items:
                self.add(item, (level + ' : ' if level else '') + clean(item.text()), 'list')
            return
        document = 'docs' in node.classes
        navigation = bool(node.classes & {'stations', 'dir', 'intent'})
        # Actuality cards have independent headings and paragraphs: keep together.
        if 'newslist' in node.classes:
            for item in items:
                heading = next(item.nodes('h3'), None)
                title = clean(heading.text()) if heading else self.section()
                self.add(item, clean(item.text()), 'paragraph', title)
            return
        if document or navigation:
            for item in items:
                self.add(item, clean(item.text()), 'document' if document else 'navigation')
            return
        # Group short related items, e.g. documents to bring and examination types.
        batch, anchor_node = [], items[0]
        for item in items:
            text = clean(item.text())
            if not text:
                continue
            kind = 'navigation' if self.links_only(item) else 'list'
            if kind == 'navigation' or len(text) > 240:
                if batch:
                    self.add(anchor_node, ' ; '.join(batch), 'list')
                    batch = []
                self.add(item, text, kind)
                continue
            if batch and len(' ; '.join(batch + [text])) > 490:
                self.add(anchor_node, ' ; '.join(batch), 'list')
                batch = []
            if not batch:
                anchor_node = item
            batch.append(text)
        if batch:
            self.add(anchor_node, ' ; '.join(batch), 'list')

    def walk(self, node):
        if node.tag in {'nav', 'script', 'style', 'svg', 'button', 'select', 'textarea', 'input', 'dialog'}:
            return
        if node.classes & {'filter', 'empty', 'result', 'field', 'prog', 'hero-actions', 'hints'}:
            return
        if node.tag in {'h1', 'h2', 'h3', 'h4'}:
            level = int(node.tag[1])
            for key in list(self.headings):
                if key >= level:
                    del self.headings[key]
            self.headings[level] = clean(node.text())
            return
        if node.tag == 'table':
            self.table(node)
            return
        if node.tag == 'dl':
            self.definition_list(node)
            return
        if node.tag in {'ul', 'ol'}:
            self.listing(node)
            return
        if node.tag in {'p', 'address', 'figcaption'}:
            kind = 'navigation' if self.links_only(node) else 'paragraph'
            self.add(node, node.text(), kind)
            return
        if node.tag == 'a':
            # Standalone clickable cards/links are navigation, not a fact.
            self.add(node, node.text(), 'navigation')
            return
        previous = dict(self.headings)
        for child in node.children:
            if isinstance(child, Node):
                self.walk(child)
        # An aside must not inherit headings from unrelated main prose sections.
        if node.tag == 'aside' or 'callout' in node.classes:
            self.headings = previous

    def extract(self):
        main = next(self.tree.root.nodes('main'), None)
        if main:
            self.walk(main)
        result = self.source
        for position, anchor in sorted(self.insertions.items(), reverse=True):
            end = result.find(' ', position)
            closing = result.find('>', position)
            insert_at = min(end, closing) if end != -1 else closing
            result = result[:insert_at] + f' id="{anchor}"' + result[insert_at:]
        return result, self.passages


def build_assistant_index(docs, metadata):
    """Indexe toutes les pages sauf l'erreur404, avec des ancres de source stables."""
    by_path = {p['u']: p for p in metadata}
    updated, passages = [], []
    page_count = 0
    for path, source in docs:
        if path == '404.html':
            updated.append((path, source))
            continue
        extractor = Extractor(path, source, by_path.get(path, {}))
        html, found = extractor.extract()
        updated.append((path, html))
        passages.extend(found)
        page_count += 1
    return updated, {
        'version': 1,
        'generatedAt': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'pages': page_count,
        'passages': passages,
    }

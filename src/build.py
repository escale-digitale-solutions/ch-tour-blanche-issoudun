#!/usr/bin/env python3
"""Génère le site statique dans ../dist. Usage : python3 src/build.py"""
import json, os, shutil, sys
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(__file__))
import core, services, pages
from assistant_index import build_assistant_index

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "dist")

# Le serveur d’aperçu peut avoir OUT comme répertoire courant : conserver son inode.
os.makedirs(OUT, exist_ok=True)
for entry in os.scandir(OUT):
    if entry.is_dir(follow_symlinks=False):
        shutil.rmtree(entry.path)
    else:
        os.unlink(entry.path)
os.makedirs(os.path.join(OUT, "assets", "fonts"), exist_ok=True)

docs = [pages.home(), pages.urgences(), pages.services_hub(), *services.all_services(), *pages.parcours(), *pages.hebergement(),
        *pages.prevention(), *pages.carrieres(), *pages.hopital(), *pages.actualites(), pages.annuaire(), pages.documents(),
        pages.pro(), pages.acces(), pages.contact(), *pages.legal()]
docs.append(pages.sitemap(list(core.PAGES)))
docs.append(pages.notfound())
docs, assistant_data = build_assistant_index(docs, core.PAGES)

with open(os.path.join(OUT, "assets", "assistant-index.json"), "w", encoding="utf-8") as fh:
    json.dump(assistant_data, fh, ensure_ascii=False, separators=(",", ":"))

for path, html in docs:
    f = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(html)

class SearchContent(HTMLParser):
    """Indexe le contenu principal et les vrais liens téléphone, sans l’en-tête."""
    def __init__(self, source):
        super().__init__()
        self.in_main = False
        self.text = []
        self.phones = []
        self.rows = []
        self.row = None
        self.cell = None
        self.anchor = ""
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.in_main = True
        if not self.in_main:
            return
        href = attrs.get("href", "")
        if tag == "a" and href.startswith("tel:"):
            phone = href[4:]
            if phone not in self.phones:
                self.phones.append(phone)
        if tag == "tbody":
            self.anchor = attrs.get("id", "")
        if tag == "tr" and "data-row" in attrs:
            self.row = []
        if tag in ("th", "td") and self.row is not None:
            self.cell = []

    def handle_data(self, value):
        if self.in_main:
            self.text.append(value)
        if self.cell is not None:
            self.cell.append(value)

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None:
            self.row.append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        if tag == "tr" and self.row is not None:
            self.rows.append((self.anchor, self.row))
            self.row = None
        if tag == "main":
            self.in_main = False


content = {path: SearchContent(html) for path, html in docs}
index = []
for pg in core.PAGES:
    if pg["u"] == "404.html":
        continue
    item = {k: v for k, v in pg.items() if k != "g"}
    item["b"] = " ".join(" ".join(content[pg["u"]].text).split())
    item["p"] = content[pg["u"]].phones
    index.append(item)

# Chaque consultation peut être retrouvée par sa spécialité ou son médecin.
for anchor, row in content["services/consultations.html"].rows:
    if len(row) != 4:
        continue
    specialty, doctor, schedule, phone = row
    index.append({"t": f"{specialty} — {doctor}",
                  "u": "services/consultations.html" + ("#" + anchor if anchor else ""),
                  "d": f"{schedule} · Rendez-vous : {phone}", "l": "soins",
                  "k": "consultation specialiste medecin rendez vous rdv", "p": [phone]})

# Annuaire ajouté à l’index de recherche, ligne par ligne.
for t, l, rows in pages.BOOK:
    for n, ph in rows:
        index.append({"t": n, "u": "annuaire.html", "d": ph, "l": l, "k": "telephone numero", "p": [ph]})
with open(os.path.join(OUT, "assets", "search-index.js"), "w", encoding="utf-8") as fh:
    fh.write("window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";")

shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True)
with open(os.path.join(OUT, "robots.txt"), "w") as fh:
    fh.write("User-agent: *\nDisallow: /\n")

print(len(docs), "pages générées")

"""Gabarit commun : en-tête, navigation, pied, composants."""
import html, json, re

SITE_NAME = "Centre Hospitalier de la Tour Blanche"
UP = "https://www.ch-issoudun.fr/wp-content/uploads/"
OFFICIAL = "https://www.ch-issoudun.fr/"

# Bandeau d'information temporaire : mettre None pour le masquer.
ALERT = None
# Bandeau de maquette : à retirer pour une mise en production validée.
PROTOTYPE = True

ICON = {
 "chev": '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 4l4.5 4.5L10.5 4" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>',
 "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5L21 21" stroke="currentColor" stroke-width="2.2"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5l3 .6 1.3 4.4-2 1.7a12 12 0 0 0 5 5l1.7-2 4.4 1.3.6 3c.1.8-.4 1.6-1.3 1.8C11.700 20.700 3.300 12.300 4.700 4.800c.2-.9 1-1.400 1.900-1.300z" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
 "cross": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z" fill="currentColor"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2.2"/></svg>',
 "doc": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2.500h8.500L19 7v14.500H6z M14 3v5h5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
 "ext": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v6H5V7h6" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
}
LOGO = '<img class="brand-logo" src="/assets/images/logo-hopital.jpg" alt="" width="650" height="480">'

def e(s): return html.escape(str(s), quote=True)

def digits(n):
    d = re.sub(r"\D", "", n)
    return "+33" + d[1:] if len(d) == 10 and d.startswith("0") else d

def tel(n, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="tel:{digits(n)}"><span class="nowrap tn">{e(n)}</span></a>'

def doc(label, url, note=""):
    n = f"<small>{e(note)}</small>" if note else ""
    u = url if url.startswith("http") or url.startswith("/") else UP + url
    icon = ICON["doc"] if u.lower().endswith((".pdf", ".jpg", ".png")) else ICON["ext"]
    return f'<li><a href="{u}">{icon}<span>{e(label)}{n}</span></a></li>'

def docs(*items):
    return '<ul class="docs">' + "".join(doc(*i) for i in items) + "</ul>"

def ul(*items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def team(*pairs):
    return '<dl class="team">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in pairs) + "</dl>"

def steps(*items):
    return '<ol class="steps">' + "".join(
        f"<li><b>{i[0]}</b>{i[1]}</li>" if isinstance(i, tuple) else f"<li>{i}</li>" for i in items) + "</ol>"

def stations(items, line=None):
    """items : (titre, url) ou (titre, url, note)"""
    out = []
    for it in items:
        note = f'<span class="off">{e(it[2])}</span>' if len(it) > 2 else ""
        out.append(f'<li><a href="{it[1]}">{e(it[0])}</a>{note}</li>')
    c = f' l-{line}' if line else ""
    return f'<ul class="stations{c}">' + "".join(out) + "</ul>"

NAV = [
 ("soins", "Soins et services", "/services/index.html", "soins", [
   ("Hospitalisation", "/services/index.html#hospitalisation", "soins", [
     ("Médecine polyvalente", "/services/medecine-polyvalente.html"),
     ("Médecine aiguë gériatrique", "/services/medecine-geriatrique.html"),
     ("Hôpital de jour médecine", "/services/hopital-de-jour.html"),
     ("Soins de suite polyvalents", "/services/soins-de-suite-polyvalents.html"),
     ("Soins de suite gériatriques", "/services/soins-de-suite-geriatriques.html")]),
   ("Rééducation", "/services/index.html#readaptation", "read", [
     ("Médecine physique et réadaptation", "/services/mpr.html"),
     ("Hôpital de jour MPR", "/services/hopital-de-jour-mpr.html"),
     ("Équipe mobile de réadaptation", "/services/equipe-mobile.html")]),
   ("Consultations et examens", "/services/index.html#consultations", "soins", [
     ("Consultations de spécialistes", "/services/consultations.html"),
     ("Imagerie médicale", "/services/imagerie.html"),
     ("Pharmacie", "/services/pharmacie.html"),
     ("Accès aux soins (PASS)", "/services/pass.html")]),
   ("Femmes et naissance", "/services/index.html#naissance", "nais", [
     ("Centre périnatal de proximité", "/services/centre-perinatal.html"),
     ("Centre de santé sexuelle", "/services/sante-sexuelle.html")]),
 ]),
 ("age", "Grand âge", "/services/ehpad.html", "age", [
   ("Vivre en EHPAD", "/services/ehpad.html", "age", [
     ("Comparer les résidences", "/services/ehpad.html"),
     ("Bel Air et Les Mésanges", "/services/ehpad-bel-air.html"),
     ("Les Reflets d’Argent", "/services/ehpad-reflets-argent.html"),
     ("Vie quotidienne", "/hebergement/vie-quotidienne.html")]),
   ("Rester à domicile", "/services/index.html#grand-age", "age", [
     ("Soins infirmiers à domicile (SSIAD)", "/services/ssiad.html"),
     ("La Parenthèse, accueil de jour", "/services/la-parenthese.html"),
     ("Équipe spécialisée Alzheimer", "/services/esa.html")]),
   ("Démarches", "/hebergement/admission.html", "age", [
     ("Demander une admission", "/hebergement/admission.html"),
     ("Tarifs et aides", "/hebergement/tarifs-aides.html"),
     ("Organismes à prévenir", "/hebergement/organismes.html")]),
 ]),
 ("parcours", "Votre parcours", "/parcours/index.html", "inst", [
   ("Avant", "/parcours/index.html", "inst", [
     ("Préparer votre venue", "/parcours/preparer-venue.html"),
     ("Venir à l’hôpital", "/acces.html")]),
   ("Pendant", "/parcours/index.html", "inst", [
     ("Votre séjour", "/parcours/sejour.html"),
     ("Visites et proches", "/parcours/visites.html"),
     ("Appui social", "/parcours/appui-social.html")]),
   ("Après", "/parcours/index.html", "inst", [
     ("Votre sortie", "/parcours/sortie.html"),
     ("Frais et facturation", "/parcours/frais.html"),
     ("Dossier médical", "/parcours/dossier-medical.html"),
     ("Vos droits", "/parcours/droits.html")]),
 ]),
 ("prev", "Prévention", "/prevention/index.html", "prev", [
   ("Santé publique", "/prevention/index.html", "prev", [
     ("Reconnaître un AVC", "/prevention/avc.html"),
     ("Vigilance canicule", "/prevention/canicule.html"),
     ("Risques numériques", "/prevention/risques-numeriques.html"),
     ("Développement durable", "/prevention/developpement-durable.html")]),
 ]),
 ("car", "Carrières", "/carrieres/index.html", "prev", [
   ("Travailler ici", "/carrieres/index.html", "prev", [
     ("Offres d’emploi", "/carrieres/index.html"),
     ("Nouveaux arrivants", "/carrieres/nouveaux-arrivants.html")]),
   ("Se former", "/carrieres/ifas.html", "prev", [
     ("Devenir aide-soignant (IFAS)", "/carrieres/ifas.html"),
     ("Stages", "/carrieres/stages.html"),
     ("Formation médicale continue", "/carrieres/formation-continue.html")]),
 ]),
 ("hop", "L’hôpital", "/hopital/index.html", "inst", [
   ("L’établissement", "/hopital/index.html", "inst", [
     ("Présentation", "/hopital/index.html"),
     ("Organisation et instances", "/hopital/organisation.html"),
     ("Qualité et sécurité des soins", "/hopital/qualite.html"),
     ("Projet d’établissement", "/hopital/projet.html")]),
   ("S’informer", "/actualites/index.html", "inst", [
     ("Actualités", "/actualites/index.html"),
     ("Centre de documents", "/documents.html"),
     ("Espace professionnels", "/professionnels.html")]),
 ]),
]

def nav_html(active):
    out = ['<nav class="nav" id="nav" aria-label="Navigation principale"><ul class="nav-list">']
    for key, label, url, line, cols in NAV:
        cur = ' aria-current="true"' if key == active else ""
        col_html = ""
        for t, u, l, items in cols:
            col_html += (f'<div class="ln l-{l}"><h3><a href="{u}">{e(t)}</a></h3>'
                         + stations(items) + "</div>")
        out.append(
            f'<li class="l-{line}"><button class="nav-btn" type="button" aria-expanded="false" '
            f'aria-controls="m-{key}"{cur}>{e(label)}{ICON["chev"]}</button>'
            f'<div class="mega" id="m-{key}"><div class="mega-in">{col_html}</div></div></li>')
    out.append("</ul></nav>")
    return "".join(out)

def head_html(active):
    prefs = ('<div class="prefs" id="prefs"><h2>Confort de lecture</h2>'
             '<fieldset><legend>Taille du texte</legend><div class="seg">'
             '<button type="button" data-size-set="normal">A</button>'
             '<button type="button" data-size-set="large" style="font-size:1.12em">A</button>'
             '<button type="button" data-size-set="xlarge" style="font-size:1.28em">A</button></div></fieldset>'
             '<fieldset><legend>Contraste</legend><div class="seg">'
             '<button type="button" data-contrast-set="normal">Standard</button>'
             '<button type="button" data-contrast-set="high">Renforcé</button></div></fieldset></div>')
    return (
     f'<header class="head"><div class="wrap">'
     f'<a class="brand" href="/index.html" aria-label="Centre Hospitalier de la Tour Blanche, accueil">{LOGO}'
     f'<span><b>Centre Hospitalier<br>de la Tour Blanche</b><i>Issoudun, Indre</i></span></a>'
     f'{nav_html(active)}'
     f'<div class="tools">'
     f'<button class="tool t-search" type="button" data-search aria-label="Rechercher">{ICON["search"]}<span class="lbl">Rechercher</span></button>'
     f'<button class="tool" type="button" data-prefs aria-expanded="false" aria-controls="prefs" aria-label="Confort de lecture">Aa</button>'
     f'<button class="tool menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{ICON["menu"]}</button>'
     f'</div>{prefs}</div></header>')

def top_bars():
    s = ""
    s += ('<div class="urgbar"><div class="wrap">'
          '<span>Urgence vitale : appelez le <a href="tel:15"><b>15</b></a> ou le <a href="tel:112"><b>112</b></a></span>'
          '<span class="right"><a class="opt" href="/urgences.html">Urgences : à partir de 19 h, appelez d’abord le 15</a>'
          '<span>Standard <a href="tel:+33254035403"><b class="tn nowrap">02 54 03 54 03</b></a></span></span>'
          '</div></div>')
    if ALERT:
        s += f'<div class="notice-bar" role="status"><div class="wrap">{ALERT}</div></div>'
    return s

def foot_html():
    return (
     '<footer class="foot"><div class="wrap"><div class="foot-top">'
     f'<div><a class="footer-brand" href="/index.html">{LOGO}<span>Centre Hospitalier<br>de la Tour Blanche</span></a>'
     '<address>Avenue Jean Bonnefont<br>CS 70190<br>36105 Issoudun Cedex</address>'
     '<a class="ftel tn" href="tel:+33254035403">02 54 03 54 03</a></div>'
     '<div><h2>Trouver</h2><ul>'
     '<li><a href="/annuaire.html">Annuaire téléphonique</a></li>'
     '<li><a href="/services/index.html">Tous les services</a></li>'
     '<li><a href="/acces.html">Venir à l’hôpital</a></li>'
     '<li><a href="/contact.html">Nous contacter</a></li></ul></div>'
     '<div><h2>S’informer</h2><ul>'
     '<li><a href="/actualites/index.html">Actualités</a></li>'
     '<li><a href="/documents.html">Centre de documents</a></li>'
     '<li><a href="/hopital/qualite.html">Qualité des soins</a></li>'
     '<li><a href="/professionnels.html">Espace professionnels</a></li></ul></div>'
     '<div><h2>Nous suivre</h2><ul>'
     '<li><a href="https://www.facebook.com/centrehospitalierdelatourblanche/">Facebook</a></li>'
     '<li><a href="https://www.linkedin.com/company/centre-hospitalier-de-la-tour-blanche/">LinkedIn</a></li>'
     '<li><a href="https://www.youtube.com/@chtbchtb2490">YouTube</a></li>'
     '<li><a href="https://twitter.com/CHTB_Issoudun">X (Twitter)</a></li></ul></div>'
     '</div><div class="foot-b"><span>Établissement public de santé</span><ul>'
     '<li><a href="/plan-du-site.html">Plan du site</a></li>'
     '<li><a href="/mentions-legales.html">Mentions légales et données personnelles</a></li>'
     '<li><a href="/accessibilite.html">Accessibilité : non conforme</a></li>'
     '</ul></div>'
     f'<div class="proto">Proposition de refonte · Version 2 · <a href="{OFFICIAL}">Consulter le site officiel actuel</a></div>'
     '</div></footer>')

def mobbar():
    return (
     '<nav class="mobbar" aria-label="Accès rapides">'
     f'<a href="tel:+33254035403">{ICON["phone"]}Appeler</a>'
     f'<a class="u" href="/urgences.html">{ICON["cross"]}Urgences</a>'
     f'<button type="button" data-search>{ICON["search"]}Rechercher</button>'
     f'<button type="button" data-open-menu>{ICON["menu"]}Menu</button></nav>')

SEARCH_DLG = (
 '<dialog class="search" aria-label="Rechercher sur le site"><div class="s-top">'
 f'<span style="width:22px;flex:none">{ICON["search"]}</span>'
 '<input type="search" placeholder="Service, médecin, démarche, numéro" aria-label="Votre recherche" autocomplete="off">'
 '<button type="button" data-close-search>Fermer</button></div>'
 '<ul class="s-res"></ul><p class="s-empty" hidden>Aucun résultat. Essayez un autre mot, ou appelez le standard au '
 '<a href="tel:+33254035403">02 54 03 54 03</a>.</p></dialog>')

JSONLD = json.dumps({
 "@context": "https://schema.org", "@type": "Hospital", "name": SITE_NAME,
 "telephone": "+33254035403", "email": "contact@ch-issoudun.fr",
 "address": {"@type": "PostalAddress", "streetAddress": "Avenue Jean Bonnefont, CS 70190",
             "postalCode": "36105", "addressLocality": "Issoudun", "addressCountry": "FR"},
 "openingHours": "Mo-Su 00:00-24:00", "medicalSpecialty": ["Emergency", "Geriatric", "PhysicalTherapy"],
}, ensure_ascii=False)

NB = "\u00a0"
def typo(s):
    """Espaces insécables françaises, hors balises."""
    def fix(m):
        t = m.group(0)
        t = re.sub(r"(\d{1,2}) h (\d{2})\b", rf"\1{NB}h{NB}\2", t)
        t = re.sub(r"(\d{1,2}) h\b", rf"\1{NB}h", t)
        t = re.sub(r" ([:;?!%€»])", rf"{NB}\1", t)
        t = t.replace("« ", "«" + NB)
        t = re.sub(r"(\d) (lits|places|ans|km|mois|jours|semaines)\b", rf"\1{NB}\2", t)
        return t
    return re.sub(r">[^<]+<", fix, s)

PAGES = []   # (path, title, description, line, group, keywords)

def page(path, title, desc, body, *, line="inst", active="", crumbs=None, group="", kw="", index=True, head=None, raw_title=None):
    """Écrit une page. `body` utilise des URL absolues depuis la racine (/...)."""
    depth = path.count("/")
    pre = "../" * depth
    body = typo(body)
    head = typo(head) if head else head
    if index:
        PAGES.append({"t": title, "u": path, "d": desc, "l": line, "g": group, "k": kw})
    full_title = raw_title or f"{title} | {SITE_NAME}, Issoudun"
    doc_html = f"""<!doctype html>
<html lang="fr" data-base="{pre}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#102f4a">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://ch-tour-blanche-seconde-version.florouss.chatgpt.site/assets/images/hopital.jpg">
<meta property="og:locale" content="fr_FR">
<link rel="icon" href="/assets/images/logo-hopital.jpg" type="image/jpeg">
<link rel="preload" href="/assets/fonts/manrope-400.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/warm.css">
<link rel="stylesheet" href="/assets/assistant.css">
<script>try{{var h=document.documentElement,s=localStorage.getItem('chtb:size'),c=localStorage.getItem('chtb:contrast');if(s&&s!='normal')h.setAttribute('data-size',s);if(c&&c!='normal')h.setAttribute('data-contrast',c)}}catch(e){{}}</script>
<script type="application/ld+json">{JSONLD}</script>
</head>
<body class="l-{line}">
<a class="skip" href="#contenu">Aller au contenu</a>
{top_bars()}
{head_html(active)}
<main id="contenu" tabindex="-1">
{head or ''}{body}
</main>
{foot_html()}
{mobbar()}
{SEARCH_DLG}
<script src="/assets/search-index.js"></script>
<script src="/assets/site.js"></script>
<script src="/assets/assistant-engine.js" defer></script>
<script src="/assets/assistant-ui.js" defer></script>
</body>
</html>
"""
    doc_html = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{pre}', doc_html)
    return path, doc_html

def phead(title, lead="", crumbs=None, tag=""):
    c = ""
    if crumbs is not None:
        items = '<li><a href="/index.html">Accueil</a></li>'
        for t, u in crumbs:
            items += f'<li><a href="{u}">{e(t)}</a></li>'
        items += f'<li aria-current="page">{e(title)}</li>'
        c = f'<nav class="crumb" aria-label="Fil d’Ariane"><ol>{items}</ol></nav>'
    t = f'<div class="tag">{e(tag)}</div>' if tag else ""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="phead"><div class="wrap">{c}{t}<h1>{e(title)}</h1>{l}</div></div>'

def body(main, aside=None):
    if aside is None:
        return f'<div class="wrap body full"><div class="prose">{main}</div></div>'
    return (f'<div class="wrap body"><div class="prose">{main}</div>'
            f'<aside class="aside" aria-label="Fiche pratique">{aside}</aside></div>')

def fiche(rows, documents=None, title="L’essentiel"):
    """rows : (terme, html). Le téléphone principal passe par bigtel()."""
    d = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows)
    x = f"<dt>Documents</dt><dd>{documents}</dd>" if documents else ""
    return f"<h2>{e(title)}</h2><dl>{d}{x}</dl>"

def bigtel(n): return tel(n, "bigtel")

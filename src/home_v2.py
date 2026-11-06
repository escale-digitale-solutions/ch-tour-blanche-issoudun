"""Accueil de la seconde proposition, construit sur le contenu de la maquette fournie."""
from core import page, ICON, e


def pictogram(name):
    paths = {
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 11h18m-14 4h3m4 0h3m-10 3h3"/>',
        "bag": '<rect x="3" y="7" width="18" height="14" rx="3"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m-4 5v5m-2.5-2.5h5"/>',
        "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',
        "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.8"/>',
        "care": '<path d="M6 3v5a4 4 0 0 0 8 0V3M4 3h4m4 0h4m-6 9v3a5 5 0 0 0 10 0v-3"/><circle cx="20" cy="9" r="3"/>',
        "move": '<circle cx="14" cy="4" r="2"/><path d="m7 11 4-4 4 3 5 1m-9-4-2 7 4 3 1 5m-5-8-4 7"/>',
        "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V10Zm6 11v-8h6v8"/>',
        "people": '<circle cx="9" cy="7" r="4"/><path d="M2 21v-3a6 6 0 0 1 6-6h2a6 6 0 0 1 6 6v3m1-17a4 4 0 0 1 0 8m2 3a5 5 0 0 1 3 5v1"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def home():
    from pages import NEWS
    arrow = ICON["arrow"]
    quick = [
        ("calendar", "Prendre rendez-vous", "Consulter un spécialiste", "/services/consultations.html"),
        ("bag", "Préparer mon séjour", "Les étapes et les documents utiles", "/parcours/preparer-venue.html"),
        ("heart", "Rendre visite", "Horaires et accueil des proches", "/parcours/visites.html"),
        ("pin", "Venir à l’hôpital", "Adresse, accès et plan du site", "/acces.html"),
    ]
    quick_html = "".join(f'<a class="quick-card" href="{u}"><span class="quick-icon">{pictogram(ic)}</span><h2>{t}</h2><p>{d}</p>{arrow}</a>' for ic,t,d,u in quick)
    care = [
        ("care", "soins", "Consultations & examens", "Des spécialistes et un plateau d’imagerie pour votre suivi, près de chez vous.", "/services/consultations.html"),
        ("bag", "soins", "Médecine & hospitalisation", "Médecine polyvalente, gériatrie, hôpital de jour : un accompagnement adapté à votre parcours.", "/services/index.html#hospitalisation"),
        ("move", "read", "Rééducation & réadaptation", "Des équipes spécialisées pour retrouver de l’autonomie, à l’hôpital et au-delà.", "/services/mpr.html"),
        ("home", "age", "Grand âge & autonomie", "EHPAD, accueil de jour et soins à domicile : des solutions pour vous et vos proches.", "/services/ehpad.html"),
    ]
    care_html = "".join(f'<a class="care-card l-{line}" href="{u}"><div class="care-copy"><span class="quick-icon">{pictogram(ic)}</span><h3>{t}</h3><p>{d}</p><span class="link-arrow">Découvrir {arrow}</span></div></a>' for ic,line,t,d,u in care)
    news_html = ""
    news_images = [("patrimoine.jpg", "La cour et les bâtiments du Centre Hospitalier", "Vie de l’hôpital"), ("sorties-velo.jpg", "Une sortie en vélo adapté avec une animatrice de l’EHPAD", "Vie des résidents"), ("hopital.jpg", "Le Centre Hospitalier de la Tour Blanche à Issoudun", "Dans la presse")]
    for n, (im, alt, tag) in zip(NEWS[:3], news_images):
        news_html += f'<article class="home-news"><a class="news-visual" href="/actualites/{n[0]}.html" tabindex="-1" aria-hidden="true"><img src="/assets/images/{im}" alt="" width="1024" height="684" loading="lazy"><span>{tag}</span></a><div class="news-copy"><time datetime="{n[2]}">{n[1]}</time><h3><a href="/actualites/{n[0]}.html">{e(n[3])}</a></h3><p>{e(n[4])}</p><a class="link-arrow" href="/actualites/{n[0]}.html" aria-label="Lire : {e(n[3])}">Lire l’article {arrow}</a></div></article>'
    b = f'''
<section class="home-hero"><div class="wrap hero-grid">
 <div class="hero-copy"><p class="eyebrow">HÔPITAL PUBLIC · ISSOUDUN, INDRE</p>
  <h1>Proches de vous.<br><em>Attentifs à chacun.</em></h1>
  <p class="lead">Soigner, accompagner, rassurer. À Issoudun, les équipes de la Tour Blanche prennent soin de vous et de vos proches.</p>
  <div class="hero-actions"><a class="btn" href="/services/index.html">Trouver un service {arrow}</a><a class="btn ghost" href="/parcours/index.html">Votre parcours patient {arrow}</a></div>
  <p class="hero-note">Un hôpital de proximité, au cœur du Berry.</p>
  <div class="hero-tags" aria-label="Nos missions"><span>Soins de proximité</span><span>Rééducation</span><span>Grand âge</span></div>
 </div>
 <div class="hero-media">
  <figure class="hero-main"><img src="/assets/images/equipes-prevention.jpg" alt="Deux professionnelles de l’hôpital accueillent un visiteur à un stand d’éducation thérapeutique" width="2048" height="1365" fetchpriority="high"><figcaption class="photo-caption"><span>Semaine de l’éducation thérapeutique</span><strong>Écouter, expliquer, accompagner.</strong></figcaption></figure>
  <figure class="hero-inset"><img src="/assets/images/hopital.jpg" alt="Le pavillon Marie Curie du Centre Hospitalier de la Tour Blanche" width="1024" height="684"><figcaption>Ici, à Issoudun</figcaption></figure>
  <span class="hero-stamp" aria-hidden="true">À vos côtés<br>chaque jour</span>
 </div>
</div></section>
<div class="wrap"><section class="quick-grid" aria-label="Vos démarches en un clic">{quick_html}</section></div>

<section class="home-section"><div class="wrap">
 <div class="service-finder"><div><h2>Comment pouvons-nous vous aider ?</h2><p>Un service, un médecin, une démarche…</p></div><form class="herosearch" data-hero-search role="search"><label class="visually-hidden" for="home-q">Rechercher dans le site</label><input id="home-q" type="search" placeholder="Que recherchez-vous ?"><button type="submit" aria-label="Lancer la recherche">{ICON["search"]}</button></form></div>
 <div class="section-heading"><div><p class="eyebrow">NOTRE OFFRE DE SOINS</p><h2>Le bon accompagnement,<br>au bon moment.</h2></div><a class="link-arrow" href="/services/index.html">Tous nos services {arrow}</a></div>
 <div class="care-grid">{care_html}</div>
 <div class="care-extra"><p>Et aussi, à vos côtés :</p><a href="/services/centre-perinatal.html">Grossesse & périnatalité {arrow}</a><a href="/services/sante-sexuelle.html">Santé sexuelle {arrow}</a><a href="/services/pass.html">Accès aux soins pour tous {arrow}</a></div>
</div></section>

<section class="home-section story-section"><div class="wrap hospital-story">
 <figure><img src="/assets/images/jardin.jpg" alt="Les jardins du Centre Hospitalier de la Tour Blanche" width="1024" height="684" loading="lazy"><figcaption>Un lieu de soins, un lieu de vie.</figcaption></figure>
 <div class="story-copy"><p class="eyebrow">UN HÔPITAL ANCRÉ DANS SON TERRITOIRE</p><h2>La proximité fait<br>partie du soin.</h2><p>Au cœur du bassin d’Issoudun, le Centre Hospitalier de la Tour Blanche associe médecine, rééducation et accompagnement du grand âge.</p><p>Un établissement public à taille humaine, en lien avec les professionnels de santé du Berry et de la région Centre-Val de Loire.</p><a class="link-arrow" href="/hopital/index.html">Découvrir notre hôpital {arrow}</a><div class="story-links"><a href="/hopital/qualite.html">Qualité & sécurité des soins</a><a href="/hopital/projet.html">Notre projet d’établissement</a></div></div>
</div></section>

<section class="home-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">LA VIE DE L’ÉTABLISSEMENT</p><h2>Au fil de l’hôpital.</h2></div><a class="link-arrow" href="/actualites/index.html">Toutes les actualités {arrow}</a></div><div class="home-news-grid">{news_html}</div></div></section>

<section class="wrap careers-banner"><div class="careers-copy"><p class="eyebrow">DONNEZ DU SENS À VOTRE MÉTIER</p><h2>Votre avenir s’écrit<br>aussi à nos côtés.</h2><p>Soignants, médecins, professionnels techniques ou administratifs : découvrez nos métiers, nos formations et nos opportunités.</p><a class="btn" href="/carrieres/index.html">Rejoindre nos équipes {arrow}</a></div><div class="careers-aside"><span class="quick-icon">{pictogram("people")}</span><h3>Apprendre. Soigner. Avancer.</h3><a href="/carrieres/ifas.html">Se former au métier d’aide-soignant {arrow}</a><a href="/carrieres/stages.html">Faire un stage à l’hôpital {arrow}</a><a href="/professionnels.html">Espace professionnels de santé {arrow}</a></div></section>

<section class="home-contact"><div class="wrap"><div><p class="eyebrow">BESOIN D’ÊTRE ORIENTÉ ?</p><h2>Nous sommes là pour vous guider.</h2></div><a href="tel:+33254035403" class="contact-number">{ICON["phone"]}02 54 03 54 03<span>Standard de l’hôpital</span></a><a class="link-arrow" href="/annuaire.html">L’annuaire des services {arrow}</a></div></section>
'''
    return page("index.html", "Accueil", "Centre Hospitalier de la Tour Blanche à Issoudun : soins, consultations, rééducation, grand âge et informations pratiques pour les patients et leurs proches.", b, line="soins", raw_title="Centre Hospitalier de la Tour Blanche — Issoudun", kw="accueil")

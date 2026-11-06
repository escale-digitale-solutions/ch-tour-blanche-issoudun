"""Pages transverses : accueil, urgences, parcours, hébergement, prévention, hôpital, etc."""
from core import *

MC = "Pavillon Marie Curie"
A = ICON["arrow"]

def p(path, title, lead, main, aside=None, line="inst", active="", crumbs=None, tag="", kw="", head=None):
    h = head or phead(title, lead, crumbs if crumbs is not None else [], tag)
    return page(path, title, re.sub("<[^>]+>", "", lead), body(main, aside), line=line, active=active, group=tag, kw=kw, head=h)

# ---------- Accueil
LEVELS = [
 ("2", "2e étage", [("Médecine polyvalente", "/services/medecine-polyvalente.html", "02 54 03 54 06", "soins")]),
 ("1", "1er étage", [("Médecine aiguë gériatrique", "/services/medecine-geriatrique.html", "02 54 03 63 18", "soins"),
                     ("Hôpital de jour médecine", "/services/hopital-de-jour.html", "02 54 03 63 18", "soins"),
                     ("Soins de suite", "/services/soins-de-suite-polyvalents.html", "02 54 03 54 04", "soins")]),
 ("0", "Rez-de-chaussée", [("Urgences et SMUR", "/urgences.html", "02 54 03 54 00", "urg"),
                     ("Consultations", "/services/consultations.html", "02 54 03 55 06", "soins"),
                     ("Centre périnatal, santé sexuelle", "/services/centre-perinatal.html", "02 54 03 54 15", "nais"),
                     ("Accueil et standard", "/contact.html", "02 54 03 54 03", "inst")]),
 ("-1", "Sous-sol", [("Imagerie médicale", "/services/imagerie.html", "02 54 03 63 99", "soins"),
                     ("Pharmacie", "/services/pharmacie.html", "02 54 03 52 00", "soins")]),
]

def totem():
    rows = ""
    for n, name, items in LEVELS:
        lis = "".join(f'<li><a data-c="{c}" href="{u}"><span>{e(t)}</span><em class="tn">{e(ph)}</em></a></li>' for t, u, ph, c in items)
        rows += f'<div class="level"><div class="level-n" aria-label="{e(name)}">{e(n.replace("-", "−"))}</div><ul>{lis}</ul></div>'
    return f'<section class="totem" aria-labelledby="t-h"><div class="totem-h"><h2 id="t-h">Pavillon Marie Curie</h2><span><a href="/acces.html" style="color:#fff">Tous les niveaux</a></span></div>{rows}</section>'

NEWS = [
 ("concert-chorale", "5 juin 2026", "2026-06-05", "Concert de la chorale du Conservatoire d’Issoudun", "La chorale variétés a donné une représentation gratuite et ouverte à tous dans la cour d’honneur, le samedi 13 juin à 15 h.", "inst",
  "<p>La chorale variétés du Conservatoire municipal d’Issoudun a donné une représentation gratuite et ouverte à tous le samedi 13 juin à 15 h, dans la cour d’honneur de l’hôpital.</p><p>En cas de mauvais temps, le concert était prévu dans la salle d’animation de l’EHPAD Les Reflets d’Argent.</p>"),
 ("sorties-velo", "20 avril 2026", "2026-04-20", "48 résidents des Reflets d’Argent à vélo dans Issoudun", "Grâce au prêt gracieux du Département de l’Indre, les animatrices ont organisé 66 sorties en vélo adapté.", "age",
  "<p>L’EHPAD Les Reflets d’Argent a organisé des sorties en vélo adapté, grâce à un prêt gracieux du Département de l’Indre. Quel que soit leur degré de dépendance, 48 résidents volontaires y ont participé.</p><p>Mme Rouzet et Mme Raimondi, animatrices de l’établissement, ont organisé 66 sorties, sur deux parcours d’environ 6 km mêlant ville et campagne. Une opération similaire était prévue début juin avec les résidents de l’EHPAD Bel Air.</p>"),
 ("pont-sanitaire", "6 mars 2026", "2026-03-06", "Un « pont sanitaire » dans le paysage médical berrichon", "La Nouvelle République consacre une enquête à la place de l’hôpital entre Bourges et Châteauroux.", "inst",
  "<p><em>La Nouvelle République de l’Indre</em> a publié une série sur la carte sanitaire du Berry. Marc Kugelstadt, directeur, et le Dr Laurent Minois, urgentiste et président de la Commission médicale d’établissement, y présentent le rôle de l’hôpital, à égale distance de Bourges et de Châteauroux.</p><p>L’établissement s’appuie sur un réseau régional pour délivrer les bons soins, au bon endroit, au bon moment. Le nombre de praticiens a doublé en cinq ans.</p>"),
 ("portes-ouvertes-ifas", "6 février 2026", "2026-02-06", "Portes ouvertes de l’IFAS d’Issoudun", "Le public a pu rencontrer l’équipe pédagogique et les élèves, le samedi 7 février, de 10 h à 16 h.", "prev",
  '<p>L’Institut de formation des aides-soignants d’Issoudun a ouvert ses portes le samedi 7 février, de 10 h à 16 h. Le public a pu rencontrer l’équipe pédagogique et les élèves pour découvrir le métier d’aide-soignant.</p><p>Retrouvez les informations sur <a href="/carrieres/ifas.html">la formation et les inscriptions</a>.</p>'),
 ("bilan-2025", "22 janvier 2026", "2026-01-22", "Bilan 2025 et perspectives 2026", "Le directeur revient sur le retour du SMR dans ses locaux, l’activité, la certification et le schéma directeur immobilier.", "inst",
  '<p>Invité du Bip Info du 21 janvier 2026, Marc Kugelstadt, directeur, a présenté le bilan de l’année.</p><ul><li><strong>Locaux du SMR :</strong> reprise de l’activité en conditions normales au premier trimestre 2025, après d’importants travaux.</li><li><strong>Activité :</strong> soutenue, en progression régulière depuis la période post-Covid.</li><li><strong>Certification :</strong> l’hôpital n’a pas été certifié. Un plan d’action est en cours et la prochaine visite est prévue en 2027.</li><li><strong>Schéma directeur immobilier :</strong> validé par l’ARS, il fixe une vision à long terme pour l’ensemble de l’établissement.</li><li><strong>Formation :</strong> l’hôpital accueille régulièrement internes et externes.</li></ul><p><a href="https://www.youtube.com/watch?v=fe8cs_V4E-M">Voir l’entretien sur YouTube</a></p>'),
 ("photobiomodulation", "3 décembre 2025", "2025-12-03", "Photobiomodulation : une nouvelle offre à l’hôpital de jour", "Une solution non invasive pour traiter les mucites liées à la chimiothérapie, sous la supervision du Dr Cherkaoui.", "soins",
  f'<p>L’hôpital de jour médecine propose désormais des séances de photobiomodulation, pour traiter les mucites chimio-induites : une complication fréquente des traitements, qui provoque des douleurs intenses et des difficultés à s’alimenter.</p><p>Cette technique non invasive vise à réduire l’inflammation, soulager la douleur et accélérer la cicatrisation des muqueuses buccales. Le Dr Adil Cherkaoui, oncologue, supervise cette activité. Les soins sont proposés selon le protocole de chimiothérapie suivi.</p><p>Contact : <a href="/services/hopital-de-jour.html">hôpital de jour</a>, {tel("02 54 03 63 18")}.</p>'),
 ("la-parenthese", "23 mai 2025", "2025-05-23", "L’accueil de jour Alzheimer devient La Parenthèse", "Le nouveau nom a été dévoilé le 22 mai, lors d’une cérémonie et d’une journée portes ouvertes.", "age",
  '<p>Ouvert en septembre 2015, l’accueil de jour Alzheimer et maladies apparentées s’appelle désormais La Parenthèse. La démarche a commencé en 2024 avec les personnes accueillies, puis un vote a retenu ce nom.</p><p>Il dit ce que le service veut offrir : un temps et un lieu de répit, de soutien et de bien-être, pour les personnes accueillies comme pour leurs proches.</p><p><a href="/services/la-parenthese.html">Découvrir La Parenthèse</a></p>'),
 ("retour-mpr", "16 avril 2025", "2025-04-16", "La rééducation retrouve ses locaux", "La directrice générale de l’ARS a visité le service le 10 avril, après trois ans de travaux et de procédures.", "read",
  '<p>Le service de médecine physique et de réadaptation a réintégré ses locaux après d’importants travaux. Surveillées depuis 2018, des fissures avaient conduit à fermer l’aile concernée en 2022, pour la sécurité du public. Les équipes ont maintenu l’activité presque au même niveau pendant cette période.</p><p>Clara de Bort, directrice générale de l’ARS, Elsa Livonnet, directrice de la délégation départementale de l’Indre, et André Laignel, président du conseil de surveillance, ont visité le service le 10 avril 2025.</p>'),
]

def news_item(n):
    return (f'<li class="l-{n[5]}"><time datetime="{n[2]}">{n[1]}</time><h3><a href="/actualites/{n[0]}.html">{e(n[3])}</a></h3><p>{e(n[4])}</p></li>')

def home():
    from home_v2 import home as redesigned_home
    return redesigned_home()

# ---------- Urgences
def urgences():
    m = ('<ul class="nums">'
      '<li><a class="u" href="tel:15"><b>15</b><span>SAMU, urgence médicale</span></a></li><li><a class="u" href="tel:112"><b>112</b><span>Numéro d’urgence européen</span></a></li>'
      '<li><a href="tel:18"><b>18</b><span>Pompiers</span></a></li><li><a href="tel:17"><b>17</b><span>Gendarmerie</span></a></li></ul>'
      '<div class="callout warn"><h3>À partir de 19 h, appelez d’abord le 15</h3><p>Ne vous présentez pas directement aux urgences : vous devez d’abord être orienté par la régulation du 15.</p></div>'
      '<h2>Votre arrivée aux urgences</h2>' + steps(("Présentez-vous à l’accueil", " avec une pièce d’identité, vos coordonnées, votre carte Vitale et vos justificatifs de mutuelle."), ("Expliquez le motif de votre venue.", " Votre état est évalué dès l’accueil."), ("Vous êtes orienté", " vers une salle de soins ou la salle d’attente."), ("Vous recevez les soins et les premiers examens.", " L’équipe décide ensuite de la suite : retour à domicile, hospitalisation en médecine polyvalente ou gériatrique, ou transfert vers un autre établissement."))
      + '<h2>Pourquoi l’attente peut varier</h2><p>L’ordre de passage peut différer de l’ordre d’arrivée. Les patients sont pris en charge selon la gravité évaluée à l’accueil, et le service reçoit aussi les patients adressés par le SAMU.</p>'
      + '<h2>L’équipe</h2>' + team(("Cheffe de service", "Dr Moreau"), ("Cadre de santé", "M. Piedois"), ("Médecins", "Neuf médecins"), ("Soignants", "Infirmiers, aides-soignants, agents hospitaliers, brancardiers, agents d’accueil"))
      + f'<h2>Autres numéros utiles</h2><p>Centre antipoison : {tel("02 41 48 21 21")}</p>')
    a = fiche([("Urgences", bigtel("02 54 03 54 00")), ("Ouverture", "24 h sur 24, 7 jours sur 7. À partir de 19 h, passez d’abord par le 15"), ("Où", f"{MC}, rez-de-chaussée. Accès piétons et ambulances séparés et signalés"), ("Hélicoptère", "Station héliportée sur le site")],
              docs(("Questionnaire de satisfaction", "2021/12/questionnaires_urgences_2017.pdf")))
    return p("urgences.html", "Urgences et SMUR", "Le service est ouvert 24 h sur 24. À partir de 19 h, appelez d’abord le 15. En cas de danger vital, appelez le 15 ou le 112.", m, a, line="urg", active="soins", tag="Urgences", kw="samu smur urgence nuit 15 112 antipoison moreau")

# ---------- Répertoire
DIR = [
 ("hospitalisation", "Hospitalisation", "soins", [("Médecine polyvalente", "/services/medecine-polyvalente.html", "30 lits, 2e étage", "02 54 03 54 06"), ("Médecine aiguë gériatrique", "/services/medecine-geriatrique.html", "20 lits, 1er étage", "02 54 03 63 18"), ("Hôpital de jour médecine", "/services/hopital-de-jour.html", "Chimiothérapie, bilans, 1er étage", "02 54 03 63 18"), ("Soins de suite polyvalents", "/services/soins-de-suite-polyvalents.html", "20 lits, 1er étage", "02 54 03 54 04"), ("Soins de suite gériatriques", "/services/soins-de-suite-geriatriques.html", "18 lits, 1er étage", "02 54 03 54 04")]),
 ("urgences", "Urgences", "urg", [("Urgences et SMUR", "/urgences.html", "24 h sur 24, rez-de-chaussée", "02 54 03 54 00")]),
 ("readaptation", "Rééducation", "read", [("Médecine physique et réadaptation", "/services/mpr.html", "85 lits, bâtiment MPR", "02 54 03 54 44"), ("Hôpital de jour MPR", "/services/hopital-de-jour-mpr.html", "15 places, bâtiment MPR", "02 54 03 56 05"), ("Équipe mobile de réadaptation du Berry", "/services/equipe-mobile.html", "À domicile, Cher et Indre", "02 54 03 54 31")]),
 ("consultations", "Consultations et examens", "soins", [("Consultations de spécialistes", "/services/consultations.html", "Quinze spécialités", "02 54 03 55 06"), ("Imagerie médicale", "/services/imagerie.html", "Radiologie, scanner, échographie, sous-sol", "02 54 03 63 99"), ("Pharmacie", "/services/pharmacie.html", "Rétrocession au public, sous-sol", "02 54 03 52 00"), ("Accès aux soins (PASS)", "/services/pass.html", "Sans couverture sociale", "02 54 03 54 29"), ("Centre de santé", "/services/centre-de-sante.html", "Activité en veille, pas de rendez-vous", "")]),
 ("naissance", "Femmes et naissance", "nais", [("Centre périnatal de proximité", "/services/centre-perinatal.html", "Grossesse, gynécologie, rez-de-chaussée", "02 54 03 54 15"), ("Centre de santé sexuelle", "/services/sante-sexuelle.html", "Contraception, IVG, dépistage", "02 54 03 54 15")]),
 ("grand-age", "Grand âge", "age", [("EHPAD Bel Air et Les Mésanges", "/services/ehpad-bel-air.html", "86 places, en ville", "02 54 03 54 14"), ("EHPAD Les Reflets d’Argent", "/services/ehpad-reflets-argent.html", "90 places, à l’hôpital", "02 54 03 46 83"), ("Soins infirmiers à domicile (SSIAD)", "/services/ssiad.html", "67 places, à domicile", "02 54 03 17 76"), ("La Parenthèse, accueil de jour Alzheimer", "/services/la-parenthese.html", "10 places", "02 54 03 67 14"), ("Équipe spécialisée Alzheimer", "/services/esa.html", "À domicile", "02 54 03 17 76")]),
]
def services_hub():
    m = '<div class="filter no-print" data-filter-for="dir"><input type="search" placeholder="Filtrer les services" aria-label="Filtrer les services"><span class="count" role="status"></span></div><div id="dir">'
    for id_, t, l, rows in DIR:
        lis = "".join(f'<li data-row><a class="row" href="{u}"><b>{e(n)}</b><span class="s">{e(s)}</span><span class="t tn">{e(ph)}</span></a></li>' for n, u, s, ph in rows)
        m += f'<section id="{id_}" class="l-{l}" data-group><h2 class="dirhead tag" style="font-size:1.4rem;color:var(--ink)">{e(t)}</h2><ul class="dir">{lis}</ul></section>'
    m += '<p class="empty" hidden>Aucun service ne correspond. Appelez le standard au 02 54 03 54 03.</p></div>'
    return p("services/index.html", "Soins et services", "Tous les services de l’hôpital, avec leur numéro direct.", m, active="soins", line="soins", tag="", kw="annuaire services liste specialites")

# ---------- Parcours
PC = [("Votre parcours", "/parcours/index.html")]
def parcours():
    o = []
    hub = (stations([("Préparer votre venue", "/parcours/preparer-venue.html", "Documents et affaires à apporter"), ("Venir à l’hôpital", "/acces.html", "Adresse, plan, niveaux"), ("Votre séjour", "/parcours/sejour.html", "Repas, soins, téléphone, Wi-Fi"), ("Visites et proches", "/parcours/visites.html", "Horaires, repas, nuit sur place"), ("Appui social", "/parcours/appui-social.html", "Retour à domicile, placement"), ("Votre sortie", "/parcours/sortie.html", "Formalités, transport, mineurs"), ("Frais et facturation", "/parcours/frais.html", "Ce qui reste à votre charge"), ("Dossier médical", "/parcours/dossier-medical.html", "Comment obtenir une copie"), ("Vos droits", "/parcours/droits.html", "Personne de confiance, directives anticipées, réclamation")], "soins")
      + '<h2>Donner votre avis</h2><p>Votre avis aide les équipes à progresser.</p>' + docs(("Questionnaire des urgences", "2021/12/questionnaires_urgences_2017.pdf")))
    o.append(p("parcours/index.html", "Votre parcours", "Tout ce qu’il faut savoir, de la préparation de votre venue à votre sortie.", hub, active="parcours", kw="patient hospitalisation"))

    chk = lambda items: "".join(f'<li><label><input type="checkbox"><span>{i}</span></label></li>' for i in items)
    m = ('<form data-checklist="venue"><h2>Votre liste de préparation</h2><p>Cochez ce qui est prêt. La liste reste enregistrée sur cet appareil. <span class="prog" role="status"></span></p>'
      '<h3>Documents</h3><ul class="check">' + chk(["Pièce d’identité en cours de validité (carte d’identité, passeport ou titre de séjour)", "Justificatif de domicile", "Carte Vitale à jour", "Carte de mutuelle", "Attestation de Complémentaire santé solidaire ou d’AME, si vous en bénéficiez", "Vos ordonnances"]) + "</ul>"
      '<h3>Affaires personnelles</h3><ul class="check">' + chk(["Nécessaire de toilette", "Linge personnel. Son entretien revient à votre entourage", "Vos traitements, à remettre à l’infirmier avec l’ordonnance", "Baskets et survêtement, pour la rééducation", "Votre adresse e-mail, pour le questionnaire de satisfaction"]) + "</ul>"
      '<div class="btns no-print"><button type="button" class="btn" data-print>Imprimer ma liste</button><button type="button" class="btn ghost" data-clear>Tout décocher</button></div></form>'
      '<h2>Selon votre situation</h2><div class="tbl-wrap"><table class="tbl"><tbody>'
      '<tr><th scope="row">Mineur</th><td>Livret de famille et autorisation parentale de soins signée par les deux parents ou le tuteur. Copie du jugement si l’autorité parentale a été retirée à un parent.</td></tr>'
      '<tr><th scope="row">Majeur protégé</th><td>Copie du jugement de protection.</td></tr><tr><th scope="row">Accident du travail</th><td>Volet de déclaration d’accident.</td></tr>'
      '<tr><th scope="row">Union européenne</th><td>Carte européenne d’assurance maladie ou certificat provisoire de remplacement.</td></tr><tr><th scope="row">Assurance privée</th><td>Attestation de prise en charge de votre assureur.</td></tr>'
      '<tr><th scope="row">Pensionné de guerre, victime d’attentat</th><td>Carnet de soins.</td></tr></tbody></table></div>'
      '<div class="callout"><h3>Il vous manque un document ?</h3><p>Vous pouvez le faire parvenir pendant votre hospitalisation par un proche, par courrier ou par e-mail à <a href="mailto:admissions@ch-issoudun.fr">admissions@ch-issoudun.fr</a>. Si vous êtes passé par les urgences, régularisez votre dossier rapidement.</p></div>'
      '<h2>Vos objets de valeur</h2><p>Évitez de garder des objets de valeur ou de l’argent dans votre chambre. Confiez-les à votre entourage, ou aux infirmiers, qui les déposeront au coffre des admissions du pavillon Marie Curie.</p>')
    a = fiche([("Standard", bigtel("02 54 03 54 03")), ("Admissions", "Hall du pavillon Marie Curie et entrée du service de rééducation")], docs(("Livret d’accueil", "2023/01/LIVRET-DACCUEIL-CHTB-2019.pdf", "Édition de 2019")))
    o.append(p("parcours/preparer-venue.html", "Préparer votre venue", "Les documents et les affaires à prévoir pour une hospitalisation, sous forme de liste à cocher.", m, a, crumbs=PC, active="parcours", kw="valise papiers documents admission carte vitale apporter"))

    t = lambda a, b: f"<h2>{a}</h2><p>{b}</p>"
    m = ('<div class="tbl-wrap"><table class="tbl"><caption class="visually-hidden">Horaires des repas</caption><thead><tr><th scope="col">Repas</th><th scope="col">Horaire</th></tr></thead><tbody><tr><td>Petit-déjeuner</td><td>À partir de 7 h 30</td></tr><tr><td>Déjeuner</td><td>12 h</td></tr><tr><td>Dîner</td><td>18 h 30</td></tr></tbody></table></div>'
      + t("Vos soins et vos médicaments", "Les soins sont assurés 24 h sur 24 sur prescription médicale, dans votre service et sur les plateaux techniques. Remettez votre traitement personnel à l’infirmière avec votre ordonnance : la pharmacie de l’établissement délivre les médicaments prescrits.")
      + t("Vos repas", "Ils sont préparés sur place et validés par une diététicienne. Signalez vos régimes et allergies au personnel. Le service se fait en chambre ou en salle à manger, selon le service.")
      + t("Linge et toilette", "Le linge hôtelier est fourni et entretenu par l’établissement. Prévoyez votre nécessaire de toilette et votre linge personnel.")
      + t("Téléphone, télévision et Wi-Fi", "Chaque chambre dispose d’une télévision et d’une ligne pour recevoir des appels. Demandez la mise en service au standard du pavillon Marie Curie ou au bureau des admissions de la rééducation. Ces services sont facturés à la sortie. Le code Wi-Fi s’obtient aux mêmes endroits.")
      + t("Soins de confort", "En médecine polyvalente et gériatrique, une aide-soignante dédiée propose sur demande soins du visage, manucure et maquillage. Une réflexologue est disponible selon la pathologie, dans tous les services. Coiffure, esthétique et pédicure restent possibles à votre charge : vous contactez le professionnel et prévenez le service.")
      + t("Interprète", "Un interprète peut vous assister. Renseignez-vous auprès du cadre de santé du service.")
      + t("Culte", "Les ministres des différents cultes peuvent vous rendre visite sur demande. Un service d’aumônerie fonctionne au Centre Hospitalier.")
      + t("Courrier", "Indiquez votre service et votre numéro de chambre. Le courrier est distribué chaque jour. Déposez votre courrier affranchi dans la boîte du pavillon Marie Curie ou au bureau des admissions de la rééducation, avant 15 h, du lundi au vendredi.")
      + t("Permission de sortie", "Si votre état de santé le permet, le médecin peut accorder une permission de 48 h au maximum. Le transport est entièrement à votre charge.")
      + t("Distributeurs", "Boissons et en-cas sont disponibles dans les halls Marie Curie et MPR.")
      + "<h2>Associations</h2><p>Ces associations interviennent gratuitement auprès des patients et des résidents.</p>"
      + ul("<strong>EADSP 36 :</strong> équipe d’appui départementale en soins palliatifs", "<strong>ALAVI :</strong> bénévoles formés à l’écoute", "<strong>Culture et Loisirs :</strong> lecture et visites", "<strong>Pour Que l’Esprit Vive :</strong> concerts réguliers", "<strong>ARCHI :</strong> événements en rééducation, journée Hand’Iss, achat d’équipements", "<strong>VMEH :</strong> visites et activités", "<strong>SAALSA :</strong> après-midi récréatifs et activités manuelles", "<strong>Art et loisirs :</strong> intervention de bénévoles", "<strong>Le Cocon :</strong> soutien à la parentalité, sous condition d’adhésion"))
    a = fiche([("Standard", bigtel("02 54 03 54 03")), ("Tabac et alcool", "Il est interdit de fumer, de vapoter ou d’introduire de l’alcool dans les locaux.")], docs(("Livret d’accueil", "2023/01/LIVRET-DACCUEIL-CHTB-2019.pdf", "Édition de 2019")))
    o.append(p("parcours/sejour.html", "Votre séjour", "La vie quotidienne pendant votre hospitalisation.", m, a, crumbs=PC, active="parcours", kw="repas wifi television telephone culte interprete association permission linge"))

    m = (t("Heures de visite", "Votre entourage est le bienvenu. Les visites sont conseillées de 13 h à 20 h, pour faciliter les soins. Les enfants restent sous la responsabilité de leurs parents.")
      + t("Partager un repas", "Les proches peuvent déjeuner avec un patient ou un résident les week-ends et jours fériés. Réservez 72 h à l’avance. Le paiement se fait au standard pour les services du pavillon Marie Curie, et aux admissions pour la rééducation.")
      + t("Dormir sur place", "Une personne de la famille ou de l’entourage peut dormir sur place. Renseignez-vous auprès du cadre de santé.")
      + '<h2>Visiter un résident en EHPAD</h2><p>Famille, proches et amis peuvent rendre visite librement de 9 h à 18 h. <a href="/hebergement/vie-quotidienne.html#visites">Lire les règles de vie en EHPAD</a></p>')
    o.append(p("parcours/visites.html", "Visites et proches", "Les visites sont conseillées de 13 h à 20 h.", m, fiche([("Horaires conseillés", "<strong>13 h à 20 h</strong>"), ("EHPAD", "<strong>9 h à 18 h</strong>"), ("Standard", bigtel("02 54 03 54 03"))]), crumbs=PC, active="parcours", kw="horaires visite repas accompagnant dormir"))

    m = ("<p>Le service social évalue vos besoins et vous accompagne, ainsi que votre entourage, dans vos démarches : aide au retour à domicile, recherche d’un établissement, accès aux droits.</p>"
      "<p>Parlez-en à l’équipe soignante, qui contactera l’assistant social de votre service.</p>"
      '<h2>Selon votre situation</h2>' + stations([("Vous n’avez pas de couverture sociale", "/services/pass.html"), ("Vous cherchez des soins à domicile", "/services/ssiad.html"), ("Vous préparez une entrée en EHPAD", "/hebergement/admission.html"), ("Vous accompagnez un proche atteint d’Alzheimer", "/services/la-parenthese.html")]))
    o.append(p("parcours/appui-social.html", "Appui social", "Le service social vous aide à préparer la suite, avec vos proches.", m, crumbs=PC, active="parcours", kw="assistante sociale aide retour domicile"))

    m = (steps(("Le médecin décide de votre sortie.", " Le secrétariat du service vous remet les ordonnances et une lettre pour votre médecin."), ("Passez au bureau des admissions", " le jour de votre départ. Vous récupérez vos documents, complétez votre dossier et réglez ce qui reste à votre charge."), ("Recevez votre bulletin de situation.", " Il justifie de vos droits auprès de votre organisme de sécurité sociale et de votre employeur."))
      + t("Votre transport", "Les trajets en taxi médical prescrits par un médecin sont pris en charge si le taxi a signé une convention avec l’Assurance Maladie. Si vous choisissez un taxi non conventionné, le trajet reste à votre charge.")
      + t("Sortie contre avis médical", "Vous pouvez quitter l’hôpital à tout moment. Vous signez alors une décharge, après avoir été informé des risques.")
      + t("Sortie d’un mineur", "Un mineur ne peut sortir qu’avec un parent ou le représentant légal. Sinon, un adulte doit être autorisé par écrit, et le personnel vérifie son identité."))
    o.append(p("parcours/sortie.html", "Votre sortie", "Le jour du départ, trois étapes et quelques règles à connaître.", m, crumbs=PC, active="parcours", kw="sortie taxi transport decharge bulletin de situation ambulance vsl"))

    m = ("<h2>Ce qui compose le coût</h2><div class=\"tbl-wrap\"><table class=\"tbl\"><tbody><tr><th scope=\"row\">Tarif journalier</th><td>En règle générale, pris en charge à 80 % par l’assurance maladie.</td></tr><tr><th scope=\"row\">Ticket modérateur</th><td>Ce qui reste à votre charge. Il peut être couvert par votre mutuelle ou votre assurance.</td></tr><tr><th scope=\"row\">Forfait journalier</th><td>Votre participation à l’hébergement et à la restauration. Son montant est fixé par arrêté ministériel. Certaines mutuelles le prennent en charge.</td></tr></tbody></table></div>"
      + t("Chambre particulière", "Les chambres sont individuelles ou à 2 lits. Vous pouvez demander une chambre particulière, selon les disponibilités, pour un supplément de 45 €. Il n’est pas remboursé par la Sécurité sociale, même à 100 %. Votre mutuelle peut le rembourser selon votre contrat.")
      + t("Comment payer", "Par espèces, chèque ou carte bancaire. À défaut, une facture est envoyée à votre domicile. Le bureau des admissions peut vous expliquer votre facture."))
    o.append(p("parcours/frais.html", "Frais et facturation", "Ce qui est pris en charge, ce qui reste à payer et comment régler.", m, crumbs=PC, active="parcours", kw="prix cout payer facture mutuelle forfait ticket moderateur chambre seule"))

    m = (t("Qui peut le demander", "Vous-même, votre tuteur si vous êtes majeur sous tutelle, ou le médecin que vous choisissez comme intermédiaire. Une personne sous curatelle consulte elle-même son dossier.")
      + "<h2>Comment le demander</h2>" + steps(("Écrivez à la direction", " en précisant votre demande et votre accord pour les frais éventuels d’impression et de poste."), ("Joignez une copie de votre pièce d’identité.", " Pour un parent décédé, ajoutez une copie du livret de famille."), ("Choisissez comment accéder au dossier :", " consultation gratuite sur place, retrait d’une copie ou envoi en recommandé."))
      + '<div class="tbl-wrap"><table class="tbl"><caption class="visually-hidden">Délais de communication</caption><thead><tr><th scope="col">Dossier</th><th scope="col">Délai après réception de la demande</th></tr></thead><tbody><tr><td>De moins de 5 ans</td><td>8 jours</td></tr><tr><td>De plus de 5 ans</td><td>2 mois</td></tr></tbody></table></div>'
      + "<p>Le dossier médical est conservé 20 ans après votre dernière hospitalisation ou consultation.</p>")
    a = fiche([("Adresse", "Direction du Centre Hospitalier<br>Avenue Jean Bonnefont<br>CS 70190<br>36105 Issoudun Cedex"), ("Standard", tel("02 54 03 54 03"))])
    o.append(p("parcours/dossier-medical.html", "Dossier médical", "Comment obtenir une copie de votre dossier, et sous quel délai.", m, a, crumbs=PC, active="parcours", kw="dossier copie compte rendu acces demande"))

    m = (t("Confidentialité", "Toutes vos informations médicales sont confidentielles. La loi du 4 mars 2002 impose aux professionnels de respecter le secret professionnel.")
      + t("Personne de confiance", "Vous pouvez désigner un parent, un proche ou votre médecin traitant. Si vous ne pouvez plus exprimer votre volonté, elle est consultée en priorité pour dire ce que vous auriez souhaité. Vous pouvez changer ce choix à tout moment.")
      + t("Personne à prévenir", "Vous indiquez les coordonnées de la personne que le service peut joindre en cas de besoin. Elle peut être différente de la personne de confiance.")
      + "<h2>Directives anticipées</h2><p>Ce sont vos instructions écrites pour votre fin de vie, si vous ne pouvez plus vous exprimer. Elles s’imposent au médecin, sauf en cas d’urgence vitale le temps d’évaluer la situation, ou si elles sont jugées inappropriées après une procédure collégiale.</p><p>Elles sont valables à vie, et vous pouvez les modifier à tout moment. Rédigez-les sur un formulaire ou sur papier libre, datées et signées. Si vous ne pouvez pas écrire, deux témoins peuvent intervenir.</p>"
      + t("Don d’organes", "Vous pouvez vous inscrire sur le registre national des refus, ou exprimer votre opposition à vos proches. Le refus peut être partiel.")
      + t("Identité et bracelet", "Avec votre accord, un bracelet d’identification vous est posé à votre arrivée. Votre identité vous sera demandée plusieurs fois : ce contrôle évite les erreurs.")
      + "<h2>Faire une réclamation</h2>" + steps("Parlez-en d’abord au cadre de santé ou au médecin du service.", "Contactez la Commission des usagers (CDU) par l’intermédiaire de ses représentants.", "Écrivez au directeur de l’établissement. Toute réclamation reçoit une réponse."))
    o.append(p("parcours/droits.html", "Vos droits", "Confidentialité, personne de confiance, directives anticipées, réclamation.", m, crumbs=PC, active="parcours", kw="plainte reclamation cdu directives anticipees personne de confiance don d organes"))
    return o

# ---------- Hébergement
HC = [("EHPAD", "/services/ehpad.html")]
def hebergement():
    o = []
    m = ("<h2>Les conditions</h2><p>Les résidences accueillent les personnes de plus de 60 ans, sauf dérogation, seules ou en couple, sans condition de ressources.</p><h2>Les étapes</h2>"
      + steps(("Visitez la résidence", " avec vos proches, avant toute décision."), ("Retirez le dossier", " au bureau des admissions en hébergement, au rez-de-chaussée du pavillon Marie Curie."), ("Constituez le dossier.", " Votre médecin traitant remplit le dossier médical. Vous ou votre famille remplissez le dossier administratif."), ("Passez une visite médicale", " avec le médecin responsable de la structure, une fois le dossier complet."), ("Attendez la décision.", " La commission d’admission se réunit tous les 15 jours. En urgence, le médecin coordonnateur peut donner son accord après analyse du dossier. La décision finale revient au directeur."), ("Signez le contrat de séjour.", " Vous recevez le règlement et pouvez désigner une personne de confiance."))
      + "<h2>Le dossier comprend</h2>" + ul("Un certificat médical d’admission, avec les traitements complets", "Le consentement éclairé du résident", "Le dossier administratif et ses pièces obligatoires", "Si vous le souhaitez, la désignation d’une personne de confiance et vos directives anticipées")
      + "<h2>Ce que regarde le médecin coordonnateur</h2><p>L’état de santé et le risque d’aggravation rapide, le niveau de dépendance (GIR), les troubles du comportement, le traitement, la liste d’attente, l’urgence, le type de résidence disponible et votre choix.</p>"
      + '<p>Si l’entrée n’est pas immédiate, votre situation est réévaluée. L’orientation peut alors changer.</p>')
    a = fiche([("Admissions", bigtel("02 54 03 54 03")), ("Où", f"{MC}, rez-de-chaussée")], docs(("Trousseau minimum de linge", "2021/12/Trousseau_minimum_de_linge_des_residents_au_moment_de_ladmission.pdf")))
    o.append(p("hebergement/admission.html", "Demander une admission en EHPAD", "Six étapes, de la visite à la signature du contrat de séjour.", m, a, line="age", active="age", crumbs=HC, kw="entrer ehpad dossier commission maison de retraite"))

    m = ("<h2>Ce que couvre le prix de séjour</h2>" + ul("<strong>L’hébergement :</strong> repas, entretien des chambres et des parties communes, linge plat", "<strong>La dépendance :</strong> les dépenses liées à la perte d’autonomie")
      + '<p>Le prix est payé par le résident, ses obligés alimentaires ou l’aide sociale. Les tarifs sont fixés chaque année par arrêté du Conseil départemental de l’Indre et affichés au tableau d’informations de chaque résidence.</p>'
      + "<h2>Selon votre niveau de dépendance</h2><div class=\"tbl-wrap\"><table class=\"tbl\"><thead><tr><th scope=\"col\">GIR</th><th scope=\"col\">Ce qui s’applique</th></tr></thead><tbody><tr><td>GIR 5-6</td><td>Le tarif dépendance GIR 5-6 reste à votre charge.</td></tr><tr><td>GIR 1-2 et 3-4</td><td>L’allocation personnalisée d’autonomie (APA) est versée par le département de votre domicile précédent.</td></tr></tbody></table></div>"
      + "<h2>Les aides</h2><p>Les résidences sont habilitées à l’aide sociale et conventionnées à l’APA et à l’APL. Selon votre situation, vous pouvez bénéficier de l’aide sociale, de l’allocation logement et de l’APA. Un agent administratif peut vous renseigner.</p>")
    a = fiche([("Bureau des admissions", bigtel("02 54 03 54 03"))], docs(("Allocation personnalisée d’autonomie", "https://www.pour-les-personnes-agees.gouv.fr/preserver-son-autonomie-s-informer-et-anticiper/perte-d-autonomie-evaluation-et-droits/lallocation-personnalisee-dautonomie-apa", "Portail national")))
    o.append(p("hebergement/tarifs-aides.html", "Tarifs et aides en EHPAD", "Ce que couvre le prix de séjour, et les aides possibles.", m, a, line="age", active="age", crumbs=HC, kw="prix cout apa apl aide sociale gir ehpad"))

    m = ('<h2 id="chambre">La chambre</h2><p>Lit médicalisé, armoire murale, table de chevet, chaise et fauteuil. Le système d’appel se trouve au-dessus du lit et dans la salle de bain, de jour comme de nuit.</p>'
      '<p>Personnalisez votre chambre avec de petits meubles, des cadres et des photos, avec l’accord du service technique. Les appareils électriques doivent être homologués, sous garantie et validés avant usage. Seul le technicien de maintenance installe les équipements personnels. Les réfrigérateurs ne sont pas admis.</p>'
      '<p>À fournir par vous ou votre famille : téléviseur et câbles, produits d’hygiène, vêtements et chaussures.</p>'
      '<h2 id="repas">Les repas</h2><div class="tbl-wrap"><table class="tbl"><tbody><tr><th scope="row">Petit-déjeuner</th><td>En chambre, à partir de 8 h</td></tr><tr><th scope="row">Déjeuner</th><td>À midi, en salle à manger</td></tr><tr><th scope="row">Collation</th><td>Vers 15 h 30</td></tr><tr><th scope="row">Dîner</th><td>En salle à manger, à partir de 18 h</td></tr></tbody></table></div>'
      '<p>La cuisine centrale de l’hôpital prépare les repas, sous le contrôle des diététiciennes. Les régimes et textures modifiées suivent la prescription médicale. L’établissement vise 50 % de produits bio ou locaux.</p>'
      '<p>Pour partager un repas avec un proche, réservez auprès du secrétariat, au moins 72 h à l’avance. Le ticket s’achète à l’accueil du bâtiment Marie Curie.</p>'
      '<h2 id="animation">L’animation</h2><p>Une animatrice diplômée et une aide médico-psychologique sont présentes les lundis, mercredis et vendredis, de 9 h à 17 h. Le planning mensuel est affiché sur le tableau d’animation et dans les chambres. La participation est libre.</p>'
      '<p>Chant, cuisine, jardinage, quiz, lotos, jeux de société et de cartes, gym douce, anniversaires, fêtes traditionnelles, spectacles, concerts, ateliers d’écriture et rencontres intergénérationnelles.</p>'
      '<h2 id="services">Les services</h2><h3>Courrier</h3><p>Distribué et relevé tous les jours, sauf le week-end. Les timbres ne sont pas fournis.</p>'
      '<h3>Téléphone</h3><p>À Bel Air, chaque chambre a une prise : vous ouvrez votre ligne auprès de l’opérateur de votre choix. Aux Reflets d’Argent, demandez l’activation au secrétariat. Les communications sont facturées chaque trimestre. Dans les deux cas, apportez votre téléphone.</p>'
      '<h3>Linge</h3><p>Le linge plat est inclus dans le prix de l’hébergement. Pour le linge personnel, trois options : votre famille, un prestataire de votre choix, ou la blanchisserie de l’établissement. Confiez-le à la blanchisserie quelques jours avant l’arrivée pour l’étiquetage. L’établissement décline toute responsabilité pour le linge non marqué.</p>'
      '<h2 id="visites">Sorties et visites</h2><p>Les sorties sont libres, à condition de prévenir le secrétariat ou les infirmières. Pour une absence pour convenances personnelles, prévenez au moins 48 h à l’avance. Famille, proches et amis peuvent rendre visite librement de 9 h à 18 h.</p>'
      '<h2 id="regles">Règles de vie</h2><p>La vie en commun repose sur le respect des rythmes de vie, des autres résidents, du personnel et des équipements. Il est interdit de fumer ou de vapoter dans les chambres et à l’intérieur de l’établissement.</p>')
    a = '<h2>Sur cette page</h2>' + stations([("La chambre", "#chambre"), ("Les repas", "#repas"), ("L’animation", "#animation"), ("Les services", "#services"), ("Sorties et visites", "#visites"), ("Règles de vie", "#regles")])
    o.append(p("hebergement/vie-quotidienne.html", "Vie quotidienne en EHPAD", "La chambre, les repas, l’animation et les services au quotidien.", m, a, line="age", active="age", crumbs=HC, kw="chambre repas animation linge courrier ehpad visite sortie"))

    m = ('<div class="tbl-wrap"><table class="tbl resp"><thead><tr><th scope="col">Organisme</th><th scope="col">Démarche</th></tr></thead><tbody>'
      '<tr><th scope="row"><a href="https://www.service-public.fr">Service-public.fr</a></th><td>Signalez en une fois votre changement d’adresse à plusieurs administrations.</td></tr>'
      '<tr><th scope="row">Assurance maladie, CAF, caisses de retraite</th><td>Signalez votre changement d’adresse à la <a href="https://www.ameli.fr">CPAM</a>, à la <a href="https://www.caf.fr">CAF</a> et à vos caisses de base et complémentaire.</td></tr>'
      '<tr><th scope="row">Conseil départemental</th><td>Prévenez le service de l’APA si vous la percevez à domicile.</td></tr>'
      '<tr><th scope="row">Impôts</th><td>Signalez votre changement de résidence principale.</td></tr>'
      '<tr><th scope="row">Banque</th><td>Donnez votre nouvelle adresse.</td></tr>'
      '<tr><th scope="row">Mairie</th><td>Inscrivez-vous sur la liste électorale de votre nouvelle commune.</td></tr></tbody></table></div>'
      '<p>L’assistante sociale de la résidence peut vous accompagner dans ces démarches.</p>')
    o.append(p("hebergement/organismes.html", "Organismes à prévenir avant l’entrée", "La liste des démarches à faire lors d’une entrée en résidence.", m, line="age", active="age", crumbs=HC, kw="changement adresse ehpad"))
    return o

# ---------- Prévention
PR = [("Prévention", "/prevention/index.html")]
def prevention():
    o = []
    o.append(p("prevention/index.html", "Prévention", "Reconnaître les signes d’alerte et adopter les bons réflexes.", stations([("Reconnaître un AVC", "/prevention/avc.html", "Chaque minute compte"), ("Vigilance canicule", "/prevention/canicule.html", "Les signes, les personnes à risque"), ("Risques numériques", "/prevention/risques-numeriques.html", "Kit de sensibilisation"), ("Développement durable", "/prevention/developpement-durable.html", "Charte et documents")], "prev"), line="prev", active="prev", kw="sante publique"))

    m = ('<div class="callout warn"><h3>Un seul de ces signes suffit : appelez le 15</h3><p>Même en cas de doute. Même si les signes disparaissent. Les personnes ayant des difficultés à parler ou à entendre peuvent contacter le 114.</p></div>'
      '<h2>Les signes d’alerte</h2>' + ul("<strong>La bouche se déforme :</strong> le sourire n’est pas symétrique.", "<strong>Un côté du corps s’affaiblit :</strong> si la personne lève les deux bras, l’un retombe.", "<strong>La parole se trouble :</strong> difficulté à parler ou à comprendre une phrase.", "<strong>Autres signes brutaux et inexpliqués :</strong> troubles de l’équilibre, maux de tête intenses, perte de la vue d’un œil ou vision double.")
      + '<p class="meta">Source : <a href="https://www.sante.fr/les-signes-de-lavc">sante.fr, les signes de l’AVC</a></p>'
      + '<h2>Après un AVC</h2><p>L’hôpital prend en charge l’AVC en <a href="/services/medecine-geriatrique.html">médecine aiguë gériatrique</a> et en rééducation, au service de <a href="/services/mpr.html">médecine physique et réadaptation</a>.</p>')
    o.append(p("prevention/avc.html", "Reconnaître un AVC", "Bouche déformée, faiblesse d’un côté, troubles de la parole : appelez immédiatement le 15.", m, fiche([("Urgence", '<a class="bigtel" href="tel:15">15</a>'), ("Parole ou audition difficile", '<a class="bigtel" href="tel:114">114</a>')]), line="prev", active="prev", crumbs=PR, kw="accident vasculaire cerebral paralysie"))

    m = ('<div class="callout warn"><h3>Malaise, propos incohérents ou forte fièvre</h3><p>Appelez immédiatement le 15.</p></div><h2>Les signes d’alerte</h2>' + ul("Maux de tête", "Fièvre supérieure à 38 °C", "Fatigue inhabituelle", "Crampes", "Vertiges ou nausées", "Propos incohérents")
      + "<h2>Les personnes les plus à risque</h2>" + ul("Les personnes de plus de 65 ans", "Les nourrissons et les enfants, surtout avant 4 ans", "Les travailleurs manuels et sportifs en extérieur", "Les personnes alitées ou en fauteuil", "Les personnes atteintes de démence, de troubles du comportement ou en perte d’autonomie", "Les personnes sous traitement au long cours", "Les personnes atteintes d’une maladie chronique ou aiguë", "Les personnes en très grande précarité")
      + '<h2>Les quatre niveaux du plan</h2><div class="tbl-wrap"><table class="tbl"><tbody><tr><th scope="row">Niveau 1</th><td>Veille saisonnière, à partir du 1er juin</td></tr><tr><th scope="row">Niveau 2</th><td>Avertissement chaleur, vigilance jaune possible</td></tr><tr><th scope="row">Niveau 3</th><td>Alerte canicule, vigilance orange Météo-France</td></tr><tr><th scope="row">Niveau 4</th><td>Mobilisation maximale, canicule exceptionnelle et durable</td></tr></tbody></table></div>')
    a = fiche([("Urgence", '<a class="bigtel" href="tel:15">15</a>')], docs(("Carte de vigilance Météo-France", "https://vigilance.meteofrance.fr/fr/canicule"), ("Vivre avec la chaleur", "https://www.vivre-avec-la-chaleur.fr/", "Santé publique France")))
    o.append(p("prevention/canicule.html", "Vigilance canicule", "Reconnaître les signes et protéger les plus fragiles.", m, a, line="prev", active="prev", crumbs=PR, kw="chaleur ete deshydratation"))

    m = ("<p>Les systèmes d’information sont essentiels au fonctionnement de l’hôpital. Les conseils donnés à nos professionnels valent aussi pour vos usages personnels : naviguer plus sûrement, utiliser les réseaux sociaux avec prudence et sécuriser vos appareils mobiles.</p>" + docs(("Kit de sensibilisation aux risques numériques", "2022/07/Kit-complet-de-sensibilisation-aux-risques-numeriques.pdf", "Juillet 2022")))
    o.append(p("prevention/risques-numeriques.html", "Risques numériques", "Quelques minutes pour mieux vous protéger en ligne.", m, line="prev", active="prev", crumbs=PR, kw="cybersecurite internet arnaque"))

    m = ("<p>L’établissement formalise sa démarche dans une charte et un projet dédiés.</p>" + docs(("Charte du développement durable", "2021/12/charte_DD_2019.pdf", "2019"), ("Notice du développement durable", "2021/12/notice_developpement_durable1.pdf"), ("Guide de l’agent éco-responsable", "2021/12/Guide_de_lagent_Eco-responsable_DD_2.pdf"), ("Projet d’établissement du développement durable", "2021/12/Projet_detablissement_DD.pdf")))
    o.append(p("prevention/developpement-durable.html", "Développement durable", "La charte et les documents de la démarche de l’établissement.", m, line="prev", active="prev", crumbs=PR, kw="environnement ecologie"))
    return o

# ---------- Carrières
CC = [("Carrières", "/carrieres/index.html")]
JOBS = [
 ("Animateur (H/F) en EHPAD", "support", "Octobre 2026", "2026/10/Annonce-animatrice.pdf"), ("Manipulateur en électroradiologie médicale (H/F)", "soin", "Octobre 2026", "/annonce-merm"), ("Secrétaire médical(e)", "support", "Octobre 2026", "2026/10/Annonce-secretaire-medicale.pdf"),
 ("Aide-soignant (H/F) de jour, pool de remplacement", "soin", "Août 2026", "2026/08/10-Annonce-AS-pool-de-remplacement.pdf"), ("Cuisinier(e)", "support", "Août 2026", "2026/08/Annonce-cuisinier.pdf"),
 ("Orthophoniste (H/F) de jour", "reed", "Mars 2026", "2026/03/ORTHOPHONISTE_2026.pdf"), ("Ergothérapeute (H/F), équipe mobile", "reed", "Mars 2026", "2026/03/ERGOTHERAPEUTE_03-2026.pdf"), ("Infirmier diplômé d’État (H/F) de jour, EHPAD", "soin", "Mars 2026", "2026/03/IDE-EHPAD-CDD.pdf"),
 ("Psychomotricien (H/F)", "reed", "Février 2026", "2026/02/annonce-psychomot.pdf"), ("Aide-soignant (H/F) de jour, secteur médico-social", "soin", "Septembre 2025", "2025/09/3-Annonce-generale-AS-V2.pdf"),
 ("Médecin généraliste", "med", "Juillet 2024", "2024/07/Affiche-Recrutement-DAM-MG-CDS.pdf"), ("Médecin spécialiste en médecine physique et réadaptation", "med", "Mai 2024", "2024/05/Affiche-Recrutement-DAM-MPR.pdf"), ("Médecin spécialiste en médecine générale", "med", "Mai 2024", "2024/05/Affiche-Recrutement-DAM-MG.pdf"),
 ("Médecin spécialiste en imagerie médicale", "med", "Mai 2024", "2024/05/Affiche-Recrutement-DAM-IM.pdf"), ("Pharmacien", "med", "Mai 2024", "2024/05/Affiche-Recrutement-DAM-PHARM.pdf"), ("Radiologue", "med", "Février 2024", "2024/02/Fiche-de-poste-partagee-IMAGERIE-CHTX-CHTB-VF.pdf"),
]
def carrieres():
    o = []
    rows = ""
    for t, c, d, u in JOBS:
        href = "https://www.ch-issoudun.fr/recrutement-formation/recrutement/offres-demploi/" if u.startswith("/") else UP + u
        rows += f'<li data-row data-cat="{c}"><a class="row" href="{href}"><b>{e(t)}</b><span class="s">Publiée en {e(d.lower())}</span><span class="t">Lire l’annonce</span></a></li>'
    chips = "".join(f'<button class="chip" type="button" aria-pressed="false" data-f="{f}">{t}</button>' for f, t in [("soin", "Soins"), ("reed", "Rééducation"), ("med", "Médecins et pharmaciens"), ("support", "Administratif, technique, animation")])
    m = (f'<div class="filter no-print" data-filter-for="jobs"><input type="search" placeholder="Métier" aria-label="Filtrer par métier">{chips}<span class="count" role="status"></span></div><div id="jobs"><ul class="dir">{rows}</ul><p class="empty" hidden>Aucune offre ne correspond. Envoyez une candidature spontanée.</p></div>'
      "<h2>Pourquoi nous rejoindre</h2>" + ul("28 jours de congés annuels", "Télétravail, selon les postes", "Prise en charge de 75 % des transports collectifs", "Logement ponctuel", "Bourses d’études", "Retraite progressive", "Self et mutuelle")
      + '<p>Une taille humaine et des valeurs humanistes, dans un établissement de référence pour plus de 30 000 habitants.</p><p><a href="/carrieres/nouveaux-arrivants.html">Lire ce qui attend les nouveaux arrivants</a></p>')
    a = fiche([("Affaires médicales", bigtel("02 54 03 55 45") + '<br><a href="mailto:affaires.medicales@ch-issoudun.fr">affaires.medicales@ch-issoudun.fr</a>'), ("Standard", tel("02 54 03 54 03")), ("Mobilité interne", "Pas d’offre en cours")], title="Contacts")
    o.append(p("carrieres/index.html", "Offres d’emploi", "Seize postes ouverts dans le soin, la rééducation, la médecine et les métiers supports.", m, a, line="prev", active="car", tag="Carrières", kw="recrutement emploi travail postuler infirmier aide soignant medecin candidature"))

    m = ("<p>Le livret d’accueil réunit les informations pratiques : démarches administratives, consignes de sécurité, statut et rémunération. Pour tout renseignement, contactez le service des ressources humaines par le standard.</p>" + docs(("Livret d’accueil, format PDF", "2026/03/Livret_nvx_arrivants_mars2026.pdf", "Mars 2026"), ("Livret d’accueil, version feuilletable", "https://www.calameo.com/read/007747658fbf856f975a4")))
    o.append(p("carrieres/nouveaux-arrivants.html", "Nouveaux arrivants", "Bienvenue au Centre Hospitalier : tout ce qu’il faut pour vos premiers jours.", m, line="prev", active="car", crumbs=CC, kw="livret accueil agent rh"))

    m = ('<p>Les demandes de stage se font par e-mail à <a href="mailto:stages@ch-issoudun.fr">stages@ch-issoudun.fr</a>. Précisez votre formation, le service souhaité et vos dates.</p><p>L’hôpital accueille régulièrement des internes. Depuis juin 2024, une convention avec le CHRU de Tours permet aussi d’accueillir des externes, de la 4e à la 6e année de médecine, toute l’année.</p>')
    o.append(p("carrieres/stages.html", "Stages", "Demandez un stage par e-mail, en précisant votre formation et vos dates.", m, line="prev", active="car", crumbs=CC, kw="stagiaire seconde interne externe"))

    m = ("<p>Institut public agréé depuis 1982, l’IFAS d’Issoudun se trouve dans l’enceinte du Centre Hospitalier. C’est une annexe de l’IFSI-IFAS du Centre Hospitalier de Châteauroux, agréée pour 33 élèves.</p>"
      "<h2>La formation</h2><p>Une session d’un an, de septembre à juillet. L’aide-soignant assure les soins d’entretien et de continuité de la vie, accompagne les actes de la vie quotidienne et travaille en équipe sous la responsabilité de l’infirmier.</p>"
      '<h2>S’inscrire</h2><p>Le dossier d’inscription pour les IFAS de l’Indre se télécharge sur <a href="https://www.ch-chateauroux-leblanc.fr/formation-as">le site du Centre Hospitalier de Châteauroux-Le Blanc</a>. Vous pouvez aussi le retirer au secrétariat, sur rendez-vous.</p>'
      "<h2>L’équipe</h2>" + team(("Direction", "Mme Sylvie Quatrehomme"), ("Formateur", f'M. François Dessard<br>{tel("07 89 33 05 13")}<br><a href="mailto:francois.dessard@ch-chateauroux.fr">francois.dessard@ch-chateauroux.fr</a>'), ("Formatrice", f'Mme Magali Tingaud<br>{tel("07 89 33 05 09")}<br><a href="mailto:magali.tingaud@ch-chateauroux.fr">magali.tingaud@ch-chateauroux.fr</a>')))
    a = fiche([("Secrétariat", bigtel("02 54 29 60 31")), ("Durée", "1 an, de septembre à juillet"), ("Promotion", "33 élèves")], docs(("Règlement intérieur", "2022/11/Reglement-interieur.pdf"), ("Arrêté de formation aide-soignant", "2022/11/arrete-formation-AS-100621.pdf"), ("Projet pédagogique", "2022/11/Projet-Pedagogique-2022-2023.pdf", "2022-2023")))
    o.append(p("carrieres/ifas.html", "Devenir aide-soignant : l’IFAS d’Issoudun", "Une formation d’un an, dans l’enceinte de l’hôpital. 33 élèves par promotion.", m, a, line="prev", active="car", crumbs=CC, kw="ifas aide soignante ecole formation inscription"))

    m = ("<h2>Journée régionale de la médecine d’urgence</h2><p>L’édition 2025 s’est tenue au Centre Hospitalier de la Tour Blanche. Retrouvez les présentations.</p>" + docs(("SOS id", "2025/12/Preesentation-SOSid-fev-2025-copie-1.pdf", "Février 2025"), ("OML", "2025/12/Presentation-OML-2025.pdf", "2025"), ("Réseau régional de traumatologie sévère", "2025/12/Reseau-regional-de-traumatologie-severe-09-10-25.pdf", "9 octobre 2025"), ("Trauma grave", "2025/12/Trauma-grave-VF-J-09-X-2025-0h30-.pdf", "9 octobre 2025")))
    o.append(p("carrieres/formation-continue.html", "Formation médicale continue", "Les ressources de la Journée régionale de la médecine d’urgence.", m, line="prev", active="car", crumbs=CC, kw="jrmu medecine urgence congres"))
    return o

# ---------- Hôpital
HC2 = [("L’hôpital", "/hopital/index.html")]
def hopital():
    o = []
    m = ('<ul class="facts l-soins"><li><b>460</b><span>lits et places</span></li><li><b>30 000+</b><span>habitants dans le bassin de population</span></li><li><b>1995</b><span>ouverture de la rééducation</span></li><li><b>33</b><span>élèves aides-soignants par promotion</span></li></ul>'
      '<h2 style="margin-top:1.3em">Notre mission</h2><p>Établissement public de santé de l’Indre, labellisé hôpital de proximité par l’ARS, le Centre Hospitalier de la Tour Blanche a pour objectif la satisfaction des besoins de santé de la population. Il réunit trois forces :</p>'
      + ul("<strong>L’expertise :</strong> un centre de rééducation à la renommée interrégionale", "<strong>Le plateau technique :</strong> des services de médecine, les urgences et l’imagerie", "<strong>La proximité :</strong> des consultations avancées de spécialistes, à Issoudun")
      + '<h2>Un hôpital en réseau</h2><p>À égale distance de Bourges et de Châteauroux, l’hôpital travaille avec les établissements du Berry et de la région Centre-Val de Loire, pour délivrer les bons soins, au bon endroit, au bon moment. Il participe aussi au Contrat local de santé d’Issoudun.</p>'
      + '<h2>Nos valeurs</h2><p>Des groupes de travail composés de membres du personnel ont élaboré la charte des valeurs de l’établissement. Les mots retenus viennent d’un questionnaire adressé à tous les agents, auquel 63 % ont répondu.</p>'
      + docs(("Charte des valeurs", "2022/04/Roue-valeurs-2-scaled.jpg")))
    a = "<h2>Pour aller plus loin</h2>" + stations([("Organisation et instances", "/hopital/organisation.html"), ("Qualité et sécurité des soins", "/hopital/qualite.html"), ("Projet d’établissement 2024-2028", "/hopital/projet.html"), ("Actualités", "/actualites/index.html")])
    o.append(p("hopital/index.html", "L’hôpital", "Un établissement public de santé au service du bassin d’Issoudun.", m, a, active="hop", kw="presentation etablissement chiffres valeurs mission"))

    m = ("<h2>La gouvernance</h2>" + team(("Directeur", "Marc Kugelstadt. Il assure la gestion administrative, financière et technique."), ("Conseil de surveillance", "Il délibère sur la stratégie et contrôle la gestion de l’établissement."), ("Directoire", "Il conseille le directeur. Il est présidé par le directeur, avec une majorité de personnel médical et pharmaceutique."), ("Commission médicale d’établissement", "Présidée par le Dr Laurent Minois, elle représente le corps médical."), ("Commission de soins (CSIRMT)", "Elle associe les acteurs du soin à la politique de l’établissement."))
      + "<h2>La prise en charge globale</h2>" + team(("Commission des usagers", "Elle veille au respect des droits et à la qualité de l’accueil."), ("CLIN", "Hygiène et lutte contre les infections associées aux soins."), ("Cellule qualité et gestion des risques", "Priorités en qualité et sécurisation des soins."), ("CLUD", "Lutte contre la douleur."), ("CLAN", "Alimentation et nutrition."), ("COMEDIMS", "Bon usage des médicaments et des dispositifs médicaux."))
      + "<h2>Les organigrammes</h2>" + docs(("Organigramme de la direction et des services supports", "2026/11/V3-5.pdf", "Novembre 2026"), ("Organigramme médical", "2026/09/organigramme-medical-VERSION-01102026.pdf", "1er octobre 2026"), ("Organigramme des services", "2024/06/organigramme-des-services-V1-31052024.pdf", "Mai 2024")))
    o.append(p("hopital/organisation.html", "Organisation et instances", "Qui décide, qui contrôle et qui veille à la qualité.", m, active="hop", crumbs=HC2, kw="directeur kugelstadt cme minois organigramme instance cdu clin clud"))

    rows = [("Prise en charge de la douleur, MCO", "100 %", "A", "2024"), ("Prise en charge de la douleur, SMR", "96 %", "A", "2024"), ("Antibiothérapie de 7 jours ou moins", "84 %", "B", "2024"), ("Lettre de liaison à la sortie (deux résultats publiés)", "62/100 et 79/100", "C et B", "2024"), ("Consommation de solutions hydro-alcooliques", "54 %", "C", "2024"), ("Projet de soins, projet de vie", "50/100", "C", "2023")]
    tb = "".join(f'<tr><th scope="row">{e(a)}</th><td class="tn">{e(b)}</td><td>{e(c)}</td><td class="tn">{e(d)}</td></tr>' for a, b, c, d in rows)
    m = ('<div class="callout"><h3>Notre situation aujourd’hui</h3><p>La Haute Autorité de santé a rendu sa décision le 22 mai 2025 : l’établissement n’est pas certifié. Un plan d’action est en cours et la prochaine visite est prévue en 2027.</p></div>'
      '<p>Nous publions cette information parce que votre confiance repose sur la transparence. La décision complète et les indicateurs sont consultables sur <a href="https://www.has-sante.fr/fiche-etablissement/360000038">la fiche de l’établissement sur le site de la HAS</a>.</p>'
      f'<h2>Les indicateurs publiés par la HAS</h2><div class="tbl-wrap"><table class="tbl"><caption class="visually-hidden">Indicateurs de qualité</caption><thead><tr><th scope="col">Indicateur</th><th scope="col">Résultat</th><th scope="col">Niveau</th><th scope="col">Année</th></tr></thead><tbody>{tb}</tbody></table></div>'
      '<p class="meta">Source : fiche HAS de l’établissement, consultée le 4 novembre 2026. L’appréciation globale des patients 2025 n’a pas de résultat publié.</p>'
      '<h2>Comment nous progressons</h2><p>Plusieurs instances pilotent la qualité au quotidien : cellule qualité et gestion des risques, CLIN, CLUD, CLAN, COMEDIMS et Commission des usagers. <a href="/hopital/organisation.html">Découvrir leur rôle</a></p>'
      '<h2>Votre avis compte</h2><p>Une difficulté pendant votre prise en charge ? <a href="/parcours/droits.html">Découvrez comment faire une réclamation</a>.</p>')
    o.append(p("hopital/qualite.html", "Qualité et sécurité des soins", "Nos résultats, publiés tels quels, et les actions en cours.", m, active="hop", crumbs=HC2, kw="certification has qualiscope indicateurs engagements"))

    m = ('<p>Le projet d’établissement fixe la stratégie de l’hôpital pour 2024-2028. Sa construction a débuté par un diagnostic et un séminaire réunissant les personnels et les représentants des usagers.</p><p>Il couvre six volets : médico-soignant, social, qualité, gestion, architectural et fonctions supports.</p><p>Le schéma directeur immobilier, validé par l’ARS, donne la vision à long terme des bâtiments.</p>' + docs(("Lire le projet d’établissement 2024-2028", "https://www.calameo.com/books/0077476583414f59de111", "Version feuilletable")))
    o.append(p("hopital/projet.html", "Projet d’établissement 2024-2028", "Les orientations de l’hôpital pour les prochaines années.", m, active="hop", crumbs=HC2, kw="strategie orientations schema directeur"))
    return o

# ---------- Actualités
OLD = [("Exposition de dessins « Pour Kungur » : résultats du concours", "expositon-talent-pour-le-monde", "20 février 2026"), ("Saint-Valentin : cérémonie et déjeuner aux Reflets d’Argent", "saint-valentin-2026", "16 février 2026"), ("Semaine de l’éducation thérapeutique : une première édition réussie", "semaine-etp", "11 février 2026"), ("Formation : un escape game qui fait voyager dans le temps", "escape-game-formation", "28 janvier 2026"), ("« Festival de la formation » : nos formateurs internes", "festival-de-la-formation", "26 juin 2025"), ("Cancer de la vessie : une opération de sensibilisation", "prevention-cancer-vessie", "23 mai 2025"), ("Covid-19 : retour sur les enseignements de la crise", "covid-enseignements-crise", "28 mars 2025"), ("12e Forum des acteurs de santé", "12eme-forum-des-acteurs-de-sante", "24 février 2025"), ("Bilan et perspectives 2025", "bilan-et-perspectives-2025", "24 janvier 2025"), ("Octobre Rose : un mois de mobilisation", "octobre-rose", "5 novembre 2024"), ("Hand’Iss : 10e édition de la journée handisport", "handiss-10eme-edition", "18 octobre 2024"), ("Bienvenue aux externes du CHRU de Tours", "accueil-externes", "11 septembre 2024"), ("Cinq nouveaux fauteuils pour les soins d’oncologie", "fauteuils-oncologie", "13 août 2024"), ("Vidéos : découvrez nos services sur YouTube", "centre-hospitalier-tour-blanche-youtube", "2 juillet 2024")]
def actualites():
    o = []
    m = ('<ul class="newslist">' + "".join(news_item(n) for n in NEWS) + '</ul><h2 style="margin-top:1.6em">Archives</h2><p>Ces articles restent sur le site actuel.</p><ul>' + "".join(f'<li><a href="{OFFICIAL}{s}/">{e(t)}</a>, {e(d)}</li>' for t, s, d in OLD) + "</ul>")
    o.append(p("actualites/index.html", "Actualités", "La vie de l’hôpital, ses services et ses équipes.", m, active="hop", kw="news evenement presse"))
    for n in NEWS:
        h = phead(n[3], "", [("Actualités", "/actualites/index.html")])
        art = f'<p class="meta"><time datetime="{n[2]}">Publié le {e(n[1])}</time></p>{n[6]}'
        if n[0] == "sorties-velo":
            art += '<figure class="article-photo"><img src="/assets/images/sorties-velo.jpg" alt="Une animatrice accompagne un résident lors d’une sortie en vélo adapté" width="2048" height="1365" loading="lazy"><figcaption>Les sorties en vélo adapté des Reflets d’Argent. Photo : Centre Hospitalier de la Tour Blanche.</figcaption></figure>'
        o.append(page(f"actualites/{n[0]}.html", n[3], n[4], body(art), line=n[5], active="hop", group="Actualités", head=h))
    return o

# ---------- Annuaire
BOOK = [
 ("Urgences et accueil", "urg", [("Urgences et SMUR", "02 54 03 54 00"), ("Accueil et standard", "02 54 03 54 03"), ("Accueil de la rééducation", "02 54 03 56 00")]),
 ("Hospitalisation", "soins", [("Médecine polyvalente, secrétariat", "02 54 03 54 06"), ("Médecine polyvalente, infirmiers", "02 54 03 54 16"), ("Médecine aiguë gériatrique, secrétariat", "02 54 03 63 18"), ("Médecine aiguë gériatrique, infirmiers", "02 54 03 66 15"), ("Hôpital de jour médecine, secrétariat", "02 54 03 63 18"), ("Hôpital de jour médecine, infirmiers", "02 54 03 56 15"), ("Soins de suite, secrétariat", "02 54 03 54 04"), ("Soins de suite polyvalents, infirmiers", "02 54 03 55 22"), ("Soins de suite gériatriques, infirmiers", "02 54 03 66 16")]),
 ("Rééducation", "read", [("Médecine physique et réadaptation", "02 54 03 54 44"), ("Consultations externes", "02 54 03 56 05"), ("Consultations, secrétariat", "02 54 03 54 53"), ("Équipe mobile de réadaptation", "02 54 03 54 31")]),
 ("Consultations et examens", "soins", [("Consultations de spécialistes", "02 54 03 55 06"), ("Consultation gériatrie et chutes", "02 54 03 54 05"), ("Diététique", "02 54 03 63 18"), ("Imagerie médicale", "02 54 03 63 99"), ("Pharmacie, rétrocession au public", "02 54 03 52 00"), ("Pharmacie, service", "02 54 03 54 11"), ("PASS", "02 54 03 54 29")]),
 ("Femmes et naissance", "nais", [("Centre périnatal, santé sexuelle", "02 54 03 54 15")]),
 ("Grand âge", "age", [("EHPAD Bel Air et Les Mésanges", "02 54 03 54 14"), ("EHPAD Les Reflets d’Argent", "02 54 03 46 83"), ("SSIAD et équipe spécialisée Alzheimer", "02 54 03 17 76"), ("La Parenthèse, accueil de jour", "02 54 03 67 14"), ("La Parenthèse, coordonnatrice", "02 54 03 55 58")]),
 ("Formation et emploi", "prev", [("IFAS, secrétariat", "02 54 29 60 31"), ("Affaires médicales", "02 54 03 55 45")]),
]
def annuaire():
    m = '<div class="filter no-print" data-filter-for="book"><input type="search" placeholder="Service ou numéro" aria-label="Filtrer l’annuaire"><span class="count" role="status"></span></div><div id="book">'
    for t, l, rows in BOOK:
        lis = "".join(f'<tr data-row><th scope="row">{e(n)}</th><td style="text-align:right">{tel(ph)}</td></tr>' for n, ph in rows)
        m += f'<section class="l-{l}" data-group><h2 class="tag" style="font-size:1.3rem;color:var(--ink);margin-top:1em">{e(t)}</h2><div class="tbl-wrap"><table class="tbl"><tbody>{lis}</tbody></table></div></section>'
    m += '<p class="empty" hidden>Aucun numéro ne correspond. Appelez le standard au 02 54 03 54 03.</p></div>'
    a = fiche([("Standard", bigtel("02 54 03 54 03")), ("Urgence vitale", '<a class="bigtel" href="tel:15">15</a>')])
    return p("annuaire.html", "Annuaire téléphonique", "Toutes les lignes directes des services.", m, a, kw="telephone numero secretariat joindre")

def documents():
    groups = [
     ("Patients", [("Livret d’accueil", "2023/01/LIVRET-DACCUEIL-CHTB-2019.pdf", "Édition de 2019"), ("Plan du Centre Hospitalier", "2021/12/PLAN-CH-ISSOUDUN-VECTO.pdf"), ("Plaquette des consultations", "2026/10/plaquette-consultations-externes-ebauche-27-05-2026.pdf", "Mai 2026"), ("Plaquette du centre périnatal", "2026/01/plaquette-CPP-13-01-2026.pdf", "Janvier 2026"), ("Plaquette PASS, français", "2025/09/PASS_FLYER_PUBLIC_FR_SEPTEMBRE2025-WEB.pdf", "Septembre 2025"), ("Leaflet PASS, English", "2025/09/PASS_FLYER_PUBLIC_ENG_SEPTEMBRE2025-WEB.pdf", "September 2025"), ("Plaquette de l’hôpital de jour MPR", "2024/06/plaquette-hopital-de-jour-mpr-v06-2024-2.pdf", "Juin 2024")]),
     ("Grand âge", [("Livret du SSIAD", "2025/11/LIVRET-SSIAD-CH-ISSOUDUN_2025.pdf", "2025"), ("Livret de La Parenthèse", "2026/03/LIVRET_AJA_23-03-2026.pdf", "Mars 2026"), ("Trousseau minimum de linge", "2021/12/Trousseau_minimum_de_linge_des_residents_au_moment_de_ladmission.pdf"), ("Charte de la personne âgée dépendante", "2021/12/Charte_des_Droits_de_la_Personne_Agee.pdf"), ("Charte Alzheimer", "2022/01/Charte-Alzheimer-Ethique-et-societe.pdf"), ("Charte de la personne accueillie", "2022/01/exe_a4_accue284e.pdf")]),
     ("Établissement", [("Organigramme de la direction et des supports", "2026/11/V3-5.pdf", "Novembre 2026"), ("Organigramme médical", "2026/09/organigramme-medical-VERSION-01102026.pdf", "1er octobre 2026"), ("Organigramme des services", "2024/06/organigramme-des-services-V1-31052024.pdf", "Mai 2024"), ("Charte du développement durable", "2021/12/charte_DD_2019.pdf", "2019")]),
     ("Professionnels", [("Formulaire de demande d’intervention, équipe mobile", "2026/10/FORMULAIRE-DDE-INTERVENTION.pdf", "Octobre 2026"), ("Plaquette de l’équipe mobile", "2024/05/PLAQUETTE-EQUIPE-MOBILE-SSR-05-2024.pdf", "Mai 2024"), ("Livret des nouveaux arrivants", "2026/03/Livret_nvx_arrivants_mars2026.pdf", "Mars 2026")]),
    ]
    m = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:30px 44px">' + "".join(f"<section><h2>{e(t)}</h2>{docs(*d)}</section>" for t, d in groups) + "</div>"
    return p("documents.html", "Centre de documents", "Les plaquettes, livrets et chartes, au même endroit, avec leur date.", m, active="hop", kw="pdf telecharger plaquette livret charte")

def pro():
    rows = [("Admission à l’hôpital de jour MPR", "Par le logiciel Trajectoire pour un établissement. Sur adressage du médecin pour un patient à domicile.", "/services/hopital-de-jour-mpr.html"), ("Équipe mobile de réadaptation", "Formulaire de demande d’intervention, puis contact avec l’équipe.", "/services/equipe-mobile.html"), ("SSIAD", "Prescription du médecin traitant et entretien infirmier.", "/services/ssiad.html"), ("Équipe spécialisée Alzheimer", "Prescription de 12 à 15 séances de réhabilitation.", "/services/esa.html"), ("Oncologie à l’hôpital de jour", "Coordination avec le Centre de lutte contre le cancer.", "/services/hopital-de-jour.html"), ("PASS", "Pour les patients sans couverture sociale.", "/services/pass.html")]
    m = ('<h2>Adresser un patient</h2><div class="tbl-wrap"><table class="tbl resp"><thead><tr><th scope="col">Service</th><th scope="col">Comment faire</th></tr></thead><tbody>'
      + "".join(f'<tr><th scope="row"><a style="white-space:normal" href="{u}">{e(a)}</a></th><td>{e(b)}</td></tr>' for a, b, u in rows) + "</tbody></table></div>"
      + '<h2>Joindre un service</h2><p>Toutes les lignes directes figurent dans <a href="/annuaire.html">l’annuaire</a>. Les consultations et leurs horaires sont sur <a href="/services/consultations.html">la page dédiée</a>.</p>'
      + '<h2>Formation médicale</h2><p><a href="/carrieres/formation-continue.html">Ressources de la Journée régionale de la médecine d’urgence</a></p>')
    a = fiche([("Urgences", bigtel("02 54 03 54 00")), ("Consultations", tel("02 54 03 55 06")), ("Affaires médicales", tel("02 54 03 55 45"))], docs(("Organigramme médical", "2026/09/organigramme-medical-VERSION-01102026.pdf", "1er octobre 2026"), ("Demande d’intervention, équipe mobile", "2026/10/FORMULAIRE-DDE-INTERVENTION.pdf")), title="Lignes utiles")
    return p("professionnels.html", "Espace professionnels", "Adresser un patient et joindre le bon service : les informations utiles aux médecins de ville et aux établissements.", m, a, active="hop", kw="medecin ville hopital adresser trajectoire relation")

def acces():
    fl = ""
    for n, name, items in LEVELS:
        lis = "".join(f'<li><a href="{u}">{e(t)}</a>{tel(ph)}</li>' for t, u, ph, c in items)
        fl += f'<div class="floor"><div class="lv">{e(n.replace("-", "−"))}<small>{e(name)}</small></div><ul>{lis}</ul></div>'
    m = (f'<h2>Le pavillon Marie Curie, niveau par niveau</h2><div class="stack">{fl}</div>'
      '<h2>Les autres bâtiments</h2>' + ul('<a href="/services/mpr.html">Bâtiment MPR</a> : rééducation, consultations externes et hôpital de jour', '<a href="/services/ehpad-reflets-argent.html">EHPAD Les Reflets d’Argent</a>, dans l’enceinte de l’hôpital. La <a href="/services/pass.html">PASS</a> est au rez-de-chaussée', '<a href="/services/la-parenthese.html">La Parenthèse</a>, accueil de jour Alzheimer', '<a href="/services/ehpad-bel-air.html">EHPAD Bel Air</a> : 26 avenue du Père Noir, à 3 km de l’hôpital')
      + '<h2>Se repérer sur place</h2>' + docs(("Plan du Centre Hospitalier", "2021/12/PLAN-CH-ISSOUDUN-VECTO.pdf")))
    a = fiche([("Adresse", "Avenue Jean Bonnefont<br>36100 Issoudun"), ("Courrier", "CS 70190<br>36105 Issoudun Cedex"), ("Standard", bigtel("02 54 03 54 03")), ("Itinéraire", '<a href="https://g.page/CH-ISSOUDUN">Ouvrir dans Google Maps</a>')])
    return p("acces.html", "Venir à l’hôpital", "L’adresse, le plan et chaque service à son niveau.", m, a, kw="adresse plan parking itineraire niveau etage acces venir")

def contact():
    m = ('<div class="callout warn"><h3>Une urgence médicale ?</h3><p>Appelez le <a href="tel:15">15</a> ou le <a href="tel:112">112</a>. La messagerie de l’établissement ne prend pas en charge les urgences.</p></div>'
      '<h2>Le bon interlocuteur pour votre demande</h2><div class="field"><label for="motif">Votre demande concerne</label><select id="motif" data-motif><option value="">Choisissez un motif</option><option value="rdv">Prendre un rendez-vous</option><option value="dossier">Obtenir mon dossier médical</option><option value="facture">Une facture</option><option value="ehpad">Une entrée en EHPAD</option><option value="emploi">Un emploi ou un stage</option><option value="autre">Une autre question</option></select></div>'
      '<div class="callout" data-motif-panel="rdv" hidden><h3>Rendez-vous et consultations</h3><p>Contactez directement le secrétariat du service. Retrouvez les numéros et les jours de consultation dans <a href="/services/consultations.html">le tableau des consultations</a>, ou consultez <a href="/annuaire.html">l’annuaire téléphonique</a>.</p></div>'
      '<div class="callout" data-motif-panel="dossier" hidden><h3>Votre dossier médical</h3><p>La demande se fait par courrier à la direction. Retrouvez les justificatifs nécessaires et les modalités de retrait.</p><a class="btn" href="/parcours/dossier-medical.html">Voir la marche à suivre</a></div>'
      '<div class="callout" data-motif-panel="facture" hidden><h3>Frais et facturation</h3><p>Le bureau des admissions peut vous expliquer votre facture. Le standard vous orientera vers le bon interlocuteur.</p><a href="/parcours/frais.html">Comprendre les frais d’hospitalisation</a></div>'
      '<div class="callout" data-motif-panel="ehpad" hidden><h3>Une entrée en EHPAD</h3><p>Consultez les conditions, les pièces à réunir et les contacts pour préparer une admission.</p><a class="btn" href="/hebergement/admission.html">Préparer la demande d’admission</a></div>'
      '<div class="callout" data-motif-panel="emploi" hidden><h3>Rejoindre l’établissement</h3><p><a href="/carrieres/index.html">Consulter les offres d’emploi</a> ou <a href="/carrieres/stages.html">préparer une demande de stage</a>.</p></div>'
      '<div class="callout" data-motif-panel="autre" hidden><h3>Nous écrire</h3><p>Pour une question administrative ou générale : <a href="mailto:contact@ch-issoudun.fr">contact@ch-issoudun.fr</a>. N’envoyez pas de dossier médical ni d’information de santé par cette messagerie.</p><a class="btn" href="mailto:contact@ch-issoudun.fr">Ouvrir ma messagerie</a></div>'
      '<h2>Vous préférez nous appeler ?</h2><p>Le standard vous oriente vers le service ou le professionnel recherché.</p>' + bigtel("02 54 03 54 03")
      + '<h2>Un courrier à nous adresser</h2><p>Centre Hospitalier de la Tour Blanche<br>Avenue Jean Bonnefont, CS 70190<br>36105 Issoudun Cedex</p><p>Précisez le service ou le destinataire concerné.</p>')
    a = fiche([("Standard", bigtel("02 54 03 54 03")), ("E-mail", '<a href="mailto:contact@ch-issoudun.fr">contact@ch-issoudun.fr</a>'), ("Adresse", "Avenue Jean Bonnefont<br>CS 70190<br>36105 Issoudun Cedex")])
    return p("contact.html", "Nous contacter", "Un rendez-vous, une démarche ou une question : trouvez le bon interlocuteur.", m, a, kw="contact email ecrire joindre")

def legal():
    o = []
    m = ('<h2>Établissement présenté</h2><p>Centre Hospitalier de la Tour Blanche, établissement public de santé<br>Avenue Jean Bonnefont, 36105 Issoudun<br>SIRET 263 600 090 00017. TVA FR 22 263600090. Code NAF 8610Z.<br>' + f'{tel("02 54 03 54 03")}, <a href="mailto:contact@ch-issoudun.fr">contact@ch-issoudun.fr</a></p>'
      '<h2>À propos de cette version</h2><p>Cette seconde proposition de refonte est réalisée par Escale Digitale Solutions. Elle est présentée sur ChatGPT Sites. Elle n’est pas le site officiel de l’établissement. Le domaine officiel reste <a href="https://www.ch-issoudun.fr/">www.ch-issoudun.fr</a>.</p><p>La publication institutionnelle, ses mentions légales définitives et les informations opérationnelles devront être validées par l’établissement avant leur transfert sur son domaine.</p>'
      '<h2>Données personnelles</h2><p>Les pages n’ajoutent aucun traceur publicitaire ni outil de mesure d’audience. Vos réglages de lecture et votre liste de préparation restent enregistrés sur votre appareil. Le site ne collecte aucun message ni dossier médical : les liens de contact ouvrent votre téléphone ou votre messagerie. L’hébergement de cette version est assuré par ChatGPT Sites. Les questions posées à l’assistant documentaire sont traitées dans votre navigateur, sans envoi à un service d’intelligence artificielle ni enregistrement de la conversation.</p>'
      '<p>Vous disposez d’un droit d’accès, de rectification et de suppression de vos données, et d’un droit de réclamation auprès de la CNIL. Contact : <a href="mailto:contact@ch-issoudun.fr">contact@ch-issoudun.fr</a>.</p>')
    o.append(p("mentions-legales.html", "Mentions légales et données personnelles", "Les informations légales du site et l’usage de vos données.", m, kw="rgpd cookies dpo cnil"))
    m = ('<p>Cette proposition vise une navigation accessible à tous. Une évaluation complète au regard du Référentiel général d’amélioration de l’accessibilité (RGAA) reste nécessaire. <strong>Aucun audit n’ayant été réalisé, le site est déclaré non conforme.</strong></p>'
      '<h2>Les aides à votre disposition</h2>' + ul("Navigation complète au clavier", "Liens d’évitement et fil d’Ariane", "Taille du texte et contraste réglables", "Respect du réglage « réduire les animations »")
      + '<h2>Signaler un problème</h2><p>Si vous ne pouvez pas accéder à un contenu, écrivez à <a href="mailto:contact@ch-issoudun.fr">contact@ch-issoudun.fr</a>. Sans réponse satisfaisante, vous pouvez saisir le Défenseur des droits.</p>')
    o.append(p("accessibilite.html", "Accessibilité", "Le niveau d’accessibilité de ce site et comment signaler un problème.", m, kw="rgaa handicap malvoyant"))
    return o

def sitemap(all_pages):
    groups = {}
    order = ["Pages principales"]
    for pg in sorted(all_pages, key=lambda x: x["u"]):
        d = pg["u"].split("/")[0] if "/" in pg["u"] else "Pages principales"
        name = {"services": "Soins et services", "parcours": "Votre parcours", "hebergement": "EHPAD", "prevention": "Prévention", "carrieres": "Carrières", "hopital": "L’hôpital", "actualites": "Actualités"}.get(d, "Pages principales")
        groups.setdefault(name, []).append(pg)
    m = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px 44px">'
    for g, ps in groups.items():
        m += f'<section><h2>{e(g)}</h2><ul>' + "".join(f'<li><a href="/{x["u"]}">{e(x["t"])}</a></li>' for x in ps) + "</ul></section>"
    m += "</div>"
    return p("plan-du-site.html", "Plan du site", "Toutes les pages du site.", m)

def notfound():
    return p("404.html", "Page introuvable", "Cette adresse ne correspond à aucune page. Elle a peut-être changé avec le nouveau site.",
      '<p>Essayez la recherche, ou repartez d’une de ces pages :</p>' + stations([("Accueil", "/index.html"), ("Tous les services", "/services/index.html"), ("Annuaire téléphonique", "/annuaire.html")], "soins"))

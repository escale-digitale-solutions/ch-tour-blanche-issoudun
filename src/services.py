"""Fiches services. Tous les faits viennent du site actuel (audit du 04/11/2026)."""
from core import *

MC = "Pavillon Marie Curie"
HUB = [("Soins et services", "/services/index.html")]
SAMU = "Adresser un patient : <a href=\"/professionnels.html\">espace professionnels</a>"

def svc(slug, name, line, group, active, lead, main, aside, kw="", next_=None):
    h = phead(name, lead, HUB if not group.startswith("EHPAD") else HUB + [("EHPAD", "/services/ehpad.html")], group)
    b = body(main, aside)
    if next_:
        b += f'<div class="nextline"><div class="wrap ln l-{line}"><h2 style="font-size:1.25rem;margin-bottom:12px">Sur la même ligne</h2>{stations(next_)}</div></div>'
    return page(f"services/{slug}.html", name, re.sub("<[^>]+>", "", lead), b, line=line, active=active, group=group, kw=kw, head=h)

HOSP = [("Médecine polyvalente", "/services/medecine-polyvalente.html"), ("Médecine aiguë gériatrique", "/services/medecine-geriatrique.html"),
        ("Hôpital de jour médecine", "/services/hopital-de-jour.html"), ("Soins de suite polyvalents", "/services/soins-de-suite-polyvalents.html"),
        ("Soins de suite gériatriques", "/services/soins-de-suite-geriatriques.html")]
def others(lst, slug): return [x for x in lst if slug not in x[1]]

COMMON_ROOM = ("<h2>Chambres</h2><p>Les chambres sont individuelles ou à deux lits, avec cabinet de toilette, lavabo et WC. "
               "Une douche est à la disposition des patients autonomes. Une salle de bain équipée d’un chariot douche est réservée aux patients plus dépendants.</p>")
STAGE = "<p>Des stagiaires et des élèves travaillent régulièrement dans le service, encadrés par les professionnels.</p>"

def all_services():
    out = []
    out.append(svc("medecine-polyvalente", "Médecine polyvalente", "soins", "Hospitalisation", "soins",
      "Une unité de 30 lits, dont 4 lits identifiés de soins palliatifs, pour des personnes souvent âgées, atteintes de plusieurs maladies et à risque de perdre leur autonomie.",
      "<h2>Motifs d’hospitalisation les plus fréquents</h2><p>Le service prend en charge les pathologies médicales aiguës :</p>"
      + ul("cardiaques", "respiratoires et pulmonaires", "gastriques", "neurologiques", "cancéreuses")
      + '<div class="callout"><p>Les pathologies traumatiques nécessitant une intervention chirurgicale ne sont pas prises en charge dans le service.</p></div>'
      + "<h2>L’équipe</h2>" + team(("Cheffe de service", "Dr Ribeiro"), ("Médecins", "Dr Abdelalim, Dr Daffe, Dr Dairi, Dr Granger (cardiologie), Dr Jouini, Dr Layouni"), ("Cadre de santé", f"Mme Lachaise, {tel('02 54 03 55 59')}"), ("Soignants", "Infirmiers, aides-soignants, agents de service hospitalier, brancardiers"))
      + "<p>Kinésithérapeutes, ergothérapeutes, diététicienne, assistant social, psychologue et cardiologue interviennent également.</p>"
      + "<h2>Soins palliatifs et accompagnement</h2><p>Le service travaille avec l’Équipe d’appui départementale en soins palliatifs de l’Indre (EADSP 36). "
        "Les bénévoles de l’association ALAVI, formés à l’écoute, et ceux de Culture et Loisirs, pour la lecture et les visites, interviennent auprès des patients.</p>"
      + "<h2>Pour les proches</h2><p>Un espace d’accueil est réservé aux familles et aux proches qui accompagnent un patient, notamment pour les repas. Il leur est également possible de dormir sur place.</p>",
      fiche([("Secrétariat", bigtel("02 54 03 54 06")), ("Infirmiers", tel("02 54 03 54 16")), ("Où", f"{MC}, 2e étage"), ("Capacité", "30 lits, dont 4 de soins palliatifs")]),
      "soins palliatifs ribeiro hospitalisation lachaise", others(HOSP, "medecine-polyvalente")))

    out.append(svc("medecine-geriatrique", "Médecine aiguë gériatrique", "soins", "Hospitalisation", "soins",
      "Une unité de 20 lits pour poser un diagnostic et traiter une crise de santé chez la personne âgée, en lien direct avec la filière gériatrique.",
      "<h2>Rôle du service</h2><p>Les hospitalisations ont d’abord un but de diagnostic et de traitement. Elles permettent de gérer un état de crise, le plus souvent déclenché par une maladie qui retentit gravement sur l’autonomie et la vie sociale de la personne âgée.</p>"
      + "<h2>Motifs d’hospitalisation les plus fréquents</h2>"
      + ul("Bilan de chutes", "Maladie d’Alzheimer ou maladies apparentées", "Troubles de l’humeur, dépression, anxiété", "Pathologies ostéo-articulaires", "Maladie de Parkinson", "Accident vasculaire cérébral", "Insuffisance cardiaque ou rénale", "Diabète", "Hémopathie et cancer", "Ulcères")
      + COMMON_ROOM + "<h2>L’équipe</h2>"
      + team(("Cheffe d’unité fonctionnelle", "Dr Chetoui"), ("Médecins", "Dr Abdenouri, Dr Aouini, Dr Skhiri"), ("Cadre de santé", "Mme Delohen"), ("Soignants", "Infirmiers, aides-soignants, agents de service hospitalier, brancardiers"))
      + "<p>Kinésithérapeutes, diététicienne, assistant social, psychologue et cardiologue interviennent également. Deux personnes formées proposent des soins esthétiques et de la relaxation par réflexologie plantaire.</p>" + STAGE,
      fiche([("Secrétariat", bigtel("02 54 03 63 18")), ("Infirmiers", tel("02 54 03 66 15")), ("Où", f"{MC}, 1er étage"), ("Capacité", "20 lits")]),
      "geriatrie aigue chetoui personne agee chute", others(HOSP, "medecine-geriatrique")))

    out.append(svc("hopital-de-jour", "Hôpital de jour médecine", "soins", "Hospitalisation", "soins",
      "Des soins sur la journée, près de chez vous : chimiothérapie, transfusions, bilans de mémoire ou de chutes, consultations de la douleur.",
      "<h2>Soins proposés</h2>" + ul("Chimiothérapie", "Photobiomodulation, pour traiter les mucites liées à la chimiothérapie", "Transfusions", "Consultations de la douleur et soins de support", "Traitements injectables", "Ponctions d’ascite ou pleurale, saignées", "Consultations d’endocrino-diabétologie et pose de pompe à insuline", "Bilans mémoire, à partir de 70 ans", "Bilans chute")
      + "<h2>Oncologie de proximité</h2><p>Le service accueille les patients suivis par un médecin du bassin d’Issoudun ou par un centre éloigné de leur domicile, en coordination avec le Centre de lutte contre le cancer. "
        "Une convention avec le Centre d’oncologie et de radiothérapie de Saint-Doulchard assure la continuité des soins. Un oncologue-radiothérapeute intervient 3 matinées par mois et une présence médicale est assurée chaque semaine.</p>"
      + "<p>Cinq fauteuils de soins ont été installés en 2024. Près de 300 personnes avaient été prises en charge en oncologie l’année précédente.</p>"
      + "<h2>Soins de support</h2><p>Diététicienne, assistante sociale, psychologue, bénévoles, soins de bien-être, réflexologie plantaire et soins socio-esthétiques adaptés à l’oncologie complètent la prise en charge.</p>"
      + "<h2>Sécurité de la prise en charge</h2><p>Le service s’appuie sur les urgences et l’imagerie de l’hôpital, sur des admissions directes en médecine et sur des lits identifiés de soins palliatifs.</p>"
      + "<h2>L’équipe</h2>" + team(("Cheffe de service", "Dr Ribeiro"), ("Oncologues", "Dr Cherkaoui, Dr Nekmouche"), ("Oncologue-radiothérapeute", "Dr Compagnon, Centre Saint-Jean de Saint-Doulchard"), ("Diabétologie et endocrinologie", "Dr Suruceanu"), ("Bilans mémoire", "Dr Tallier-Huglo"), ("Cadre de santé", f"Mme Delohen, {tel('02 54 03 55 04')}"))
      + "<h2>Partenaires</h2><p>Unité de reconstitution de chimiothérapie de Vierzon, Centre Saint-Jean de Saint-Doulchard, CHU et CHR de la région Centre-Val de Loire, établissements du territoire, établissements privés et hospitalisation à domicile.</p>",
      fiche([("Secrétariat", bigtel("02 54 03 63 18")), ("Infirmiers", tel("02 54 03 56 15") + '<br><a href="mailto:ide.hdj@ch-issoudun.fr">ide.hdj@ch-issoudun.fr</a>'), ("Où", f"{MC}, 1er étage"), ("Ouverture", "Du lundi au vendredi, de 8 h 30 à 18 h"), ("Sur place", "Repas fournis, télévision, 6 places")]),
      "chimiotherapie cancer oncologie photobiomodulation mucite diabete memoire", others(HOSP, "hopital-de-jour")))

    SMR = '<div class="callout"><p>Les soins de suite sont aussi appelés soins médicaux et de réadaptation (SMR).</p></div>'
    out.append(svc("soins-de-suite-polyvalents", "Soins de suite polyvalents", "soins", "Hospitalisation", "soins",
      "Une unité de 20 lits pour retrouver des forces et de l’autonomie avant de rentrer chez soi, après une opération ou une maladie aiguë.",
      SMR + "<h2>Pour qui</h2><p>Le service accueille des patients en convalescence après une intervention chirurgicale ou une pathologie aiguë, ainsi que des patients atteints de pathologies oncologiques. Il facilite le rapprochement familial des patients du bassin d’Issoudun.</p>"
      + "<h2>Objectif</h2><p>Stabiliser l’état physique et gagner en autonomie pour préparer au mieux le retour à domicile. Un kinésithérapeute intervient chaque jour. Le plateau technique et des séances de balnéothérapie sont accessibles si nécessaire.</p>"
      + COMMON_ROOM + "<h2>Vie dans le service</h2><p>Le service dispose d’un petit salon et d’une salle à manger. Des permissions sont possibles pendant le séjour, après validation du chef de service.</p>"
      + "<h2>L’équipe</h2>" + team(("Chef de service", "Dr Tallier-Huglo"), ("Médecins", "Dr Masabo, Dr Nsibi, Dr Sayhi"), ("Cadre de santé", "Mme Duguet"), ("Soignants", "Infirmiers, aides-soignants, agents de service hospitalier, brancardiers"))
      + "<p>Kinésithérapeutes, ergothérapeutes, diététicienne, assistant social, psychologue et cardiologue interviennent également.</p>" + STAGE,
      fiche([("Secrétariat", bigtel("02 54 03 54 04")), ("Infirmiers", tel("02 54 03 55 22")), ("Où", f"{MC}, 1er étage"), ("Capacité", "20 lits")]),
      "smr ssr convalescence reeducation", others(HOSP, "soins-de-suite-polyvalents")))

    out.append(svc("soins-de-suite-geriatriques", "Soins de suite gériatriques", "soins", "Hospitalisation", "soins",
      "Une unité de 18 lits pour les personnes très âgées en perte d’autonomie physique, psychique ou sociale.",
      SMR + "<h2>Pour qui</h2><p>Les patients viennent surtout de la médecine aiguë gériatrique, des services médicaux et chirurgicaux du Berry ou de la médecine polyvalente d’Issoudun.</p>"
      + "<h2>Ce que fait le service</h2>" + ul("Limiter les handicaps physiques", "Accompagner le patient et son entourage", "Poursuivre les soins et le traitement", "Réaliser une évaluation gériatrique globale et prévenir les aggravations", "Prendre en charge les décompensations médicales multiples", "Préparer le retour à domicile ou l’entrée en structure", "Accompagner la fin de vie")
      + COMMON_ROOM + "<h2>Vie dans le service</h2><p>Le service dispose d’un petit salon et d’une salle à manger. Le chef de service peut valider des permissions.</p>"
      + "<h2>L’équipe</h2>" + team(("Cheffe de service", "Dr Tallier-Huglo"), ("Médecins", "Dr Chetoui, Dr Masabo, Dr Sayhi"), ("Cadre de santé", "Mme Duguet"), ("Soignants", "Infirmiers, aides-soignants, agents de service hospitalier, brancardiers"))
      + "<p>Kinésithérapeutes, ergothérapeutes, diététicienne, assistant social, psychologue et cardiologue interviennent également.</p>" + STAGE,
      fiche([("Secrétariat", bigtel("02 54 03 54 04")), ("Infirmiers", tel("02 54 03 66 16")), ("Où", f"{MC}, 1er étage"), ("Capacité", "18 lits")]),
      "smr ssr geriatrie personne agee", others(HOSP, "soins-de-suite-geriatriques")))

    READ = [("Médecine physique et réadaptation", "/services/mpr.html"), ("Hôpital de jour MPR", "/services/hopital-de-jour-mpr.html"), ("Équipe mobile de réadaptation", "/services/equipe-mobile.html")]
    out.append(svc("mpr", "Médecine physique et réadaptation", "read", "Rééducation", "soins",
      "Le centre de rééducation d’Issoudun, ouvert en 1995, répond aux besoins de rééducation et de réadaptation fonctionnelles du département et de la région.",
      '<ul class="facts"><li><b>66</b><span>lits d’hospitalisation complète</span></li><li><b>13</b><span>lits d’hospitalisation de semaine</span></li><li><b>6</b><span>lits pour états végétatifs chroniques et pauci-relationnels</span></li><li><b>15</b><span>places d’hospitalisation de jour</span></li></ul>'
      + "<h2>Pathologies de l’adulte prises en charge</h2><h3>Affections neurologiques</h3>" + ul("Accident vasculaire cérébral", "Traumatisme crânien", "Atteintes médullaires : paraplégie, tétraplégie", "Affections dégénératives : sclérose en plaques, maladie de Parkinson, sclérose latérale amyotrophique")
      + "<h3>Affections traumatiques, rhumatologiques ou vasculaires</h3>" + ul("Traumatologie des membres et du rachis", "Traumatologie du sport", "Amputations", "Arthroplasties et chirurgie de réparation", "Lombalgies chroniques, avec un programme de restauration fonctionnelle du rachis")
      + "<h3>États végétatifs chroniques et pauci-relationnels</h3><p>Le service dispose de 6 lits dédiés à ces patients.</p>"
      + "<h2>Éducation thérapeutique</h2><p>L’équipe propose des programmes pour les patients amputés des membres inférieurs et pour les personnes vivant avec un handicap neurologique central, ainsi que des ateliers transverses.</p>"
      + "<h2>Plateau technique</h2><p>Kinésithérapie, ergothérapie, balnéothérapie, orthophonie et appareillage. Le service a réintégré ses locaux en 2025, après d’importants travaux dans l’aile concernée.</p><p>Chaque année, le service organise avec l’association ARCHI la journée handisport Hand’Iss, dont la 10e édition a réuni environ 250 participants en 2024.</p>"
      + "<h2>L’équipe</h2>" + team(("Chef de service", "Dr Éric Tallier"), ("Médecins", "Dr Chekrouni, Dr Cornette, Dr Molcard, Dr Mundreuil, Dr Pisciotta, Dr Pontis, Dr Rabemanontany, Dr Ribeiro (bilans urodynamiques), Dr Tamasag"), ("Cadre de santé, hospitalisation", "Mme Potin"), ("Cadre de santé, plateau technique", "M. Pinto"))
      + '<h2>Consultations externes</h2><p>Consultations MPR, médecine du sport, toxine botulique, bilans urodynamiques et restauration fonctionnelle du rachis : retrouvez <a href="/services/consultations.html#readaptation">les médecins et leurs horaires</a>.</p>',
      fiche([("Service", bigtel("02 54 03 54 44")), ("Accueil", tel("02 54 03 56 00")), ("Secrétariat des consultations", f"{tel('02 54 03 54 53')} ou {tel('02 54 03 56 05')}, du lundi au vendredi, de 9 h à 12 h"), ("Où", "Bâtiment MPR")],
            docs(("Plaquette de l’équipe mobile", "2024/05/PLAQUETTE-EQUIPE-MOBILE-SSR-05-2024.pdf"))),
      "reeducation rehabilitation kine balneotherapie avc paraplegie handicap ssr smr tallier mpr", others(READ, "/mpr")))

    out.append(svc("hopital-de-jour-mpr", "Hôpital de jour MPR", "read", "Rééducation", "soins",
      "Un programme de rééducation personnalisé sur la journée, en venant de chez vous ou en sortant d’hospitalisation. 15 places.",
      "<h2>Votre prise en charge</h2>" + steps(("Un bilan initial.", " Le médecin référent et les professionnels de rééducation évaluent votre situation."), ("Un programme personnalisé.", " Les soins sont individuels. Des activités collectives sont possibles, comme un atelier d’éducation thérapeutique."), ("Un suivi régulier.", " Le médecin coordonne l’ensemble. Il fixe la durée du séjour avec les thérapeutes et la réévalue selon vos besoins."))
      + "<h2>Comment être admis</h2><h3>Depuis votre domicile</h3><p>Votre médecin traitant ou un spécialiste vous adresse au service. Un médecin du service vous reçoit en consultation et décide de l’admission.</p>"
      + "<h3>Depuis un autre établissement</h3><p>La demande passe par le logiciel Trajectoire. Une consultation avec un médecin du service précède la programmation de l’admission.</p>"
      + "<h3>Depuis le Centre Hospitalier</h3><p>Vous passez de l’hospitalisation complète à l’hospitalisation de jour. Le planning vous est remis à la sortie et la même équipe assure votre suivi.</p>"
      + "<h2>Votre transport</h2><p>Le service est conventionné par la Sécurité sociale et agréé par les mutuelles. Selon la réglementation, les transports adaptés à votre état de santé (ambulance, VSL, taxi) peuvent être pris en charge par l’Assurance Maladie pour le trajet entre votre domicile et l’hôpital de jour.</p>",
      fiche([("Rendez-vous", bigtel("02 54 03 56 05")), ("Où", "Bâtiment MPR, rez-de-chaussée"), ("Capacité", "15 places")],
            docs(("Plaquette de présentation", "2024/06/plaquette-hopital-de-jour-mpr-v06-2024-2.pdf", "Juin 2024"))),
      "reeducation jour trajectoire", others(READ, "hopital-de-jour-mpr")))

    out.append(svc("equipe-mobile", "Équipe mobile de réadaptation du Berry", "read", "Rééducation", "soins",
      "Une équipe qui intervient dans le Cher et l’Indre, auprès des adultes en difficulté dans leur vie quotidienne après une atteinte cérébrale, corporelle, sensorielle ou liée à l’âge.",
      "<h2>Ses objectifs</h2>" + ul("Favoriser le maintien à domicile et l’adaptation du logement", "Développer l’autonomie", "Construire le projet social de la personne", "Faciliter les soins par les intervenants") + "<h2>Pour qui</h2><p>Les personnes de plus de 18 ans, à domicile, dans le Cher et l’Indre.</p><h2>Demander une intervention</h2><p>Remplissez le formulaire de demande, puis contactez l’équipe.</p>",
      fiche([("Téléphone", bigtel("02 54 03 54 31")), ("Secteur", "Cher et Indre")], docs(("Plaquette de présentation", "2024/05/PLAQUETTE-EQUIPE-MOBILE-SSR-05-2024.pdf", "Mai 2024"), ("Formulaire de demande d’intervention", "2026/10/FORMULAIRE-DDE-INTERVENTION.pdf", "Octobre 2026"))),
      "domicile handicap smr ssr adaptation logement", others(READ, "equipe-mobile")))

    # Consultations
    rows = [
     ("Addictologie", "Dr Pujo", "Mardi 10 h 30 à 11 h 50, vendredi 14 h 40 à 16 h 50", "2,5"), ("Allergologie", "Dr Pauquet", "2 semaines par mois", ""),
     ("Chirurgie orthopédique", "Dr Acosta", "Jeudi 9 h à 12 h 45", "4"), ("Chirurgie orthopédique", "Dr Tallier E.", "Lundi 10 h à 12 h", "1"),
     ("Chirurgie vasculaire", "Dr Vignes-Oudot", "Jeudi 14 h 25 à 16 h", "4"), ("Chirurgie viscérale", "Dr Batoko", "Mercredi 10 h à 13 h", "3"),
     ("Chirurgie viscérale", "Dr Vinet", "Mercredi 8 h 30 à 11 h 45", "3"), ("Dermatologie", "Dr Ferrandiz", "Mardi 11 h à 12 h 15 et 13 h 30 à 16 h 45", "2"),
     ("Néphrologie", "Dr Brillet", "Mardi après-midi", "2"), ("Neurologie", "Dr Daffe", "Lundi et jeudi 14 h à 16 h", "1,4"),
     ("ORL", "Dr Alrajeh", "Lundi 10 h à 12 h et 13 h 45 à 15 h 30", "1"), ("Pneumologie et allergologie", "Dr Cotte", "Du mardi au vendredi 8 h 45 à 10 h 45", "2,3,4,5"),
     ("Rhumatologie", "Dr Rolland", "Lundi 10 h à 12 h et 14 h à 17 h 30", "1"), ("Urologie", "Dr Aad", "Mercredi 10 h 40 à 12 h 25 et 14 h à 15 h 20", "3"),
     ("Soins non programmés", "Dr Ribeiro", "Du lundi au vendredi", "1,2,3,4,5"),
    ]
    tr = lambda r, t: (f'<tr data-row data-days="{r[3]}"><th scope="row">{e(r[0])}</th><td>{e(r[1])}</td><td>{e(r[2])}</td><td>{tel(t)}</td></tr>')
    ext = [("Gériatrie et chutes", "Dr Tallier L.", "Mardi et mercredi 14 h à 17 h", "2,3"), ("Diététique", "Mme Chichery", "Mercredi 14 h à 16 h 30, vendredi 9 h à 13 h", "3,5")]
    mpr = [("MPR, rééducation", "Dr Molcard", "Mardi matin", "2"), ("MPR, rééducation", "Dr Pisciotta", "Mardi matin", "2"), ("Toxine botulique, bilans urodynamiques", "Dr Mundreuil", "Jeudi", "4"),
           ("MPR, médecine du sport", "Dr Cornette", "Mercredi et vendredi, jeudi après-midi", "3,4,5"), ("Toxine botulique", "Dr Cornette", "Lundi matin", "1"), ("Chirurgie orthopédique", "Dr Tallier E.", "Mercredi après-midi", "3"),
           ("MPR, restauration fonctionnelle du rachis", "Dr Tamasag", "Mercredi matin", "3"), ("Bilans urodynamiques", "Dr Tamasag", "Mardi matin", "2"), ("MPR", "Dr Pontis S.", "Lundi matin", "1"), ("Toxine botulique", "Dr Pontis S.", "Lundi après-midi", "1"), ("Bilans urodynamiques", "Dr Ribeiro", "Vendredi après-midi", "5")]
    thead = '<thead><tr><th scope="col">Spécialité</th><th scope="col">Médecin</th><th scope="col">Jours et horaires</th><th scope="col">Rendez-vous</th></tr></thead>'
    main = ('<div class="callout"><h3>Avant chaque consultation</h3><p>Passez au bureau des admissions avec votre carte Vitale et votre carte de mutuelle. Il se trouve dans le hall du pavillon Marie Curie et à l’entrée du service de rééducation.</p></div>'
      '<div class="filter no-print" data-filter-for="tbl-c"><input type="search" placeholder="Spécialité ou médecin" aria-label="Filtrer par spécialité ou médecin"><button class="chip" type="button" aria-pressed="false" data-f="today">Aujourd’hui</button><span class="count" role="status"></span></div>'
      f'<div class="tbl-wrap" id="tbl-c"><table class="tbl resp"><caption class="visually-hidden">Consultations de spécialistes</caption>{thead}<tbody data-group><tr><th colspan="4" class="grp" scope="colgroup">Pavillon Marie Curie, secrétariat des consultations</th></tr>'
      + "".join(tr(r, "02 54 03 55 06") for r in rows) + "".join(tr(r, "02 54 03 54 05" if r[0].startswith("Gér") else "02 54 03 63 18") for r in ext) + "</tbody>"
      + f'<tbody data-group id="readaptation"><tr><th colspan="4" class="grp" scope="colgroup">Rééducation, secrétariat de 9 h à 12 h</th></tr>' + "".join(tr(r, "02 54 03 54 53") for r in mpr) + "</tbody></table><p class=\"empty\" hidden>Aucune consultation ne correspond à votre recherche.</p></div>"
      + '<h2>Gynécologie et suivi de grossesse</h2><p>Les consultations ont lieu au <a href="/services/centre-perinatal.html">centre périnatal de proximité</a>, sur rendez-vous au ' + tel("02 54 03 54 15") + ".</p>"
      + '<h2>Imagerie</h2><p>Radiologie, scanner et échographie sont réalisés sur rendez-vous : consultez la page <a href="/services/imagerie.html">imagerie médicale</a>.</p>')
    out.append(svc("consultations", "Consultations de spécialistes", "soins", "Consultations et examens", "soins",
      "Quinze spécialités consultent à Issoudun. Filtrez par spécialité ou affichez les consultations d’aujourd’hui.", main,
      fiche([("Rendez-vous", bigtel("02 54 03 55 06")), ("Horaires du secrétariat", "Du lundi au vendredi, de 9 h à 17 h"), ("Rendez-vous en rééducation", f"{tel('02 54 03 54 53')} ou {tel('02 54 03 56 05')}, de 9 h à 12 h"), ("Où", f"{MC}, rez-de-chaussée. Gériatrie : 1er étage"), ("Prise de rendez-vous", "Par téléphone uniquement")],
            docs(("Plaquette des consultations", "2026/10/plaquette-consultations-externes-ebauche-27-05-2026.pdf", "Mai 2026"))),
      "rendez vous rdv specialiste dermatologue orl urologue rhumatologue neurologue pneumologue allergologue addictologie chirurgien dieteticienne ophtalmologie"))

    out.append(svc("imagerie", "Imagerie médicale", "soins", "Consultations et examens", "soins",
      "Radiologie conventionnelle, scanner et échographie, pour les patients hospitalisés, les urgences et les consultations externes.",
      "<h2>Examens proposés</h2>" + ul("Radiologie conventionnelle", "Scanner", "Échographie") + "<p>L’activité est assurée pour les urgences 24 h sur 24. Des radiographies et des échographies peuvent être réalisées au lit du patient.</p>"
      + "<h2>L’équipe</h2>" + team(("Cheffe de service", "Dr Pontis"), ("Radiologues", "Dr Pontis, Dr Rakotonaivo"), ("Cadre de santé", "M. Piedois"), ("Soignants", "Manipulateurs en électroradiologie médicale, infirmière, secrétariat médical")),
      fiche([("Rendez-vous", bigtel("02 54 03 63 99")), ("E-mail", '<a href="mailto:imagerie@ch-issoudun.fr">imagerie@ch-issoudun.fr</a>'), ("Accueil téléphonique", "Du lundi au vendredi, de 9 h 30 à 12 h 30 et de 13 h 30 à 16 h 15"), ("Secrétariat", "Du lundi au vendredi, de 8 h 30 à 17 h 30"), ("Où", f"{MC}, sous-sol (niveau -1)")]),
      "radio radiologie scanner echographie irm examen"))

    out.append(svc("pharmacie", "Pharmacie", "soins", "Consultations et examens", "soins",
      "La pharmacie de l’hôpital délivre aussi au public certains médicaments absents des pharmacies de ville : c’est la rétrocession.",
      "<h2>La délivrance au public</h2><p>Cette mission s’adresse aux patients non hospitalisés, pour des médicaments qu’on ne trouve généralement pas en officine de ville :</p>"
      + ul("médicaments inscrits sur la liste de rétrocession (article L.5126-4 du code de la santé publique)", "médicaments sous autorisation nominative, non réservés à l’usage hospitalier", "médicaments sous autorisation d’importation, non réservés à l’usage hospitalier", "médicaments contre la douleur chronique rebelle et pour les soins palliatifs")
      + "<h2>Pièces à apporter</h2>" + ul("Votre ordonnance originale", "Votre carte Vitale ou une attestation de droits ouverts", "Vos éléments de prise en charge par la mutuelle") + "<p>Selon votre situation, apportez aussi votre carnet de suivi ou votre attestation d’Aide médicale de l’État (AME) ou de Complémentaire santé solidaire.</p>"
      + "<h2>Durée de délivrance</h2><p>La délivrance couvre un mois de traitement. Pour un départ à l’étranger plus long, faites une demande expresse à votre centre de sécurité sociale et présentez l’accord obtenu avec vos pièces.</p>"
      + "<h2>Les missions de la pharmacie à usage intérieur</h2>" + ul("Achat des médicaments et dispositifs médicaux stériles, dans le groupement d’achat régional", "Analyse pharmaceutique des prescriptions et conciliation médicamenteuse", "Dispensation quotidienne, globale et nominative aux patients hospitalisés", "Préparation des piluliers des résidents d’EHPAD et d’une partie des patients hospitalisés", "Gestion et suivi des chimiothérapies préparées en sous-traitance", "Pharmacovigilance et matériovigilance", "Gestion des gaz médicaux et des produits diététiques")
      + "<h2>L’équipe</h2>" + team(("Chef de service", "Dr Mare"), ("Pharmaciens", "Dr Ledroit, Dr Mansour, Dr Negbane"), ("Cadre de santé", "Mme Lachaise")),
      fiche([("Rétrocession au public", bigtel("02 54 03 52 00")), ("Service", tel("02 54 03 54 11")), ("Accueil du public", "Du lundi au vendredi, de 8 h 30 à 17 h"), ("En dehors", "Astreinte pharmaceutique les week-ends et jours fériés"), ("Où", f"{MC}, sous-sol (niveau -1)")]),
      "retrocession medicament ordonnance pui"))

    out.append(svc("pass", "Permanence d’accès aux soins de santé (PASS)", "soins", "Consultations et examens", "soins",
      "Vous n’avez pas de couverture sociale, ou elle est incomplète ? La PASS vous soigne et vous accompagne dans vos droits, sans avance de frais.",
      '<div class="callout"><p><strong>Aucune avance de frais</strong> n’est demandée au patient.</p></div><h2>Pour qui</h2>'
      + ul("Personnes sans couverture sociale ou avec une couverture incomplète", "Personnes en rupture ou renoncement de soins, faute de droits ou par grande précarité", "Personnes dont les droits sont en cours d’ouverture ou de renouvellement", "Personnes qui ont besoin d’un accompagnement médico-social adapté")
      + "<h2>Prise en charge médicale</h2>" + ul("Consultations de médecine générale ou spécialisée", "Soins infirmiers", "Accès au plateau technique : radiologie, scanner", "Traitements médicamenteux si nécessaire", "Orientation vers un médecin spécialiste")
      + "<h2>Prise en charge sociale</h2>" + ul("Évaluation globale de votre situation et conseils", "Aide aux démarches, en priorité pour l’accès aux droits de santé", "Coordination avec les partenaires sanitaires et sociaux")
      + "<p>L’équipe vous suit jusqu’à l’ouverture de vos droits ou l’accès à l’Aide médicale de l’État. Elle vous oriente ensuite vers les soins habituels, à l’hôpital ou en ville.</p>"
      + "<h2>L’équipe</h2>" + team(("Médecin référent", "Dr Nizigiyimana"), ("Infirmière", "Mme Geraut"), ("Assistante sociale", "Mme Nassez"), ("Coordinatrice", "Mme Cotta")),
      fiche([("Secrétariat", bigtel("02 54 03 54 29") + "<br>Messagerie vocale en dehors des horaires"), ("E-mail", '<a href="mailto:pass@ch-issoudun.fr">pass@ch-issoudun.fr</a>'), ("Accueil", "Sur rendez-vous, du lundi au vendredi, de 13 h 30 à 16 h 30"), ("Où", "EHPAD Les Reflets d’Argent, rez-de-chaussée, dans l’enceinte de l’hôpital")],
            docs(("Plaquette en français", "2025/09/PASS_FLYER_PUBLIC_FR_SEPTEMBRE2025-WEB.pdf", "Septembre 2025"), ("Leaflet in English", "2025/09/PASS_FLYER_PUBLIC_ENG_SEPTEMBRE2025-WEB.pdf", "September 2025"))),
      "precarite ame couverture sociale sans papiers cmu c2s social gratuit"))

    out.append(svc("centre-perinatal", "Centre périnatal de proximité", "nais", "Femmes et naissance", "soins",
      "Suivi de grossesse, gynécologie et préparation à la naissance à Issoudun, avec des sages-femmes et des gynécologues obstétriciens.",
      "<h2>Consultations et suivi</h2>" + ul("Gynécologie et stérilité, avec un médecin ou une sage-femme", "Suivi de grossesse du début à la visite post-natale, avec un carnet personnel de grossesse", "Consultations pré-conceptionnelles", "Échographies gynécologiques et de grossesse", "Préparation à la naissance et à la parentalité", "Suivi de l’allaitement maternel", "Suivi de grossesse à risque sur prescription médicale, à l’hôpital ou à domicile", "Rééducation périnéale", "Prise en charge des interruptions volontaires de grossesse", "Suivi psychologique autour de la grossesse et du deuil périnatal", "Homéopathie et phytothérapie")
      + "<h2>L’équipe</h2>" + team(("Gynécologues obstétriciens", "Dr Djoufack Fotseu, Dr Kervella-Julien, Dr Khireddine, Dr Teleaga"), ("Sages-femmes", "Aurélie Esnault, Hélène Jobic, Céline Trevien, Anthony Weber (échographiste)"), ("Psychologue", "Jessica Moreau"), ("Conseillère conjugale et familiale", "Émilie Dubourg"), ("Secrétaire", "Florence Lestard"))
      + '<h2>Association Le Cocon</h2><p>Cette association d’aide à la parentalité propose des ateliers sur inscription dans les locaux du centre : portage et massage bébé, gestes de premiers secours pédiatriques, haptonomie, couches lavables, communication bienveillante et langage des signes. L’adhésion est de 6 €.</p>'
      + f'<p>Contact : {tel("02 54 03 54 15")}, <a href="mailto:lecocon.issoudun@gmail.com">lecocon.issoudun@gmail.com</a></p>',
      fiche([("Secrétariat", bigtel("02 54 03 54 15")), ("Accueil", "Sur rendez-vous, du lundi au vendredi, de 9 h à 17 h"), ("Où", f"{MC}, rez-de-chaussée"), ("Ouvert depuis", "1992")], docs(("Plaquette du centre", "2026/01/plaquette-CPP-13-01-2026.pdf", "Janvier 2026"))),
      "grossesse gynecologie sage femme enceinte bebe maternite echographie naissance allaitement cocon", [("Centre de santé sexuelle", "/services/sante-sexuelle.html")]))

    out.append(svc("sante-sexuelle", "Centre de santé sexuelle", "nais", "Femmes et naissance", "soins",
      "Accueil, écoute et consultations confidentiels et gratuits, avec ou sans rendez-vous. Le mercredi de 14 h à 16 h, venez sans rendez-vous.",
      "<h2>Ce que nous proposons</h2>" + ul("Vie sexuelle et affective", "Contraception, y compris d’urgence", "Diagnostic de grossesse", "Accès à l’interruption volontaire de grossesse (IVG)", "Prévention, dépistage et traitement des infections sexuellement transmissibles", "Difficultés au sein de la famille ou du couple", "Actions d’éducation et de prévention auprès des collégiens et lycéens")
      + "<p>La conseillère conjugale et familiale peut vous recevoir avant ou après une IVG, ou en cas de difficultés familiales ou de couple.</p><h2>L’équipe</h2><p>L’équipe est celle du centre périnatal de proximité : gynécologues obstétriciens, sages-femmes, psychologue et conseillère conjugale et familiale.</p>",
      fiche([("Rendez-vous", bigtel("02 54 03 54 15")), ("Sans rendez-vous", "Le mercredi, de 14 h à 16 h"), ("Sur rendez-vous", "Les autres jours"), ("Où", f"{MC}, rez-de-chaussée"), ("Tarif", "Gratuit et confidentiel")], docs(("Plaquette des activités", "2026/01/plaquette-CPP-13-01-2026.pdf", "Janvier 2026"))),
      "planning familial contraception ivg ist depistage pilule du lendemain sexualite", [("Centre périnatal de proximité", "/services/centre-perinatal.html")]))

    out.append(svc("centre-de-sante", "Centre de santé", "inst", "Consultations et examens", "soins",
      "L’activité du centre de santé est actuellement en veille. Aucune prise de rendez-vous n’est possible.",
      '<div class="callout warn"><h3>Activité en veille</h3><p>Pour une urgence vitale, appelez le 15. Pour un besoin de soins sans couverture sociale, contactez la <a href="/services/pass.html">PASS</a>.</p></div>'
      '<p>Pour un avis médical sans urgence, adressez-vous à votre médecin traitant. Pour un rendez-vous de spécialité, consultez la page <a href="/services/consultations.html">consultations</a>.</p>',
      None, "medecin generaliste generale veille"))

    # Grand âge
    lines_age = [("Soins infirmiers à domicile", "/services/ssiad.html"), ("La Parenthèse, accueil de jour", "/services/la-parenthese.html"), ("Équipe spécialisée Alzheimer", "/services/esa.html"), ("EHPAD", "/services/ehpad.html")]
    cmp = ('<div class="tbl-wrap"><table class="tbl compare"><caption class="visually-hidden">Comparatif des résidences</caption><thead><tr><th scope="col"><span class="visually-hidden">Critère</span></th>'
      '<th scope="col">Bel Air et Les Mésanges</th><th scope="col">Les Reflets d’Argent</th></tr></thead><tbody>'
      '<tr><th scope="row">Situation</th><td>En ville, quartier de Bel Air, à 3 km de l’hôpital, avec un parc</td><td>Dans l’enceinte du Centre Hospitalier</td></tr>'
      '<tr><th scope="row">Adresse</th><td>26 avenue du Père Noir, Issoudun. Entrée des Mésanges : rue de Bourgogne</td><td>Avenue Jean Bonnefont, Issoudun</td></tr>'
      '<tr><th scope="row">Capacité</th><td>84 lits et 2 lits d’hébergement temporaire, dont 20 aux Mésanges</td><td>90 places : 76 chambres individuelles et 7 chambres doubles</td></tr>'
      '<tr><th scope="row">Chambres</th><td>Toutes individuelles, avec cabinet de toilette, WC et douche</td><td>Individuelles ou doubles, avec WC et lavabo</td></tr>'
      '<tr><th scope="row">Depuis</th><td>Annexe des Mésanges créée en 2001</td><td>Ouverte en 1985, restructurée en octobre 2019</td></tr>'
      f'<tr><th scope="row">Téléphone</th><td>{tel("02 54 03 54 14")}</td><td>{tel("02 54 03 46 83")}</td></tr>'
      '<tr><th scope="row">En savoir plus</th><td><a href="/services/ehpad-bel-air.html">Bel Air et Les Mésanges</a></td><td><a href="/services/ehpad-reflets-argent.html">Les Reflets d’Argent</a></td></tr>'
      "</tbody></table></div>")
    out.append(svc("ehpad", "EHPAD : vivre en résidence", "age", "Grand âge", "age",
      "Deux résidences publiques à Issoudun, pour les personnes âgées dont le maintien à domicile est devenu difficile.",
      "<h2>Comparer les résidences</h2>" + cmp
      + "<h2>Vos démarches</h2>" + stations([("Demander une admission", "/hebergement/admission.html"), ("Tarifs et aides financières", "/hebergement/tarifs-aides.html"), ("Vie quotidienne : chambre, repas, animation", "/hebergement/vie-quotidienne.html"), ("Organismes à prévenir avant l’entrée", "/hebergement/organismes.html")]),
      fiche([("Admissions", bigtel("02 54 03 54 03") + "<br>Demandez le bureau des admissions en hébergement"), ("Où retirer le dossier", f"{MC}, rez-de-chaussée"), ("Conditions", "Plus de 60 ans, sauf dérogation, seul ou en couple, sans condition de ressources")], docs(("Charte de la personne âgée dépendante", "2021/12/Charte_des_Droits_de_la_Personne_Agee.pdf"), ("Trousseau minimum de linge", "2021/12/Trousseau_minimum_de_linge_des_residents_au_moment_de_ladmission.pdf"))),
      "maison de retraite personne agee hebergement residence dependance", [x for x in lines_age if "ehpad" not in x[1]]))

    PRO = ("<h2>Suivi médical</h2><p>Les soins sont assurés 24 h sur 24, par votre médecin traitant ou, à défaut, par le médecin responsable de la structure ou le médecin de garde de l’hôpital. "
           "Votre carte Vitale, votre attestation de sécurité sociale et votre carte de mutuelle peuvent être conservées au poste infirmier.</p>")
    out.append(svc("ehpad-bel-air", "EHPAD Bel Air et Les Mésanges", "age", "EHPAD", "age",
      "Une résidence publique avec un parc, en ville, dans le quartier de Bel Air, à 3 km de l’hôpital.",
      "<h2>La résidence</h2><p>La résidence compte 84 lits et 2 lits d’hébergement temporaire, répartis en trois unités : le rez-de-chaussée, le 1er étage et Les Mésanges, 20 lits créés en 2001, avec une entrée rue de Bourgogne.</p>"
      + "<p>Toutes les chambres sont individuelles, avec cabinet de toilette, WC et douche. Elles sont meublées et équipées d’une sonnette d’appel d’urgence et de prises pour la télévision et le téléphone.</p>"
      + "<h2>Accueillir ses proches</h2><p>Un espace famille et un salon permettent de recevoir vos proches. Vous pouvez aussi sortir avec eux quelques heures, une journée ou plus, après en avoir informé l’équipe soignante.</p>"
      + PRO + "<h2>Les services</h2>" + ul("Une collation chaude ou froide tous les jours à 16 h", "Coiffure, pédicure, manucure et soins de confort. Les intervenants extérieurs sont à votre charge", "Soins d’esthétique à la demande, au salon de bien-être", "Liberté de culte et visite du ministre du culte de votre choix")
      + "<h2>L’équipe</h2>" + team(("Médecin coordonnateur", "Dr Salomon"), ("Praticien associé", "Dr Harerimana"), ("Cadre de santé", "Mme Brossard"), ("Infirmière coordinatrice", "Mme Ferron"), ("Infirmière en pratique avancée", "Mme Savignaud"), ("Intervenants", "Masseurs-kinésithérapeutes, diététicienne, animatrices")),
      fiche([("Téléphone", bigtel("02 54 03 54 14")), ("Adresse", "26 avenue du Père Noir, 36100 Issoudun"), ("Les Mésanges", "Entrée rue de Bourgogne"), ("Visites", "Libres, de 9 h à 18 h")]),
      "maison de retraite pere noir mesanges", [("Les Reflets d’Argent", "/services/ehpad-reflets-argent.html"), ("Demander une admission", "/hebergement/admission.html")]))

    out.append(svc("ehpad-reflets-argent", "EHPAD Les Reflets d’Argent", "age", "EHPAD", "age",
      "Une résidence dans l’enceinte de l’hôpital, restructurée en 2019 : 76 chambres individuelles et 7 chambres doubles.",
      "<h2>La résidence</h2><p>Ouverte depuis 1985, la résidence a achevé sa restructuration en octobre 2019. Chaque chambre est meublée et dispose d’un bouton d’appel, d’un WC, d’un lavabo et de prises pour la télévision et le téléphone.</p>"
      + "<h2>Suivi médical</h2><p>Le médecin responsable passe chaque semaine, ou à la demande de l’infirmière. Les soins sont assurés 24 h sur 24. Vous pouvez garder votre médecin traitant.</p>"
      + "<h2>Accueillir ses proches</h2><p>Un espace permet de partager un repas en famille, sur réservation. Le ticket repas accompagnant s’achète à la boutique du pavillon Marie Curie, du lundi au vendredi.</p>"
      + "<h2>Animation</h2><p>Gymnastique douce, art-thérapie, fêtes saisonnières et goûter musical de fin d’année rythment l’année. Toutes les activités sont gratuites pour les résidents.</p><p>Associations partenaires : SAALSA, Pour Que l’Esprit Vive, Art et loisirs, VMEH.</p>"
      + "<p>En 2026, 48 résidents ont participé à 66 sorties en vélo adapté, grâce au prêt du Département de l’Indre.</p>"
      + "<h2>L’équipe</h2>" + team(("Médecin coordonnateur", "Dr Salomon"), ("Praticien associé", "Dr Harerimana"), ("Cadre de santé", "Mme Brossard"), ("Infirmière coordinatrice", "Mme Carnel"), ("Infirmière en pratique avancée", "Mme Savignaud"), ("Intervenants", "Masseurs-kinésithérapeutes, ergothérapeutes, diététicienne, animatrices, aide médico-psychologique")),
      fiche([("Téléphone", bigtel("02 54 03 46 83")), ("Adresse", "Avenue Jean Bonnefont, dans l’enceinte de l’hôpital"), ("Capacité", "90 places"), ("Visites", "Libres, de 9 h à 18 h")]),
      "maison de retraite reflets argent", [("Bel Air et Les Mésanges", "/services/ehpad-bel-air.html"), ("Demander une admission", "/hebergement/admission.html")]))

    communes = ["Ambrault", "Avail", "Bommiers", "Brives", "Chouday", "Condé", "Diou", "Issoudun", "La Champenoise", "Les Bordes", "Lizeray", "Meunet-Planches", "Migny", "Neuvy-Pailloux", "Paudy", "Pruniers", "Reuilly", "Saint-Aoustrille", "Saint-Aubin", "Saint-Georges-sur-Arnon", "Saint-Valentin", "Sainte-Fauste", "Sainte-Lizaigne", "Ségry", "Thizay", "Vouillon"]
    out.append(svc("ssiad", "Service de soins infirmiers à domicile (SSIAD)", "age", "Grand âge", "age",
      "Des soins à la maison pour garder ou retrouver votre autonomie, éviter une hospitalisation ou retarder l’entrée en établissement.",
      '<h2>Votre commune est-elle couverte ?</h2>'
      f'<form class="no-print" data-communes="{e("|".join(communes))}"><div class="field"><label for="commune">Votre commune</label><input id="commune" type="text" autocomplete="off" placeholder="Par exemple : Reuilly"></div><p class="result" role="status" hidden></p></form>'
      f'<details><summary>Voir toutes les communes</summary><p>{e(", ".join(communes))}.</p></details>'
      + "<h2>Pour qui</h2>" + ul("Les personnes de plus de 60 ans devenues dépendantes pour les actes de la vie quotidienne, de façon temporaire ou durable", "Les personnes de moins de 60 ans atteintes d’une affection invalidante")
      + "<h2>Comment être admis</h2>" + steps(("Assurance maladie.", " Être assuré ou ayant droit, et fournir la copie de l’attestation de droits ouverts."), ("Prescription.", " Obtenir une prescription de soins de votre médecin traitant."), ("Entretien.", " Rencontrer une infirmière du service."))
      + "<p>Selon la charge du service, un délai peut être nécessaire. En cas d’urgence, le service peut vous orienter vers une autre solution.</p>"
      + "<h2>Ce que ça coûte</h2><p>Une fois l’admission acceptée, le prix de journée est pris en charge à 100 % par les caisses d’assurance maladie. Il couvre les salaires, le fonctionnement et les actes infirmiers.</p>"
      + "<h2>L’équipe</h2><p>L’infirmière coordinatrice, Mme Audrey Mahen, évalue les besoins et assure le lien avec les familles, les médecins et les autres intervenants. Les aides-soignants réalisent les soins d’hygiène et de confort : toilette, habillage, lever et coucher. "
        "Pour les actes infirmiers, vous pouvez choisir un infirmier libéral conventionné avec le service. Ces soins sont directement rémunérés par le SSIAD.</p>",
      fiche([("Téléphone", bigtel("02 54 03 17 76")), ("Interventions", "De 7 h 30 à 19 h 30"), ("Où", "Avenue Jean Bonnefont, près de l’hôpital")], docs(("Livret d’accueil", "2025/11/LIVRET-SSIAD-CH-ISSOUDUN_2025.pdf", "2025"), ("Allocation personnalisée d’autonomie", "https://www.pour-les-personnes-agees.gouv.fr/preserver-son-autonomie-s-informer-et-anticiper/perte-d-autonomie-evaluation-et-droits/lallocation-personnalisee-dautonomie-apa"))),
      "domicile infirmier toilette aide soignant apa " + " ".join(communes), [x for x in lines_age if "ssiad" not in x[1]]))

    out.append(svc("la-parenthese", "La Parenthèse, accueil de jour Alzheimer", "age", "Grand âge", "age",
      "Dix places à la journée pour les personnes qui vivent à domicile avec la maladie d’Alzheimer ou une maladie apparentée, et un temps de répit pour leurs proches.",
      "<h2>Une journée à La Parenthèse</h2>" + '<div class="tbl-wrap"><table class="tbl"><tbody><tr><th scope="row">9 h à 10 h</th><td>Arrivée depuis le domicile</td></tr><tr><th scope="row">Vers 9 h 30</th><td>Collation</td></tr><tr><th scope="row">10 h à 16 h</th><td>Ateliers et vie à l’accueil de jour</td></tr><tr><th scope="row">Vers 12 h</th><td>Déjeuner</td></tr><tr><th scope="row">Vers 15 h 30</th><td>Collation</td></tr><tr><th scope="row">16 h à 17 h</th><td>Retour au domicile</td></tr></tbody></table></div>'
      + "<p>Ateliers proposés : cuisine, motricité, gymnastique douce, ateliers cognitifs et sensoriels, jardinage. Le personnel accompagne chaque geste « avec la personne et non pour elle ».</p>"
      + "<h2>Pour qui</h2>" + ul("Les personnes de 60 ans et plus atteintes de la maladie d’Alzheimer ou d’une maladie apparentée", "Les personnes qui vivent encore à domicile et dont l’autonomie nécessite la présence constante d’un tiers")
      + "<h2>Pour les proches</h2><p>L’accueil de jour offre un lieu de répit et d’écoute. Les aidants peuvent bénéficier d’un soutien psychologique ponctuel, d’informations pratiques et de groupes de formation.</p>"
      + "<h2>Les lieux</h2><p>Un lieu de vie lumineux, des fauteuils adaptés, un jardin thérapeutique clos, une cuisine thérapeutique et un espace de repos. Le bâtiment est à distance des pôles de soins, pour limiter le sentiment d’hospitalisation.</p>"
      + "<h2>Comment être admis</h2>" + steps(("Retirer le dossier", " auprès des secrétaires des soins de suite, au 1er étage du pavillon Marie Curie."), ("Déposer le dossier complet", " au même secrétariat."), ("Visite de pré-admission.", " Si le dossier est accepté, l’infirmière ou la psychologue vous contacte. En cas de refus, les raisons vous sont expliquées."), ("Rencontre avec l’équipe.", " Elle présente le fonctionnement et remet le contrat de séjour, le règlement et le livret d’accueil."), ("Période d’essai d’un mois.", " Une réunion de synthèse évalue si la prise en charge est adaptée."))
      + "<h2>Ce que ça coûte</h2><p>Le coût journalier comprend un forfait soins et un forfait hébergement, à la charge de la personne accueillie. Une partie peut être prise en charge par l’APA ou d’autres organismes : renseignez-vous auprès du service social.</p>"
      + "<div class=\"callout\"><p>L’accueil de jour n’est pas un lieu de soins. Il ne remplace ni le médecin traitant ni la consultation mémoire. Seuls les médicaments du midi sont distribués, sur copie de la prescription.</p></div>"
      + "<h2>L’équipe</h2><p>Deux aides-soignantes assurent la présence quotidienne, avec une infirmière coordinatrice, une neuropsychologue, une ergothérapeute et une psychomotricienne.</p>",
      fiche([("Téléphone", bigtel("02 54 03 67 14")), ("Coordonnatrice", f"Mme Rit, {tel('02 54 03 55 58')}"), ("E-mail", '<a href="mailto:ajalzheimer@ch-issoudun.fr">ajalzheimer@ch-issoudun.fr</a>'), ("Ouverture", "Du lundi au vendredi, de 9 h à 17 h. Fermé les week-ends et jours fériés"), ("Capacité", "10 places")],
            docs(("Livret d’accueil", "2026/03/LIVRET_AJA_23-03-2026.pdf", "Mars 2026"), ("Charte Alzheimer", "2022/01/Charte-Alzheimer-Ethique-et-societe.pdf"), ("Charte de la personne accueillie", "2022/01/exe_a4_accue284e.pdf"))),
      "accueil de jour alzheimer memoire aidant repit demence parenthese aja", [x for x in lines_age if "parenthese" not in x[1]]))

    out.append(svc("esa", "Équipe spécialisée Alzheimer (ESA)", "age", "Grand âge", "age",
      "Des séances de réhabilitation à domicile, sur prescription médicale, pour préserver les capacités et soutenir les proches.",
      "<h2>Pour qui</h2>" + ul("Les personnes vivant à domicile avec la maladie d’Alzheimer ou une maladie apparentée, dont la maladie a des répercussions sur la vie quotidienne", "Leurs proches aidants")
      + "<h2>Objectifs</h2>" + ul("Maintenir et développer les capacités préservées", "Réhabiliter les gestes de la vie quotidienne", "Aider les aidants à comprendre la maladie", "Sécuriser le domicile par des conseils d’aménagement", "Favoriser l’estime de soi")
      + "<h2>Le déroulement</h2>" + steps("Prescription par votre médecin traitant de 12 à 15 séances", "Évaluation à domicile", "Programme de soins personnalisé", "Une séance par semaine à domicile, d’environ une heure, pendant environ trois mois", "Évaluation finale", "Compte rendu et coordination avec les professionnels du domicile")
      + "<p>La prise en charge est renouvelable chaque année et intégralement financée par l’assurance maladie.</p><h2>L’équipe</h2><p>Une infirmière coordonnatrice, une ergothérapeute et une assistante de soins en gérontologie.</p>",
      fiche([("Secrétariat du SSIAD", bigtel("02 54 03 17 76") + "<br>Du lundi au vendredi, de 9 h à 17 h"), ("Interventions", "Du mardi au vendredi, de 8 h 30 à 16 h 30"), ("Où", "À votre domicile"), ("Coût", "Pris en charge par l’assurance maladie")]),
      "alzheimer domicile ergotherapeute memoire", [x for x in lines_age if "esa" not in x[1]]))

    return out

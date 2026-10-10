# -*- coding: utf-8 -*-
"""All Academy courses, transcribed from predika.pro.

Each entry is exactly what Predika's public course page shows. Individual
lesson titles are not public (the module accordions need an account), so each
module carries its lesson count and running time only.

`image` is the catalogue artwork already in assets/courses/; `card` is the
anchor the homepage catalogue card and the hero tiles used to point at.
"""

def mins(s):
    """'3h 10min' / '30min' / '6h 5min' -> minutes."""
    h = m = 0
    import re
    hh = re.search(r'(\d+)\s*h', s)
    mm = re.search(r'(\d+)\s*min', s)
    if hh: h = int(hh.group(1))
    if mm: m = int(mm.group(1))
    return h * 60 + m


COURSES = [

 dict(slug='fondamentaux-finance-islamique', card='#course-1',
   title='Fondamentaux de la Finance Islamique',
   subtitle='Introduction au Fiqh al-Muamalat et aux principes économiques islamiques',
   category='Islamic Banking', level='Fondamentaux',
   image='assets/courses/fondamentaux-finance-islamique.jpg',
   price='69 000', currency='FCFA', enrolled=12, scarcity='Place limitée', lessons=24,
   description=("Ce cours introduit les principes fondamentaux de la finance islamique, le "
     "Fiqh al-Muamalat et les objectifs économiques de la Sharia. Il présente les interdictions "
     "majeures telles que le Riba, le Gharar et le Maysir ainsi que l’évolution de l’industrie "
     "financière islamique mondiale."),
   outcomes=["Comprendre les principes de la finance islamique.",
             "Maîtriser les bases du Fiqh al-Muamalat.",
             "Identifier les interdictions Sharia majeures.",
             "Analyser l’écosystème mondial Islamic Finance."],
   modules=[("Fondements Théologiques, Éthiques et Cadre Juridique", 6, "6h 5min", ""),
            ("Ingénierie des Produits de Financement aux Particuliers (Retail Banking)", 4, "3h 30min", ""),
            ("Ingénierie des Produits de Financement aux Entreprises (Corporate Banking)", 3, "2h 30min", ""),
            ("Gestion des Produits de Dépôt et d'Investissement", 3, "2h 30min", ""),
            ("Trésorerie Interbancaire et Gestion Actif-Passif (ALM)", 2, "1h 23min", ""),
            ("Comptabilité AAOIFI et Reporting Prudentiel IFSB", 3, "2h 38min", ""),
            ("Gouvernance, Déontologie et Audit Charia Interne", 2, "1h 23min", ""),
            ("Evaluation Finale", 1, "1h 25min", "Révision intégrale du cours — 85 min")],
   tags=["Fiqh al-Muamalat", "Riba", "Gharar", "Maysir", "Islamic Banking",
         "AAOIFI", "IFSB", "Audit Charia", "ALM"],
   tutors=['Yaya SOW', 'Abdoulaye WANE', 'Modou SALL', 'Moustapha ABAKAR MOUSSA']),

 dict(slug='digital-islamic-banking', card='#course-2',
   title='Digital Islamic Banking',
   subtitle='Cours sur la transformation digitale des banques islamiques.',
   category='Islamic Banking', level='Expertise',
   image='assets/courses/digital-islamic-banking.jpg',
   price='69 000', currency='FCFA', enrolled=None, scarcity='Place limitée', lessons=26,
   description=("Le cours couvre la digitalisation complète d'une banque islamique : systèmes "
     "d'information et core banking adapté, open banking et API Sharia-compliant, wallets et "
     "paiements mobiles islamiques, RegTech/SupTech et compliance automation, Agentic AI "
     "bancaire et modèles LLM pour le secteur. Public : DSI, Chief Digital Officer, "
     "responsables transformation, chefs de projet."),
   outcomes=["Choisir un core banking islamique adapté",
             "Déployer l'open banking conforme Sharia",
             "Lancer des wallets et paiements mobiles",
             "Automatiser la compliance par RegTech",
             "Exploiter l'IA agentique bancaire"],
   modules=[("Systèmes d'Information et Core Banking Islamique", 5, "3h 10min", ""),
            ("Open Banking, API et Connectivité", 5, "3h 10min", ""),
            ("Wallets Islamiques et Paiements Mobiles", 5, "3h 10min", ""),
            ("RegTech, SupTech et Compliance Automation", 5, "3h", ""),
            ("Agentic AI Bancaire et Modèles LLM", 5, "3h 10min", ""),
            ("Evaluation Finale", 1, "30min", "")],
   tags=["Core Banking", "Open Banking", "API", "Wallets", "RegTech", "SupTech",
         "Agentic AI", "LLM", "Digital Banking"],
   tutors=['Modou SALL', 'Bashir Diaby', 'Yaya SOW', 'Abdoulaye WANE']),

 dict(slug='islamic-treasury-liquidite', card='#course-3',
   title='Islamic Treasury & Liquidité',
   subtitle="Cours d'expertise sur la trésorerie et la gestion de liquidité bancaire islamique.",
   category='Islamic Banking', level='Expertise',
   image='assets/courses/islamic-treasury-liquidite.jpg',
   price='69 000', currency='FCFA', enrolled=2, scarcity='Place limitée', lessons=26,
   description=("Le cours couvre l'ensemble du cycle de l'Islamic Treasury : organisation de la "
     "salle des marchés Sharia-compliant, sukuk souverains et titres publics, wakala "
     "interbancaire, gestion actif-passif (ALM) islamique, marché monétaire islamique et "
     "refinancement banques centrales. Public visé : trésoriers, ALM managers, dealers, "
     "responsables liquidité."),
   outcomes=["Organiser une Islamic Treasury complète",
             "Maîtriser les sukuk souverains",
             "Pratiquer la wakala interbancaire",
             "Piloter l'ALM islamique au quotidien",
             "Refinancer auprès des banques centrales"],
   modules=[("Organisation de l'Islamic Treasury", 5, "3h 10min", ""),
            ("Sukuk Souverains et Titres Publics Islamiques", 5, "3h 10min", ""),
            ("Pratique de la Wakala Interbancaire", 5, "3h 10min", ""),
            ("Gestion Actif-Passif (ALM Islamique)", 5, "3h 10min", ""),
            ("Marché Monétaire Islamique et Refinancement Banques Centrales", 5, "3h 10min", ""),
            ("Evaluation Finale", 1, "30min", "")],
   tags=["Treasury", "Sukuk", "Wakala", "ALM", "Marché monétaire", "Liquidité",
         "Banques centrales"],
   tutors=['Moustapha ABAKAR MOUSSA', 'Modou SALL', 'Abdoulaye WANE', 'Yaya SOW']),

 dict(slug='gestion-des-risques-compliance', card='#course-4',
   title='Gestion des Risques & Compliance',
   subtitle=("Cours fondamental sur la gestion intégrée des risques et la compliance dans les "
             "Institutions Financières Islamiques."),
   category='Islamic Banking', level='Fondamentaux',
   image='assets/courses/gestion-risques-compliance.jpg',
   price='69 000', currency='FCFA', enrolled=None, scarcity='Place limitée', lessons=26,
   description=("Le cours couvre les piliers de la gestion des risques et de la compliance dans "
     "les IFI : Sharia Non-Compliance Risk (SNCR) comme risque spécifique majeur, gestion du "
     "risque de liquidité dans le cadre des contraintes Sharia, dispositif AML/CFT adapté aux "
     "contrats islamiques, compliance bancaire et déontologie, contrôle réglementaire et "
     "application des normes prudentielles IFSB et bâloises adaptées."),
   outcomes=["Gérer le Sharia Non-Compliance Risk",
             "Gérer le risque de liquidité Sharia-compliant",
             "Déployer un dispositif AML/CFT",
             "Organiser la compliance bancaire et la déontologie",
             "Appliquer les normes prudentielles IFSB"],
   modules=[("Risque de Non-Conformité Sharia", 5, "3h 5min", ""),
            ("Gestion du Risque de Liquidité", 5, "3h 10min", ""),
            ("Dispositif AML/CFT", 5, "3h 10min", ""),
            ("Compliance Bancaire et Déontologie", 5, "3h 45min", ""),
            ("Contrôle Réglementaire et Normes Prudentielles", 5, "3h 10min", ""),
            ("Evaluation Finale du cours", 1, "30min", "")],
   tags=["SNCR", "Risque de liquidité", "AML/CFT", "Compliance", "Déontologie",
         "IFSB", "Bâle"],
   tutors=['Yaya SOW', 'Abdoulaye WANE', 'Modou SALL', 'Moustapha ABAKAR MOUSSA']),

 dict(slug='comptabilite-audit-islamique', card='#course-5',
   title='Comptabilité & Audit Islamique',
   subtitle=("Cours fondamental sur la comptabilité et l'audit des Institutions Financières "
             "Islamiques selon les FAS AAOIFI."),
   category='Islamic Banking', level='Fondamentaux',
   image='assets/courses/comptabilite-audit-islamique.jpg',
   # the catalogue thumbnail carries its own title across the top, which would
   # sit behind the page's own h1; the hero-grid tile is the same artwork
   # without any type on it
   hero_image='assets/trail/01.jpg',
   price='69 000', currency='FCFA', enrolled=1, scarcity='Place limitée', lessons=26,
   description=("Le cours couvre l'ensemble du cycle comptable des IFI : référentiel FAS AAOIFI "
     "(35+ standards) et articulation avec IFRS/SYSCOHADA, application opérationnelle aux "
     "contrats clés (Murabaha FAS 28, Ijara FAS 32), élaboration des états financiers "
     "spécifiques (PER, IRR, Charity, Zakat), méthodologie d'audit financier adaptée aux IFI "
     "incluant le double référentiel comptable et la dimension Sharia."),
   outcomes=["Maîtriser le référentiel FAS AAOIFI",
             "Comptabiliser une Murabaha selon FAS 28",
             "Comptabiliser une Ijara selon FAS 32",
             "Élaborer des états financiers IFI complets",
             "Conduire un audit financier d'IFI"],
   modules=[("Référentiel Comptable FAS de l'AAOIFI", 5, "3h 10min", ""),
            ("Pratique Comptable de la Murabaha", 5, "3h 10min", ""),
            ("Pratique Comptable de l'Ijara", 5, "3h 10min", ""),
            ("Élaboration des États Financiers Islamiques", 5, "3h 12min", ""),
            ("Méthodologie de l'Audit Financier IFI", 5, "3h 15min", ""),
            ("Evaluation Finale du cours", 1, "30min", "")],
   tags=["FAS AAOIFI", "Murabaha", "Ijara", "IFRS", "SYSCOHADA", "Zakat",
         "États financiers", "Audit"],
   tutors=['Yaya SOW', 'Moustapha ABAKAR MOUSSA', 'Abdoulaye WANE', 'Modou SALL']),

 dict(slug='islamic-corporate-banking', card='#course-6',
   title='Islamic Corporate Banking',
   subtitle=("Cours sur le financement d'entreprise, trade finance, syndication et opérations "
             "corporate islamiques."),
   category='Islamic Banking', level='Expertise',
   image='assets/courses/islamic-corporate-banking.jpg',
   price='69 000', currency='FCFA', enrolled=None, scarcity='Place limitée', lessons=27,
   description=("Ce cours présente le financement corporate islamique : Murabaha import-export, "
     "Salam matières premières, Istisna' biens d'équipement, Musharaka projets, syndications "
     "islamiques, lettres de crédit islamiques (L/C Wakala), garanties Kafala, trade finance, "
     "financement de projet (project finance Sharia)."),
   outcomes=["Structurer un crédit corporate islamique",
             "Concevoir une syndication Sharia avec banque chef de file",
             "Émettre une lettre de crédit islamique conforme",
             "Évaluer un projet de project finance islamique",
             "Calibrer une garantie Kafala bancaire"],
   modules=[("Éléments de Trade Finance Islamique (Commerce International)", 6, "4h 25min", ""),
            ("Financement de l'Exploitation, de l'Équipement et de la Trésorerie des PME", 5, "3h 8min", ""),
            ("Financements Syndiqués et Grands Enjeux Corporate (Syndication Islamique)", 5, "3h 15min", ""),
            ("Régime des Garanties et Sûretés Islamiques (Mitigation des Risques)", 5, "3h 10min", ""),
            ("Ingénierie Financière et Structuration Corporate Avancée", 5, "3h 10min", ""),
            ("Evaluation Finale", 1, "25min", "")],
   tags=["Trade finance", "Murabaha", "Salam", "Istisna'", "Musharaka",
         "Syndication", "L/C Wakala", "Kafala", "Project finance"],
   tutors=['Yaya SOW', 'Moustapha ABAKAR MOUSSA', 'Modou SALL', 'Abdoulaye WANE']),

 dict(slug='islamic-retail-banking', card='#course-7',
   title='Islamic Retail Banking',
   subtitle=("Cours sur les produits et opérations de banque de détail islamique : comptes "
             "courants, comptes Mudaraba, financement personnel, automobile, immobilier, "
             "cartes islamiques, paiements."),
   category='Islamic Banking', level='Expertise',
   image='assets/courses/islamic-retail-banking.jpg',
   price='69 000', currency='FCFA', enrolled=1, scarcity='Place limitée', lessons=18,
   description=("Ce cours couvre l'ensemble des produits et processus de banque de détail "
     "islamique : comptes courants Wadia, comptes d'épargne Mudaraba, financement à la "
     "consommation (Murabaha équipement), automobile (Ijara MB), immobilier (Musharaka "
     "Mutanaqisa), cartes de paiement islamiques, virements et opérations courantes. Inclut "
     "digital onboarding e-KYC et bonnes pratiques UX bancaire."),
   outcomes=["Structurer les produits courants de banque de détail islamique",
             "Structurer des financements particuliers",
             "Évaluer la satisfaction client (NPS) sur produits islamiques",
             "Maîtriser les processus e-KYC Sharia-compliant"],
   modules=[("Gestion des Comptes de Dépôts et Moyens de Paiement Islamiques", 4, "2h 25min", ""),
            ("Financement de l'Exploitation et de la Trésorerie des Entreprises (PME/PMI)", 4, "2h 25min", ""),
            ("Financement des Investissements Corporels et de l'Équipement Professionnel", 3, "1h 40min", ""),
            ("Ingénierie du Financement Immobilier (Retail & Professionnel)", 3, "1h 40min", ""),
            ("Mobile Banking, Canaux Digitaux et Inclusion Financière des PME", 3, "1h 40min", ""),
            ("Evaluation Finale", 1, "12min", "")],
   tags=["Wadia", "Mudaraba", "Ijara MB", "Musharaka Mutanaqisa", "Cartes islamiques",
         "e-KYC", "Mobile banking", "NPS"],
   tutors=['Yaya SOW', 'Modou SALL', 'Abdoulaye WANE', 'Moustapha ABAKAR MOUSSA']),

 dict(slug='contrats-islamiques-structuration', card='#course-8',
   title='Contrats Islamiques & Structuration',
   subtitle=("Ce cours couvre les principaux contrats utilisés dans les banques islamiques et "
             "les marchés financiers islamiques."),
   category='Islamic Banking', level='Fondamentaux',
   image='assets/courses/contrats-islamiques-structuration.jpg',
   hero_image='assets/trail/02.jpg',
   price='69 000', currency='FCFA', enrolled=None, scarcity='Place limitée', lessons=None,
   description=("Ce cours couvre les principaux contrats utilisés dans les banques islamiques "
     "et les marchés financiers islamiques."),
   outcomes=[],
   modules=[],
   tags=["Contrats islamiques", "Structuration", "Islamic Banking"],
   tutors=['Yaya SOW', 'Modou SALL']),
]

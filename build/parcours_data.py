# -*- coding: utf-8 -*-
"""The parcours catalogue, transcribed from predika.pro/learning-paths.

One parcours is published today: Certified Islamic Banker (CIB), at
predika.pro/learning-paths/bgT8SxWQ40d5TW38WpV9. Everything below — the price,
the à-la-carte total, the discount, the three payment plans and their fees, the
outcomes, the presentation, the benefits and the closing copy — is that page's
own, kept word for word where it is editorial.

Two figures on Predika's page contradict each other and are flagged rather than
silently fixed:
  · the header says "10 cours inclus", the bundle section lists 8 and says
    "8 cours complets". We follow the list: 8.
  · the à-la-carte total is printed as 800 000 FCFA, but the 8 courses are
    priced at 69 000 each on their own pages, which comes to 552 000. We print
    Predika's 800 000 and do not recompute it.
"""

PARCOURS = [
  dict(
    slug='certified-islamic-banker',
    title='Certified Islamic Banker (CIB)',
    tagline='Bundle −50 %',
    subtitle="Certification Professionnelle en Banque Islamique & Opérations Bancaires "
             "Sharia-Compliant",
    image='assets/parcours/certified-islamic-banker.png',
    category='Banque & microfinance',
    level='Intermédiaire',

    # the eight courses of the bundle, in Predika's order
    courses=[
      'fondamentaux-finance-islamique',
      'contrats-islamiques-structuration',
      'islamic-retail-banking',
      'islamic-corporate-banking',
      'comptabilite-audit-islamique',
      'gestion-des-risques-compliance',
      'islamic-treasury-liquidite',
      'digital-islamic-banking',
    ],

    price=400000,          # FCFA, bundle
    retail=800000,         # FCFA, "si achetés séparément", as printed
    discount=50,           # %, as printed
    currency='FCFA',
    recommended=3,         # the plan shown black, with the flag — as on Predika

    # the payment plans, with Predika's own fractionnement fees
    plans=[
      dict(n=1, title='Paiement unique', per=400000, total=400000, fee=None,
           line="Le parcours réglé en une fois, à l'inscription.",
           items=["Accès immédiat", "1 seul virement", "Aucun frais"],
           cta="Payer en 1×"),
      dict(n=2, title='2 versements', per=210000, total=420000, fee='+5 %',
           line="La moitié à l'inscription, le solde au second versement.",
           items=["Accès immédiat", "2 versements mensuels",
                  "+5 % de frais de fractionnement"],
           cta="Payer en 2×"),
      dict(n=3, title='3 versements', per=146667, total=440000, fee='+10 %',
           line="Un tiers à l'inscription, puis deux versements mensuels.",
           items=["Accès immédiat", "3 versements mensuels",
                  "+10 % de frais de fractionnement"],
           cta="Démarrer pour 146 667 FCFA"),
    ],
    pay_ways=['Wave', 'Orange Money', 'Moov Money', 'Carte bancaire'],
    pay_note="Paiement sécurisé &middot; <b>Satisfait ou remboursé 7 jours</b> "
             "&middot; Aucune surprise",
    plans_lede="Accès immédiat dès le premier versement — peu importe l'option choisie. "
               "Zéro frais caché. Votre parcours débloqué dès le premier jour.",

    # head facts, as the page's badge row prints them
    badges=['8 cours inclus', 'Certificat Alal Academy', 'Accès à vie', 'Accès immédiat'],

    outcomes_lede="Des compétences directement applicables en entreprise — pas de théorie "
                  "creuse.",
    # (short title, the sentence as predika.pro writes it) — the title is the
    # bold line Alal_Stats_UnderlineRow puts above its description
    outcomes=[
      ("Fondamentaux",
       "Comprendre les principes fondamentaux de la finance islamique et du Fiqh "
       "al-Muamalat."),
      ("Structuration",
       "Structurer des produits bancaires islamiques conformes aux standards AAOIFI."),
      ("Opérations",
       "Superviser des opérations retail et corporate Sharia-compliant."),
      ("Gouvernance",
       "Appliquer les mécanismes de gouvernance Sharia, conformité et gestion des "
       "risques."),
      ("Transformation digitale",
       "Comprendre les enjeux de transformation digitale des banques islamiques."),
      ("Afrique",
       "Accompagner le développement des institutions financières islamiques en "
       "Afrique."),
    ],

    presentation=[
      "Le programme Certified Islamic Banker (CIB) est une certification professionnelle "
      "dédiée aux opérations bancaires islamiques et à la gestion des institutions "
      "financières Sharia-compliant. Le parcours prépare les participants à comprendre les "
      "fondements du Fiqh al-Muamalat, structurer des produits bancaires islamiques et "
      "superviser des opérations conformes aux standards internationaux de la finance "
      "islamique.",
      "Le programme couvre les principaux domaines de l'Islamic Banking moderne, notamment "
      "les contrats islamiques, les opérations retail et corporate, la gouvernance Sharia, "
      "la conformité AAOIFI, la gestion des risques, la trésorerie islamique et la "
      "transformation digitale des banques islamiques. Une attention particulière est "
      "accordée aux réalités réglementaires et opérationnelles des marchés africains, "
      "notamment dans l'espace UEMOA et CIMA.",
      "Le parcours combine théorie, études de cas, simulations opérationnelles, analyse "
      "documentaire et applications pratiques afin de permettre aux participants de "
      "développer une compréhension concrète des mécanismes bancaires islamiques modernes.",
      "À l'issue du programme, les participants seront capables de structurer des produits "
      "bancaires Sharia-compliant, comprendre les mécanismes de gouvernance islamique, "
      "appliquer les standards AAOIFI, gérer les risques et accompagner les projets de "
      "transformation bancaire islamique et digitale.",
      "Le programme s'adresse aux professionnels bancaires, banques islamiques, fenêtres "
      "islamiques, SFD, établissements financiers, consultants, régulateurs, auditeurs, "
      "étudiants et professionnels souhaitant développer une expertise spécialisée en "
      "Islamic Banking.",
    ],

    tutors_lede="Praticiens en poste dans les banques, SFD et fintechs africaines — pas des "
                "académiciens.",

    benefits=[
      ("Accès à vie",
       "Revenez quand vous voulez, même un an après. Le contenu reste le vôtre pour "
       "toujours."),
      ("Certificat officiel",
       "Un certificat reconnu par les institutions financières et les recruteurs "
       "partenaires."),
      ("Démarrage immédiat",
       "Votre accès est activé dans les 5 minutes qui suivent le paiement. Pas d'attente."),
      ("Formateurs praticiens",
       "Des experts en poste — banques islamiques, SFD, fintechs — pas des théoriciens."),
      ("À votre rythme",
       "Mobile, tablette, desktop. En ligne ou hors ligne. Vous choisissez quand et où vous "
       "apprenez."),
      ("Remboursement 7 jours",
       "Si ce n'est pas fait pour vous dans les 7 jours, vous êtes remboursé intégralement. "
       "Sans question."),
    ],


    # ── sections Predika's page does not have, kept from our own build and
    #    restated against its figures ──────────────────────────────────────
    audience=[
      ("Professionnels bancaires",
       "Chargés de clientèle, analystes et responsables d'agence en banque "
       "islamique, en fenêtre islamique ou en SFD."),
      ("Fonctions de contrôle",
       "Risque, conformité, audit interne et comptabilité amenés à couvrir des "
       "opérations conformes à la Charia."),
      ("Consultants et régulateurs",
       "Cabinets, superviseurs et régulateurs qui encadrent ou accompagnent les "
       "institutions financières islamiques."),
      ("Étudiants et jeunes diplômés",
       "Profils finance, droit ou gestion qui visent un premier poste dans "
       "l'industrie — aucun prérequis n'est exigé."),
    ],

    prereqs=[
      ("Prérequis", "Aucun. Le parcours s'ouvre sur les Fondamentaux."),
      ("Niveau", "Intermédiaire."),
      ("Langue", "Français, supports en français."),
      ("Rythme", "À votre rythme, accès à vie au contenu."),
      ("Supports", "Mobile, tablette, desktop — en ligne ou hors ligne."),
      ("Certificat", "Un certificat par cours, plus le certificat du parcours."),
    ],

    steps=[
      ("Vérifiez que le parcours vous correspond",
       "Parcourez les huit cours du bundle et leurs programmes. Aucun prérequis "
       "n'est demandé, mais l'ordre compte."),
      ("Choisissez votre plan de paiement",
       "Paiement unique, 2 ou 3 versements. L'accès est le même dans les trois cas."),
      ("Réglez par mobile money ou carte",
       "Wave, Orange Money, Moov Money ou carte bancaire. Le paiement est sécurisé."),
      ("Accédez au bundle immédiatement",
       "Votre accès est activé dans les 5 minutes qui suivent le paiement, dès le "
       "premier versement."),
      ("Obtenez votre certification",
       "Chaque cours terminé délivre son certificat ; les huit obtenus, le "
       "certificat du parcours est délivré."),
    ],

    after=dict(
      title="Et après le parcours",
      text="Le parcours est la marche d'avant les titres officiels. Les "
           "qualifications AAOIFI — CPSS, CIPA, CSAA — sont délivrées par "
           "l'AAOIFI elle-même après son examen ; ce parcours en couvre le "
           "socle de connaissances.",
      link=('Voir les qualifications AAOIFI', 'index.html#aaoifi'),
    ),

    faq=[
      ("Puis-je acheter les cours séparément ?",
       "Oui. Chaque cours du bundle reste disponible à l'unité à 69 000 FCFA. Le "
       "bundle existe pour qui veut les huit : il revient à 400 000 FCFA au lieu "
       "de 800 000 FCFA à la carte."),
      ("Dois-je suivre les cours dans l'ordre ?",
       "C'est recommandé — les Fondamentaux posent le vocabulaire que les sept "
       "autres réutilisent — mais rien ne vous en empêche : l'accès aux huit "
       "cours est ouvert dès le premier versement."),
      ("Combien de temps ai-je pour terminer ?",
       "Aucune limite. L'accès est à vie : revenez quand vous voulez, même un an "
       "après."),
      ("Le paiement en plusieurs fois coûte-t-il plus cher ?",
       "Oui, légèrement : 2 versements portent le total à 420 000 FCFA (+5 % de "
       "frais de fractionnement) et 3 versements à 440 000 FCFA (+10 %). Le "
       "paiement unique reste à 400 000 FCFA."),
      ("Que se passe-t-il si le parcours ne me convient pas ?",
       "Vous êtes remboursé intégralement si vous le demandez dans les 7 jours, "
       "sans justification."),
      ("Ce parcours délivre-t-il une certification AAOIFI ?",
       "Non. Les titres AAOIFI sont délivrés par l'AAOIFI après réussite de son "
       "examen officiel. Le parcours délivre les certificats Alal Academy de "
       "chaque cours et le certificat du parcours, et prépare au socle exigé."),
    ],

    cta=dict(
      title="Prêt à maîtriser le Certified Islamic Banker (CIB) ?",
      text="Des centaines de professionnels africains ont déjà transformé leur carrière avec "
           "ces formations. Vous êtes le prochain.",
      button="Obtenir le bundle maintenant",
      note="Accès immédiat &middot; Paiement sécurisé &middot; Remboursement garanti 7 jours",
    ),
  ),
]

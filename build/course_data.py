# -*- coding: utf-8 -*-
"""Course 1, transcribed from predika.pro/courses/introduction-au-systeme-financier-islamique.

Everything here is on Predika's public course page. The individual lesson
titles are NOT public (the module accordions do not expand without an
account), so modules carry their lesson count and duration only.
"""

COURSE = dict(
    slug='fondamentaux-finance-islamique',
    category='Islamic Banking',
    level='Fondamentaux',
    title='Fondamentaux de la Finance Islamique',
    subtitle='Introduction au Fiqh al-Muamalat et aux principes économiques islamiques',
    description=(
        "Ce cours introduit les principes fondamentaux de la finance islamique, le "
        "Fiqh al-Muamalat et les objectifs économiques de la Sharia. Il présente les "
        "interdictions majeures telles que le Riba, le Gharar et le Maysir ainsi que "
        "l’évolution de l’industrie financière islamique mondiale."
    ),
    price='69 000',
    currency='FCFA',
    enrolled=12,
    scarcity='Place limitée',
    lessons=24,
    image='assets/courses/fondamentaux-finance-islamique.jpg',
    outcomes=[
        "Comprendre les principes de la finance islamique.",
        "Maîtriser les bases du Fiqh al-Muamalat.",
        "Identifier les interdictions Sharia majeures.",
        "Analyser l’écosystème mondial Islamic Finance.",
    ],
    modules=[
        ("Fondements Théologiques, Éthiques et Cadre Juridique", 6, "6h 5min", 365, ""),
        ("Ingénierie des Produits de Financement aux Particuliers (Retail Banking)", 4, "3h 30min", 210, ""),
        ("Ingénierie des Produits de Financement aux Entreprises (Corporate Banking)", 3, "2h 30min", 150, ""),
        ("Gestion des Produits de Dépôt et d'Investissement", 3, "2h 30min", 150, ""),
        ("Trésorerie Interbancaire et Gestion Actif-Passif (ALM)", 2, "1h 23min", 83, ""),
        ("Comptabilité AAOIFI et Reporting Prudentiel IFSB", 3, "2h 38min", 158, ""),
        ("Gouvernance, Déontologie et Audit Charia Interne", 2, "1h 23min", 83, ""),
        ("Evaluation Finale", 1, "1h 25min", 85, "Révision intégrale du cours — 85 min"),
    ],
    guarantees=[
        "Confirmation sous 24h après paiement",
        "Certificat à la fin du cours",
        "Accès illimité au contenu",
        "Paiement sécurisé hors-ligne",
    ],
    tags=["Fiqh al-Muamalat", "Riba", "Gharar", "Maysir", "Islamic Banking",
          "AAOIFI", "IFSB", "Audit Charia", "ALM"],
    tutors=[
        dict(name='Yaya SOW', photo='assets/formateurs/04.jpg',
             credentials=("Certified Shari’ah Adviser and Auditor — CSAA – AAOIFI, Master en "
                          "Islamic Finance – CIBAFI et Master en Études Islamiques & Jurisprudence."),
             bio=("PhD Candidate Islamic Finance – Al-Azhar University. Seize ans d'expérience "
                  "pratique et pédagogique dans l'enseignement ; expertise confirmée en finance "
                  "islamique, jurisprudence islamique et gouvernance charia ; compétences reconnues "
                  "en audit charia, contrôle de conformité et gestion éthique des ressources "
                  "financières."),
             linkedin='https://www.linkedin.com/in/yaya-sow-2024m/'),
        dict(name='Abdoulaye WANE', photo='assets/formateurs/01.jpg',
             credentials=("Expert en finance islamique et Auditeur Charia, Certified Islamic "
                          "Specialist in Shari'a Auditing (CISSA) – CIBAFI, Master en Banque."),
             bio=("Auditeur charia interne à la Banque Islamique du Sénégal, première banque "
                  "islamique de la zone UEMOA. Expert en finance islamique avec plus de 12 ans "
                  "d'expérience couvrant la microfinance islamique, l'audit Charia, la "
                  "digitalisation des processus et la formation professionnelle. Auditeur Charia "
                  "certifié CIBAFI ayant exercé au sein de plusieurs institutions pionnières au "
                  "Sénégal, contribuant à l'opérationnalisation de produits conformes, à la "
                  "conduite d'audits rigoureux selon les normes AAOIFI, et à l'accompagnement de "
                  "Fintechs dans le développement de solutions dédiées."),
             linkedin='https://www.linkedin.com/in/abdoulaye-wane-83029216a'),
        dict(name='Modou SALL', photo='assets/formateurs/05.jpg',
             credentials=("Diplômé de l’ITB – ESBanque, Certified Islamic Banking – INCEIF et "
                          "Certified Digital Finance Practitioner – Fletcher School."),
             bio=("Professionnel de la banque et de la fintech avec plus de 15 ans d’expérience "
                  "dans les services financiers, la transformation digitale et le conseil en "
                  "Afrique. Spécialiste en Islamic Banking and Capital Market, il œuvre au "
                  "rapprochement entre finance conventionnelle et finance islamique pour promouvoir "
                  "une finance plus inclusive et durable en Afrique."),
             linkedin='https://www.linkedin.com/in/modousall/'),
        dict(name='Moustapha ABAKAR MOUSSA', photo='assets/formateurs/02.jpg',
             credentials=("Docteur en comptabilité et finance, expert Charia Governance & Audit, "
                          "normes comptables FAS AAOIFI, IFRS, OHADA."),
             bio=("Docteur en Comptabilité et Finance de l'Université de Sakarya (Turquie), avec "
                  "une expérience internationale en Turquie, Tunisie et Afrique centrale. "
                  "Spécialiste du reporting financier, de l'audit, du contrôle de gestion, de la "
                  "fiscalité et des normes comptables internationales. Expert des référentiels "
                  "IFRS, AAOIFI, OHADA et PCEC, il accompagne les institutions financières et les "
                  "entreprises dans l'amélioration de leur performance financière, leur conformité "
                  "réglementaire et leurs dispositifs de gouvernance."),
             linkedin='https://td.linkedin.com/in/dr-moustapha-abakar-moussa-08b28023a'),
    ],
)

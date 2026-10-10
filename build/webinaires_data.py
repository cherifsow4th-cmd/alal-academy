# -*- coding: utf-8 -*-
"""The webinar calendar, transcribed from predika.pro/webinaires.

Predika's page has no session booked and four replays, the most recent of which
carries a YouTube recording, a speaker bio and a moderator. That is reproduced
here as-is: nothing is invented, and UPCOMING is deliberately empty so the page
shows the same empty state Predika's does.

One edit. The 19 June summary on predika.pro begins with a line of editorial
instructions left in by mistake ("Voici une version ultra-courte et
percutante…"); only the summary itself is kept below.
"""

UPCOMING = []

REPLAYS = [
  dict(
    slug='deficit-infrastructurel-africain',
    date='26 juillet 2026',
    iso='2026-07-26',
    status='Dernière présentation',
    featured=True,
    format='Webinaire',
    theme='Finance islamique',
    title="Combler le déficit infrastructurel africain par la finance islamique",
    summary="",
    # the embed Predika runs on its own page, resumed where it does
    video=dict(id='FmpB1cvTSUs', start=1037),
    speakers=[
      dict(name='Dr Mufti Yousuf Sultan', role='Votre intervenant', photo=None,
           bio="Dr Mufti Yousuf Sultan est un expert chevronné de la finance islamique, "
               "alliant une solide maîtrise de la charia à une spécialisation de pointe en "
               "fintech. Conseiller charia agréé auprès de la Commission des valeurs "
               "mobilières de Malaisie et de l'autorité de Labuan, il est certifié CIFE par "
               "Ethica (Dubaï). Distingué par les prix BAFF 2023 et du Président de l'INCEIF "
               "2023 en tant que meilleur doctorant, il est également co-auteur de l'ouvrage "
               "de référence « Finance responsable — Finance éthique et islamique » aux côtés "
               "de Tan Sri Dr Zeti, ancienne Gouverneure de la Banque centrale de Malaisie."),
      dict(name='Bashir Diaby', role='Modérateur', photo='assets/formateurs/06.jpg', bio=''),
    ],
  ),
  dict(
    slug='demarrage-parcours-cib',
    date='11 juillet 2026',
    iso='2026-07-11',
    status='Replay disponible',
    featured=False,
    format="Séance d'information",
    theme='Parcours certifiants',
    title="Séance d'information sur le démarrage du parcours certifiant CIB",
    summary="",
    video=None,
    # predika.pro publishes no recording for this session; the card carries a
    # picture from the brand library until the replay is linked
    thumb='assets/webinaires/demarrage-parcours-cib.png',
    speakers=[],
  ),
  dict(
    slug='produits-et-services-financiers-islamiques',
    date='19 juin 2026',
    iso='2026-06-19',
    status='Replay disponible',
    featured=False,
    format='Webinaire',
    theme='Produits islamiques',
    title="Les principaux produits et services financiers islamiques",
    summary="Comprenez les mécanismes essentiels de la finance islamique et ses alternatives "
            "concrètes au système conventionnel : les financements éthiques — Mourabaha "
            "(achat/revente à marge) et Ijara (leasing) ; les partenariats d'investissement — "
            "Moucharaka et Moudaraba (partage des profits et des pertes) ; les placements et "
            "levées de fonds — les Sukuk (titres adossés à des actifs réels).",
    video=None,
    # predika.pro publishes no recording for this session; the card carries a
    # picture from the brand library until the replay is linked
    thumb='assets/webinaires/produits-et-services-financiers-islamiques.png',
    speakers=[
      dict(name='Abdoulaye WANE', role='Intervenant', photo='assets/formateurs/01.jpg', bio=''),
      dict(name='Yaya SOW', role='Intervenant', photo='assets/formateurs/04.jpg', bio=''),
    ],
  ),
  dict(
    slug='introduction-finance-islamique',
    date='11 juin 2026',
    iso='2026-06-11',
    status='Replay disponible',
    featured=False,
    format='Webinaire',
    theme='Fondamentaux',
    title="Introduction à la Finance Islamique",
    summary="Un webinaire introductif conçu pour les professionnels, étudiants et "
            "entrepreneurs souhaitant comprendre les principes économiques et juridiques de "
            "la finance islamique. Découvrez les principes clés : interdiction de l'intérêt, "
            "partage des profits et gestion des risques.",
    video=None,
    # predika.pro publishes no recording for this session; the card carries a
    # picture from the brand library until the replay is linked
    thumb='assets/webinaires/introduction-finance-islamique.png',
    speakers=[
      dict(name='Abdoulaye WANE', role='Intervenant', photo='assets/formateurs/01.jpg', bio=''),
      dict(name='Yaya SOW', role='Intervenant', photo='assets/formateurs/04.jpg', bio=''),
    ],
  ),
]

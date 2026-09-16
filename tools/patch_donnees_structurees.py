#!/usr/bin/env python3
"""Donnees structurees : dire aux moteurs qui est derriere le site.

Sans elles, Google devine. Avec elles, il sait qu'il a affaire a un
studio lyonnais, il connait son adresse, son telephone, ses prestations,
et peut afficher ces informations dans ses resultats.

Rien n'est invente : tout vient des mentions legales et des pages.
"""
import json, os

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
SITE = 'https://www.biladesigns.com'

ORGANISATION = {
    "@type": "ProfessionalService",
    "@id": SITE + "/#studio",
    "name": "Bila Designs",
    "description": "Studio indépendant de design et d'automatisation : sites web sur "
                   "mesure, identité de marque, référencement et agents IA.",
    "url": SITE + "/accueil/",
    "email": "mathieu@biladesigns.com",
    "telephone": "+33659086800",
    "founder": {"@type": "Person", "name": "Mathieu Bila"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "320 avenue Berthelot",
        "postalCode": "69008",
        "addressLocality": "Lyon",
        "addressCountry": "FR",
    },
    "areaServed": {"@type": "Country", "name": "France"},
    "priceRange": "€€",
    "sameAs": [
        "https://www.instagram.com/biladesigns",
        "https://www.linkedin.com/company/biladesigns",
    ],
    "knowsLanguage": "fr",
}

SERVICES = {
    "@type": "OfferCatalog",
    "name": "Prestations",
    "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Création de site web et référencement"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Identité de marque et rebranding"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Automatisations et agents IA"}},
    ],
}


def fil(*etapes):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
            for i, (n, u) in enumerate(etapes)
        ],
    }


PAGES = {
    'accueil/index.html': [
        dict(ORGANISATION, hasOfferCatalog=SERVICES),
        {"@type": "WebSite", "@id": SITE + "/#site", "name": "Bila Designs",
         "url": SITE + "/accueil/", "inLanguage": "fr-FR",
         "publisher": {"@id": SITE + "/#studio"}},
    ],
    'avocats/index.html': [
        {"@type": "Service",
         "name": "Sites web et référencement pour cabinets d'avocats",
         "serviceType": "Création de site web, référencement et agents IA pour avocats",
         "provider": {"@id": SITE + "/#studio"},
         "areaServed": {"@type": "Country", "name": "France"},
         "audience": {"@type": "Audience", "audienceType": "Cabinets d'avocats"},
         "url": SITE + "/avocats/"},
        fil(("Accueil", "/accueil/"), ("Avocats", "/avocats/")),
    ],
    'services/index.html': [
        {"@type": "Service",
         "name": "Sites web et branding",
         "serviceType": "Stratégie de marque, identité visuelle, site web et référencement",
         "provider": {"@id": SITE + "/#studio"},
         "url": SITE + "/services/"},
        fil(("Accueil", "/accueil/"), ("Sites web & branding", "/services/")),
    ],
    'contact/index.html': [
        {"@type": "ContactPage", "url": SITE + "/contact/",
         "mainEntity": {"@id": SITE + "/#studio"}},
        fil(("Accueil", "/accueil/"), ("Contact", "/contact/")),
    ],
}

for page, blocs in PAGES.items():
    chemin = R + page
    if not os.path.exists(chemin):
        continue
    s = open(chemin, encoding='utf-8').read()
    if 'application/ld+json' in s:
        continue
    graphe = {"@context": "https://schema.org", "@graph": blocs}
    script = ('<script type="application/ld+json">%s</script>\n'
              % json.dumps(graphe, ensure_ascii=False, separators=(',', ':')))
    assert '</head>' in s
    s = s.replace('</head>', script + '</head>', 1)
    open(chemin, 'w', encoding='utf-8').write(s)
    print('%-28s %d bloc(s)' % (page, len(blocs)))

# La racine et le duplicata servent la meme page que /accueil/.
for f in ('index.html', 'accueil.html'):
    if not os.path.exists(R + f):
        continue
    s = open(R + 'accueil/index.html', encoding='utf-8').read()
    open(R + f, 'w', encoding='utf-8').write(s)
print('racine et accueil.html resynchronises')

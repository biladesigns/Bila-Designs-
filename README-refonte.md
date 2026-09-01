# Refonte biladesigns.com — septembre 2026

Le site est genere a partir des maquettes Claude Design (`.dc.html`), qui
restent la source de verite visuelle. Le runtime de prototypage
(`support.js`, `<x-dc>`, `<sc-for>`, `style-hover`, `x-import`) n'est pas
porte : il est traduit en HTML, CSS et JavaScript standard.

## Reconstruire

    sh tools/build_all.sh

Le script enchaine l'optimisation des images, la conversion des cinq
maquettes, les etapes de cablage, puis trois controles : structure des
balises, accessibilite de base, et absence de vestiges de l'ancien site.
Il echoue si l'un d'eux ne passe pas.

## Tester

    node tools/tests/responsive.js   # 11 largeurs x 8 pages
    node tools/tests/vitesse.js      # poids, FCP, LCP, CLS

Les deux ont besoin d'un serveur local a la racine du depot :

    python3 -m http.server 8899 --bind 127.0.0.1

**Piege connu** : en JavaScript l'option Playwright est `viewport`, pas
`viewportSize` (qui est la forme Python). Mal nommee, elle est ignoree
sans erreur et toutes les mesures se font a 1280 px. Le harnais verifie
desormais la largeur obtenue avant de conclure.

## Ce que fait chaque outil

| Fichier | Role |
|---|---|
| `tools/dc_convert.py` | Traduction mecanique d'une maquette en page autonome |
| `tools/build.py` | Les cinq pages, leurs metadonnees, et deux corrections de maquette |
| `tools/optimiser_images.py` | Illustrations de DA en WebP |
| `tools/optimiser_captures.py` | Captures de realisations en quatre largeurs |
| `tools/patch_contact.py` | Pastilles a choix unique en vraies radios |
| `tools/patch_avocats.py` | Constats d'audit et chaine du dossier |
| `tools/patch_forms.py` | Formulaires postables, validation, anti-robot |
| `tools/patch_liens.py` | Captures de realisations, srcset, liens externes |
| `tools/patch_nav.py` | Navigation et boutons alignes sur le brief |
| `tools/patch_images.py` | Priorites de chargement |
| `tools/patch_3d.py` | Realisations presentees en ecran incline |
| `tools/patch_mobile.py` | Marquages `.fx-row` et `.tN` pour le telephone |
| `tools/patch_annexes.py` | Redirections, plan du site, racine |
| `tools/build_annexes.py` | Pages legales et desabonnement dans la DA |
| `tools/sous_ensemble_polices.py` | Polices reduites aux caracteres utiles |
| `tools/valide.py` | Imbrication des balises |
| `tools/audit.py` | Accessibilite de base et liens internes |
| `tools/menage.py` | Aucun vestige de l'ancien site, aucun lien mort |

## Deux valeurs pilotees par variable

Toute la mise en page passe par deux variables definies dans
`assets/css/bila.css` :

- `--gut` : la gouttiere laterale du contenu (90 px au-dela de 1180 px)
- `--rail` : la position des filets verticaux (64 px au-dela de 1180 px)

Les redefinir dans une media query suffit a decliner le site. C'est ce
qui permet de tenir la regle « aucun filet ne croise du texte » a toutes
les largeurs, verifiee de 360 a 1920 px.

Les corps de police superieurs a 30 px sont convertis en `clamp()` qui
vaut exactement la valeur de la maquette au-dela de 1440 px de large.
Les corps inferieurs a 15 px recoivent une classe `.tN` et un plancher
de lisibilite sur telephone.

## Formulaires

Les trois formulaires postent sur FormSubmit. **L'activation est requise
par page** : la premiere soumission depuis une URL non activee declenche
un mail d'activation et n'arrive jamais. Les cinq pages du site sont
activees.

FormSubmit repond **HTTP 200 meme lorsqu'il refuse** : le seul signal
fiable est le champ `success` du corps de reponse. Ne jamais se fier a
`response.ok` seul.

## Ce qui reste a faire

- `assets/img/og.png` — l'image de partage referencee par les balises
  Open Graph n'existe pas encore.
- La page `/automatisations` est une page d'attente, en `noindex` et
  absente du plan du site.
- La page de confirmation du worker Cloudflare de desabonnement est
  encore dans l'ancien style generique.

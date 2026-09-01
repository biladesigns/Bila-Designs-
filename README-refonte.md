# Refonte biladesigns.com — septembre 2026

Le site est genere a partir des maquettes Claude Design (`.dc.html`), qui
restent la source de verite visuelle. Le runtime de prototypage
(`support.js`, `<x-dc>`, `<sc-for>`, `style-hover`, `x-import`) n'est pas
porte : il est traduit en HTML, CSS et JavaScript standard.

## Reconstruire

    sh tools/build_all.sh

Le script enchaine la conversion des cinq maquettes puis les etapes de
cablage, et se termine par deux controles : structure des balises et
audit (un seul `h1` par page, `alt` presents, aucun lien interne mort).

Les maquettes sont lues depuis le dossier d'origine ; leur chemin est en
tete de `tools/build.py`.

## Ce que fait chaque outil

| Fichier | Role |
|---|---|
| `tools/dc_convert.py` | Traduction mecanique d'une maquette en page autonome |
| `tools/build.py` | Les cinq pages, leurs metadonnees, et deux corrections de maquette |
| `tools/patch_contact.py` | Pastilles a choix unique en vraies radios |
| `tools/patch_avocats.py` | Constats d'audit et chaine du dossier |
| `tools/patch_forms.py` | Formulaires postables, validation, anti-robot |
| `tools/patch_liens.py` | Captures de realisations et liens externes |
| `tools/patch_nav.py` | Navigation et boutons alignes sur le brief |
| `tools/patch_images.py` | Priorites de chargement des images |
| `tools/patch_annexes.py` | Redirections, plan du site, racine |
| `tools/patch_annexes_da.py` | Palette et caracteres des pages legales |
| `tools/valide.py` | Imbrication des balises |
| `tools/audit.py` | Accessibilite de base et liens internes |

## Deux valeurs pilotees par variable

Toute la mise en page passe par deux variables definies dans
`assets/css/bila.css` :

- `--gut` : la gouttiere laterale du contenu (90 px au-dela de 1180 px)
- `--rail` : la position des filets verticaux (64 px au-dela de 1180 px)

Les redefinir dans une media query suffit a decliner le site. C'est ce
qui permet de tenir la regle « aucun filet ne croise du texte » a toutes
les largeurs, verifiee de 390 a 1920 px.

Les corps de police superieurs a 30 px sont convertis en `clamp()` qui
vaut exactement la valeur de la maquette au-dela de 1440 px de large.

## Ce qui reste a faire

- **Les quatre images de direction artistique** (`assets/img/`) sont des
  emplacements temporaires. Deposer les vrais fichiers du dossier
  `assets/` de la maquette, sous les memes noms :
  `hero-arche-crop.png`, `hero-avocats.png`, `hero-atelier.png`,
  `section-arche.png`.
- **L'image de partage** `assets/img/og.png`, referencee par les balises
  Open Graph, n'existe pas encore.

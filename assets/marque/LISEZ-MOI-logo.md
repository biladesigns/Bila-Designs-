# Logo « Deux encres » — dossier d'implémentation

Nouveau logotype Bila Designs. Ce dossier contient tout ce qu'il faut pour le poser sur le site et remplacer l'ancienne marque, sans avoir à décider quoi que ce soit.

---

## 1. Ce qu'est la marque

Deux lettres — **B** et **D** — composées en **Fraunces 600** et imprimées l'une sur l'autre. Le D remonte sur le B de `-0.34em`, et les deux lettres sont en `mix-blend-mode: multiply`. La zone commune produit une **troisième couleur**.

Ce n'est pas un effet décoratif : le recouvrement *est* la marque. Sans lui, ce ne sont plus que deux initiales côte à côte.

| Encre | Valeur | Rôle |
|---|---|---|
| B | `#101B33` | Encre de fond, la plus dense |
| D | `#2743E3` | Encre de dessus, transparente |
| Recouvrement | `#02072D` | Produit des deux — à reproduire tel quel si le mélange est impossible |

Sur fond navy, la logique s'inverse : `mix-blend-mode: screen`, B en `#FFFFFF`, D en `#5D7EFF`.

---

## 2. Ce que contient le dossier

### `png/`

| Fichier | Dimensions | Usage |
|---|---|---|
| `bd-light.png` | 120 × 89 | Fond clair, densité 1× |
| `bd-light-2x.png` | 240 × 178 | Fond clair, écrans Retina |
| `bd-light-4x.png` | 565 × 420 | Master fond clair |
| `bd-light-transparent-4x.png` | 565 × 420 | Fond transparent, à poser sur du crème ou du blanc cassé |
| `bd-dark.png` / `-2x` / `-4x` | idem | Fond navy |
| `bd-dark-transparent-4x.png` | 565 × 420 | Fond transparent, pour fonds sombres |
| `bd-mono-4x.png` | 565 × 420 | Monochrome navy, D à 62 % — tampon, gravure, impression une couleur |

Ratio constant : **1.345** (565 / 420).

### `favicon/`

| Fichier | Usage |
|---|---|
| `favicon-16.png` … `favicon-512.png` | Jeu complet, fond navy `#101B33` |
| `favicon-180.png` | Apple touch icon |
| `favicon-192.png` / `favicon-512.png` | Manifeste PWA |
| `apple-touch-1024.png` | App Store / grandes tuiles |
| `favicon-light-512.png` | Variante fond blanc, pour un thème clair forcé |

Le favicon est la **seule exception de format** : carré 1:1, fond navy, monogramme centré. Il ne porte jamais le nom.

---

## 3. Comment l'implémenter sur le site

### Cas nominal — texte vivant

Sur le site, le logo n'est **pas une image**. Il est composé en HTML, ce qui le garde net à toutes les tailles et permet au navigateur de le rendre avec la vraie Fraunces déjà chargée par le site.

```html
<a class="logo" href="/" aria-label="Bila Designs — accueil">
  <span class="logo__bd" aria-hidden="true">
    <span class="logo__b">B</span><span class="logo__d">D</span>
  </span>
  <span class="logo__rule"></span>
  <span class="logo__name">Bila Designs</span>
</a>
```

```css
.logo        { display: inline-flex; align-items: center; gap: 15px; }
.logo__bd    { display: inline-flex; isolation: isolate;
               font-family: Fraunces, Georgia, serif; font-weight: 600;
               font-size: 44px; line-height: 0.82; letter-spacing: -0.02em; }
.logo__b     { color: #101B33; mix-blend-mode: multiply; }
.logo__d     { margin-left: -0.34em; color: #2743E3; mix-blend-mode: multiply; }
.logo__rule  { width: 1px; align-self: stretch; background: rgba(16, 27, 51, 0.2); }
.logo__name  { font-family: Archivo, sans-serif; font-weight: 700;
               font-size: 0.48em; letter-spacing: -0.012em; color: #101B33; }

/* en-tête sur fond navy */
.logo--dark .logo__b    { color: #FFFFFF; mix-blend-mode: screen; }
.logo--dark .logo__d    { color: #5D7EFF; mix-blend-mode: screen; }
.logo--dark .logo__name { color: #FFFFFF; }
.logo--dark .logo__rule { background: rgba(255, 255, 255, 0.22); }

/* repli sans mélange — PDF, export, capture */
.logo--flat .logo__b,
.logo--flat .logo__d { mix-blend-mode: normal; }
```

**Trois points à ne pas rater :**

1. `isolation: isolate` sur `.logo__bd` est **obligatoire**. Sans lui, les lettres se mélangent avec le fond de la page entière, pas seulement entre elles.
2. Fraunces doit être chargée en graisse **600**. Si la police n'est pas encore arrivée, le repli Georgia donne un rendu acceptable ; ne mets pas `font-display: block`, qui ferait clignoter le logo.
3. `.logo__name` est en `em` : il suit automatiquement la taille du monogramme. Ne le fixe pas en pixels.

### Où utiliser les PNG à la place

Uniquement là où le mélange ne passe pas : e-mails, exports PDF, Open Graph, favicon, documents bureautiques, partenaires. Partout ailleurs sur le site, c'est du texte.

---

## 4. Balises à poser dans le `<head>`

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon/favicon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="/favicon/favicon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#101B33">
```

Génère le `.ico` multi-résolutions à partir de `favicon-16.png`, `favicon-32.png` et `favicon-48.png`.

`site.webmanifest` :

```json
{
  "name": "Bila Designs",
  "short_name": "Bila",
  "icons": [
    { "src": "/favicon/favicon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/favicon/favicon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#101B33",
  "background_color": "#FBFBFA",
  "display": "standalone"
}
```

---

## 5. Verrouillage, air, tailles

- **Verrouillage** : monogramme, filet vertical de 1 px `rgba(16,27,51,0.2)` à hauteur du monogramme, puis le nom en Archivo 700. Écart de 15 px de chaque côté du filet.
- **Nom** : Archivo 700 à **0.48 ×** le corps du monogramme, interlettrage `-0.012em`.
- **Zone de protection** : la hauteur du B, sur les quatre côtés. Rien dedans — ni texte, ni filet, ni bord de conteneur.
- **Taille minimale** : corps 20 px à l'écran, 7 mm en impression. En dessous, le recouvrement se referme et les deux lettres se confondent.

---

## 6. Ce qui casse la marque

- Décoller les lettres, ou modifier le `-0.34em`.
- Inverser les couleurs : le bleu est **toujours** l'encre de dessus.
- Changer de police. Sans le contraste du sérif, le recouvrement devient une bouillie.
- Ajouter contour, ombre, dégradé, ou arrondir quoi que ce soit.
- Poser le monogramme sur une photo ou une texture : le mélange devient illisible. Sur image, utiliser un PNG à fond plein.

---

## 7. À remplacer sur le site

L'ancienne marque — le rectangle bleu avec ses deux jambes blanches — apparaît dans l'en-tête et le pied de page de **toutes** les pages, ainsi que dans le favicon. Remplace chaque occurrence par le verrouillage ci-dessus :

- en-tête : monogramme à 26 px de corps environ, avec le nom ;
- pied de page : même verrouillage, corps légèrement réduit ;
- favicon et manifeste : les fichiers de `favicon/`.

La charte visuelle complète, avec les rendus de chaque cas et les contre-exemples, est dans `Charte Logo Deux Encres.dc.html` à la racine du projet.

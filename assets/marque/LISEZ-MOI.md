# Signature mail — Bila Designs

Logo **« Deux encres »**, version prospection avocats. Le fichier `signature-bila-designs.html` est la source de vérité : ouvre-le dans un navigateur, le bloc à copier est la première `<table>` de la page.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `signature-bila-designs.html` | Page de copie + signature complète, monogramme embarqué en base64 |
| `assets/bd-mark.png` | Le monogramme rendu, 424 × 315 (densité ≈ 7×), fond blanc |

## Le logo — « Deux encres »

Deux lettres en **Fraunces 600** imprimées l'une sur l'autre. Le D remonte sur le B de `-0.34em` et les deux sont en `mix-blend-mode: multiply`, ce qui crée une troisième couleur dans la zone commune. Ce n'est pas un effet décoratif : c'est la marque.

| Encre | Valeur | Rôle |
|---|---|---|
| B | `#101B33` | Encre de fond |
| D | `#2743E3` | Encre de dessus, transparente |
| Recouvrement | `#02072D` | Produit des deux, à reproduire tel quel si le mélange est impossible |

Sur fond navy la logique s'inverse : `mix-blend-mode: screen`, B en `#FFFFFF`, D en `#5D7EFF`.

**Contrainte de code :** le mélange exige `isolation: isolate` sur le conteneur, sinon les lettres se mélangent avec le fond de la page. La charte complète est dans `Charte Logo Deux Encres.dc.html`.

## Pourquoi le monogramme est une image

Aucun client mail ne gère `mix-blend-mode`, et Fraunces ne s'y charge pas non plus : en texte, la marque tomberait en Times avec deux lettres qui se chevauchent bêtement. Le monogramme est donc rendu en PNG à densité 7×, **encodé en base64 directement dans le `src`** — rien à héberger, rien à recharger, et il survit au copier-coller vers Gmail.

Si tu régénères ce PNG : rends-le sur fond blanc, recadre au pixel d'encre, et garde le ratio **1.346** (424 × 315). Dans la signature il est affiché à `width="62" height="46"`.

## Contenu de la signature

- **Mathieu Bila**
- Fondateur · Bila Designs
- Sites web, référencement & automatisations
- mathieu@biladesigns.com — `mailto:`
- 06 59 08 68 00 — `tel:+33659086800` · biladesigns.com
- Accroche en serif : « Des cabinets m'ont déjà confié leur site. » + lien **Voir leur avant / après →** vers `https://biladesigns.com`
- Mention de clôture : Lyon, France · réponse sous 24 h ouvrées

Un filet vertical `rgba(16,27,51,0.18)` sépare le monogramme du bloc texte — c'est le verrouillage défini dans la charte.

## Typographie

| Élément | Police | Corps | Couleur |
|---|---|---|---|
| Nom | Archivo 700 (repli Helvetica, Arial) | 17 px | `#101B33` |
| Fonction | Archivo 400/600 | 12,5 px | `#4A5163` / `#101B33` |
| Spécialités | Archivo 400 | 12,5 px | `#6B7280` |
| Coordonnées | Archivo 400/600 | 12,5 px | `#4A5163` / `#2743E3` |
| Accroche | Georgia | 14,5 px | `#101B33` |
| Clôture | Archivo 400 | 11 px | `#A0A5B0` |

Georgia remplace Fraunces dans le corps de la signature : c'est le seul serif fiable dans les clients mail. Ne charge aucune webfont.

## Intégration

1. Ouvrir `signature-bila-designs.html` dans un navigateur.
2. Sélectionner du monogramme jusqu'à « réponse sous 24 h ouvrées », copier.
3. Gmail → Paramètres → Général → Signature → Créer, puis coller.

Pour Outlook, Apple Mail ou un autre client : reprendre la `<table>` telle quelle. Elle est en styles `inline`, sans classe ni feuille de style — c'est voulu, aucun client mail ne garantit le `<style>`.

## Contraintes à respecter

- Largeur fixée à 520 px. Ne pas dépasser 540 : au-delà, la signature casse sur mobile.
- Tables et styles inline uniquement. Pas de flex, pas de grid, pas d'image de fond.
- Pas de tracker, pas de pixel espion.
- Les liens gardent `text-decoration: none` et une couleur explicite, sinon Gmail les repasse en bleu système.
- Toujours un repli après chaque police : `Georgia, 'Times New Roman', serif` et `Archivo, Helvetica, Arial, sans-serif`.

## `bd-mark-mail@3x.png` — la version des signatures de mail

258 × 210, a afficher en 86 × 70. C'est `bd-mark@3x.png` pose au centre d'une
plaque blanche avec 36 px de marge de chaque cote (12 px une fois affiche).

Le monogramme est livre sans marge : dans une signature de mail lue en mode
sombre, le rectangle blanc de l'image epouse exactement les lettres et le logo
parait enferme dans une boite. La marge lui rend de l'air.

Ne pas remplacer `bd-mark@3x.png` par celle-ci : le site s'en sert sans fond
blanc. Deux usages, deux fichiers.

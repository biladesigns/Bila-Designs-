# Signature mail — Bila Designs

Version retenue : **prospection avocats**. Le fichier `signature-bila-designs.html` contient la signature prête à copier, entourée d'un mode d'emploi ; le bloc à reprendre est la seule `<table>` de la page.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `signature-bila-designs.html` | Page de copie + signature complète (source de vérité) |
| `assets/logo-mark.svg` | Marque seule, 44 × 50 — sur fond navy uniquement |
| `assets/logo-mark-framed.svg` | Marque dans son cadre navy, 58 × 64 — **c'est celle de la signature** |
| `assets/favicon.svg` | Carré 32 × 32, exception de format |

## La marque

Champ bleu `#2743E3` de 44 × 50, deux jambes blanches en quart d'ellipse (largeur 12, hauteur 50) à fleur des bords gauche et droit, vide central bleu de 20 en bas.

```
M0 0 L0 50 L12 50 A12 50 0 0 0 0 0 Z
M44 0 L44 50 L32 50 A12 50 0 0 1 44 0 Z
```

**Règle non négociable :** sur fond clair — et le corps d'un mail est blanc — la marque doit porter son cadre navy `#101B33` (marge de 7 sur les quatre côtés, soit 1/7 de la largeur). Sans lui, les jambes blanches se fondent dans le fond et il ne reste qu'un V bleu. C'est pour cette raison que la signature utilise `logo-mark-framed.svg` et non `logo-mark.svg`.

Ne jamais : arrondir les angles, changer le rapport 44/50, ajouter dégradé, ombre ou contour, descendre sous 24 px de large.

## Contenu de la signature

- **Mathieu Bila**
- Bila Designs · sites web pour cabinets d'avocats
- mathieu@biladesigns.com — `mailto:`
- 06 59 08 68 00 — `tel:+33659086800`
- Accroche : « Des cabinets m'ont déjà confié leur site. » + lien **Voir leur avant / après →** vers `https://biladesigns.com`

Le nom et l'intitulé sont à confirmer côté Mathieu.

## Typographie

| Élément | Police | Corps | Couleur |
|---|---|---|---|
| Nom | Archivo 700 (repli Helvetica, Arial) | 16 px | `#101B33` |
| Ligne d'activité | Archivo 400 | 12,5 px | `#4A5163` |
| Coordonnées | Archivo 400 / 600 | 12,5 px | `#4A5163` / `#2743E3` |
| Accroche | Georgia (serif) | 14,5 px | `#101B33` |

Fraunces, la police de titrage du site, ne s'affiche pas dans les clients mail : Georgia la remplace, dans le même registre. Ne pas charger de webfont — aucun client mail fiable ne les honore.

Filet de séparation au-dessus de l'accroche : 1 px `rgba(39,67,227,0.28)`.

## Intégration

1. **Gmail (le plus simple).** Ouvrir `signature-bila-designs.html` dans un navigateur, sélectionner la signature du « M » de Mathieu jusqu'à la flèche en incluant le carré bleu, copier, puis Paramètres → Général → Signature → Créer, et coller.
2. **Outlook, Apple Mail, clients divers.** Reprendre le bloc `<table>` tel quel. Il est en styles `inline`, sans classe ni feuille de style : c'est voulu, aucun client mail ne garantit le `<style>`.
3. **Si la marque ne passe pas.** Certains clients rabotent `border-radius` sur les `<div>`. Dans ce cas, remplacer le bloc de la marque par une image hébergée : exporter `assets/logo-mark-framed.svg` en PNG à 116 × 128 (densité 2×), l'héberger sur `biladesigns.com`, et l'appeler en `<img src="…" width="58" height="64" alt="Bila Designs">`. Ne pas utiliser de SVG en pièce jointe : Gmail ne l'affiche pas.

## Contraintes à respecter

- Largeur totale libre, mais rien ne doit dépasser 540 px : au-delà, la signature casse sur mobile.
- Pas d'image de fond, pas de `position: fixed`, pas de flex : uniquement des tables et des styles inline.
- Pas de tracker, pas de pixel espion.
- Les liens gardent `text-decoration: none` et une couleur explicite : sans cela, Gmail les repasse en bleu système.
- Une seule police par élément, avec son repli. Jamais `font-family: Fraunces` sans `Georgia, serif` derrière.

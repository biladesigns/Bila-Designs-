#!/bin/sh
# Reconstruit tout le site a partir des maquettes, dans l'ordre.
set -e
cd "$(dirname "$0")/.."
python3 tools/optimiser_images.py
python3 tools/optimiser_captures.py
python3 tools/faire_og.py
python3 tools/build.py
python3 tools/patch_contact.py
python3 tools/patch_avocats.py
python3 tools/patch_avocats_audit.py
python3 tools/patch_seo_schema.py
python3 tools/patch_services_etapes.py
python3 tools/patch_avocats_details.py
python3 tools/patch_forms.py
python3 tools/patch_liens.py
python3 tools/patch_nav.py
python3 tools/patch_images.py
python3 tools/patch_3d.py
python3 tools/patch_logo.py
python3 tools/patch_donnees_structurees.py
python3 tools/patch_annexes.py
python3 tools/build_annexes.py
python3 tools/audit.py
python3 tools/patch_menu.py
python3 tools/patch_mobile.py
python3 tools/patch_versions.py
python3 tools/menage.py
python3 tools/valide.py accueil/index.html services/index.html avocats/index.html contact/index.html automatisations/index.html mentions-legales/index.html politique-confidentialite/index.html desabonnement/index.html index.html accueil.html

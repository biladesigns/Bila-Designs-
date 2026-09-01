#!/bin/sh
# Reconstruit tout le site a partir des maquettes, dans l'ordre.
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
python3 tools/patch_contact.py
python3 tools/patch_avocats.py
python3 tools/patch_forms.py
python3 tools/patch_liens.py
python3 tools/patch_nav.py
python3 tools/patch_images.py
python3 tools/patch_annexes.py
python3 tools/patch_annexes_da.py
python3 tools/audit.py
python3 tools/valide.py accueil/index.html services/index.html avocats/index.html contact/index.html automatisations/index.html

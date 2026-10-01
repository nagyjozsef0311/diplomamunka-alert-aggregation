#!/usr/bin/env bash
# A thesis/ mappából Overleafbe importálható zip készítése (Overleaf: New Project → Upload Project).
#
# Használat:
#   scripts/export_overleaf.sh [verziónév]     # alapértelmezés: a legutóbbi thesis-v* tag vagy a dátum
#
# Az eredmény: thesis/export/diplomamunka_<verzió>.zip (a .gitignore miatt nem kerül a tárolóba).
# A személyes adatot tartalmazó előlapok (feladatlap, borítólap) csak akkor kerülnek bele, ha helyben
# megvannak; ha nincsenek, Overleafben kell feltölteni őket az includes/ mappába.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root/thesis"

version="${1:-$(git describe --tags --match 'thesis-v*' --abbrev=0 2>/dev/null || date +%Y-%m-%d)}"
mkdir -p export
out="export/diplomamunka_${version}.zip"
rm -f "$out"

zip -q -r "$out" main.tex template.tex acronyms.tex references.bib chapters img includes \
    -x '*.aux' '*.log' '.DS_Store'

echo "[kész] thesis/$out"

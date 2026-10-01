#!/bin/bash
# Munkamenet-indító: a webes (Claude Code on the web) munkamenetben telepíti a Python-csomagot
# a fejlesztői függőségekkel (pytest, ruff, jupyterlab, matplotlib), és a dolgozat fordításához
# szükséges LaTeX-et (pdflatex, biber, latexmk, magyar nyelvi csomag). Többször is futtatható.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Python: a csomag szerkeszthető telepítése a fejlesztői eszközökkel
python3 -m pip install --quiet --disable-pip-version-check --root-user-action=ignore -e ".[dev]"

# LaTeX a thesis/ fordításához (csak ha még nincs fent)
if ! command -v pdflatex >/dev/null || ! command -v biber >/dev/null || ! command -v latexmk >/dev/null; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq --no-install-recommends \
    texlive-latex-recommended texlive-latex-extra texlive-lang-european \
    texlive-fonts-recommended texlive-bibtex-extra biber latexmk zip >/dev/null
fi

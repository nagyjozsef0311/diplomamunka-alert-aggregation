#!/usr/bin/env python3
"""3. lépés-előkészítés: a rangsoroló súlyainak kiszámítása a szerző páros összehasonlításából.

Dolgozat: 4.3 (súlyozott összeg, AHP, következetességi arány), 6.3 (előzetes rögzítés).
Bemenet:  config/elozetes_rogzites/ahp_rangsorolo_itelet.yaml (a szerző tölti ki)
Futtatás: python experiments/03_rangsorolo_ahp_sulyok_szamitasa.py
Eredmény: results/03_rangsorolo_ahp_sulyok.md
"""

from __future__ import annotations

import sys
from pathlib import Path

from alertagg import paros_osszehasonlitas

ROOT = Path(__file__).resolve().parents[1]
BE = ROOT / "config" / "elozetes_rogzites" / "ahp_rangsorolo_itelet.yaml"
KI = ROOT / "results" / "03_rangsorolo_ahp_sulyok.md"
NEVEK = {"r": "kockázati pontszám", "g": "gép fontossága", "a": "alkalmazhatóság",
         "m": "megfigyeltség"}


def main() -> int:
    try:
        e = paros_osszehasonlitas.betoltes(BE)
    except ValueError as err:
        print(f"[NINCS KÉSZ] {err}\nTöltsd ki: {BE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    sorok = [
        "# A rangsoroló súlyai – páros összehasonlítás (AHP)",
        "",
        f"Bemenet: `{BE.relative_to(ROOT)}` · dolgozat: 4.3, 6.3",
        "",
        "| Szempont | Súly |",
        "| --- | ---: |",
        *[f"| {NEVEK.get(k, k)} ({k}) | {v:.3f} |" for k, v in e.sulyok.items()],
        "",
        (f"λmax = {e.lambda_max:.4f} · CI = {e.ci:.4f} · **CR = {e.cr:.4f}** "
        f"({'elfogadható, < 0,10' if e.kovetkezetes else 'NEM elfogadható, felül kell vizsgálni'})"),
        "",
    ]
    KI.write_text("\n".join(sorok), encoding="utf-8")
    print("\n".join(sorok))
    return 0 if e.kovetkezetes else 2


if __name__ == "__main__":
    sys.exit(main())

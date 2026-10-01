#!/usr/bin/env python3
"""A CATS (Uetz et al. 2026) kódjának és átalakított adathalmazainak letöltése.

Forrás: https://github.com/962012d09b/cats – a cikk bírálata miatt jelenleg névtelenített tároló,
licenc nincs megadva. Ezért NEM tesszük a saját tárolónkba, csak rögzített commitra letöltjük
a data/external/cats/ mappába (amely a .gitignore miatt nem kerül fel).

Hivatkozás: R. Uetz, P. Bönninghausen, L. Hackländer-Jansen, M. Henze:
"Can Risk-Based Alerting Mitigate Cybersecurity Alert Fatigue?", arXiv:2609.02465 (2026).

Használat:
    python scripts/download_cats.py [--dest data/external/cats] [--ref 628cf48]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_URL = "https://github.com/962012d09b/cats.git"
DEFAULT_REF = "628cf48"  # az "Initial commit", 2026-10-01-i állapot
AIT_ARCHIVES = ["ait_wazuh.zip", "ait_suricata.zip"]


def run(*cmd: str, cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", type=Path, default=Path("data/external/cats"))
    parser.add_argument("--ref", default=DEFAULT_REF, help="a használt commit (rögzített verzió)")
    args = parser.parse_args()

    if not (args.dest / ".git").exists():
        args.dest.parent.mkdir(parents=True, exist_ok=True)
        run("git", "clone", REPO_URL, str(args.dest))
    run("git", "fetch", "--all", "--quiet", cwd=args.dest)
    run("git", "checkout", "--quiet", args.ref, cwd=args.dest)

    # Az AIT-ADS CATS-formátumú (felcímkézett) változatainak kicsomagolása
    out = args.dest.parent / "cats_datasets"
    out.mkdir(parents=True, exist_ok=True)
    for name in AIT_ARCHIVES:
        archive = args.dest / "datasets" / name
        if not archive.exists():
            print(f"[HIÁNYZIK] {archive}", file=sys.stderr)
            return 1
        with zipfile.ZipFile(archive) as z:
            z.extractall(out)
        print(f"[kicsomagolva] {name} -> {out}")

    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.dest, check=True,
                            capture_output=True, text=True).stdout.strip()
    print(f"[kész] CATS commit: {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

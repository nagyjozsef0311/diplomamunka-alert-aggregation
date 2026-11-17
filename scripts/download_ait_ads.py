#!/usr/bin/env python3
"""Az AIT Alert Data Set (AIT-ADS) 1. verziójának letöltése és kicsomagolása.

Forrás: Zenodo 8263181 (CC BY 4.0) – Landauer, Skopik, Wurzenberger (2024),
"Introducing a New Alert Data Set for Multi-Step Attack Analysis", DOI 10.1145/3675741.3675748.

Használat:
    python scripts/download_ait_ads.py [--dest data/ait_ads] [--no-extract]

A letöltött fájlok MD5-ellenőrzőösszegét a Zenodo által közölt értékkel vetjük össze,
így biztos, hogy mindenki ugyanazon az adaton mér.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

RECORD_ID = "8263181"
FILES = {
    # fájlnév: (letöltési URL, MD5, méret bájtban) – a Zenodo API szerint, 2026-10-01
    "ait_ads.zip": (
        f"https://zenodo.org/api/records/{RECORD_ID}/files/ait_ads.zip/content",
        "43db6b1f0996e0024befd617706c50e9",
        96_202_946,
    ),
    "labels.csv": (
        f"https://zenodo.org/api/records/{RECORD_ID}/files/labels.csv/content",
        "60ff33796c77fd2136c4d1a4bc841bd9",
        3_703,
    ),
}


def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, target: Path, size: int) -> None:
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with target.open("wb") as f, tqdm(total=size, unit="B", unit_scale=True,
                                          desc=target.name) as bar:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
                bar.update(len(chunk))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", type=Path, default=Path("data/ait_ads"))
    parser.add_argument("--no-extract", action="store_true", help="ne csomagolja ki a zip-et")
    args = parser.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)

    for name, (url, expected_md5, size) in FILES.items():
        target = args.dest / name
        if target.exists() and md5sum(target) == expected_md5:
            print(f"[megvan] {name}")
            continue
        print(f"[letöltés] {name}")
        download(url, target, size)
        actual = md5sum(target)
        if actual != expected_md5:
            print(f"[HIBA] {name}: MD5 eltér ({actual} != {expected_md5})", file=sys.stderr)
            return 1
        print(f"[rendben] {name}")

    if not args.no_extract:
        archive = args.dest / "ait_ads.zip"
        with zipfile.ZipFile(archive) as z:
            z.extractall(args.dest)
        print(f"[kicsomagolva] {args.dest}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

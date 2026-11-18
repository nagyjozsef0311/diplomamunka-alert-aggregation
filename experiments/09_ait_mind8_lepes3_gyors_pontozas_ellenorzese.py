#!/usr/bin/env python3
"""A kockázati pontszám gyors (vektoros) számításának ellenőrzése a CATS eredeti kódjával.

Dolgozat: 4.2.1, 7. fejezet (megvalósítás). A CATS minden riasztásnál végigjárja az időablakot, ami a
nagy forgatókönyveken (450–500 ezer gépi riasztás) négyzetes futásidőt ad. A gyors változat
(``kockazati_pontszam.component_scores_vektoros``) ugyanazokat a képleteket számolja; ez a szkript
riasztásonként összeveti a kettőt azokon a forgatókönyveken, ahol az eredeti kód belátható idő alatt
lefut (CATS-változat: russellmitchell; eredeti formátum: russellmitchell, santos, shaw, wardbeck).
CÍMKÉKET NEM HASZNÁL.

Futtatás: python experiments/09_ait_mind8_lepes3_gyors_pontozas_ellenorzese.py
Eredmény: results/09_ait_mind8_lepes3_gyors_pontozas_ellenorzese.md
"""

from __future__ import annotations

import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from alertagg import kockazati_pontszam as kp
from alertagg.egysegesito import load_ait_wazuh_json, load_cats_jsonl

ROOT = Path(__file__).resolve().parents[1]
AIT = ROOT / "data" / "ait_ads"
CATS = ROOT / "data" / "external" / "cats_datasets"
CACHE = ROOT / "data" / "cache"
NEV = "09_ait_mind8_lepes3_gyors_pontozas_ellenorzese"
FORGATOKONYVEK = ["russellmitchell", "santos", "shaw", "wardbeck"]


def osszevet(alerts: pd.DataFrame, cimke: str, cache: Path | None = None) -> dict:
    t0 = time.time()
    if cache is not None and cache.exists():
        ref = pd.read_pickle(cache).loc[alerts["alert_id"]]
        t_cats = float("nan")
    else:
        ref = kp.component_scores(alerts)
        t_cats = time.time() - t0
        if cache is not None:
            ref.to_pickle(cache)
    t1 = time.time()
    gyors = kp.component_scores_vektoros(alerts)
    t_gyors = time.time() - t1
    d = (gyors - ref.to_numpy()).abs().max()
    return {"adat": cimke, "riasztas": len(alerts), "CATS_mp": t_cats, "gyors_mp": t_gyors,
            **{f"max_elteres_{m}": d[m] for m in kp.MODULES}}


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    sorok = []
    for nev in ["ait_wazuh", "ait_suricata"]:
        alerts, _ = load_cats_jsonl(CATS / f"{nev}.jsonl")  # a címkét eldobjuk
        sorok.append(osszevet(alerts, f"CATS-változat {nev}",
                              CACHE / f"{nev}_kockazati_reszpontszamok.pkl"))
    for f in FORGATOKONYVEK:
        for erz in ["wazuh", "suricata"]:
            alerts = load_ait_wazuh_json(AIT / f"{f}_wazuh.json", f, erzekelo=erz)
            sorok.append(osszevet(alerts, f"eredeti {f} {erz}",
                                  CACHE / f"ait_{f}_{erz}_cats_eredeti.pkl"))
            print(sorok[-1], flush=True)
    df = pd.DataFrame(sorok)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    md = ["# A gyors kockázati pontszám ellenőrzése a CATS eredeti kódjával", "",
          f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · CATS: 628cf48a", "",
          ("A táblázat riasztásonként a legnagyobb abszolút eltérést adja a két számítás között "
           "(részpontszámonként; a pontszámok 0 és 1 közé esnek). A CATS_mp üres, ha az eredeti "
           "kód eredménye a gyorsítótárból jött."), "",
          df.to_markdown(index=False, floatfmt=".3g"), ""]
    (ROOT / "results" / f"{NEV}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

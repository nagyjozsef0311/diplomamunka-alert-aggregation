#!/usr/bin/env python3
"""1. mérés: a kockázatalapú pontozás (Uetz és mtsai. 2026) visszamérése az AIT-ADS russellmitchell
forgatókönyvén (CATS-változat). Ez a 3. értékelési lépés hitelességének ellenőrzése.

Futtatás:  python experiments/01_ait_russellmitchell_lepes1_3_alapvonal_visszamerese.py
Eredmény:  results/01_ait_russellmitchell_lepes1_3_alapvonal_visszamerese.csv és .md

A részpontszámokat a data/ mappában gyorsítótárazzuk (a Wazuh-adathalmazon kb. 4 perc).
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from alertagg import ertekeles, kockazati_pontszam
from alertagg.egysegesito import load_cats_jsonl

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "external" / "cats_datasets"
CACHE = ROOT / "data" / "cache"
OUT = ROOT / "results"

# A cikk 4. táblázatának értékei (AUROC), összevetéshez
PAPER = {
    "ait_wazuh": {"level": 0.99, "accumulation": 1.00, "variety": 1.00, "rarity": 0.07,
                  "aperiodicity": 0.01, "pipeline_loo": 0.98},
    "ait_suricata": {"level": 0.81, "accumulation": 0.66, "variety": 0.96, "rarity": 0.99,
                     "aperiodicity": 0.95, "pipeline_loo": 0.99},
}


def components(name: str) -> tuple[pd.DataFrame, pd.Series]:
    alerts, labels = load_cats_jsonl(DATA / f"{name}.jsonl")
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{name}_kockazati_reszpontszamok.pkl"
    if cache.exists():
        comp = pd.read_pickle(cache)
    else:
        comp = kockazati_pontszam.component_scores(alerts)
        comp.to_pickle(cache)
    return comp, labels.loc[comp.index]


def main() -> None:
    rows = []
    for name in ["ait_wazuh", "ait_suricata"]:
        comp, y = components(name)
        sensor = name.split("_")[1]
        variants = {m: comp[m] for m in kockazati_pontszam.MODULES}
        variants["pipeline_mean"] = kockazati_pontszam.risk_score(comp, kockazati_pontszam.WEIGHTS["mean"])
        variants["pipeline_loo"] = kockazati_pontszam.risk_score(comp, kockazati_pontszam.WEIGHTS[f"loo_{sensor}"])
        for variant, scores in variants.items():
            row = {"dataset": name, "variant": variant, "n": len(y), "n_true": int(y.sum())}
            row.update(ertekeles.summary(y.to_numpy(), scores.to_numpy()))
            row["paper_auroc"] = PAPER[name].get(variant)
            rows.append(row)
    df = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    df.to_csv(OUT / "01_ait_russellmitchell_lepes1_3_alapvonal_visszamerese.csv", index=False, float_format="%.4f")

    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    cats = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT / "data/external/cats",
                          capture_output=True, text=True, check=False).stdout.strip()
    fmt = df.copy()
    for c in ["auroc", "ap", "recall_top10", "workload_98", "paper_auroc"]:
        fmt[c] = fmt[c].map(lambda v: "" if pd.isna(v) else f"{v:.3f}")
    fmt["true_in_top10"] = fmt["true_in_top10"].map(lambda v: f"{v:.1f}")
    lines = [
        "# 1. mérés – a kockázatalapú pontozás visszamérése (AIT-ADS, russellmitchell)",
        "",
        (f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · "
         f"CATS: `{cats}` · adat: CATS-változat (`ait_wazuh.jsonl`, `ait_suricata.jsonl`)"),
        "",
        ("Oszlopok: rangsor-pontosság (AUROC), átlagos pontosság (AP), a valódi riasztások aránya "
         "és várható száma a lista első 10%-ában, a 98%-os találathoz átnézendő listarész, a "
         "cikkben közölt AUROC."),
        "",
        fmt.drop(columns=["n"]).to_markdown(index=False),
        "",
    ]
    (OUT / "01_ait_russellmitchell_lepes1_3_alapvonal_visszamerese.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

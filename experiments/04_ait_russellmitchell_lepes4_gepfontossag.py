#!/usr/bin/env python3
"""4. lépés: a kockázati pontszám kiegészítése a gép fontosságával (AIT-ADS, russellmitchell).

Dolgozat: 4.3 (súlyozott összeg, a kimaradó szempontok súlyának elhagyása és újranormálás),
6.2. táblázat (4. lépés), 6.3 (mérőszámok, ellenpróba összekevert fokozatokkal, ±20%-os
érzékenységvizsgálat).

Előzetesen rögzített bemenetek (a mérés előtt commitolva):
  config/elozetes_rogzites/ait_russellmitchell_gepfontossag_v2.yaml   (gépfontosság, D25)
  config/elozetes_rogzites/ahp_rangsorolo_itelet.yaml                  (AHP-súlyok, CR = 0,084)

Futtatás: python experiments/04_ait_russellmitchell_lepes4_gepfontossag.py
Eredmény: results/04_ait_russellmitchell_lepes4_gepfontossag.{csv,md}
Előfeltétel: az 01-es szkript gyorsítótára (data/cache/*_kockazati_reszpontszamok.pkl)
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from alertagg import ertekeles, kockazati_pontszam, kornyezet, paros_osszehasonlitas
from alertagg.egysegesito import load_cats_jsonl
from alertagg.gepnyilvantartas import Gepnyilvantartas

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "external" / "cats_datasets"
CACHE = ROOT / "data" / "cache"
ROGZ = ROOT / "config" / "elozetes_rogzites"
NYILV = ROGZ / "ait_russellmitchell_gepfontossag_v2.yaml"
AHP = ROGZ / "ahp_rangsorolo_itelet.yaml"
OUT = ROOT / "results" / "04_ait_russellmitchell_lepes4_gepfontossag"
ELLENPROBAK = 100
ERZEKENYSEG = (-0.20, 0.20)


def resz(name: str) -> pd.DataFrame:
    p = CACHE / f"{name}_kockazati_reszpontszamok.pkl"
    if not p.exists():
        raise SystemExit(f"Hiányzik: {p}. Előbb futtasd az 01-es szkriptet.")
    return pd.read_pickle(p)


def meres(nev: str, y: np.ndarray, valtozat: str, s: np.ndarray) -> dict:
    return {"adathalmaz": nev, "valtozat": valtozat, **ertekeles.summary(y, s)}


def lepes4(r: pd.Series, g: pd.Series, w: dict[str, float]) -> pd.Series:
    return w["r"] * r + w["g"] * g


def main() -> None:
    nyilv = Gepnyilvantartas.from_yaml(NYILV)
    ahp = paros_osszehasonlitas.betoltes(AHP)
    assert ahp.kovetkezetes, "Az AHP-ítéletek nem következetesek (CR >= 0,10)."
    w4 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g"])

    sorok = []
    for nev in ["ait_wazuh", "ait_suricata"]:
        alerts, labels = load_cats_jsonl(DATA / f"{nev}.jsonl")
        comp = resz(nev).loc[alerts["alert_id"]]
        y = labels.loc[alerts["alert_id"]].to_numpy()  # a címke csak itt, az értékelésnél kerül elő
        r = kockazati_pontszam.risk_score(comp, kockazati_pontszam.WEIGHTS["mean"]).to_numpy()
        g = kornyezet.kornyezeti_meroszamok(alerts, nyilv)["g"].to_numpy()

        sorok.append(meres(nev, y, "lepes1_sulyossag", comp["level"].to_numpy()))
        sorok.append(meres(nev, y, "lepes3_kockazati", r))
        valodi = meres(nev, y, "lepes4_kockazati+gep", lepes4(r, g, w4))
        sorok.append(valodi)

        for d in ERZEKENYSEG:
            wg = w4["g"] * (1 + d)
            w = {"r": w4["r"] / (w4["r"] + wg), "g": wg / (w4["r"] + wg)}
            sorok.append(meres(nev, y, f"lepes4_erzekenyseg_g{int(d * 100):+d}%", lepes4(r, g, w)))

        plac = []
        for seed in range(ELLENPROBAK):
            fok = kornyezet.osszekevert_fokozatok(nyilv, seed)
            gp = kornyezet.kornyezeti_meroszamok(alerts, nyilv, fok)["g"].to_numpy()
            plac.append(ertekeles.summary(y, lepes4(r, gp, w4)))
        plac = pd.DataFrame(plac)
        sorok.append({"adathalmaz": nev, "valtozat": f"ellenproba_atlag_{ELLENPROBAK}",
                      **plac.mean().to_dict()})
        sorok.append({"adathalmaz": nev, "valtozat": "ellenproba_aranya_ami_jobb_vagy_egyenlo",
                      "auroc": float((plac["auroc"] >= valodi["auroc"]).mean()),
                      "ap": float((plac["ap"] >= valodi["ap"]).mean()),
                      "workload_98": float((plac["workload_98"] <= valodi["workload_98"]).mean())})

    df = pd.DataFrame(sorok)
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT.with_suffix(".csv"), index=False, float_format="%.4f")

    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    fmt = df.copy()
    for c in ["auroc", "ap", "recall_top10", "workload_98"]:
        fmt[c] = fmt[c].map(lambda v: "" if pd.isna(v) else f"{v:.3f}")
    fmt["true_in_top10"] = fmt["true_in_top10"].map(lambda v: "" if pd.isna(v) else f"{v:.1f}")
    md = [
        "# 4. lépés – kockázati pontszám + gép fontossága (AIT-ADS, russellmitchell)",
        "",
        (f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · dolgozat: 4.3, "
         "6.2. táblázat, 6.3"),
        "",
        (f"Súlyok (AHP, újranormálva r és g között): r = {w4['r']:.3f}, g = {w4['g']:.3f} · "
         f"gépfontosság: `{NYILV.relative_to(ROOT)}` · ellenpróba: {ELLENPROBAK} véletlen keverés "
         "(rögzített kezdőértékek 0–99)"),
        "",
        ("Oszlopok: rangsor-pontosság (AUROC), átlagos pontosság (AP), a valódi riasztások aránya és "
         "várható száma a lista első 10%-ában, a 98%-os találathoz átnézendő listarész (kisebb = "
         "jobb). Az „ellenproba_aranya” sor azt adja meg, a keverések hány százaléka érte el vagy "
         "múlta felül a valódi gépfontossággal mért eredményt."),
        "",
        fmt.to_markdown(index=False),
        "",
    ]
    OUT.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

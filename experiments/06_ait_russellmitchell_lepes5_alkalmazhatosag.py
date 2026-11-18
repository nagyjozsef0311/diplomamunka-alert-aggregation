#!/usr/bin/env python3
"""5. lépés: a 4. lépés kiegészítése a támadás alkalmazhatóságával (AIT-ADS, russellmitchell).

Dolgozat: 4.2.3 (alkalmazhatóság), 4.3 (súlyozott összeg, újranormálás), 6.2. táblázat (5. lépés),
6.3 (mérőszámok, ellenpróba, ±20%-os érzékenység). Riasztás- és csoportszinten is kiértékel; a
csoportok a 2. lépésben kiválasztott időközzel készülnek (results/05_…, D26).

Előzetesen rögzített bemenetek (a mérés előtt commitolva):
  config/elozetes_rogzites/ait_russellmitchell_gepfontossag_v2.yaml  (D25)
  config/elozetes_rogzites/ait_russellmitchell_alkalmazhatosag.yaml  (jóváhagyva, 42036e1)
  config/elozetes_rogzites/ahp_rangsorolo_itelet.yaml                (650abd0)

Ellenpróba: a gépek szolgáltatáskészleteinek 100 véletlen keverése a gépek között.
Futtatás: python experiments/06_ait_russellmitchell_lepes5_alkalmazhatosag.py
Eredmény: results/06_ait_russellmitchell_lepes5_alkalmazhatosag.{csv,md}
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from alertagg import (
    csoportosito,
    ertekeles,
    kockazati_pontszam,
    kornyezet,
    paros_osszehasonlitas,
    serulekenysegi,
)
from alertagg.egysegesito import load_cats_jsonl
from alertagg.gepnyilvantartas import Gepnyilvantartas

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "external" / "cats_datasets"
CACHE = ROOT / "data" / "cache"
ROGZ = ROOT / "config" / "elozetes_rogzites"
LEPES2 = ROOT / "results" / "05_ait_russellmitchell_lepes2_csoportositas.csv"
OUT = ROOT / "results" / "06_ait_russellmitchell_lepes5_alkalmazhatosag"
ELLENPROBAK = 100
ERZEKENYSEG = (-0.20, 0.20)


def sor(nev, y, valtozat, s, csop=None, szab=None) -> dict:
    row = {"adathalmaz": nev, "valtozat": valtozat, **ertekeles.summary(y, s.to_numpy())}
    if csop is not None:
        gs = csoportosito.csoport_pontszam(s, csop, szab)
        row.update({f"csoport_{k}": v for k, v in ertekeles.summary(y, gs.to_numpy()).items()
                    if k in ("auroc", "ap")})
        row["csoport_terheles_98"] = ertekeles.csoport_terheles_98(y, csop.to_numpy(),
                                                                   gs.to_numpy())
    return row


def main() -> None:
    nyilv = Gepnyilvantartas.from_yaml(ROGZ / "ait_russellmitchell_gepfontossag_v2.yaml")
    nyilv.alkalmazhatosag_betoltese(ROGZ / "ait_russellmitchell_alkalmazhatosag.yaml")
    ahp = paros_osszehasonlitas.betoltes(ROGZ / "ahp_rangsorolo_itelet.yaml")
    assert ahp.kovetkezetes
    w4 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g"])
    w5 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g", "a"])
    idokoz = pd.read_csv(LEPES2).groupby("adathalmaz")["idokoz_perc"].first().to_dict()

    sorok, eloszlas = [], []
    for nev in ["ait_wazuh", "ait_suricata"]:
        alerts, labels = load_cats_jsonl(DATA / f"{nev}.jsonl")
        ids = alerts["alert_id"]
        k = kornyezet.kornyezeti_meroszamok(alerts, nyilv)
        a = serulekenysegi.alkalmazhatosag(alerts, k["erintett_gep"], nyilv)
        eloszlas.append({"adathalmaz": nev, **{f"a={v}": int((a == v).sum())
                                                 for v in (0.25, 0.5, 0.75, 1.0)}})
        comp = pd.read_pickle(CACHE / f"{nev}_kockazati_reszpontszamok.pkl").loc[ids]
        y = labels.loc[ids].to_numpy()  # a címke csak az értékelésnél
        r = kockazati_pontszam.risk_score(comp, kockazati_pontszam.WEIGHTS["mean"])
        g = k["g"]
        csop = csoportosito.csoportosit(alerts, pd.Timedelta(minutes=int(idokoz[nev])),
                                        k["erintett_gep"])
        szab = pd.Series(alerts["rule_id"].to_numpy(), index=ids)

        def s5(a_, w=w5, r=r, g=g):
            return w["r"] * r + w["g"] * g + w["a"] * a_

        sorok.append(sor(nev, y, "lepes3_kockazati", r, csop, szab))
        sorok.append(sor(nev, y, "lepes4_+gep", w4["r"] * r + w4["g"] * g, csop, szab))
        valodi = sor(nev, y, "lepes5_+alkalmazhatosag", s5(a), csop, szab)
        sorok.append(valodi)
        for d in ERZEKENYSEG:
            wa = w5["a"] * (1 + d)
            ossz = w5["r"] + w5["g"] + wa
            w = {"r": w5["r"] / ossz, "g": w5["g"] / ossz, "a": wa / ossz}
            sorok.append(sor(nev, y, f"lepes5_erzekenyseg_a{int(d * 100):+d}%", s5(a, w),
                             csop, szab))
        plac = []
        for seed in range(ELLENPROBAK):
            ap_ = serulekenysegi.alkalmazhatosag(
                alerts, k["erintett_gep"], nyilv,
                serulekenysegi.osszekevert_szolgaltatasok(nyilv, seed))
            plac.append(sor(nev, y, "p", s5(ap_), csop, szab))
        plac = pd.DataFrame(plac).drop(columns=["adathalmaz", "valtozat"])
        sorok.append({"adathalmaz": nev, "valtozat": f"ellenproba_atlag_{ELLENPROBAK}",
                      **plac.mean().to_dict()})
        sorok.append({"adathalmaz": nev, "valtozat": "ellenproba_aranya_ami_jobb_vagy_egyenlo",
                      "auroc": float((plac["auroc"] >= valodi["auroc"]).mean()),
                      "ap": float((plac["ap"] >= valodi["ap"]).mean()),
                      "workload_98": float((plac["workload_98"] <= valodi["workload_98"]).mean()),
                      "csoport_terheles_98": float(
                          (plac["csoport_terheles_98"] <= valodi["csoport_terheles_98"]).mean())})

    df = pd.DataFrame(sorok)
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT.with_suffix(".csv"), index=False, float_format="%.4f")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    md = [
        "# 5. lépés – + a támadás alkalmazhatósága (AIT-ADS, russellmitchell)",
        "",
        (f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · dolgozat: 4.2.3, "
         "4.3, 6.2. táblázat, 6.3"),
        "",
        (f"Súlyok (AHP, újranormálva): r = {w5['r']:.3f}, g = {w5['g']:.3f}, a = {w5['a']:.3f} · "
         f"csoportok időköze: {idokoz} perc · ellenpróba: a szolgáltatáskészletek "
         f"{ELLENPROBAK} véletlen keverése (kezdőértékek 0–99)"),
        "",
        "## Az alkalmazhatóság eloszlása (riasztásszám, címkék nélkül)",
        "",
        pd.DataFrame(eloszlas).to_markdown(index=False),
        "",
        "## Eredmények",
        "",
        ("workload_98: a riasztáslista, csoport_terheles_98: a csoportlista hányad részét kell "
         "átnézni a valódi riasztások 98%-áig (kisebb = jobb). Az „ellenproba_aranya” sor: a "
         "keverések hány százaléka érte el vagy múlta felül a valódi eredményt."),
        "",
        df.to_markdown(index=False, floatfmt=".3f"),
        "",
    ]
    OUT.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

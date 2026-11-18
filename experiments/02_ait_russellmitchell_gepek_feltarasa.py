#!/usr/bin/env python3
"""4. lépés-előkészítés: a gépek feltárása és a gépnyilvántartás lefedettsége (AIT-ADS, russellmitchell).

Dolgozat: 5.4 (gépnyilvántartás), 6.1 (a nyilvántartás összeállítása), 4.2.2 és D25 (az érintett gép
meghatározása). A TÁMADÁSI CÍMKÉKET SZÁNDÉKOSAN NEM HASZNÁLJA (6.3, torzítás elleni védekezés).

Futtatás: python experiments/02_ait_russellmitchell_gepek_feltarasa.py
Eredmény: results/02_ait_russellmitchell_gepek_feltarasa.md
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from alertagg import kornyezet
from alertagg.egysegesito import load_cats_jsonl
from alertagg.gepnyilvantartas import Gepnyilvantartas

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "external" / "cats_datasets"
NYILV = ROOT / "config" / "elozetes_rogzites" / "ait_russellmitchell_gepfontossag.yaml"
KI = ROOT / "results" / "02_ait_russellmitchell_gepek_feltarasa.md"


def main() -> None:
    nyilv = Gepnyilvantartas.from_yaml(NYILV)
    sorok = ["# Gépek és a gépnyilvántartás lefedettsége – AIT-ADS, russellmitchell", "",
             ("Dolgozat: 5.4, 6.1, D25 · **a támadási címkéket ez a lépés nem használja** (6.3) · "
             f"nyilvántartás: `{NYILV.relative_to(ROOT)}`"), ""]
    for nev in ["ait_wazuh", "ait_suricata"]:
        alerts, _ = load_cats_jsonl(DATA / f"{nev}.jsonl")  # a címkét eldobjuk
        k = kornyezet.kornyezeti_meroszamok(alerts, nyilv)
        sorok += [f"## {nev}", "",
                  (f"Riasztás: {len(alerts)} · azonosított érintett gép: "
                  f"{(~k['ismeretlen']).sum()} ({(~k['ismeretlen']).mean():.1%}) · "
                  f"ismeretlen (semleges 0,5): {k['ismeretlen'].sum()}"), ""]
        tab = (k.assign(fokozat=k["erintett_gep"].map(nyilv.fokozatok()))
               .groupby("erintett_gep", dropna=False)
               .agg(riasztas=("g", "size"), fokozat=("fokozat", "first"), g=("g", "first"))
               .sort_values("riasztas", ascending=False).reset_index())
        tab["erintett_gep"] = tab["erintett_gep"].fillna("(ismeretlen)")
        sorok += [tab.to_markdown(index=False, floatfmt=".2f"), ""]
        if nev == "ait_suricata":
            ism = alerts.loc[k["ismeretlen"].to_numpy()]
            parok = (pd.concat([ism["src_ip"], ism["dst_ip"]]).value_counts().head(8))
            sorok += ["Leggyakoribb IP-címek az azonosítatlan Suricata-riasztásokban:", "",
                      parok.rename_axis("ip").reset_index(name="előfordulás")
                      .to_markdown(index=False), ""]
    KI.write_text("\n".join(sorok), encoding="utf-8")
    print("\n".join(sorok))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""2. lépés: csoportosítás (AIT-ADS, russellmitchell) – az időköz kiválasztása a rögzített szabály
szerint, majd a csoportok rangsorolása. A 3. és a 4. lépést csoportszinten is kiértékeli (4.3: a
csoport pontszáma a tagjai közül a legmagasabb).

Dolgozat: 5.3 (csoportosító agent), 6.2. táblázat (2. lépés), 6.3 (a csoportok tisztasága,
tételszám-csökkenés, terhelés).
Előzetesen rögzítve: config/elozetes_rogzites/csoportosito_idokoz_valasztas.yaml (D26),
  ait_russellmitchell_gepfontossag_v2.yaml (D25), ahp_rangsorolo_itelet.yaml.
A russellmitchell a hangoló forgatókönyv: itt a 2. lépés eredménye mintán belüli.

Futtatás: python experiments/05_ait_russellmitchell_lepes2_csoportositas.py
Eredmény: results/05_ait_russellmitchell_lepes2_csoportositas.{csv,md}
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import yaml

from alertagg import (
    csoportosito,
    ertekeles,
    kockazati_pontszam,
    kornyezet,
    paros_osszehasonlitas,
)
from alertagg.egysegesito import load_cats_jsonl
from alertagg.gepnyilvantartas import Gepnyilvantartas

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "external" / "cats_datasets"
CACHE = ROOT / "data" / "cache"
ROGZ = ROOT / "config" / "elozetes_rogzites"
OUT = ROOT / "results" / "05_ait_russellmitchell_lepes2_csoportositas"


def valaszt(tisztasagok: dict[int, float], kuszob: float) -> int:
    """A rögzített szabály (D26): a legnagyobb időköz, amelynél a tisztaság >= küszöb."""
    jok = [p for p, t in tisztasagok.items() if t >= kuszob]
    return max(jok) if jok else max(tisztasagok, key=tisztasagok.get)


def main() -> None:
    szabaly = yaml.safe_load((ROGZ / "csoportosito_idokoz_valasztas.yaml").read_text("utf-8"))
    nyilv = Gepnyilvantartas.from_yaml(ROGZ / "ait_russellmitchell_gepfontossag_v2.yaml")
    ahp = paros_osszehasonlitas.betoltes(ROGZ / "ahp_rangsorolo_itelet.yaml")
    w4 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g"])

    valaszt_sorok, sorok = [], []
    for nev in ["ait_wazuh", "ait_suricata"]:
        alerts, labels = load_cats_jsonl(DATA / f"{nev}.jsonl")
        ids = alerts["alert_id"]
        y = labels.loc[ids].to_numpy()
        komp = kornyezet.kornyezeti_meroszamok(alerts, nyilv)
        comp = pd.read_pickle(CACHE / f"{nev}_kockazati_reszpontszamok.pkl").loc[ids]

        # 1) az időköz kiválasztása a rögzített szabály szerint
        tiszt = {}
        for perc in szabaly["jeloltek_perc"]:
            c = csoportosito.csoportosit(alerts, pd.Timedelta(minutes=perc), komp["erintett_gep"])
            tiszt[perc] = ertekeles.csoport_tisztasag(y, c.to_numpy())
            valaszt_sorok.append({"adathalmaz": nev, "idokoz_perc": perc, "tisztasag": tiszt[perc],
                                  "tetelszam_csokkenes": ertekeles.tetelszam_csokkenes(c)})
        perc = valaszt(tiszt, szabaly["tisztasag_kuszob"])
        csop = csoportosito.csoportosit(alerts, pd.Timedelta(minutes=perc), komp["erintett_gep"])
        szab = pd.Series(alerts["rule_id"].to_numpy(), index=ids)

        # 2) rangsorolás: riasztásszinten és csoportszinten
        r = kockazati_pontszam.risk_score(comp, kockazati_pontszam.WEIGHTS["mean"])
        s4 = w4["r"] * r + w4["g"] * komp["g"]
        lepesek = {"lepes1_sulyossag": comp["level"], "lepes3_kockazati": r,
                   "lepes4_kockazati+gep": s4}
        for nev_l, s in lepesek.items():
            gs = csoportosito.csoport_pontszam(s, csop, szab)
            for szint, pont in [("riasztas", s), ("csoport", gs)]:
                cimke = ("lepes2_csoportositas" if nev_l == "lepes1_sulyossag" and szint == "csoport"
                         else f"{nev_l}_{szint}szint")
                row = {"adathalmaz": nev, "valtozat": cimke, "idokoz_perc": perc,
                       **ertekeles.summary(y, pont.to_numpy())}
                if szint == "csoport":
                    row.update({
                        "csoportok": int(csop.nunique()),
                        "tetelszam_csokkenes": ertekeles.tetelszam_csokkenes(csop),
                        "tisztasag": ertekeles.csoport_tisztasag(y, csop.to_numpy()),
                        "csoport_terheles_98": ertekeles.csoport_terheles_98(
                            y, csop.to_numpy(), gs.to_numpy()),
                    })
                sorok.append(row)

    df = pd.DataFrame(sorok)
    vdf = pd.DataFrame(valaszt_sorok)
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT.with_suffix(".csv"), index=False, float_format="%.4f")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    md = [
        "# 2. lépés – csoportosítás (AIT-ADS, russellmitchell)",
        "",
        (f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · dolgozat: 5.3, "
         "6.2. táblázat, 6.3 · időköz-szabály: D26 · **hangoló forgatókönyv, mintán belüli**"),
        "",
        ("## Az időköz kiválasztása (tisztasági küszöb: "
        f"{szabaly['tisztasag_kuszob']})"),
        "",
        vdf.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Rangsorolás riasztás- és csoportszinten",
        "",
        ("A csoportszintű sorokban minden riasztás a csoportja pontszámát kapja (4.3). "
         "csoport_terheles_98: a csoportok hányad részét kell átnézni a valódi riasztások 98%-áig."),
        "",
        df.to_markdown(index=False, floatfmt=".3f"),
        "",
    ]
    OUT.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

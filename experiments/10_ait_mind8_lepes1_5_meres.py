#!/usr/bin/env python3
"""Az 1–5. lépés mérése mind a 8 AIT-ADS forgatókönyvön (hálózati és gépi riasztások külön).

Dolgozat: 6.2. táblázat, 6.3 (mérőszámok, ellenpróba, ±20%, hiányos nyilvántartás, tanult súlyok).
Előzetesen rögzített terv: config/elozetes_rogzites/ait_mind8_meresi_terv.yaml (D29); nyilvántartások:
ait_<forgatókönyv>_gepfontossag.yaml / _alkalmazhatosag.yaml (russellmitchell: _gepfontossag_v2);
AHP: ahp_rangsorolo_itelet.yaml; csoportosítás: 60 perc (D26). Címke: időszak-alapú (D28); a
russellmitchellen a CATS riasztásonkénti címkéjével is.

A címke csak az értékelésnél kerül elő (a pontszámok számítása után).

Futtatás: python experiments/10_ait_mind8_lepes1_5_meres.py [forgatókönyv ...]
Eredmény: results/10_ait_mind8_lepes1_5_meres.csv (forgatókönyvenkénti mérőszámok),
          results/10_ait_mind8_lepes1_5_meres_racs.csv (a tanult súlyok rácsa),
          results/10_ait_mind8_lepes1_5_meres.md (áttekintés)
A statisztikai összevetés: experiments/11_ait_mind8_statisztika.py
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from alertagg import (
    csoportosito,
    ertekeles,
    kockazati_pontszam,
    kornyezet,
    paros_osszehasonlitas,
    serulekenysegi,
)
from alertagg.egysegesito import (
    AIT_FORGATOKONYVEK,
    ait_idoszak_cimkek,
    ait_idoszak_fazis,
    ait_idoszakok,
    load_ait_wazuh_json,
)
from alertagg.gepnyilvantartas import Gepnyilvantartas

ROOT = Path(__file__).resolve().parents[1]
AIT = ROOT / "data" / "ait_ads"
CATS = ROOT / "data" / "external" / "cats_datasets"
CACHE = ROOT / "data" / "cache"
ROGZ = ROOT / "config" / "elozetes_rogzites"
NEV = "10_ait_mind8_lepes1_5_meres"
OUT = ROOT / "results" / NEV
IDOKOZ = pd.Timedelta(minutes=60)  # D26
ELLENPROBAK = 100
ERZEKENYSEG = (-0.20, 0.20)
HIANY = (0.2, 0.5)
HIANY_ISMETLES = 20
RACS_LEPES = 0.05


def nyilv_fajlok(f: str) -> tuple[Path, Path]:
    gep = ROGZ / ("ait_russellmitchell_gepfontossag_v2.yaml" if f == "russellmitchell"
                  else f"ait_{f}_gepfontossag.yaml")
    return gep, ROGZ / f"ait_{f}_alkalmazhatosag.yaml"


def nyilvantartas(gep_yaml: Path, alk_yaml: Path, kihagy: set[str] = frozenset()):
    """A nyilvántartás betöltése; ``kihagy``: a hiányos nyilvántartás vizsgálatához elhagyott gépek."""
    if not kihagy:
        n = Gepnyilvantartas.from_yaml(gep_yaml)
        n.alkalmazhatosag_betoltese(alk_yaml)
        return n
    g = yaml.safe_load(gep_yaml.read_text(encoding="utf-8"))
    a = yaml.safe_load(alk_yaml.read_text(encoding="utf-8"))
    g["gepek"] = [x for x in g["gepek"] if x["nev"] not in kihagy]
    a["szoftverkeszlet"] = {k: v for k, v in a["szoftverkeszlet"].items() if k not in kihagy}
    with tempfile.TemporaryDirectory() as d:
        pg, pa = Path(d) / "g.yaml", Path(d) / "a.yaml"
        pg.write_text(yaml.safe_dump(g, allow_unicode=True), encoding="utf-8")
        pa.write_text(yaml.safe_dump(a, allow_unicode=True), encoding="utf-8")
        n = Gepnyilvantartas.from_yaml(pg)
        n.alkalmazhatosag_betoltese(pa)
    return n


def reszpontszamok(f: str, erz: str, alerts: pd.DataFrame) -> pd.DataFrame:
    p = CACHE / f"ait_{f}_{erz}_reszpontszamok_gyors.pkl"
    if p.exists():
        return pd.read_pickle(p).loc[alerts["alert_id"]]
    comp = kockazati_pontszam.component_scores_vektoros(alerts)
    CACHE.mkdir(parents=True, exist_ok=True)
    comp.to_pickle(p)
    return comp


def cats_cimkek(alerts: pd.DataFrame, erz: str) -> np.ndarray:
    """A russellmitchell CATS riasztásonkénti címkéje az eredeti rekordazonosítón keresztül."""
    m = {}
    with open(CATS / f"ait_{erz}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            m[rec["full_alert"]["id"]] = bool(rec["metadata"]["misuse"])
    return np.array([m[r["eredeti_id"]] for r in alerts["raw"]])


def racs(lepes: float) -> list[tuple[float, float, float]]:
    k = round(1 / lepes)
    return [(i / k, j / k, (k - i - j) / k) for i in range(k + 1) for j in range(k + 1 - i)]


def meres_egy(f: str, erz: str, w4: dict, w5: dict, w_ahp: dict) -> tuple[list[dict], list[dict]]:
    t0 = time.time()
    alerts = load_ait_wazuh_json(AIT / f"{f}_wazuh.json", f, erzekelo=erz)
    ids = alerts["alert_id"]
    comp = reszpontszamok(f, erz, alerts)
    gep_yaml, alk_yaml = nyilv_fajlok(f)
    nyilv = nyilvantartas(gep_yaml, alk_yaml)
    k = kornyezet.kornyezeti_meroszamok(alerts, nyilv)
    a = serulekenysegi.alkalmazhatosag(alerts, k["erintett_gep"], nyilv)
    csop = csoportosito.csoportosit(alerts, IDOKOZ, k["erintett_gep"])
    szab = pd.Series(alerts["rule_id"].to_numpy(), index=ids)

    r = kockazati_pontszam.risk_score(comp, kockazati_pontszam.WEIGHTS["mean"])
    g = k["g"]
    s1 = comp["level"]
    s4 = w4["r"] * r + w4["g"] * g
    s5 = w5["r"] * r + w5["g"] * g + w5["a"] * a
    pont = {"lepes1": s1, "lepes3": r, "lepes4": s4, "lepes5": s5}
    csop_pont = {n: csoportosito.csoport_pontszam(s, csop, szab) for n, s in pont.items()}

    # --- csak innentől kerül elő a címke (értékelés) ---
    iv = ait_idoszakok(AIT / "labels.csv", f)
    cimkek = {"idoszak": ait_idoszak_cimkek(alerts, iv).loc[ids].to_numpy()}
    if f == "russellmitchell":
        cimkek["cats"] = cats_cimkek(alerts, erz)
    fazis = ait_idoszak_fazis(alerts, iv).loc[ids].to_numpy()

    alap = {"forgatokonyv": f, "erzekelo": erz, "riasztas": len(alerts),
            "azonositott_gep_arany": float((~k["ismeretlen"]).mean()),
            "a_semleges_arany": float((a == 0.5).mean())}
    sorok = []
    for cimke, y in cimkek.items():
        b = {**alap, "cimke": cimke, "tamadas": int(y.sum())}
        for n, s in pont.items():
            sorok.append({**b, "valtozat": n, "szint": "riasztas",
                          **ertekeles.summary(y, s.to_numpy())})
        cs = csop.to_numpy()
        csoport_kozos = {"csoportok": int(csop.nunique()),
                         "tetelszam_csokkenes": ertekeles.tetelszam_csokkenes(cs),
                         "tisztasag_ketertek": ertekeles.csoport_tisztasag(y, cs),
                         "tisztasag_fazis": ertekeles.csoport_tisztasag_fazis(fazis, cs)}
        for n, gs in csop_pont.items():
            nev = "lepes2" if n == "lepes1" else n
            sorok.append({**b, "valtozat": nev, "szint": "csoport",
                          **ertekeles.summary(y, gs.to_numpy()), **csoport_kozos,
                          "csoport_terheles_98": ertekeles.csoport_terheles_98(
                              y, cs, gs.to_numpy())})
        if cimke != "idoszak":
            continue

        # ±20% érzékenység
        for d in ERZEKENYSEG:
            wg = w4["g"] * (1 + d)
            s = (w4["r"] * r + wg * g) / (w4["r"] + wg)
            sorok.append({**b, "valtozat": f"lepes4_erzekenyseg_g{int(d * 100):+d}%",
                          "szint": "riasztas", **ertekeles.summary(y, s.to_numpy())})
            wa = w5["a"] * (1 + d)
            ossz = w5["r"] + w5["g"] + wa
            s = (w5["r"] * r + w5["g"] * g + wa * a) / ossz
            sorok.append({**b, "valtozat": f"lepes5_erzekenyseg_a{int(d * 100):+d}%",
                          "szint": "riasztas", **ertekeles.summary(y, s.to_numpy())})
        # ellenpróba: összekevert fokozatok (4.) és szolgáltatáskészletek (5.)
        for seed in range(ELLENPROBAK):
            fok = kornyezet.osszekevert_fokozatok(nyilv, seed)
            gp = k["erintett_gep"].map(lambda n, fok=fok: (fok[n] - 1) / 4 if n in fok else 0.5)
            sorok.append({**b, "valtozat": "lepes4_ellenproba", "seed": seed, "szint": "riasztas",
                          **ertekeles.summary(y, (w4["r"] * r + w4["g"] * gp.astype(float))
                                              .to_numpy())})
            ap_ = serulekenysegi.alkalmazhatosag(
                alerts, k["erintett_gep"], nyilv,
                serulekenysegi.osszekevert_szolgaltatasok(nyilv, seed))
            sorok.append({**b, "valtozat": "lepes5_ellenproba", "seed": seed, "szint": "riasztas",
                          **ertekeles.summary(y, (w5["r"] * r + w5["g"] * g + w5["a"] * ap_)
                                              .to_numpy())})
        # hiányos nyilvántartás: a gépek 20/50%-a kimarad
        gepek = sorted(nyilv.gepnevek())
        for arany in HIANY:
            for seed in range(HIANY_ISMETLES):
                rng = np.random.default_rng(seed)
                kihagy = set(rng.choice(gepek, size=round(arany * len(gepek)), replace=False))
                nh = nyilvantartas(gep_yaml, alk_yaml, kihagy)
                kh = kornyezet.kornyezeti_meroszamok(alerts, nh)
                ah = serulekenysegi.alkalmazhatosag(alerts, kh["erintett_gep"], nh)
                for n, s in (("lepes4", w4["r"] * r + w4["g"] * kh["g"]),
                             ("lepes5", w5["r"] * r + w5["g"] * kh["g"] + w5["a"] * ah)):
                    sorok.append({**b, "valtozat": f"{n}_hiany{int(arany * 100)}", "seed": seed,
                                  "szint": "riasztas", **ertekeles.summary(y, s.to_numpy())})

    # a tanult súlyok rácsa (időszak-címke), csak AP és terhelés
    y = cimkek["idoszak"]
    racs_sorok = []
    R, G, A = r.to_numpy(), g.to_numpy(), a.to_numpy()
    for wr, wg, wa in racs(RACS_LEPES):
        s = wr * R + wg * G + wa * A
        racs_sorok.append({"forgatokonyv": f, "erzekelo": erz, "w_r": wr, "w_g": wg, "w_a": wa,
                           "ap": ertekeles.average_precision(y, s),
                           "workload_98": ertekeles.workload_at_recall(y, s, 0.98)})
    print(f"[kész] {f} {erz}: {len(alerts)} riasztás, {time.time() - t0:.0f} mp", flush=True)
    return sorok, racs_sorok


def main() -> None:
    forg = sys.argv[1:] or AIT_FORGATOKONYVEK
    ahp = paros_osszehasonlitas.betoltes(ROGZ / "ahp_rangsorolo_itelet.yaml")
    assert ahp.kovetkezetes
    w4 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g"])
    w5 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g", "a"])
    OUT.parent.mkdir(exist_ok=True)
    csv, racs_csv = OUT.with_suffix(".csv"), OUT.parent / f"{NEV}_racs.csv"
    regi = pd.read_csv(csv) if csv.exists() and sys.argv[1:] else None
    regi_racs = pd.read_csv(racs_csv) if racs_csv.exists() and sys.argv[1:] else None
    sorok, racs_sorok = [], []
    for f, erz in itertools.product(forg, ["wazuh", "suricata"]):
        s, rs = meres_egy(f, erz, w4, w5, w5)
        sorok += s
        racs_sorok += rs
    df, rdf = pd.DataFrame(sorok), pd.DataFrame(racs_sorok)
    if regi is not None:  # részleges futtatás: a többi forgatókönyv sorai maradnak
        df = pd.concat([regi[~regi.forgatokonyv.isin(forg)], df], ignore_index=True)
        rdf = pd.concat([regi_racs[~regi_racs.forgatokonyv.isin(forg)], rdf], ignore_index=True)
    df.to_csv(csv, index=False, float_format="%.6f")
    rdf.to_csv(racs_csv, index=False, float_format="%.6f")

    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    fo = df[(df.cimke == "idoszak") & df.valtozat.isin(
        ["lepes1", "lepes2", "lepes3", "lepes4", "lepes5"])]
    tab = fo.pivot_table(index=["erzekelo", "forgatokonyv"], columns=["szint", "valtozat"],
                         values=["ap", "workload_98"])
    md = ["# Az 1–5. lépés a 8 AIT-ADS forgatókönyvön – forgatókönyvenkénti eredmények", "",
          (f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · terv: "
           "`config/elozetes_rogzites/ait_mind8_meresi_terv.yaml` · súlyok (AHP, újranormálva): "
           f"4. lépés r = {w4['r']:.3f}, g = {w4['g']:.3f}; 5. lépés r = {w5['r']:.3f}, "
           f"g = {w5['g']:.3f}, a = {w5['a']:.3f} · időköz: 60 perc · címke: időszak-alapú"), "",
          ("A teljes táblázat (minden mérőszám, a russellmitchell CATS-címkés változata, az "
           "ellenpróbák, a ±20% és a hiányos nyilvántartás sorai): "
           f"`results/{NEV}.csv`. A statisztikai összevetés: `results/11_ait_mind8_statisztika.md`."),
          "", "## Átlagos pontosság (AP) és a 98%-hoz átnézendő listarész", "",
          tab.round(3).to_markdown(), "",
          "## Riasztások és támadások forgatókönyvenként", "",
          fo[fo.valtozat == "lepes1"][["erzekelo", "forgatokonyv", "riasztas", "tamadas",
                                       "azonositott_gep_arany", "a_semleges_arany"]]
          .drop_duplicates().to_markdown(index=False, floatfmt=".3f"), ""]
    OUT.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

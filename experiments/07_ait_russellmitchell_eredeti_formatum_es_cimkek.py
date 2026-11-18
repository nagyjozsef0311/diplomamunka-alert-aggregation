#!/usr/bin/env python3
"""Az eredeti AIT-ADS formátum és az időszak-alapú címkék összevetése a CATS-változattal (russellmitchell).

Dolgozat: 5.3 (egységesítő agent), 6.1 (az adathalmaz és a címkék). A többi hét forgatókönyvhöz csak az
eredeti formátum és a ``labels.csv`` támadási időszakai léteznek; ez a szkript megmutatja, hogy
(1) az egységesítő az eredeti fájlból ugyanazokat a riasztásokat állítja elő, mint a CATS-változat, és
(2) mennyiben tér el az időszak-alapú címke a CATS riasztásonkénti címkéjétől.

Futtatás: python experiments/07_ait_russellmitchell_eredeti_formatum_es_cimkek.py
Eredmény: results/07_ait_russellmitchell_eredeti_formatum_es_cimkek.md (+ .csv)
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

from alertagg.egysegesito import (
    ait_idoszak_cimkek,
    ait_idoszakok,
    ait_rekord_fajtaja,
    load_ait_wazuh_json,
)

ROOT = Path(__file__).resolve().parents[1]
AIT = ROOT / "data" / "ait_ads"
CATS = ROOT / "data" / "external" / "cats_datasets"
NEV = "07_ait_russellmitchell_eredeti_formatum_es_cimkek"
KI_MD, KI_CSV = ROOT / "results" / f"{NEV}.md", ROOT / "results" / f"{NEV}.csv"


def _cats_rekordok() -> dict[str, dict]:
    out = {}
    for fn in ("ait_wazuh.jsonl", "ait_suricata.jsonl"):
        with open(CATS / fn, encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                out[rec["full_alert"]["id"]] = rec
    return out


def main() -> None:
    path = AIT / "russellmitchell_wazuh.json"
    # 1. az eredeti fájl összetétele
    fajtak, helyek = Counter(), Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            fajtak[ait_rekord_fajtaja(rec) or "fast.log-másolat (kihagyva)"] += 1
            helyek[rec.get("location")] += 1
    df = load_ait_wazuh_json(path)
    cats = _cats_rekordok()
    sajat = {r["eredeti_id"]: r for r in df["raw"]}
    hianyzik, tobblet = set(cats) - set(sajat), set(sajat) - set(cats)
    elteres = Counter()
    peldak = []
    for i, c in cats.items():
        if i not in sajat:
            continue
        a, b = sajat[i]["features"], c["features"]
        for k in set(a) | set(b):
            if a.get(k) != b.get(k):
                elteres[k] += 1
                peldak.append((i, k, a.get(k), b.get(k), c["full_alert"].get("location")))

    # 2. címkék: időszak-alapú vs. a CATS riasztásonkénti címkéje
    iv = ait_idoszakok(AIT / "labels.csv", "russellmitchell")
    df["idoszak"] = ait_idoszak_cimkek(df, iv).to_numpy()
    df["cats"] = df["raw"].map(lambda r: bool(cats[r["eredeti_id"]]["metadata"]["misuse"]))
    df["fazis"] = None
    for row in iv.itertuples(index=False):
        m = (df["timestamp"] >= row.start) & (df["timestamp"] <= row.end) & df["fazis"].isna()
        df.loc[m, "fazis"] = row.attack

    sorok = [
        "# Az eredeti AIT-ADS formátum és az időszak-alapú címkék – russellmitchell", "",
        ("Dolgozat: 5.3, 6.1 · forrás: Zenodo 8263181 (`russellmitchell_wazuh.json`, `labels.csv`) és a "
        "CATS-változat (`ait_wazuh.jsonl`, `ait_suricata.jsonl`, commit 628cf48a)"), "",
        "## 1. Az eredeti fájl összetétele", "",
        pd.Series(fajtak).rename_axis("rekordfajta").reset_index(name="rekord").to_markdown(index=False),
        "",
        pd.Series(helyek).sort_values(ascending=False).rename_axis("napló (location)")
        .reset_index(name="rekord").to_markdown(index=False), "",
        ("A Suricata minden riasztása kétszer szerepel: szerkezetten (`eve.json`) és a Wazuh saját "
        "szabályával feldolgozott szöveges másolatként (`fast.log`). A másolatokat kihagyjuk."), "",
        "## 2. Egyezés a CATS-változattal", "",
        (f"- Egységesített riasztás: {len(df)} (Suricata {int((df.sensor == 'suricata').sum())}, "
        f"Wazuh {int((df.sensor == 'wazuh').sum())}); CATS-változat: {len(cats)}."),
        (f"- Csak a CATS-ban: {len(hianyzik)}; csak az eredetiből: {len(tobblet)} "
        "(az illesztés kulcsa a Wazuh-kezelő rekordazonosítója)."),
        f"- Mezőeltérés: {dict(elteres) or 'nincs'}.", "",
    ]
    if peldak:
        sorok += ["| rekord | mező | sajat | CATS | napló |", "| --- | --- | --- | --- | --- |"]
        sorok += [f"| {i} | {k} | {a} | {b} | {loc} |" for i, k, a, b, loc in peldak[:10]]
        sorok += ["", ("Az eltérés oka: a CATS a Horde-webmail néhány riasztását kézi, időpont- és "
                  "IP-alapú szabállyal más géphez rendeli; az egységesítő forgatókönyvtől független "
                  "szabályt használ (a naplósor gépneve, az Apache-napló helye, a Wazuh-ügynök "
                  "IP-címe)."), ""]

    sorok += ["## 3. Időszak-alapú címke kontra a CATS riasztásonkénti címkéje", "",
              ("Időszak-alapú címke: támadás, ha a riasztás ideje a `labels.csv` valamelyik "
              "támadási időszakába esik (zárt időszak). A CATS címkéje az AIT-LDSv2 eseményszintű "
              "címkéiből jön (csak a russellmitchellre van ilyen)."), ""]
    tab = []
    for s, g in df.groupby("sensor"):
        ct = pd.crosstab(g["cats"], g["idoszak"])
        tp = int(ct.loc[True, True]) if True in ct.index and True in ct.columns else 0
        fp = int(ct.loc[False, True]) if True in ct.columns else 0
        fn = int(ct.loc[True, False]) if True in ct.index and False in ct.columns else 0
        tab.append({"érzékelő": s, "riasztás": len(g), "CATS: támadás": int(g.cats.sum()),
                    "időszak: támadás": int(g.idoszak.sum()), "mindkettő": tp,
                    "csak időszak (zaj a támadás alatt)": fp, "csak CATS (kimaradna)": fn,
                    "időszak-címke pontossága": tp / (tp + fp) if tp + fp else float("nan"),
                    "időszak-címke teljessége": tp / (tp + fn) if tp + fn else float("nan")})
    tab = pd.DataFrame(tab)
    tab.to_csv(KI_CSV, index=False)
    sorok += [tab.to_markdown(index=False, floatfmt=".3f"), "",
              "### Az időszak-címke többlete fázisonként és szabályonként", ""]
    zaj = df[df.idoszak & ~df.cats]
    sorok += [zaj.groupby(["sensor", "fazis"]).size().rename("riasztás").reset_index()
              .to_markdown(index=False), "",
              zaj.groupby(["sensor", "hostname", "rule_name"], dropna=False).size()
              .sort_values(ascending=False).head(12).rename("riasztás").reset_index()
              .to_markdown(index=False), ""]
    KI_MD.write_text("\n".join(sorok), encoding="utf-8")
    print("\n".join(sorok))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""A 8 forgatókönyves mérés statisztikai kiértékelése (Wilcoxon-próba, hatásnagyság, tanult súlyok).

Dolgozat: 6.3 (páros, egyoldali Wilcoxon-próba a 8 forgatókönyvön, érzékelőnként; hatásnagyság;
ellenpróba; ±20%; hiányos nyilvántartás; tanult súlyok egy-kihagyással). A terv:
config/elozetes_rogzites/ait_mind8_meresi_terv.yaml (D29). Bemenet: results/10_…csv és _racs.csv.

Futtatás: python experiments/11_ait_mind8_statisztika.py
Eredmény: results/11_ait_mind8_statisztika.md (+ _wilcoxon.csv, _tanult_sulyok.csv)
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from alertagg import ertekeles, paros_osszehasonlitas

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
BE = RES / "10_ait_mind8_lepes1_5_meres.csv"
BE_RACS = RES / "10_ait_mind8_lepes1_5_meres_racs.csv"
NEV = "11_ait_mind8_statisztika"
ROGZ = ROOT / "config" / "elozetes_rogzites"

METRIKAK = {"auroc": True, "ap": True, "recall_top10": True, "workload_98": False}
OSSZEVETESEK = [("lepes3", "lepes1"), ("lepes4", "lepes3"), ("lepes5", "lepes4"),
                ("lepes5", "lepes3")]
NEVEK = {"lepes1": "1. súlyosság", "lepes2": "2. csoportosítás", "lepes3": "3. kockázati",
         "lepes4": "4. + gép fontossága", "lepes5": "5. + alkalmazhatóság"}


def fmt_p(p: float) -> str:
    return f"{p:.4f}" if p >= 0.0001 else f"{p:.1e}"


def wilcoxon_tabla(fo: pd.DataFrame) -> pd.DataFrame:
    sorok = []
    for erz, d in fo[fo.szint == "riasztas"].groupby("erzekelo"):
        piv = d.pivot(index="forgatokonyv", columns="valtozat")
        for m, nagyobb in METRIKAK.items():
            blokk = []
            for uj, regi in OSSZEVETESEK:
                res = ertekeles.paros_wilcoxon(piv[(m, uj)], piv[(m, regi)], nagyobb)
                blokk.append({"erzekelo": erz, "meroszam": m, "osszevetes": f"{uj} > {regi}",
                              **res})
            adj = ertekeles.holm([b["p"] for b in blokk])
            for b, a in zip(blokk, adj, strict=True):
                b["p_holm"] = float(a)
            sorok += blokk
    # 2. lépés: csoportlista kontra riasztáslista (az átnézendő tételek aránya)
    for erz, d in fo.groupby("erzekelo"):
        cs = d[(d.szint == "csoport") & (d.valtozat == "lepes2")].set_index("forgatokonyv")
        r1 = d[(d.szint == "riasztas") & (d.valtozat == "lepes1")].set_index("forgatokonyv")
        res = ertekeles.paros_wilcoxon(cs["csoport_terheles_98"], r1.loc[cs.index, "workload_98"],
                                       nagyobb_jobb=False)
        sorok.append({"erzekelo": erz, "meroszam": "terheles_98 (csoport vs. riasztás)",
                      "osszevetes": "lepes2 > lepes1", **res, "p_holm": res["p"]})
    return pd.DataFrame(sorok)


def atlag_tabla(fo: pd.DataFrame) -> str:
    out = []
    for (erz, szint), d in fo.groupby(["erzekelo", "szint"]):
        cols = ["auroc", "ap", "recall_top10", "workload_98"]
        if szint == "csoport":
            cols += ["csoport_terheles_98"]
        g = d.groupby("valtozat")[cols].agg(["mean", "std"])
        sor = g.apply(lambda r, cols=cols: pd.Series(
            {c: f"{r[(c, 'mean')]:.3f} ± {r[(c, 'std')]:.3f}" for c in cols}), axis=1)
        sor.index = [NEVEK.get(i, i) for i in sor.index]
        out += [f"### {erz} – {'riasztásszint' if szint == 'riasztas' else 'csoportszint'}", "",
                sor.to_markdown(), ""]
    return "\n".join(out)


def tanult_sulyok(racs: pd.DataFrame, w5: dict) -> pd.DataFrame:
    sorok = []
    for erz, d in racs.groupby("erzekelo"):
        forg = sorted(d.forgatokonyv.unique())
        if len(forg) < 2:
            continue
        for ki in forg:
            tan = d[d.forgatokonyv != ki].groupby(["w_r", "w_g", "w_a"])["ap"].mean().reset_index()
            best = tan["ap"].max()
            jel = tan[np.isclose(tan["ap"], best, rtol=0, atol=1e-12)].copy()
            jel["tav"] = ((jel.w_r - w5["r"]) ** 2 + (jel.w_g - w5["g"]) ** 2
                          + (jel.w_a - w5["a"]) ** 2)
            w = jel.sort_values("tav").iloc[0]
            teszt = d[d.forgatokonyv == ki]
            t = teszt[np.isclose(teszt.w_r, w.w_r) & np.isclose(teszt.w_g, w.w_g)
                      & np.isclose(teszt.w_a, w.w_a)].iloc[0]
            # az AHP-súlyok a rácson kívül esnek: a mérés a 10-es szkript fő soraiból jön
            sorok.append({"erzekelo": erz, "kihagyott": ki, "w_r": w.w_r, "w_g": w.w_g,
                          "w_a": w.w_a, "tanulo_ap": w.ap, "ap_tanult": t.ap,
                          "workload_98_tanult": t.workload_98})
    return pd.DataFrame(sorok)


def main() -> None:
    df = pd.read_csv(BE)
    racs = pd.read_csv(BE_RACS)
    ahp = paros_osszehasonlitas.betoltes(ROGZ / "ahp_rangsorolo_itelet.yaml")
    w5 = paros_osszehasonlitas.renormalt(ahp.sulyok, ["r", "g", "a"])
    fo = df[(df.cimke == "idoszak") & df.valtozat.isin(list(NEVEK))]
    n_forg = fo.forgatokonyv.nunique()

    wt = wilcoxon_tabla(fo)
    wt.to_csv(RES / f"{NEV}_wilcoxon.csv", index=False, float_format="%.6f")
    wt_md = wt.assign(p=wt.p.map(fmt_p), p_holm=wt.p_holm.map(fmt_p))[
        ["erzekelo", "meroszam", "osszevetes", "javult", "romlott", "kulonbseg_median",
         "kulonbseg_atlag", "rang_biszerialis", "p", "p_holm"]]

    # ellenpróba: a keverések hány %-a éri el a valódi eredményt
    ell = []
    for (f, erz), d in df[df.cimke == "idoszak"].groupby(["forgatokonyv", "erzekelo"]):
        for lep in ("lepes4", "lepes5"):
            val = d[(d.valtozat == lep) & (d.szint == "riasztas")].iloc[0]
            p = d[d.valtozat == f"{lep}_ellenproba"]
            ell.append({"erzekelo": erz, "forgatokonyv": f, "lepes": lep,
                        "AP_valodi": val.ap, "AP_kevert_atlag": p.ap.mean(),
                        "kevert_AP_>=_valodi": (p.ap >= val.ap).mean(),
                        "kevert_terheles_<=_valodi": (p.workload_98 <= val.workload_98).mean()})
    ell = pd.DataFrame(ell)

    # ±20% és hiányos nyilvántartás: az AP változása a teljes beállításhoz képest
    erz_sorok = []
    for (f, erz), d in df[df.cimke == "idoszak"].groupby(["forgatokonyv", "erzekelo"]):
        alap = d[d.szint == "riasztas"].set_index("valtozat")
        for v in d.valtozat.unique():
            for lep in ("lepes4", "lepes5"):
                if v.startswith((f"{lep}_erzekenyseg", f"{lep}_hiany")):
                    x = d[d.valtozat == v]
                    erz_sorok.append({"erzekelo": erz, "forgatokonyv": f, "valtozat": v,
                                      "dAP": x.ap.mean() - alap.loc[lep, "ap"],
                                      "dTerheles": x.workload_98.mean()
                                      - alap.loc[lep, "workload_98"],
                                      "AP_vs_lepes3": x.ap.mean() - alap.loc["lepes3", "ap"]})
    erz_df = pd.DataFrame(erz_sorok)
    erz_osszes = erz_df.groupby(["erzekelo", "valtozat"])[["dAP", "dTerheles", "AP_vs_lepes3"]] \
        .agg(["mean", "min", "max"]).round(4)

    # tanult súlyok
    ts = tanult_sulyok(racs, w5)
    if ts.empty:
        ts = pd.DataFrame(columns=["erzekelo", "kihagyott", "w_r", "w_g", "w_a", "tanulo_ap",
                                   "ap_tanult", "workload_98_tanult"])
    ahp_sor = fo[(fo.szint == "riasztas") & (fo.valtozat == "lepes5")].set_index(
        ["erzekelo", "forgatokonyv"])
    ts["ap_ahp"] = [ahp_sor.loc[(e, f), "ap"] for e, f in zip(ts.erzekelo, ts.kihagyott,
                                                               strict=True)]
    ts["workload_98_ahp"] = [ahp_sor.loc[(e, f), "workload_98"]
                             for e, f in zip(ts.erzekelo, ts.kihagyott, strict=True)]
    ts.to_csv(RES / f"{NEV}_tanult_sulyok.csv", index=False, float_format="%.6f")
    ts_teszt = []
    for erz, d in ts.groupby("erzekelo"):
        for m in ("ap", "workload_98"):
            dd = d[f"{m}_tanult"] - d[f"{m}_ahp"]
            p = float(wilcoxon(dd[dd != 0], alternative="two-sided").pvalue) \
                if (dd != 0).sum() else 1.0
            ts_teszt.append({"erzekelo": erz, "meroszam": m,
                             "atlag_tanult": d[f"{m}_tanult"].mean(),
                             "atlag_ahp": d[f"{m}_ahp"].mean(),
                             "tanult_jobb": int(((dd > 0) if m == "ap" else (dd < 0)).sum()),
                             "p_ketoldali": p})

    # címke-érzékenység (russellmitchell)
    rm = df[(df.forgatokonyv == "russellmitchell") & df.valtozat.isin(list(NEVEK))]
    rm_tab = rm.pivot_table(index=["erzekelo", "szint", "valtozat"], columns="cimke",
                            values=["ap", "workload_98"]).round(3)

    # csoportszint
    cs = fo[(fo.szint == "csoport") & (fo.valtozat == "lepes2")][
        ["erzekelo", "forgatokonyv", "riasztas", "csoportok", "tetelszam_csokkenes",
         "tisztasag_fazis", "tisztasag_ketertek"]]

    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    md = [
        "# A 8 forgatókönyves mérés statisztikai kiértékelése (AIT-ADS, 1–5. lépés)", "",
        (f"Készült: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · kód: `{commit}` · forgatókönyvek: "
         f"{n_forg} · terv: `config/elozetes_rogzites/ait_mind8_meresi_terv.yaml` (D29) · címke: "
         "időszak-alapú (D28) · bemenet: `results/10_ait_mind8_lepes1_5_meres.csv`"), "",
        "## 1. Átlag ± szórás a forgatókönyvek között", "",
        ("auroc: rangsor-pontosság; ap: átlagos pontosság; recall_top10: a valódi riasztások "
         "aránya a lista első 10%-ában; workload_98 (csoportszinten csoport_terheles_98): a "
         "lista hányad részét kell átnézni a valódi riasztások 98%-áig (kisebb = jobb)."), "",
        atlag_tabla(fo),
        "## 2. Páros, egyoldali Wilcoxon-próba (H1: az újabb lépés jobb)", "",
        ("javult/romlott: a forgatókönyvek száma; a különbség a „jobb” irányba előjelezve "
         "(terhelésnél a csökkenés pozitív); rang_biszerialis: párosított rang-biszeriális "
         "korreláció (+1: minden forgatókönyvön javult); p_holm: Holm-korrekció érzékelőnként és "
         "mérőszámonként a négy riasztásszintű összevetésre. 8 párnál a legkisebb elérhető "
         "p-érték 0,0039."), "",
        wt_md.to_markdown(index=False, floatfmt=".4f"), "",
        "## 3. Ellenpróba (100 keverés forgatókönyvenként)", "",
        ("kevert_AP_>=_valodi: a keverések hányad része érte el vagy múlta felül a valódi "
         "nyilvántartással mért AP-t (kicsi = a javulás a környezeti információnak köszönhető)."),
        "", ell.to_markdown(index=False, floatfmt=".3f"), "",
        "## 4. ±20%-os súlyváltozás és hiányos nyilvántartás", "",
        ("dAP, dTerheles: a változás a lépés teljes beállításához képest (átlag, legkisebb, "
         "legnagyobb a 8 forgatókönyvön); AP_vs_lepes3: a 3. lépéshez képest. A hiányos "
         "nyilvántartásnál 20 véletlen ismétlés átlaga."), "",
        erz_osszes.to_markdown(), "",
        "## 5. Tanult súlyok egy-kihagyással kontra AHP-súlyok (5. lépés: r, g, a)", "",
        (f"AHP (újranormálva): r = {w5['r']:.3f}, g = {w5['g']:.3f}, a = {w5['a']:.3f}. A tanult "
         "súlyok a 7 tanító forgatókönyv átlagos AP-jét maximalizálják a 0,05-ös rácson; a mérés "
         "a kihagyott forgatókönyvön."), "",
        ts.to_markdown(index=False, floatfmt=".3f"), "",
        pd.DataFrame(ts_teszt).to_markdown(index=False, floatfmt=".4f"), "",
        "## 6. Címke-érzékenység: russellmitchell, időszak-alapú kontra CATS-címke", "",
        rm_tab.to_markdown(), "",
        "## 7. Csoportosítás (2. lépés, 60 perc)", "",
        ("tisztasag_fazis: a csoportokban a leggyakoribb támadási lépéshez (vagy a normál "
         "forgalomhoz) tartozó riasztások aránya; a russellmitchell a hangoló forgatókönyv."), "",
        cs.to_markdown(index=False, floatfmt=".4f"), "",
    ]
    (RES / f"{NEV}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

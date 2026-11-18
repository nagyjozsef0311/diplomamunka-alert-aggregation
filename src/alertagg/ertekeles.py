"""Értékelési mérőszámok (6. fejezet, 6.3): a rangsor és a terhelés mérése.

Minden függvény egy pontszám-sorozatot (nagyobb = előrébb a listában) és a hozzá tartozó, igaz/hamis
címkét kap. Holtversenynél a sorrend a pontszámok átlagos helyezésén alapul, így az eredmény nem függ
az adatok eredeti sorrendjétől.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def auroc(y_true, scores) -> float:
    """Rangsor-pontosság: annak valószínűsége, hogy egy valódi riasztás egy téves elé kerül."""
    return float(roc_auc_score(np.asarray(y_true, bool), np.asarray(scores, float)))


def average_precision(y_true, scores) -> float:
    """Átlagos pontosság: erősebben bünteti a lista elején álló téves riasztásokat."""
    return float(average_precision_score(np.asarray(y_true, bool), np.asarray(scores, float)))


def _expected_true_in_top(y_true: np.ndarray, scores: np.ndarray, k: int) -> float:
    """A lista első k helyén lévő valódi riasztások várható száma (holtversenyek arányos osztásával)."""
    order = np.argsort(-scores, kind="stable")
    s, y = scores[order], y_true[order]
    if k <= 0:
        return 0.0
    cutoff = s[k - 1]
    above = s > cutoff
    tie = s == cutoff
    n_above = int(above.sum())
    slots = k - n_above
    tie_true = y[tie].sum()
    return float(y[above].sum() + slots * tie_true / tie.sum())


def recall_at_fraction(y_true, scores, fraction: float = 0.10) -> float:
    """A valódi riasztások hányad része kerül a lista első ``fraction`` részébe (várható érték)."""
    y = np.asarray(y_true, bool)
    s = np.asarray(scores, float)
    k = int(np.ceil(fraction * len(s)))
    total = y.sum()
    return _expected_true_in_top(y, s, k) / total if total else float("nan")


def true_in_top_fraction(y_true, scores, fraction: float = 0.10) -> float:
    """A lista első ``fraction`` részébe kerülő valódi riasztások várható száma."""
    y = np.asarray(y_true, bool)
    s = np.asarray(scores, float)
    return _expected_true_in_top(y, s, int(np.ceil(fraction * len(s))))


def workload_at_recall(y_true, scores, recall: float = 0.98) -> float:
    """Terhelés: a lista mekkora részét kell átnézni, hogy a valódi riasztások ``recall`` része meglegyen.

    Holtversenynél pesszimista: a teljes azonos pontszámú blokkot átnézettnek tekinti.
    A terheléscsökkentés ennek kiegészítője: ``1 - workload_at_recall``.
    """
    y = np.asarray(y_true, bool)
    s = np.asarray(scores, float)
    total = y.sum()
    if not total:
        return float("nan")
    need = int(np.ceil(recall * total))
    order = np.argsort(-s, kind="stable")
    ss, yy = s[order], y[order]
    cum = np.cumsum(yy)
    idx = int(np.searchsorted(cum, need))  # az első hely, ahol megvan a szükséges találat
    last_tied = int(np.searchsorted(-ss, -ss[idx], side="right"))  # a holtverseny-blokk vége
    return last_tied / len(s)


def summary(y_true, scores) -> dict[str, float]:
    """Az összes rangsor-mérőszám egy szótárban."""
    return {
        "auroc": auroc(y_true, scores),
        "ap": average_precision(y_true, scores),
        "recall_top10": recall_at_fraction(y_true, scores, 0.10),
        "true_in_top10": true_in_top_fraction(y_true, scores, 0.10),
        "workload_98": workload_at_recall(y_true, scores, 0.98),
    }


# --- csoportszintű mérőszámok (6.3: a csoportosítás minősége és a tételszám csökkenése) ----------

def csoport_tisztasag(y_true, csoport) -> float:
    """A csoportok riasztásszámmal súlyozott tisztasága: a csoportokban a többségi címkéhez tartozó
    riasztások aránya az összes riasztáshoz képest (1 = minden csoport egynemű)."""
    import pandas as pd

    df = pd.DataFrame({"y": np.asarray(y_true, bool), "c": np.asarray(csoport)})
    tobbseg = df.groupby("c")["y"].agg(lambda s: max(s.sum(), len(s) - s.sum()))
    return float(tobbseg.sum() / len(df))


def tetelszam_csokkenes(csoport) -> float:
    """A riasztásszám csökkenése: 1 - csoportok száma / riasztások száma."""
    c = np.asarray(csoport)
    return float(1 - len(np.unique(c)) / len(c))


def csoport_terheles_98(y_true, csoport, csoport_pontszam, recall: float = 0.98) -> float:
    """A csoportok hányad részét kell (pontszám szerinti sorrendben) átnézni, hogy a valódi
    riasztások ``recall`` része meglegyen. Holtversenynél pesszimista, mint a ``workload_at_recall``."""
    import pandas as pd

    df = pd.DataFrame({"y": np.asarray(y_true, bool), "c": np.asarray(csoport),
                       "s": np.asarray(csoport_pontszam, float)})
    g = df.groupby("c").agg(y=("y", "sum"), s=("s", "max"))
    total = g["y"].sum()
    if not total:
        return float("nan")
    g = g.sort_values("s", ascending=False, kind="stable")
    cum = g["y"].cumsum().to_numpy()
    idx = int(np.searchsorted(cum, int(np.ceil(recall * total))))
    s = g["s"].to_numpy()
    last_tied = int(np.searchsorted(-s, -s[idx], side="right"))
    return last_tied / len(g)


def csoport_tisztasag_fazis(fazis, csoport) -> float:
    """A csoportok tisztasága a támadási lépés szerint (6.3: egy csoportba csak egy támadási lépés
    riasztásai kerüljenek): a csoportokban a leggyakoribb lépéshez (vagy a „normál”-hoz) tartozó
    riasztások aránya, riasztásszámmal súlyozva."""
    import pandas as pd

    df = pd.DataFrame({"f": np.asarray(fazis, dtype=object), "c": np.asarray(csoport)})
    tobbseg = df.groupby(["c", "f"]).size().groupby(level=0).max()
    return float(tobbseg.sum() / len(df))


# --- statisztika a forgatókönyvek között (6.3) ---------------------------------------------------

def paros_wilcoxon(uj, regi, nagyobb_jobb: bool = True) -> dict[str, float]:
    """Páros, egyoldali Wilcoxon-próba (H1: az új jobb) és hatásnagyság.

    A nulla különbségű párok kimaradnak (Wilcoxon eredeti eljárása). Hatásnagyság: a különbségek
    mediánja és átlaga (a „jobb” irányba előjelezve), valamint a párosított rang-biszeriális
    korreláció (+1: minden pár az új javára, −1: mind a régi javára).
    """
    from scipy.stats import rankdata, wilcoxon

    uj, regi = np.asarray(uj, float), np.asarray(regi, float)
    d = (uj - regi) if nagyobb_jobb else (regi - uj)
    nz = d[d != 0]
    out = {"n": len(d), "n_nem_nulla": len(nz), "javult": int((d > 0).sum()),
           "romlott": int((d < 0).sum()), "kulonbseg_median": float(np.median(d)),
           "kulonbseg_atlag": float(np.mean(d))}
    if len(nz) == 0:
        return {**out, "W_plusz": 0.0, "p": 1.0, "rang_biszerialis": 0.0}
    r = rankdata(np.abs(nz))
    wp, wm = float(r[nz > 0].sum()), float(r[nz < 0].sum())
    res = wilcoxon(nz, alternative="greater", zero_method="wilcox")
    return {**out, "W_plusz": wp, "p": float(res.pvalue), "rang_biszerialis": (wp - wm) / (wp + wm)}


def holm(p) -> np.ndarray:
    """Holm–Bonferroni-korrekció (a korrigált p-értékek, eredeti sorrendben)."""
    p = np.asarray(p, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (m - k) * p[i]))
        adj[i] = run
    return adj

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

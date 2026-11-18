"""Páros összehasonlítás (AHP, Saaty 1990): a rangsoroló súlyainak meghatározása (4. fejezet, 4.3).

A szakértő minden szempontpárról megadja, melyik fontosabb és mennyivel (1–9 skála, 4.4. táblázat).
A súlyok a páros összehasonlítási mátrix fő sajátvektorából adódnak; az ítéletek akkor fogadhatók el,
ha a következetességi arány (CR) 0,1 alatt marad:

    CI = (λmax - n) / (n - 1),    CR = CI / RI

ahol RI a véletlenszerűen kitöltött mátrixok átlagos következetlensége (Saaty-féle táblázat).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

# Saaty véletlen indexe a mátrix méretének függvényében (n = 1 … 10)
RANDOM_INDEX = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45,
                10: 1.49}
CR_HATAR = 0.10


@dataclass(frozen=True)
class AhpEredmeny:
    szempontok: tuple[str, ...]
    sulyok: dict[str, float]
    lambda_max: float
    ci: float
    cr: float

    @property
    def kovetkezetes(self) -> bool:
        return self.cr < CR_HATAR


def matrix_itiletekbol(szempontok: list[str], itelet: dict[tuple[str, str], float]) -> np.ndarray:
    """Reciprok mátrix a páronkénti ítéletekből. ``itelet[(a, b)] = 3`` jelentése: az ``a``
    valamivel fontosabb, mint a ``b``; ``1/3``: a ``b`` valamivel fontosabb, mint az ``a``."""
    n = len(szempontok)
    idx = {s: i for i, s in enumerate(szempontok)}
    a = np.ones((n, n))
    for (x, y), v in itelet.items():
        if v <= 0:
            raise ValueError(f"Az ítélet pozitív szám kell legyen: {x}–{y}: {v}")
        a[idx[x], idx[y]] = v
        a[idx[y], idx[x]] = 1.0 / v
    hianyzo = [(szempontok[i], szempontok[j]) for i in range(n) for j in range(i + 1, n)
               if (szempontok[i], szempontok[j]) not in itelet
               and (szempontok[j], szempontok[i]) not in itelet]
    if hianyzo:
        raise ValueError(f"Hiányzó ítéletek: {hianyzo}")
    return a


def sulyok(szempontok: list[str], matrix: np.ndarray) -> AhpEredmeny:
    """Súlyok a fő sajátvektorból, következetességi mutatókkal."""
    n = len(szempontok)
    ertekek, vektorok = np.linalg.eig(matrix)
    k = int(np.argmax(ertekek.real))
    lam = float(ertekek[k].real)
    w = np.abs(vektorok[:, k].real)
    w = w / w.sum()
    ci = (lam - n) / (n - 1) if n > 2 else 0.0
    ri = RANDOM_INDEX[n]
    cr = ci / ri if ri else 0.0
    return AhpEredmeny(tuple(szempontok), dict(zip(szempontok, map(float, w), strict=True)),
                       lam, ci, cr)


def betoltes(path: str | Path) -> AhpEredmeny:
    """Az ítéletek betöltése YAML-ból (``szempontok`` lista + ``iteletek`` lista) és kiértékelés."""
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    szempontok = list(cfg["szempontok"])
    itelet = {}
    for t in cfg["iteletek"]:
        if t.get("ertek") is None:
            raise ValueError(f"Kitöltetlen ítélet: {t['a']} – {t['b']}")
        itelet[(t["a"], t["b"])] = float(eval_tort(t["ertek"]))
    return sulyok(szempontok, matrix_itiletekbol(szempontok, itelet))


def eval_tort(v) -> float:
    """``3``, ``"1/3"`` vagy ``0.333`` alakú érték számmá alakítása."""
    if isinstance(v, str) and "/" in v:
        szamlalo, nevezo = v.split("/")
        return float(szamlalo) / float(nevezo)
    return float(v)


def renormalt(sulyok_: dict[str, float], bent: list[str]) -> dict[str, float]:
    """A lépésenkénti értékelésnél a kimaradó szempontok súlyát elhagyjuk, a többit 1-re normáljuk
    (4.3, utolsó előtti bekezdés)."""
    s = sum(sulyok_[k] for k in bent)
    return {k: sulyok_[k] / s for k in bent}

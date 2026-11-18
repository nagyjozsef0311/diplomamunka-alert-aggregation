"""A kockázatalapú riasztás-pontozás (Uetz és mtsai. 2026, CATS) öt részpontszáma.

Ez a 3. értékelési lépés, az összehasonlítási alap. A pontszámot nem írjuk újra: a CATS saját moduljait
hívjuk meg, hogy az eredmény a közölttel azonos legyen. A CATS kódjának nincs licence, ezért nem kerül
a tárolóba; a ``scripts/download_cats.py`` tölti le rögzített commitra a ``data/external/cats/``
mappába, és ez a modul onnan importálja (az elérési út a ``CATS_BACKEND`` környezeti változóval
felülírható).

A beállítás a cikk alapértelmezése (2. táblázat): középre igazított, háromszög alakú ablak; a
halmozódás egyperces, a változatosság egyórás, a ritkaság és a szabálytalanság egynapos ablakkal; a
gépet a gépi riasztásoknál a gépnév, a hálózatiaknál a forrás-IP-cím azonosítja.
"""

from __future__ import annotations

import os
import sys
from importlib import import_module
from pathlib import Path

import numpy as np
import pandas as pd

MODULES = ["level", "accumulation", "variety", "rarity", "aperiodicity"]

# Az öt részpontszám súlya: a nyolc adathalmaz átlaga, illetve az AIT-ADS egy-kihagyásos súlyai
# (Uetz és mtsai. 2026, 5. táblázat). Sorrend: MODULES.
WEIGHTS = {
    "mean": (0.12, 0.24, 0.44, 0.10, 0.10),
    "loo_wazuh": (0.09, 0.24, 0.44, 0.11, 0.12),
    "loo_suricata": (0.12, 0.27, 0.41, 0.09, 0.11),
}

_DEFAULT_BACKEND = Path(__file__).resolve().parents[2] / "data" / "external" / "cats" / "backend"


def _cats():
    backend = Path(os.environ.get("CATS_BACKEND", _DEFAULT_BACKEND))
    if not (backend / "modules").is_dir():
        raise FileNotFoundError(
            f"A CATS nem található itt: {backend}. Futtasd: python scripts/download_cats.py"
        )
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))
    return import_module("processing.data_models")


def module_args(sensor: str) -> dict[str, tuple[str, list]]:
    """A CATS-modulok fájlneve és paraméterei a cikk alapértelmezése szerint."""
    group = "Hostname" if sensor == "wazuh" else "Source IP"
    return {
        "level": ("level_score", []),
        "accumulation": ("accumulated_risk", [group, "Triangle", "One minute", "Past + Future"]),
        "variety": ("variety", [group, "Triangle", "One hour", "Past + Future"]),
        "rarity": ("rarity", ["Alert Type", "Triangle", "One day", "Past + Future"]),
        "aperiodicity": ("aperiodicity", ["Alert Type", "One day", "Past + Future", 5]),
    }


def _entries(dm, alerts: pd.DataFrame):
    """A közös formájú riasztásokból CATS-bejegyzések (címke nélkül!)."""
    out = []
    for row in alerts.itertuples(index=False):
        feat = dict(row.raw["features"])
        meta = {
            "alert_id": row.alert_id,
            "alert_source": row.raw["metadata"]["alert_source"],
            "risk_score": 0.5,
            "raw_risk_scores": [],
        }
        out.append(dm.DatasetEntry(full_alert={}, features=feat, metadata=meta))
    return out


def component_scores(alerts: pd.DataFrame, sensor: str | None = None) -> pd.DataFrame:
    """Az öt részpontszám riasztásonként (0–1), ``alert_id`` indexszel.

    :param alerts: az egységesítő kimenete, egyetlen érzékelő riasztásai, időrendben
    :param sensor: ``"wazuh"`` vagy ``"suricata"``; alapból az ``alerts.sensor`` oszlopból
    """
    sensor = sensor or alerts["sensor"].iloc[0]
    if alerts["sensor"].nunique() != 1:
        raise ValueError("Egyszerre csak egy érzékelő riasztásai pontozhatók (a cikk is így mér).")
    if not alerts["timestamp"].is_monotonic_increasing:
        raise ValueError("A riasztásoknak időrendben kell lenniük.")
    dm = _cats()
    result = {}
    for name, (file_name, args) in module_args(sensor).items():
        dataset = dm.Dataset(data=_entries(dm, alerts), file_names=[])
        mod = import_module(f"modules.{file_name}")
        dataset, logs = mod.process(dataset, args, weight=1.0,
                                    averaging_method=dm.AveragingMethod.ARITHMETIC_MEAN)
        errors = [m for m in _flatten(logs) if "Error" in m or "Exception" in m]
        if errors:
            raise RuntimeError(f"CATS-hiba a(z) {name} modulban: {errors[:3]}")
        result[name] = [e.metadata["raw_risk_scores"][0] for e in dataset.data]
    return pd.DataFrame(result, index=pd.Index(alerts["alert_id"], name="alert_id"))[MODULES]


def _flatten(logs) -> list[str]:
    out = []
    for item in logs:
        out.extend(_flatten(item) if isinstance(item, list) else [str(item)])
    return out


def risk_score(components: pd.DataFrame, weights=WEIGHTS["mean"]) -> pd.Series:
    """A részpontszámok súlyozott számtani közepe (a súlyokat 1-re normáljuk)."""
    w = np.asarray(weights, float)
    w = w / w.sum()
    return pd.Series(components[MODULES].to_numpy() @ w, index=components.index, name="r")

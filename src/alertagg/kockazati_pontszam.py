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


# ---------------------------------------------------------------------------------------------
# Vektoros (gyors) számítás – ugyanaz a matematika, mint a CATS moduljaiban
# ---------------------------------------------------------------------------------------------
#
# A CATS minden riasztásnál végigjárja az időablak összes riasztását. A nagy AIT-ADS
# forgatókönyvekben (450–500 ezer gépi riasztás, órás csúcsokkal) ez négyzetes futásidőt jelent.
# Az alábbi függvények ugyanazokat a képleteket számolják (``modules/src/*.py`` és a modulok
# ``process`` függvényei, CATS 628cf48a) rendezett időbélyegeken, prefixösszegekkel és bináris
# kereséssel. Az egyezést a russellmitchell teljes adatán a CATS saját kódjával ellenőrizzük
# (``tests/test_kockazati_pontszam.py`` és ``experiments/09_…``).

_EULER_GAMMA = 0.5772156649015329
_MIN_REL_WINDOW_LENGTH = 1 / (2 * 365 * 24 * 60)
_ABLAK_US = {"accumulation": 60 * 10**6, "variety": 3600 * 10**6, "rarity": 86400 * 10**6,
             "aperiodicity": 86400 * 10**6}


def _ido_us(alerts: pd.DataFrame) -> np.ndarray:
    """Időbélyegek egész mikroszekundumban (a CATS ezredmásodperces időbélyegéből)."""
    return alerts["timestamp"].dt.tz_convert("UTC").astype("datetime64[us, UTC]").astype("int64") \
        .to_numpy()


def _csoportok(kulcs: pd.Series) -> list[np.ndarray]:
    """A nem hiányzó kulcsú riasztások indexei csoportonként, időrendben."""
    k = kulcs.to_numpy(dtype=object)
    ok = np.array([v is not None and not (isinstance(v, float) and np.isnan(v)) for v in k])
    idx = np.flatnonzero(ok)
    if len(idx) == 0:
        return []
    codes, _ = pd.factorize(pd.Series(k[idx]))
    order = np.argsort(codes, kind="stable")
    bounds = np.flatnonzero(np.diff(codes[order])) + 1
    return np.split(idx[order], bounds)


def _ablak_hatarok(t: np.ndarray, h: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """[t-h, t] és (t, t+h] határindexei egy rendezett csoporton belül."""
    lo = np.searchsorted(t, t - h, side="left")
    mid = np.searchsorted(t, t, side="right")
    hi = np.searchsorted(t, t + h, side="right")
    return lo, mid, hi


def _haromszog_osszeg(t: np.ndarray, h: int) -> np.ndarray:
    """Σ_j (1 - |t_i - t_j| / h) az ablakban (|t_i - t_j| <= h)."""
    lo, mid, hi = _ablak_hatarok(t, h)
    tf = (t - t[0]).astype(np.float64)
    cs = np.concatenate([[0.0], np.cumsum(tf)])
    n_l, n_r = mid - lo, hi - mid
    s_l, s_r = cs[mid] - cs[lo], cs[hi] - cs[mid]
    return n_l - (n_l * tf - s_l) / h + n_r - (s_r - n_r * tf) / h


def _atlagos_tavolsag(t: np.ndarray, w: int, ds0: int, ds1: int) -> np.ndarray:
    """calculate_average_distance_for_triangle (include_future=True)."""
    ws, we = t - w / 2, t + w / 2
    ol = (t - np.maximum(ws, ds0)) / (w * 0.5)
    orr = (np.minimum(we, ds1) - t) / (w * 0.5)
    return ((1 - 0.5 * ol) * ol + (1 - 0.5 * orr) * orr) / (ol + orr)


def _tobblet_vart(t: np.ndarray, w: int, ds0: int, ds1: int, n: int) -> np.ndarray:
    """additional_alerts_expected (include_future=True)."""
    eff = np.minimum(t + w / 2, ds1) - np.maximum(t - w / 2, ds0)
    return eff / (ds1 - ds0) * (n - 1)


def _halmozodas_ritkasag(t_all: np.ndarray, csoportok: list[np.ndarray], w: int,
                         ritkasag: bool) -> np.ndarray:
    n = len(t_all)
    ds0, ds1 = t_all[0], t_all[-1]
    out = np.full(n, 0.5)
    ng = len(csoportok)
    for idx in csoportok:
        t = t_all[idx]
        s = _haromszog_osszeg(t, w // 2)
        avg = _atlagos_tavolsag(t, w, ds0, ds1)
        add = _tobblet_vart(t, w, ds0, ds1, n) / ng
        if ritkasag:
            norm = 1 + avg * add
            with np.errstate(divide="ignore", invalid="ignore"):
                sc = np.where(norm == 1, 1.0, (norm - 1) / (s + norm - 2))
        else:
            sc = 1 - 0.5 ** (s / (1 + avg * add))
        out[idx] = np.clip(sc, 0.0, 1.0)
    return out


def _valtozatossag(t_all: np.ndarray, rule: np.ndarray, csoportok: list[np.ndarray],
                   w: int) -> np.ndarray:
    n = len(t_all)
    ds0, ds1 = t_all[0], t_all[-1]
    out = np.full(n, 0.5)
    tipusok, tip_kod = np.unique(rule, return_inverse=True)
    darab = np.bincount(tip_kod, minlength=len(tipusok)).astype(np.float64)
    ng = len(csoportok)
    lam = darab / ng                                  # típusonként várt darab csoportonként
    h = w // 2
    for idx in csoportok:
        t, kod = t_all[idx], tip_kod[idx]
        # Σ_típus (1 - a típus legközelebbi riasztásának relatív távolsága), ha az ablakban van
        s = np.zeros(len(idx))
        for k in np.unique(kod):
            tk = t[kod == k]
            pos = np.searchsorted(tk, t)
            bal = np.where(pos > 0, t - tk[np.maximum(pos - 1, 0)], np.iinfo(np.int64).max)
            jobb = np.where(pos < len(tk), tk[np.minimum(pos, len(tk) - 1)] - t,
                            np.iinfo(np.int64).max)
            d = np.minimum(bal, jobb)
            s += np.where(d <= h, 1 - np.minimum(d, h) / h, 0.0)
        eff = np.minimum(t + h, ds1) - np.maximum(t - h, ds0)
        rel = eff / (ds1 - ds0)
        # várt további változatosság és várt relatív távolság (modules/src/variety.py)
        L = np.outer(rel, lam)                        # (riasztás × típus)
        p = 1 - np.exp(-L)
        exp_add = p.sum(axis=1) - p[np.arange(len(idx)), kod]
        with np.errstate(divide="ignore", invalid="ignore"):
            cev = np.where(L < _MIN_REL_WINDOW_LENGTH, 0.5 * rel[:, None],
                           (1 - np.exp(-L) * (1 + L)) / (lam[None, :] * p))
            erd = np.where(rel == 0, 0.0, (p * cev).sum(axis=1) / p.sum(axis=1) / rel)
        sc = 1 - 0.5 ** (s / (1 + exp_add * (1 - erd)))
        out[idx] = np.clip(sc, 0.0, 1.0)
    return out


def _aperiodicitas_egy(ev_us: np.ndarray, sulyok: np.ndarray, small_n: float) -> float:
    """modules/src/aperiodicity.py aperiodicity_score, súlyozott (azonos időpontú) eseményekkel."""
    db = sulyok.sum()
    if db <= 2:
        return 1.0
    off = (ev_us - ev_us[0]) / 1e6
    span = off[-1]
    if span <= 0 or span <= 1:
        return 1.0
    n_bins = int(np.ceil(span))
    b = np.minimum(off.astype(np.int64), n_bins - 1)
    c = np.bincount(b, weights=sulyok, minlength=n_bins).astype(np.float64)
    c -= c.mean()
    power = np.abs(np.fft.rfft(c)) ** 2
    power = power[1:]
    if len(power) == 0:
        return 1.0
    am = np.mean(power)
    if am <= 0:
        return 1.0
    sf = np.exp(np.mean(np.log(np.maximum(power, np.finfo(np.float64).tiny)))) / am
    sf = float(np.clip(sf / np.exp(-_EULER_GAMMA), 0.0, 1.0))
    conf = 1.0 - np.exp(-db / small_n)
    return sf * conf + (1.0 - conf)


def _aperiodicitas(t_all: np.ndarray, csoportok: list[np.ndarray], w: int,
                   small_n: float = 5) -> np.ndarray:
    n = len(t_all)
    nyers = np.full(n, np.nan)
    h = w // 2
    for idx in csoportok:
        t = t_all[idx]
        u, inv, cnt = np.unique(t, return_inverse=True, return_counts=True)
        lo = np.searchsorted(u, u - h, side="left")
        hi = np.searchsorted(u, u + h, side="right")
        cache: dict[tuple[int, int], float] = {}
        su = np.empty(len(u))
        for i in range(len(u)):
            key = (lo[i], hi[i])
            if key not in cache:
                cache[key] = _aperiodicitas_egy(u[lo[i]:hi[i]], cnt[lo[i]:hi[i]], small_n)
            su[i] = cache[key]
        nyers[idx] = su[inv]
    ertekelt = ~np.isnan(nyers)
    mean = nyers[ertekelt].mean()
    out = np.full(n, 0.5)
    if mean in (0, 1):
        out[ertekelt] = nyers[ertekelt]
    else:
        out[ertekelt] = nyers[ertekelt] ** (np.log(0.5) / np.log(mean))
    return out


def component_scores_vektoros(alerts: pd.DataFrame, sensor: str | None = None) -> pd.DataFrame:
    """Az öt részpontszám, ugyanazzal a matematikával, mint :func:`component_scores`, gyorsan."""
    sensor = sensor or alerts["sensor"].iloc[0]
    if alerts["sensor"].nunique() != 1:
        raise ValueError("Egyszerre csak egy érzékelő riasztásai pontozhatók (a cikk is így mér).")
    if not alerts["timestamp"].is_monotonic_increasing:
        raise ValueError("A riasztásoknak időrendben kell lenniük.")
    t = _ido_us(alerts)
    gep = alerts["hostname"] if sensor == "wazuh" else alerts["src_ip"]
    gep_cs = _csoportok(gep.reset_index(drop=True))
    rule = alerts["rule_id"].astype(str).to_numpy()
    tip_cs = _csoportok(pd.Series(rule, dtype=object))
    res = {
        "level": alerts["severity"].to_numpy(dtype=float),
        "accumulation": _halmozodas_ritkasag(t, gep_cs, _ABLAK_US["accumulation"], False),
        "variety": _valtozatossag(t, rule, gep_cs, _ABLAK_US["variety"]),
        "rarity": _halmozodas_ritkasag(t, tip_cs, _ABLAK_US["rarity"], True),
        "aperiodicity": _aperiodicitas(t, tip_cs, _ABLAK_US["aperiodicity"]),
    }
    return pd.DataFrame(res, index=pd.Index(alerts["alert_id"], name="alert_id"))[MODULES]

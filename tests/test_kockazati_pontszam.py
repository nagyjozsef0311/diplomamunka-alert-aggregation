from pathlib import Path

import pandas as pd
import pytest

from alertagg import kockazati_pontszam
from alertagg.egysegesito import normalize_records

CATS = Path(__file__).resolve().parents[1] / "data" / "external" / "cats" / "backend"
needs_cats = pytest.mark.skipif(not (CATS / "modules").is_dir(),
                                reason="a CATS nincs letöltve (scripts/download_cats.py)")


def test_weights_sum_to_one():
    for w in kockazati_pontszam.WEIGHTS.values():
        assert sum(w) == pytest.approx(1.0)


def test_risk_score_is_weighted_mean():
    comp = pd.DataFrame([[1, 0, 0, 0, 0], [0, 0, 1, 0, 0]], columns=kockazati_pontszam.MODULES,
                        index=pd.Index(["a", "b"], name="alert_id"))
    r = kockazati_pontszam.risk_score(comp, (1, 0, 3, 0, 0))
    assert r["a"] == pytest.approx(0.25) and r["b"] == pytest.approx(0.75)


@needs_cats
def test_components_on_small_synthetic_set():
    recs = []
    for i in range(30):
        recs.append({"full_alert": {}, "features": {
            "timestamp": f"2022-01-21T00:{i:02d}:00.000Z", "rule_id": str(100 + i % 3),
            "rule_name": "x", "rule_level": "5", "hostname": "web" if i % 2 else "mail"},
            "metadata": {"alert_source": "ait_wazuh", "alert_id": f"a{i}", "misuse": i > 25}})
    df, _ = normalize_records(recs)
    comp = kockazati_pontszam.component_scores(df)
    assert list(comp.columns) == kockazati_pontszam.MODULES
    assert len(comp) == 30
    assert comp.to_numpy().min() >= 0 and comp.to_numpy().max() <= 1


def test_vektoros_szamitas_egyezik_a_cats_kodjaval():
    """A gyors számítás riasztásonként ugyanazt adja, mint a CATS eredeti kódja (egy részhalmazon)."""
    from pathlib import Path

    import pytest

    from alertagg import kockazati_pontszam as kp
    from alertagg.egysegesito import load_cats_jsonl

    p = Path(__file__).resolve().parents[1] / "data/external/cats_datasets/ait_suricata.jsonl"
    try:
        kp._cats()
    except FileNotFoundError:
        pytest.skip("a CATS nincs letöltve")
    if not p.exists():
        pytest.skip("a CATS-adat nincs letöltve")
    alerts, _ = load_cats_jsonl(p)
    alerts = alerts.iloc[:3000].reset_index(drop=True)
    ref = kp.component_scores(alerts)
    gyors = kp.component_scores_vektoros(alerts)
    assert (gyors - ref.to_numpy()).abs().max().max() < 1e-9

from pathlib import Path

import pandas as pd
import pytest

from alertagg import rba
from alertagg.normalizer import normalize_records

CATS = Path(__file__).resolve().parents[1] / "data" / "external" / "cats" / "backend"
needs_cats = pytest.mark.skipif(not (CATS / "modules").is_dir(),
                                reason="a CATS nincs letöltve (scripts/download_cats.py)")


def test_weights_sum_to_one():
    for w in rba.WEIGHTS.values():
        assert sum(w) == pytest.approx(1.0)


def test_risk_score_is_weighted_mean():
    comp = pd.DataFrame([[1, 0, 0, 0, 0], [0, 0, 1, 0, 0]], columns=rba.MODULES,
                        index=pd.Index(["a", "b"], name="alert_id"))
    r = rba.risk_score(comp, (1, 0, 3, 0, 0))
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
    comp = rba.component_scores(df)
    assert list(comp.columns) == rba.MODULES
    assert len(comp) == 30
    assert comp.to_numpy().min() >= 0 and comp.to_numpy().max() <= 1

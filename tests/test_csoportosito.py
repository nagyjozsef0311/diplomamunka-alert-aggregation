import pandas as pd
import pytest

from alertagg import csoportosito, ertekeles


def _alerts():
    t = pd.to_datetime(["2022-01-01 00:00", "2022-01-01 00:01", "2022-01-01 00:30",
                        "2022-01-01 00:00", "2022-01-01 00:02"], utc=True)
    return pd.DataFrame({"alert_id": list("abcde"), "timestamp": t,
                         "hostname": ["h1", "h1", "h1", None, None],
                         "src_ip": [None, None, None, "10.0.0.1", "10.0.0.1"]})


def test_grouping_by_host_and_gap():
    c = csoportosito.csoportosit(_alerts(), pd.Timedelta(minutes=5))
    assert c["a"] == c["b"] != c["c"]          # 29 perces szünet: új csoport
    assert c["d"] == c["e"] != c["a"]          # gépnév hiányában a forrás-IP
    c60 = csoportosito.csoportosit(_alerts(), pd.Timedelta(minutes=60))
    assert c60["a"] == c60["c"]


def test_group_score_max_and_tiebreak():
    s = pd.Series([0.2, 0.9, 0.5], index=list("abc"))
    c = pd.Series([1, 1, 2], index=list("abc"))
    r = pd.Series(["x", "y", "x"], index=list("abc"))
    gs = csoportosito.csoport_pontszam(s, c, r)
    assert gs["a"] == pytest.approx(0.9, abs=1e-5) and gs["a"] > gs["b"] - 1e-9
    assert gs["c"] == pytest.approx(0.5, abs=1e-5)


def test_group_metrics():
    y = [1, 1, 0, 0, 1]
    c = [1, 1, 1, 2, 3]
    assert ertekeles.csoport_tisztasag(y, c) == pytest.approx(4 / 5)
    assert ertekeles.tetelszam_csokkenes(c) == pytest.approx(1 - 3 / 5)
    # csoportok pontszám szerint: 3 (1 valódi), 1 (2 valódi), 2 -> 3/3 valódi a 2. csoportnál
    assert ertekeles.csoport_terheles_98(y, c, [0.5, 0.5, 0.5, 0.1, 0.9]) == pytest.approx(2 / 3)

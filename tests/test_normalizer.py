import pandas as pd

from alertagg.normalizer import COLUMNS, normalize_records, severity_score


def _rec(i, ts, source, level, misuse, **feat):
    f = {"timestamp": ts, "rule_id": "100", "rule_name": "teszt", "rule_level": level}
    f.update(feat)
    return {"full_alert": {}, "features": f,
            "metadata": {"alert_source": source, "alert_id": f"a{i}", "misuse": misuse}}


def test_severity_mapping_matches_cats():
    assert severity_score("suricata", "1") == 0.75
    assert severity_score("suricata", "3") == 0.25
    assert severity_score("suricata", "7") == 0.25
    assert severity_score("wazuh", 15) == 1.0
    assert severity_score("wazuh", 0) == 0.0


def test_common_form_order_and_label_separation():
    recs = [
        _rec(1, "2022-01-21T00:00:02.000Z", "ait_wazuh", "5", True, hostname="web"),
        _rec(2, "2022-01-21T00:00:01.000Z", "ait_suricata", "2", False,
             source_ip="10.0.0.1", rule_name="ET EXPLOIT CVE-2020-24186 wpDiscuz"),
    ]
    df, lab = normalize_records(recs)
    assert list(df.columns) == COLUMNS
    # a címke nem része a riasztások táblájának (adatszivárgás elleni védelem)
    assert "label" not in df.columns and "misuse" not in df.columns
    # időrend
    assert list(df["alert_id"]) == ["a2", "a1"]
    assert list(lab.index) == ["a2", "a1"] and list(lab) == [False, True]
    assert isinstance(df["timestamp"].dtype, pd.DatetimeTZDtype)
    # CVE-hivatkozás kinyerése és a hiányzó gépnév
    assert df.loc[0, "cves"] == ["CVE-2020-24186"]
    assert df.loc[0, "hostname"] is None
    assert df.loc[1, "sensor"] == "wazuh" and df.loc[1, "severity"] == 5 / 15

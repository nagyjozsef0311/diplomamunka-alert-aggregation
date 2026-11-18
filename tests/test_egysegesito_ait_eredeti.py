"""Az egységesítő eredeti AIT-ADS formátumra írt része."""

import json
from pathlib import Path

import pandas as pd
import pytest

from alertagg.egysegesito import (
    COLUMNS,
    ait_cats_formara,
    ait_gepnev_szabalyok,
    ait_idoszak_cimkek,
    load_ait_wazuh_json,
)

ROOT = Path(__file__).resolve().parents[1]
EREDETI = ROOT / "data/ait_ads/russellmitchell_wazuh.json"
CATS = ROOT / "data/external/cats_datasets"


def _wazuh(i, ip, host=None, loc="/var/log/syslog", **extra):
    rec = {"@timestamp": "2022-01-24T03:59:30.123456Z", "id": f"1.{i}", "location": loc,
           "agent": {"ip": ip}, "rule": {"id": "5710", "level": 5, "description": "sshd",
                                         "groups": ["sshd"]}}
    if host:
        rec["predecoder"] = {"hostname": host}
    rec.update(extra)
    return rec


def test_fast_log_kimarad_es_gepnev_szabalyok():
    eve = {"@timestamp": "2022-01-24T03:59:30.123456Z", "id": "2.1",
           "location": "/var/log/suricata/eve.json", "agent": {"ip": "10.0.0.9"},
           "data": {"src_ip": "1.2.3.4", "dest_ip": "10.0.0.5", "src_port": "4444",
                    "dest_port": "80", "proto": "TCP",
                    "alert": {"signature_id": 2001, "signature": "ET X", "severity": "2",
                              "category": "Web Attack"}}}
    fast = dict(eve, id="2.2", location="/var/log/suricata/fast.log")
    recs = [_wazuh(1, "10.0.0.1", host="mail"), _wazuh(2, "10.0.0.1", loc="/var/log/audit/audit.log"),
            _wazuh(3, "10.0.0.2", loc="/var/log/apache2/intranet-access.log"),
            _wazuh(4, "10.0.0.3", loc="/var/log/apache2/proxy-access-access.log"), eve, fast]
    ug = ait_gepnev_szabalyok(recs)
    assert ug == {"10.0.0.1": "mail"}  # a Suricata-ügynök nem számít
    out = [ait_cats_formara(r, ug, "teszt") for r in recs]
    assert out[5] is None  # fast.log-másolat
    assert [o["features"].get("hostname") for o in out[:5]] == [
        "mail", "mail", "intranet-server", "proxy-server", None]
    s = out[4]
    assert s["metadata"] == {"alert_source": "ait_suricata", "alert_id": "teszt:2.1"}
    assert s["features"]["rule_id"] == "2001" and s["features"]["destination_port"] == 80
    assert s["features"]["timestamp"] == "2022-01-24T03:59:30.123Z"
    assert "misuse" not in s["metadata"]  # címke nélkül


def test_idoszak_cimke_zart_intervallum():
    df = pd.DataFrame({"alert_id": ["a", "b", "c"], "timestamp": pd.to_datetime(
        ["2022-01-24T03:00:59Z", "2022-01-24T03:01:00Z", "2022-01-24T03:05:00Z"], utc=True)})
    iv = pd.DataFrame({"attack": ["scan"],
                       "start": pd.to_datetime(["2022-01-24T03:01:00Z"], utc=True),
                       "end": pd.to_datetime(["2022-01-24T03:05:00Z"], utc=True)})
    lab = ait_idoszak_cimkek(df, iv)
    assert list(lab.index) == ["a", "b", "c"] and list(lab) == [False, True, True]


@pytest.mark.skipif(not (EREDETI.exists() and (CATS / "ait_wazuh.jsonl").exists()),
                    reason="az AIT-ADS vagy a CATS-adat nincs letöltve")
def test_russellmitchell_eredetibol_ugyanazok_a_riasztasok_mint_a_cats_valtozatbol():
    df = load_ait_wazuh_json(EREDETI)
    assert list(df.columns) == COLUMNS
    sajat = {r["eredeti_id"]: r for r in df["raw"]}
    cats = {}
    for fn in ("ait_wazuh.jsonl", "ait_suricata.jsonl"):
        with open(CATS / fn, encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                cats[rec["full_alert"]["id"]] = rec
    # ugyanaz a riasztáshalmaz (a fast.log-másolatok nélkül)
    assert set(sajat) == set(cats)
    assert (df["sensor"] == "suricata").sum() == 9186 and (df["sensor"] == "wazuh").sum() == 23116
    elteres = []
    for i, c in cats.items():
        assert sajat[i]["metadata"]["alert_source"] == c["metadata"]["alert_source"]
        a, b = sajat[i]["features"], c["features"]
        elteres += [(i, k) for k in set(a) | set(b) if a.get(k) != b.get(k)]
    # egyetlen ismert eltérés: 3 Horde-riasztás gépneve (a CATS kézi, időpont-alapú szabálya)
    assert len(elteres) == 3 and {k for _, k in elteres} == {"hostname"}

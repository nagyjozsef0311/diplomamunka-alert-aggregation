from pathlib import Path

import pandas as pd
import pytest

from alertagg import kornyezet
from alertagg.gepnyilvantartas import Gepnyilvantartas

YAML = """
kozos_ip_szabaly: max
gepek:
  - {nev: web,   ip: [10.0.0.1], fokozat: 5}
  - {nev: proxy, ip: [10.0.0.1], fokozat: 3}
  - {nev: ws,    ip: [10.0.0.9], fokozat: 2, megfigyeltseg: {gepi: false, halozati: true}}
"""


@pytest.fixture
def nyilv(tmp_path: Path) -> Gepnyilvantartas:
    p = tmp_path / "gepek.yaml"
    p.write_text(YAML, encoding="utf-8")
    return Gepnyilvantartas.from_yaml(p)


def test_lookup_and_shared_ip(nyilv):
    assert nyilv.gep_ip_alapjan("10.0.0.1") == "web"  # közös IP: a magasabb fokozat
    assert nyilv.gep_ip_alapjan("8.8.8.8") is None
    assert nyilv.fokozat("ws") == 2
    assert nyilv.lefedettseg("ws") == 0.5 and nyilv.lefedettseg("web") == 1.0


def test_context_metrics(nyilv):
    alerts = pd.DataFrame({
        "alert_id": ["w1", "s1", "s2", "s3"],
        "sensor": ["wazuh", "suricata", "suricata", "suricata"],
        "hostname": ["ws", None, None, None],
        "src_ip": [None, "8.8.8.8", "10.0.0.9", "1.1.1.1"],
        "dst_ip": [None, "10.0.0.1", "8.8.4.4", "2.2.2.2"],
    })
    k = kornyezet.kornyezeti_meroszamok(alerts, nyilv)
    assert list(k["erintett_gep"]) == ["ws", "web", "ws", None]   # cél előre, aztán forrás
    assert list(k["g"]) == [0.25, 1.0, 0.25, 0.5]                 # ismeretlen: semleges 0,5
    assert list(k["m"]) == [0.5, 0.0, 0.5, 0.5]
    assert list(k["ismeretlen"]) == [False, False, False, True]


def test_placebo_is_permutation(nyilv):
    p = kornyezet.osszekevert_fokozatok(nyilv, seed=1)
    assert sorted(p.values()) == sorted(nyilv.fokozatok().values())
    assert p == kornyezet.osszekevert_fokozatok(nyilv, seed=1)  # megismételhető


def test_wazuh_gepnev_nelkul_az_ugynok_ip_alapjan(nyilv):
    alerts = pd.DataFrame({
        "alert_id": ["a", "b", "c", "d"],
        "sensor": ["wazuh"] * 4,
        "hostname": [None, None, "ws", None],
        "src_ip": [None] * 4, "dst_ip": [None] * 4,
        "raw": [{"ugynok_ip": "10.0.0.9"},                      # eredeti AIT-formátum
                {"full_alert": {"agent": {"ip": "10.0.0.1"}}},  # CATS-formátum
                {"ugynok_ip": "10.0.0.1"},                      # a gépnév elsőbbséget kap
                {"ugynok_ip": "8.8.8.8"}],                      # ismeretlen ügynök
    })
    assert list(kornyezet.erintett_gep(alerts, nyilv)) == ["ws", "web", "ws", None]

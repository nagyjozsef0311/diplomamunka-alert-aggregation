from pathlib import Path

import pandas as pd
import pytest

from alertagg import serulekenysegi
from alertagg.gepnyilvantartas import Gepnyilvantartas

GEPEK = "gepek:\n  - {nev: web, ip: [10.0.0.1], fokozat: 5}\n  - {nev: db, ip: [10.0.0.2], fokozat: 4}\n"
ALK = """
allapot: jovahagyva
szoftverkeszlet:
  web: [linux, web]
szabalyok:
  wazuh: {"1": web, "2": imap, "3": altalanos}
"""


@pytest.fixture
def nyilv(tmp_path: Path) -> Gepnyilvantartas:
    (tmp_path / "g.yaml").write_text(GEPEK, encoding="utf-8")
    (tmp_path / "a.yaml").write_text(ALK, encoding="utf-8")
    n = Gepnyilvantartas.from_yaml(tmp_path / "g.yaml")
    n.alkalmazhatosag_betoltese(tmp_path / "a.yaml")
    return n


def test_values(nyilv):
    alerts = pd.DataFrame({"alert_id": list("abcdef"), "sensor": ["wazuh"] * 6,
                           "rule_id": ["1", "2", "3", "9", "1", "1"],
                           "cves": [[]] * 6})
    eg = pd.Series(["web", "web", "web", "web", "db", None], index=list("abcdef"))
    a = serulekenysegi.alkalmazhatosag(alerts, eg, nyilv)
    # web-szabály webgépen; imap-szabály webgépen; általános; ismeretlen szabály;
    # ismeretlen szoftverkészletű gép; ismeretlen gép
    assert list(a) == [0.75, 0.25, 0.5, 0.5, 0.5, 0.5]


def test_requires_approval(tmp_path):
    (tmp_path / "g.yaml").write_text(GEPEK, encoding="utf-8")
    (tmp_path / "a.yaml").write_text(ALK.replace("jovahagyva", "javaslat"), encoding="utf-8")
    n = Gepnyilvantartas.from_yaml(tmp_path / "g.yaml")
    with pytest.raises(ValueError):
        n.alkalmazhatosag_betoltese(tmp_path / "a.yaml")


def test_placebo_permutes_sets(nyilv):
    p = serulekenysegi.osszekevert_szolgaltatasok(nyilv, 0)
    assert sorted(map(str, p.values())) == sorted(map(str, [nyilv.szolgaltatasok("web"),
                                                            nyilv.szolgaltatasok("db")]))

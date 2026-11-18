"""Egységesítő agent: a Suricata- és a Wazuh-riasztásokat közös formára hozza.

A közös forma (5. fejezet, 5.2. táblázat) egy pandas-tábla, riasztásonként egy sorral. A támadás-címke
**nem** része a táblának: külön sorozatként adjuk vissza, hogy a rangsoroló semmilyen úton ne lássa
(adatszivárgás elleni védelem, D23). A tábla oszlopai:

==============  ===========================================================================
alert_id        a riasztás azonosítója (a forrásból)
timestamp       a riasztás ideje (UTC, pandas Timestamp)
sensor          ``"suricata"`` vagy ``"wazuh"``
rule_id         a szabály azonosítója (szöveg)
rule_name       a szabály neve
severity_raw    az eredeti súlyossági érték (szöveg)
severity        0–1 közé alakított súlyosság (a CATS szabályszint-leképezésével egyezően)
src_ip, dst_ip  a hálózati kapcsolat két végpontja (hiányozhat)
hostname        az érintett gép neve (a Suricatánál hiányzik, a gépnyilvántartásból pótolható)
user            az érintett felhasználó (ha van)
cves            a szabály által hivatkozott CVE-azonosítók listája (lehet üres)
techniques      a szabályhoz rendelt MITRE ATT&CK-technikák listája (lehet üres)
raw             az eredeti rekord, változatlanul
==============  ===========================================================================
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

COLUMNS = [
    "alert_id", "timestamp", "sensor", "rule_id", "rule_name", "severity_raw", "severity",
    "src_ip", "dst_ip", "hostname", "user", "cves", "techniques", "raw",
]

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.IGNORECASE)

# A Suricata prioritása: 1 a legsúlyosabb. A 3-nál nagyobb értékeket 3-ként kezeljük (mint a CATS).
_SURICATA_SEVERITY = {"1": 0.75, "2": 0.5, "3": 0.25}


def severity_score(sensor: str, level: str | int) -> float:
    """Az eredeti súlyossági szintet 0 és 1 közé alakítja.

    A leképezés megegyezik a CATS szabályszint-moduljáéval (Uetz és mtsai. 2026), hogy a 3. lépés
    összehasonlítási alapja pontosan visszamérhető legyen.
    """
    level = str(level)
    if sensor == "suricata":
        if 3 < int(level) < 256:
            level = "3"
        return _SURICATA_SEVERITY[level]
    if sensor == "wazuh":
        return int(level) / 15.0
    raise ValueError(f"Ismeretlen érzékelő: {sensor}")


def _find_cves(*texts: object) -> list[str]:
    found: set[str] = set()
    for t in texts:
        if t:
            found.update(m.upper() for m in CVE_RE.findall(json.dumps(t) if not isinstance(t, str)
                                                            else t))
    return sorted(found)


def _sensor_of(alert_source: str) -> str:
    if "suricata" in alert_source:
        return "suricata"
    if "wazuh" in alert_source:
        return "wazuh"
    raise ValueError(f"Ismeretlen riasztásforrás: {alert_source}")


def normalize_cats_record(rec: dict) -> tuple[dict, bool]:
    """Egy CATS-formátumú (JSON Lines) rekordot közös formára hoz; visszaadja a címkét is."""
    feat, meta, full = rec["features"], rec["metadata"], rec.get("full_alert", {})
    sensor = _sensor_of(meta["alert_source"])
    data = full.get("data", {})
    rule = full.get("rule", {})
    row = {
        "alert_id": meta["alert_id"],
        "timestamp": feat["timestamp"],
        "sensor": sensor,
        "rule_id": str(feat["rule_id"]),
        "rule_name": feat.get("rule_name"),
        "severity_raw": str(feat["rule_level"]),
        "severity": severity_score(sensor, feat["rule_level"]),
        "src_ip": feat.get("source_ip"),
        "dst_ip": feat.get("destination_ip"),
        "hostname": feat.get("hostname"),
        "user": feat.get("username"),
        "cves": _find_cves(feat.get("rule_name"), data.get("alert", {}).get("metadata"),
                           rule.get("cve")),
        "techniques": list(feat.get("rule_attacktechniques") or []),
        "raw": rec,
    }
    return row, bool(meta.get("misuse", False))


def normalize_records(records: Iterable[dict]) -> tuple[pd.DataFrame, pd.Series]:
    """Riasztások közös formára hozása.

    :return: (riasztások táblája időrendben, címkék ugyanabban a sorrendben, ``alert_id`` indexszel)
    """
    rows, labels = [], []
    for rec in records:
        row, label = normalize_cats_record(rec)
        rows.append(row)
        labels.append(label)
    df = pd.DataFrame(rows, columns=COLUMNS)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="ISO8601")
    lab = pd.Series(labels, index=df["alert_id"], name="label")
    order = df["timestamp"].argsort(kind="stable").to_numpy()
    df = df.iloc[order].reset_index(drop=True)
    lab = lab.iloc[order]
    return df, lab


def load_cats_jsonl(path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    """Egy CATS-formátumú adathalmaz (pl. ``ait_wazuh.jsonl``) betöltése és egységesítése."""
    with open(path, encoding="utf-8") as f:
        return normalize_records(json.loads(line) for line in f if line.strip())

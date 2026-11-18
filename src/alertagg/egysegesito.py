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


# ---------------------------------------------------------------------------------------------
# Az eredeti AIT-ADS formátum (Zenodo 8263181, ``<forgatókönyv>_wazuh.json``)
# ---------------------------------------------------------------------------------------------
#
# A fájl a Wazuh-kezelő kimenete, soronként egy JSON-rekord. Három fajta rekord van benne:
#
# * ``location == /var/log/suricata/eve.json`` – a hálózati (Suricata-) riasztás, szerkezetten;
# * ``location == /var/log/suricata/fast.log`` – **ugyanannak** a Suricata-riasztásnak a szöveges
#   másolata, amelyre a Wazuh saját szabálya (pl. 20100, 20101) is lefut. Ezeket kihagyjuk, mert
#   kétszer számolnák ugyanazt a hálózati eseményt (a CATS-változatban sincsenek benne);
# * minden más – a gépi (Wazuh-) riasztások.
#
# Az AMiner-riasztások külön fájlban vannak (``*_aminer.json``), ezeket nem olvassuk (D10).
#
# A jellemzőket a CATS átalakítójának AIT-beállításai (``tools/normalizer/config/ait_*.yml``)
# szerint képezzük, egyetlen eltéréssel: a gépnév meghatározása forgatókönyvtől független
# szabályokkal történik (lásd :func:`ait_gepnev_szabalyok`), nem a russellmitchell-re kézzel írt
# folyamatazonosító- és időpont-feltételekkel.

AIT_SURICATA_EVE = "/var/log/suricata/eve.json"
AIT_SURICATA_FAST = "/var/log/suricata/fast.log"
AIT_FORGATOKONYVEK = ["fox", "harrison", "russellmitchell", "santos", "shaw", "wardbeck",
                      "wheeler", "wilson"]

_LIP_RE = re.compile(r"lip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
_RIP_RE = re.compile(r"rip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
_TECH_RE = re.compile(r"[tT]\d{4}")


def ait_rekord_fajtaja(rec: dict) -> str | None:
    """``"suricata"``, ``"wazuh"``, vagy ``None`` (a kihagyandó fast.log-másolat)."""
    loc = rec.get("location", "")
    if loc == AIT_SURICATA_EVE:
        return "suricata"
    if loc == AIT_SURICATA_FAST:
        return None
    return "wazuh"


def _cats_ido(ts: str) -> str:
    """Az időbélyeg a CATS alakjában: UTC, ezredmásodpercre levágva, ``Z`` végződéssel."""
    t = pd.Timestamp(ts).tz_convert("UTC")
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _int_or_none(v: object) -> int | None:
    try:
        return int(v)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _first_regex(regex: re.Pattern, text: str | None) -> str | None:
    if not text:
        return None
    m = regex.findall(text)
    return m[0] if m else None


def ait_gepnev_szabalyok(records: Iterable[dict]) -> dict[str, str]:
    """A Wazuh-ügynök IP-címe → gépnév megfeleltetés, ugyanabból a fájlból, címkék nélkül.

    Minden ügynök-IP-hez azt a gépnevet rendeljük, amely a naplósor fejlécében
    (``predecoder.hostname``) a legtöbbször szerepel az adott ügynök rekordjaiban. A Suricata-rekordok
    nem számítanak (ott az ügynök az érzékelő, nem az érintett gép).
    """
    from collections import Counter, defaultdict

    szamlalo: dict[str, Counter] = defaultdict(Counter)
    for rec in records:
        if ait_rekord_fajtaja(rec) != "wazuh":
            continue
        ip = rec.get("agent", {}).get("ip")
        host = rec.get("predecoder", {}).get("hostname")
        if ip and host:
            szamlalo[ip][host] += 1
    return {ip: c.most_common(1)[0][0] for ip, c in szamlalo.items()}


def ait_gepnev(rec: dict, ugynok_gep: dict[str, str]) -> str | None:
    """Az érintett gép neve egy gépi riasztásnál.

    Sorrend: (1) a naplósor fejlécének gépneve; (2) az Apache-naplók helye (a CATS szabályával:
    ``apache2/intranet`` → ``intranet-server``, ``apache2/proxy`` → ``proxy-server``); (3) a beküldő
    Wazuh-ügynök IP-címéhez tartozó gépnév (:func:`ait_gepnev_szabalyok`).
    """
    host = rec.get("predecoder", {}).get("hostname")
    if host:
        return host
    loc = rec.get("location", "")
    if "/var/log/apache2/intranet" in loc:
        return "intranet-server"
    if "/var/log/apache2/proxy" in loc:
        return "proxy-server"
    return ugynok_gep.get(rec.get("agent", {}).get("ip"))


def ait_cats_formara(rec: dict, ugynok_gep: dict[str, str], forgatokonyv: str) -> dict | None:
    """Egy eredeti AIT-ADS rekordot CATS-formájú (``features`` + ``metadata``) rekorddá alakít.

    A címke (``metadata.misuse``) **nem** kerül bele. A fast.log-másolatnál ``None``.
    Az ``alert_id`` a Wazuh-kezelő saját azonosítója (``id``) a forgatókönyv nevével előtagolva.
    """
    fajta = ait_rekord_fajtaja(rec)
    if fajta is None:
        return None
    data = rec.get("data", {}) or {}
    rule = rec.get("rule", {}) or {}
    if fajta == "suricata":
        al = data.get("alert", {}) or {}
        feat = {
            "timestamp": _cats_ido(rec["@timestamp"]),
            "protocol": data.get("proto"),
            "rule_name": al.get("signature"),
            "rule_id": str(al.get("signature_id")),
            "rule_level": str(al.get("severity")),
            "rule_category": [al["category"]] if al.get("category") else None,
            "source_ip": data.get("src_ip"),
            "destination_ip": data.get("dest_ip"),
            "source_port": _int_or_none(data.get("src_port")),
            "destination_port": _int_or_none(data.get("dest_port")),
        }
    else:
        full_log = rec.get("full_log")
        mitre = rule.get("mitre", {}) or {}
        techs = list(dict.fromkeys(t for i in (mitre.get("id") or [])
                                   for t in _TECH_RE.findall(i)))
        feat = {
            "timestamp": _cats_ido(rec["@timestamp"]),
            "event_source": rec.get("location"),
            "hostname": ait_gepnev(rec, ugynok_gep),
            "rule_name": rule.get("description"),
            "rule_id": str(rule.get("id")),
            "rule_level": str(rule.get("level")),
            "rule_category": list(rule.get("groups") or []) or None,
            "rule_attacktechniques": [t.lower() for t in techs] or None,
            "rule_attacktactics": [t.lower() for t in (mitre.get("tactic") or [])] or None,
            "source_ip": data.get("srcip") or _first_regex(_LIP_RE, full_log),
            "destination_ip": data.get("dstip") or _first_regex(_RIP_RE, full_log),
            "source_port": _int_or_none(data.get("srcport")),
            "destination_port": _int_or_none(data.get("dstport")),
        }
    feat = {k: v for k, v in feat.items() if v is not None}
    return {
        "features": feat,
        "metadata": {"alert_source": f"ait_{fajta}", "alert_id": f"{forgatokonyv}:{rec['id']}"},
        "eredeti_id": rec["id"],
        "ugynok_ip": rec.get("agent", {}).get("ip"),
    }


def _sorok(path: str | Path) -> Iterable[dict]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load_ait_wazuh_json(path: str | Path, forgatokonyv: str | None = None,
                        erzekelo: str | None = None) -> pd.DataFrame:
    """Egy eredeti ``<forgatókönyv>_wazuh.json`` betöltése és egységesítése, **címkék nélkül**.

    :param erzekelo: ``"wazuh"`` vagy ``"suricata"``, ha csak az egyik kell (memóriatakarékos)
    :return: a közös formájú riasztások táblája időrendben (a címkét :func:`ait_idoszak_cimkek` adja)
    """
    path = Path(path)
    forgatokonyv = forgatokonyv or path.name.split("_")[0]
    ugynok_gep = ait_gepnev_szabalyok(_sorok(path))
    rows = []
    for rec in _sorok(path):
        cats = ait_cats_formara(rec, ugynok_gep, forgatokonyv)
        if cats is None:
            continue
        if erzekelo and cats["metadata"]["alert_source"] != f"ait_{erzekelo}":
            continue
        row, _ = normalize_cats_record(cats)
        rows.append(row)
    df = pd.DataFrame(rows, columns=COLUMNS)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="ISO8601")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)


def ait_idoszakok(labels_csv: str | Path, forgatokonyv: str) -> pd.DataFrame:
    """A ``labels.csv`` támadási időszakai egy forgatókönyvre (``attack``, ``start``, ``end`` UTC)."""
    t = pd.read_csv(labels_csv)
    t = t[t["scenario"] == forgatokonyv].copy()
    t["start"] = pd.to_datetime(t["start"], unit="s", utc=True)
    t["end"] = pd.to_datetime(t["end"], unit="s", utc=True)
    return t[["attack", "start", "end"]].reset_index(drop=True)


def ait_idoszak_cimkek(alerts: pd.DataFrame, idoszakok: pd.DataFrame) -> pd.Series:
    """Időszak-alapú címke: támadás, ha a riasztás ideje valamelyik támadási időszakba esik.

    Az időszak zárt: ``start <= idő <= end``. A címke ``alert_id`` indexű sorozat, külön a
    riasztások táblájától (D23).
    """
    ts = alerts["timestamp"]
    lab = pd.Series(False, index=alerts.index)
    for row in idoszakok.itertuples(index=False):
        lab |= (ts >= row.start) & (ts <= row.end)
    return pd.Series(lab.to_numpy(), index=alerts["alert_id"].to_numpy(), name="label")

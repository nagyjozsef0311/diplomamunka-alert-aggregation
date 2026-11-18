"""Környezeti agent: a riasztás által érintett gép fontossága és megfigyeltsége (4. fejezet 4.2.2 és
4.2.4; 5. fejezet 5.3).

Kimenet riasztásonként:

* ``erintett_gep`` – a gépnyilvántartás szerinti gépnév (ha nem azonosítható: hiányzik)
* ``g``            – a gép fontossága: ``(fokozat - 1) / 4``; ismeretlen gépnél a semleges 0,5
* ``m``            – a megfigyeltség (vakfolt-tényező): ``1 - lefedettség``; ismeretlen gépnél 0,5
* ``ismeretlen``   – igaz, ha a gép nem szerepel a nyilvántartásban (az elemző lássa, hogy a pontszám
  részben hiányos adaton alapul)

Az érintett gép meghatározása (D25):

* gépi érzékelő (Wazuh): a riasztásban szereplő gépnév; ha hiányzik vagy nem ismert, a riasztást
  beküldő Wazuh-ügynök IP-címéhez tartozó gép (5.2. táblázat: „ha hiányzik, az IP-cím alapján
  kikeresve”; D28);
* hálózati érzékelő (Suricata): ha a cél-IP-cím ismert gépé, az; különben ha a forrás-IP-cím ismert
  gépé, az; különben ismeretlen. A célt azért vesszük előre, mert a támadás a célgépen okozhat kárt.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from alertagg.gepnyilvantartas import Gepnyilvantartas

SEMLEGES = 0.5


def ugynok_ip(raw: dict | None) -> str | None:
    """A riasztást beküldő Wazuh-ügynök IP-címe az eredeti rekordból (mindkét formátumban)."""
    if not isinstance(raw, dict):
        return None
    if raw.get("ugynok_ip"):
        return raw["ugynok_ip"]
    return ((raw.get("full_alert") or {}).get("agent") or {}).get("ip")


def erintett_gep(alerts: pd.DataFrame, nyilv: Gepnyilvantartas) -> pd.Series:
    """Riasztásonként az érintett gép neve a nyilvántartásban (vagy ``None``)."""
    out = []
    raw = alerts["raw"] if "raw" in alerts.columns else pd.Series([None] * len(alerts))
    cols = alerts[["sensor", "hostname", "src_ip", "dst_ip"]].itertuples(index=False)
    ismert: dict = {}
    ip_gep: dict = {}

    def gep_ip(ip):  # memoizált lekérdezés (az eredmény ugyanaz)
        if ip not in ip_gep:
            ip_gep[ip] = nyilv.gep_ip_alapjan(ip)
        return ip_gep[ip]

    for row, r in zip(cols, raw, strict=True):
        if row.sensor == "wazuh":
            h = row.hostname
            if h not in ismert:
                ismert[h] = nyilv.ismert_gep(h)
            out.append(h if ismert[h] else gep_ip(ugynok_ip(r)))
        else:
            out.append(gep_ip(row.dst_ip) or gep_ip(row.src_ip))
    return pd.Series(out, index=alerts["alert_id"], name="erintett_gep", dtype=object)


def kornyezeti_meroszamok(alerts: pd.DataFrame, nyilv: Gepnyilvantartas,
                          fokozatok: dict[str, int] | None = None) -> pd.DataFrame:
    """A gép fontossága (``g``) és megfigyeltsége (``m``) riasztásonként.

    :param fokozatok: a gépek fokozatának felülírása – az ellenpróbához (összekevert fokozatok);
        alapból a nyilvántartás fokozatai
    """
    gep = erintett_gep(alerts, nyilv)
    fok = fokozatok if fokozatok is not None else nyilv.fokozatok()
    g = gep.map(lambda n: (fok[n] - 1) / 4 if n in fok else SEMLEGES).astype(float)

    lef: dict[str, float | None] = {n: nyilv.lefedettseg(n) for n in set(gep.dropna())}
    m = gep.map(lambda n: 1 - lef[n] if n in lef and lef[n] is not None else SEMLEGES)
    return pd.DataFrame({
        "erintett_gep": gep,
        "g": g,
        "m": m.astype(float),
        "ismeretlen": gep.isna(),
    })


def osszekevert_fokozatok(nyilv: Gepnyilvantartas, seed: int) -> dict[str, int]:
    """Ellenpróba (6.3): a gépek fokozatainak véletlen permutációja, rögzített kezdőértékkel.

    Ha az összekevert, értelmetlen nyilvántartás is javít a rangsoron, a javulás nem a környezeti
    információnak, hanem a pontszám szerkezetének köszönhető.
    """
    fok = nyilv.fokozatok()
    nevek = sorted(fok)
    ertekek = np.random.default_rng(seed).permutation([fok[n] for n in nevek])
    return dict(zip(nevek, (int(v) for v in ertekek), strict=True))

"""Csoportosító agent: az összetartozó riasztások csoportokba rendezése (5. fejezet, 5.3; 6.2. táblázat,
2. lépés).

Két riasztás akkor kerül egy csoportba, ha ugyanazt a gépet érintik, és a köztük eltelt idő nem haladja
meg a beállított időközt (``idokoz``). Gépenként időrendben haladva új csoport kezdődik, ha az előző
riasztás óta eltelt idő nagyobb az időköznél (egyszeres láncolás az időtengelyen).

A gép a környezeti agent által azonosított érintett gép (D25); ha az ismeretlen, a gépnév, ennek
hiányában a forrás-IP-cím. A csoport megőrzi a tagjai azonosítóját, így a riasztásszintű és a
csoportszintű értékelés ugyanabból az eredményből készül (5.3).

A csoport pontszáma a tagjai közül a legmagasabb (4.3); egyenlő pontszámnál az a csoport kerül előre,
amelyben több különböző szabály jelzett (4.3, utolsó bekezdés).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# A holtverseny-feloldás súlya: kisebb, mint bármely két valódi pontszám-különbség a gyakorlatban
HOLTVERSENY_SULY = 1e-6


def csoport_kulcs(alerts: pd.DataFrame, erintett_gep: pd.Series | None = None) -> pd.Series:
    """A csoportosítás gépkulcsa riasztásonként."""
    kulcs = pd.Series(alerts["hostname"].to_numpy(), index=alerts["alert_id"], dtype=object)
    if erintett_gep is not None:
        eg = erintett_gep.reindex(alerts["alert_id"])
        kulcs = eg.where(eg.notna(), kulcs)
    src = pd.Series(alerts["src_ip"].to_numpy(), index=alerts["alert_id"], dtype=object)
    return kulcs.where(kulcs.notna(), src).fillna("(ismeretlen)")


def csoportosit(alerts: pd.DataFrame, idokoz: pd.Timedelta,
                erintett_gep: pd.Series | None = None) -> pd.Series:
    """Csoportazonosító riasztásonként (``alert_id`` indexszel)."""
    kulcs = csoport_kulcs(alerts, erintett_gep)
    df = pd.DataFrame({"kulcs": kulcs.to_numpy(), "ido": alerts["timestamp"].to_numpy()},
                      index=alerts["alert_id"])
    df = df.sort_values(["kulcs", "ido"], kind="stable")
    uj = (df["kulcs"] != df["kulcs"].shift()) | (df["ido"].diff() > idokoz)
    df["csoport"] = np.cumsum(uj.to_numpy())
    return df["csoport"].reindex(alerts["alert_id"]).rename("csoport")


def csoport_pontszam(pontszam: pd.Series, csoport: pd.Series, szabaly: pd.Series) -> pd.Series:
    """Riasztásonként a csoportja pontszáma: a tagok maximuma, plusz a különböző szabályok számával
    arányos, elhanyagolható holtverseny-feloldó tag."""
    df = pd.DataFrame({"s": pontszam, "c": csoport, "r": szabaly})
    max_s = df.groupby("c")["s"].transform("max")
    kul = df.groupby("c")["r"].transform("nunique")
    return (max_s + HOLTVERSENY_SULY * kul).rename("csoport_pontszam")

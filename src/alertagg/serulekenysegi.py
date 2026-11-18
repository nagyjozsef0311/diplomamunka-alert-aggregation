"""Sérülékenységi agent: működhet-e a riasztásban jelzett támadás az érintett gépen (4. fejezet,
4.2.3; 5. fejezet, 5.3).

Az alkalmazhatóság (``a``) értékei:

* 1    – a szabály a gépen futó szoftver ismert sérülékenységére (CVE) hivatkozik;
* 0,75 – a szabály szolgáltatása fut a gépen (termék- vagy szolgáltatásegyezés);
* 0,25 – a gép szoftverkészlete ismert, és a szabály szolgáltatása nem fut rajta;
* 0,5  – semleges: a szabály nem köthető szolgáltatáshoz („altalanos” vagy nincs a listában), az
  érintett gép ismeretlen, vagy a gép szoftverkészlete nem ismert.

Az érték csak a pontszámot módosítja, riasztást nem távolít el (4.1, a „nem szűr” követelmény).
"""

from __future__ import annotations

import pandas as pd

from alertagg.gepnyilvantartas import Gepnyilvantartas

CVE_EGYEZES, SZOLG_EGYEZES, SZOLG_NINCS, SEMLEGES = 1.0, 0.75, 0.25, 0.5
ALTALANOS = "altalanos"


def alkalmazhatosag(alerts: pd.DataFrame, erintett_gep: pd.Series,
                    nyilv: Gepnyilvantartas,
                    szolgaltatasok: dict[str, set[str] | None] | None = None) -> pd.Series:
    """Az alkalmazhatóság riasztásonként (``alert_id`` indexszel).

    :param erintett_gep: a környezeti agent kimenete (``alert_id`` indexszel)
    :param szolgaltatasok: a gépek szolgáltatásainak felülírása – az ellenpróbához; alapból a
        nyilvántartás szoftverkészlete
    """
    eg = erintett_gep.reindex(alerts["alert_id"]).to_numpy()
    gyors: dict[str, set[str] | None] = {}
    cve_k: dict[str, set[str]] = {}
    szab_k: dict[tuple[str, str], str | None] = {}
    out = []
    for gep, sensor, rule_id, cves in zip(eg, alerts["sensor"], alerts["rule_id"],
                                          alerts["cves"], strict=True):
        if gep is None or (isinstance(gep, float) and pd.isna(gep)):
            out.append(SEMLEGES)
            continue
        if gep not in cve_k:
            cve_k[gep] = nyilv.gep_cve_i(gep)
        if cves and cve_k[gep] & set(cves):
            out.append(CVE_EGYEZES)
            continue
        kulcs = (sensor, str(rule_id))
        if kulcs not in szab_k:
            szab_k[kulcs] = nyilv.szabaly_szolgaltatasa(*kulcs)
        szolg = szab_k[kulcs]
        if szolg is None or szolg == ALTALANOS:
            out.append(SEMLEGES)
            continue
        if szolgaltatasok is not None:
            keszlet = szolgaltatasok.get(gep)
        else:
            if gep not in gyors:
                gyors[gep] = nyilv.szolgaltatasok(gep)
            keszlet = gyors[gep]
        if keszlet is None:
            out.append(SEMLEGES)
        else:
            out.append(SZOLG_EGYEZES if szolg in keszlet else SZOLG_NINCS)
    return pd.Series(out, index=alerts["alert_id"], name="a", dtype=float)


def osszekevert_szolgaltatasok(nyilv: Gepnyilvantartas, seed: int) -> dict[str, set[str] | None]:
    """Ellenpróba (6.3 mintájára): a gépek szolgáltatáskészleteinek véletlen permutációja a gépek
    között, rögzített kezdőértékkel."""
    import numpy as np

    gepek = sorted(nyilv.gepnevek())
    keszletek = [nyilv.szolgaltatasok(g) for g in gepek]
    perm = np.random.default_rng(seed).permutation(len(gepek))
    return {g: keszletek[i] for g, i in zip(gepek, perm, strict=True)}

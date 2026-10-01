# Kutatási jegyzet #2 – Értékelés és adathalmazok (K4+K5)
2026-09-21 · A források: Scholar Gateway, Consensus, alphaXiv, Crossref

## Döntések
- **A C1 monitorozási lefedettség** egyszerű formában kerül be.
  - Eszközönként azt nézzük, hogy aktív-e a Wazuh agent, és látja-e a Suricata az adott szegmenst.
  - Az alacsony lefedettség **bizonytalansági jelzőként** jelenik meg, nem pedig büntetésként.
- **A metrika-kombináció módszere** (AHP, fuzzy vagy ML) még nyitott kérdés.

## Fő megállapítás: az AIT-ADS
- **Mi ez?** Landauer et al. (2024, CSET) adathalmaza: Suricata-, Wazuh- és AMiner-riasztások, összesen kb. 2,6 millió riasztás.
  - 8 szcenárióból áll, támadási fázis-címkékkel.
  - A támadások: scanek, WordPress-exploit, jelszótörés, privilege escalation, DNS-exfiltráció.
  - Nyilvános: Zenodo 8263181.
- **Miért fontos?** Ugyanazt a stacket használja, mint a te homelabod, és ez az egyetlen nyilvános, riasztás-szintű, csoportcímkés benchmark (Karner et al. 2026 szerint).
- **Hiány:** nincs benne CMDB- és sérülékenységi adat. Ezt az AIT-LDSv2 hálózatleírásából lehet rekonstruálni: intranet, DMZ és internet zónák, valamint a sérülékeny WordPress plugin.
- **Kész baseline:** a time-delta csoportosítás (Landauer 2022) nyílt kóddal elérhető.

## Javasolt kétpályás értékelés
1. **Külső validitás – AIT-ADS.** Reprodukálható és összevethető a szakirodalommal.
2. **Belső kísérlet – saját homelab.** Itt a CMDB, a sérülékenységi adat és a lefedettség teljesen szabályozható, a ground truth pedig a támadás-orchestrációs szkript időbélyegeiből jön.

## Javasolt ablációs terv (K1-re is választ ad)

| Változat | Leírás |
|---|---|
| B0 | Nyers riasztások |
| B1 | Csak súlyosság szerinti rangsor |
| B2 | Time-delta csoportosítás (Landauer 2022) |
| M1 | Saját aggregáció kontextus nélkül (G1–G2 + A1–A6) |
| M2 | M1 + eszközmetrikák (S1–S4) |
| M3 | M2 + sérülékenység (V1–V2) |
| M4 | M3 + lefedettség (C1) = teljes modell |

Mérőszámok:
- **Terhelés-csökkenés:** ARR/QRR (E1).
- **Kihagyott valós támadások:** FNR, cél < 2% (E2).
- **Rangsor-minőség:** Precision@k, nDCG@k, MRR (E3).
- **Becsült elemzői terhelés** (E4).
- **Csoportosítás pontossága:** páronkénti TPR/TNR vagy purity (E5).

A változatok közötti különbség mutatja meg, hogy melyik metrikacsoport mennyit tesz hozzá az eredményhez.

## További értékelési források
- **Maggi et al. (2009), Njogu et al. (2012), Sommestad & Franke (2015):** kontextus- és sérülékenység-alapú szűrés.
  - Sommestad & Franke kritikusan méri a hasznát, ezért a korlátok tárgyalásánál érdemes idézni.
- **Riyad et al. (2019):** a riasztás-csökkentési arány, a completeness és a soundness klasszikus mérőszámai.
- **Shittu et al. (2015):** téves pozitívok csökkentésének mérése cyber range adaton.

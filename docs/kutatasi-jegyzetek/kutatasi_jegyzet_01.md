# Kutatási jegyzet #1 – Metrikák és kontextus (K1+K2)
2026-09-21 · Feldolgozva: Jalalvand 2024 (ACM CSUR), Tariq 2025 (ACM CSUR), Ndichu 2026 (arXiv)

## Fő megállapítások
- **Jalalvand et al. (2024)** 89 cikket vizsgált, és 5 kategóriába sorolja a priorizálási kritériumokat: **elemző, riasztás, eszköz, szervezet, külső környezet**. Ez a taxonómia a metrikarendszer vázaként használható.
  - Az eszközhöz kötött kritériumok (kritikalitás, CIA, pótolhatóság, sérülékenység, *coverage*, *applicability of attack to asset*) a második leggyakoribbak, de szinte csak automatizált módon használják őket.
  - A módszerek hat csoportba sorolhatók: ML, MCDM (AHP, TOPSIS, OWA), játékelmélet, optimalizálás, gráfalapú és hibrid.
- **Anuar et al. (2012), AHP-RIM:** AHP-vel súlyozza a kritikalitást, a karbantarthatóságot, a pótolhatóságot, a súlyosságot, a hasonlóságot és a gyakoriságot, és ezekből risk indexet számol. Ez **kész minta a metrika-kombinációra** (R1).
- **Alsubhi et al. (2008), FuzMet:** IDS-specifikus metrikák (applicability, importance, sensor sensitivity, severity), fuzzy logikával kombinálva.
- **Ndichu et al. (2026)** négy szűrési szakaszt különít el: szűrés, priorizálás, korreláció és LLM-támogatás.
  - Értékelési metrikák: QRR rögzített FNR mellett (FNR < 2%), nDCG@k, MRR, incidens-rekonstrukciós precision/recall, NASA-TLX.
  - Hiányként nevezi meg a benchmarkok hiányát és a valós, termelési validáció hiányát.
- **Tariq et al. (2025)** az alert fatigue négy okát azonosítja:
  1. munkaerő- és szakemberhiány,
  2. magas téves riasztási arány,
  3. szétaprózott, túlterhelt dashboardok,
  4. nem hatékony SOP-k.

  A megoldásokat az automatizálás–kiegészítés–együttműködés (A²C) szempontjai szerint rendszerezi.

## Következmények a dolgozatra
1. **A metrikarendszer vázát** a Jalalvand-taxonómia adja. A felhasznált kontextus-adatforrások: CMDB és sérülékenységi adatok (Wazuh Vulnerability Detector).
2. **A legerősebb téves pozitív szűrő a V2 „támadás alkalmazhatósága”.** Megmutatja, hogy a riasztott CVE vagy szolgáltatás valóban létezik-e a célgépen. Ez Valeur „verification” lépésének felel meg.
3. **A kombinációs módszer** AHP-súlyozott score legyen (indokolható, reprodukálható, nem kell tanítani). A DBSCAN csak az aggregációban (G1–G2) marad.
4. **Az értékelésben** a baseline a csak súlyosság szerinti rangsor legyen, a mérés pedig QRR@FNR, P@k/nDCG@k és a becsült terhelés (Shah 2019).
5. **Nyitott kérdés:** a monitorozási lefedettség (C1). A feladatlap „monitorozási szempontokat” említ, de a választott adatforrások között nem szerepel.

## Hazai forrás
- Hámornik & Krasznay (2017): SOC csapatszintű emberi tényezők (AHFE, Springer).

A teljes lista a `Diplomamunka_forrasok.xlsx` fájlban és a `claude/forrasok.bib` fájlban található.

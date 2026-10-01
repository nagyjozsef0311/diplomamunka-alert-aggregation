# Átadás a kutatás (Cowork) és a kódolás (Claude Code) között

Ez a fájl köti össze a két munkafelületet. Rövid tételeket írj bele, dátummal. Az elintézett
tételt jelöld `[x]`-szel, és ne töröld.

## Kutatásból a kódolásnak

Ezek a döntések készek, és megvalósíthatók.

- [ ] 2026-10-01 – Az 1. hét feladatai a `docs/munkaterv.md` szerint: környezet felállítása,
  adatletöltés, adatfeltárás (`experiments/01_adatfeltaras.ipynb`).
- [ ] 2026-10-01 – Az AMiner-riasztásokat kihagyjuk (D10). A Suricata-riasztásokat a
  `<forgatókönyv>_wazuh.json` fájlokból kell kiszűrni.
- [ ] 2026-10-01 – **D12, háromrétegű megvalósítás.** Most csak a mag készül: sima Python-modulok
  a `src/alertagg/`-ban, LangGraph- és MCP-függőség nélkül, meghatározott bemenettel és kimenettel,
  tömeges (pandas) feldolgozással. A LangGraph-vezérlés az AIT-mérések után jön, az MCP opcionális.
  Részletek: `CLAUDE.md` 3. pont és `docs/kutatasi-jegyzetek/kutatasi_jegyzet_05.md`.

## Kódolásból a kutatásnak

Ide kerülnek a kódolás közben felmerült kérdések, meglepő adatok és mérési eredmények.

- [ ] 2026-10-01 – Első adatfeltárás: az AIT-ADS riasztásaiban nincs sérülékenység-azonosító
  (CVE), és a Suricata-riasztásokban nincs gépnév. Kérdés: hogyan indokoljuk a dolgozatban a
  szolgáltatásszintű illesztést? (Részletek: `docs/munkaterv.md`.)

# Feladatlista

2026-10-01 óta (D14) minden munka a Claude Code-ban folyik, ezért ez a fájl már nem két munkafelület
közti átadás, hanem a közös feladatlista. Rövid tételeket írj bele, dátummal. Az elintézett tételt
jelöld `[x]`-szel, és ne töröld. A korábbi két rész (lent) megmarad.

## A szerzőtől vár

- [x] 2026-10-01 – A kari szakdolgozat-készítési útmutató (PDF) feltöltése.
- [x] 2026-10-01 – Az Overleaf-sablon forrása zipben.
- [ ] 2026-10-01 – A konzulens nevének alakja a fájlnevekben („Vorosne” vagy „BanatiBaumann”).
- [ ] 2026-10-01 – A 2026/27. őszi félév pontos dátumai (a szorgalmi időszak vége, a beszámoló hete).
- [ ] 2026-10-01 – Hálózati beállítás: `zenodo.org`, `api.crossref.org`, `arxiv.org`, `export.arxiv.org` engedélyezése.

## Diplomamunka II.

- [x] 2026-10-01 – Követelmények, leadandók és fejezetvázlat: `docs/diplomamunka-2.md`.
- [x] 2026-10-01 – Új ütemterv a decemberi leadásig (D13): `docs/munkaterv.md`.
- [x] 2026-10-01 – A kari sablon és az útmutató a `thesis/` mappában (v0.1, javítások nélkül).
- [ ] 2026-10-01 – A sablon formai hiányosságainak javítása (margó, sorköz, oldalszám, fejezetcím,
  hivatkozási stílus) – a szerző jóváhagyására vár.
- [ ] 2026-10-01 – **IP SCAN Portál:** megtörtént-e a témabejelentés? (MSc: a szorgalmi időszak 9.
  hetének utolsó munkanapja; a teljesítés feltétele.)

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

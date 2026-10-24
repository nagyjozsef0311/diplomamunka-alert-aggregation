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

- [x] 2026-10-01 – Az 1. fejezet (Bevezetés) írási csomagja: `docs/irasi-csomagok/01_bevezetes.md`.
- [x] 2026-10-07 – Az írási csomag bővítése pontonkénti forrásjegyzettel (D19); ellenőrizve: Uetz,
  Ndichu, Alahmadi, Tariq, Kokulu, Vielberth; a `references.bib`-ben pótolva Tariq, Jalalvand, Vielberth adatai.
- [ ] 2026-10-07 – Még ellenőrizendő: Jalalvand 2025 tartalmi számai (89 cikk, 5 szempontcsoport) és a
  Hámornik–Krasznay-cikk tartalma (Springer, könyvtári hozzáféréssel).
- [x] 2026-10-07 – A szerző első Bevezetés-vázlata a tárolóban; átnézés: `docs/atnezesek/01_bevezetes_2026-10-07.md`.
- [x] 2026-10-07 – Az írási csomag 3. változata: átvehető, forrásfüggetlen LaTeX-blokkok (D20), lefordítva ellenőrizve.
- [ ] 2026-10-07 – **A szerző átdolgozza** a Bevezetést (elsőként a csomagból átvett megfogalmazásokat).
- [ ] 2026-10-01 – Döntés: kell-e a két ábra (a riasztások útja; a dolgozat felépítése) és a kutatási
  kérdések táblázata az 1. fejezetbe.

- [x] 2026-10-01 – Követelmények, leadandók és fejezetvázlat: `docs/diplomamunka-2.md`.
- [x] 2026-10-01 – Új ütemterv a decemberi leadásig (D13): `docs/munkaterv.md`.
- [x] 2026-10-01 – A kari sablon és az útmutató a `thesis/` mappában (v0.1, javítások nélkül).
- [x] 2026-10-01 – A sablon formai hiányosságainak javítása (v0.2, `thesis/VALTOZASOK.md`).
- [x] 2026-10-01 – IP SCAN Portál: a témabejelentés megvolt (a szerző szerint).
- [ ] 2026-10-01 – **A szerző javítja a Word-sablonokban, majd PDF-ben feltölti Overleafbe:** a belső
  borítólapon a mintaszám maradt (T-000123/FI12904 helyett T/0012125/FI12904/N), az évszám a végleges
  dolgozatnál 2027; a konzultációs naplók kitöltése (most GIPSZ JAKAB mintaadat).
- [ ] 2026-10-01 – `thesis/references.bib`: mind az 55 cikknél hiányzik a kötet és az oldalszám
  (az útmutató kéri); pótlás a Crossrefből szkripttel, amint az `api.crossref.org` elérhető.
  Webes forrásoknál (`langgraph2025`, `mcp2026spec`) az `urldate` a tényleges megtekintéskor kerül be.

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

## 2. fejezet

- [x] 2026-10-08 – Írási csomag: `docs/irasi-csomagok/02_ids_es_soc.md` (6 alfejezet, táblázat, lefordítva ellenőrizve).
- [ ] 2026-10-08 – Ellenőrizendő: Denning 1987 DOI-ja; a NIST SP 800-94 érvényessége a CSRC-oldalon.
- [x] 2026-10-08 – A csomag 2. változata: 2.2 behatolásérzékelő eszközök, 2.3 SIEM-eszközök (összehasonlító táblázatokkal), 2.4 SOC-szervezeti modellek.
- [ ] 2026-10-08 – A kutatási rés pontosítása a Bevezetésben: a Splunk kockázatalapú riasztása már használ eszköz- és felhasználói adatot; a rés a *nyilvánosan mért* hozzáadott érték.
- [ ] 2026-10-08 – Döntés: kell-e a két ábra (az IDS-ek csoportosítása; a riasztások útja a SOC-ban).

## 3. fejezet

- [x] 2026-10-08 – Írási csomag: `docs/irasi-csomagok/03_szakirodalom.md` (6 alfejezet, 4 összehasonlító táblázat, köztük a rések és a saját rendszer megfeleltetése; lefordítva ellenőrizve, kb. 10 oldal).
- [x] 2026-10-08 – `references.bib`: Njogu 2013, 6(1), 15–27; Anuar évszáma 2013 (a kulcsok nem változtak). `acronyms.tex`: AHP, CVSS, AUROC, MCP, RAG.
- [ ] 2026-10-08 – Ellenőrizendő: Hmimou 2025 (csak a kivonat alapján), AgentSOC pontos kísérleti adatai, Wilkens/Nadeem/Shittu tartalma (most szám nélkül szerepelnek).
- [ ] 2026-10-08 – Döntés: kell-e ábra a Valeur-féle feldolgozási lépésekről a saját agentek hozzárendelésével.
- [ ] 2026-10-08 – **A szerző megírja** a `chapters/3_Modszerek.tex`-et a csomag alapján.

## 4. fejezet

- [x] 2026-10-23 – A szerző v0.3-as zipje behozva (1–3. fejezet, main.tex, acronyms.tex); a references.bib javításai (Njogu, Anuar) megmaradtak, `saaty1990` új. Átnézés: `docs/atnezesek/03_modszerek_2026-10-23.md`.
- [x] 2026-10-23 – Írási csomag: `docs/irasi-csomagok/04_megoldas_es_metrikak.md` (választás, négy mérőszám, összevonás AHP-val; a mérés terve a 6. fejezetnek előre megírva). Lefordítva ellenőrizve, kb. 6,5 oldal.
- [ ] 2026-10-23 – **A szerző dönt:** a gép fontosságának szabályai (4.2. táblázat), az alkalmazhatóság négy lépcsője, a megfigyeltség a pontszámba kerüljön-e (D21).
- [ ] 2026-10-23 – **A szerző elvégzi** a páros összehasonlítást (4 szempont, 6 pár) a mérés előtt; kérésre kitölthető táblázat.
- [ ] 2026-10-23 – A `saaty1990` DOI-ját a kiadói oldalon ellenőrizni (másodlagos forrásból).
- [x] 2026-10-23 – A diasor 7. diája javítva (plafonhatás, D22).

## 5. fejezet

- [x] 2026-10-23 – Írási csomag: `docs/irasi-csomagok/05_rendszerterv.md` (agent-fogalom, felépítés, hét agent, közös riasztásforma, gépnyilvántartás, eszközválasztás). Lefordítva ellenőrizve, kb. 8 oldal.
- [x] 2026-10-23 – Három ábra (TikZ, vektoros): `thesis/img/agent_architektura.pdf`, `adatmodell.pdf`, `magyarazo.pdf`; forrásuk `thesis/img/src/`. **A szerző jóváhagyására vár.**
- [x] 2026-10-23 – Új források: Wooldridge–Jennings 1995, AutoGen (Wu és mtsai. 2023), CrewAI-dokumentáció, Ollama.
- [ ] 2026-10-23 – Az agent-meghatározást (5.1) megmutatni a konzulensnek.
- [ ] 2026-10-23 – Ha a laborban a Wazuh sérülékenység-észlelőjét használjuk: dokumentáció a `.bib`-be.

## 6. fejezet

- [x] 2026-10-24 – Írási csomag: `docs/irasi-csomagok/06_teszteles_es_ertekeles.md` (AIT-ADS, labor, mérési terv, magyarázó agent értékelése, programtesztelés, érvényességi korlátok). A mérési terv a 4. csomagból ide került. Lefordítva ellenőrizve, kb. 7 oldal.
- [x] 2026-10-24 – Laborábra (TikZ): `thesis/img/labor.pdf`, forrása `thesis/img/src/labor.tex`. **A szerző jóváhagyására vár.**
- [ ] 2026-10-24 – **A szerző dönt:** a háttérzaj tartalma; legyen-e levelező kiszolgáló a laborban.
- [ ] 2026-10-24 – Ha a CVE-2020-24186-ra hivatkozunk: NVD-oldal a `.bib`-be.

## Előadások

- [x] 2026-10-14 – Kutatási eredmények diasor a NIK-sablonban: `docs/prezentaciok/kutatasi_eredmenyek_2026-10-14.pptx` (címdia + 6 tartalmi dia, jegyzetekkel: probléma és rés, adathalmazok, módszerek, hét agent, különbségek, várt eredmények). Előállítás: `scripts/build_kutatasi_deck.py`.

## Kódolásból a kutatásnak

Ide kerülnek a kódolás közben felmerült kérdések, meglepő adatok és mérési eredmények.

- [ ] 2026-10-01 – Első adatfeltárás: az AIT-ADS riasztásaiban nincs sérülékenység-azonosító
  (CVE), és a Suricata-riasztásokban nincs gépnév. Kérdés: hogyan indokoljuk a dolgozatban a
  szolgáltatásszintű illesztést? (Részletek: `docs/munkaterv.md`.)

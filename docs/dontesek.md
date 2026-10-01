# Döntésnapló

Minden fontos döntés egy sorban: mit döntöttünk, mikor, és miért. Ha egy döntés változik, a régit
nem töröljük, hanem új sort írunk, és megjelöljük, melyiket váltja.

| # | Dátum | Döntés | Indok | Forrás |
| --- | --- | --- | --- | --- |
| D1 | 2026-09-21 | A kontextus forrásai: gépnyilvántartás (szerep, fontosság, zóna) és sérülékenységi adat | A Wazuh gépleltára és sérülékenység-keresője közvetlenül használható | kutatási jegyzet #1 |
| D2 | 2026-09-21 | A megfigyeltség (Wazuh agent és Suricata-lefedettség) egyszerű formában bekerül | A feladatlap monitorozási szempontot is kér | kutatási jegyzet #2 |
| D3 | 2026-09-21 | A pontszám determinisztikus, páros összehasonlítással (AHP) súlyozott; a nyelvi modell csak magyarázatot ír | Megismételhető, tanítás nélküli; a szakirodalom is hibrid felépítést javasol | kutatási jegyzet #3 |
| D4 | 2026-09-21 | Kétpályás értékelés: AIT-ADS nyilvános adathalmaz + saját labor | Külső összevethetőség és teljes kontroll | kutatási jegyzet #2 |
| D5 | 2026-09-21 | Erős összehasonlítási alap: kockázatalapú riasztás-pontozás (Uetz et al. 2026, CATS) | Ez a legerősebb, környezetet nem használó módszer; a dolgozat ehhez képest mér | kutatási jegyzet #4 |
| D6 | 2026-09-21 | A gépnyilvántartás relációs adatbázis (SQLite / PostgreSQL), a szoftver-azonosító (CPE) az illesztési kulcs | Átlátható, prototípushoz elég; tudásgráf: továbbfejlesztési lehetőség | kutatási jegyzet #4 |
| D7 | 2026-10-01 | Először az AIT-ADS-en dolgozunk (offline), utána épül a labor | Gyors, laborfüggetlen első eredmény | AIT-ADS munkaterv |
| D8 | 2026-10-01 | A labor vegyes: VMware a gépekhez és zónákhoz, Docker az alkalmazásokhoz és az elemző oldalhoz | Valódi sérülékenységi és megfigyeltségi adat, megismételhető telepítés | megbeszélés, 2026-10-01 |
| D9 | 2026-10-01 | SOC-os kolléga nélkül: a súlyokat a szerző adja szakértőként, érzékenységvizsgálattal és adatból tanult súlyokkal összevetve | A bevonás bizonytalan; így is védhető | megbeszélés, 2026-10-01 |
| D10 | 2026-10-01 | Az AMiner-riasztásokat kihagyjuk | Hiányzik belőlük a gépnév és a súlyosság; anomáliadetektort a laborban sem használunk | AIT-ADS munkaterv |
| D11 | 2026-10-01 | Privát GitHub-tároló, a beadás után publikus; adat és CATS-kód nem kerül bele, csak letöltő szkript | Az AIT-ADS nagy, a CATS-nek nincs licence | megbeszélés, 2026-10-01 |
| D12 | 2026-10-01 | Háromrétegű megvalósítás: a mag sima Python-modulokból áll (keretrendszertől független); a vezérlést LangGraph adja az AIT-mérések után; az MCP csak opcionális csatlakozó a gépnyilvántartáshoz, a laborban | A mérések gyorsak és megismételhetők maradnak; a LangGraph kézzelfoghatóvá teszi az agent-felépítést; a kis helyi modellek rosszul vezénylik a vizsgálatot (HESP 2026), ezért a menet a modellen kívül marad | kutatási jegyzet #5 |
| D13 | 2026-10-01 | A Diplomamunka II. leadásáig (2026. december) az írás az elsődleges: a 30–35 oldalas beszámoló fejezetei hetente haladnak, a kód az első eredményig (alapok visszamérése, egy forgatókönyv 3–5. lépcsője) megy; a csoportosító agent, a 8 forgatókönyv, a LangGraph és a labor a III. félévre marad. A D7 9 hetes ütemezését felváltja | A Diplomamunka II. elmélet, specifikáció és terv bemutatását kéri, a megvalósítás az utolsó félévre maradhat | `docs/diplomamunka-2.md`, megbeszélés, 2026-10-01 |
| D14 | 2026-10-01 | Minden munka (kutatás, dolgozatírás LaTeX-ben, kód) a Claude Code-ban folyik; a `docs/atadas.md` feladatlistaként marad meg. A 0. pontbeli munkamegosztást felváltja | Egy helyen marad a teljes háttér; a tároló a közös emlékezet | megbeszélés, 2026-10-01 |
| D15 | 2026-10-01 | A feladatlap és más személyes adatot (Neptun-kód, törzskönyvi szám) tartalmazó fájl nem kerül a gitbe; a tartalmukat a `docs/` fájlok foglalják össze | A tároló a beadás után nyilvános lesz | megbeszélés, 2026-10-01 |

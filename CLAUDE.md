# CLAUDE.md – a diplomamunka teljes háttere

Ez a fájl minden munkamenet elején betöltődik. Benne van minden, ami a 2026. szeptember 21. és
október 1. közötti Cowork-beszélgetésben kialakult, hogy itt, a Claude Code-ban ugyanonnan
folytathassuk. A részletek a `docs/` mappában vannak. Ha valami itt és ott eltér, a `docs/dontesek.md`
az irányadó.

## 1. Kiről és miről szól

| | |
| --- | --- |
| Szerző | Nagy József („Csoza”), medior SOC-mérnök, MSc-hallgató |
| Iskola | Óbudai Egyetem, Neumann János Informatikai Kar, Kiberbiztonsági mérnöki MSc |
| Konzulens | Vörösné Dr. Bánáti-Baumann Anna |
| Cím | Agent-alapú, metrika-vezérelt IDS riasztásaggregáció SOC környezetben |
| Beadási határidő | 2027-05-15 |
| Kötelező alap | A feladatlap (claude.ai projekt: `3FMSc_KIBERBIZTONSÁGI ... .doc`). A kutatási terv (`Diplomamunka_kutatasi_terv.txt`) csak a probléma feltárására szolgál. |

**A probléma:** a SOC-elemzőket elárasztják a behatolásérzékelő riasztásai (riasztási fáradtság).
**A cél:** a Suricata (hálózati) és a Wazuh (gépi) riasztásait csoportosítani és rangsorolni,
mérőszámok és a környezetből származó információk alapján, együttműködő agentekkel.

## 2. Hogyan dolgozzunk együtt (a szerző kérései)

- **Magyarul** kommunikálj, egyszerű, közérthető szavakkal.
- **Ne használj megmagyarázatlan rövidítést vagy metrikakódot** (például ne „S1”, „AUROC”, „RBA”
  magyarázat nélkül). Ha kell, először írd ki magyarul, a rövidítést csak zárójelben add meg.
  Ez a szerző kifejezett visszajelzése volt: „túl sok benne a rövidítés, ami még nekem sem világos”.
- **Kérdezz rá, mit csináljunk.** A szerző azt kérte: „Folyton kérdezz tőlem, hogy mit csinálj.”
  Szereti a **választható lehetőségeket** (2–4 opció, az ajánlott jelölve) és a **döntési
  táblázatokat** (lehetőség, mellette, ellene, forrás, döntés).
- Röviden, lényegre törően válaszolj. Ne ismételd el, amit már tud.
- A szakirodalomnál: **lektorált forrás és friss arXiv** egyaránt jöhet. Minden hivatkozás
  DOI-ját vagy arXiv-azonosítóját ellenőrizni kell (Crossref), kitalált szerzőnév nem kerülhet be.
  Ha egy társszerző nem ellenőrizhető: „and others”.

## 3. A kutatás eddigi eredménye röviden

Részletesen: `docs/kutatasi-eredmenyek.md` (kérdésenként döntési táblázatokkal és fogalomtárral),
`docs/kutatasi-jegyzetek/01–04`, `docs/metrika-katalogus.md`.

### A dolgozat helye a szakirodalomban

- A legerősebb, környezetet nem használó módszer a **kockázatalapú riasztás-pontozás**
  (risk-based alerting): Uetz és mtsai. 2026, arXiv:2609.02465, eszközük a **CATS**.
  - Öt részpontszám: a szabály szintje (súlyosság), halmozódás (1 perces ablak), változatosság
    (1 órás ablak), ritkaság és szabálytalanság (1 napos ablak).
  - Az ajánlott súlyok: 12 / 24 / 44 / 10 / 10 %.
  - Eredmény az AIT-ADS-en: rangsor-pontosság (AUROC) kb. 0,92, szemben a csak súlyosság szerinti
    rangsor kb. 0,72-es értékével.
  - **Nem használja** a gépek fontosságát és a sérülékenységeket. Ez a dolgozat rése: mennyit ad
    hozzá a környezeti információ a kockázatalapú pontozáshoz képest.

### A kutatási kérdésekre adott válaszok

| Kérdés | Választott megoldás |
| --- | --- |
| 1. Milyen mérőszámokkal priorizáljunk? | Kockázatalapú pontozás mérőszámai, kiegészítve a gép fontosságával, a sérülékenységgel és a megfigyeltséggel. Összevonás: súlyozott összeg, a súlyok páros összehasonlításból (AHP). |
| 2. Hogyan tároljuk a környezetet? | Relációs adatbázis (SQLite, később PostgreSQL). Táblák: gép, szolgáltatás, sérülékenység, megfigyeltség, szabály–sérülékenység kapcsolat. Illesztési kulcs: szabványos szoftver-azonosító (CPE). Tudásgráf csak továbbfejlesztésként. |
| 3. Milyen agentek kellenek? | Vegyes felépítés: a pontszámot kiszámítható program adja, a nyelvi modell (helyben futó Ollama) csak magyarázatot ír, amit egy ellenőrző lépés átnéz. |
| 4. Hogyan mérjük a terhelés csökkenését? | Riasztásszám-csökkenés úgy, hogy legfeljebb 2% valós támadás csússzon át; becsült elemzői idő. |
| 5. Hogyan mérjük a rangsor minőségét? | Rangsor-pontosság (AUROC), átlagos pontosság (AP), valós riasztások aránya a lista első 10%-ában, csoportok tisztasága. |

### A hét agent

| Agent | Feladat |
| --- | --- |
| Egységesítő | A Suricata- és a Wazuh-riasztást közös formára hozza |
| Csoportosító | Az összetartozó riasztásokat összefogja (közös IP-cím vagy felhasználó, időbeli közelség) |
| Környezet | Kikeresi az érintett gép adatait (fontosság, zóna, megfigyeltség) |
| Sérülékenységi | Megnézi, működhet-e a támadás azon a gépen |
| Rangsoroló | Kiszámolja a pontszámot a páros összehasonlításból kapott súlyokkal |
| Magyarázó | Rövid szöveges összefoglalót ír (nyelvi modell + ellenőrzés) |
| Vezérlő | Sorba rendezi a lépéseket, naplóz, időt mér |

A technológia **még nyitott**: külön Python-szolgáltatások, LangGraph vagy MCP. Addig az agentek
egy Python-csomag (`src/alertagg/`) moduljai, így később bármelyik keretbe beköthetők.

### Az értékelés lépcsői (lépésenkénti bővítés)

| Lépés | Mit rangsorolunk |
| --- | --- |
| 0 | Nyers riasztások, rangsor nélkül |
| 1 | Csak a súlyosság szerint |
| 2 | Csoportosítás után |
| 3 | Kockázatalapú pontozás (Uetz 2026, CATS) – az erős összehasonlítási alap |
| 4 | 3. lépés + a gépek fontossága |
| 5 | 4. lépés + sérülékenységek |
| 6 | 5. lépés + megfigyeltség |

- A forgatókönyvek közti különbséget Wilcoxon-próbával vizsgáljuk (8 forgatókönyv).
- A szakértői súlyokat a mérés **előtt** rögzítjük (Arp és mtsai. 2022 hibalistája miatt).
- Az adatból tanult súlyokat „egyet kihagyunk” módon tanítjuk: 7 forgatókönyvön tanulunk, a 8.-on mérünk.

## 4. Adatok

| Adat | Hol | Megjegyzés |
| --- | --- | --- |
| AIT-ADS | Zenodo 8263181, CC BY 4.0 | `ait_ads.zip` (MD5 43db6b1f…, 96 202 946 bájt) és `labels.csv` (MD5 60ff3379…, 3 703 bájt). 8 forgatókönyv. A Suricata-riasztások is a `<forgatókönyv>_wazuh.json` fájlokban vannak. Letöltés: `python scripts/download_ait_ads.py` |
| CATS + felcímkézett AIT-változat | github.com/962012d09b/cats, commit 628cf48a6f569cafc463f47d512bc626d0ac366a | `datasets/ait_wazuh.zip`, `ait_suricata.zip`, JSON-sorok (címke: `metadata.misuse`, jellemzők: `features.*`), csak a russellmitchell forgatókönyv. **Nincs licence, ezért nem kerül a tárolóba.** Letöltés: `python scripts/download_cats.py` |

**Első adatfeltárás (2026-10-01, CATS-változat, russellmitchell):**

| | Wazuh | Suricata |
| --- | --- | --- |
| Riasztások | 23 116 | 9 186 |
| Ebből támadás | 7 661 (33%) | 44 (0,5%) |
| Különböző szabályok | 20 | 13 |
| Gépnév | van | nincs, IP-cím alapján kell illeszteni |
| CVE-hivatkozás | 0 | 0 |

**Következmény:** az AIT-ADS-en a „működhet-e a támadás ezen a gépen” csak szolgáltatás- és
termékszinten mérhető (pl. webes támadás WordPresst futtató gépre). CVE-szintű illesztés: a laborban.
Az AMiner-riasztásokat kihagyjuk (nincs bennük gépnév és súlyosság).

## 5. Labor (az AIT-ADS-mérések után)

- Vegyes: **VMware** a gépekhez és zónákhoz (Wazuh agentek, Suricata egy „promiscuous” port
  csoporton), **Docker** a sérülékeny alkalmazásokhoz és az elemző oldalhoz. 64–128 GB RAM áll rendelkezésre.
- Az AIT hálózatát másoljuk le (pl. WordPress 5.8.2 + wpDiscuz, CVE-2020-24186), és teszünk mellé
  egy ártalmatlan „háttérzaj”-generátort.
- A régi, Geminivel készült Docker-környezet elveszett, elölről kezdjük.

## 6. SOC-os kolléga nélkül

A súlyokat a szerző adja meg szakértőként, páros összehasonlítással (a következetességi arány 0,1
alatt legyen). Ezt ±20%-os érzékenységvizsgálattal és adatból tanult súlyokkal vetjük össze. Az elemzői
terhelést kérdőív (NASA-TLX) helyett becsléssel számoljuk.

## 7. Nyitott kérdések

A konzulenssel még nem egyeztetett kérdések:

- jóváhagyja-e az irányt;
- elfogadja-e az „agent” meghatározásunkat;
- bevonhatók-e SOC-os kollégák a súlyozásba;
- hivatkozhatók-e a még nem lektorált arXiv-cikkek.

Technikai döntés még nem született: milyen keretben fussanak az agentek (Python-szolgáltatások, LangGraph vagy MCP).

## 8. Munkaterv és a következő lépés

A 9 hetes terv: `docs/munkaterv.md` (rövid) és `docs/munkaterv-reszletes.md` (teljes). A cél,
hogy december első hetére meglegyen az első mérhető eredmény.

**Most következik – 1. hét (okt. 5–11):**

1. `python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`
2. A két letöltő szkript futtatása.
3. Adatfeltárás egy notebookban (`experiments/01_adatfeltaras.ipynb`):
   - mezők, riasztástípusok, időtartam;
   - az eredeti és a CATS-változat összevetése;
   - mely IP melyik géphez tartozik.
4. Ezután (2. hét) az **egységesítő agent** (`src/alertagg/normalizer.py`) a közös
   riasztásformával: idő, forrás- és cél-IP, gépnév, szabály, súlyosság, sérülékenység-hivatkozás,
   támadási technika. Teszttel igazoljuk, hogy a CATS-változatból és az eredetiből ugyanazok a riasztások jönnek ki.

## 9. Szabályok a tárolóban

- **Adat soha nem kerül a gitbe** (`data/` és `*.zip`/`*.jsonl` a `.gitignore`-ban). A CATS kódja sem.
- Minden fontos döntés új sort kap a `docs/dontesek.md`-ben, a régit nem töröljük.
- A tároló privát, a beadás után lesz publikus.
- Kódstílus: ruff (100 karakteres sorhossz), tesztek: pytest a `tests/` mappában.

## 10. Kapcsolódó anyagok a claude.ai-on

- „UNI - Diplomamunka” projekt (feladatlap, kutatási terv, kutatási jegyzetek, forrásjegyzék).
- Konzulensi diasor: https://claude.ai/artifact/E7GeaF5VNKwYvBVX2cmcGr
- „Kutatási eredmények – döntések kutatási kérdésenként” (doksi): https://claude.ai/code/artifact/d0c6b0a6-6dc5-49ef-b30d-a26adc52479e – a tárolóban: `docs/kutatasi-eredmenyek.md`
- „AIT-ADS munkaterv” (doksi): https://claude.ai/code/artifact/8c2f6d55-6b09-431f-95d9-f4c3ffe84ceb – a tárolóban: `docs/munkaterv-reszletes.md`
- Forrásjegyzék: `thesis/references.bib` (61 tétel) és `thesis/forrasok.xlsx`.

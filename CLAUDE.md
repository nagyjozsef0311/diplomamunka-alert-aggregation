# CLAUDE.md – a diplomamunka teljes háttere

Ez a fájl minden munkamenet elején betöltődik. Benne van minden, ami a 2026. szeptember 21. és
október 1. közötti Cowork-beszélgetésben kialakult, hogy itt, a Claude Code-ban ugyanonnan
folytathassuk. A részletek a `docs/` mappában vannak. Ha valami itt és ott eltér, a `docs/dontesek.md`
az irányadó.

## 0. Munkamegosztás: minden itt folyik (D14, 2026-10-01)

- **Itt, a Claude Code-ban folyik minden:** szakirodalom-kutatás, módszertani döntések, a dolgozat
  írása LaTeX-ben (`thesis/`), a konzulensnek szóló anyagok, a kód, a mérések és a tesztek.
  (Korábban a kutatás a claude.ai Cowork-ban folyt; az ott készült anyagok a `docs/` mappában vannak.)
- **A tároló a közös emlékezet.** Ami nincs commitolva és felküldve, az a munkamenet végén elvész.
  Minden munkadarab után commit és push.
- **A `docs/atadas.md` a feladatlista.** Az elintézett tételt jelöld `[x]`-szel, ne töröld.
- Minden döntés új sort kap a `docs/dontesek.md`-ben; a kutatás eredménye kutatási jegyzetbe
  (`docs/kutatasi-jegyzetek/`), a hivatkozás a `thesis/references.bib`-be kerül (ellenőrzött DOI-val vagy arXiv-azonosítóval).
- Mérési eredményt (számokat, táblázatokat) mindig a `results/` mappába írj.
- Személyes adat (Neptun-kód, törzskönyvi szám, a feladatlap fájlja) nem kerül a gitbe (D15).

## 1. Kiről és miről szól

| | |
| --- | --- |
| Szerző | Nagy József („Csoza”), medior SOC-mérnök, MSc-hallgató |
| Iskola | Óbudai Egyetem, Neumann János Informatikai Kar, Kiberbiztonsági mérnöki MSc |
| Konzulens | Vörösné Dr. Bánáti-Baumann Anna |
| Cím | Agent-alapú, metrika-vezérelt IDS riasztásaggregáció SOC környezetben |
| Beadási határidő | 2027-05-15, **16:00** (diplomaportál) |
| Most | **Diplomamunka II.** (2026/27. ősz): legalább 30–35 oldalas beszámoló a szorgalmi időszak utolsó napjáig (2026. december), 8 perces előadás a vizsgaidőszak 3. hetében. Részletek: `docs/diplomamunka-2.md` |
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

**A technológia (D12, 2026-10-01), három rétegben:**

1. **Mag – sima Python:** minden agent egy modul a `src/alertagg/`-ban, meghatározott bemenettel és
   kimenettel (dataclass vagy pydantic), LangGraph- és MCP-függőség nélkül. Az AIT-ADS-mérések
   közvetlenül ezen futnak, tömegesen (pandas), nem riasztásonként.
2. **Vezérlés – LangGraph:** az AIT-mérések után (kb. 8–9. hét, illetve a laborral együtt) a
   modulokat egy `StateGraph` csomópontjaiként kötjük be. Ide kerül a magyarázó agent (Ollama), és
   bizonyítani kell, hogy a vezérelt változat ugyanazt az eredményt adja, mint a mag.
3. **Csatlakozó – MCP (opcionális):** a laborban a gépnyilvántartást csak olvasható MCP-szolgáltatásként
   is elérhetővé tesszük a magyarázó modellnek. Ha kifut az idő, elhagyható.

A nyelvi modell soha nem dönti el a lépések sorrendjét, és nem ad pontszámot.

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

A Diplomamunka II.-höz:

- a kari szakdolgozat-készítési útmutató és az Overleaf-sablon forrása még nincs a tárolóban;
- a konzulens nevének alakja a leadandó fájlok nevében („Vorosne” vagy „BanatiBaumann”);
- a 2026/27. őszi félév pontos dátumai.

A konzulenssel még nem egyeztetett kérdések:

- jóváhagyja-e az irányt;
- elfogadja-e az „agent” meghatározásunkat;
- bevonhatók-e SOC-os kollégák a súlyozásba;
- hivatkozhatók-e a még nem lektorált arXiv-cikkek.

A keretrendszer kérdése eldőlt (D12, lásd a 3. pontot).

## 8. Munkaterv és a következő lépés

Az érvényes ütemterv (D13) a `docs/munkaterv.md` elején van: a Diplomamunka II. decemberi leadásáig
hetente egy-két fejezet és egy kódlépés. A tartalmi részletek: `docs/munkaterv-reszletes.md`. A
beszámoló fejezetvázlata: `docs/diplomamunka-2.md`.

**Most következik – 1. hét (okt. 5–11):**

1. Írás: a `thesis/` LaTeX-váza a kari sablonból (ehhez kell a sablon forrása és az útmutató),
   az 1. fejezet vázlata. A LaTeX-et minden munkamenetben telepíteni kell (Ubuntu-csomagból).
2. Kód: `python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`, a két
   letöltő szkript (ehhez a hálózati beállításban engedélyezni kell a `zenodo.org`-ot), majd
   adatfeltárás az `experiments/01_adatfeltaras.ipynb` notebookban:
   - mezők, riasztástípusok, időtartam;
   - az eredeti és a CATS-változat összevetése;
   - mely IP melyik géphez tartozik.
3. Ezután (2. hét) az **egységesítő agent** (`src/alertagg/normalizer.py`) a közös
   riasztásformával: idő, forrás- és cél-IP, gépnév, szabály, súlyosság, sérülékenység-hivatkozás,
   támadási technika. Teszttel igazoljuk, hogy a CATS-változatból és az eredetiből ugyanazok a riasztások jönnek ki.

## 9. Szabályok a tárolóban

- **Adat soha nem kerül a gitbe** (`data/` és `*.zip`/`*.jsonl` a `.gitignore`-ban). A CATS kódja sem.
- Minden fontos döntés új sort kap a `docs/dontesek.md`-ben, a régit nem töröljük.
- A tároló privát, a beadás után lesz publikus.
- Kódstílus: ruff (100 karakteres sorhossz), tesztek: pytest a `tests/` mappában.

## 10. Kapcsolódó anyagok a claude.ai-on

- „UNI - Diplomamunka” projekt (feladatlap, kutatási terv, kutatási jegyzetek, forrásjegyzék) – a korábbi Cowork-munka helye.
- A dolgozat Overleaf-projektje (a megosztási link a szerzőnél van, szerkesztési jogot ad, ezért nem kerül a tárolóba; innen a sablon forrását zipben kell ide hozni; a munkakörnyezetből az Overleaf nem érhető el).
- Kari tudnivalók és útmutató: https://nik.uni-obuda.hu/altalanos-tudnivalok/ · Diplomaportál: https://diploma.uni-obuda.hu/
- Konzulensi diasor: https://claude.ai/artifact/E7GeaF5VNKwYvBVX2cmcGr
- „Kutatási eredmények – döntések kutatási kérdésenként” (doksi): https://claude.ai/code/artifact/d0c6b0a6-6dc5-49ef-b30d-a26adc52479e – a tárolóban: `docs/kutatasi-eredmenyek.md`
- „AIT-ADS munkaterv” (doksi): https://claude.ai/code/artifact/8c2f6d55-6b09-431f-95d9-f4c3ffe84ceb – a tárolóban: `docs/munkaterv-reszletes.md`
- Forrásjegyzék: `thesis/references.bib` (61 tétel) és `thesis/forrasok.xlsx`.

# Kutatási eredmények – döntések kutatási kérdésenként

Sep 21, 2026 · @Csoza

## Összefoglaló

A dolgozat öt kutatási kérdésére a szakirodalom alapján az alábbi megoldásokat javaslom. Minden kérdésnél lejjebb egy táblázat hasonlítja össze a lehetőségeket, és megindokolja a választást.

| Kérdés | Javasolt megoldás | Fő indok |
| --- | --- | --- |
| 1. Milyen mérőszámokkal priorizáljunk? | A kockázatalapú riasztás-pontozás bevált mérőszámai, kiegészítve az eszköz fontosságával, a sérülékenységeivel és a megfigyeltségével | Az alapmódszer bizonyítottan működik, de az eszközökről szóló információt nem használja – ezt a rést tölti ki a dolgozat |
| 2. Hogyan tároljuk a környezetről szóló információt? | Egyszerű relációs adatbázisban (eszköznyilvántartás), a szoftverek szabványos azonosítójával összekötve a sérülékenységekkel | A Wazuh adataiból közvetlenül feltölthető, és egy prototípushoz átlátható |
| 3. Hogyan épüljenek fel az agentek? | Vegyes felépítés: a pontozást kiszámítható programrészek végzik, a nyelvi modell csak magyarázatot ír | Megismételhető eredményt ad, és a friss szakirodalom is így kezeli a nyelvi modell tévedéseit |
| 4. Hogyan mérjük az elemzők terhelésének csökkenését? | A riasztások számának csökkenése, miközben legfeljebb 2% valós támadás csúszhat át; nyilvános adathalmazon és saját laborban | Így a csökkentés nem mehet a biztonság rovására |
| 5. Hogyan mérjük a rangsor pontosságát? | Rangsor-pontossági mérőszámok, lépésről lépésre bővített modellváltozatokkal | Megmutatja, melyik információforrás mennyit javít |

### Fogalmak

| Fogalom | Jelentése |
| --- | --- |
| SOC | Biztonsági műveleti központ, ahol az elemzők a riasztásokat kezelik |
| IDS | Behatolásérzékelő rendszer (itt: Suricata, Wazuh), ez adja a riasztásokat |
| Kockázatalapú riasztás-pontozás (RBA) | Minden riasztás kap egy pontszámot, és az azonos gépen rövid időn belül halmozódó riasztások pontszáma összeadódik; az elemző a legmagasabb pontszámúakkal kezd |
| Eszköznyilvántartás (CMDB) | Adatbázis a hálózat gépeiről: szerepük, fontosságuk, futó szoftvereik |
| Szoftver-azonosító (CPE) | Szabványos név egy szoftververzióra; ezzel köthető össze a gép és a rá vonatkozó sérülékenység |
| Sérülékenység-azonosító (CVE) és súlyossága (CVSS) | Egy ismert szoftverhiba nyilvános azonosítója, illetve 0–10-es súlyossági pontszáma |
| Páros összehasonlításos súlyozás (AHP) | A szakértő mindig két szempontot hasonlít össze („melyik fontosabb és mennyivel”), ebből számolódnak a súlyok |
| Nagy nyelvi modell (LLM) | Szöveget író mesterséges intelligencia; itt a helyben futó Ollama |
| Elszalasztott támadások aránya (FNR) | A valós támadásokhoz tartozó riasztások hány százaléka kerül hátra vagy tűnik el |
| Rangsor-pontosság (AUROC) | 0,5 = véletlen sorrend, 1 = minden valós riasztás a lista elején |
| Átlagos pontosság (AP) | Mint az előző, de jobban bünteti, ha a lista legelején téves riasztás áll |
| Ablációs vizsgálat | A modellt lépésenként bővítjük, és minden lépés után mérünk – így látszik, mi mennyit ér |
| Baseline | Viszonyítási alap: egy egyszerűbb módszer, amelyhez képest a javulást mérjük |

## 1. Milyen mérőszámok alkalmasak a riasztások csoportosítására és rangsorolására?

**Javaslat:** a kockázatalapú riasztás-pontozás bevált mérőszámai (a riasztás súlyossága, az azonos gépen halmozódó riasztások száma és változatossága). Ezeket három új szemponttal egészítjük ki: mennyire fontos az érintett gép, van-e rajta olyan sérülékenység, amelyet a támadás kihasználhat, és mennyire figyeljük a gépet. A szempontok csoportosítását Jalalvand et al. (2024) rendszerezése adja.

### Melyik mérőszám-készlet?

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| Csak a riasztás saját súlyossága | Egyszerű, minden rendszerben megvan | Gyenge rangsor (rangsor-pontosság kb. 0,72); a környezetet nem veszi figyelembe | Uetz 2026 | Viszonyítási alap |
| Kockázatalapú pontozás (súlyosság + halmozódás + változatosság) | Átlátható, nem kell hozzá tanítóadat, rangsor-pontossága kb. 0,92 nyolc adathalmazon | A gépek fontosságát és sérülékenységeit nem nézi; a „ritka riasztás” szempont nem jobb a véletlennél | Uetz 2026 | Alap, egyben erős viszonyítási pont |
| Gépi tanulással kitanított jellemzők | Nagy pontosság érhető el | Sok felcímkézett riasztás kell, idővel romlik, nehezen magyarázható | Wang 2024; van Ede 2022; Arp 2022 | Nem választott, csak összevetéshez |
| **Kockázatalapú pontozás + gép fontossága + sérülékenység + megfigyeltség** | Lefedi a feladatlap infrastrukturális, kockázati és monitorozási szempontjait; a szakirodalom rését tölti ki | Fel kell építeni a gépek és sérülékenységek nyilvántartását | Jalalvand 2024; Porras 2002; Njogu 2012; Anuar 2012 | **Választott** |

### Hogyan legyen a mérőszámokból egyetlen pontszám?

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| **Súlyozott összeg, a súlyok páros összehasonlításból (AHP)** | Átlátható és megismételhető; a súlyokat SOC-os kollégák véleménye alapján lehet beállítani | A súlyok szubjektívek, ellenőrizni kell, hogy a válaszok következetesek-e | Anuar 2012; Jalalvand 2024 | **Választott** |
| Fuzzy logika („részben igaz” szabályok) | Jól kezeli a bizonytalanságot | Sok beállítandó paraméter, nehezebb megindokolni | Alsubhi 2008, 2011 | Továbbfejlesztési lehetőség |
| Gépi tanulás | Alkalmazkodik az adatokhoz | Tanítóadat kell, és könnyű torzított eredményt kapni | Wang 2024; Arp 2022 | Nem választott |
| A nyelvi modell adja a pontszámot | Rugalmas | Nem megismételhető, tévedhet („hallucinál”) | Vallabhaneni 2026; Wei 2025 | Nem választott |

**Miért ez?** Minden mérőszámnak van szakirodalmi előzménye, ezért a címben szereplő „metrika-vezérelt” jelző megalapozott. Mivel a kockázatalapú pontozás az alap, közvetlenül mérhető lesz, mennyit tesznek hozzá az új szempontok.

## 2. Hogyan ábrázolható a környezetről szóló információ (infrastruktúra és biztonság)?

**Javaslat:** egyszerű relációs adatbázis néhány táblával: gépek, rajtuk futó szolgáltatások, ismert sérülékenységek, megfigyeltség, valamint az, hogy melyik riasztási szabály melyik sérülékenységhez tartozik. A gépet és a sérülékenységet a szoftver szabványos azonosítója (CPE) köti össze. A riasztások csoportosításához külön riasztás-gráfot használunk: azok a riasztások kerülnek egy csoportba, amelyekben ugyanaz az IP-cím vagy felhasználó szerepel.

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| **Relációs adatbázis (SQL)** | A Wazuh gépleltara és sérülékenység-keresője közvetlenül betölthető; egyszerű, gyors, átlátható | Több lépésen átívelő kapcsolatokat (sérülékenység → hibatípus → támadási technika) nehezebb lekérdezni | Anuar 2012; Njogu 2012; Shi 2024 | **Választott** |
| Tudásgráf (pl. Neo4j) | Gazdag kapcsolatrendszer, külső tudásbázisok beköthetők | Egy prototípushoz túl nagy; több karbantartás | Kiesling 2019; Sikos 2023 | Továbbfejlesztési lehetőség |
| Riasztás-gráf közös IP-cím vagy felhasználó alapján | Az AIT-ADS adathalmazon tisztább csoportokat ad, mint a pusztán időablakos csoportosítás | A gépek fontosságáról nem mond semmit, csak a riasztások kapcsolatáról | Eckhoff 2025 | **Választott a csoportosításhoz** |
| Szabványos biztonsági adatformátum (OCSF, STIX) | Más rendszerekkel könnyen összeköthető | Nagy és bonyolult; kevés rá épülő kutatás | – | Csak a mezőnevekhez mintának |

### Mit kezdjünk a sérülékenységi információval?

A kérdés: ha a riasztás egy olyan támadást jelez, amely a célgépen nem működhet (mert nincs rajta az érintett szoftver), akkor mi történjen vele?

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| Kiszűrjük, az elemző nem látja | Nagyon sok riasztás eltűnik | Ha a nyilvántartás hiányos, valós támadás is elveszhet | Njogu 2012; Sommestad & Franke 2015 | Nem választott |
| **Pontot vonunk le, de a riasztás megmarad** (egyezés esetén teljes pont, csak termék-egyezésnél fél, egyébként nulla) | A riasztás csak hátrébb kerül, nem vész el | Kisebb a riasztásszám-csökkenés | Kruegel 2004; Valeur 2004 | **Választott** |

**Miért ez?** Az adatbázis a homelab Wazuh-adataiból és az AIT-ADS-hez tartozó hálózatleírásból is felépíthető. Utóbbiban ismertek a hálózati zónák, a szoftververziók és a kihasznált WordPress-bővítmény-hiba. A pontlevonás véd a szűrés ismert gyengesége, az átcsúszó támadások ellen.

## 3. Hogyan alkalmazható agent-alapú feldolgozás?

**Javaslat:** vegyes felépítés hét, egy-egy feladatra szakosodott agenttel. A mérőszámokat és a pontszámot kiszámítható programrészek számolják, amelyek ugyanarra a bemenetre mindig ugyanazt adják. A nyelvi modell (a helyben futó Ollama) csak rövid magyarázatot ír, amit egy ellenőrző lépés átnéz. A dolgozatban az „agent” önálló feldolgozó egységet jelent, saját bemenettel, feladattal és kimenettel. A nyelvi modell ennek csak az egyik lehetséges megvalósítása.

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| Egyetlen program minden lépéssel | Egyszerű | Nem felel meg a feladatlap „agent-alapú” követelményének; nehezen bővíthető | – | Nem választott |
| Klasszikus többagentes rendszer (nyelvi modell nélkül) | Kiforrott behatolásérzékelési szakirodalom, témában közel áll | Régebbi források, a mai nyelvi modellek lehetőségeit nem használja | Yu 2005; Taha 2010; Bougueroua 2021 | Elméleti alap |
| Csak nyelvi modellekből álló agentek (a döntést is ők hozzák) | Pontosabb, mint egyetlen nyelvi modell | Kb. 5,7-szer több számítás és 3,4-szer lassabb; tévedhet; nem megismételhető | Wei 2025; Hmimou 2025 | Nem választott |
| **Vegyes: kiszámítható döntés + nyelvi modelles magyarázat ellenőrzéssel** | Megismételhető, olcsó, visszakövethető; a 2026-os szakirodalom is ezt az irányt követi | A nyelvi modell kisebb szerepet kap | Vallabhaneni 2026; Roy 2026; Abdennebi 2026 | **Választott** |

### Az agentek feladatai

| Agent | Feladata | Milyen információval dolgozik | Működése |
| --- | --- | --- | --- |
| Egységesítő | A Suricata- és Wazuh-riasztásokat közös formára hozza | A nyers riasztások | Kiszámítható |
| Csoportosító | Összefogja az összetartozó riasztásokat | Közös IP-cím vagy felhasználó, időbeli közelség, ismétlődés | Kiszámítható |
| Környezet-agent | Kikeresi az érintett gép adatait | Gép fontossága, hálózati zónája, megfigyeltsége | Kiszámítható |
| Sérülékenységi agent | Megnézi, működhet-e a támadás azon a gépen | A gép ismert sérülékenységei és azok súlyossága | Kiszámítható |
| Rangsoroló | Kiszámolja a végső pontszámot | Az összes fenti információ, a súlyokkal | Kiszámítható |
| Magyarázó | Rövid szöveges összefoglalót ír a csoportról | A csoport és a pontszám | Nyelvi modell + ellenőrzés |
| Vezérlő | Sorba rendezi a lépéseket, naplóz, időt mér | – | Kiszámítható |

**Miért ez?** A vegyes felépítés teljesíti a feladatlap agent-alapú követelményét, mégis megismételhető mérést ad. Nyitott még, milyen technológiával valósulnak meg az agentek: külön Python-szolgáltatásként vagy egy agent-keretrendszerrel.

## 4. Mennyivel csökken az elemzők riasztási terhelése?

**Javaslat:** azt mérjük, hány százalékkal kevesebb tétel kerül az elemző elé. Feltétel, hogy a valós támadásokhoz tartozó riasztásoknak legfeljebb 2%-a csúszhat hátra vagy tűnhet el. Emellett megbecsüljük, mennyi elemzői idő spórolható meg. A mérés két helyen történik: egy nyilvános adathalmazon (AIT-ADS) és a saját laborban.

### Hogyan mérjük a terhelést?

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| Csak a riasztások számának csökkenése | Egyszerű és összevethető | Önmagában félrevezető: ha mindent eldobunk, az is „csökkenés” | Landauer 2022 | Részben |
| **Riasztásszám-csökkenés legfeljebb 2% elszalasztott támadás mellett, plusz becsült elemzői idő** | A csökkenés árát (az elszalasztott támadásokat) is méri; az időbecslés összevethető a csapat kapacitásával | Az egy riasztásra jutó kezelési idő feltételezés, forrással kell alátámasztani | Ndichu 2026; Shah 2019 | **Választott** |
| Elemzők kikérdezése szabványos terhelési kérdőívvel (NASA-TLX) | A tényleges terhelést méri | Sok résztvevő és idő kell hozzá | Ndichu 2026; Tariq 2025 | Opcionális, néhány SOC-os kollégával |

### Milyen adatokon mérjünk?

| Adathalmaz | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| **AIT-ADS (az osztrák AIT intézet nyilvános riasztás-adathalmaza)** | Suricata- és Wazuh-riasztások (kb. 2,6 millió), 8 forgatókönyv, a támadási lépések felcímkézve; az összehasonlítási alapul szolgáló pontozást is ezen mérték | Nincs hozzá gépnyilvántartás, a leírásból kell összeállítani | Landauer 2024; Uetz 2026 | **Választott – külső ellenőrzéshez** |
| **Saját homelab** | Minden környezeti adat a kezünkben van; pontosan tudjuk, mikor mi volt támadás | A háttérforgalom mesterséges | – | **Választott – saját kísérlethez** |
| AIT-ADS zajjal kiegészített változata | Megmutatja, bírja-e a módszer a sok téves riasztást | Még nem lektorált, csak a csoportok vannak felcímkézve | Karner 2026 | Opcionális |
| További tesztkörnyezetek adatai (SOCBED, DEDALE, APT29) | Jobban általánosítható eredmény | Más riasztórendszerek, rövid felvételek | Uetz 2026; Bönninghausen 2024 | Opcionális |
| Régi, hálózati forgalom-adathalmazok (CIC-IDS, DARPA) | Sokan ismerik | Elavultak, vagy nem riasztásokat, hanem forgalmat tartalmaznak | Landauer 2024 kritikája | Nem választott |

**Miért ez?** A két mérési hely együtt ad összevethetőséget a szakirodalommal és teljes kontrollt a saját környezetben. A 2%-os korlát miatt a terheléscsökkenés nem mehet a biztonság rovására.

## 5. Hogyan változik a riasztások relevanciája és a rangsor pontossága?

**Javaslat:** olyan mérőszámokat használunk, amelyek az egész rangsort értékelik, nem csak egy vágási pontot: rangsor-pontosság (AUROC) és átlagos pontosság (AP). Melléjük egy szemléletes számot is adunk: a lista első 10%-ában hány valós riasztás van. A modellt lépésről lépésre bővítjük, és minden lépés után mérünk.

### Mérőszámok

| Lehetőség | Mellette | Ellene | Forrás | Döntés |
| --- | --- | --- | --- | --- |
| Találati pontosság egyetlen vágási pontnál (F1) | Ismert | Csak egy adott csapatméretet modellez | Uetz 2026 | Nem választott |
| **Rangsor-pontosság (AUROC) és átlagos pontosság (AP)** | Minden lehetséges vágási pontot lefed; az átlagos pontosság külön bünteti a lista elején álló téves riasztást | Kevésbé szemléletes | Uetz 2026 | **Választott** |
| **Valós riasztások aránya a lista első 10%-ában** | Szemléletes: „ha az elemző csak a lista elejét tudja megnézni” | Egyetlen pont | Uetz 2026; Ndichu 2026 | **Választott** |
| A csoportok tisztasága (egy csoportban csak egy támadási lépés riasztásai vannak-e) | A csoportosítás pontosságát méri | Csak a csoportosításról szól | Eckhoff 2025; Karner 2026 | **Választott a csoportosításhoz** |

### A lépésenkénti bővítés sorrendje

| Lépés | Mit rangsorolunk | Mit mutat meg |
| --- | --- | --- |
| 0 | Nyers riasztások, rangsor nélkül | A kiindulási terhelést |
| 1 | Csak a riasztás súlyossága szerint | A mai gyakorlatot |
| 2 | Csoportosítás időablak vagy közös IP-cím alapján | Mennyit ér a csoportosítás önmagában |
| 3 | Kockázatalapú pontozás (Uetz 2026 nyilvános eszköze) | Az erős, környezetet nem ismerő viszonyítási alapot |
| 4 | 3. lépés + a gépek fontossága | Mennyit hoz a gépnyilvántartás |
| 5 | 4. lépés + sérülékenységek | Mennyit hoz a sérülékenységi információ |
| 6 | 5. lépés + megfigyeltség | A teljes modell eredményét |

**Miért ez?** A lépésenkénti bővítés egyszerre válaszol az 1. kérdésre (melyik mérőszám mennyit ér) és az 5. kérdésre. A gyakori módszertani hibákat Arp et al. (2022) foglalja össze, ilyen például, ha a tesztadat beleszivárog a beállításba, vagy ha csak laborban értékelünk.

## Nyitott kérdések és források

- [x] Elfogadja-e a konzulens a dolgozat irányát: mennyit javít a környezeti információ a kockázatalapú pontozáshoz képest?
- [x] Megfelel-e az általános „agent” definíció?
- [ ] A súlyok beállításához bevonhatók-e SOC-os kollégák egy rövid páros összehasonlító kérdőívvel?
- [ ] Mennyire hivatkozhatók a még nem lektorált, arXiv-on megjelent cikkek (LanG, CORTEX, Uetz 2026)?
- [ ] Milyen technológiával készüljenek az agentek: külön Python-szolgáltatásokként vagy egy agent-keretrendszerrel (pl. LangGraph)?

**Kulcsforrások:**

- [Uetz et al. 2026 – Can Risk-Based Alerting Mitigate Cybersecurity Alert Fatigue?](https://arxiv.org/abs/2609.02465)
- [Jalalvand et al. 2024 – Alert Prioritisation in SOCs (ACM CSUR)](https://doi.org/10.1145/3695462)
- [Tariq et al. 2025 – Alert Fatigue in SOCs (ACM CSUR)](https://doi.org/10.1145/3723158)
- [Landauer et al. 2024 – AIT Alert Data Set (CSET)](https://doi.org/10.1145/3675741.3675748)
- [Anuar et al. 2012 – AHP Risk Index Model](https://doi.org/10.1002/sec.673)
- [Eckhoff et al. 2025 – Graph-Based Alert Contextualisation](https://doi.org/10.1007/978-3-032-08124-7_24)
- [Wei et al. 2025 – CORTEX](https://arxiv.org/abs/2510.00311)
- [Sommestad & Franke 2015 – Alert filtering based on network information](https://doi.org/10.1002/sec.1173)

A teljes, 61 tételes lista a projektben található (forrasok.bib és Diplomamunka\_forrasok.xlsx), a részletes indoklás pedig a négy kutatási jegyzetben.

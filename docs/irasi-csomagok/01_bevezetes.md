# Írási csomag – 1. fejezet: Bevezetés

2026-10-01, bővítve 2026-10-07-én (a szerző kérésére, D19).

> **Fontos (D16, D19):** ez **forrásjegyzet és gondolatébresztő**, nem a dolgozat szövege. A mondatokat
> Claude írta, ezért **egyetlen mondatot se másolj át, és ne is fogalmazz át szorosan** – a
> plágiumkereső és a hallgatói nyilatkozat miatt a fejezetet a saját gondolatmeneteddel, a saját
> szavaiddal kell megírnod. Olvasd el, gondold végig a kérdéseket, aztán csukd be a fájlt, és úgy írj.
> Egy forrásra csak akkor hivatkozz, ha a hivatkozott részt magad is elolvastad.

## Mit vár el az útmutató ettől a fejezettől

- Kari útmutató, 3. melléklet, 1. pont: *a megoldandó probléma megfogalmazása, felvétele, a dolgozat
  célja, felépítése*.
- Feladatlap: a probléma (riasztási terhelés a SOC-ban), a cél (agent-alapú, metrika-vezérelt
  riasztás-összevonás), a feladat (szakirodalom, tervezés, megvalósítás, értékelés).
- Terjedelem: a Diplomamunka II. beszámolóban kb. **3 oldal** (`docs/diplomamunka-2.md`), a végleges
  dolgozatban 4–5 oldal.

## A források ellenőrzöttsége

| Kulcs | Mi ellenőrizve, honnan | Állapot |
| --- | --- | --- |
| `uetz2026rba` | A teljes szöveg (alphaXiv, 2026-10-01) | **Ellenőrizve**, a számok a cikkből |
| `ndichu2026` | A cikk részletes összefoglalója (alphaXiv, 2026-10-07) | **Ellenőrizve** |
| `alahmadi2022` | A USENIX-oldal és az oxfordi kivonat (webes keresés, 2026-10-07) | **Ellenőrizve** (kivonat szintjén) |
| `tariq2025` | ACM DL-adatlap és Semantic Scholar (webes keresés, 2026-10-07): Tariq, Baruwal Chhetri, Nepal, Paris; ACM Computing Surveys 57(9), 224. cikk, 2025 | **Ellenőrizve** (kivonat szintjén) |
| `jalalvand2024` | Webes keresés (2026-10-07): Jalalvand, Baruwal Chhetri, Nepal, Paris; ACM Computing Surveys 57(2), 42:1–42:36, **2025** | Létezik; **a tartalmi számokat (89 cikk, 5 kategória) még nem ellenőriztem** |
| `kokulu2019` | Webes keresés (2026-10-07): ACM CCS 2019, 18 félig strukturált interjú | **Ellenőrizve** (kivonat szintjén) |
| `vielberth2020` | Webes keresés (2026-10-07): IEEE Access 8, 227756–227779 | **Ellenőrizve** (kivonat szintjén) |
| `hamornik2017` | Webes keresés (2026-10-07): a kötet (AISC 593, AHFE 2017) és az oldalszám (224–236) | Létezik; **a tartalmát nem tudtam ellenőrizni** – csak akkor használd, ha elolvastad |

„Kivonat szintjén”: a kivonatban és a kiadói adatlapon szereplő állításokat ellenőriztem, a teljes
szöveget nem. A pontos részleteket hivatkozás előtt nézd meg a cikkben.

## Javasolt felépítés (4 rész)

A részek témája javaslat; az alfejezetcímeket a saját szavaiddal add meg.

### 1. A probléma: a riasztások mennyisége és a riasztási fáradtság (kb. 1 oldal)

**1.1. Sok riasztás, kevés valós támadás.**
Az Uetz-cikk számai jól mutatják az arányokat ugyanazon az adathalmazon, amelyen te is mérni fogsz:
az AIT-ADS egyik forgatókönyvének Suricata-riasztásai közül 44 tartozik valós támadáshoz, 9 142 nem.
Ez kb. 0,5% – vagyis az elemző minden valós riasztásra kb. kétszáz továbbit is lát. A saját
adatfeltárásunk (`CLAUDE.md`, 4. pont) ugyanezt adta, ami jó jel: a te számaid és a cikké egyeznek.
Kérdés neked: a saját munkahelyi tapasztalatod alapján ez az arány túlzó, reális vagy optimista?
Ha írsz róla, jelöld, hogy saját tapasztalat – ez erős, hiteles motiváció lehet.

**1.2. Mit gondolnak erről maguk az elemzők? (`alahmadi2022`)**
Alahmadi és szerzőtársai 20 SOC-szakembert kérdeztek kérdőívvel, majd 21 szakemberrel mélyebb,
kvalitatív vizsgálatot végeztek a biztonsági eszközök riasztásainak minőségéről. Az érdekes
megállapítás az, hogy a „téves” riasztások nagy része valójában nem hibás észlelés: a szabály jól
működött, csak a kiváltó ok a szervezet szokásos, jóindulatú működése volt. Az ilyen riasztások
ellenőrzése fárasztó, és a szerzők szerint kiégéshez és eltompuláshoz vezet. Öt tulajdonságot
fogalmaznak meg, amelyekkel egy riasztás gyorsabban ellenőrizhető; ezek egyike, hogy legyen
**környezetfüggő** (contextual). Gondolkodj el: a te dolgozatod pontosan ezt a környezeti információt
adja hozzá a riasztáshoz – ez természetes híd lehet a probléma és a célkitűzés között.

**1.3. Miért alakul ki a riasztási fáradtság? (`tariq2025`)**
Tariq és szerzőtársai (ACM Computing Surveys, 2025) áttekintő cikkükben a riasztási fáradtság négy
fő okát azonosítják; a kiadói kivonat ezek közül kiemeli a képzett szakemberek hiányát, amely hosszú
munkaidőhöz és túlterheléshez vezet. A megoldásokat három nézőpontból rendezik: automatizálás,
az elemző munkájának kiegészítése, valamint ember és mesterséges intelligencia együttműködése.
A cikk ipari felméréseket is idéz (pl. hogy a SOC-csapatok jelentős része túlterheltnek érzi magát) –
ha ilyen számot használsz, nézd meg, melyik eredeti felmérésből származik, és jelöld, hogy a Tariq-cikk
idézi. Kérdés neked: a négy ok közül melyik jellemző leginkább arra a SOC-ra, ahol dolgozol, és melyikre
ad választ a te megoldásod?

**1.4. A SOC mint szervezet: nem csak technikai kérdés (`kokulu2019`, `vielberth2020`)**
Kokulu és szerzőtársai 18 interjút készítettek SOC-elemzőkkel és -vezetőkkel, és azt találták, hogy a
vezetők és az elemzők sok kérdésben másként látják a SOC működését; ez az eltérés a SOC hatékonyságát
veszélyezteti. Az elemzők panaszai között szerepel a gyenge minőségű fenyegetési információ és a hosszú
jelentések, naplók feldolgozása. Vielberth és szerzőtársai (IEEE Access, 2020) szisztematikus
áttekintésükben a SOC fő építőelemeit gyűjtik össze, és hiányként jelölik meg, hogy a kutatás külön
foglalkozik az emberrel és a technológiával, de keveset a kettőt összekötő folyamatokkal. Ez a te
dolgozatodnak érdekes keret lehet: a riasztás-rangsorolás éppen egy ilyen folyamat, amely a
technológia kimenetét az ember figyelméhez igazítja.

**1.5. Mi történik, ha nem kezeljük a problémát? (`ndichu2026`)**
Ndichu és szerzőtársai 2026-os áttekintése a riasztások szűrését, rangsorolását, összefűzését és
nyelvi modellekkel való kiegészítését vizsgálja, 119 forrás alapján. Leírják, hogy a túlterhelt elemzők
gyakran kerülőutakat választanak: általános elnyomó szabályokat vezetnek be, vagy kizárólag az
eszköz által adott súlyosságra hagyatkoznak – ezek pedig a támadó számára kihasználható vakfoltokat
hoznak létre. Azt is kimondják, hogy a csak súlyosság szerinti rangsorolás széles körben elégtelennek
számít. Kérdés neked: láttál már ilyen „vakon” elnyomott szabályt a gyakorlatban? Egy anonimizált,
általános példa (cégnév és részletek nélkül) sokat adhat a bevezetéshez.

**1.6. Hazai nézőpont (`hamornik2017`) – csak elolvasás után**
Hámornik és Krasznay a SOC-csapatok emberi tényezőit vizsgálta csapatszinten (AHFE 2017,
Springer-kötet). A tartalmát nem tudtam ellenőrizni, ezért erről nem írok összefoglalót. Ha hozzáférsz
(az egyetemi könyvtár Springer-előfizetésén keresztül valószínű), érdemes lehet egy mondatban utalni
rá, mert hazai szerzők munkája, és a konzulens is értékelheti. Ha nem olvastad el, hagyd ki.

### 2. A meglévő megoldások és a rés (kb. 0,5–1 oldal)

**2.1. A kockázatalapú riasztás-pontozás mint erős alap (`uetz2026rba`)**
Uetz és szerzőtársai a kockázatalapú riasztás-pontozást (risk-based alerting) folyamatos rangsorolási
feladatként fogalmazták újra, öt „kockázati hipotézisre” bontották (a szabály szintje, halmozódás,
változatosság, ritkaság, szabálytalanság), és ezeket CATS nevű eszközükben nyolc riasztás-adathalmazon
mérték. A legjobb kombináció átlagos rangsor-pontossága 0,92 (szórás 0,09), szemben a csak a szabály
súlyossága szerinti rangsor 0,72-es (szórás 0,21) értékével. Gyakorlati példájuk szerint, ha az
elemző csak a lista első 10%-át tudja átnézni, az AIT-ADS Suricata-riasztásainál a kockázatalapú
rangsor a 44 valós riasztásból 43-at a lista elejére tesz, a súlyosság szerinti rangsor átlagosan csak
28,6-ot. A szerzők maguk írják, hogy módszerük „erős összehasonlítási alap” a bonyolultabb (például
nyelvi modelles) megoldásokhoz – ez a te dolgozatod kiindulópontja.

**2.2. A rés: a környezet hiánya**
Az Uetz-féle öt hipotézis mind a riasztásokból magukból számolható: hányszor, milyen változatosan,
milyen ritkán jelez egy gép vagy szabály. Egyik sem kérdezi meg, hogy mennyire fontos az érintett gép,
vagy hogy egyáltalán működhet-e rajta a jelzett támadás. Ez a te kutatási réseden: a kérdés nem az,
hogy a környezeti információ „jó-e”, hanem hogy **mennyit tesz hozzá** egy már erős módszerhez.
Gondold végig, hogyan fogalmaznád meg ezt egyetlen kérdésben – ez lehet a dolgozat központi kérdése.

**2.3. A szakirodalom is számon tartja a környezeti szempontokat (`jalalvand2024`)**
Jalalvand és szerzőtársai (ACM Computing Surveys, 2025) a SOC-beli riasztás-rangsorolás szempontjait és
módszereit rendszerezik. A korábbi kutatási jegyzet (`kutatasi_jegyzet_01.md`) szerint öt csoportba
sorolják a szempontokat (elemző, riasztás, eszköz, szervezet, külső környezet), és az eszközhöz kötött
szempontok (pl. a gép fontossága, sérülékenysége) gyakoriak. **Ezeket a számokat még nem ellenőriztem**
– olvasd el a cikk megfelelő részét, mielőtt használod. Ha igaz, erős érv, hogy a gép fontossága és a
sérülékenység nem a te ötleted, hanem ismert szempont, amelynek a hozzáadott értékét viszont kevesen
mérték.

**2.4. Kevés a valósághű értékelés (`ndichu2026`)**
Ndichu és szerzőtársai a vizsgált 87 fő tanulmányból mindössze 9-et találtak, amely éles SOC-adaton
értékelt; a többség nyilvános tesztadathalmazon (65) vagy korlátozott szimuláción (13) mért. Azt is
kiemelik, hogy nincs olyan nyilvános adathalmaz, amely a rangsorolás értékeléséhez minden szükséges
információt (elemzői döntéseket, hosszabb időtávot) tartalmazna. Ez kétféleképpen is a dolgozatodhoz
kapcsolódik: indokolja, miért nyilvános adathalmazzal (AIT-ADS) kezdesz, és miért építesz mellé saját
labort. Kérdés neked: hogyan mutatod be őszintén, hogy a saját méréseid sem éles SOC-adaton készülnek?

### 3. A dolgozat célja és a kutatási kérdések (kb. 0,5–1 oldal)

**3.1. A cél a feladatlap szerint**
A feladatlap három dolgot kér: egy agent-alapú, metrika-vezérelt aggregációs modell **tervezését**,
**megvalósítását** és **értékelését**, infrastrukturális, kockázati és monitorozási szempontok
alapján. Érdemes a célt úgy megfogalmaznod, hogy a három szempont (infrastruktúra = a gép fontossága,
kockázat = sérülékenység, monitorozás = megfigyeltség) egyértelműen megjelenjen benne, mert a bíráló a
feladatlappal fogja összevetni. A „metrika-vezérelt” jelző azt ígéri, hogy a döntés mérőszámokon
alapul – ezt a célkitűzésben is érdemes kimondani. Kérdés neked: hogyan magyaráznád el egy nem
biztonsági szakembernek egy mondatban, mit csinál a rendszered?

**3.2. A kutatási kérdések**
Az öt kérdés (mérőszámok; a környezet ábrázolása; agent-alapú felépítés; a terhelés csökkenése; a rangsor
minősége) a `docs/kutatasi-eredmenyek.md` elején van. A bevezetésben elég felsorolni őket, a válaszok a
későbbi fejezetekbe tartoznak. Figyelj rá, hogy a kérdések mérhetők legyenek: „mennyivel javul…”,
„milyen mérőszámmal…”. A Diplomamunka II.-ben a kérdésekre még csak a tervet adod meg, a mért választ a
III. félévben – ezt egy mondatban érdemes jelezni.

**3.3. Lehatárolás: mit nem vállal a dolgozat**
Segít a bírálónak, ha kimondod, mi nincs a dolgozatban: nem új behatolásérzékelőt fejlesztesz, nem gépi
tanulásos osztályozót tanítasz, és a nyelvi modell nem dönt és nem ad pontszámot, csak magyaráz (D3,
D12). Az utóbbit a szakirodalom is alátámasztja: a kis, helyben futó nyelvi modellek a vizsgálati lépések
levezénylésében megbízhatatlanok (`liu2026hesp`, lásd `kutatasi_jegyzet_05.md`; ezt hivatkozás előtt
olvasd el). A lehatárolás nem gyengeség, hanem azt mutatja, hogy tudatosan választottad meg a kereteket.

### 4. A dolgozat felépítése (kb. 0,5 oldal)

**4.1. Fejezetenként egy-két tagmondat**
A `docs/diplomamunka-2.md` vázlata szerint sorold fel, mi következik: elméleti háttér, szakirodalmi
módszerek összehasonlítása, specifikáció, felépítés és eszközválasztás, tesztkörnyezet, értékelési terv,
első eredmények. A felsorolás akkor jó, ha a fejezetek logikai sorrendje is látszik belőle (elmélet →
mások megoldásai → saját megoldás → hogyan mérem). Ezt a részt érdemes utoljára megírni, amikor a
többi fejezet szerkezete már végleges. Egy egyszerű ábra (lent) itt sokat segíthet.

## Ábrajavaslatok ehhez a fejezethez

| Ábra | Mit mutat | Forrás az ábra alá |
| --- | --- | --- |
| A riasztások útja a SOC-ban | Suricata és Wazuh → riasztások → elemzői sor; jelölve, hol avatkozik be a dolgozat (összevonás, rangsorolás) | Saját ábra |
| A dolgozat felépítése | A fejezetek sorrendje és kapcsolata | Saját ábra |
| (opcionális) Rangsor-összevetés | A 2.1. pont példája oszlopdiagramon: a lista első 10%-ában talált valós riasztások (43 a 28,6-tal szemben) | „Forrás: [Uetz 2026] adatai alapján” |

Mindegyiket `thesis/img/`-be készíteném vektorgrafikusan (PDF), a te jóváhagyásod után.

## Figyelj rá

- **Rövidítések:** első előfordulásnál írd ki (pl. biztonsági műveleti központ, angolul Security
  Operations Center, SOC), és vedd fel az `acronyms.tex`-be.
- **Számokat csak forrással** (vagy „saját tapasztalat” jelöléssel). Ha egy cikk más felmérését idézi,
  jelöld, hogy közvetett forrás.
- **Angol forrásból vett gondolat:** saját szavaiddal, hivatkozással. Szó szerinti idézet csak
  `\enquote{…}`-val és hivatkozással; saját fordításnál jelöld: „(saját fordítás)”.
- **Hivatkozás LaTeX-ben:** `szöveg~\cite{uetz2026rba}`; több forrás: `\cite{tariq2025,ndichu2026}`.
- A `docs/` mappa szövegeit (ezt a jegyzetet is) Claude írta: forrásként használd, a megfogalmazást ne vedd át.

## Ha elkészültél

Töltsd fel a zipet (Overleaf: Menu → Download → Source). Átnézem, és a beszélgetésben jelzem: formai
hibák, hiányzó hivatkozás, rövidítés, ellentmondás a döntésnaplóval. A szövegedet nem írom át.

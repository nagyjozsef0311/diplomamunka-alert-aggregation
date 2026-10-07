# Írási csomag – 1. fejezet: Bevezetés (3. változat, D20)

2026-10-07. Átvehető szöveg a forrásoktól független, saját megfogalmazásban. A **szürke kódblokkok**
tartalma bemásolható a `chapters/1_Bevezetes.tex`-be, és szabadon átírható. A blokkok **alatti**
„Megjegyzés” sorok neked szólnak – azok ne kerüljenek a dolgozatba.

Feltételezett rövidítések az `acronyms.tex`-ben: SOC (Security Operations Center), SIEM (Security
Information and Event Management), IDS (Intrusion Detection System), RBA (Risk-Based Alerting).

## A források ellenőrzöttsége

| Kulcs | Állapot |
| --- | --- |
| `uetz2026rba` | Teljes szöveg alapján ellenőrizve (alphaXiv, 2026-10-01) |
| `ndichu2026` | Részletes összefoglaló alapján ellenőrizve (alphaXiv, 2026-10-07) |
| `alahmadi2022`, `tariq2025`, `kokulu2019`, `vielberth2020` | Kivonat és kiadói adatlap alapján ellenőrizve (2026-10-07) |
| `jalalvand2024` | A cikk létezik (ACM Computing Surveys 57(2), 2025); a tartalmát csak általánosan használjuk |

---

## 1. Nyitó bekezdés (a fejezetcím alatt, alfejezet előtt)

```latex
A szervezetek informatikai védelmében a biztonsági műveleti központok -- angolul \ac{SOC} -- töltenek be
kulcsszerepet: ide fut be a hálózatból és a végpontokról érkező biztonsági események jelentős része,
és itt döntik el az elemzők, melyik eseménnyel kell foglalkozni.
Az események gyűjtését és egységes kezelését jellemzően egy \ac{SIEM} rendszer végzi, amely a
különböző forrásokból érkező naplókat és riasztásokat egy helyen teszi kereshetővé.
A riasztások egyik legfontosabb forrását a behatolásérzékelő rendszerek -- angolul \ac{IDS} -- adják.
Ezeknek két fő típusa van: a hálózati forgalmat figyelő változat (a dolgozatban a Suricata) és az
egyes gépeken futó, a rendszer- és alkalmazásnaplókat elemző változat (a dolgozatban a Wazuh).
Mindkét típus jellemzően előre megírt szabályok és mintázatok alapján jelez, így nagy forgalmú
környezetben folyamatosan és nagy mennyiségben állít elő riasztásokat.
```

Megjegyzés: az első `\ac{IDS}` itt toldalék nélkül áll, utána már írhatod: `\ac{IDS}-ek`.

---

## 2. Alfejezet: a riasztások mennyisége és a riasztási fáradtság

```latex
\subsection{A riasztások mennyisége és a riasztási fáradtság}\label{sec:problema}

A riasztásoknak azonban csak kis része jelez valódi támadást.
A dolgozatban később használt nyilvános adathalmaz (AIT-ADS) egyik támadási forgatókönyvében például
a Suricata 9186 riasztásából mindössze 44 tartozott a támadáshoz, ami fél százaléknál is kevesebb~\cite{uetz2026rba}.
Ez azt jelenti, hogy egy elemzőnek minden valódi találatért nagyjából kétszáz további riasztást is
át kellene néznie.
```

Megjegyzés: ide jöhet egy-két mondat a saját SOC-os tapasztalatodról (pl. hogyan néz ki egy műszak
riasztási terhelése) – ezt csak te írhatod meg; jelöld, hogy saját tapasztalat.

```latex
Az elemzők nézőpontját Alahmadi és szerzőtársai kérdőíves és interjús vizsgálattal tárták fel~\cite{alahmadi2022}.
Eredményeik szerint a terhelés jelentős részét nem a hibásan működő szabályok okozzák, hanem az olyan
riasztások, amelyek technikailag helyesek, de a szervezet megszokott, ártalmatlan működése váltja ki őket.
Ezek kivizsgálása mégis az elemző idejét köti le, és a folyamatos ismétlődés hosszú távon az éberség
csökkenéséhez vezet.
A szerzők szerint a riasztások ellenőrzését többek között az gyorsítaná, ha a riasztás eleve
tartalmazná a környezetére vonatkozó információkat; ez a gondolat a jelen dolgozat egyik kiindulópontja.

Ezt a jelenséget nevezi a szakirodalom riasztási fáradtságnak.
Tariq és szerzőtársai áttekintése a kialakulását több, egymást erősítő tényezőre vezeti vissza,
amelyek közé tartozik a képzett szakemberek hiánya és az ebből fakadó tartós túlterhelés~\cite{tariq2025}.
A lehetséges megoldásokat aszerint csoportosítják, hogy a gép átveszi-e a feladatot, támogatja-e az
elemző munkáját, vagy a kettő együttműködik.

A túlterhelésnek biztonsági kockázata is van.
Ndichu és szerzőtársai áttekintése szerint a túlterhelt csapatok gyakran általános elnyomó
szabályokkal csökkentik a riasztások számát, vagy kizárólag az eszköz által megadott súlyosság
alapján döntenek; mindkét megoldás olyan vakfoltot hagy, amelyet egy támadó kihasználhat~\cite{ndichu2026}.
Ugyanez a munka rögzíti azt is, hogy a pusztán súlyosság szerinti sorrend nem elegendő a valódi
támadások kiemeléséhez.
A probléma ráadásul nem kizárólag technikai: interjús vizsgálatok szerint a SOC-vezetők és az
elemzők gyakran eltérően ítélik meg a munka nehézségeit~\cite{kokulu2019}, a szakirodalom pedig
kevés figyelmet fordít azokra a folyamatokra, amelyek az embert és az eszközöket összekötik~\cite{vielberth2020}.
```

Megjegyzés: az utolsó mondat (Kokulu, Vielberth) elhagyható, ha rövidíteni kell.

---

## 3. Alfejezet: a meglévő megoldások és a kutatási rés

```latex
\subsection{Meglévő megoldások és a kutatási rés}\label{sec:megoldasok}

A riasztások csoportosításának és rangsorolásának kiterjedt szakirodalma van, amelyet a 3. fejezet
tekint át részletesen.
Az egyik legerősebb, tanítóadatot nem igénylő megközelítés jelenleg a kockázatalapú
riasztás-pontozás (\ac{RBA}).
Uetz és szerzőtársai öt, a riasztásokból közvetlenül számolható szempontot -- a szabály súlyosságát,
a riasztások időbeli halmozódását, változatosságát, ritkaságát és szabálytalanságát -- súlyozva vontak
össze, és a módszert nyolc adathalmazon vizsgálták~\cite{uetz2026rba}.
A legjobb beállítás rangsor-pontossága (AUROC) átlagosan 0,92 volt, a csak súlyosság szerinti sorrendé 0,72.
Ez a mérőszám annak a valószínűségét adja meg, hogy egy véletlenszerűen választott valódi riasztás
a rangsorban egy téves riasztás elé kerül; az 1 tökéletes, a 0,5 véletlenszerű sorrendet jelent.
Ha például az elemző csak a lista első tizedét tudja átnézni, az AIT-ADS Suricata-riasztásai közül a
kockázatalapú sorrend a 44 valódi riasztásból 43-at ebbe a részbe helyezi, a súlyosság szerinti sorrend
átlagosan csak 28,6-ot.

Az \ac{RBA} szempontjai azonban kizárólag a riasztások folyamából származnak: azt mérik, milyen gyakran,
milyen változatosan és mennyire szokatlanul jelez egy gép vagy egy szabály.
Nem veszik figyelembe, mennyire fontos az érintett gép a szervezet számára, fut-e rajta olyan szoftver,
amelyet a jelzett támadás ténylegesen kihasználhat, és mennyire látják a gépet a megfigyelőeszközök.
A riasztás-rangsorolás szakirodalma ismeri és rendszerezi az ilyen környezeti szempontokat~\cite{jalalvand2024},
azt azonban kevés munka vizsgálja, hogy mennyit javítanak egy már erős, környezetet nem használó
módszerhez képest.
Ez a dolgozat kutatási rése.
Az értékelés módja azért is lényeges, mert a terület megoldásainak kis részét vizsgálták valós
működési körülmények között: egy friss áttekintés 87 tanulmányából mindössze 9 alapult éles SOC-adatokon~\cite{ndichu2026}.
```

Megjegyzés: a „kevés munka vizsgálja” állítást a 3. fejezetben a saját szakirodalmi áttekintésed
támasztja alá; ha ott mégis találsz ilyen munkát, ezt a mondatot igazítsd hozzá.

---

## 4. Alfejezet: a dolgozat célja és a kutatási kérdések

A célkitűzést (a mostani 19. sorod) a saját szavaiddal már jól megírtad – azt érdemes megtartani, a
`docs/atnezesek/01_bevezetes_2026-10-07.md` B) és D) pontjai szerint javítva. Kiegészítésnek a
kutatási kérdések:

```latex
A dolgozat a következő kérdésekre keres választ:
\begin{enumerate}
    \item Milyen mérőszámok alkalmasak az \ac{IDS}-riasztások csoportosításának és rangsorolásának
          támogatására, ha a riasztás saját jellemzői mellett az érintett gép fontosságát,
          sérülékenységeit és megfigyeltségét is figyelembe vesszük?
    \item Hogyan ábrázolható és kapcsolható a riasztásokhoz a környezetre vonatkozó információ?
    \item Hogyan valósítható meg a feldolgozás együttműködő agentekkel úgy, hogy az eredmény
          megismételhető maradjon?
    \item Mennyivel csökkenthető az elemzők elé kerülő tételek száma, ha a valódi támadásokhoz
          tartozó riasztásoknak legfeljebb 2\%-a kerülhet hátra?
    \item Mennyivel javul a rangsor minősége a kockázatalapú pontozáshoz képest a környezeti
          szempontok bevonásával?
\end{enumerate}
A Diplomamunka II. keretében a kérdésekhez tartozó módszertant és a mérések tervét mutatom be;
a mérési eredmények a megvalósítás után, a dolgozat későbbi fejezeteiben szerepelnek.
```

Megjegyzés: az utolsó mondat csak a Diplomamunka II. beszámolóba kell; a végleges dolgozatból törlendő.

---

## 5. Alfejezet: a dolgozat felépítése

```latex
\subsection{A dolgozat felépítése}\label{sec:felepites}

A 2. fejezet a behatolásérzékelő rendszerek és a biztonsági műveleti központok működését, valamint a
riasztási fáradtság hátterét mutatja be.
A 3. fejezet a riasztások csoportosítására és rangsorolására javasolt módszereket tekinti át és
hasonlítja össze.
A 4. fejezet a választott megközelítést indokolja, és részletesen ismerteti a mérőszámrendszert.
Az 5. fejezet az agent-alapú rendszer felépítését és a felhasznált eszközök kiválasztását írja le.
A 6. fejezet a tesztkörnyezetet, valamint a tesztelés és az értékelés módszertanát tárgyalja.
A 7. fejezet az első eredményeket és a további munka ütemezését foglalja össze.
```

Megjegyzés: a fejezetszámokat a végleges szerkezethez igazítsd (`docs/dolgozat-szerkezet.md`). Ha a
fejezetek `\label`-t kapnak a `main.tex`-ben, a számok helyett `\ref{...}` is írható – akkor maguktól frissülnek.

---

## Átvételkor figyelj

- A blokkokat nyugodtan írd át a saját stílusodra; minél többet igazítasz rajta, annál inkább a tiéd.
- A számokat és a hivatkozásokat ne változtasd meg (ellenőrzöttek).
- A „--” a LaTeX-ben gondolatjel (–); a `~` a hivatkozás előtti nem törhető szóköz.
- Az első `\ac{...}`-t ne tedd zárójelbe: a csomag maga tesz zárójelet, így dupla lenne. Ezért szerepel gondolatjelek között.

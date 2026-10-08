# Írási csomag – 2. fejezet: Az IDS és a SOC működése, kihívásai

2026-10-08 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Feladatlap:** F1 – az IDS és SOC rendszerek működésének és kihívásainak áttekintése.
- **Útmutató:** 2. pont – a probléma elemzése (elméleti háttér).
- **Diplomamunka II.:** 1. pont – az elméleti háttér elmélyítése. Terjedelem: kb. **6 oldal** (a végleges
  dolgozatban 8–10).
- **Fájl:** `chapters/2_IDS_es_SOC.tex`; a `main.tex`-ben a Bevezetés után:

```latex
\clearpage
\section{BEHATOLÁSÉRZÉKELÉS ÉS BIZTONSÁGI MŰVELETI KÖZPONTOK}\label{sec:ids-soc}
\input{chapters/2_IDS_es_SOC}
```

Megjegyzés: a fejezetcím munkacím, írd át nyugodtan (csupa nagybetűvel).

## Rövidítések, amelyek ebben a fejezetben kellenek (`acronyms.tex`)

```latex
\DeclareAcronym{IPS}{
  short = IPS,
  long  = Intrusion Prevention System
}
\DeclareAcronym{NIST}{
  short = NIST,
  long  = National Institute of Standards and Technology
}
```

Megjegyzés: a SOC, SIEM, IDS és RBA már az 1. fejezetből megvan.

## Források és ellenőrzöttségük

| Kulcs | Mire használjuk | Ellenőrzés (2026-10-08) |
| --- | --- | --- |
| `denning1987` | A behatolásérzékelés első általános modellje | Szerzői és könyvtári oldalak: IEEE TSE SE-13(2), 222–232. **A DOI-t nem sikerült megerősíteni, ezért kimaradt.** |
| `scarfone2007nist` | Az IDS-ek csoportosítása és a felismerési módszerek | NIST CSRC-oldal; a módszerek leírása a dokumentum másolataiból. **Nézd meg a CSRC-oldalon, hogy a dokumentum még érvényes-e** (egy forrás szerint 2022-ben visszavonták). |
| `axelsson2000` | Miért sok a téves riasztás (alapgyakoriság-hiba) | ACM TISSEC 3(3), 186–205, DOI 10.1145/357830.357849; a kivonat alapján |
| `strom2018attack` | A MITRE ATT\&CK tudásbázis | MITRE-oldal (MP180360R1, 2020-as átdolgozás) |
| `suricatadocs`, `wazuhrules` | A két eszköz működése | Hivatalos dokumentáció (OISF, illetve Wazuh) |
| `landauer2024aitads` | Az AIT-ADS adathalmaz | Korábban ellenőrizve |
| `vielberth2020`, `kokulu2019`, `alahmadi2022`, `tariq2025`, `ndichu2026` | SOC, elemzői munka, riasztási fáradtság | 2026-10-07-én ellenőrizve |
| `vermeer2023` | A hálózati szabályok kezelése a SOC-okban | ACM CCS 2023, 2770–2784; a kivonat alapján |
| `chhetri2024` | Ember és mesterséges intelligencia együttműködése | ACM TOIT 2024; a kivonat alapján |

---

## 2.1. A behatolásérzékelés alapjai

```latex
\subsection{A behatolásérzékelés alapjai}\label{sec:ids-alapok}

Behatolásérzékelésen azoknak az eseményeknek a megfigyelését és elemzését értjük, amelyek egy
informatikai rendszer biztonságának megsértésére utalhatnak.
A terület elméleti alapjait Denning 1987-ben megjelent modellje fektette le, amely a rendszer
naplóiból felhasználónként és erőforrásonként profilt épít, és a megszokottól eltérő működést
tekinti gyanúsnak~\cite{denning1987}.
A modell már akkor kimondta azt a gondolatot, amely ma is minden behatolásérzékelő alapja: a
támadás nyomot hagy a rendszer eseményeiben, és ez a nyom automatikusan kereshető.

Az amerikai szabványügyi intézet (\ac{NIST}) útmutatója a behatolásérzékelő rendszereket
elsősorban aszerint csoportosítja, hogy milyen eseményeket figyelnek és hová telepítik
őket~\cite{scarfone2007nist}.
A dolgozat szempontjából két csoport lényeges.
A \emph{hálózati} behatolásérzékelő a hálózati forgalmat figyeli egy vagy több megfigyelési ponton,
és a csomagok, illetve a kapcsolatok tartalmából következtet a támadásra.
A \emph{gépi} (host-alapú) behatolásérzékelő egy-egy gépen fut, és annak napló-, fájl- és
folyamatadataiból dolgozik.
A két típus kiegészíti egymást: a hálózati érzékelő a gépek közötti forgalmat látja, a gépi érzékelő
pedig azt is, ami a titkosított kapcsolatokon belül vagy magán a gépen történik.
Ha a rendszer a felismert támadást meg is tudja akadályozni, behatolásmegelőző rendszerről (\ac{IPS})
beszélünk.

Az útmutató három fő felismerési módszert különböztet meg~\cite{scarfone2007nist}.
A \emph{szignatúraalapú} felismerés az ismert támadások jellegzetes mintázatait keresi a
forgalomban vagy a naplókban; ismert támadásokra megbízható, de az új vagy álcázott változatokat
nem ismeri fel.
Az \emph{anomáliaalapú} felismerés egy tanulási időszak alatt felépített „normális” működéshez
hasonlítja a megfigyelt eseményeket, és a jelentős eltérést jelzi; elvben új támadásokat is
észrevehet, de a normális működés változása is riasztást okozhat.
A \emph{protokollállapot-elemzés} azt vizsgálja, hogy egy kommunikáció lépései megfelelnek-e a
protokoll elvárt viselkedésének.
A gyakorlatban a legtöbb termék több módszert is alkalmaz egyszerre.
```

Megjegyzés: a „gépi” helyett a „hosztalapú” is bevett; válassz egyet, és azt használd végig.

---

## 2.2. A dolgozatban vizsgált eszközök: Suricata és Wazuh

```latex
\subsection{A vizsgált eszközök: Suricata és Wazuh}\label{sec:eszkozok}

A dolgozat két, széles körben használt, nyílt forráskódú eszköz riasztásaival dolgozik.
A Suricata hálózati behatolásérzékelő és -megelőző rendszer, amelyet az Open Information Security
Foundation nevű nonprofit szervezet fejleszt~\cite{suricatadocs}.
Élő forgalmon és rögzített forgalmi fájlokon is futtatható; működése alapvetően szabályalapú, vagyis
a beállított szabálykészlet mintázataira illeszkedő forgalomra riasztást ad, emellett részletes
forgalmi naplót is készít.
Megfigyelő (passzív) és a forgalomba beépülő (aktív) módban is üzemeltethető.

A Wazuh gépi oldali biztonsági platform: a megfigyelt gépekre telepített ügynökök gyűjtik és
továbbítják a napló- és rendszeradatokat egy központi kiszolgálónak, amely szabályok alapján
riasztásokat állít elő.
Minden szabálynak van egy szintje, amely a riasztás súlyosságát fejezi ki: a legalacsonyabb szintű
események nem is jutnak el a felületre, a középső szintek a sikertelen bejelentkezésekhez és
hasonló, önmagukban ritkán veszélyes eseményekhez tartoznak, a legmagasabb szintek pedig nagy
valószínűséggel támadásra utalnak~\cite{wazuhrules}.
A Wazuh más forrásokból is képes riasztásokat fogadni; a dolgozatban használt nyilvános
adathalmazban (AIT-ADS) a Suricata riasztásai is a Wazuh-n keresztül kerültek
gyűjtésre~\cite{landauer2024aitads}.

A két eszköz eltérő módon fejezi ki a súlyosságot: a Suricata néhány prioritási fokozatot, a Wazuh
egy több fokozatú szintskálát használ.
Ahhoz, hogy a két forrás riasztásai közösen rangsorolhatók legyenek, ezeket közös skálára kell
hozni; ez a feladat a 4. fejezetben bemutatott egységesítő lépés egyik része.
```

Megjegyzések:
- A Suricata prioritási fokozatainak pontos számát (a szabályokban 1–4, a gyakorlatban 1–3 jellemző)
  nem ellenőriztem a dokumentációban, ezért a szöveg csak „néhány fokozatot” ír. Ha a dokumentációban
  megnézed, beírhatod a pontos értéket.
- A „4. fejezet” utalást igazítsd a végleges számozáshoz.

---

## 2.3. A biztonsági műveleti központ felépítése és a riasztások útja

```latex
\subsection{A biztonsági műveleti központ felépítése}\label{sec:soc}

A biztonsági műveleti központ a szervezet biztonsági eseményeinek folyamatos megfigyelésére,
kivizsgálására és kezelésére létrehozott egység.
Vielberth és szerzőtársai szisztematikus irodalmi áttekintésükben a \ac{SOC} működését három,
egymásra utalt terület -- az emberek, a folyamatok és a technológia -- együtteseként írják le, és
megállapítják, hogy a kutatások jellemzően az emberi és a technológiai oldallal foglalkoznak, a
kettőt összekötő folyamatokkal kevésbé~\cite{vielberth2020}.

A technológiai oldal központi eleme a \ac{SIEM}, amely a különböző érzékelők és rendszerek
eseményeit egységes formában tárolja, összekapcsolja és szabályok alapján riasztásokká alakítja.
Egy riasztás útja jellemzően a következő: az érzékelő (például a Suricata vagy a Wazuh) jelez, a
riasztás a \ac{SIEM}-be kerül, ott egy várakozási sorba áll, majd az elemző a sorból kiválasztja,
megvizsgálja és eldönti, hogy valódi incidensről vagy téves riasztásról van-e szó.
Ez az első szűrés a triázs, és a riasztási terhelés legnagyobb része itt jelentkezik.

A támadások leírásához és a riasztások egységes értelmezéséhez a \ac{SOC}-ok egyre gyakrabban
használják a MITRE ATT\&CK tudásbázist, amely valós megfigyelések alapján rendszerezi a támadók
céljait (taktikák) és az ezek eléréséhez használt módszereket (technikák)~\cite{strom2018attack}.
Ha egy riasztáshoz ismert a hozzá tartozó technika, az elemző könnyebben elhelyezi a támadás
folyamatában, és több riasztás összefüggése is jobban látszik.

Az emberi oldal legalább ilyen fontos.
Kokulu és szerzőtársai interjús vizsgálata szerint a \ac{SOC}-ok problémái jelentős részben nem
technikaiak: a vezetők és az elemzők gyakran eltérően ítélik meg, mi a hatékony működés, és ez az
eltérés rontja a központ teljesítményét~\cite{kokulu2019}.
```

Megjegyzés: ide illik egy **ábra a riasztások útjáról** (lásd lent). A „triázs” szó helyett
„elsődleges szűrés” is írható; ha a triázst használod, első előfordulásnál magyarázd meg.

---

## 2.4. Miért sok a téves riasztás?

```latex
\subsection{A téves riasztások okai}\label{sec:teves}

A téves riasztások nagy aránya nem csupán a rosszul beállított szabályok következménye, hanem a
feladat természetéből is adódik.
Axelsson az alapgyakoriság-hibára (base-rate fallacy) vezette vissza a jelenséget: mivel a
valódi támadások a teljes eseményforgalomhoz képest nagyon ritkák, egy érzékelő riasztásainak
nagy része akkor is téves lesz, ha az érzékelő önmagában pontosnak tűnik~\cite{axelsson2000}.
Ahhoz, hogy a riasztások többsége valódi legyen, a téves riasztási aránynak olyan alacsonynak kellene
lennie, amely a gyakorlatban alig érhető el.

A hatás egy egyszerű számpéldán is látható.
Ha tízezer eseményből egy támadás, és az érzékelő minden támadást észrevesz, de a többi esemény
egy százalékára is téves riasztást ad, akkor nagyjából száz riasztásból csak egy lesz valódi.
A riasztások mennyiségét tehát nem elég az érzékelő pontosításával csökkenteni; a már kiadott
riasztásokat is rangsorolni kell, hogy az elemző figyelme a valószínűleg valódiakra jusson.

A szabálykezelés is hozzájárul a problémához.
Vermeer és szerzőtársai hálózatmegfigyelést végző szakemberekkel készített interjúi szerint a
szabályok kezelését a szabályok pontossága, a riasztások összmennyisége és a téves riasztások
aránya egyszerre befolyásolja; a szerzők pontosabb szabályokat és a felismeréstől a
szabályfejlesztésig visszavezető, kifejezett visszacsatolást javasolnak~\cite{vermeer2023}.
Végül a téves riasztások egy része technikailag nem is hibás: a szabály helyesen működik, de a
kiváltó esemény a szervezet ártalmatlan, megszokott működéséből ered~\cite{alahmadi2022}.
Ezek megkülönböztetéséhez a riasztás önmagában kevés, a környezetre vonatkozó információ is kell.
```

Megjegyzés: a számpélda saját számítás (Bayes-tétel): 1 valódi riasztás áll szemben kb. 100 téves
riasztással (a 9999 ártalmatlan esemény 1%-a). Ha a pontos arányt is meg akarod adni:
1/(1+99,99) ≈ 1%. A dolgozatban nyugodtan levezetheted egy képlettel is (`\begin{equation}`).

---

## 2.5. A riasztási fáradtság és kezelésének irányai

```latex
\subsection{A riasztási fáradtság}\label{sec:faradtsag}

Riasztási fáradtságnak azt az állapotot nevezzük, amikor a riasztások mennyisége és ismétlődése
miatt az elemzők figyelme és döntéseik minősége tartósan csökken.
Tariq és szerzőtársai áttekintése szerint a jelenség több, egymást erősítő okra vezethető vissza,
amelyek között a szakemberhiány és a tartós túlterhelés is szerepel~\cite{tariq2025}.
A következmények biztonsági kockázatot is jelentenek: a túlterhelt csapatok gyakran általános
elnyomó szabályokkal vagy kizárólag a súlyosság alapján szűrnek, ami vakfoltokat hagy~\cite{ndichu2026}.

A kezelés lehetséges irányait Baruwal Chhetri és szerzőtársai három működési módba
rendezik~\cite{chhetri2024}.
Az \emph{automatizálás} a rutinszerű riasztásokat emberi beavatkozás nélkül kezeli, a
\emph{kiegészítés} az elemző döntését gyorsítja további információval, az \emph{együttműködés}
pedig az összetett, új típusú esetek közös feltárását jelenti.
A dolgozatban kialakított rendszer elsősorban a kiegészítés módjába illeszkedik: nem dönt az
elemző helyett, hanem a riasztásokat csoportosítja, rangsorolja és a környezetükre vonatkozó
információval egészíti ki.
```

---

## 2.6. Összegzés: a kihívásokból adódó követelmények

```latex
\subsection{A fejezet összegzése}\label{sec:ids-soc-osszegzes}

A fejezetben bemutatott kihívások közvetlenül meghatározzák, mit kell teljesítenie egy riasztásokat
összevonó és rangsoroló megoldásnak.
Ezeket \az{\ref{tab:kihivasok}}. táblázat foglalja össze.

\begin{table}[H]
    \centering
    \caption{A riasztáskezelés kihívásai és az ezekből adódó követelmények}
    \label{tab:kihivasok}
    \begin{tabular}{|p{4cm}|p{4.4cm}|p{4.8cm}|}
        \hline
        \textbf{Kihívás} & \textbf{Következmény} & \textbf{Követelmény a megoldással szemben} \\ \hline
        Sok riasztás, kevés valódi támadás & Az elemző ideje nagyrészt téves riasztásokra megy el & A valószínűleg valódi riasztások kerüljenek a lista elejére \\ \hline
        Ártalmatlan okú, de helyes riasztások & A riasztás önmagában nem dönti el, hogy veszélyes-e & A riasztás egészüljön ki a környezetére vonatkozó információval \\ \hline
        Két érzékelő eltérő formátummal és súlyossági skálával & A riasztások nem hasonlíthatók össze közvetlenül & Közös riasztásforma és közös súlyossági skála \\ \hline
        Összetartozó riasztások külön tételként & Egy támadás sok tételként jelenik meg & Az összetartozó riasztások csoportosítása \\ \hline
        Elnyomó szabályok, csak súlyosság szerinti szűrés & Vakfoltok, elveszett valódi riasztások & A riasztások ne tűnjenek el, csak hátrébb kerüljenek; a hátra kerülő valódi riasztások aránya legyen mérhető \\ \hline
        Az elemző felelőssége megmarad & Az automatikus döntés bizalmi és felelősségi kérdést vet fel & Átlátható, megismételhető pontszám és rövid magyarázat; a döntés az elemzőé \\ \hline
    \end{tabular}
\end{table}

A következő fejezet azt vizsgálja, hogy a szakirodalomban javasolt módszerek mennyiben teljesítik
ezeket a követelményeket.
```

Megjegyzés: a táblázat celláit nyugodtan igazítsd. Ha a táblázat túl széles, a `p{…cm}` értékeket
csökkentsd (összesen kb. 14–15 cm fér el a szövegtükörben).

---

## Ábrajavaslatok

| Ábra | Hova | Mit mutat |
| --- | --- | --- |
| A behatolásérzékelők csoportosítása | 2.1 | Hálózati és gépi típus × szignatúra-, anomália- és protokollállapot-alapú felismerés (Forrás: \cite{scarfone2007nist} alapján) |
| A riasztások útja a SOC-ban | 2.3 | Suricata és Wazuh → \ac{SIEM} → várakozási sor → elemző (triázs) → incidens vagy lezárás; jelölve, hol avatkozik be a dolgozat |

Mindkettőt elkészítem PDF-ben a `thesis/img/` mappába, ha kéred.

## Átvételkor figyelj

- A blokkokat a fenti sorrendben másold be a `2_IDS_es_SOC.tex`-be; átírhatod őket.
- A hivatkozási kulcsok és a számok ellenőrzöttek, ne változtasd meg őket.
- Az `ATT\&CK` írásmódban a `\&` kötelező.
- Terjedelem: a hat blokk együtt kb. 5–6 oldal a sablonban (ábrák nélkül).

# Írási csomag – 2. fejezet: Az IDS és a SOC működése, kihívásai

2026-10-08 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Feladatlap:** F1 – az IDS és SOC rendszerek működésének és kihívásainak áttekintése.
- **Útmutató:** 2. pont – a probléma elemzése (elméleti háttér).
- **Diplomamunka II.:** 1. pont – az elméleti háttér elmélyítése; 3. pont – hasonló megoldások
  (eszközök) összehasonlítása. Terjedelem: kb. **9–10 oldal** a két összehasonlító táblázattal.
- **2026-10-08, 2. változat:** a szerző kérésére külön alfejezet a behatolásérzékelő eszközökről (2.2)
  és a SIEM-eszközökről (2.3), összehasonlító táblázatokkal; a SOC-rész a szervezeti modellekkel bővült (2.4).
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
\DeclareAcronym{MSSP}{
  short = MSSP,
  long  = Managed Security Service Provider
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
| `suricatadocs`, `wazuhrules`, `zeekdocs`, `ossec`, `wazuhossec` | Az eszközök működése | Hivatalos dokumentációk és projektoldalak |
| `roesch1999snort` | A Snort | USENIX LISA '99, 229–238 |
| `paxson1999bro` | A Zeek (Bro) | Computer Networks 31(23–24), 2435–2463; **DOI nem található, kimaradt** |
| `shah2018snort` | Snort és Suricata összehasonlítása | FGCS 80, 157–170; a kivonat és az arXiv-változat alapján |
| `gonzalez2021siem` | A SIEM-ek áttekintése | Sensors 21(14), 4759, DOI 10.3390/s21144759; nyílt hozzáférésű |
| `knerler2022mitre` | SOC-szervezeti modellek | MITRE, 2022; a kivonat és másodlagos összefoglaló alapján |
| `splunkrba`, `sentinelkql`, `elasticsecurity` | SIEM-termékek jellemzői | Gyártói dokumentáció |
| `splunkmq2025`, `microsoftmq2025`, `googlemq2025` | A Gartner 2025-ös értékelése | A gyártók saját közleményei (a jelentés fizetős) |
| `ciscosplunk2024`, `paloaltoqradar` | A piac átrendeződése | Cisco befektetői közlemény; Palo Alto Networks oldala |
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

## 2.2. Behatolásérzékelő eszközök

```latex
\subsection{Behatolásérzékelő eszközök}\label{sec:ids-eszkozok}

A gyakorlatban használt behatolásérzékelő eszközök működési elvük és telepítési helyük alapján is
jelentősen eltérnek egymástól.
A következőkben a legelterjedtebb nyílt forráskódú eszközöket mutatom be, mert ezek működése
nyilvánosan dokumentált, és a kutatások is jellemzően ezekre épülnek; a kereskedelmi termékek egy
része ugyanezekre az alapokra épül.

\subsubsection{Hálózati eszközök}

A Snort az egyik első és legismertebb hálózati behatolásérzékelő.
Roesch 1999-ben könnyűsúlyú, szabályalapú eszközként mutatta be, amely egyszerű szabálynyelvvel írja
le a keresett forgalmi mintázatokat~\cite{roesch1999snort}.
Szabálynyelve a terület egyik alapjává vált: a később megjelent eszközök egy része is ehhez hasonló
szabályokat használ.

A Suricata ugyancsak szabályalapú hálózati behatolásérzékelő és -megelőző rendszer, amelyet az Open
Information Security Foundation nevű nonprofit szervezet fejleszt~\cite{suricatadocs}.
Szabálykészlete a Snortéhoz hasonló, a legfontosabb építészeti különbség pedig az volt, hogy a
Suricata kezdettől fogva több szálon dolgozza fel a forgalmat, míg a Snort hosszú ideig egyetlen
szálon~\cite{shah2018snort}.
Shah és Issac azonos hardveren, nagy sebességű forgalommal végzett összehasonlítása szerint a
Suricata nagyobb forgalmat tudott feldolgozni kevesebb csomagvesztéssel, ennek ára viszont a
nagyobb erőforrásigény volt~\cite{shah2018snort}.
A Suricata a riasztások mellett részletes forgalmi naplót is készít, és megfigyelő (passzív) és
a forgalomba beépülő (aktív) módban is üzemeltethető~\cite{suricatadocs}.

A Zeek (korábbi nevén Bro) eltérő megközelítést képvisel.
Paxson eredetileg valós idejű behatolásérzékelő rendszerként mutatta be~\cite{paxson1999bro}, a mai
változat azonban elsősorban hálózati forgalomelemző és -megfigyelő eszköz, amely nem klasszikus
szignatúraalapú behatolásérzékelő~\cite{zeekdocs}.
A forgalomból részletes, protokollonkénti naplókat készít, az elemzést pedig egy saját szkriptnyelven
írt programok végzik, így viselkedés- és anomáliaalapú vizsgálatokra is alkalmas.
A Zeek ezért inkább kiegészíti a szabályalapú eszközöket, mint helyettesíti őket.

\subsubsection{Gépi eszközök}

Az OSSEC nyílt forráskódú, gépi behatolásérzékelő rendszer, amely a naplóelemzést, a
fájlintegritás-figyelést és a rootkitek felismerését egyesíti, és ügynökkel, valamint ügynök nélkül
is képes gépeket megfigyelni~\cite{ossec}.
A Wazuh 2015-ben az OSSEC továbbfejlesztett változataként (forkjaként) indult, mert az eredeti projekt
fejlesztése lelassult~\cite{wazuhossec}.
Azóta a gépi felismerés mellett sérülékenység-felismeréssel, saját webes felülettel és a riasztások
központi gyűjtésével is bővült, így kisebb környezetekben a \ac{SIEM} szerepét is betölti.
A Wazuh szabályai súlyossági szinteket kapnak, amelyek a jelentéktelen eseményektől a nagy
valószínűséggel támadásra utaló riasztásokig terjednek~\cite{wazuhrules}.

\Az{\ref{tab:ids-eszkozok}}. táblázat összefoglalja a bemutatott eszközök fő tulajdonságait.

\begin{table}[H]
    \centering
    \caption{Elterjedt nyílt forráskódú behatolásérzékelő eszközök összehasonlítása}
    \label{tab:ids-eszkozok}
    \small
    \begin{tabular}{|L{1.7cm}|L{1.6cm}|L{3.4cm}|L{3.1cm}|L{3.1cm}|}
        \hline
        \textbf{Eszköz} & \textbf{Típus} & \textbf{Felismerési elv} & \textbf{Feldolgozás, kimenet} & \textbf{Megjegyzés} \\ \hline
        Snort & hálózati & szignatúra (szabályalapú) & riasztás; a régebbi változatok egyszálúak & az egyik első nyílt forráskódú hálózati eszköz \\ \hline
        Suricata & hálózati & szignatúra, protokollelemzés & többszálú; riasztás és forgalmi napló & a Snortéhoz hasonló szabálykészlet; passzív és aktív mód \\ \hline
        Zeek & hálózati & viselkedés- és anomáliaalapú szkriptek & protokollonkénti naplók & nem klasszikus szignatúraalapú eszköz; kiegészítő szerep \\ \hline
        OSSEC & gépi & naplóelemzés, fájlintegritás, rootkitfelismerés & ügynökös és ügynök nélküli megfigyelés & a Wazuh elődje \\ \hline
        Wazuh & gépi & szabályalapú naplóelemzés, sérülékenység-felismerés & ügynökök és központi kiszolgáló; súlyossági szintek & az OSSEC forkja; SIEM-funkciók \\ \hline
    \end{tabular}
\end{table}

A dolgozat a Suricata és a Wazuh riasztásaival dolgozik.
A két eszköz eltérő módon fejezi ki a súlyosságot, ezért a riasztásokat a közös rangsoroláshoz
egységes formára és közös súlyossági skálára kell hozni.
```

Megjegyzések:
- Forrás a táblázat alá nem kell külön, mert a szövegben minden állítás hivatkozva van; ha mégis
  szeretnéd: „Forrás: [Roesch], [Paxson], [Shah–Issac] és a dokumentációk alapján, saját összeállítás”.
- A Snort 3-as változata ma már többszálú; ezt csak másodlagos forrás erősítette meg, ezért a
  szöveg óvatosan fogalmaz („a régebbi változatok egyszálúak”). Ha a hivatalos Snort-dokumentációban
  megnézed, kiegészítheted.
- **Kereskedelmi termékek:** ha ezekről is szeretnél írni (pl. a Cisco Snort-alapú megelőző
  rendszere, a végpontvédelmi EDR-termékek), szólj, és ellenőrzött forrással kiegészítem.

---

## 2.3. SIEM-eszközök

```latex
\subsection{Biztonsági információ- és eseménykezelő rendszerek}\label{sec:siem}

A \ac{SIEM} a biztonsági műveleti központ legfontosabb eszköze: a különböző érzékelők, köztük a
behatolásérzékelők eseményeit egy központi platformon gyűjti, egységes formára hozza, összekapcsolja
és szabályok alapján riasztásokká alakítja~\cite{gonzalez2021siem}.
González-Granadillo és szerzőtársai áttekintése szerint a \ac{SIEM}-ek az egyszerű naplógyűjtőkből
átfogó rendszerekké fejlődtek, amelyek a kockázatos területek gyors felismerésével csökkentik az
incidensek kezelésének idejét, és egyre inkább összeolvadnak a nagy adatmennyiségek elemzésére
szolgáló platformokkal~\cite{gonzalez2021siem}.

A piacot néhány nagy szereplő uralja.
A Gartner piacelemző cég 2025-ös értékelésében vezető helyen szerepelt többek között a Splunk, a
Microsoft Sentinel és a Google Security Operations~\cite{splunkmq2025,microsoftmq2025,googlemq2025}.
A piac az utóbbi években jelentősen átrendeződött: a Splunkot 2024-ben felvásárolta a
Cisco~\cite{ciscosplunk2024}, az IBM pedig QRadar termékének felhőszolgáltatását a Palo Alto Networks
cégnek adta el, amely a felhőügyfeleket saját platformjára költöztette~\cite{paloaltoqradar}.

A termékek közötti különbségek közül a dolgozat szempontjából három lényeges: hol fut a rendszer
(saját infrastruktúrán vagy felhőben), milyen nyelven fogalmazhatók meg a lekérdezések és a
felismerési szabályok, és milyen eszközt kínál a riasztások rangsorolására.
A Microsoft Sentinel felhőalapú rendszer, amely adatait az Azure naplóelemző tárolójában tartja, és a
lekérdezésekhez, valamint a felismerési szabályokhoz a Kusto lekérdezőnyelvet használja~\cite{sentinelkql}.
Az Elastic Security az Elasticsearch keresőmotorra és a Kibana felületre épül, és egységes
adatsémát vár el a különböző forrásoktól~\cite{elasticsecurity}.
A Splunk Enterprise Security saját lekérdezőnyelvvel dolgozik, és beépített kockázatalapú riasztást
kínál: az egyes gyanús találatok nem önálló riasztásként jelennek meg, hanem kockázati pontszámként
gyűlnek az érintett eszközhöz vagy felhasználóhoz, és csak egy küszöb átlépésekor keletkezik belőlük
kivizsgálandó riasztás~\cite{splunkrba}.
A pontszám az eszközök és a felhasználók tulajdonságai alapján módosítható, vagyis a kereskedelmi
gyakorlatban a környezeti információ bevonása már megjelent~\cite{splunkrba}.

\Az{\ref{tab:siem-eszkozok}}. táblázat a jellemző \ac{SIEM}-eszközöket hasonlítja össze.

\begin{table}[H]
    \centering
    \caption{Elterjedt SIEM-eszközök összehasonlítása}
    \label{tab:siem-eszkozok}
    \small
    \begin{tabular}{|L{2.6cm}|L{2.6cm}|L{3.4cm}|L{4.2cm}|}
        \hline
        \textbf{Eszköz} & \textbf{Üzemeltetés} & \textbf{Lekérdezés, szabályok} & \textbf{Megjegyzés} \\ \hline
        Splunk Enterprise Security & saját infrastruktúra vagy felhő & saját lekérdezőnyelv & beépített kockázatalapú riasztás; 2024 óta a Cisco tulajdona \\ \hline
        Microsoft Sentinel & felhő (Azure) & Kusto lekérdezőnyelv & a Microsoft felhőszolgáltatásaihoz illeszkedik \\ \hline
        IBM QRadar & saját infrastruktúra & -- & a felhőszolgáltatás 2024-ben a Palo Alto Networkshöz került \\ \hline
        Elastic Security & saját infrastruktúra vagy felhő & Elasticsearch-alapú lekérdezések & egységes adatséma; nyílt fejlesztésű alapokra épül \\ \hline
        Wazuh & saját infrastruktúra & szabályalapú elemzés & nyílt forráskódú; gépi felismerés és SIEM-funkciók egy rendszerben \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzések:
- **A kutatási rés pontosítása:** a Splunk kockázatalapú riasztása már használ eszköz- és
  felhasználói adatokat. A dolgozat rése ezért így pontos: *a nyilvánosan, mérhetően értékelt
  kockázatalapú pontozás (Uetz és mtsai.) nem használja a környezetet, és nincs nyilvános mérés arról,
  mennyit ad hozzá.* Ezt a Bevezetésben és a 3. fejezetben is így érdemes megfogalmazni.
- A Gartner-értékelést a gyártók saját közleményei alapján hivatkozom (a jelentés maga fizetős). Ha
  hozzáférsz a jelentéshez (pl. egy gyártó ingyenes másolatán keresztül), cseréld arra a hivatkozást.
- A QRadar lekérdezőnyelvét nem ellenőriztem, ezért szerepel „--” a táblázatban.
- A „Splunk Enterprise Security … saját infrastruktúra vagy felhő” általános tudás, a Splunk felhős
  kiadása miatt; ha szigorúan forrással akarod, hagyd el a cellát.

---

## 2.4. A biztonsági műveleti központ felépítése és a riasztások útja

```latex
\subsection{A biztonsági műveleti központ felépítése}\label{sec:soc}

A biztonsági műveleti központ a szervezet biztonsági eseményeinek folyamatos megfigyelésére,
kivizsgálására és kezelésére létrehozott egység.
Vielberth és szerzőtársai szisztematikus irodalmi áttekintésükben a \ac{SOC} működését három,
egymásra utalt terület -- az emberek, a folyamatok és a technológia -- együtteseként írják le, és
megállapítják, hogy a kutatások jellemzően az emberi és a technológiai oldallal foglalkoznak, a
kettőt összekötő folyamatokkal kevésbé~\cite{vielberth2020}.

A \ac{SOC}-ok szervezeti felépítése is sokféle lehet.
Knerler és szerzőtársai a MITRE gyakorlati útmutatójában azt hangsúlyozzák, hogy nincs két egyformán
felépített \ac{SOC}: a szervezeti formát a kiszolgált szervezet mérete, a vállalt feladatok és a
szükséges rendelkezésre állás határozza meg~\cite{knerler2022mitre}.
A legfontosabb döntések a következők: a központ egy helyen, egységes irányítás alatt működik-e
(központosított), vagy a szervezet több részén elosztva; az elemzők feladatait szintekre bontják-e
(például elsődleges szűrés, mélyebb kivizsgálás), vagy szintek nélkül dolgoznak; és a feladatokat
saját munkatársak látják-e el, vagy részben vagy egészben külső szolgáltatóhoz kerülnek~\cite{knerler2022mitre}.
A külső, menedzselt biztonsági szolgáltatók (MSSP) egyszerre több ügyfél riasztásait kezelik, ezért
náluk a riasztási terhelés és a szabálykezelés különösen fontos kérdés~\cite{vermeer2023}.

A technológiai oldal központi eleme a \ac{SIEM}.
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

Megjegyzések:
- A szervezeti modellek (központosított, elosztott, szintekre bontott, kiszervezett) a MITRE-könyv 3.
  stratégiájából valók; a részleteket csak a könyv kivonatából és másodlagos összefoglalóból tudtam
  ellenőrizni. A könyv ingyenesen letölthető a MITRE oldaláról – ha belenézel, egy táblázatba is
  összefoglalhatjuk a modelleket (előnyök, hátrányok, kinek való).
- Az MSSP rövidítést első előfordulásnál vedd fel az `acronyms.tex`-be (Managed Security Service Provider).
- Ide illik az **ábra a riasztások útjáról**.

---

## 2.5. Miért sok a téves riasztás?

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

## 2.6. A riasztási fáradtság és kezelésének irányai

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

## 2.7. Összegzés: a kihívásokból adódó követelmények

```latex
\subsection{A fejezet összegzése}\label{sec:ids-soc-osszegzes}

A fejezetben bemutatott kihívások közvetlenül meghatározzák, mit kell teljesítenie egy riasztásokat
összevonó és rangsoroló megoldásnak.
Ezeket \az{\ref{tab:kihivasok}}. táblázat foglalja össze.

\begin{table}[H]
    \centering
    \caption{A riasztáskezelés kihívásai és az ezekből adódó követelmények}
    \label{tab:kihivasok}
    \begin{tabular}{|L{4cm}|L{4.4cm}|L{4.8cm}|}
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
| A riasztások útja a SOC-ban | 2.4 | Suricata és Wazuh → \ac{SIEM} → várakozási sor → elemző (triázs) → incidens vagy lezárás; jelölve, hol avatkozik be a dolgozat |

Mindkettőt elkészítem PDF-ben a `thesis/img/` mappába, ha kéred.

## Átvételkor figyelj

- A táblázatok `L{…}` oszlopai balra igazított, sortörő oszlopok; ehhez a v0.8-as `template.tex` kell.
- A blokkokat a fenti sorrendben másold be a `2_IDS_es_SOC.tex`-be; átírhatod őket.
- A hivatkozási kulcsok és a számok ellenőrzöttek, ne változtasd meg őket.
- Az `ATT\&CK` írásmódban a `\&` kötelező.
- Terjedelem: a hét blokk együtt kb. 9–10 oldal a sablonban (ábrák nélkül).

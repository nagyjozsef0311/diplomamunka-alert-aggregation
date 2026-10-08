# Írási csomag – 3. fejezet: A riasztások csoportosításának és rangsorolásának módszerei

2026-10-08 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Feladatlap:** F2 – a riasztásaggregáció és -priorizálás módszereinek áttekintése és összehasonlítása.
- **Útmutató:** 2. pont – a probléma elemzése, a meglévő megoldások kritikai értékelése.
- **Diplomamunka II.:** 2–3. pont – szakirodalom-kutatás és hasonló megoldások összehasonlítása.
  Ez a beszámoló **leghosszabb** fejezete: kb. **11–13 oldal** a négy táblázattal.
- **Vezérfonal (a szerző kérése):** minden módszercsaládnál külön kimondjuk a **gyengeséget**, és a
  fejezet végén táblázat mutatja, melyik rést melyik eleme tölti be a saját rendszernek.
- **Fájl:** `chapters/3_Modszerek.tex`; a `main.tex`-ben a 2. fejezet után:

```latex
\clearpage
\section{A RIASZTÁSOK CSOPORTOSÍTÁSA ÉS RANGSOROLÁSA}\label{sec:modszerek}
\input{chapters/3_Modszerek}
```

## Rövidítések, amelyek ebben a fejezetben kellenek (`acronyms.tex`)

```latex
\DeclareAcronym{AHP}{
  short = AHP,
  long  = Analytic Hierarchy Process
}
\DeclareAcronym{CVSS}{
  short = CVSS,
  long  = Common Vulnerability Scoring System
}
\DeclareAcronym{AUROC}{
  short = AUROC,
  long  = Area Under the Receiver Operating Characteristic Curve
}
\DeclareAcronym{MCP}{
  short = MCP,
  long  = Model Context Protocol
}
\DeclareAcronym{RAG}{
  short = RAG,
  long  = Retrieval-Augmented Generation
}
```

Megjegyzés: az LLM már az 1. fejezetből megvan. Ha az AUROC-ot az 1. fejezetben is `\ac{}`-vel
használod, az első előfordulás ott lesz – ez így rendben van.

## Források és ellenőrzöttségük

| Kulcs | Mire használjuk | Ellenőrzés |
| --- | --- | --- |
| `valeur2004` | A feldolgozás lépései (összetevő-alapú modell) | TDSC 1(3), 2004; kivonat, korábban ellenőrizve |
| `salah2013`, `sadoddin2006`, `kotenko2022`, `mirheidari2013` | Áttekintések a korrelációs módszerekről | Kiadói adatlap; csak a csoportosításukat használjuk |
| `julisch2003` | Ok-feltárás csoportosítással | Kivonat: néhány tucat kiváltó ok adja a riasztások több mint 90%-át |
| `landauer2022` | Tartományfüggetlen csoportosítás | Kivonat (2026-10-08): kb. 80%-kal kevesebb csoport; a csoportokhoz rendelt osztályozók kb. 80% találati arány, 5% alatti téves riasztás |
| `karner2026alertbert` | Nyelvi modellel támogatott csoportosítás | arXiv:2602.06534, teljes szöveg alapján (2026-10-08 előtt) |
| `eckhoff2025` | Gráfalapú riasztás-kontextus | ISC 2025, LNCS; kivonat és teljes szöveg alapján |
| `vanede2022` | DeepCASE | IEEE S\&P 2022; kivonat: az események 86,72%-át szűri, a munkaterhet 90,53%-kal csökkenti |
| `wilkens2021`, `nadeem2021`, `shittu2015` | Többlépcsős támadások felismerése | Csak cím és kivonat szintjén – konkrét számot ne írj belőlük |
| `uetz2026rba` | Kockázatalapú pontozás | Teljes szöveg alapján (2026-10-01) |
| `anuar2012` | AHP-alapú kockázati index | Kivonat (2026-10-08): az incidensek 100%-a pontozható, a CVSS-sel csak 17,23%. **Az évszám 2013** (javítva a `.bib`-ben, a kulcs maradt) |
| `alsubhi2008`, `alsubhi2011fuzmet` | Fuzzy logikájú rangsorolás | Kivonat; a szempontok listája |
| `porras2002` | Küldetésre gyakorolt hatás | RAID 2002, kivonat |
| `kruegel2004verification` | Riasztás-ellenőrzés | PIK 2004, kivonat és teljes szöveg alapján |
| `njogu2012` | Sérülékenységalapú szűrés | **2013, 6(1), 15–27** (javítva a `.bib`-ben, a kulcs maradt) |
| `sommestad2015` | A hálózati információ alapú szűrés próbája | Kivonat és másodlagos forrás; csak az irányát használjuk |
| `meng2015`, `chergui2020` | Tudásalapú és kontextusalapú szűrés | Kivonat szintjén |
| `wang2024alertpro`, `liu2022rapid`, `hassan2019` | Tanuló és származáskövető rangsorolás | Kivonat; a NoDoze 86%-a és a 364 riasztás az NDSS-oldal szerint |
| `homayoun2026`, `guo2026` | Friss megerősítéses tanulásos / tanuló rangsorolás | Kiadói adatlap; csak létezésüket és irányukat említjük |
| `jalalvand2024` | A rangsorolás szempontjainak rendszerezése | ACM CSUR 57(2); általános hivatkozásként |
| `yu2005trinetr`, `taha2010`, `bougueroua2021` | Klasszikus többágenses rendszerek | Kiadói adatlap és kivonat |
| `wei2025cortex` | CORTEX | arXiv:2510.00311, teljes szöveg alapján |
| `liu2026hesp` | HESP | arXiv:2609.33446, teljes szöveg alapján |
| `vallabhaneni2026sentinel` | SENTINEL-RL | arXiv:2609.04159, teljes szöveg alapján |
| `abdennebi2026lang` | LanG | arXiv:2604.05440, teljes szöveg alapján |
| `roy2026agentsoc` | AgentSOC | IEEE ICAIC 2026; arXiv-változat alapján |
| `hmimou2025` | Három agent + korreláció nyelvi modellel | IEEE Access 13, 150199–150215; **csak a kivonat alapján** |
| `ismail2025copilot` | Wazuh + RAG alapú segéd | Sensors 25(3), 870; kivonat (2026-10-08) |
| `chhetri2024` | Ember és MI együttműködése a SOC-ban | ACM TOIT; kivonat |
| `arp2022`, `ndichu2026`, `landauer2024aitads` | Értékelési gyakorlat | Korábban ellenőrizve |

Kimaradt: `shah2019` (a cím és a DOI nem ellenőrizhető), `srinivas2025` (a szerzők nem ellenőrizhetők –
csak „and others” formában maradhatna, ezért inkább kihagytuk).

---

## 3.0 Nyitó bekezdés

```latex
Az előző fejezet bemutatta, hogy a behatolásérzékelők és a \ac{SIEM} rendszerek több riasztást
állítanak elő, mint amennyit az elemzők érdemben fel tudnak dolgozni.
Ez a fejezet azokat a módszereket tekinti át, amelyeket a kutatók és a gyártók e probléma kezelésére
javasoltak.
A módszereket két kérdés mentén vizsgálom: mit nyerünk velük, és milyen feltételezésekre, adatokra
vagy erőforrásokra van szükségük.
Mivel a dolgozatban tervezett rendszer a meglévő megoldások hiányosságaira épül, minden
módszercsaládnál külön kitérek a gyengeségekre is; ezeket a fejezet végén egy összefoglaló
táblázat veti össze a saját megközelítés elemeivel.
```

---

## 3.1 A riasztásfeldolgozás lépései

```latex
\subsection{A riasztásfeldolgozás lépései és fogalmai}\label{sec:lepesek}

A riasztások utólagos feldolgozásának szakirodalma nem egységes szóhasználatú: ugyanazt a
műveletet egyes szerzők korrelációnak, mások aggregációnak vagy összevonásnak nevezik.
Valeur és szerzőtársai ezért a feldolgozást egymás után kapcsolható összetevőkre bontották, és egy
közös keretben helyezték el a korábbi megoldásokat~\cite{valeur2004}.
Modelljükben a riasztásokat először egységes formára hozzák, majd összevonják az ugyanazt az
eseményt leíró jelzéseket, ellenőrzik, hogy a támadás sikeres lehetett-e, összekapcsolják az egy
támadáshoz tartozó lépéseket, végül értékelik a kapott csoportok fontosságát.
Későbbi áttekintések a korrelációs módszereket elsősorban aszerint csoportosítják, hogy
hasonlóságon, előre leírt támadási forgatókönyveken, ok-okozati előfeltételeken vagy statisztikai
összefüggéseken alapulnak~\cite{sadoddin2006,salah2013,mirheidari2013,kotenko2022}.

A dolgozatban három fogalmat különítek el.
\emph{Csoportosításon} azt értem, amikor az összetartozó riasztásokat egyetlen egységbe -- a
szakirodalomban gyakran meta-riasztásba -- fogjuk össze; ez csökkenti az elemző elé kerülő tételek számát.
\emph{Rangsoroláson} azt, amikor a riasztásokat vagy csoportokat fontosság szerint sorba rendezzük;
ez nem csökkenti a tételek számát, de meghatározza, mivel kezdjen az elemző.
\emph{Szűrésen} pedig azt, amikor egyes riasztásokat az elemző elől teljesen elrejtünk.
A szűrés a leghatékonyabb a terhelés csökkentésében, de egyben a legkockázatosabb is, mert a tévesen
eltávolított riasztás valódi támadást rejthet.
Ndichu és szerzőtársai áttekintése szerint a terület módszerei ezen lépések köré szerveződnek, és a
legújabb munkák negyedik lépésként a nagy nyelvi modellekkel történő támogatást is bevezetik~\cite{ndichu2026}.
```

Megjegyzés: ide jól illik egy saját ábra a Valeur-féle lépésekről, a saját agentjeid hozzárendelésével
(egységesítő → csoportosító → környezet/sérülékenységi → rangsoroló → magyarázó). Ha kéred,
elkészítem `thesis/img/`-be (forrás: „saját ábra \cite{valeur2004} alapján”).

---

## 3.2 Csoportosítás és korreláció

```latex
\subsection{A riasztások csoportosítása és korrelációja}\label{sec:csoportositas}

\subsubsection{Hasonlóság és időbeli közelség alapján}

A legegyszerűbb és a gyakorlatban legelterjedtebb megoldás azokat a riasztásokat vonja össze,
amelyek néhány kulcsmezőben -- például a forrás- vagy a cél-IP-címben, a szabályban vagy a
felhasználóban -- megegyeznek, és rövid időn belül követik egymást.
A módszer gyors, nem igényel tanítóadatot, és könnyen magyarázható, hiszen az elemző látja, mely
mező alapján kerültek egy csoportba a riasztások.
Gyengesége, hogy az eredmény erősen függ a kulcsmezők és az időablak megválasztásától: túl szűk
ablakkal egy támadás több csoportra esik szét, túl széles ablakkal pedig a párhuzamos, egymástól
független események egy csoportba kerülnek.
A mezőkre épülő szabályok ráadásul feltételezik, hogy minden riasztás tartalmazza ugyanazokat a
mezőket, ami a hálózati és a gépi érzékelők riasztásainak együttes kezelésénél nem teljesül.

Landauer és szerzőtársai ezt a korlátot olyan, tartománytól független eljárással oldották fel,
amely tetszőleges, félig strukturált riasztások között képes hasonlóságot számolni, és a
csoportokat időben egymást átfedő riasztásokból építi fel~\cite{landauer2022}.
Kiértékelésük szerint a módszer nagyjából 80\%-kal csökkentette az elemző elé kerülő csoportok
számát, és a csoportokhoz rendelt támadástípusokat mintegy 80\%-os találati és 5\%-nál kisebb
téves riasztási aránnyal ismerte fel.
A megközelítés azonban továbbra is az időbeli közelségre támaszkodik, ezért erősen zajos
környezetben vagy egyszerre zajló támadásoknál a csoportok összemosódhatnak.

\subsubsection{Ok-feltárás csoportosítással}

Julisch abból indult ki, hogy a riasztások túlnyomó többségét néhány, tartósan fennálló ok -- például
egy hibásan beállított szolgáltatás vagy egy szokatlan, de jóindulatú alkalmazás -- váltja ki~\cite{julisch2003}.
Vizsgálatai szerint néhány tucat ilyen kiváltó ok felelt a riasztások több mint 90\%-áért.
Ha ezeket az okokat csoportosítással feltárjuk és megszüntetjük, a jövőbeli riasztások száma
tartósan csökken.
A módszer ereje, hogy nem tüneti kezelést ad, hanem az okot szünteti meg; gyengesége, hogy emberi
értelmezést igényel, utólagos (nem valós idejű), és a valódi támadásokat nem rangsorolja, csak
a jóindulatú zajt segít eltávolítani.

\subsubsection{Többlépcsős támadások összekapcsolása}

A korreláció másik iránya a támadás lépéseit kapcsolja össze: ha egy felderítést egy sikeres
bejelentkezés, majd jogosultságszerzés követ ugyanazon a gépen, ezek együtt sokkal többet
jelentenek, mint külön-külön.
Erre a célra a szakirodalom támadási forgatókönyveket, a támadás szakaszait követő
állapotgépeket~\cite{wilkens2021}, a riasztásokból tanult támadási gráfokat~\cite{nadeem2021} és a
korreláció utáni elemzést~\cite{shittu2015} egyaránt javasolt.
Közös gyengeségük, hogy előre rögzített tudást -- forgatókönyveket, a lépések sorrendjét vagy
tanítóadatot -- igényelnek, így a modellben nem szereplő támadási lánc rejtve maradhat, a
fenntartásuk pedig jelentős szakértői munkát kíván.

\subsubsection{Gépi tanulásra és gráfokra épülő csoportosítás}

Az újabb munkák a csoportosítást tanuló modellekkel végzik.
A DeepCASE az egy géphez tartozó eseménysorozatokból tanulja meg, mely korábbi események adnak
magyarázatot egy újabb riasztásra, és a hasonló helyzeteket egyszerre, egy döntéssel
kezelteti az elemzővel~\cite{vanede2022}.
A szerzők szerint az események 86,72\%-át tudta így automatikusan kezelni, és az elemzői munkát
90,53\%-kal csökkentette.
Az AlertBERT a riasztásokat egy maszkolt nyelvi modellel alakítja számvektorrá, majd sűrűségalapú
csoportosítást végez; a szerzők szerint zajos környezetben és egyidejű támadások esetén
megbízhatóbb, mint az időkülönbségre épülő csoportosítás~\cite{karner2026alertbert}.
Eckhoff és szerzőtársai a riasztásokat közös jellemzőik -- például IP-cím vagy felhasználó --
mentén gráffá kötik össze, és a gráfrészletek hasonlóságát tanuló modellel vizsgálják~\cite{eckhoff2025}.

Ezek a módszerek pontosabbak a kézi szabályoknál, de áruk van.
Tanítóadatot vagy legalább egy betanítási időszakot igényelnek, a környezet változásakor újra kell
tanítani őket, és döntéseik nehezebben magyarázhatók az elemző számára.
Kiértékelésük ráadásul jellemzően a csoportok tisztaságára vagy a csökkentés mértékére irányul,
arra kevésbé, hogy a csoportok közül melyik a legfontosabb.
```

Megjegyzés: a DeepCASE két számát (86,72% és 90,53%) ne kerekítsd, így szerepel a kivonatban.
A Wilkens, Nadeem és Shittu munkákból szándékosan nincs szám – csak kivonatszinten ellenőriztem őket.

### 3.1. táblázat – a csoportosítási módszerek (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A riasztás-csoportosítási módszerek összehasonlítása (Forrás: saját összeállítás)}
    \label{tab:csoportositas}
    \small
    \begin{tabular}{|L{2.8cm}|L{2.4cm}|L{4.0cm}|L{4.0cm}|}
        \hline
        \textbf{Módszercsalád} & \textbf{Példa} & \textbf{Erősség} & \textbf{Gyengeség} \\ \hline
        Kulcsmezők és időablak & \cite{valeur2004} & Gyors, tanítás nélküli, átlátható & Az ablak és a mezők megválasztásától függ; eltérő formátumú riasztásoknál nehéz \\ \hline
        Tartomány\-független hasonlóság & \cite{landauer2022} & Tetszőleges riasztásformára működik & Az időbeli közelségre épül; zajban a csoportok összemosódnak \\ \hline
        Ok-feltárás & \cite{julisch2003} & A zaj okát szünteti meg & Utólagos, emberi értelmezést kíván, nem rangsorol \\ \hline
        Többlépcsős korreláció & \cite{wilkens2021,nadeem2021} & A támadási láncot egyben mutatja & Előre rögzített tudást vagy tanítóadatot igényel \\ \hline
        Gépi tanulás, gráf & \cite{vanede2022,karner2026alertbert,eckhoff2025} & Pontos, zajtűrő & Tanítást igényel, nehezen magyarázható, nem a fontosságot méri \\ \hline
    \end{tabular}
\end{table}
```

---

## 3.3 Rangsorolás

```latex
\subsection{A riasztások rangsorolása}\label{sec:rangsorolas}

\subsubsection{Rangsorolás a súlyosság szerint}

A legtöbb behatolásérzékelő és \ac{SIEM} rendszer minden szabályhoz súlyossági szintet rendel,
és az elemzők ezt használják a sorrend kialakítására.
A módszer előnye, hogy semmilyen többletadatot nem igényel; hátránya, hogy a súlyosságot a szabály
írója a szabály megírásakor, a konkrét környezet ismerete nélkül határozza meg.
Ugyanaz a szabály ugyanazt a súlyosságot kapja egy tesztgépen és egy kritikus adatbázis-kiszolgálón,
és akkor is, ha a megcélzott szoftver nem is fut az adott gépen.
A súlyossági szintek emellett durvák: néhány fokozatba sok ezer riasztás kerül, amelyeken belül
nincs további sorrend.
Uetz és szerzőtársai mérése szerint a csak súlyosság szerinti sorrend rangsor-pontossága (\ac{AUROC})
átlagosan 0,72 volt~\cite{uetz2026rba}, Ndichu és szerzőtársai áttekintése pedig kifejezetten
kockázatként írja le, ha egy csapat kizárólag erre hagyatkozik~\cite{ndichu2026}.

\subsubsection{Többszempontú döntési módszerek}

A többszempontú döntéstámogató módszerek több mérőszámot vonnak össze egyetlen pontszámmá.
Anuar és szerzőtársai a páros összehasonlításon alapuló \ac{AHP}-t használták arra, hogy az
érintett eszköz kritikusságát, helyettesíthetőségét és más tulajdonságait súlyozzák, és ebből
kockázati indexet számoljanak~\cite{anuar2012}.
Kiértékelésükben ezzel az incidensek mindegyikét sorba lehetett állítani, míg a sérülékenységek
szabványos pontozása (\ac{CVSS}) alapján csak 17,23\%-ukat.
Alsubhi és szerzőtársai fuzzy logikával kombinálták többek között a támadás alkalmazhatóságát, az
áldozat fontosságát, az érzékelő állapotát és a korábbi riasztásokkal való kapcsolatot~\cite{alsubhi2008,alsubhi2011fuzmet}.

E módszerek erőssége, hogy átláthatók és szakértői tudással közvetlenül hangolhatók.
Gyengeségük, hogy a súlyokat és a szabályokat jellemzően egy szakértő adja meg, ennek hatását
ritkán vizsgálják érzékenységvizsgálattal, és kiértékelésük többnyire régi, mesterséges
adathalmazokon történt.
Így nem tudjuk, mennyit érnek egy korszerű, erős összehasonlítási alaphoz képest.
Jalalvand és szerzőtársai áttekintése a rangsorolás szempontjait és módszereit rendszerezi, és
ugyancsak azt jelzi, hogy a szempontok bősége mellett kevés az összevethető, megismételhető
kiértékelés~\cite{jalalvand2024}.

\subsubsection{Környezeti információ és riasztás-ellenőrzés}

Egy riasztás jelentősége nagymértékben attól függ, hol történik.
Porras és szerzőtársai már 2002-ben olyan rangsorolást javasoltak, amely a szervezet működése
szempontjából fontos gépeket és szolgáltatásokat, valamint a hálózat felépítését is figyelembe
veszi~\cite{porras2002}.
Kruegel és szerzőtársai a riasztás-ellenőrzést vizsgálták: azt, hogy egy támadási kísérlet
sikeres lehetett-e az adott célponton~\cite{kruegel2004verification}.
Rámutattak, hogy a környezeti információ önmagában nem elég, mert az ellenőrzés csak akkor
megbízható, ha a gépekről tárolt adatok naprakészek.
Njogu és szerzőtársai a hálózat sérülékenységeit vetették össze a riasztásokkal, és azokat a
riasztásokat, amelyek nem érintettek meglévő sérülékenységet, alacsonyabb prioritásúnak
tekintették~\cite{njogu2012}.
Hasonló irányt követnek a tudásalapú és a kontextusalapú szűrők is~\cite{meng2015,chergui2020}.

A környezetre épülő módszerek legfőbb gyengesége, hogy jellemzően \emph{szűrnek}: a nem
illeszkedő riasztást eltávolítják vagy hátrasorolják.
Ha a nyilvántartás hiányos -- egy gépről nem tudjuk, hogy fut rajta egy sérülékeny szolgáltatás --,
a valódi támadás is kieshet.
Sommestad és Franke kísérletében a hálózati információra épülő szűrés valóban jelentősen
csökkentette a riasztások számát, de a valódi támadásokhoz tartozó riasztások egy részét is
eltávolította~\cite{sommestad2015}.
További gyengeség, hogy e munkák többsége a környezeti információt egyetlen, magában álló
rangsorolóban használja, és nem méri, mennyit tesz hozzá egy olyan módszerhez, amely a
riasztások folyamából már önmagában is jó sorrendet ad.

\subsubsection{Kockázatalapú riasztás-pontozás}

A kockázatalapú riasztás-pontozás (\ac{RBA}) nem az egyes riasztásokat, hanem az egy géphez vagy
felhasználóhoz kapcsolódó, időben halmozódó kockázatot értékeli.
Az iparban a Splunk vezette be ezt a szemléletet, ahol a riasztások kockázati pontokat adnak az
érintett eszközhöz vagy személyhez, és az elemző csak akkor kap jelzést, ha az összeg egy küszöböt
átlép~\cite{splunkrba}.
A gyártói megvalósítás az eszközök és személyek fontosságát is beszámíthatja, a hatásáról azonban
nincs nyilvános, megismételhető mérés.

Uetz és szerzőtársai a módszer nyílt, tanítóadatot nem igénylő változatát dolgozták ki és mérték
fel nyolc adathalmazon~\cite{uetz2026rba}.
A pontszám öt, a riasztásokból közvetlenül számolható részből áll: a szabály súlyosságából, a
riasztások rövid időn belüli halmozódásából, a változatosságukból, valamint a ritkaságukból és a
szokásos mintától való eltérésükből.
Ezzel a rangsor-pontosság átlagosan 0,92-re nőtt a csak súlyosság szerinti 0,72-höz képest.
Ez a módszer a dolgozat legerősebb összehasonlítási alapja: nyilvános, megismételhető, és nem
igényel tanítást.
Gyengesége ugyanakkor, hogy minden információja a riasztások folyamából származik.
Nem tudja, hogy az érintett gép mennyire fontos, fut-e rajta a támadás által kihasználható
szoftver, és mennyire látják a megfigyelőeszközök; egy kritikus, de ritkán riasztó kiszolgálón
történő egyetlen, célzott támadás így hátrébb kerülhet egy zajos tesztgép riasztásainál.

\subsubsection{Tanuló és származáskövető rangsorolás}

A tanuló módszerek a fontosságot adatból becslik.
Az AlertPro a riasztások környezeti jellemzőit megerősítéses tanulással dolgozza fel, és az
elemzők visszajelzéseiből tanulja meg a többlépcsős támadások lépéseinek előresorolását~\cite{wang2024alertpro}.
A NoDoze minden riasztáshoz felépíti az érintett folyamatok és fájlok ok-okozati gráfját, és azt
értékeli, mennyire szokatlan ez a gráf a szervezetben korábban látottakhoz képest~\cite{hassan2019}.
A szerzők 364 riasztáson végzett kiértékelése szerint a téves riasztások száma 86\%-kal csökkent.
A RAPID ugyanezt a származáskövetést valós idejűvé tette, és a már folyamatban lévő vizsgálatokat
is figyelembe veszi~\cite{liu2022rapid}.
Hasonló, megerősítéses tanulásra vagy tanuló modellekre épülő megoldások a legfrissebb
irodalomban is megjelennek~\cite{homayoun2026,guo2026}.

E módszerek gyengesége a tanítóadat iránti igény: az elemzők címkéi, visszajelzései vagy hosszú
megfigyelési időszak nélkül nem használhatók, a címkék pedig a valós SOC-okban ritkák és
következetlenek.
A származáskövető megoldások ráadásul részletes, gépi szintű eseménynaplót igényelnek, amely a
hálózati behatolásérzékelők riasztásaihoz nem áll rendelkezésre.
Végül a tanult súlyok nehezen magyarázhatók, és a környezet megváltozásakor újratanítást igényelnek.
```

Megjegyzés: a Splunk-bekezdés a kutatási rés pontosított megfogalmazása (a Splunk RBA használ
eszköz- és személyadatot – a rés a **nyilvános mérés** hiánya). Ezt érdemes az 1. fejezet
„kutatási rés” bekezdésébe is átvezetni (lásd `docs/atadas.md`).

### 3.2. táblázat – a rangsorolási módszerek (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A riasztás-rangsorolási módszerek összehasonlítása (Forrás: saját összeállítás)}
    \label{tab:rangsorolas}
    \small
    \begin{tabular}{|L{2.5cm}|L{2.3cm}|L{1.6cm}|L{1.6cm}|L{4.8cm}|}
        \hline
        \textbf{Módszercsalád} & \textbf{Példa} & \textbf{Környe\-zet} & \textbf{Tanítás} & \textbf{Fő gyengeség} \\ \hline
        Súlyosság & gyártói szabályok & nem & nem & Durva, a környezettől független \\ \hline
        Többszempontú (\ac{AHP}, fuzzy) & \cite{anuar2012,alsubhi2011fuzmet} & igen & nem & Szakértői súlyok érzékenységvizsgálat nélkül; régi adathalmazokon mérve \\ \hline
        Környezet és ellenőrzés & \cite{porras2002,kruegel2004verification,njogu2012} & igen & nem & Szűr: hiányos nyilvántartásnál valódi támadást is eltávolít \\ \hline
        Kockázatalapú (\ac{RBA}) & \cite{uetz2026rba,splunkrba} & nyilvános mérésben nem & nem & Csak a riasztások folyamából dolgozik \\ \hline
        Tanuló, származáskövető & \cite{wang2024alertpro,hassan2019,liu2022rapid} & részben & igen & Címkét vagy részletes gépi naplót igényel; nehezen magyarázható \\ \hline
    \end{tabular}
\end{table}
```

---

## 3.4 Agent-alapú és nyelvimodell-alapú megközelítések

```latex
\subsection{Agent-alapú és nagy nyelvi modellekre épülő megközelítések}\label{sec:agentek}

\subsubsection{Klasszikus többágenses rendszerek}

Az agent-alapú felépítés nem új a behatolásérzékelésben.
A többágenses rendszerekben önálló, egymással üzenetekkel együttműködő programrészek végzik az
adatgyűjtést, az elemzést és a döntést; ez jól illeszkedik az elosztott hálózatokhoz, és lehetővé
teszi, hogy az egyes feladatokat külön, cserélhető összetevők lássák el~\cite{bougueroua2021}.
A TRINETR például külön agentekkel gyűjtötte össze a riasztásokat, tudásalapú szabályokkal
értékelte őket, majd korrelálta az eredményeket~\cite{yu2005trinetr}; Taha és szerzőtársai
szintén agentekre bontották a riasztások korrelációját~\cite{taha2010}.
Ezekben a rendszerekben az agent szerepe a munka megosztása és a modularitás volt; a döntések
szabályokon alapultak, ezért kiszámíthatók voltak, de a szabályok karbantartása nagy munkát igényelt.

\subsubsection{A nagy nyelvi modellek megjelenése a SOC-ban}

A nagy nyelvi modellek (\ac{LLM}) új lehetőséget hoztak: természetes nyelvű szöveget értenek
és állítanak elő, így képesek a riasztások tartalmát összefoglalni, a vizsgálat következő lépését
javasolni, vagy a szervezet dokumentációjából releváns részeket előkeresni.
Ismail és szerzőtársai például a Wazuh eseményeihez olyan segédet készítettek, amely a választ
egy keresésen alapuló szövegelőállítással (\ac{RAG}) támasztja alá: az incidenskezelési tudásból,
a MITRE ATT\&CK tudásbázisból és a NIST kiberbiztonsági keretrendszeréből keres elő
összefüggéseket~\cite{ismail2025copilot}.
Hmimou és szerzőtársai három szakosodott agentet -- levélellenőrző, naplóelemző és IP-cím-vizsgáló --
kötöttek össze egy központi összetevővel, amely az eredményeiket nyelvi modell segítségével
korrelálja~\cite{hmimou2025}.
Chhetri és szerzőtársai hangsúlyozzák, hogy ezek a rendszerek az elemzőt nem kiváltják, hanem
vele együttműködve kell működniük~\cite{chhetri2024}.

\subsubsection{Nyelvi modellekre épülő agentrendszerek a riasztások kezelésében}

A legújabb munkák több, nyelvi modellel működő agentet kapcsolnak össze a riasztások
vizsgálatára.
A CORTEX-ben egy-egy agent a viselkedést elemzi, a bizonyítékokat gyűjti és a döntést hozza meg;
az adatokhoz szabványos eszközfelületen (\ac{MCP}) férnek hozzá~\cite{wei2025cortex}.
A szerzők mérése szerint a többágenses változat pontosabb volt az egyetlen modellnél: a
beavatkozást igénylő esetek felismerésének F1-értéke 0,66-ról 0,78-ra nőtt, a téves riasztások
aránya pedig 24,9\%-ról 14,2\%-ra csökkent.
Ennek ára azonban számottevő: riasztásonként mintegy 23\,600 szövegegységet (tokent) dolgozott fel,
nagyjából 5,7-szer többet, és egy riasztás vizsgálata átlagosan 152 másodpercig tartott, ami
körülbelül 3,4-szeres lassulás.

A LanG egységes biztonsági műveleti platformot ír le, amelyben a korrelációt gráfalapú
közösségkereső algoritmus és valószínűségi pontozás végzi, a nyelvi modell pedig csak
hipotéziseket fogalmaz meg; a bizonytalan válaszokat egy küszöb kiszűri, a lényeges döntésekhez
pedig emberi jóváhagyás kell~\cite{abdennebi2026lang}.
Az AgentSOC hasonló elven a nyelvi modell javaslatait egy kiszámítható, gráfalapú ellenőrzésen
engedi át, és a gépnyilvántartás adatait is felhasználja; kiértékelése azonban egy kisméretű,
részben mesterséges környezetben, előre felcímkézett összehasonlító adathalmaz nélkül történt,
és a futásidő nagyjából 95\%-át a nyelvi modell tette ki~\cite{roy2026agentsoc}.

\subsubsection{A nyelvi modellek korlátai és a vegyes felépítés}

A nyelvi modellek használatának több, jól dokumentált korlátja van.
Kimenetük nem determinisztikus, így ugyanarra a riasztásra két futás eltérő választ adhat; ez a
megismételhető mérést és az utólagos elszámoltathatóságot is megnehezíti.
Hihető, de hamis állításokat is előállíthatnak, a feldolgozható szöveg hossza korlátos, és a
futtatásuk -- különösen nagy riasztásmennyiségnél -- lassú és költséges.
A felhőben futó modellek használata ráadásul azt jelenti, hogy érzékeny naplóadatok hagyják el a
szervezetet.

Liu és Wang vizsgálata szerint a helyben futtatható, kisebb modellek önállóan nem képesek
megbízhatóan végigvezetni egy riasztás vizsgálatát: rossz lépést választanak, vagy nem tudják,
mikor kell megállniuk~\cite{liu2026hesp}.
Ha viszont a lépések sorrendjét és a leállás feltételét a modellen kívüli, kiszámítható vezérlő
határozza meg, egy hétmilliárd paraméteres modell ellenőrzött befejezési aránya 0,125-ről 1,000-ra nőtt.
A SENTINEL-RL hasonló következtetésre jut: a hálózati összefüggések elemzését és a döntést egy erre
tanított, nem nyelvi modell végzi, a nyelvi modell csak az eredmény szöveges magyarázatát írja meg,
amelyet egy további ellenőrző lépés hagy jóvá~\cite{vallabhaneni2026sentinel}.

Ezekből a munkákból egy közös irány rajzolódik ki: a nyelvi modell ott hasznos, ahol szöveget kell
értelmezni vagy előállítani, a pontozást és a lépések sorrendjét azonban célszerű kiszámítható
programra bízni.
A jelenlegi nyelvimodell-alapú rendszerek közös gyengesége ugyanakkor az értékelés: a legtöbb
saját, nem nyilvános vagy mesterségesen előállított adaton mér, ezért eredményeik nem vethetők
össze egymással, és nem derül ki, mennyit adnak hozzá egy erős, nyelvi modell nélküli rangsoroláshoz.
```

Megjegyzés: a „nem determinisztikus / hihető, de hamis állítás / felhő → adatkiáramlás” bekezdés
általános szakmai tudás; ha a konzulens forrást kér rá, a `vallabhaneni2026sentinel` és a
`liu2026hesp` használható (mindkettő tárgyalja). Az AgentSOC „5000 esemény, 50 csomópont” részletét
szándékosan nem írtam bele – ha kell, szólj, és a pontos számokat átnézem.

### 3.3. táblázat – agent- és nyelvimodell-alapú rendszerek (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{Agent-alapú és nyelvimodell-alapú riasztáskezelő rendszerek (Forrás: saját összeállítás)}
    \label{tab:agentek}
    \small
    \begin{tabular}{|L{2.3cm}|L{3.2cm}|L{3.0cm}|L{4.7cm}|}
        \hline
        \textbf{Rendszer} & \textbf{A nyelvi modell szerepe} & \textbf{Kiértékelés} & \textbf{Gyengeség} \\ \hline
        TRINETR \cite{yu2005trinetr} & nincs (szabályok) & saját környezet & Kézi szabálykarbantartás \\ \hline
        CORTEX \cite{wei2025cortex} & minden lépés & saját adat & Kb. 5,7-szeres szövegmennyiség, 3,4-szeres lassulás \\ \hline
        LanG \cite{abdennebi2026lang} & hipotézis, küszöbbel szűrve & saját adat & Összetett platform; nincs nyilvános összehasonlító mérés \\ \hline
        AgentSOC \cite{roy2026agentsoc} & hipotézis, gráffal ellenőrizve & kis, részben mesterséges környezet & Nincs címkézett összehasonlító adathalmaz \\ \hline
        HESP \cite{liu2026hesp} & vizsgálati lépések, külső vezérlővel & saját feladatsor & A rangsor minőségét nem méri \\ \hline
        SENTINEL-RL \cite{vallabhaneni2026sentinel} & csak magyarázat, ellenőrzéssel & mesterséges hálózat & Tanított döntési modellt igényel \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a „Kiértékelés” oszlop tömör jellemzés; ha valamelyiknél pontosítani szeretnél (pl. a
CORTEX adathalmazának neve), szólj, és kikeresem a cikkből.

---

## 3.5 Az értékelés gyakorlata

```latex
\subsection{A kiértékelés gyakorlata és buktatói}\label{sec:ertekeles-irodalom}

A módszerek összehasonlítását nehezíti, hogy kiértékelésük nagyon eltérő módon történik.
Arp és szerzőtársai a gépi tanulást alkalmazó biztonsági kutatások gyakori hibáit gyűjtötték
össze~\cite{arp2022}.
Ezek közül a riasztáskezelés szempontjából a legfontosabbak: a valóságot rosszul tükröző
mintavétel; az, ha a módszer beállításai a tesztadatból származó tudást is felhasználnak; a túl
gyenge összehasonlítási alap; a feladathoz nem illő mérőszám; a valódi támadások ritkaságának
figyelmen kívül hagyása; valamint az, ha a módszert csak laboratóriumi körülmények között vizsgálják.
Ndichu és szerzőtársai áttekintése szerint a riasztási fáradtság csökkentésére javasolt
módszerek közül 87 tanulmányból csak 9 alapult éles SOC-adatokon~\cite{ndichu2026}.

A megismételhető összehasonlításhoz nyilvános, felcímkézett adathalmaz kell.
Az AIT-ADS egy több lépésből álló támadást nyolc, eltérő felépítésű környezetben játszik le, és a
hálózati és gépi érzékelők riasztásait a támadáshoz tartozás jelölésével együtt teszi
közzé~\cite{landauer2024aitads}.
Uetz és szerzőtársai ugyanezen az adathalmazon mérték a kockázatalapú pontozást~\cite{uetz2026rba},
így a dolgozat eredményei közvetlenül összevethetők az övékkel.
A dolgozat értékelési terve ezekre a tanulságokra épül: a szakértői súlyokat a mérés előtt
rögzítem, az adatból tanult súlyokat egy forgatókönyv kihagyásával tanítom és azon mérem, és az
összehasonlítási alap a legerősebb nyilvánosan mért módszer.
```

Megjegyzés: az utolsó mondat a saját módszertanod – a 6. fejezetben részletezed; itt elég ennyi előre utalásnak.

---

## 3.6 Összegzés: a módszerek gyengeségei és a dolgozat válasza

```latex
\subsection{Összegzés: a meglévő megoldások hiányosságai}\label{sec:resek}

Az áttekintett módszercsaládok mindegyike a probléma egy részét oldja meg.
A csoportosítás csökkenti az elemző elé kerülő tételek számát, de nem mondja meg, melyik csoporttal
kell kezdeni.
A súlyosság szerinti sorrend egyszerű, de a környezettől független és durva.
A többszempontú és a környezetre épülő módszerek a gép fontosságát és a sérülékenységeket is
figyelembe veszik, de többnyire szűrnek, és nem mérik, mennyit tesznek hozzá egy erős alaphoz.
A kockázatalapú pontozás nyilvános mérésben a legjobb tanítás nélküli módszer, de semmit nem tud
a környezetről.
A tanuló módszerek pontosak, de címkéket igényelnek és nehezen magyarázhatók.
A nyelvi modellekre épülő agentrendszerek jól magyaráznak, de lassúak, költségesek, kimenetük nem
megismételhető, és kiértékelésük nem nyilvános adatokon történik.
\Az{\ref{tab:resek}}. táblázat összefoglalja, hogy a dolgozatban tervezett rendszer mely elemei
melyik hiányosságra adnak választ.
```

### 3.4. táblázat – a rések és a saját rendszer (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A meglévő megoldások hiányosságai és a tervezett rendszer válaszai (Forrás: saját összeállítás)}
    \label{tab:resek}
    \small
    \begin{tabular}{|L{4.4cm}|L{2.6cm}|L{6.6cm}|}
        \hline
        \textbf{Hiányosság} & \textbf{Érintett módszerek} & \textbf{A tervezett rendszer válasza} \\ \hline
        A legerősebb nyilvános, tanítás nélküli módszer nem használ környezeti információt & \cite{uetz2026rba} & A kockázatalapú pontszámot a gép fontosságával, a sérülékenységekkel és a megfigyeltséggel bővíti, lépésenként mérve a hozzáadott értéket \\ \hline
        A környezeti módszerek szűrnek, hiányos nyilvántartásnál valódi támadást is eltávolítanak & \cite{njogu2012,sommestad2015} & A környezet csak súlyként módosítja a sorrendet, riasztást nem töröl; az átcsúszó támadások arányát legfeljebb 2\%-ban korlátozza \\ \hline
        A szakértői súlyok hatását ritkán vizsgálják & \cite{anuar2012,alsubhi2011fuzmet} & Páros összehasonlítással (\ac{AHP}) rögzített súlyok, érzékenységvizsgálat és adatból tanult súlyokkal való összevetés \\ \hline
        A tanuló módszerek címkét vagy részletes gépi naplót igényelnek & \cite{wang2024alertpro,hassan2019} & Tanítóadat nélkül működik; tanult súlyokat csak összehasonlításként használ \\ \hline
        A nyelvimodell-alapú agentek lassúak és nem megismételhetők & \cite{wei2025cortex,liu2026hesp} & A pontszámot kiszámítható program adja, a lépések sorrendjét vezérlő tartja; a nyelvi modell csak magyarázatot ír, helyben futtatva, ellenőrzéssel \\ \hline
        Az eredmények nem nyilvános vagy mesterséges adatokon születnek & \cite{ndichu2026,roy2026agentsoc} & Nyilvános, felcímkézett adathalmazon (AIT-ADS) mér, a meglévő mérésekkel közvetlenül összevethetően \\ \hline
        A csoportosítás és a rangsorolás külön-külön készül & \cite{landauer2022,uetz2026rba} & Az összetartozó riasztásokat csoportosítja, és a csoportokat rangsorolja \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a 3.4. táblázat a fejezet „csúcspontja” – a konzulensi előadás egyik diája is lehet.
Ha a megfogalmazást a saját szavaidra írod át, a hivatkozásokat hagyd meg.

---

## Átvételkor figyelj

- A blokkokat nyugodtan írd át a saját stílusodra; a számokat és a hivatkozásokat ne változtasd meg.
- A táblázatokhoz a sablonban megvan az `L{}` oszloptípus (v0.8) és a `float` csomag (`[H]`).
- A 3.2–3.3. alfejezetek a legterjedelmesebbek; ha rövidíteni kell, a 3.2.3 (többlépcsős támadások)
  és a 3.4.1 (klasszikus agentek) bekezdése tömöríthető egy-két mondatra.
- Ide tartozó, még nyitott ellenőrzés: Hmimou 2025 (csak kivonat), AgentSOC pontos kísérleti adatai.

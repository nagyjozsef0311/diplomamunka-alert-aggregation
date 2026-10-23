# Írási csomag – 5. fejezet: Az agent-alapú rendszer felépítése és az eszközök kiválasztása

2026-10-23 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Feladatlap:** F4 – az agent-alapú rendszer tervezése.
- **Útmutató:** 6. pont – tervezés.
- **Diplomamunka II.:** 4–6. pont – specifikáció és terv. Terjedelem: kb. **7–8 oldal** a három ábrával.
- **Fájl:** `chapters/5_Rendszerterv.tex`; a `main.tex`-ben a 4. fejezet után:

```latex
\clearpage
\section{AZ AGENT-ALAPÚ RENDSZER FELÉPÍTÉSE}\label{sec:rendszer}
\input{chapters/5_Rendszerterv}
```

## Ábrák (Claude készítette, a jóváhagyásod után kerülnek be)

| Fájl | Mit mutat | Forrás (TikZ) |
| --- | --- | --- |
| `img/agent_architektura.pdf` | A hét agent, az adatfolyam, a gépnyilvántartás, a súlyok és a vezérlő | `img/src/agent_architektura.tex` |
| `img/adatmodell.pdf` | A gépnyilvántartás táblái és kapcsolataik | `img/src/adatmodell.tex` |
| `img/magyarazo.pdf` | A magyarázó agent belső lépései: kérés, modell, ellenőrzés, tartalék | `img/src/magyarazo.tex` |

Overleafbe a három PDF-et töltsd fel az `img/` mappába (az `img/src/` nem kell). Mindhárom vektoros, a
dolgozat betűtípusával készült. Ha szöveget módosítanál rajtuk, szólj, és újrarajzolom.

## Rövidítések (`acronyms.tex`)

Nincs új rövidítés; használt: SOC, IDS, LLM, MCP, AHP, CPE, CVE.

## Források és ellenőrzöttségük

| Kulcs | Mire használjuk | Ellenőrzés |
| --- | --- | --- |
| `wooldridge1995` | **Új.** Az agent „gyenge” fogalma: önállóság, együttműködés, reagálás, kezdeményezés | Knowledge Engineering Review 10(2), 115–152, DOI 10.1017/S0269888900008122 – kiadói és egyetemi oldalak |
| `wu2023autogen` | **Új.** Beszélgetésre épülő agent-keretrendszer: a vezérlést a beszélgetés hajtja | arXiv:2308.08155, a teljes szöveg 1–5. oldala alapján |
| `crewaidocs` | **Új.** A CrewAI felépítése (Crews és Flows) | Hivatalos dokumentáció, 2026-10-23 |
| `ollama` | **Új.** Nyelvi modellek helyi futtatása | Projektoldal (GitHub), 2026-10-23 |
| `langgraph2025`, `mcp2026spec` | A vezérlő és az opcionális csatlakozó | Korábban ellenőrizve (kutatási jegyzet #5) |
| `liu2026hesp`, `roy2026agentsoc`, `wei2025cortex`, `vallabhaneni2026sentinel` | A nyelvi modell szerepének korlátozása | Korábban ellenőrizve |
| `bougueroua2021`, `uetz2026rba`, `shi2024cpe`, `landauer2024aitads` | Többágenses rendszerek, pontszám, CPE, adathalmaz | Korábban ellenőrizve |

---

## 5.0 Nyitó bekezdés

```latex
Ez a fejezet azt írja le, hogyan valósítja meg a rendszer az előző fejezetben rögzített
mérőszámrendszert.
Először meghatározom, mit értek a dolgozatban agenten, majd bemutatom a rendszer felépítését, az
egyes agentek feladatát, bemenetét és kimenetét, valamint a környezeti információt tároló
gépnyilvántartást.
A fejezet végén az eszközök kiválasztását indokolom.
A leírás terv: a megvalósítás a mérésekkel párhuzamosan készül, és a tapasztalatok alapján egyes
részletei változhatnak.
```

---

## 5.1 Az agent fogalma

```latex
\subsection{Az agent fogalma a dolgozatban}\label{sec:agent-fogalom}

Az agent kifejezést a szakirodalom nagyon eltérő értelemben használja.
Wooldridge és Jennings klasszikus meghatározása szerint az agent olyan számítógépes rendszer, amely
önállóan, emberi beavatkozás nélkül működik, más agentekkel együttműködik, reagál a környezete
változásaira, és saját céljai érdekében kezdeményezni is képes~\cite{wooldridge1995}.
A behatolásérzékelés többágenses rendszerei is erre a meghatározásra épülnek: bennük az egyes
feladatokat önálló, egymással üzenetekkel kommunikáló összetevők végzik~\cite{bougueroua2021}.
Az utóbbi években a fogalom jelentése szűkült, és ma gyakran kizárólag a nagy nyelvi modellre épülő,
a következő lépést maga választó programot értik alatta.

A dolgozatban az első, tágabb értelmezést követem.
Agentnek nevezek minden olyan önálló feldolgozó egységet, amelynek pontosan meghatározott feladata,
bemenete és kimenete van, a többi agenttel egy közös állapoton keresztül működik együtt, és egy
vezérlő hangolja össze a működését.
A nagy nyelvi modell ebben a felfogásban az egyik agent egyik eszköze, és nem a rendszer egésze.
Ennek oka a 3. fejezetben bemutatott tapasztalat: a nyelvi modellre bízott vezérlés és pontozás
lassú, költséges és nem megismételhető, a kisebb, helyben futtatható modellek pedig külső vezérlés
nélkül nem képesek megbízhatóan végigvinni egy vizsgálatot~\cite{liu2026hesp}.
```

Megjegyzés: a konzulenssel még nem egyeztetted, elfogadja-e ezt a meghatározást (CLAUDE.md, 7. pont) –
ezt a bekezdést érdemes megmutatni neki.

---

## 5.2 A rendszer felépítése

```latex
\subsection{A rendszer felépítése}\label{sec:felepites-rendszer}

A rendszer hét agentből áll (\ref{fig:architektura}.~ábra).
A feldolgozás egy irányba halad: a riasztások a hálózati és a gépi érzékelőtől indulnak, és a
rangsorolt, magyarázattal ellátott csoportlistában érnek véget, amelyet az elemző kap meg.
Az első öt agent kiszámítható program, vagyis ugyanarra a bemenetre mindig ugyanazt az eredményt adja;
a pontszám és a sorrend kizárólag ezekből származik.
A hatodik, magyarázó agent az egyetlen, amely nyelvi modellt használ, és ennek kimenete a sorrendet
nem befolyásolja.
A hetedik, vezérlő agent nem dolgozza fel a riasztásokat, hanem meghatározza a lépések sorrendjét,
továbbadja az állapotot, naplózza a lépéseket és méri a futásidejüket.

A környezeti információt egy közös gépnyilvántartás tárolja, amelyet a környezeti és a sérülékenységi
agent olvas.
A rangsoroló a mérés előtt rögzített súlyokat egy beállítófájlból kapja, így a súlyok változtatása
nem igényli a program módosítását.
A szaggatott vonal az opcionális bővítést jelöli: a laboratóriumi mérésben a gépnyilvántartás egy
szabványos, csak olvasható csatlakozón (\ac{MCP}) keresztül a magyarázó agent számára is elérhetővé
válhat~\cite{mcp2026spec}.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\linewidth]{img/agent_architektura.pdf}
    \caption{A tervezett agent-alapú rendszer felépítése (Forrás: saját ábra)}
    \label{fig:architektura}
\end{figure}
```

---

## 5.3 Az agentek tervezett felépítése

```latex
\subsection{Az agentek tervezett felépítése}\label{sec:agentek-terv}

Minden agent egy önálló programmodul, amelynek bemenete és kimenete rögzített szerkezetű adat.
Ez teszi lehetővé, hogy az agenteket egyenként lehessen tesztelni, cserélni és mérni, és hogy
ugyanazok a modulok a nyilvános adathalmazon tömegesen, a laborban pedig riasztásonként is
futtathatók legyenek.
Az agentek feladatát, bemenetét és kimenetét \az{\ref{tab:agentek-terv}}. táblázat foglalja össze.

\subsubsection{Egységesítő agent}
A Suricata és a Wazuh eltérő szerkezetű riasztásokat állít elő, ezért az első agent ezeket közös
formára hozza (\ref{tab:kozos-forma}.~táblázat).
A közös forma minden olyan mezőt tartalmaz, amelyre a későbbi agenteknek szükségük van, az eredeti
rekordot pedig változatlanul megőrzi, hogy az elemző vissza tudja keresni.
A súlyossági szinteket a két eszköz eltérő skálán adja meg: a Wazuh 0-tól 15-ig terjedő
szabályszinteket használ~\cite{wazuhrules}, a Suricata pedig kis egész számmal jelzi a prioritást,
ahol az 1 a legsúlyosabb.
Az agent mindkettőt megőrzi, és a kockázati pontszám számításához 0 és 1 közé alakítja.
A nyilvános adathalmaz hálózati riasztásaiban nincs gépnév, ezért ezeknél az agent a cél- vagy
forrás-IP-cím alapján a gépnyilvántartásból keresi ki az érintett gépet.

\subsubsection{Csoportosító agent}
A csoportosító az összetartozó riasztásokat fogja össze.
Két riasztás akkor kerül egy csoportba, ha ugyanazt a gépet érintik -- gépnév vagy IP-cím alapján --,
és a köztük eltelt idő nem haladja meg a beállított értéket.
A csoport megőrzi a tagjai azonosítóját, így a riasztásszintű és a csoportszintű értékelés
ugyanabból az eredményből készülhet.
Az időköz értékét a nyilvános adathalmaz egyik forgatókönyvén választom ki, és a többin már
változatlanul alkalmazom.

\subsubsection{Környezeti és sérülékenységi agent}
A környezeti agent az érintett gép azonosítója alapján kikeresi a gép fontossági fokozatát és
megfigyeltségét, és kiszámolja a 4. fejezetben definiált két mérőszámot.
A sérülékenységi agent a riasztást kiváltó szabály hivatkozásait veti össze a gépen futó szoftverekkel,
és megadja a támadás alkalmazhatóságát.
Ha a gép vagy a szoftverkészlete nem szerepel a nyilvántartásban, mindkét agent a semleges értéket
adja, és ezt a kimenetben jelzi, hogy az elemző lássa: a pontszám részben hiányos adaton alapul.

\subsubsection{Rangsoroló agent}
A rangsoroló kiszámolja a riasztások kockázati pontszámát, majd a súlyozott összeget, végül a
csoportok pontszámát és sorrendjét.
A kimenet minden csoportnál tartalmazza az összetevőket is, vagyis azt, hogy a pontszámból mennyi
származik a riasztások folyamából, a gép fontosságából, az alkalmazhatóságból és a megfigyeltségből.
Ez teszi a sorrendet ellenőrizhetővé, és ebből dolgozik a magyarázó agent is.
```

### 5.1. táblázat – az agentek (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{Az agentek feladata, bemenete és kimenete (Forrás: saját összeállítás)}
    \label{tab:agentek-terv}
    \small
    \begin{tabular}{|L{2.4cm}|L{3.6cm}|L{3.6cm}|L{3.4cm}|}
        \hline
        \textbf{Agent} & \textbf{Bemenet} & \textbf{Kimenet} & \textbf{Megvalósítás} \\ \hline
        1. Egységesítő & Suricata- és Wazuh-riasztások & riasztások közös formában & kiszámítható program \\ \hline
        2. Csoportosító & egységesített riasztások & csoportok a tagok azonosítójával & kiszámítható program \\ \hline
        3. Környezet & csoportok, gépnyilvántartás & gép fontossága, megfigyeltség & kiszámítható program, adatbázis-lekérdezés \\ \hline
        4. Sérülékenységi & csoportok, szoftverkészlet, szabályhivatkozások & alkalmazhatóság & kiszámítható program, \acs{CPE}-illesztés \\ \hline
        5. Rangsoroló & mérőszámok, súlyok & pontszám, összetevők, sorrend & kiszámítható program \\ \hline
        6. Magyarázó & csoport és összetevői & rövid szöveges magyarázat & helyi nyelvi modell és ellenőrzés \\ \hline
        7. Vezérlő & a teljes állapot & lépéssorrend, napló, futásidők & Python, később LangGraph \\ \hline
    \end{tabular}
\end{table}
```

### 5.2. táblázat – a közös riasztásforma (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{Az egységesített riasztás mezői (Forrás: saját összeállítás)}
    \label{tab:kozos-forma}
    \small
    \begin{tabular}{|L{3.4cm}|L{10.2cm}|}
        \hline
        \textbf{Mező} & \textbf{Tartalom} \\ \hline
        időpont & a riasztás keletkezésének ideje, egységes időzónában \\ \hline
        forrás & melyik érzékelő adta (hálózati vagy gépi) \\ \hline
        szabály & a szabály azonosítója és neve \\ \hline
        súlyosság & az eredeti érték és a 0--1 közé alakított érték \\ \hline
        forrás- és cél-IP-cím & a hálózati kapcsolat két végpontja, ha van \\ \hline
        gép & az érintett gép neve; ha hiányzik, az IP-cím alapján kikeresve \\ \hline
        felhasználó & az érintett felhasználó, ha a riasztás tartalmazza \\ \hline
        sérülékenység & a szabály által hivatkozott \acs{CVE}-azonosítók listája (lehet üres) \\ \hline
        támadási technika & a szabályhoz rendelt MITRE ATT\&CK technika, ha van \\ \hline
        címke & mérésnél: a riasztás támadáshoz tartozik-e (csak értékeléshez, a rangsorolás nem látja) \\ \hline
        eredeti rekord & a nyers riasztás változatlanul, visszakereséshez \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a „címke” sor fontos módszertani pont – a rangsoroló **nem** láthatja (különben adat
szivárogna a tesztből). Ezt a kódban teszt is ellenőrzi majd.

```latex
\subsubsection{Magyarázó agent}
A magyarázó agent minden csoporthoz rövid, néhány mondatos összefoglalót ír az elemzőnek: mely gépet
érinti, milyen szabályok jeleztek, és miért került a csoport a lista adott helyére.
A szöveget helyben futó nyelvi modell állítja elő, így a naplóadatok nem hagyják el a szervezetet.
A modell kizárólag a csoport adatait és a rangsoroló által kiszámolt összetevőket kapja meg, egy
rögzített kérés-sablonba illesztve (\ref{fig:magyarazo}.~ábra).

A nyelvi modell hihető, de hamis állításokat is megfogalmazhat, ezért a kimenetet egy kiszámítható
ellenőrző lépés vizsgálja.
Az ellenőrzés kigyűjti a szövegből a gépneveket, IP-címeket, szabályneveket és számokat, és
megnézi, szerepelnek-e a csoport adataiban.
Ha a szöveg olyan adatot tartalmaz, amely a csoportban nincs, a modell egyszer újra próbálkozhat a
hibák megjelölésével; ha ez sem sikerül, a rendszer sablonból, nyelvi modell nélkül készít magyarázatot.
Így az elemző minden csoporthoz kap magyarázatot, és az soha nem tartalmazhat a csoportban nem szereplő
gépet vagy szabályt.
Ez a felépítés a nyelvi modell kimenetének független ellenőrzésére épülő újabb javaslatokat
követi~\cite{vallabhaneni2026sentinel}.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{img/magyarazo.pdf}
    \caption{A magyarázó agent belső lépései (Forrás: saját ábra)}
    \label{fig:magyarazo}
\end{figure}

\subsubsection{Vezérlő agent}
A vezérlő agent határozza meg a lépések sorrendjét, és adja tovább közöttük a közös állapotot.
Minden lépés kezdetét, végét, a feldolgozott tételek számát és a futásidőt naplózza.
A futásidő mérése azért fontos, mert a nyelvi modellt használó rendszerekben a teljes futásidő döntő
részét jellemzően a modell teszi ki~\cite{roy2026agentsoc,wei2025cortex}; a naplóból kiderül, mekkora
többletidővel jár a magyarázó agent.
A vezérlő a nyelvi modelltől semmilyen döntést nem vesz át: a lépések sorrendje rögzített, és
elágazás csak kiszámítható feltétel alapján történhet, például ha egy csoport pontszáma egy küszöb
alatt marad, nem kap magyarázatot.
```

---

## 5.4 A gépnyilvántartás

```latex
\subsection{A gépnyilvántartás}\label{sec:nyilvantartas}

A környezeti információt egy kis relációs adatbázis tárolja (\ref{fig:adatmodell}.~ábra).
A \emph{gép} tábla a gépek nevét, IP-címét, hálózati zónáját, szerepét és fontossági fokozatát
tartalmazza; a \emph{megfigyeltség} tábla gépenként azt, hogy fut-e rajta gépi érzékelő, és látja-e a
hálózati érzékelő.
A \emph{szoftver} tábla a gépeken futó termékeket és verzióikat szabványos szoftverazonosítóval
(\ac{CPE}) tárolja, a \emph{sérülékenység} tábla pedig az ismert sérülékenységeket és az érintett
szoftverazonosítókat.
A szabványos azonosító teszi lehetővé, hogy a gépet és a sérülékenységet külön kézi összerendelés
nélkül lehessen összekapcsolni~\cite{shi2024cpe}.
A \emph{szabályhivatkozás} tábla azt rögzíti, hogy egy érzékelőszabály melyik sérülékenységre vagy
melyik termékre, szolgáltatásra vonatkozik; ezt a sérülékenységi agent használja az alkalmazhatóság
meghatározásához.

A nyilvános adathalmazhoz a nyilvántartást a hálózat közzétett leírásából állítom össze; ott a
sérülékenységi táblák csak a termék- és szolgáltatásszintű illesztéshez szükséges adatokat
tartalmazzák~\cite{landauer2024aitads}.
A laborban a gépi érzékelő által gyűjtött szoftverkészletből és sérülékenységi adatokból töltöm fel.
A relációs adatbázist a gráfadatbázissal szemben azért választottam, mert a szükséges lekérdezések
egyszerűek, a táblák közvetlenül feltölthetők, és a prototípus így egyetlen fájlban tárolható.

\begin{figure}[H]
    \centering
    \includegraphics[width=\linewidth]{img/adatmodell.pdf}
    \caption{A gépnyilvántartás adatmodellje (Forrás: saját ábra)}
    \label{fig:adatmodell}
\end{figure}
```

Megjegyzés: a laborban a Wazuh sérülékenység-keresőjének adatait használnád – erre még nincs
hivatkozás a `.bib`-ben. Ha ezt a mondatot konkretizálod („a Wazuh sérülékenység-észlelő modulja”),
szólj, és felveszem a dokumentációt.

---

## 5.5 Az eszközök kiválasztása

```latex
\subsection{Az eszközök kiválasztása}\label{sec:eszkozok}

A megvalósítás három rétegből áll.
Az első réteg a mag: minden agent egy egyszerű Python-modul, külső keretrendszer nélkül.
Ezen futnak a nyilvános adathalmazon végzett mérések, mert így a több millió riasztás tömegesen,
táblázatos adatkezeléssel dolgozható fel, és a mérési eredményt nem befolyásolja a keretrendszer.
A második réteg a vezérlés: a magot a LangGraph könyvtár állapotgráfjába illesztem, amelyben az
agentek a gráf csomópontjai, a lépések sorrendjét pedig a gráf élei rögzítik~\cite{langgraph2025}.
Ebbe a rétegbe kerül a magyarázó agent is.
A harmadik, opcionális réteg a csatlakozó, amely a gépnyilvántartást csak olvasható formában teszi
elérhetővé a nyelvi modell számára~\cite{mcp2026spec}.

A rétegezés követelménye, hogy a vezérelt változat ugyanazt a sorrendet adja, mint a mag.
Ezt automatikus teszttel ellenőrzöm: ugyanarra a riasztáskészletre mindkét változat lefut, és a
pontszámoknak és a sorrendnek egyezniük kell.
Az eszközválasztás indoklását \az{\ref{tab:eszkozok}}. táblázat foglalja össze.

A vezérléshez azért nem választottam a beszélgetésre épülő agent-keretrendszereket, mert azokban a
lépések sorrendjét az agentek -- jellemzően nyelvi modellek -- közötti üzenetváltás alakítja
ki~\cite{wu2023autogen}, ami ellentétes a megismételhetőség követelményével.
A CrewAI újabb változatai már rögzített folyamatot is támogatnak~\cite{crewaidocs}, ennek előnye
azonban a nyelvi modellekből álló csapatok összehangolásában van, amelyre a tervezett rendszerben
nincs szükség.
A nyelvi modellt helyben, az Ollama futtatókörnyezettel futtatom~\cite{ollama}, mert így a naplóadatok
nem hagyják el a gépet, a futtatás nem jár díjjal, és a modell változata rögzíthető; a felhőben futó
szolgáltatások modelljei előzetes értesítés nélkül is változhatnak, ami a mérések megismételhetőségét
veszélyeztetné.
Kis, helyben futtatható nyelvi modellekkel korábban is végeztek riasztásvizsgálati kísérleteket
ugyanilyen futtatókörnyezetben~\cite{liu2026hesp}.
```

Megjegyzés: a „felhős modellek előzetes értesítés nélkül változhatnak” állítás általános tapasztalat;
ha forrást kérnek rá, szólj, és keresek. A konkrét modellt (pl. 7–8 milliárd paraméteres) a labor
gépének memóriája alapján később választjuk – ezt a 7. fejezet ütemezésébe teheted.

### 5.3. táblázat – az eszközválasztás (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{Az eszközök kiválasztása (Forrás: saját összeállítás)}
    \label{tab:eszkozok}
    \small
    \begin{tabular}{|L{2.2cm}|L{3.0cm}|L{3.9cm}|L{4.0cm}|}
        \hline
        \textbf{Feladat} & \textbf{Lehetőség} & \textbf{Mellette} & \textbf{Ellene} \\ \hline
        Vezérlés & \textbf{egyszerű Python (mag)} & tömeges mérés, nincs függőség, könnyen tesztelhető & a vezérlést, naplózást magunknak kell megírni \\ \cline{2-4}
         & \textbf{LangGraph (vezérlés)} & rögzített gráf, állapotmentés, újrajátszás & tanulási idő, átállási lépés \\ \cline{2-4}
         & AutoGen & rugalmas, sok példa & a sorrendet a beszélgetés alakítja \\ \cline{2-4}
         & CrewAI & nyelvimodell-csapatok egyszerű összehangolása & a rendszerben nincs ilyen csapat \\ \hline
        Nyelvi modell & \textbf{helyi (Ollama)} & az adat helyben marad, díjmentes, rögzíthető változat & kisebb modell, gyengébb szöveg, gépigény \\ \cline{2-4}
         & felhőszolgáltatás & erősebb modellek & az adat kikerül, díjas, a modell változhat \\ \hline
        Adattár & \textbf{SQLite} & egyetlen fájl, nincs kiszolgáló & egyszerre csak korlátozott írás \\ \cline{2-4}
         & PostgreSQL & többfelhasználós, nagy adatmennyiség & a prototípushoz túlméretezett \\ \cline{2-4}
         & gráfadatbázis & összetett kapcsolatok lekérdezése & a szükséges lekérdezések egyszerűek \\ \hline
        Csatlakozó & \textbf{\acs{MCP} (opcionális)} & szabványos, csak olvasható hozzáférés & elhagyható, ha kifut az idő \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a táblázat első oszlopában a csoportcím csak az első sorban áll – ez szándékos, így nem kell
hozzá külön csomag. A félkövér a választott lehetőség.

---

## 5.6 Összefoglalás

```latex
\subsection{Összefoglalás}

A tervezett rendszer hét, pontosan meghatározott feladatú agentből áll.
Az első öt agent kiszámítható program, ezek adják a pontszámot és a sorrendet; a magyarázó agent
helyben futó nyelvi modellel ír összefoglalót, amelyet független ellenőrzés vizsgál, a vezérlő pedig
rögzített sorrendben hangolja össze a lépéseket, és méri a futásidőt.
A környezeti információt egy kis relációs gépnyilvántartás tárolja, amelyet a gépeket és a
sérülékenységeket összekötő szabványos szoftverazonosító tesz egyszerűen lekérdezhetővé.
A megvalósítás rétegesen épül fel: a méréseket keretrendszer nélküli modulokon végzem, és teszttel
igazolom, hogy a vezérlőréteggel kiegészített változat ugyanazt az eredményt adja.
A következő fejezet a tesztkörnyezetet és az értékelés módszertanát mutatja be.
```

---

## Átvételkor figyelj

- Az ábrákat töltsd fel az `img/` mappába; a `\includegraphics` útvonala `img/...pdf`.
- A `\acs{...}` mindig a rövid alakot írja ki (táblázatban hasznos, ahol nem akarjuk a teljes nevet).
- Az 5.3. táblázatban a `\cline{2-4}` csak a 2–4. oszlop alá húz vonalat – így látszik a csoportosítás.

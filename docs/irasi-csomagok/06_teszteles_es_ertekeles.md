# Írási csomag – 6. fejezet: Tesztkörnyezet, tesztelés és értékelési módszertan

2026-10-24 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Feladatlap:** F5 – a rendszer tesztelése és értékelése (a terv a DM II.-ben, a mérés később).
- **Útmutató:** 8–9. pont – tesztelés, eredmények és összevetés (most: a módszertan).
- **Diplomamunka II.:** a tesztelés terve. Terjedelem: kb. **7–8 oldal** a laborábrával és három táblázattal.
- **Fájl:** `chapters/6_Teszteles.tex`; a `main.tex`-ben az 5. fejezet után (a `\label` kötelező, mert a
  4. fejezet hivatkozik rá):

```latex
\clearpage
\section{TESZTKÖRNYEZET ÉS ÉRTÉKELÉSI MÓDSZERTAN}\label{sec:ertekeles}
\input{chapters/6_Teszteles}
```

- **Áthelyezés:** a 4. csomagban előre megírt mérési terv (lépések, mérőszámok, plafonhatás, torzítás)
  ide került, a 4. csomagból kivettem. A blokkok szövege kis mértékben pontosodott.

## Ábra (Claude készítette, a jóváhagyásod után kerül be)

| Fájl | Mit mutat | Forrás |
| --- | --- | --- |
| `img/labor.pdf` | A tervezett labor: szimulált internet (támadó, háttérzaj), DMZ (sérülékeny WordPress, levelező), belső hálózat (egy gép szándékosan Wazuh-ügynök nélkül), megfigyelő és elemző zóna (Suricata, Wazuh-kezelő, riasztásfeldolgozó, Ollama); a támadási napló csak az értékeléshez jut el | `img/src/labor.tex` |

## Rövidítések

Nincs új; használt: AUROC, CVE, MCP, SOC.

## Források és ellenőrzöttségük

| Kulcs | Mire használjuk | Ellenőrzés |
| --- | --- | --- |
| `landauer2024aitads` | Az AIT-ADS felépítése: 8 forgatókönyv, Suricata, Wazuh, AMiner, többlépéses támadás, szimulált felhasználói viselkedés | Zenodo-adatlap és a CSET-előadás, 2026-10-24 |
| `landauer2023aitlds` | Az AIT-ADS alapja (AIT-LDSv2) | Korábban ellenőrizve |
| `uetz2026rba` | A hálózat mérete (9–27 kliens, DMZ, szimulált internet), a russellmitchell számai, az AMiner kihagyása, a forgatókönyv-választás, az azonos kezelési idő feltevése | Teljes szöveg, 6–7. és 4. oldal |
| `karner2026alertbert` | Zajjal bővített AIT-ADS | Korábban ellenőrizve |
| `arp2022` | Módszertani buktatók | Korábban ellenőrizve |
| CVE-2020-24186 | wpDiscuz 7.0.0–7.0.4, hitelesítés nélküli fájlfeltöltés → kódfuttatás; javítva a 7.0.5-ben | NVD-, Wordfence- és Debian-oldal, 2026-10-24. **Nincs `.bib`-bejegyzés** – ha a dolgozatban hivatkozol rá, szólj, és felveszem az NVD-oldalt (URL + megtekintési dátum) |

---

## 6.0 Nyitó bekezdés

```latex
Ez a fejezet azt mutatja be, hogyan ellenőrzöm a tervezett rendszer helyes működését, és hogyan
mérem, mennyit javít a riasztások rangsorán.
A rendszert két környezetben vizsgálom: egy nyilvános, felcímkézett riasztás-adathalmazon, amely a
szakirodalom eredményeivel való összevetést teszi lehetővé, és egy saját laboratóriumi
tesztkörnyezetben, ahol a környezeti információ teljes, és a körülmények szabályozhatók.
A fejezet a két környezet leírása után ismerteti a mérés tervét, a program tesztelésének módját,
végül azokat a tényezőket, amelyek az eredmények érvényességét korlátozhatják.
```

---

## 6.1 A nyilvános adathalmaz

```latex
\subsection{A nyilvános adathalmaz}\label{sec:aitads}

A mérések elsődleges adatforrása az AIT-ADS riasztás-adathalmaz~\cite{landauer2024aitads}.
Az adathalmaz egy kisvállalati hálózatot modellező tesztkörnyezetben készült, amelyben szimulált
felhasználók végzik a napi munkát, és ezzel párhuzamosan egy többlépéses támadás zajlik: felderítés,
webalkalmazás elleni támadás, jelszótörés, távoli parancsfuttatás és jogosultságszerzés.
A hálózat több felhasználói gépből, egy határvédelmi zónában elhelyezett kiszolgálókból és egy
szimulált internetes zónából áll~\cite{uetz2026rba}.
A támadást nyolc forgatókönyvben, eltérő beállításokkal játszották le, és a keletkező naplókból
három behatolásérzékelő -- a Suricata, a Wazuh és az AMiner -- riasztásait gyűjtötték össze.
Az adathalmaz egy korábbi, nyers naplókat tartalmazó adathalmazra épül, így a riasztások
keletkezése a naplókig visszakövethető~\cite{landauer2023aitlds}.

Az AMiner-riasztásokat nem használom, mert hiányzik belőlük a gépnév és a súlyossági szint; ezt a
döntést Uetz és szerzőtársai is ugyanígy hozták meg~\cite{uetz2026rba}.
A hálózati és a gépi riasztásokat külön adathalmazként kezelem, mert a kockázati pontszám
paraméterezése a kettőnél eltér.
A legkisebb forgatókönyvben (russellmitchell) 23\,116 gépi riasztás szerepel, ebből 7661 tartozik a
támadáshoz, valamint 9186 hálózati riasztás, ebből mindössze 44 támadási~\cite{uetz2026rba}.

A riasztásokhoz tartozó címkék két forrásból származnak.
Az adathalmaz kiadói a támadási lépések kezdő- és záróidőpontját adják meg, így egy riasztás akkor
számít támadásinak, ha a támadási időszakba esik.
Ez durva címkézés, mert a támadás ideje alatt keletkező jóindulatú riasztások is támadásinak
minősülnek.
A russellmitchell forgatókönyvhöz Uetz és szerzőtársai riasztásonként felcímkézett változatot is
közzétettek; ezen összevetem a kétféle címkét, és a különbséget a többi forgatókönyv eredményeinek
értelmezésénél figyelembe veszem.

Az adathalmazhoz nem tartozik gépnyilvántartás, ezért azt a hálózat közzétett leírásából állítom
össze: a gépek szerepét, hálózati zónáját, a futó szolgáltatásokat és a szoftververziókat.
A fontossági fokozatokat a 4. fejezetben rögzített szabályok alapján, a címkék megtekintése előtt
határozom meg.
```

Megjegyzés: a „címkék megtekintése előtt” mondat csak akkor igaz, ha valóban így csinálod – a
russellmitchell címkéit már láttuk (október 1.). Javaslat: a fontossági szabályokat a **szerepből**
származtasd (4.2. táblázat), ne a gépek listájából, és ezt így is írd le.

---

## 6.2 A laboratóriumi tesztkörnyezet

```latex
\subsection{A laboratóriumi tesztkörnyezet}\label{sec:labor}

A nyilvános adathalmaz két fontos korlátja, hogy riasztásai nem hivatkoznak ismert sérülékenységre,
és benne minden gép azonos módon megfigyelt.
Emiatt a támadás alkalmazhatósága csak termékszinten, a megfigyeltség hatása pedig egyáltalán nem
mérhető rajta.
Ezeket a mérőszámokat egy saját laboratóriumi tesztkörnyezetben vizsgálom, amelynek tervezett
felépítését \az{\ref{fig:labor}}. ábra mutatja.

A tesztkörnyezet az AIT-ADS hálózatának szerkezetét követi.
A gépek és a hálózati zónák virtuális gépként, a sérülékeny alkalmazások konténerként futnak.
A határvédelmi zónában egy WordPress-alapú webkiszolgáló üzemel a wpDiscuz bővítmény sérülékeny,
7.0.4-es változatával, amely hitelesítés nélküli fájlfeltöltést, és ezen keresztül távoli
kódfuttatást tesz lehetővé (CVE-2020-24186).
A belső hálózatban munkaállomások és egy fájlkiszolgáló működik, gépi érzékelővel.
Egy munkaállomáson szándékosan nem fut gépi érzékelő, és a hálózati érzékelő csak a határvédelmi zóna
forgalmát látja; így a megfigyeltség gépenként különbözik, és a hatása mérhetővé válik.

A támadásokat előre megírt forgatókönyvek hajtják végre egy külön támadó gépről, és minden lépés
kezdetét és végét időbélyeggel naplózzák.
Ebből a naplóból készülnek a címkék, amelyek kizárólag az értékeléshez jutnak el, a riasztásfeldolgozó
nem látja őket.
A jóindulatú háttérforgalmat egy zajgenerátor állítja elő -- webes böngészés, levelezés,
fájlműveletek, hibás bejelentkezések --, mert e nélkül szinte minden riasztás támadási lenne, és a
rangsorolás nem lenne értelmezhető.
A gépnyilvántartást a gépi érzékelő szoftverleltárából töltöm fel, így a laborban a \acs{CVE}-szintű illesztés is vizsgálható.
A nyelvi modell ugyanebben a környezetben, helyben fut, és itt mérem a magyarázó agent futásidejét is.

\begin{figure}[H]
    \centering
    \includegraphics[width=\linewidth]{img/labor.pdf}
    \caption{A laboratóriumi tesztkörnyezet tervezett felépítése (Forrás: saját ábra)}
    \label{fig:labor}
\end{figure}
```

Megjegyzés: a háttérzaj tartalmát (böngészés, levelezés, …) te döntsd el – ez most javaslat. Az ábrán a
„Levelező kiszolgáló” is javaslat; ha nem lesz, szólj, és kiveszem. A labor erőforrása (64–128 GB RAM)
ide is beírható egy mondatban.

### 6.1. táblázat – a két környezet összevetése (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A két tesztkörnyezet összevetése (Forrás: saját összeállítás)}
    \label{tab:kornyezetek}
    \small
    \begin{tabular}{|L{3.4cm}|L{5.0cm}|L{5.0cm}|}
        \hline
        \textbf{Szempont} & \textbf{AIT-ADS} & \textbf{Saját labor} \\ \hline
        Riasztások & Suricata és Wazuh, 8 forgatókönyv & Suricata és Wazuh, saját forgatókönyvek \\ \hline
        Címkék & a támadási időszakok alapján (egy forgatókönyvhöz riasztásonként is) & a támadási napló időbélyegei alapján \\ \hline
        Gép fontossága & a hálózatleírásból összeállítva & a tervezett szerepekből \\ \hline
        Alkalmazhatóság & termék- és szolgáltatásszinten & \acs{CVE}-szinten is \\ \hline
        Megfigyeltség & minden gépen azonos & gépenként eltérő, szándékosan \\ \hline
        Erőssége & nyilvános, összevethető a szakirodalommal & teljes környezeti információ, szabályozható \\ \hline
        Gyengesége & durva címkék, hiányos környezet & mesterséges háttérforgalom \\ \hline
    \end{tabular}
\end{table}
```

---

## 6.3 A mérés terve

```latex
\subsection{A mérés terve}\label{sec:meresterv}

A mérőszámok hozzájárulását lépésenkénti bővítéssel vizsgálom (\ref{tab:lepesek}.~táblázat).
A kiindulópont a rangsor nélküli riasztáslista, majd a súlyosság szerinti sorrend és a csoportosítás
következik.
A harmadik lépés a kockázatalapú pontozás, amely a dolgozat összehasonlítási alapja; ennél a lépésnél
azt is ellenőrzöm, hogy a saját megvalósítás a közölt értékeket adja-e.
Ezután egyenként adom hozzá a gép fontosságát, az alkalmazhatóságot és a megfigyeltséget, így minden
lépés közvetlenül megmutatja az új információ hatását.

A rangsor minőségét három mérőszámmal értékelem.
A rangsor-pontosság (\ac{AUROC}) annak valószínűsége, hogy egy véletlenszerűen választott valódi
riasztás a rangsorban egy téves riasztás elé kerül.
Az átlagos pontosság azt méri, mennyire tiszta a lista eleje, ezért erősebben bünteti a lista első
helyein álló téves riasztásokat.
A harmadik mérőszám a lista első tíz százalékába kerülő valódi riasztások aránya, amely azt modellezi,
amikor az elemzőnek csak a lista elejére van ideje.
A terhelés csökkenését úgy számolom, hogy megkeresem azt a legrövidebb listarészt, amely a valódi
támadásokhoz tartozó riasztások legalább 98\%-át tartalmazza, és megadom, a teljes lista hányad
részét kell így átnézni.
A csoportosítás minőségét a csoportok tisztaságával mérem, vagyis azzal, hogy egy csoportba csak egy
támadási lépés riasztásai kerülnek-e.

A különbségek statisztikai vizsgálatára párosított, egyoldali Wilcoxon-próbát alkalmazok, amely nem
feltételez normális eloszlást; a párokat az AIT-ADS nyolc forgatókönyve adja, a hálózati és a gépi
riasztásokra külön-külön.
Nyolc pár esetén a próba legkisebb elérhető p-értéke $1/2^8 \approx 0{,}004$, ezért szignifikáns
eredmény csak akkor adódik, ha a javulás a forgatókönyvek többségében következetesen jelentkezik.
```

### 6.2. táblázat – a lépések (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A lépésenkénti értékelés lépései (Forrás: saját összeállítás)}
    \label{tab:lepesek}
    \small
    \begin{tabular}{|L{1.2cm}|L{5.2cm}|L{7.2cm}|}
        \hline
        \textbf{Lépés} & \textbf{Rangsorolás alapja} & \textbf{Mit mutat meg} \\ \hline
        0 & nincs rangsor & a kiindulási terhelést \\ \hline
        1 & szabályszint (súlyosság) & a mai, egyszerű gyakorlatot \\ \hline
        2 & csoportosítás, csoportonként a legmagasabb súlyosság & a csoportosítás hatását \\ \hline
        3 & kockázati pontszám ($r_i$) & az erős, környezetet nem használó alapot \\ \hline
        4 & $r_i$ + gép fontossága & a gépnyilvántartás hozzájárulását \\ \hline
        5 & 4. lépés + alkalmazhatóság & a szoftverkészlet hozzájárulását \\ \hline
        6 & 5. lépés + megfigyeltség & a teljes modellt (a megfigyeltség csak a laborban) \\ \hline
    \end{tabular}
\end{table}
```

```latex
\subsubsection{A plafonhatás kezelése}

Uetz és szerzőtársai az AIT-ADS-ből csak egyetlen forgatókönyvet vizsgáltak, és azon a kockázatalapú
pontozás rangsor-pontossága a gépi riasztásoknál 0,98, a hálózati riasztásoknál 0,99
volt~\cite{uetz2026rba}.
Ha ez a többi forgatókönyvre is jellemző, a rangsor-pontosság alig hagy teret a javulásnak, és a
környezeti mérőszámok hatása ezzel a mérőszámmal nem mutatható ki.
Ezért a mérést mind a nyolc forgatókönyvön elvégzem, és nagyobb súlyt adok azoknak a mérőszámoknak,
amelyek a lista elejére érzékenyek, vagyis az átlagos pontosságnak és a terheléscsökkentésnek.
Ezen felül a riasztásokat az AIT-ADS zajjal kiegészített változatán~\cite{karner2026alertbert} is
rangsorolom, ahol a jóindulatú riasztások aránya többszöröse az eredetinek, valamint a laboratóriumi
tesztkörnyezetben, ahol a környezeti információ teljes.

\subsubsection{A torzítás elleni védekezés}\label{sec:torzitas}

A környezeti mérőszámok legnagyobb módszertani kockázata, hogy a kutató a támadások ismeretében --
akár öntudatlanul -- úgy állítja be a gépek fontosságát vagy a súlyokat, hogy az eredmény kedvezőbb
legyen.
Ez a tesztadatból származó információ beszivárgásának egyik formája, amelyet a biztonsági tárgyú
gépi tanulási kutatások egyik gyakori hibájaként tartanak számon~\cite{arp2022}.
Ennek elkerülésére négy intézkedést teszek.
A gépek fontossági szabályait és a páros összehasonlítás ítéleteit a mérés előtt rögzítem, és a
rögzítés időpontját a verziókezelő rendszer naplója igazolja.
A súlyok hatását $\pm 20\%$-os érzékenységvizsgálattal ellenőrzöm.
A szakértői súlyokat adatból tanult súlyokkal is összevetem, amelyeket hét forgatókönyvön tanítok, és a
kihagyott nyolcadikon mérek.
Végül ellenpróbát végzek: a gépek fontossági fokozatait véletlenszerűen összekeverem, és megvizsgálom,
hogy az így kapott, értelmetlen nyilvántartás is javít-e a rangsoron.
Ha igen, a javulás nem a környezeti információnak, hanem a pontszám szerkezetének köszönhető.

A nyilvántartás hiányosságainak hatását is mérem: a gépek egy részét -- 20, illetve 50 százalékát --
véletlenszerűen eltávolítom a nyilvántartásból, és megvizsgálom, mennyit romlik a rangsor.
A semleges értékek miatt a rangsor várhatóan fokozatosan közelít a kockázatalapú pontozáséhoz, de nem
lesz annál rosszabb.

\subsubsection{A magyarázó agent értékelése}

A magyarázó agent nem befolyásolja a sorrendet, ezért külön értékelem.
Három mennyiséget mérek: hány magyarázat felel meg elsőre az ellenőrzésnek, hányszor kell a
sablonalapú tartalékot használni, és mennyi a magyarázat elkészítésének átlagos ideje csoportonként.
Ezen felül véletlenszerűen kiválasztott csoportok magyarázatait magam is átnézem, és rögzítem, hogy a
szöveg helytálló, teljes és az elemző számára hasznos-e.
Ez utóbbi szubjektív értékelés, ezért csak kiegészítő jellegű.
```

### 6.3. táblázat – mit mérünk és hol (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A mérések összefoglalása (Forrás: saját összeállítás)}
    \label{tab:meresek}
    \small
    \begin{tabular}{|L{4.0cm}|L{5.6cm}|L{1.7cm}|L{1.7cm}|}
        \hline
        \textbf{Kérdés} & \textbf{Mérőszám} & \textbf{AIT-ADS} & \textbf{Labor} \\ \hline
        Javul-e a rangsor? & rangsor-pontosság, átlagos pontosság, első 10\% & igen & igen \\ \hline
        Csökken-e a terhelés? & átnézendő listarész 98\%-os találatnál & igen & igen \\ \hline
        Jók-e a csoportok? & a csoportok tisztasága & igen & igen \\ \hline
        Valódi-e a környezet hatása? & ellenpróba összekevert fontossággal & igen & igen \\ \hline
        Mennyire érzékeny a súlyokra? & $\pm 20\%$ súlyváltozás, tanult súlyok & igen & -- \\ \hline
        Bírja-e a hiányos adatot? & 20 és 50\% eltávolított gép & igen & igen \\ \hline
        Megfigyeltség hatása & lépés 6 vs. lépés 5 & -- & igen \\ \hline
        Magyarázatok minősége & elsőre helyes arány, tartalék aránya, futásidő & -- & igen \\ \hline
    \end{tabular}
\end{table}
```

---

## 6.4 A program tesztelése

```latex
\subsection{A program tesztelése}\label{sec:szoftverteszt}

A mérési eredmények csak akkor hihetők, ha a program helyesen számol.
Ezért minden agenthez automatikus egységtesztek készülnek, amelyek kis, kézzel ellenőrizhető
bemeneteken vizsgálják a kimenetet: például hogy az egységesítő minden mezőt helyesen tölt-e ki, vagy
hogy a csoportosító a megadott időközön belüli riasztásokat egy csoportba teszi-e.
Három tesztcsoport kiemelt jelentőségű.
Az első azt ellenőrzi, hogy a kockázati pontszám saját megvalósítása ugyanazokat az értékeket adja-e,
mint a szerzők nyilvános eszköze ugyanarra a forgatókönyvre.
A második azt, hogy a vezérlőréteggel kiegészített változat pontosan ugyanazt a sorrendet adja-e, mint
a keretrendszer nélküli mag.
A harmadik azt, hogy a támadás-címke semmilyen úton nem jut el a rangsorolóhoz; ez a teszt az
adatszivárgás egyik leggyakoribb formáját zárja ki.

Az eredmények megismételhetősége érdekében minden mérés rögzíti a program verzióját, a felhasznált
adatfájlok ellenőrzőösszegét, a súlyokat és a véletlenszám-generátor kezdőértékét.
A nyelvi modellnél a modell pontos változatát és a mintavételi beállításokat is rögzítem.
A mérési eredmények a verziókezelt tárolóban, a programmal együtt kerülnek tárolásra.
```

---

## 6.5 Az érvényességet korlátozó tényezők

```latex
\subsection{Az érvényességet korlátozó tényezők}\label{sec:korlatok}

A mérések tervezésekor több olyan tényezővel számolok, amely az eredmények érvényességét
korlátozhatja (\ref{tab:korlatok}.~táblázat).
Az egyik a címkék pontatlansága: a nyilvános adathalmaz időszak alapú címkéi a támadás alatt keletkezett
jóindulatú riasztásokat is támadásinak tekintik.
A másik, hogy mindkét tesztkörnyezet mesterséges: a felhasználói viselkedést program szimulálja, ezért a
jóindulatú riasztások összetétele eltérhet egy valós szervezetétől.
A harmadik a szakértői döntések szubjektivitása, amelyet \az{\ref{sec:torzitas}}. alfejezetben leírt
intézkedések mérsékelnek.
Végül a terheléscsökkentés számítása azt feltételezi, hogy minden riasztás kivizsgálása ugyanannyi időt
vesz igénybe; ezt a feltevést Uetz és szerzőtársai is alkalmazták, mert a riasztásonkénti kezelési időre
nincs elfogadott becslési modell~\cite{uetz2026rba}.
```

### 6.4. táblázat – korlátok és kezelésük (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{Az érvényességet korlátozó tényezők és kezelésük (Forrás: saját összeállítás)}
    \label{tab:korlatok}
    \small
    \begin{tabular}{|L{3.6cm}|L{4.8cm}|L{5.2cm}|}
        \hline
        \textbf{Tényező} & \textbf{Hatás} & \textbf{Kezelés} \\ \hline
        Időszak alapú címkék & téves riasztás támadásinak számít & összevetés a riasztásonként címkézett forgatókönyvvel \\ \hline
        Mesterséges környezet & a jóindulatú riasztások eltérhetnek a valóstól & két különböző környezet; zajjal bővített változat \\ \hline
        Szakértői súlyok és fokozatok & a kutató torzíthat & előzetes rögzítés, érzékenységvizsgálat, ellenpróba \\ \hline
        Plafonhatás & a javulás nem látszik & nyolc forgatókönyv, a lista elejére érzékeny mérőszámok \\ \hline
        Azonos kezelési idő & a terhelés becslése durva & a szakirodalmi gyakorlat követése, a korlát jelzése \\ \hline
        Kis mintaszám (8 forgatókönyv) & gyenge statisztikai erő & nem paraméteres próba, hatásnagyság közlése \\ \hline
    \end{tabular}
\end{table}
```

---

## 6.6 Összefoglalás

```latex
\subsection{Összefoglalás}

A rendszert két, egymást kiegészítő környezetben értékelem.
A nyilvános AIT-ADS adathalmaz nyolc forgatókönyve a szakirodalom legerősebb eredményével való
közvetlen összevetést teszi lehetővé, a laboratóriumi tesztkörnyezet pedig azokat a mérőszámokat is
vizsgálhatóvá teszi, amelyekhez a nyilvános adat nem elegendő.
A mérés lépésenként bővülő modellváltozatokat hasonlít össze, a lista elejére érzékeny mérőszámokat
is használva, és ellenpróbával ellenőrzi, hogy a javulás valóban a környezeti információból ered.
A program helyességét automatikus tesztek, az eredmények megismételhetőségét a beállítások rögzítése
biztosítja.
```

---

## Átvételkor figyelj

- A `\label{sec:ertekeles}` a fejezetcímnél kell (a 4. fejezet hivatkozik rá).
- Az ábrát töltsd fel az `img/` mappába (`img/labor.pdf`).
- A „hatásnagyság közlése” (6.4. táblázat) azt jelenti, hogy a p-érték mellett a javulás mértékét is
  megadod (pl. átlagos különbség) – erről a 7. fejezetben lesz szó.

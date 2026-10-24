# Írási csomag – 4. fejezet: A megoldás kiválasztása és a mérőszámrendszer

2026-10-23 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Feladatlap:** F3 – a választott megoldás indoklása és a mérőszámrendszer kidolgozása.
- **Útmutató:** 4–5. pont – a megoldási módszer kiválasztása és indoklása, részletes specifikáció.
- **Diplomamunka II.:** 4. pont – a saját megoldás specifikációja. Terjedelem: kb. **6–7 oldal**
  (a mérési terv nélkül, amely a 6. fejezetbe kerül).
- **Vezérfonal:** a 3. fejezet résein (3.4. táblázat) indulunk; itt dől el *mi* és *miért*, a
  megvalósítás (agentek, eszközök) az 5. fejezet.
- **Fájl:** `chapters/4_Megoldas.tex`; a `main.tex`-ben a 3. fejezet után:

```latex
\clearpage
\section{A MEGOLDÁS KIVÁLASZTÁSA ÉS A MÉRŐSZÁMRENDSZER}\label{sec:megoldas}
\input{chapters/4_Megoldas}
```

## Rövidítések, amelyek ebben a fejezetben kellenek (`acronyms.tex`)

```latex
\DeclareAcronym{CVE}{
  short = CVE,
  long  = Common Vulnerabilities and Exposures
}
\DeclareAcronym{CPE}{
  short = CPE,
  long  = Common Platform Enumeration
}
```

Megjegyzés: az AHP, CVSS, AUROC, RBA már megvan nálad.

## Források és ellenőrzöttségük

| Kulcs | Mire használjuk | Ellenőrzés |
| --- | --- | --- |
| `uetz2026rba` | A riasztásból számolt öt részpontszám, az ablakok, a súlyok, a kiértékelés; **a környezeti módosítókat szándékosan nem vizsgálták** | Teljes szöveg alapján, 2026-10-23 (4., 6., 8–11. és 20. oldal) |
| `saaty1990` | **Új.** Páros összehasonlítás, következetességi arány, véletlen index | EJOR 48(1), 9–26, 1990. szeptember – több független forrás. A DOI másodlagos hivatkozásból: **a kiadói oldalon nézd meg** |
| `anuar2012` | Páros összehasonlítás a riasztások rangsorolásában | Korábban ellenőrizve (2013) |
| `jalalvand2024` | A rangsorolási szempontok rendszerezése | Általános hivatkozásként |
| `porras2002`, `kruegel2004verification`, `valeur2004` | A gép fontossága; a támadás alkalmazhatósága | Korábban ellenőrizve |
| `njogu2012`, `sommestad2015` | A szűrés kockázata | Korábban ellenőrizve |
| `chamkar2024` | Megfigyeltség (lefedettség) | Kiadói adatlap |
| `shi2024cpe` | A CVE–CPE kapcsolat | Kiadói adatlap |
| `landauer2024aitads`, `karner2026alertbert`, `arp2022`, `ndichu2026` | Adathalmaz, zajos változat, módszertani buktatók | Korábban ellenőrizve |

A `saaty1990` bejegyzés bekerült a `references.bib`-be.

---

## 4.0 Nyitó bekezdés

```latex
Az előző fejezet összehasonlítása azt mutatta, hogy a meglévő módszerek mindegyike a probléma egy
részét kezeli, és mindegyiknek van olyan gyengesége, amely a gyakorlati használatot korlátozza.
Ebben a fejezetben először azt indokolom, melyik megközelítésre épül a dolgozatban tervezett
rendszer, majd részletesen leírom a mérőszámokat, azok összevonásának módját és azt, hogyan
mérem a rendszer hatását.
A fejezet célja, hogy a mérőszámrendszer a megvalósítás előtt egyértelműen rögzítve legyen:
minden mérőszám definíciója, értékkészlete és adatforrása itt szerepel, így a későbbi mérések
eredménye nem befolyásolhatja a választásokat.
```

---

## 4.1 A megközelítés kiválasztása

```latex
\subsection{A megközelítés kiválasztása}\label{sec:valasztas}

A választáshoz öt követelményt fogalmaztam meg.
A rendszernek tanítóadat nélkül is működnie kell, mert a valós \ac{SOC}-okban felcímkézett riasztás
alig áll rendelkezésre.
Az eredménynek megismételhetőnek kell lennie: ugyanarra a bemenetre mindig ugyanazt a sorrendet kell
adnia, különben a mérések nem vethetők össze.
A rendszernek fel kell használnia a környezetre vonatkozó információt, hiszen ez a dolgozat kutatási
kérdése.
A riasztásokat nem szabad eltávolítania, csak a sorrendjüket módosíthatja, mert a hiányos
nyilvántartás miatti szűrés valódi támadást is elrejthet~\cite{sommestad2015}.
Végül a sorrend indokának az elemző számára követhetőnek kell lennie.

\Az{\ref{tab:valasztas}}. táblázat a 3. fejezetben bemutatott módszercsaládokat veti össze ezekkel a
követelményekkel.
Egyik meglévő megközelítés sem teljesíti mind az ötöt: a kockázatalapú pontozás négyet teljesít, de a
környezetet nem használja; a környezetre épülő ellenőrzés használja a környezetet, de szűr.
A választott megoldás ezért a kockázatalapú pontozást veszi alapul, és azt egészíti ki három környezeti
mérőszámmal úgy, hogy azok csak a pontszámot módosítják, riasztást nem távolítanak el.
A mérőszámokat súlyozott összeggel vonom össze, a súlyokat páros összehasonlítással határozom meg.
A nagy nyelvi modell ebben a folyamatban nem vesz részt; szerepe a sorrend utólagos, szöveges
magyarázatára korlátozódik, amelyet az 5. fejezet tárgyal.
```

### 4.1. táblázat – a választás indoklása (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A módszercsaládok összevetése a megoldással szemben támasztott követelményekkel (Forrás: saját összeállítás)}
    \label{tab:valasztas}
    \small
    \begin{tabular}{|L{3.4cm}|L{1.5cm}|L{1.8cm}|L{1.6cm}|L{1.7cm}|L{1.9cm}|}
        \hline
        \textbf{Módszercsalád} & \textbf{Tanítás nélkül} & \textbf{Megismé\-telhető} & \textbf{Környe\-zet} & \textbf{Nem szűr} & \textbf{Követhető indok} \\ \hline
        Súlyosság szerint & igen & igen & nem & igen & igen \\ \hline
        Többszempontú (\ac{AHP}, fuzzy) & igen & igen & igen & igen & igen, de régi adaton mérve \\ \hline
        Környezet és ellenőrzés & igen & igen & igen & nem & igen \\ \hline
        Kockázatalapú pontozás & igen & igen & nem & igen & igen \\ \hline
        Tanuló, származáskövető & nem & részben & részben & igen & nehezen \\ \hline
        Nyelvimodell-agentek & igen & nem & részben & igen & szövegesen, ellenőrizetlenül \\ \hline
        \textbf{Választott megoldás} & \textbf{igen} & \textbf{igen} & \textbf{igen} & \textbf{igen} & \textbf{igen} \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a „Többszempontú” sor majdnem mindent teljesít – ezért a választott megoldás valójában
a kockázatalapú pontozás és a többszempontú súlyozás **egyesítése**. Ezt a mondatot érdemes saját
szavaiddal kiemelni, mert ez a dolgozat egyik újdonsága.

---

## 4.2 A mérőszámrendszer felépítése

```latex
\subsection{A mérőszámrendszer felépítése}\label{sec:metrikak}

A mérőszámrendszer két rétegből áll.
Az első réteg a riasztások folyamából számolt kockázati pontszám, amelyet változtatás nélkül veszek át
Uetz és szerzőtársai munkájából~\cite{uetz2026rba}; ez biztosítja, hogy az eredmény közvetlenül
összevethető legyen a nyilvánosan mért legerősebb módszerrel.
A második réteg három környezeti mérőszám: az érintett gép fontossága, a támadás alkalmazhatósága az
adott gépen, valamint a gép megfigyeltsége.
A szempontok kiválasztásánál a riasztás-rangsorolás szakirodalmának rendszerezésére
támaszkodtam~\cite{jalalvand2024}.
Minden mérőszám értéke 0 és 1 közé esik, ahol a nagyobb érték nagyobb kockázatot jelez.
A mérőszámok összefoglalását \az{\ref{tab:metrikak}}. táblázat tartalmazza.

\subsubsection{A riasztásokból számolt kockázati pontszám}

Az átvett pontszám öt részből áll, amelyek mindegyike egy-egy feltevést fejez ki arról, mi
különbözteti meg a támadást a jóindulatú működéstől~\cite{uetz2026rba}.
A \emph{szabályszint} a riasztást kiváltó szabály súlyossági fokozatát alakítja át 0 és 1 közötti
értékké.
A \emph{halmozódás} azt méri, hány riasztás érinti ugyanazt a gépet egy rövid, egyperces
időablakban.
A \emph{változatosság} azt, hogy egyórás ablakban hány különböző szabály jelzett ugyanarra a gépre.
A \emph{ritkaság} és a \emph{szabálytalanság} egynapos ablakban azt vizsgálja, mennyire szokatlan,
illetve mennyire nem ismétlődő mintázatú az adott riasztástípus.
Az időablakok a riasztás időpontjára középre igazítottak és háromszög alakúak, vagyis a távolabbi
riasztások kisebb súllyal számítanak.
A gépet a gépi érzékelő riasztásainál a gépnév, a hálózati érzékelő riasztásainál a forrás-IP-cím
azonosítja.
A szerzők az öt részpontszámot súlyozott számtani középpel vonták össze, és a súlyokat nyolc
adathalmazon, egy adathalmaz kihagyásával optimalizálták; az így kapott átlagos súlyok rendre
12, 24, 44, 10 és 10 százalék.
A dolgozatban ezt a beállítást használom, és az $i$-edik riasztás kockázati pontszámát $r_i$-vel
jelölöm.

Fontos megjegyezni, hogy Uetz és szerzőtársai a gépekre vagy felhasználókra vonatkozó
módosító tényezőket szándékosan kihagyták a vizsgálatból, mert azok megadása szerintük nagyrészt
szubjektív, és torzíthatja az eredményt, ha a kutató ismeri az adathalmazban szereplő
támadásokat~\cite{uetz2026rba}.
A dolgozat éppen ezt a kihagyott területet vizsgálja, ezért a torzítás elleni védekezést a
mérőszámok definíciójába is beépítettem, a mérési tervben pedig ellenpróbával ellenőrzöm
(\ref{sec:ertekeles}.~fejezet).
```

```latex
\subsubsection{A gép fontossága}

A gép fontossága azt fejezi ki, mekkora kárt okozna a szervezetnek, ha az adott gépet sikeres
támadás érné.
Ezt a szempontot már a korai, küldetésre gyakorolt hatást vizsgáló rangsorolók is
használták~\cite{porras2002}, és a páros összehasonlításra épülő kockázati indexek egyik fő
összetevője~\cite{anuar2012}.
A fontosságot ötfokú skálán adom meg, és a $g_i = (k_i - 1)/4$ képlettel alakítom 0 és 1 közötti
értékké, ahol $k_i$ az $i$-edik riasztás által érintett gép fokozata.

A fokozatot nem gépenként, egyedi mérlegelés alapján határozom meg, hanem a gép szerepéből és
hálózati helyéből, előre rögzített szabályok szerint (\ref{tab:fontossag}.~táblázat).
Ennek két oka van.
Egyrészt így a besorolás megismételhető, és egy másik szervezet is alkalmazhatja a saját
nyilvántartására.
Másrészt a szabályok a gépek szerepéből, és nem a támadások ismeretéből indulnak ki, ami csökkenti a
torzítás veszélyét.
Ha egy gép nem szerepel a nyilvántartásban, a fontossága a semleges $g_i = 0{,}5$ értéket kapja, így a
hiányos nyilvántartás sem előre, sem hátra nem sorolja a riasztást.
```

### 4.2. táblázat – a gép fontosságának szabályai (Claude készítette, átvehető; a fokozatokat te döntsd el)

```latex
\begin{table}[H]
    \centering
    \caption{A gépek fontossági fokozatának meghatározása szerep és hálózati hely alapján (Forrás: saját összeállítás)}
    \label{tab:fontossag}
    \small
    \begin{tabular}{|L{1.4cm}|L{6.6cm}|L{5.6cm}|}
        \hline
        \textbf{Fokozat} & \textbf{Szabály} & \textbf{Példa} \\ \hline
        5 & Az internet felől elérhető kiszolgáló, amely üzleti adatot tárol vagy felhasználókat azonosít & nyilvános webkiszolgáló adatbázissal, távoli elérést biztosító átjáró \\ \hline
        4 & Belső kiszolgáló, amelytől sok más gép vagy felhasználó működése függ & címtár, levelezés, belső fájlmegosztás \\ \hline
        3 & Belső kiszolgáló korlátozott felhasználói körrel & belső wiki, fejlesztői kiszolgáló \\ \hline
        2 & Felhasználói munkaállomás & irodai kliensgépek \\ \hline
        1 & Teszt- vagy ideiglenes gép, üzleti adat nélkül & tesztkörnyezet \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: ez **javaslat**, a fokozatokat a mérés előtt neked kell véglegesítened (szakértőként).
A szabályokat az AIT-ADS hálózatleírásának **elolvasása
előtt** érdemes rögzíteni (lásd lent: „A torzítás elleni védekezés”).

```latex
\subsubsection{A támadás alkalmazhatósága}

A második környezeti mérőszám azt vizsgálja, működhet-e egyáltalán a riasztásban jelzett támadás az
érintett gépen.
Ez a riasztás-ellenőrzés gondolatán alapul~\cite{kruegel2004verification,valeur2004}, de attól
eltérően nem dönt a riasztás sorsáról, csak a pontszámát módosítja.
Az alkalmazhatóság értéke háromféle lehet: $a_i = 1$, ha a gépen fut olyan szoftver, amelynek ismert
sérülékenységére (\ac{CVE}) a riasztást kiváltó szabály hivatkozik; $a_i = 0{,}75$, ha csak a termék
vagy a szolgáltatás egyezik (például webes támadás webkiszolgálót futtató gépen); és $a_i = 0{,}25$,
ha a gép ismert szoftverkészlete alapján a támadás nem alkalmazható.
Ha a gép szoftverkészlete nem ismert, a mérőszám a semleges $a_i = 0{,}5$ értéket kapja.

Az illesztéshez a gépeken futó szoftvereket szabványos szoftverazonosítóval (\ac{CPE}) tartom nyilván,
mert a sérülékenység-adatbázisok ugyanezzel az azonosítóval kötik a sérülékenységet az érintett
termékekhez~\cite{shi2024cpe}.
A nem alkalmazható támadás azért nem kap nulla értéket, mert a nyilvántartás hibája esetén a
riasztásnak a lista hátsó részében is láthatónak kell maradnia; a szűrésre épülő módszerek fő
gyengesége éppen az volt, hogy ilyenkor a valódi támadás is eltűnik~\cite{njogu2012,sommestad2015}.
A nyilvános AIT-ADS adathalmaz riasztásai nem hivatkoznak sérülékenység-azonosítóra, ezért ott csak a
termék- és szolgáltatásszintű illesztés mérhető; a sérülékenység-azonosító szintű illesztést a saját
tesztkörnyezetben vizsgálom.
```

Megjegyzés: a 0,25 / 0,5 / 0,75 / 1 lépcsőket én javaslom (a korábbi „1 / 0,5 / 0” helyett), mert így
az ismeretlen gép (0,5) pontosan középen van, és a nem alkalmazható támadás sem nullázódik. Ha az
eredeti, háromlépcsős változatot szeretnéd, szólj – az új döntést a `docs/dontesek.md`-be is felírom.

```latex
\subsubsection{A megfigyeltség}

A harmadik környezeti mérőszám azt írja le, mennyire látják az érintett gépet a megfigyelőeszközök.
A megfigyelési lefedettség a \ac{SOC}-ok működésének egyik ismert hiányossága~\cite{chamkar2024}, és a
kockázatalapú pontozásra közvetlen hatással van: a halmozódás és a változatosság annál nagyobb, minél
több érzékelő jelez ugyanarra a gépre.
Egy gyengén megfigyelt gépen ugyanaz a támadás kevesebb riasztást vált ki, ezért a pontszáma
alacsonyabb lesz, holott a kockázat nem kisebb, csak kevésbé látható.

A lefedettséget gépenként két jellemzőből számolom: fut-e a gépen működő gépi érzékelő, és látja-e a
hálózati érzékelő a gép hálózati szegmensét.
A $c_e$ lefedettség a teljesülő feltételek aránya, értéke 0, 0,5 vagy 1.
A mérőszám ennek a kiegészítője, $m_i = 1 - c_{e(i)}$, vagyis a kevésbé látható gép riasztásai kissé
előrébb kerülnek, ellensúlyozva a halmozódás és a változatosság alulbecslését.
A nyilvános adathalmazban minden gép azonos módon megfigyelt, ezért ott ez a mérőszám állandó, és a
hatása csak a saját tesztkörnyezetben mérhető, ahol a lefedettséget szándékosan változtathatom.
```

Megjegyzés: ez a döntés új (eddig csak „bizonytalansági jelző” volt). A logikája: a kockázatalapú
pontozás a sok érzékelőt jutalmazza, a vakfoltos gépet bünteti – ezt egyenlíti ki. Ha inkább csak
megjelenítenéd az elemzőnek (pontszám nélkül), az is védhető; szólj, és átírom.

### 4.3. táblázat – a mérőszámok összefoglalása (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A mérőszámrendszer elemei (Forrás: saját összeállítás, a kockázati pontszám \cite{uetz2026rba} alapján)}
    \label{tab:metrikak}
    \small
    \begin{tabular}{|L{2.4cm}|L{3.4cm}|L{2.4cm}|L{2.7cm}|L{1.9cm}|}
        \hline
        \textbf{Mérőszám} & \textbf{Jelentés} & \textbf{Értékek} & \textbf{Adatforrás} & \textbf{AIT-ADS} \\ \hline
        Kockázati pontszám ($r_i$) & öt részpontszám súlyozott átlaga: szabályszint, halmozódás, változatosság, ritkaság, szabálytalanság & 0--1, folytonos & riasztások & mérhető \\ \hline
        Gép fontossága ($g_i$) & a gép szerepéből és hálózati helyéből adódó fokozat & 0; 0,25; \ldots; 1 (ismeretlen: 0,5) & gépnyilvántartás & mérhető \\ \hline
        Alkalmaz\-hatóság ($a_i$) & működhet-e a támadás a gépen & 0,25; 0,5; 0,75; 1 & szoftverkészlet, szabály hivatkozásai & termék\-szinten \\ \hline
        Megfigyeltség ($m_i$) & mennyire vakfoltos a gép & 0; 0,5; 1 & érzékelők állapota & állandó \\ \hline
    \end{tabular}
\end{table}
```

---

## 4.3 A mérőszámok összevonása

```latex
\subsection{A mérőszámok összevonása}\label{sec:osszevonas}

Az $i$-edik riasztás végső pontszáma a négy mérőszám súlyozott összege:
\begin{equation}
    S_i = w_r\, r_i + w_g\, g_i + w_a\, a_i + w_m\, m_i, \qquad w_r + w_g + w_a + w_m = 1 .
    \label{eq:pontszam}
\end{equation}
A súlyozott összeg mellett két érv szól.
Egyrészt átlátható: az elemző minden riasztásnál látja, melyik összetevő mennyivel járult hozzá a
pontszámhoz.
Másrészt egyik összetevő sem tudja egyedül lenullázni a pontszámot, ami a szűrés elkerülésének
feltétele.
Szorzatos összevonásnál -- amilyet a gyártói megvalósítások kockázati módosítói alkalmaznak -- egy
alacsony környezeti érték a riasztás teljes pontszámát elnyomhatná.

A súlyokat páros összehasonlítással (\ac{AHP}) határozom meg~\cite{saaty1990}.
A módszerben a szakértő minden szempontpárról megmondja, melyik fontosabb és mennyivel, egy 1-től
9-ig terjedő skálán, ahol az 1 az egyenlő, a 9 a sokkal nagyobb fontosságot jelenti.
Az ítéletekből egy négyszer négyes mátrix áll elő, amelynek fő sajátvektora adja a súlyokat.
Az ítéletek következetességét a következetességi aránnyal ellenőrzöm:
\begin{equation}
    CI = \frac{\lambda_{\max} - n}{n - 1}, \qquad CR = \frac{CI}{RI},
    \label{eq:cr}
\end{equation}
ahol $\lambda_{\max}$ a mátrix legnagyobb sajátértéke, $n = 4$ a szempontok száma, $RI$ pedig a
véletlenszerűen kitöltött mátrixok átlagos következetlensége, amely négy szempontnál 0,90.
Az ítéleteket akkor fogadom el, ha a következetességi arány 0,1 alatt marad; ellenkező esetben
felülvizsgálom őket~\cite{saaty1990}.
A páros összehasonlítást a riasztások rangsorolásában korábban is alkalmazták~\cite{anuar2012}; a
dolgozatban a módszer újdonsága az, hogy a kockázatalapú pontszámot egyetlen szempontként kezeli,
és ehhez képest méri a környezeti szempontok hozzájárulását.

A lépésenkénti értékelésben (\ref{sec:ertekeles}.~fejezet) nem minden mérőszám vesz részt
egyszerre.
Ilyenkor a kimaradó mérőszámok súlyát elhagyom, a megmaradókat pedig úgy arányosítom, hogy összegük
ismét 1 legyen; így a lépések közötti különbség kizárólag az új mérőszám hatását mutatja.

Az összetartozó riasztások csoportjának pontszáma a csoport legmagasabb pontszámú riasztásáé.
Ezt azért választottam az átlag helyett, mert egy sok jóindulatú riasztást tartalmazó csoportban az
átlag elfedné az egyetlen, valódi támadásra utaló jelzést.
Egyenlő pontszám esetén az a csoport kerül előre, amelyben több különböző szabály jelzett.
```

Megjegyzés: a páros összehasonlítást **te** végzed el szakértőként (4 szempont = 6 pár). Ha kéred,
készítek hozzá egy kitölthető táblázatot (Excel vagy egy egyszerű oldal), ami azonnal kiszámolja a
súlyokat és a következetességi arányt.

### 4.4. táblázat – a páros összehasonlítás skálája (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A páros összehasonlítás értékskálája (Forrás: saját összeállítás \cite{saaty1990} alapján)}
    \label{tab:ahp-skala}
    \small
    \begin{tabular}{|L{1.8cm}|L{11.6cm}|}
        \hline
        \textbf{Érték} & \textbf{Jelentés (az A szempont a B-hez képest)} \\ \hline
        1 & egyformán fontos \\ \hline
        3 & valamivel fontosabb \\ \hline
        5 & lényegesen fontosabb \\ \hline
        7 & sokkal fontosabb \\ \hline
        9 & rendkívül fontosabb \\ \hline
        2, 4, 6, 8 & köztes értékek; a fordított viszonyt a reciprok fejezi ki (például $1/3$) \\ \hline
    \end{tabular}
\end{table}
```

---

## A mérés terve – áthelyezve

A korábban itt előre megírt mérési terv (lépések, mérőszámok, plafonhatás, torzítás elleni védekezés)
átkerült a 6. fejezet csomagjába: `docs/irasi-csomagok/06_teszteles_es_ertekeles.md`. A 4. fejezet a
`\ref{sec:ertekeles}` hivatkozással utal rá.

---

## 4.4 Összefoglalás (a 4. fejezet vége)

```latex
\subsection{Összefoglalás}

A választott megoldás a nyilvánosan mért legerősebb, tanítás nélküli rangsorolási módszert, a
kockázatalapú pontozást egészíti ki a gép fontosságával, a támadás alkalmazhatóságával és a gép
megfigyeltségével.
A környezeti mérőszámok csak a pontszámot módosítják, riasztást nem távolítanak el, a hiányzó
adatot pedig semleges érték helyettesíti.
Az összevonás súlyozott összeggel történik, amelynek súlyait páros összehasonlítással, a mérés előtt
határozom meg.
A hatást lépésenként, a nyilvános adathalmaz nyolc forgatókönyvén és a saját tesztkörnyezetben mérem;
a mérés részletes tervét \az{\ref{sec:ertekeles}}. fejezet tartalmazza.
A következő fejezet azt mutatja be, hogyan valósítják meg ezt a mérőszámrendszert az egymással
együttműködő agentek.
```

---

## Átvételkor figyelj

- A képletekben a tizedesvessző `{,}` – így nem tesz utána szóközt a LaTeX (`0{,}5`).
- A `\ref{...}~alfejezet` forma a sablon magyar névelő-kezelésével működik; a mondat elején `\Az{\ref{...}}`.
- A 4.2. táblázat fokozatai és a 4.3 súlyai **a te szakértői döntéseid** – ezeket a mérés előtt rögzítsd.
- Nyitott döntések (neked): az alkalmazhatóság négy lépcsője; a megfigyeltség a pontszámba kerüljön-e.

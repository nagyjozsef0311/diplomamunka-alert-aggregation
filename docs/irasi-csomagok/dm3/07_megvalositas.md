# Írási csomag (DM III.) – 7. fejezet: Megvalósítás

2026-11-18 · **Élő csomag**: a megvalósítással együtt bővül. D20 szerint: a **kódblokkok** tartalma
átvehető (forrásoktól független, saját megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Útmutató:** 7. pont – megvalósítás. **Feladatlap:** F4.
- **Terjedelem:** kb. 8–10 oldal a végleges változatban.
- **Fájl:** `chapters/7_Megvalositas.tex`; a `main.tex`-ben a 6. fejezet után:

```latex
\clearpage
\section{MEGVALÓSÍTÁS}\label{sec:megvalositas}
\input{chapters/7_Megvalositas}
```

**Állapot:** 7.1–7.7 a már elkészült részekről szól (2026-11-18). Hiányzik: a vezérlőréteg (LangGraph),
a magyarázó agent (Ollama), a laborkörnyezet – ezek a megvalósításuk után kerülnek ide.

## Források

`uetz2026rba`, `saaty1990`, `landauer2023aitlds`, `landauer2024aitads`, `arp2022` – mind ellenőrzött,
a `references.bib`-ben megvannak. Új forrás nem kell.

---

## 7.0 Nyitó bekezdés

```latex
Ez a fejezet az 5. fejezetben tervezett rendszer megvalósítását mutatja be.
A rendszer egy Python-csomag, amelyben minden agent külön modul, pontosan meghatározott bemenettel és
kimenettel.
A fejezet először a csomag felépítését és a mérések szervezését ismerteti, majd sorra veszi az
egyes agenteket, végül azt mutatja be, hogyan valósult meg a gyakorlatban a mérési beállítások
előzetes rögzítése.
```

---

## 7.1 A csomag felépítése és a mérések szervezése

```latex
\subsection{A csomag felépítése és a mérések szervezése}\label{sec:csomag}

A megvalósítás az 5.5. alfejezetben leírt három réteg közül elsőként a magot tartalmazza: minden
agent egy keretrendszer nélküli Python-modul, amely táblázatos adatszerkezetet kap és ad vissza.
A modulok neve az általuk megvalósított agentet követi (\ref{tab:modulok}.~táblázat), így a kód és a
dolgozat fejezetei kölcsönösen visszakereshetők.

A méréseket külön futtatható szkriptek végzik.
Minden szkript egyetlen mérést vagy előkészítő lépést hajt végre, a nevében szerepel a futtatás
sorszáma, az adathalmaz, az ablációs lépés és a feladat, az eredményét pedig azonos nevű fájlba írja.
Az eredményfájl rögzíti a program verzióját is, így minden szám visszavezethető arra a
programállapotra, amely előállította.
A forráskód, a beállítások és az eredmények egy verziókezelt tárolóban vannak; a letöltött adatok
nem részei a tárolónak, azokat ellenőrzőösszeggel ellenőrzött letöltő szkriptek állítják elő.
```

### 7.1. táblázat – modulok és agentek (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A megvalósítás moduljai és az általuk megvalósított agentek (Forrás: saját összeállítás)}
    \label{tab:modulok}
    \small
    \begin{tabular}{|L{4.0cm}|L{4.4cm}|L{5.0cm}|}
        \hline
        \textbf{Modul} & \textbf{Agent / szerep} & \textbf{Feladat} \\ \hline
        \texttt{egysegesito} & 1. Egységesítő & közös riasztásforma; a címke külön tárolva \\ \hline
        \texttt{csoportosito} & 2. Csoportosító & csoportok gép és időköz szerint; csoportpontszám \\ \hline
        \texttt{gepnyilvantartas} & gépnyilvántartás & öt tábla relációs adatbázisban \\ \hline
        \texttt{kornyezet} & 3. Környezeti & a gép fontossága és megfigyeltsége; ellenpróba \\ \hline
        \texttt{kockazati\_\allowbreak pontszam} & 5. Rangsoroló (alap) & a kockázati pontszám öt részpontszáma \\ \hline
        \texttt{paros\_\allowbreak osszehasonlitas} & 5. Rangsoroló (súlyok) & súlyok és következetességi arány \\ \hline
        \texttt{ertekeles} & értékelés & rangsor-, terhelés- és csoportmérőszámok \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a 4. (sérülékenységi), 6. (magyarázó) és 7. (vezérlő) agent sora akkor kerül be, amikor
elkészül. A `\texttt{}` a kódnevek egyenletes szélességű betűje; az alávonás LaTeX-ben `\_`.

---

## 7.2 Az egységesítő agent

```latex
\subsection{Az egységesítő agent}

Az egységesítő agent a Suricata- és a Wazuh-riasztásokat az 5.2. táblázatban leírt közös formára
hozza, és időrendbe rendezi.
A súlyosságot a két eszköz eltérő skálájáról 0 és 1 közé alakítja, a kockázatalapú pontozás
eredeti megvalósításával egyező módon, hogy az összehasonlítási alap pontosan visszamérhető legyen.
A szabályok szövegéből és metaadataiból kigyűjti a sérülékenység-azonosítókat is; az AIT-ADS
riasztásaiban egyetlen ilyen hivatkozás sem fordul elő, ami megerősíti a 6.1. alfejezetben leírt
korlátot.

A támadás-címkét az agent nem a riasztások táblájában, hanem külön adatsorként adja vissza.
Így a rangsorolást végző részek technikailag sem férhetnek hozzá, a címke csak az értékelés
lépésében kerül elő; ezt automatikus teszt is ellenőrzi.
```

---

## 7.3 A kockázati pontszám és visszamérése

```latex
\subsection{A kockázati pontszám és visszamérése}\label{sec:visszameres}

A kockázati pontszám öt részpontszámát nem írtam újra, hanem a szerzők nyilvános eszközének
moduljait hívom meg, egy rögzített programváltozatból~\cite{uetz2026rba}.
Az eszköz forráskódja nem része a dolgozat tárolójának, mert nincs megadott felhasználási
engedélye; a letöltő szkript a rögzített változatot külön mappába tölti le, és a modulok onnan
töltődnek be.
Ezzel elkerülhető, hogy egy saját újraírás apró eltérései torzítsák az összehasonlítást.

A megvalósítás helyességét a közölt eredmények visszamérésével ellenőriztem az AIT-ADS
russellmitchell forgatókönyvén (\ref{tab:visszameres}.~táblázat).
Az öt részpontszám és a teljes pontszám rangsor-pontossága legfeljebb 0,01-gyel tér el a közölt
értékektől, és a hálózati riasztások listájának első tíz százalékába a közölttel egyezően 43, a
súlyosság szerinti sorrendben 28,6 valódi riasztás került.
A gépi riasztásoknál a teljes pontszám 0,971-es értéke 0,009-cel marad el a közölt 0,98-tól, amit
a súlyok egész százalékra kerekített közlése magyarázhat.
Ezzel a 6.4. alfejezetben előírt első kiemelt teszt teljesült: az összehasonlítási alap hiteles.
```

### 7.2. táblázat – visszamérés (Claude készítette, átvehető; a számok: `results/01_…`)

```latex
\begin{table}[H]
    \centering
    \caption{A kockázatalapú pontozás visszamérése, rangsor-pontosság (Forrás: saját mérés, a közölt értékek \cite{uetz2026rba})}
    \label{tab:visszameres}
    \small
    \begin{tabular}{|L{4.0cm}|L{2.2cm}|L{2.2cm}|L{2.2cm}|L{2.2cm}|}
        \hline
        \textbf{Részpontszám} & \textbf{Wazuh, saját} & \textbf{Wazuh, közölt} & \textbf{Suricata, saját} & \textbf{Suricata, közölt} \\ \hline
        szabályszint & 0,993 & 0,99 & 0,806 & 0,81 \\ \hline
        halmozódás (1 perc) & 0,999 & 1,00 & 0,656 & 0,66 \\ \hline
        változatosság (1 óra) & 1,000 & 1,00 & 0,956 & 0,96 \\ \hline
        ritkaság (1 nap) & 0,071 & 0,07 & 0,991 & 0,99 \\ \hline
        szabálytalanság (1 nap) & 0,005 & 0,01 & 0,954 & 0,95 \\ \hline
        teljes pontszám & 0,971 & 0,98 & 0,987 & 0,99 \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a „teljes pontszám” sor az egy-kihagyásos súlyokkal mért érték (a cikk is azt közli). A
mérésekben a nyolc adathalmaz átlagos súlyait használjuk (4.2.1); azzal a Wazuh 0,987, a Suricata 0,991.

---

## 7.4 A gépnyilvántartás és a környezeti agent

```latex
\subsection{A gépnyilvántartás és a környezeti agent}

A gépnyilvántartás az 5.2. ábra öt tábláját valósítja meg egy beágyazott relációs adatbázisban.
Az AIT-ADS-hez tartozó nyilvántartást a riasztásokban szereplő gépnevekből és a hálózat közzétett
leírásából állítottam össze~\cite{landauer2023aitlds}: a russellmitchell forgatókönyvben tizenegy
gép szerepel a határvédelmi zónában, az intraneten, a zónahatáron és az internetes zónában.

A gépek fontossági fokozatát a 4.2. táblázat szabályai alapján, a gépek szerepéből határoztam meg,
és a mérés előtt rögzítettem.
Az első változat a gépneveket a hálózat leírásának ismerete nélkül értelmezte; a leírás alapján
kiderült, hogy két gép valójában külső levelezőkiszolgáló, egy pedig a globális névkiszolgáló.
Ezek a szervezeten kívüli gépek, ezért a fokozatukat a mérés előtt, dokumentált módon
1-re javítottam, és a 4.2. táblázat legalacsonyabb fokozatát ezzel az esettel egészítettem ki.

A környezeti agent riasztásonként meghatározza az érintett gépet.
A gépi riasztásoknál ez a riasztásban szereplő gépnév, a hálózatiaknál a cél-IP-címhez tartozó gép,
ha az ismert, különben a forrás-IP-címé.
A hálózati riasztások több mint felében a tűzfal külső címe szerepelt, amelyen a belső gépek
kimenő forgalma megjelenik; ennek a címnek a tűzfalhoz rendelésével mindkét érzékelő riasztásainál
minden érintett gép azonosíthatóvá vált.
Az ellenpróbához az agent a gépek fokozatait rögzített kezdőértékű véletlen permutációval is meg
tudja keverni.
```

Megjegyzés: a „mérés előtt” állításokat a 7.7 commitazonosítói igazolják – hivatkozz rá.

---

## 7.5 A csoportosító agent

```latex
\subsection{A csoportosító agent}

A csoportosító agent gépenként időrendben halad, és új csoportot kezd, ha az előző riasztás óta
eltelt idő meghaladja a beállított időközt.
Az időköz kiválasztásának szabályát a kiértékelés előtt rögzítettem: a jelölt értékek közül
érzékelőnként a legnagyobbat választom, amelynél a csoportok tisztasága még legalább 0,95.
A hangoláshoz a russellmitchell forgatókönyvet használtam, ezért azon a csoportosítás eredménye
mintán belüli; a többi forgatókönyvön a kiválasztott időköz változatlanul érvényes.

A szabály mindkét érzékelőnél a legnagyobb jelöltet, a 60 percet választotta, mert a tisztaság
minden jelöltnél 0,99 fölött maradt.
Ez egyben azt is jelzi, hogy a kétértékű címkékkel számolt tisztaság ezen az adathalmazon kevéssé
különbözteti meg a jelölteket; a támadási lépések szerinti tisztaság a nyolc forgatókönyv eredeti
címkéivel vizsgálható.
```

Megjegyzés: a csoportosítás eredményei (pl. 23 116 riasztás → 29 csoport) a 8. fejezetbe valók, nem ide.

---

## 7.6 A rangsoroló súlyai

```latex
\subsection{A rangsoroló súlyai}

A súlyozott összeg súlyait a 4.3. alfejezetben leírt páros összehasonlítással
határoztam meg~\cite{saaty1990}.
Az első körben a következetességi arány 0,40 lett, mert a kockázati pontszámra, a gép fontosságára és
az alkalmazhatóságra vonatkozó ítéletek körbeértek: mindhárom szempont fontosabbnak bizonyult a
következőnél.
Az egyik ítélet felülvizsgálata után az arány 0,084-re csökkent, ami a 0,1-es küszöb alatt marad.
A végleges súlyok: a kockázati pontszám 0,511, a gép fontossága 0,292, az alkalmazhatóság 0,153, a
megfigyeltség 0,045.
A lépésenkénti értékelésben a kimaradó szempontok súlyát elhagyom, a többit újranormálom; a 4. lépésben
így a kockázati pontszám súlya 0,636, a gép fontosságáé 0,364.
```

---

## 7.7 Az előzetes rögzítés a gyakorlatban

```latex
\subsection{Az előzetes rögzítés a gyakorlatban}\label{sec:rogzites}

A 6.3. alfejezetben vállalt előzetes rögzítést úgy valósítottam meg, hogy minden szakértői döntést
egy külön beállítófájl tartalmaz, amely a vele végzett első mérés előtt, önálló változatként került a
verziókezelt tárolóba (\ref{tab:rogzites}.~táblázat).
A változatkezelő napló minden változathoz időbélyeget és egyedi azonosítót rendel, így utólag is
ellenőrizhető, hogy a beállítás megelőzte a mérést.
A rögzített fájlokat nem írtam felül: a javított gépfontosság új fájlba került, az első változat a
tárolóban maradt.
Ez a gyakorlat a tesztadatból származó információ beszivárgása ellen véd~\cite{arp2022}.
```

### 7.3. táblázat – a rögzítések (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{Az előzetesen rögzített beállítások (Forrás: saját összeállítás)}
    \label{tab:rogzites}
    \small
    \begin{tabular}{|L{5.2cm}|L{2.0cm}|L{2.6cm}|L{3.2cm}|}
        \hline
        \textbf{Beállítás} & \textbf{Azonosító} & \textbf{Időpont (UTC)} & \textbf{Első mérés vele} \\ \hline
        gépfontosság, 1. változat & 5c63392 & 2026-11-18 11:51 & nem volt (javítva) \\ \hline
        gépfontosság, 2. változat & 7c6ceed & 2026-11-18 11:59 & 4. lépés \\ \hline
        páros összehasonlítás (súlyok) & 650abd0 & 2026-11-18 12:19 & 4. lépés \\ \hline
        a csoportosítás időközének szabálya & dc23189 & 2026-11-18 12:34 & 2. lépés \\ \hline
        az alkalmazhatóság megfeleltetése & 42036e1 & 2026-11-18 12:46 & 5. lépés \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a táblázat az 5. lépés rögzítésével (42036e1) teljes a russellmitchellre; a 8 forgatókönyv gépnyilvántartásai új sorokat kapnak.

---

## 7.8 A program tesztelése

```latex
\subsection{A program tesztelése}

A modulokhoz automatikus egységtesztek tartoznak, amelyek kis, kézzel ellenőrizhető bemeneteken
vizsgálják a kimenetet.
A tesztek ellenőrzik többek között a súlyossági skálák átalakítását, a címke elkülönítését, az
érintett gép meghatározását és a semleges értékeket, a páros összehasonlítás súlyait egy
tökéletesen következetes mátrixon, a csoportosítás időközkezelését, valamint a mérőszámok
holtversenykezelését.
A 6.4. alfejezetben előírt első kiemelt tesztet, a kockázati pontszám egyezését a szerzők
eszközével, a \ref{sec:visszameres}. alfejezetben leírt visszamérés teljesíti.
```

Megjegyzés: a tesztek száma most 21 – a végleges számot a leadás előtt írd be, ha meg akarod adni.

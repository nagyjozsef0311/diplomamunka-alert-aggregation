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

**Állapot:** 7.1–7.9 a már elkészült részekről szól (2026-11-18; a 8 forgatókönyves méréssel bővítve). Hiányzik: a vezérlőréteg (LangGraph),
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
        \texttt{serulekenysegi} & 4. Sérülékenységi & a támadás alkalmazhatósága; ellenpróba \\ \hline
        \texttt{kockazati\_\allowbreak pontszam} & 5. Rangsoroló (alap) & a kockázati pontszám öt részpontszáma \\ \hline
        \texttt{paros\_\allowbreak osszehasonlitas} & 5. Rangsoroló (súlyok) & súlyok és következetességi arány \\ \hline
        \texttt{ertekeles} & értékelés & rangsor-, terhelés- és csoportmérőszámok \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a 6. (magyarázó) és 7. (vezérlő) agent sora akkor kerül be, amikor
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

Az agent két bemeneti formátumot ismer.
Az egyik a kockázatalapú pontozás szerzőinek felcímkézett változata, amely csak a russellmitchell
forgatókönyvet tartalmazza, a másik az AIT-ADS eredeti kiadása, amely mind a nyolc forgatókönyvet.
Az eredeti kiadásban a hálózati riasztások kétszer szerepelnek: egyszer a Suricata szerkezett
kimenetéből, egyszer pedig a Wazuh által egy szöveges naplóból újra feldolgozott másolatként.
A másolatokat az agent elhagyja, mert ugyanazt a hálózati eseményt kétszer számolnák.
A gépi riasztásoknál a gépnevet elsősorban a naplósor fejlécéből veszi; ha az hiányzik, a
webkiszolgálói naplók helyéből, végül a riasztást beküldő Wazuh-ügynök címéhez ugyanabban a
fájlban legtöbbször tartozó gépnévből.
Ez a szabály egyik forgatókönyv sajátosságaira sem támaszkodik.
A russellmitchell forgatókönyvön az eredeti kiadásból ugyanaz a 32\,302 riasztás állt elő, mint a
felcímkézett változatból, és a jellemzők egyetlen kivétellel megegyeztek: három webes levelezési
riasztásnál a felcímkézett változat kézzel írt, időpont-alapú szabállyal más gépet ad meg.

Az eredeti kiadás címkéje nem riasztásonkénti: a kiadók a támadási lépések kezdő- és záróidejét
adják meg~\cite{landauer2024aitads}.
Az agent ezért egy riasztást akkor tekint támadásinak, ha az ideje egy támadási időszakba esik.
A russellmitchell forgatókönyvön ez a címke egyetlen, a riasztásonkénti címke szerint támadásinak
számító riasztást sem hagyott ki, de a támadás ideje alatt keletkező jóindulatú riasztásokat is
támadásinak jelölte: a hálózati riasztásoknál 44 valódi mellett 169, a gépieknél 7661 mellett 450
ilyen riasztás volt, nagyrészt az adatkiszivárogtatás egyórás időszakában
(\ref{tab:cimkek}.~táblázat).
```

### 7.x. táblázat – a kétféle címke (Claude készítette, átvehető; a számok: `results/07_…`)

```latex
\begin{table}[H]
    \centering
    \caption{Az időszak-alapú és a riasztásonkénti címke a russellmitchell forgatókönyvön (Forrás: saját mérés \cite{landauer2024aitads,uetz2026rba} adatain)}
    \label{tab:cimkek}
    \small
    \begin{tabular}{|L{2.4cm}|L{2.2cm}|L{2.6cm}|L{2.6cm}|L{2.8cm}|}
        \hline
        \textbf{Érzékelő} & \textbf{Riasztás} & \textbf{Támadás, riasztásonként} & \textbf{Támadás, időszak szerint} & \textbf{Ebből jóindulatú} \\ \hline
        Suricata & 9186 & 44 & 213 & 169 \\ \hline
        Wazuh & 23\,116 & 7661 & 8111 & 450 \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a 6.1 („A riasztásokhoz tartozó címkék két forrásból…”) ezt előre jelzi; itt a számok
kerülnek mellé. A „kézzel írt szabály” a CATS átalakítójának `ait_wazuh.yml` beállítása (nem kell
külön forrás, a `uetz2026rba` eszközéről van szó). A döntések: D27, D28.

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

### 7.3 kiegészítés – a gyors számítás és az egyezés ellenőrzése (átvehető; a számok: `results/09_…`)

```latex
A szerzők eszköze minden riasztásnál végigjárja az időablakba eső összes riasztást, ezért a futásidő
a riasztások számával közel négyzetesen nő.
A russellmitchell forgatókönyv 23 ezer gépi riasztásán ez néhány perc, a santos 38 ezer riasztásán
már 11 perc volt; a legnagyobb forgatókönyvek közel félmillió riasztására becslés szerint napokig
tartott volna.
Ezért az öt részpontszám képleteit változatlan matematikai tartalommal, de más számítási sorrendben is
megvalósítottam: az időablakokba eső riasztásokat rendezett időbélyegeken, bináris kereséssel és
halmozott összegekkel határozom meg, az azonos időpontú riasztásokat pedig egyszer számolom.

A két megvalósítás egyezését riasztásonként ellenőriztem négy forgatókönyv tíz adathalmazán,
amelyeken az eredeti eszköz belátható idő alatt lefut (\ref{tab:gyors}.~táblázat).
Az öt részpontszám egyikében sem volt nagyobb eltérés $6 \cdot 10^{-11}$-nél, ami a lebegőpontos
számábrázolás kerekítési hibájának nagyságrendje; a rangsort ez nem befolyásolja.
A gyors változat ugyanazokon az adatokon 25--280-szor rövidebb idő alatt futott le, és a legnagyobb
forgatókönyvön is néhány perc alatt végzett.
Az egyezést automatikus teszt is ellenőrzi.
A további mérésekben ezért a gyors változatot használom; az összehasonlítási alap ettől nem változik.
```

### 7.x. táblázat – az egyezés (Claude készítette, átvehető)

```latex
\begin{table}[H]
    \centering
    \caption{A kockázati pontszám kétféle számításának egyezése (Forrás: saját mérés)}
    \label{tab:gyors}
    \small
    \begin{tabular}{|L{3.8cm}|L{1.8cm}|L{2.2cm}|L{2.0cm}|L{2.6cm}|}
        \hline
        \textbf{Adathalmaz} & \textbf{Riasztás} & \textbf{Eredeti eszköz (s)} & \textbf{Gyors (s)} & \textbf{Legnagyobb eltérés} \\ \hline
        russellmitchell, Wazuh & 23\,116 & 286 & 4,9 & $4 \cdot 10^{-14}$ \\ \hline
        russellmitchell, Suricata & 9186 & 83 & 2,2 & $1 \cdot 10^{-11}$ \\ \hline
        santos, Wazuh & 38\,289 & 662 & 12,8 & $2 \cdot 10^{-15}$ \\ \hline
        santos, Suricata & 44\,112 & 858 & 117 & $3 \cdot 10^{-11}$ \\ \hline
        shaw, Wazuh & 35\,139 & 485 & 10,4 & $4 \cdot 10^{-14}$ \\ \hline
        shaw, Suricata & 16\,692 & 145 & 1,2 & $2 \cdot 10^{-11}$ \\ \hline
        wardbeck, Wazuh & 39\,184 & 651 & 13,1 & $1 \cdot 10^{-14}$ \\ \hline
        wardbeck, Suricata & 24\,510 & 362 & 3,1 & $5 \cdot 10^{-11}$ \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a CATS-változat két adathalmaza (a russellmitchell felcímkézett változata) ugyanígy egyezik; a
táblázatba elég az eredeti formátum nyolc sora. A futásidők egy 4 magos felhőgépen mértek, csak az
arányuk érdekes. A 7.3 első bekezdésének „nem írtam újra” mondata így pontosítandó: „az
összehasonlítási alapot a szerzők eszközével számoltam, és a gyors változatot ehhez mértem” (D29).


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
Ha egy gépi riasztásból a gépnév hiányzik, az agent az 5.2. táblázat szerint a riasztást beküldő
Wazuh-ügynök címe alapján keresi ki a gépet a nyilvántartásból.

A további hét forgatókönyv hálózata ugyanolyan felépítésű, de a címek forgatókönyvenként
véletlenszerűek, és a hálózat leírása ezeket nem közli.
A gépek szerepét, zónáját, fokozatát és szolgáltatásait ezért a russellmitchellre rögzített
szabályokból vettem át, a címeket pedig kilenc rögzített szabállyal a riasztások szerkezetéből
vezettem le, a címkék megtekintése nélkül.
A legfontosabb szabályok: minden gép saját hálózati érzékelőt is futtat, amelynek riasztásaiban a
gép címe szinte mindig szerepel; a tűzfal érzékelőjénél ez a cím a külső, címfordított cím; a
gépnév nélküli Wazuh-ügynököt a beküldött naplók fajtája azonosítja.
A szabályok helyességét azzal ellenőriztem, hogy a russellmitchell forgatókönyvön pontosan a
korábban jóváhagyott nyilvántartást adják vissza.
Mind a hét új forgatókönyvben mind a nyolc szervezeti szerep azonosítható volt; a gépek száma a
külső levelezőkiszolgálók számától függően 11 és 13 között van.
```

Megjegyzés: a kilenc szabály (G1–G9) és a forgatókönyvenkénti táblázat: `results/08_ait_mind8_nyilvantartas_javaslat.md`;
ha részletesen akarod, a G1–G9 táblázat mellékletbe tehető. A 6.1 „a hálózat közzétett leírásából
állítom össze” mondata mellé kell egy fél mondat a címekről (a feladatlistában is szerepel).

Megjegyzés: a „mérés előtt” állításokat a 7.7 commitazonosítói igazolják – hivatkozz rá.

---

## 7.4b A sérülékenységi agent

```latex
\subsection{A sérülékenységi agent}

A sérülékenységi agent azt becsüli, működhet-e a riasztásban jelzett támadás az érintett gépen.
Az AIT-ADS riasztásai nem hivatkoznak sérülékenység-azonosítóra, ezért az agent itt szolgáltatás
szintjén dolgozik: minden szabályhoz egy szolgáltatás-kategória tartozik (például web, levelezés,
névfeloldás), minden géphez pedig a rajta futó szolgáltatások köre, a hálózat közzétett leírása
alapján~\cite{landauer2023aitlds}.
Ha a szabály szolgáltatása fut a gépen, az alkalmazhatóság 0,75, ha a gép szolgáltatásai ismertek,
de a szabályé nincs köztük, 0,25; az ismert sérülékenységre hivatkozó szabály 1-et kapna.
Ha a szabály nem köthető szolgáltatáshoz, vagy a gép ismeretlen, az érték a semleges 0,5.
A szabályok és a szolgáltatások megfeleltetését a mérés előtt rögzítettem; a további hét
forgatókönyvben előforduló húsz új szabályt ugyanazon elv szerint soroltam be.
Az ellenpróbához az agent a gépek szolgáltatáskészleteit véletlenszerűen összekeveri a gépek között.
```

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
különbözteti meg a jelölteket.
A 6.3. alfejezetben leírt, támadási lépések szerinti tisztaságot az eredeti kiadás időszakaiból
számolom: minden riasztás annak a támadási lépésnek a nevét kapja, amelynek időszakába esik, a
többi a normál forgalomhoz tartozik.
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
        a hét további forgatókönyv nyilvántartása & 398c581 & 2026-11-18 13:28 & 1--5. lépés, 8 forgatókönyv \\ \hline
        a nyolc forgatókönyves mérés terve & 47cfb7a & 2026-11-18 13:43 & 1--5. lépés, 8 forgatókönyv \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: a 8 forgatókönyves mérés 13:45-kor indult (a terv rögzítése után). A mérési terv
(`config/elozetes_rogzites/ait_mind8_meresi_terv.yaml`) a dolgozatban nem előírt részleteket is
rögzít (Holm-korrekció, 20 ismétlés a hiányos nyilvántartásnál, a tanult súlyok rácsa) – ezeket a
6.3-ban egy-egy félmondattal érdemes megemlíteni.

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

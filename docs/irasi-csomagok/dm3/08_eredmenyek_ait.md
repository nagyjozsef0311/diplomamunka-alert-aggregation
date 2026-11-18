# Írási csomag (DM III.) – 8. fejezet: Eredmények az AIT-ADS-en (ablációs vizsgálat)

2026-11-18 · **1. változat, a 8 forgatókönyves mérés után.** D20 szerint a `latex` kódblokkok
átvehetők (forrásoktól független, saját megfogalmazás); a „Megjegyzés” sorok neked szólnak.

- **Útmutató:** 9. pont – eredmények és összevetés. **Feladatlap:** F6. **Terjedelem:** kb. 8–10 oldal.
- **Fájl:** `chapters/8_Eredmenyek_AIT.tex`.
- **Számok forrása:** `results/10_ait_mind8_lepes1_5_meres.{md,csv}` (forgatókönyvenként),
  `results/11_ait_mind8_statisztika.md` (átlagok, Wilcoxon, ellenpróba, ±20%, hiányos nyilvántartás,
  tanult súlyok, címke-érzékenység), `results/07_…` (címkék), `results/09_…` (a gyors pontozás egyezése).
- **Források:** `uetz2026rba`, `landauer2024aitads`, `landauer2023aitlds`, `arp2022` – mind megvan.

## Szabály a fejezethez

- Minden eredményt a rögzített beállításokkal közlünk, a romlásokat is (6.3, 8.0). Az okok
  értelmezése a 10. fejezetbe tartozik; itt csak a tények és a közvetlen magyarázat.
- A russellmitchell a csoportosítás hangoló forgatókönyve (2. lépés: mintán belüli).
- A hálózati riasztások abszolút értékei (AP ≈ 0,06–0,1) az időszak-alapú címke zaja miatt
  alacsonyak (8.7); a lépések közti **különbség** az érdemi eredmény.

## Szerkezet

| Alfejezet | Tartalom | Állapot |
| --- | --- | --- |
| 8.0 | nyitó bekezdés | kész |
| 8.1 | az összehasonlítási alap | kész |
| 8.2 | az adatok és a mérés menete (8.1. táblázat) | kész |
| 8.3 | a csoportosítás (2. lépés) | kész |
| 8.4 | a kockázati pontszám a súlyossághoz képest (3. lépés) | kész |
| 8.5 | a gép fontossága (4. lépés) | kész |
| 8.6 | az alkalmazhatóság (5. lépés) | kész |
| 8.7 | robusztusság: ellenpróba, ±20%, hiányos nyilvántartás, címke | kész |
| 8.8 | szakértői és tanult súlyok | kész |
| 8.9 | összegzés | kész |

---

## 8.0 Nyitó bekezdés

```latex
Ez a fejezet a nyilvános AIT-ADS adathalmazon végzett mérések eredményeit mutatja be.
A mérések a 6. fejezetben leírt lépésenkénti bővítést követik: a súlyosság szerinti sorrendből
kiindulva előbb a csoportosítás, majd a kockázatalapú pontozás, végül egyenként a környezeti
mérőszámok hatását vizsgálom.
Minden eredmény az előzetesen rögzített beállításokkal készült (\ref{sec:rogzites}.~alfejezet), és
a hálózati, illetve a gépi riasztásokat külön adathalmazként kezeli.
A romlást mutató eredményeket is változatlan beállításokkal közlöm; az okaikat a 10. fejezet
elemzi.
```

## 8.1 Az összehasonlítási alap

```latex
\subsection{Az összehasonlítási alap}

A kockázatalapú pontozás visszamérése (\ref{sec:visszameres}.~alfejezet) a közölt eredményeket
legfeljebb 0,01-es eltéréssel adta vissza, így a 3. lépés hiteles összehasonlítási alap.
A további lépések javulását vagy romlását ehhez az alaphoz mérem.
```

## 8.2 Az adatok és a mérés menete

```latex
\subsection{Az adatok és a mérés menete}

A mérés az AIT-ADS mind a nyolc forgatókönyvét felhasználja (\ref{tab:ait-adatok}.~táblázat).
A forgatókönyvek mérete nagyon eltérő: a gépi riasztások száma 23 ezer és közel félmillió között
változik.
A négy legnagyobb forgatókönyvben a gépi riasztások 87--94\%-a a támadási időszakba esik, mert a
támadó webes könyvtárpróbálgatása a belső webkiszolgálón több százezer naplóbejegyzést és riasztást
okozott.
Ezekben a forgatókönyvekben a támadási riasztások vannak többségben, ezért a gépi riasztások
rangsorolásának mérőszámai már a legegyszerűbb sorrendnél is magasak, és alig hagynak teret a
javulásnak.
A hálózati riasztások 1--3\%-a esik a támadási időszakba.

A címke a 7.2. alfejezetben leírt módon a támadási időszakokból származik.
A nyolc forgatókönyv eredményeit érzékelőnként és lépésenként átlagolom, a lépések közti
különbséget pedig a 6.3. alfejezetben rögzített, páros, egyoldali Wilcoxon-próbával vizsgálom.
A négy riasztásszintű összevetés p-értékét érzékelőnként és mérőszámonként Holm-módszerrel
korrigálom; nyolc forgatókönyvnél a legkisebb elérhető p-érték 0,0039, korrekció után 0,016.
```

### 8.1. táblázat – az adatok (Claude készítette, átvehető; `results/10_…`)

```latex
\begin{table}[H]
    \centering
    \caption{Az AIT-ADS forgatókönyvei: riasztások és a támadási időszakba eső riasztások (Forrás: saját mérés \cite{landauer2024aitads} adatain)}
    \label{tab:ait-adatok}
    \small
    \begin{tabular}{|L{2.8cm}|R{2.0cm}|R{2.2cm}|R{2.0cm}|R{2.2cm}|}
        \hline
        \textbf{Forgatókönyv} & \textbf{Wazuh} & \textbf{ebből támadás} & \textbf{Suricata} & \textbf{ebből támadás} \\ \hline
        fox & 440\,355 & 93,5\% & 11\,084 & 3,1\% \\ \hline
        harrison & 448\,959 & 93,0\% & 67\,384 & 3,3\% \\ \hline
        russellmitchell & 23\,116 & 35,1\% & 9\,186 & 2,3\% \\ \hline
        santos & 38\,289 & 22,8\% & 44\,112 & 0,9\% \\ \hline
        shaw & 35\,139 & 15,8\% & 16\,692 & 1,2\% \\ \hline
        wardbeck & 39\,184 & 14,4\% & 24\,510 & 0,8\% \\ \hline
        wheeler & 466\,636 & 89,9\% & 68\,629 & 1,0\% \\ \hline
        wilson & 495\,227 & 86,6\% & 65\,038 & 2,6\% \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: az `R{}` oszloptípus (jobbra igazított) a sablon `main.tex`-jében az `L{}` mellett
van-e – ha nincs, cseréld `L{}`-re. A „ebből támadás” az időszak-alapú címke szerint értendő.

## 8.3 A csoportosítás

```latex
\subsection{A csoportosítás}

A csoportosító agent a rögzített 60 perces időközzel mind a nyolc forgatókönyvön a riasztások
számát két-három nagyságrenddel csökkentette: a gépi riasztásokból forgatókönyvenként 29--79, a
hálózatiakból 60--106 csoport lett, ami 99,9, illetve 99,6\%-os átlagos tételszám-csökkenés.
A csoportok a támadási lépések szerint is tiszták maradtak: a csoportokban a leggyakoribb lépéshez
tartozó riasztások aránya a gépi riasztásoknál átlagosan 0,95, a hálózatiaknál 0,98 volt.
A legalacsonyabb értéket (0,84) a hangoló russellmitchell forgatókönyv gépi riasztásai adták, mert
ott egy-egy gépen az egymást követő támadási lépések 60 percen belül követték egymást.

A csoportlista átnézése mindkét érzékelőnél kevesebb tételt jelent, mint a riasztáslistáé: ha a
csoportokat a legsúlyosabb tagjuk szerint rendezzük, a valódi riasztások 98\%-ának megtalálásához
a gépi riasztásoknál átlagosan a csoportok 6\%-át, a hálózatiaknál 53\%-át kell átnézni, míg a
súlyosság szerint rendezett riasztáslistának mindkét érzékelőnél szinte egészét.
A különbség minden forgatókönyvön a csoportosítás javára szólt (gépi riasztások: 8 forgatókönyvből
8, $p = 0{,}004$; hálózati riasztások: 7 különböző értékű párból 7, $p = 0{,}008$).
A két érték nem ugyanazt méri -- egy csoport átnézése több munka egy riasztásénál --, ezért az
eredmény a tételszám csökkenéseként értelmezendő.
```

Megjegyzés: a 2. lépés eredménye a russellmitchellen mintán belüli (a 6.3/7.5 szerint) – ha
akarod, lábjegyzetben jelöld.

## 8.4 A kockázati pontszám a súlyossághoz képest

```latex
\subsection{A kockázati pontszám a súlyossághoz képest}

A kockázatalapú pontozás (3. lépés) mindkét érzékelőnél minden forgatókönyvön csökkentette a
terhelést, vagyis a lista azon részét, amelyet a valódi riasztások 98\%-áig át kell nézni
(\ref{tab:ait-atlag}.~táblázat).
A hálózati riasztásoknál ez a súlyosság szerinti 100\%-ról átlagosan 84\%-ra, a gépieknél 95\%-ról
84\%-ra csökkent (mindkét esetben 8 forgatókönyvből 8, korrigált $p = 0{,}016$).
A rangsor elejének tisztaságát mérő átlagos pontosság viszont a gépi riasztásoknál mind a nyolc
forgatókönyvön kissé romlott (medián különbség $-0{,}002$, átlag $-0{,}04$), a hálózatiaknál
pedig nem változott szignifikánsan.
A gépi riasztásoknál tehát a súlyosság már önmagában is jó sorrendet ad a lista elején, a
kockázati pontszám előnye a lista egészén, a terhelésben jelentkezik.
Ez összhangban van Uetz és szerzőtársai eredményével, akiknél a gépi riasztások szabályszintje
egyedül is magas rangsor-pontosságot ért el~\cite{uetz2026rba}.
```

### 8.2. táblázat – átlagok (Claude készítette, átvehető; `results/11_…`, 1. pont)

```latex
\begin{table}[H]
    \centering
    \caption{A lépések átlagos eredménye a nyolc forgatókönyvön, riasztásszinten (átlag $\pm$ szórás; Forrás: saját mérés)}
    \label{tab:ait-atlag}
    \small
    \begin{tabular}{|L{3.6cm}|L{2.3cm}|L{2.3cm}|L{2.3cm}|L{2.3cm}|}
        \hline
        & \multicolumn{2}{c|}{\textbf{Suricata}} & \multicolumn{2}{c|}{\textbf{Wazuh}} \\ \hline
        \textbf{Lépés} & \textbf{AP} & \textbf{terhelés} & \textbf{AP} & \textbf{terhelés} \\ \hline
        1. súlyosság & 0,059 $\pm$ 0,043 & 1,000 $\pm$ 0,000 & 0,949 $\pm$ 0,060 & 0,953 $\pm$ 0,055 \\ \hline
        3. kockázati pontszám & 0,072 $\pm$ 0,058 & 0,841 $\pm$ 0,119 & 0,907 $\pm$ 0,126 & 0,844 $\pm$ 0,063 \\ \hline
        4. + gép fontossága & 0,099 $\pm$ 0,067 & 0,811 $\pm$ 0,177 & 0,706 $\pm$ 0,309 & 0,823 $\pm$ 0,111 \\ \hline
        5. + alkalmazhatóság & 0,106 $\pm$ 0,067 & 0,814 $\pm$ 0,174 & 0,707 $\pm$ 0,308 & 0,821 $\pm$ 0,115 \\ \hline
    \end{tabular}
\end{table}
```

Megjegyzés: „AP” = átlagos pontosság (az acronyms.tex-ben vedd fel, ha még nincs), „terhelés” = a
98%-hoz átnézendő listarész. A rangsor-pontosság (AUROC) és az első 10% oszlopa a
`results/11_…` 1. pontjában van – ha kell, külön táblázatba.

## 8.5 A gép fontossága

```latex
\subsection{A gép fontossága}

A gép fontosságának hozzáadása (4. lépés) a két érzékelőnél ellentétes hatású volt
(\ref{tab:ait-wilcoxon}.~táblázat).
A hálózati riasztásoknál az átlagos pontosság nyolc forgatókönyvből hétben javult (medián
különbség $+0{,}030$, rang-biszeriális korreláció 0,94, korrigált $p = 0{,}031$), a terhelés
viszont nem változott szignifikánsan (négy javulás, négy romlás).
Az ellenpróba megerősíti, hogy a javulás a gépnyilvántartás tartalmának köszönhető: a
fontossági fokozatok száz véletlen összekeverése közül hét forgatókönyvben legfeljebb 8\% érte el
a valódi nyilvántartással mért átlagos pontosságot; a kivétel a shaw forgatókönyv, ahol a hálózati
riasztások közül alig néhány esik a támadási időszakba.

A gépi riasztásoknál a gép fontossága mind a nyolc forgatókönyvön rontott: az átlagos pontosság
mediánja 0,17-tel, a rangsor-pontosságé 0,08-dal csökkent.
Az ellenpróbánál a keverések 36--64\%-a legalább ilyen eredményt adott, vagyis a gépi
riasztásoknál a fontossági fokozat nem hordoz a támadásra utaló információt.
A romlás közvetlen oka, hogy a gépi támadási riasztások zöme a belső webkiszolgálón keletkezik,
amelynek fokozata alacsonyabb az internet felől elérhető levelezőkiszolgálóénál, ahol viszont a
jóindulatú riasztások nagy része keletkezik.
```

### 8.3. táblázat – Wilcoxon-próba, a fő összevetések (Claude készítette, átvehető; `results/11_…`, 2. pont)

```latex
\begin{table}[H]
    \centering
    \caption{Páros, egyoldali Wilcoxon-próba a nyolc forgatókönyvön; a különbség a jobb irányba előjelezve (Forrás: saját mérés)}
    \label{tab:ait-wilcoxon}
    \small
    \begin{tabular}{|L{1.9cm}|L{3.0cm}|L{1.7cm}|L{1.5cm}|L{1.7cm}|L{1.4cm}|L{1.4cm}|}
        \hline
        \textbf{Érzékelő} & \textbf{Összevetés, mérőszám} & \textbf{javult / romlott} & \textbf{medián} & \textbf{rang-biszer.} & \textbf{$p$} & \textbf{$p$ (Holm)} \\ \hline
        Suricata & 3 > 1, terhelés & 8 / 0 & 0,113 & 1,00 & 0,004 & 0,016 \\ \hline
        Suricata & 4 > 3, AP & 7 / 1 & 0,030 & 0,94 & 0,008 & 0,031 \\ \hline
        Suricata & 4 > 3, terhelés & 4 / 4 & 0,006 & 0,33 & 0,231 & 0,691 \\ \hline
        Suricata & 5 > 4, AP & 4 / 4 & 0,003 & 0,44 & 0,156 & 0,313 \\ \hline
        Suricata & 5 > 3, AP & 7 / 1 & 0,034 & 0,94 & 0,008 & 0,031 \\ \hline
        Wazuh & 3 > 1, terhelés & 8 / 0 & 0,075 & 1,00 & 0,004 & 0,016 \\ \hline
        Wazuh & 3 > 1, AP & 0 / 8 & $-0{,}002$ & $-1{,}00$ & 1,000 & 1,000 \\ \hline
        Wazuh & 4 > 3, AP & 0 / 8 & $-0{,}166$ & $-1{,}00$ & 1,000 & 1,000 \\ \hline
        Wazuh & 5 > 4, AP & 8 / 0 & 0,001 & 1,00 & 0,004 & 0,016 \\ \hline
    \end{tabular}
\end{table}
```

## 8.6 Az alkalmazhatóság

```latex
\subsection{Az alkalmazhatóság}

Az alkalmazhatóság (5. lépés) hatása mindkét érzékelőnél kicsi volt.
A hálózati riasztásoknál a 4. lépéshez képest az átlagos pontosság nem változott szignifikánsan,
a terhelés pedig hét forgatókönyvben kissé nőtt (medián $0{,}001$); a 3. lépéshez képest a
javulás (hét forgatókönyvből nyolcban, korrigált $p = 0{,}031$) lényegében a gép fontosságából
ered.
A gépi riasztásoknál mind a nyolc forgatókönyvön javult az átlagos pontosság és a terhelés, de a
javulás mértéke elhanyagolható (medián $+0{,}001$): a statisztikai szignifikancia itt a hatás
következetességét, nem a nagyságát jelzi.

A gyenge hatás oka, hogy az AIT-ADS riasztásai nem hivatkoznak sérülékenységre, így az
alkalmazhatóság csak szolgáltatásszinten számítható.
A gépi riasztások 96--99,8\%-a ugyanabba a kategóriába esik (a szabály szolgáltatása fut a
gépen), a hálózatiaknál pedig két forgatókönyvben a riasztások többsége semleges értéket kap, mert
a szabály nem köthető szolgáltatáshoz.
A sérülékenység szintű alkalmazhatóságot ezért a laboratóriumi környezetben vizsgálom (9. fejezet).
```

Megjegyzés: a 0,75-ös arány forgatókönyvenként 96,3–99,8% (ellenőrizve 2026-11-18, a 10-es mérés
bemenetéből; az eredményfájl ezt nem írja ki). A két forgatókönyv: harrison (71% semleges) és santos (59%).
A gépi támadási riasztások 89–100%-a a belső webkiszolgálón (g = 0,75), a jóindulatúak 40–59%-a
a DMZ-levelezőn (g = 1) keletkezik – ez a 8.5 „közvetlen ok” mondatának alapja.

## 8.7 Robusztusság

```latex
\subsection{A beállítások és a címkék hatása}

A szakértői súlyok $\pm 20\%$-os megváltoztatása a hálózati riasztásoknál alig mozdította el az
eredményt: az átlagos pontosság forgatókönyvenként legfeljebb 0,006-tal változott, a terhelés
gyakorlatilag nem.
A gépi riasztásoknál a gép fontosságának kisebb súlya javított, a nagyobb rontott, ami a
8.5. alfejezet eredményével összhangban van.

A hiányos nyilvántartás hatását úgy vizsgáltam, hogy a gépek 20, illetve 50\%-át húsz
ismétlésben véletlenszerűen elhagytam.
A hálózati riasztásoknál a rangsor fokozatosan romlott: 50\%-os hiánynál az átlagos pontosság
átlagosan 0,014-gyel csökkent, de átlagosan a 6.3. alfejezetben várt módon a kockázati pontszám
fölött maradt; egyes forgatókönyvekben legfeljebb 0,005-tel alá is került.
A gépi riasztásoknál a gépek elhagyása javított, mert a semleges érték kevésbé torzít, mint a
támadással nem összefüggő fokozat.

A címkézés hatását a russellmitchell forgatókönyvön vizsgáltam, ahol riasztásonkénti címke is
van.
A hálózati riasztások átlagos pontossága az időszak-alapú címkével jóval alacsonyabb (például a
kockázati pontszámnál 0,19 a riasztásonkénti címkével mért 0,81 helyett), mert a támadás
ideje alatt keletkező jóindulatú riasztások támadásinak számítanak.
A lépések közti változás iránya azonban mindkét címkével azonos volt: a gép fontossága mindkettővel
javított a hálózati és rontott a gépi riasztásoknál.
Az időszak-alapú címkével mért abszolút értékek ezért alulbecslik a valódi pontosságot, a lépések
összevetésére azonban alkalmasak.
```

Megjegyzés: a 4 > 3 hálózati AP a CATS-címkével 0,808 → 0,863, időszakkal 0,194 → 0,225; a gépi
0,921 → 0,586, ill. 0,900 → 0,592 (`results/11_…`, 6. pont).

## 8.8 Szakértői és tanult súlyok

```latex
\subsection{Szakértői és tanult súlyok}

A páros összehasonlításból kapott súlyokat adatból tanult súlyokkal vetettem össze.
A kockázati pontszám, a gép fontossága és az alkalmazhatóság súlyát 0,05-ös lépésközű rácson
választottam meg úgy, hogy hét forgatókönyv átlagos pontossága a lehető legnagyobb legyen, és a
nyolcadikon mértem; ezt mind a nyolc forgatókönyvvel megismételtem.

A hálózati riasztásoknál a tanult súlyok közel estek a szakértőiekhez (a kockázati pontszámé
0,55--0,70, a gép fontosságáé 0,20--0,30, az alkalmazhatóságé 0,10--0,20, szemben a szakértői
0,535, 0,306 és 0,160 értékkel), és a kihagyott forgatókönyveken mért eredmény sem tért el
szignifikánsan.
A gépi riasztásoknál a tanulás a gép fontosságának szinte nulla súlyt adott (0--0,05), és a
kihagyott forgatókönyvön mind a nyolc esetben jobb átlagos pontosságot ért el a szakértői
súlyoknál (átlagosan 0,90 a 0,71 helyett, kétoldali $p = 0{,}008$).
A szakértői súlyok tehát a hálózati riasztásokra az adatokkal összhangban vannak, a gépi
riasztásokra viszont túlbecsülik a gép fontosságának szerepét.
```

## 8.9 Összegzés

```latex
\subsection{Összegzés}

Az AIT-ADS nyolc forgatókönyvén a mérések négy fő eredményt adtak.
A csoportosítás a tételszámot két-három nagyságrenddel csökkentette, a csoportok a támadási
lépések szerint tiszták maradtak.
A kockázatalapú pontozás mindkét érzékelőnél minden forgatókönyvön csökkentette a terhelést a
súlyosság szerinti sorrendhez képest.
A gép fontossága a hálózati riasztásoknál következetesen javította a rangsor elejét, és ez az
ellenpróba szerint a nyilvántartás tartalmának köszönhető; a gépi riasztásoknál viszont minden
forgatókönyvön rontott.
Az alkalmazhatóság szolgáltatásszinten gyakorlatilag nem változtatott a rangsoron.
A környezeti információ hozzáadott értéke tehát érzékelőfüggő, és a gépi riasztásoknál a
szakértői súlyozás felülvizsgálatra szorul; ennek okait a 10. fejezet elemzi.
```

Megjegyzés: a 10. fejezetbe (elemzés) javasolt témák: (1) miért ront a gép fontossága a Wazuh-nál
(a támadás a belső webkiszolgálón, a zaj a DMZ-levelezőn – a fokozat a kárt, nem a valószínűséget
méri); (2) a plafonhatás a 4 nagy forgatókönyvben (87–94% támadás); (3) a címkezaj a hálózati
riasztásoknál; (4) a szakértői súly érzékelőnkénti megadásának lehetősége (ez már új beállítás
lenne, csak továbbfejlesztési javaslatként, a rögzített mérést nem érinti).

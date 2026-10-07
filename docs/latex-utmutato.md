# LaTeX-útmutató a dolgozat sablonjához

Kezdőknek, kifejezetten a `thesis/` sablonhoz (kari sablon, Overleaf). A példák csak a szerkezetet
mutatják; a szöveget mindig te írod.

## 1. Hogyan épül fel a projekt

| Fájl / mappa | Mi van benne | Szerkeszted? |
| --- | --- | --- |
| `main.tex` | A fő fájl: előlapok, absztrakt, tartalomjegyzék, **a fejezetek listája**, jegyzékek | Igen, de csak a fejezetlistát |
| `template.tex` | Formázás (margó, betű, sorköz, hivatkozási stílus) | **Nem** |
| `chapters/*.tex` | A fejezetek szövege, fejezetenként külön fájl | **Igen, ide írsz** |
| `references.bib` | Az irodalomjegyzék adatai (BibTeX) | Ritkán; az új forrást én is előkészítem |
| `acronyms.tex` | Rövidítések jegyzéke | Igen |
| `img/` | Ábrák (PDF, PNG) | Feltöltöd ide |
| `includes/` | Előlapok PDF-ben (borító, feladatlap, nyilatkozat, napló) | Csak cserélni |

Overleafben a **Main document a `main.tex`** legyen (Menu → Main document).

## 2. Új fejezet létrehozása

1. Overleafben a bal oldali fájllistában a `chapters` mappán: **New file** → pl. `2_Elmeleti_hatter.tex`
   (ékezet és szóköz nélküli fájlnév).
2. A `main.tex`-ben a Bevezetés után vedd fel (a cím **csupa nagybetűvel**, mert így kerül a tartalomjegyzékbe):

   ```latex
   \clearpage
   \section{A FEJEZET CÍME}\label{sec:elmelet}
   \input{chapters/2_Elmeleti_hatter}
   ```

   - `\clearpage`: új oldalon kezdődik a fejezet (az útmutató ezt kéri).
   - `\label{...}`: egy név, amellyel később hivatkozhatsz a fejezetre.
3. A fejezetfájlon **belül** csak alfejezeteket használj (legfeljebb 3 szint):

   ```latex
   \subsection{Alfejezet címe}\label{sec:alfejezet}
   Szöveg ...

   \subsubsection{Al-alfejezet címe}
   Szöveg ...
   ```

## 3. Szöveg írása – az alapok

| Mit akarsz | Így írd | Megjegyzés |
| --- | --- | --- |
| Új bekezdés | egy **üres sor** | Egy sima sortörés nem kezd új bekezdést |
| Dőlt kiemelés | `\emph{szöveg}` | |
| Félkövér | `\textbf{szöveg}` | Ritkán, folyó szövegben inkább ne |
| Magyar idézőjel „…” | `\enquote{szöveg}` | Magától „…” lesz |
| Lábjegyzet | `szöveg\footnote{megjegyzés}` | |
| Megjegyzés magadnak (nem jelenik meg) | `% ez nem látszik` | Overleafben: Ctrl+/ |
| Felsorolás | lásd lent | A sablon „–” jelet tesz elé |
| Különleges karakter | `\%`, `\&`, `\_`, `\#`, `\$` | Ezek nélkül hibát kapsz |
| Nem törhető szóköz | `~` | Pl. hivatkozás előtt: `szöveg~\cite{...}` |

Felsorolás:

```latex
\begin{itemize}
    \item első elem
    \item második elem
\end{itemize}
```

Számozott felsorolás: `enumerate` az `itemize` helyett.

**Tipp:** írj **egy mondatot egy sorba**. A PDF-ben nem látszik, de sokkal könnyebb javítani, és a
változások is jobban követhetők.

## 4. Hivatkozás forrásra

1. A forrás adatai a `references.bib`-ben vannak, mindegyiknek van egy **kulcsa**, pl.
   `@misc{uetz2026rba, ...}` → a kulcs: `uetz2026rba`.
2. A szövegben: `\cite{uetz2026rba}` → a PDF-ben **[n]** lesz, az irodalomjegyzék pedig magától
   elkészül (betűrendben, ahogy az útmutató kéri).
3. Több forrás egyszerre: `\cite{tariq2025,ndichu2026}` → [n, m].
4. A hivatkozás elé nem törhető szóközt tegyél: `... a riasztások~\cite{alahmadi2022}.`
5. **Csak az kerül az irodalomjegyzékbe, amire hivatkoztál.** Ezért nem baj, hogy a `.bib`-ben több forrás van.
6. A kulcsok listája: Overleafben nyisd meg a `references.bib`-et, vagy kérd tőlem a listát.
   Ha a `\cite{` után elkezded gépelni a kulcsot, az Overleaf felajánlja a lehetőségeket.
7. **Szó szerinti idézet:** `\enquote{…}` és utána `\cite{...}`. Angol forrás saját fordításánál
   jelöld: „(saját fordítás)”.
8. **Új forrás:** szólj, és elkészítem a BibTeX-bejegyzést ellenőrzött DOI-val vagy arXiv-azonosítóval.

## 5. Hivatkozás ábrára, táblázatra, fejezetre

A `\label{...}` névvel, a `\ref{...}` paranccsal. A magyar névelőt (a/az) a `\az{...}` parancs
magától helyesen teszi ki:

```latex
\Az{\ref{fig:soc-folyamat}}. ábra mutatja ...      % mondat elején, nagy kezdőbetűvel
... ahogy \az{\ref{tab:kerdesek}}. táblázatban látható.
... részletesen \az{\ref{sec:elmelet}}. fejezetben.
```

Eredmény: „Az 1.1. ábra mutatja …”, „az 1.2. táblázatban”, „az 1. fejezetben”.

## 6. Ábra beillesztése

1. Töltsd fel a képet az `img/` mappába (Overleaf: Upload). PDF vagy PNG legyen.
2. A szövegben:

   ```latex
   \begin{figure}[H]
       \centering
       \includegraphics[width=0.8\linewidth]{img/soc_folyamat.pdf}
       \caption{Az ábra rövid címe (Forrás: saját ábra)}
       \label{fig:soc-folyamat}
   \end{figure}
   ```

   - `[H]`: pontosan ott jelenjen meg, ahol a kódban van.
   - `width=0.8\linewidth`: a szövegszélesség 80%-a.
   - A felirat (`\caption`) kötelező; ha más forrásból van, a forrást is írd bele (`\cite{...}`).
   - Az ábrajegyzékbe magától bekerül.

## 7. Táblázat

Az egyszerű táblázatot én is elkészítem neked külön fájlba (`tables/`), te csak beilleszted:
`\input{tables/kutatasi_kerdesek}`. Ha magad írod:

```latex
\begin{table}[H]
    \centering
    \caption{A táblázat címe}
    \label{tab:kerdesek}
    \begin{tabular}{|l|p{9cm}|}
        \hline
        \textbf{Oszlop 1} & \textbf{Oszlop 2} \\ \hline
        cella & hosszabb szöveg, amely több sorba is törhet \\ \hline
    \end{tabular}
\end{table}
```

- `&` választja el a cellákat, `\\` zárja a sort, `\hline` vízszintes vonal.
- `l`, `c`, `r`: balra, középre, jobbra igazított oszlop; `p{9cm}`: 9 cm széles, sortörő oszlop.

## 8. Rövidítések

Első előfordulásnál írd ki a szövegben, pl. „behatolásérzékelő rendszer (Intrusion Detection System,
IDS)”. Utána vedd fel az `acronyms.tex`-be:

```latex
\acronym{IDS}{Intrusion Detection System – behatolásérzékelő rendszer}
```

Az első rövidítés felvételekor a `main.tex` végén a „RÖVIDÍTÉSEK” rész elől töröld a `%` jeleket.

## 9. Overleaf – hatékony munka

| Mit | Hogyan |
| --- | --- |
| Fordítás (PDF frissítése) | **Recompile** gomb vagy **Ctrl+Enter** (Macen Cmd+Enter) |
| Ugrás a PDF-ből a forrásba | Dupla kattintás a PDF-ben a szövegre |
| Ugrás a forrásból a PDF-be | A kód és a PDF közötti nyíl gomb |
| Vázlat (fejezetek fája) | Bal oldalt lent: **File outline** |
| Szövegszerkesztő mód | Fent: **Code Editor / Visual Editor** kapcsoló – a Visual Editor Word-szerűbb, kezdéshez kényelmes |
| Hibák | A **Logs and outputs** ikon (piros szám): rákattintva a hibás sorhoz ugrik |
| Korábbi változatok | **History** (fent): visszanézhető, mi változott |
| Helyesírás | Menu → Spell check: **Hungarian** |

**Hibák kezelése:**

- A **figyelmeztetés (sárga)** általában nem baj, a PDF elkészül.
- A **hiba (piros)** esetén a leggyakoribb okok: lemaradt `}` vagy `\end{...}`; `%`, `&`, `_` jel
  `\` nélkül; elírt parancs; nem létező kép vagy hivatkozási kulcs.
- Ha nem találod, másold be ide a hibaüzenetet.

## 10. Hogyan dolgozunk együtt

1. Te írsz Overleafben (a `chapters/` fájlokba).
2. Ha egy darabbal elkészültél: Overleaf → Menu → **Download → Source** (zip), és feltöltöd ide.
3. Behozom a tárolóba, lefordítom, és a beszélgetésben jelzem a formai hibákat, a hiányzó
   hivatkozásokat és a rövidítéseket. **A szövegedet nem írom át** (D16).
4. Ha én változtatok valamit (ábra, táblázat, `references.bib`, `template.tex`), új zipet kapsz;
   ilyenkor a megadott fájlokat töltsd fel Overleafben (Upload → felülírás), vagy importáld új projektként.

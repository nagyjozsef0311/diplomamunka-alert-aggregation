# Diplomamunka II. – követelmények, leadandók, a beszámoló vázlata

Forrás: a kari tárgyleírás (Moodle, a 2025/26. tavaszi félév szövege, a szerző másolta be
2026-10-01-én) és a feladatlap. A dátumok a tavalyi kiírásból vannak; a 2026/27. őszi félév pontos
dátumait a Moodle-ben kell ellenőrizni.

## Határidők

| Tárgy | Mikor | Mi a követelmény |
| --- | --- | --- |
| Diplomamunka I. | kész (2026 tavasz) | Téma, konzulens, feladatlap |
| **Diplomamunka II.** (2026/27. ősz) | **Leadás: a szorgalmi időszak utolsó napja, 23:59 (2026. december, pontos nap: Moodle)** | A 4 fájl egy zipben (lásd lent) |
| | Pótlás: kb. egy héttel később, pótlási díj befizetése után | Ha addig sincs hiánytalan anyag: „letiltva” |
| | **Beszámoló: a vizsgaidőszak 3. hetének péntekje és/vagy szombatja (2027. január)** | 8 perces előadás bizottság előtt, személyesen; a beosztás a beszámoló előtti héten kerül a Moodle-be |
| Diplomamunka III. (2027 tavasz) | **2027. május 15., 16:00** (nem 23:59!) – nem hosszabbítható | A kész dolgozat mellékletekkel a diplomaportálon: https://diploma.uni-obuda.hu/ |
| Elévülés | 2029. május 15. | A feladatlap szerint (ÓE HKR 54. § (10)) |

## A Diplomamunka II. tartalmi követelményei

A tárgyleírás szerint a beszámolónak ezeket kell bemutatnia:

1. az elméleti háttér elmélyítése;
2. a téma tudományos szakirodalmának megismerése és kiértékelése;
3. hasonló megoldások elemzése, összehasonlítása és kiértékelése;
4. a saját megoldás részletes specifikációja és terve;
5. szükség esetén a megvalósítási vagy tesztkörnyezet terve;
6. az eszközök, módszerek és technikák kiválasztása **indoklással** (milyen lehetőségek közül, milyen szempontok alapján);
7. a tesztelés, a tesztelhetőség és a tesztelési mérőszámok terve;
8. terjedelem: **legalább 30–35 oldal**, a szakdolgozat formai követelményei szerint.

Az utolsó félévre csak a megvalósítás, a tesztelés és a kiértékelés maradhat, de ezek tervét már
most be kell mutatni.

## A leadandó fájlok

A neveket ékezet nélkül kell írni. A rossz nevű fájl nem számít beadottnak.

| Fájl | Név | Állapot |
| --- | --- | --- |
| Feladatlap (mindkét oldal, aláírás nélkül) | `<Neptun>_Nagy_<Konzulens>_FELADATLAP` | Megvan (.doc), PDF-be kell menteni |
| Írásos beszámoló (min. 30–35 oldal) | `<Neptun>_Nagy_<Konzulens>_BESZ` | LaTeX, `thesis/` |
| Az előadás diasora | `<Neptun>_Nagy_<Konzulens>_PREZ` | Később |
| Konzultációs napló, a konzulens aláírásával és javasolt érdemjeggyel | `<Neptun>_Nagy_<Konzulens>_KONZ.pdf` | A szerző és a konzulens |
| Az egész egy tömörített fájlban | `<Neptun>_Nagy_<Konzulens>.zip` | A végén |

- `<Neptun>`: a Neptun-kód (a feladatlapon szerepel; személyes adat, ezért nem írjuk be ide).
- `<Konzulens>`: a belső konzulens vezetékneve ékezet nélkül. **Nyitott kérdés:** „Vorosne” vagy
  „BanatiBaumann”? A konzulenssel vagy a Moodle-példákból kell tisztázni.

## A beszámoló (8 perc)

Elvárt tartalom: a probléma, a jelentősége és a célok; az elméleti háttér (csak amennyi a megértéshez
kell); a szakirodalmi megoldások összehasonlítása és értékelése; a saját megoldás terve, megvalósítása
és tesztelhetősége. A bizottság a dolgozat formáját, felépítését, az előadás tartalmát, módját és az
időtartást értékeli. Ajánlás a tárgyleírásból: kevés szöveg, sok folyamatábra, felépítési ábra,
rendszerterv és táblázat.

## A feladatlap kötelező tartalma (a végleges dolgozatra)

Cím: *Agent-alapú, metrika-vezérelt IDS riasztásaggregáció SOC környezetben* (angolul: *Agent-Based
Metric-Driven IDS Alert Aggregation in SOC Environments*). Intézet: Biomatika és Alkalmazott
Mesterséges Intelligencia Intézet. Külső konzulens nincs.

A dolgozatnak tartalmaznia kell:

- F1. a behatolásérzékelő (IDS) és a SOC rendszerek működésének és kihívásainak áttekintését;
- F2. a riasztás-összevonási és rangsorolási megoldások elemzését;
- F3. a kialakított mérőszámrendszer és az agent-alapú modell bemutatását;
- F4. a rendszer felépítésének és megvalósításának ismertetését;
- F5. a tesztelési és értékelési módszertan bemutatását;
- F6. az eredmények elemzését és a továbbfejlesztési lehetőségeket.

A feladat szövege kiemeli: a metrikák és értékelési szempontok meghatározása a dolgozat fő súlypontja,
és a megoldást „különböző biztonsági és infrastruktúrális szempontok alapján” kell értékelni.

## A Diplomamunka II. beszámolójának vázlata

A fejezetek egyszerre fedik le a feladatlapot (F1–F6) és a Diplomamunka II. követelményeit (1–8).
A végleges dolgozat ugyanerre a szerkezetre épül, a 8. fejezet helyére a mérési eredmények kerülnek.

| Fejezet | Feladatlap | DM II. | Alapanyag a tárolóban | Oldal |
| --- | --- | --- | --- | --- |
| 1. Bevezetés: probléma, jelentőség, célok, kutatási kérdések | – | – | `kutatasi-eredmenyek.md` | 3 |
| 2. A behatolásérzékelők és a SOC működése, kihívásai (riasztási fáradtság) | F1 | 1 | jegyzetek 01–02 | 6 |
| 3. Riasztás-összevonási és rangsorolási módszerek: elemzés és összehasonlítás | F2 | 2, 3 | jegyzetek 03–04, `references.bib` | 8 |
| 4. A saját megoldás specifikációja: mérőszámrendszer és agent-modell | F3 | 4 | `metrika-katalogus.md`, D1–D12 | 6 |
| 5. Felépítés és eszközválasztás indoklással (Python-mag, LangGraph, MCP, adatbázis, nyelvi modell) | F4 (terv) | 4, 6 | jegyzet 05 | 4 |
| 6. A tesztkörnyezet terve: AIT-ADS és saját labor | F4 (terv) | 5 | `munkaterv-reszletes.md` | 3 |
| 7. Tesztelési és értékelési módszertan, mérőszámok | F5 | 7 | `metrika-katalogus.md`, mérési szabályok | 4 |
| 8. Első eredmények és ütemterv a Diplomamunka III.-ra | F6 (részben) | – | `results/` | 2 |
| **Összesen** (+ címlap, tartalomjegyzék, irodalomjegyzék nélkül) | | | | **kb. 36** |

## Nyitott teendők

- [ ] A kari szakdolgozat-készítési útmutató (formai előírások) feltöltése vagy elérhetővé tétele.
- [ ] Az Overleaf-sablon forrásának feltöltése (Overleaf: Menu → Download → Source, zip).
- [ ] A konzulens nevének alakja a fájlnevekben.
- [ ] A 2026/27. őszi félév pontos dátumai (a szorgalmi időszak utolsó napja, a beszámoló hete).
- [ ] Konzultációs napló: az alkalmak folyamatos vezetése, a végén aláíratás.

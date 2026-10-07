# A dolgozat szerkezete – mi hova kerül, és mi a követelmény

Forrás: kari útmutató (`thesis/utmutato/`, 2.2–2.3 pont és 3. melléklet), a feladatlap („A
diplomamunkának tartalmaznia kell” F1–F6) és a Diplomamunka II. tárgyleírása (DM II. 1–8,
`docs/diplomamunka-2.md`). A fejezetcímek munkacímek; a végleges címeket a szerző adja meg.

## Terjedelem

| | Követelmény |
| --- | --- |
| Diplomamunka II. beszámoló (2026. dec.) | legalább **30–35 oldal** (a Moodle-kiírás szerint; az útmutató 15–20 oldalt ír) |
| Végleges dolgozat (2027. máj. 15., 16:00) | legalább **60 oldal** és **80 000 karakter** (szóközökkel), legfeljebb **80 oldal** mellékletekkel |

## Előlapok (oldalszám nélkül, kötelező sorrendben)

| Elem | Követelmény | Hol van |
| --- | --- | --- |
| Belső borítólap | kari minta (4. melléklet), a valódi törzskönyvi számmal | `includes/BELSO-BORITOLAP_DM.pdf` |
| Feladatlap | mindkét oldal; DM II.-ben aláírás nélkül, a végleges dolgozatban **aláírva, képként** | `includes/FELADATLAP.pdf` |
| Hallgatói nyilatkozat | végleges dolgozatban aláírva, képként | `includes/HALLGATOI-NYILATKOZAT_DM.pdf` |
| Konzultációs napló | 4 alkalom láttamozva, a konzulens javasolt jegyével | `includes/KONZULTACIOS-NAPLO_...pdf` |
| Absztrakt magyarul és angolul | rövid tartalmi kivonat (cél, módszer, eredmény) | `main.tex` (ABSZTRAKT, ABSTRACT) |
| Tartalomjegyzék | **innen kezdődik az oldalszámozás** | magától készül |

## Fejezetek

| # | Fejezet (munkacím) | Mit kell tartalmaznia | Útmutató | Feladatlap | DM II.-ben | Oldal (DM II. / végleges) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bevezetés | A probléma megfogalmazása és jelentősége, a dolgozat célja, kutatási kérdések, lehatárolás, a dolgozat felépítése | 1. | – (a feladat leírása) | **igen** | 3 / 4–5 |
| 2 | Az IDS és a SOC működése, kihívásai | Elméleti háttér: behatolásérzékelők (hálózati és gépi), SIEM, a SOC felépítése és folyamatai, riasztási fáradtság; **a probléma elemzése** | 2. | **F1** | **igen** (DM II. 1) | 6 / 8–10 |
| 3 | Riasztás-összevonási és rangsorolási megoldások | Szakirodalmi áttekintés: korreláció, csoportosítás, rangsorolás (kockázatalapú pontozás, környezetfüggő módszerek, gépi tanulás, nyelvi modelles agentek); **összehasonlító táblázat és értékelés** | 3. | **F2** | **igen** (DM II. 2–3) | 8 / 12–14 |
| 4 | A megoldás kiválasztása és a mérőszámrendszer | Miért ez a megközelítés (a választás indoklása); a mérőszámok (riasztás, gép, sérülékenység, megfigyeltség) és az összevonás módja (páros összehasonlítás); **részletes specifikáció** | 4–5. | **F3** | **igen** (DM II. 4) | 6 / 8–10 |
| 5 | A rendszer felépítése és tervezése | Az agent-alapú modell (7 agent), a felépítés ábrája, adatfolyam, gépnyilvántartás; **eszközválasztás indoklással** (Python, LangGraph, MCP, SQLite, Ollama) | 6. | **F4** (terv) | **igen** (DM II. 4–6) | 5 / 6–8 |
| 6 | Megvalósítás | A modulok és a vezérlés megvalósítása, a labor felépítése | 7. | **F4** | nem (csak terv szinten az 5. fejezetben) | – / 6–8 |
| 7 | Tesztelési és értékelési módszertan | Adathalmazok (AIT-ADS, labor), **tesztkörnyezet**, mérőszámok (rangsor-pontosság, terhelés-csökkenés), az értékelés lépcsői, statisztikai próba | 8. | **F5** | **igen** (DM II. 5, 7) | 4 / 5–6 |
| 8 | Eredmények és értékelés | Mérési eredmények, összevetés a kockázatalapú pontozással és más rendszerekkel | 9. | **F6** | DM II.-ben: **első eredmények** (ha van) **és ütemterv a III. félévre** | 2 / 8–10 |
| 9 | Elemzés és továbbfejlesztés | Korlátok, alkalmazhatóság, továbbfejlesztési lehetőségek | 10. | **F6** | nem | – / 3–4 |

## Záró részek

| Elem | Követelmény | Hol van |
| --- | --- | --- |
| Összefoglalás (magyar) | tartalmi összefoglaló és következtetések, **1500–2500 karakter** | `chapters/Osszefoglalas.tex` |
| Summary (angol) | ugyanez angolul | `chapters/Summary.tex` |
| Irodalomjegyzék | kötelező; [n] sorszám, az első szerző szerint betűrendben | magától, a `\cite{}`-okból |
| Ábrajegyzék, táblajegyzék | kötelező, ha van ábra, illetve táblázat | magától |
| Rövidítések | összesítve az elején vagy a végén | `acronyms.tex` |
| Mellékletek | ami nem fér a szövegbe (pl. hosszabb táblázatok, konfiguráció) | `chapters/Mellekletek.tex` |

## Általános követelmények (minden fejezetre)

- **Saját munka**; minden átvett gondolatnál hivatkozás, szó szerinti idézet idézőjelben.
- Ábra és táblázat: fejezetenként számozva, címmel, a szövegben hivatkozva, a forrás feltüntetve.
- Fejezetcím: új oldalon, 14 pont, nagybetűs; alfejezet legfeljebb 3 szintig.
- Magyar műszaki szaknyelv, felesleges rövidítés és zsargon nélkül.
- Képletből csak azt számozd, amelyikre hivatkozol.

## Javasolt fájlnevek a `chapters/` mappában

`1_Bevezetes.tex` (megvan), `2_IDS_es_SOC.tex`, `3_Szakirodalom.tex`, `4_Metrikarendszer.tex`,
`5_Rendszerterv.tex`, `6_Megvalositas.tex`, `7_Teszteles.tex`, `8_Eredmenyek.tex`,
`9_Tovabbfejlesztes.tex`. A Diplomamunka II.-höz az 1–5., a 7. és a 8. kell.

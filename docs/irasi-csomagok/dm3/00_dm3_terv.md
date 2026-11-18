# Diplomamunka III. – a végleges dolgozat terve és az írási csomagok

2026-11-18 · Élő dokumentum: a megvalósítással párhuzamosan frissül. A DM II. beszámolóba **nem** kerül
bele semmi ebből (D24); az itteni csomagok a 2027. tavaszi, végleges dolgozathoz készülnek.

## Követelmények (kari útmutató, `thesis/utmutato/`, 11–16. o.; `docs/diplomamunka-2.md`)

| Előírás | Érték |
| --- | --- |
| Terjedelem | legalább **60 oldal** és **80 000 karakter** (szóközökkel); legfeljebb **80 oldal** mellékletekkel |
| Leadás | **2027. május 15., 16:00**, diplomaportál, **egyetlen** feltöltés, 1 kereshető PDF |
| Melléklet-zip | forráskód, tesztadatok és eredmények, a prezentáció (ppt/pptx) |
| Előlapok | a feladatlap és a hallgatói nyilatkozat **aláírva, képként** |
| Plágium | 20% szövegegyezésig a konzulens dönt |
| Összefoglaló | magyarul 1500–2500 karakter, angolul is – a végleges eredményekkel frissíteni |

## A végleges szerkezet és a terjedelmi keret (D24)

| # | Fejezet | Forrás | Oldal (becsült) | Állapot |
| --- | --- | --- | ---: | --- |
| 1–6 | A DM II. fejezetei | `docs/irasi-csomagok/01–06` | kb. 40–45 | kész, a végleges változathoz igazítandó (lent) |
| 7 | Megvalósítás | `dm3/07_megvalositas.md` | 8–10 | **folyamatban** – a megvalósítással együtt bővül |
| 8 | Eredmények az AIT-ADS-en (ablációs vizsgálat) | `dm3/08_eredmenyek_ait.md` | 8–10 | **váz** – a 8 forgatókönyv után véglegesíthető |
| 9 | Laboratóriumi tesztek | `dm3/09_labor.md` | 6–8 | még nincs (a labor után) |
| 10 | Elemzés és továbbfejlesztés | `dm3/10_elemzes.md` | 3–4 | még nincs |
| – | Összefoglalás, Summary, absztrakt | `07_osszefoglalas.md` frissítése | 1–2 | a végén |
| | **Összesen** | | **kb. 66–79** | a 60–80 oldalas keretbe illeszkedik |

## Az 1–6. fejezet igazítása a végleges változathoz

- **Bevezetés, a dolgozat felépítése:** a végleges blokk a `01_bevezetes.md` 5. pontjában (7–10. fejezet).
- **4.2. táblázat:** az 1-es sor kiegészítése: „a szervezeten kívüli gép” (D25).
- **4. és 6. fejezet:** a jövő idejű tervmondatok („mérem”, „rögzítem”) múlt időre váltása, ahol már
  megtörtént; a 6.3 torzítás elleni védekezésénél a rögzítés commitazonosítóinak megadása (lásd 7.7).
- **6.3:** a csoportosító időközének kiválasztási szabálya (D26) és a tisztaság kétértékű volta.
- **5. fejezet:** ha a LangGraph- vagy az MCP-réteg kimarad, az 5.5 igazítása.
- **6.1:** a gépnyilvántartás IP-címei nem a közzétett leírásból, hanem a riasztások szerkezetéből,
  rögzített szabályokkal (G1–G9) származnak – egy félmondat; a címkéknél a számok a 7.2-ben (D28).
- **6.3:** a mérési terv dolgozatban nem előírt részletei (D29): Holm-korrekció, a hiányos
  nyilvántartás 20 ismétlése, a tanult súlyok 0,05-ös rácsa és AP-célfüggvénye.
- **4.2.1 / 7.3:** a kockázati pontszám a nagy forgatókönyveken a CATS képleteinek vektoros
  megvalósításával készült, a CATS kódjával riasztásonként egyezően (D29).

## Mérések és eredményfájlok (a 8. fejezethez)

| Lépés | Szkript | Eredmény | Állapot |
| --- | --- | --- | --- |
| 1., 3. (visszamérés) | `experiments/01_…` | `results/01_…` | kész, russellmitchell |
| 2. (csoportosítás) | `experiments/05_…` | `results/05_…` | kész, russellmitchell (hangoló forgatókönyv) |
| 4. (+ gép fontossága) | `experiments/04_…` | `results/04_…` | kész, russellmitchell |
| 5. (+ alkalmazhatóság) | `experiments/06_…` | `results/06_…` | kész, russellmitchell |
| eredeti formátum, időszak-címke (russellmitchell) | `experiments/07_…` | `results/07_…` | kész (D27, D28) |
| a 7 új forgatókönyv nyilvántartása (G1–G9) | `experiments/08_…` | `results/08_…`, `config/elozetes_rogzites/ait_<f>_*.yaml` | jóváhagyva, rögzítve (398c581) |
| a gyors kockázati pontszám egyezése a CATS-szal | `experiments/09_…` | `results/09_…` | fut / kész (D29) |
| 1–5. mind a 8 forgatókönyvön (+ ellenpróba, ±20%, hiányos nyilvántartás, rács) | `experiments/10_…` | `results/10_…` | terv rögzítve (47cfb7a), mérés |
| Wilcoxon, hatásnagyság, tanult súlyok, címke-érzékenység | `experiments/11_…` | `results/11_…` | a 10-es után |
| 6. (megfigyeltség), magyarázó agent | – | – | labor |

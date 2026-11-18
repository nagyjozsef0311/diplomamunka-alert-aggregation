# experiments/ – a mérések futtatói

Elv: **egy szkript = egy mérés vagy előkészítő lépés**, az eredmény a `results/` mappába kerül, ugyanazzal
a névvel (`.md` és ha van, `.csv`). Az előzetesen rögzített beállítások a `config/elozetes_rogzites/`
mappában vannak (dolgozat 6.3).

## Elnevezés

`<sorszám>_<adathalmaz vagy agent>_<fázis>_<mit csinál>.py`

- **sorszám:** a futtatás sorrendje;
- **adathalmaz / agent:** `ait_<forgatókönyv>` (AIT-ADS), `labor`, vagy az érintett agent (pl. `rangsorolo`);
- **fázis:** az ablációs lépés(ek) a dolgozat 6.2. táblázata szerint (`lepes1_3`, `lepes4`, …),
  vagy hiányzik, ha előkészítés;
- **mit csinál:** néhány szó (`alapvonal_visszamerese`, `gepek_feltarasa`, `ahp_sulyok_szamitasa`).

## A szkriptek

| Szkript | Fázis | Mit csinál | Dolgozat |
| --- | --- | --- | --- |
| `01_ait_russellmitchell_lepes1_3_alapvonal_visszamerese.py` | 1. és 3. lépés | A súlyosság szerinti rangsor és a kockázatalapú pontozás visszamérése a cikk értékeivel | 6.3, 6.4 (első kiemelt teszt) |
| `02_ait_russellmitchell_gepek_feltarasa.py` | a 4. lépés előkészítése | A gépek feltárása és a gépnyilvántartás lefedettsége a fokozatok 2. változatával (D25) – **címkék nélkül** | 5.4, 6.1, 6.3 |
| `03_rangsorolo_ahp_sulyok_szamitasa.py` | a 4–6. lépés előkészítése | A rangsoroló súlyai a szerző páros összehasonlításából, következetességi aránnyal | 4.3, 6.3 |
| `05_ait_russellmitchell_lepes2_csoportositas.py` | 2. lépés (+ a 3–4. csoportszinten) | Az időköz kiválasztása a rögzített szabállyal (D26), csoportok rangsorolása, tisztaság, tételszám-csökkenés | 5.3, 6.2. táblázat, 6.3 |
| `06_ait_russellmitchell_lepes5_alkalmazhatosag.py` | 5. lépés | Kockázati pontszám + gép fontossága + alkalmazhatóság; riasztás- és csoportszinten, ellenpróba (a szolgáltatáskészletek keverése), ±20% | 4.2.3, 4.3, 6.2. táblázat, 6.3 |
| `04_ait_russellmitchell_lepes4_gepfontossag.py` | 4. lépés | Kockázati pontszám + gép fontossága; összevetés az 1. és 3. lépéssel, ellenpróba (100 keverés), ±20%-os érzékenység | 4.3, 6.2. táblázat, 6.3 |

## A csomag moduljai (`src/alertagg/`) – az agentek szerint

| Modul | Agent / szerep | Dolgozat |
| --- | --- | --- |
| `egysegesito.py` | 1. Egységesítő agent – közös riasztásforma, a címke külön | 5.3, 5.2. táblázat |
| `kockazati_pontszam.py` | 5. Rangsoroló – a kockázati pontszám (r), a CATS moduljaival | 4.2.1 |
| `gepnyilvantartas.py` | Gépnyilvántartás (SQLite, öt tábla) | 5.4, 5.2. ábra |
| `kornyezet.py` | 3. Környezeti agent – a gép fontossága (g), megfigyeltsége (m), ellenpróba | 4.2.2, 4.2.4, 6.3 |
| `serulekenysegi.py` | 4. Sérülékenységi agent – a támadás alkalmazhatósága (a), ellenpróba | 4.2.3, 5.3 |
| `csoportosito.py` | 2. Csoportosító agent – gép + időköz, csoportpontszám (maximum, holtverseny-feloldás) | 5.3, 4.3 |
| `paros_osszehasonlitas.py` | 5. Rangsoroló – súlyok páros összehasonlítással, CR | 4.3 |
| `ertekeles.py` | Értékelési mérőszámok | 6.3 |

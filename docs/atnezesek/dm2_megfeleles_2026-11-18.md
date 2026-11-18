# A Diplomamunka II. beszámoló megfelelése a követelményeknek – átnézés, 2026-11-18

Átnézett változat: a szerző v0.3-as Overleaf-zipje (`diplomamunka_v0_3.zip`), behozva a `thesis/`
mappába. Lefordítva: 65 PDF-oldal, ebből az 1–6. fejezet (törzsszöveg) 42 oldal, kb. 89 ezer karakter.
A fordítás hibátlan: nincs feloldatlan hivatkozás vagy kereszthivatkozás, csak néhány 1–8 pontos sortúllógás.

**Mihez mértem:** a kari útmutató (`thesis/utmutato/NIK_SZD_DM_TAJ_20252601_2025.pdf`, 4. feladat:
8–9. o., 2.2–2.4: 14–16. o., 1–3. melléklet), a DM II. tárgyleírás (`docs/diplomamunka-2.md`), a
feladatlap (F1–F6) és a megvalósítás eddigi állapota. A kari honlap (nik.uni-obuda.hu) ebből a
környezetből **nem érhető el** (a hálózati beállításban engedélyezni kellene); az ott közzétett,
esetleg frissebb kiírást a szerzőnek kell összevetnie ezzel a listával.

A szerző szövegét nem írtam át (D16/D20). Két technikai javítást végeztem a sablonban (lent, D).

Jelölés: ✅ megfelel · ⚠️ javítandó vagy döntés kell · ❌ a leadás előtt kötelezően pótolandó.

---

## A) Összkép

A beszámoló **tartalmilag és terjedelemben megfelel** a DM II. követelményeinek. A tárgyleírás nyolc
pontját és a feladatlap F1–F5 pontját lefedi; az F6 (eredmények) a DM III. feladata (D24).

**Leadás előtt kötelező (❌):**

1. A **konzultációs napló** kitöltése, a konzulens javaslatával és aláírásával. Most a sablon
   mintaadatai vannak benne (GIPSZ JAKAB). Az útmutató szerint ennek hiánya a tárgy letiltásával jár.
2. A **belső borítólapon** a mintaszám áll (T-000123/FI12904) a helyes törzskönyvi szám helyett.
   *(Már a 2026-10-01-i feladatlistán is szerepel.)*
3. A **prezentáció** (`…_PREZ`). Az útmutató 8. oldala szerint a DM II.-nél ezt is fel kell tölteni.
4. Az 1. fejezet egy bekezdéséből **hiányzik a hivatkozás** („Egy kutatás … 119 forrás alapján”, a
   `ndichu2026`). Hivatkozás nélküli átvett állítás plágiumnak minősülhet. *(Az október 7-i
   átnézésben is szerepelt.)*
5. A **fájlnevekben** a konzulens nevének alakja („Vorosne” vagy „BanatiBaumann”), és a **pontos
   határidő**: a 14. hét péntek 23:59 a Moodle-ben. Mindkettő nyitott kérdés.

---

## B) Leadandók és határidők (útmutató, 8–9. o.; tárgyleírás)

| Előírás | Állapot |
| --- | --- |
| Feltöltés a Moodle-be a szorgalmi időszak 14. hetének péntekén, 23:59-ig | ⚠️ a pontos dátumot a Moodle-ben ellenőrizni |
| Írásos összefoglaló: az útmutató szerint legalább 15–20 oldal, a tárgy kiírása szerint 30–35 oldal (a fedlap, a feladatlap és a napló nélkül) | ✅ 42 oldal (1–6. fejezet), az összefoglalóval együtt 44 |
| A szakdolgozat formai követelményei | ✅ / ⚠️ – lásd C) |
| Konzultációs napló a konzulens értékelésével és javaslatával, aláírva | ❌ sablon |
| Prezentáció | ❌ még nincs |
| Feladatlap (`…_FELADATLAP`), mindkét oldal | ✅ megvan (a zipben) |
| Fájlnevek ékezet nélkül: `<Neptun>_Nagy_<Konzulens>_BESZ` / `_PREZ` / `_KONZ` / `_FELADATLAP`, egy zipben | ⚠️ a konzulens nevének alakja nyitott |
| IP SCAN témabejelentés (a 9. hét utolsó munkanapja) | ✅ a szerző szerint megvolt |
| Beszámoló: a vizsgaidőszak 3. hetének péntekje, 8 perc, személyesen | – a diasor később |

---

## C) Formai követelmények (útmutató 2.2–2.3, 1–3. melléklet)

| Előírás | Állapot |
| --- | --- |
| A4; margó fent 40, lent 25, kívül 25, kötésoldalon 35 mm | ✅ |
| 1,5-es sorköz; Times New Roman, 12 pont, sorkizárt | ✅ |
| Oldalszám fent, a lap közepén, a széltől 20 mm-re; a számozás a tartalomjegyzéknél kezdődik | ✅ |
| Fejezetcím arab számmal, 14 pont, nagybetűs, **középre igazítva**, új lap tetején | ⚠️ **balra igazított** (D18, a szerző döntése). Az útmutató szerint középre kellene, és a „más szövegszerkesztőkre is érvényes” kitétel a LaTeX-et is érinti. Javaslat: kérdezd meg a konzulenst, vagy állítsd középre (`template.tex`: `\filright` helyett `\filcenter`). |
| Alfejezet legfeljebb 3 szint, 12 pont, félkövér, balra | ✅ |
| Ábrák és táblázatok fejezetenként számozva, címmel, hivatkozva a szövegben | ✅ a javítás után (D/1). Minden ábrára és táblázatra van hivatkozás. |
| A felhasznált ábrák, képek, **adatok forrása** feltüntetve | ⚠️ A táblázatcímek többségéből hiányzik a forrás. A 3. fejezet négy táblázatából a v0.3-ban kikerült a „(Forrás: saját összeállítás)”. Az 5.2. ábránál nincs forrás, a másik háromnál van. **Javaslat:** egységesen minden ábra- és táblázatcímbe; ahol a táblázat irodalmi adatokat foglal össze: „(Forrás: saját összeállítás [x, y] alapján)”. Ez a 2.1–2.3., 3.1–3.4. táblázatnál a legfontosabb. |
| Képletek: csak a hivatkozottakat kell számozni, fejezetenként | ✅ (a két számozott képletre nincs hivatkozás; ez megengedett, de a számozás el is hagyható) |
| Rövidítések összesítve a dolgozat elején vagy végén | ✅ a végén |
| Előlapok sorrendje: belső borítólap, feladatlap, hallgatói nyilatkozat, konzultációs napló | ✅ a sorrend; ❌ a borítólap és a napló tartalma (A/1–2) |
| | ⚠️ A DM III. üres konzultációs naplója is benne van. A DM II. beszámolóból kivehető (`main.tex`, az `includepdf` sora). |
| Absztrakt magyarul és angolul | ✅ |
| Összefoglaló magyarul 1500–2500 karakter, és angolul | ✅ 1832, illetve 1782 karakter |
| Hivatkozás [n] formában; irodalomjegyzék az első szerző szerint betűrendben | ✅ (biblatex, `sorting=nyt`) |
| Internetes forrásnál az URL és a megtekintés dátuma | ⚠️ **9 tételnél** van URL, de hiányzik a megtekintés dátuma: `ndichu2026`, `abdennebi2026lang`, `wei2025cortex`, `karner2026alertbert`, `vallabhaneni2026sentinel`, `uetz2026rba`, `liu2026hesp`, `langgraph2025`, `mcp2026spec`. Az arXiv-cikkek internetes források, ezért ide is kell az `urldate`. |
| Folyóiratcikknél a kötet és a kezdő–záró oldal | ⚠️ **30 cikknél** hiányzik a kötet- vagy az oldalszám. Ez régi feladat; pótlása a Crossrefből szkripttel lehetséges, ha a hálózati beállításban engedélyezed az `api.crossref.org`-ot. |
| Szó szerinti idézet idézőjelben | ⚠️ 1.2: „erős összehasonlítási alap” – idézőjelben áll, de fordítás, nem szó szerinti idézet. Vagy jelöld „(saját fordítás)”-ként, vagy írd át idézőjel nélkül. |
| A felépítés (3. melléklet) | ✅ A DM II.-ben az 1–6. pont, plusz az összefoglaló, a summary, az irodalomjegyzék és a jegyzékek. ⚠️ Az Ábrajegyzék és a Táblajegyzék számozott fejezet (10., 11.), a Rövidítések nem – egységesíteni érdemes (mind számozatlan). |

---

## D) Amit javítottam (technikai, a sablonban)

1. **A táblázatok számozása fejezetenként újrakezdődik.** Eddig folytatólagos volt (2.1–2.3, majd 3.4,
   …, 6.18), az útmutató 2. melléklete szerint hibásan. Most 2.1–2.3, 3.1–3.4, 4.1–4.4, 5.1–5.3,
   6.1–6.4. (`template.tex`: `\numberwithin{table}{section}`.)
2. A szerző v0.3-as változatát behoztam a `thesis/` mappába: `main.tex`, `acronyms.tex`, a
   `chapters/*.tex` és a három új fejezet. A személyes előlapok (feladatlap, borítólap) nem kerültek a
   gitbe (D15).

---

## E) Tartalmi követelmények

| DM II. követelmény (tárgyleírás) | Hol | Állapot |
| --- | --- | --- |
| 1. az elméleti háttér elmélyítése | 2. fejezet | ✅ |
| 2. a szakirodalom megismerése és kiértékelése | 3. fejezet | ✅ |
| 3. hasonló megoldások elemzése, összehasonlítása | 3. fejezet (3.1–3.4. táblázat), 4.1. táblázat | ✅ |
| 4. a saját megoldás részletes specifikációja és terve | 4–5. fejezet | ✅ |
| 5. a megvalósítási, illetve tesztkörnyezet terve | 6.1–6.2, 6.1. ábra | ✅ |
| 6. eszközök, módszerek választása indoklással | 4.1, 5.5 (5.3. táblázat) | ✅ |
| 7. a tesztelés, a tesztelhetőség és a mérőszámok terve | 6.3–6.5 | ✅ |
| 8. terjedelem legalább 30–35 oldal | 42 oldal | ✅ |

A feladatlap szerint az F1 a 2. fejezetben, az F2 a 3.-ban, az F3 a 4–5.-ben, az F4 az 5.-ben (terv),
az F5 a 6.-ban teljesül. Az F6 (eredmények elemzése, továbbfejlesztés) a DM III.-ra marad. Az
Összefoglalás utolsó mondata ezt jelzi.

---

## F) Az 1. fejezet nyelvi és tartalmi hibái

A sorszám itt bekezdést jelöl (`1_Bevezetes.tex`). A ⟲ jel azt mutatja, hogy a pont az október
7-i átnézésben is szerepelt (`docs/atnezesek/01_bevezetes_2026-10-07.md`).

| # | Hol | Észrevétel |
| --- | --- | --- |
| 1 | 1. bek. | **Tartalmi ellentmondás:** „IDS riasztások **szűrésére** és priorizálására” – a 4. fejezet első követelménye éppen az, hogy a rendszer **nem szűr** (riasztást nem távolít el). Javaslat: „csoportosítására és rangsorolására”. |
| 2 | 1. bek. | ⟲ Az IDS-t csak hálózati behatolásérzékelőként mutatod be, a dolgozat a gépi (Wazuh) riasztásokkal is dolgozik. Az „anomáliákat detektálni” pontatlan, a Suricata főleg szignatúrák alapján jelez. |
| 3 | 1. bek. | Nyelvi hibák: „Analyst-okat” → „elemzőket”; „Ezek a logok lehetne” → „lehetnek”; „logok” → „naplók” (az útmutató a zsargon kerülését kéri); „Mivel minden vállalatnál elmondható, hogy igénybe vesz…” – egyeztetési hiba; „néhány azon a problémák közül amivel” → „néhány azon problémák közül, amelyekkel”; vessző hiányzik: „megoldás kidolgozása, amely”, „rendszert, amely”. |
| 4 | 1.1, 1. bek. | „Az Uetz-cikk” – írásban: „Uetz és szerzőtársai”. A 0,5% csak a forgatókönyv **hálózati** riasztásaira igaz, ezt pontosítsd. ⟲ |
| 5 | 1.1, 2. bek. | ⟲ A hivatkozás a mondatzáró pont után áll, és két pont van: „(contextual). \cite{…}.” → „(contextual)~\cite{alahmadi2022}.” Ugyanez a 3. bekezdésben (`tariq2025`) és az 1.2 végén (`uetz2026rba`, `jalalvand2024`). „ezekből az egyik legfontosabb” – a forrás nem rangsorol. ⟲ |
| 6 | 1.1, 3. bek. | ⟲ „a kiadói kivonat ezek közül kiemeli” – munkajegyzet maradt benne, nem a dolgozatba való fordulat. |
| 7 | 1.1, 4. bek. | ❌ ⟲ **Nincs hivatkozás**: „Egy kutatás … 119 forrás alapján” (`ndichu2026`). |
| 8 | 1.2, 1. bek. | ⟲ Az RBA rövidítés és a 0,92/0,72 érték mérőszáma (rangsor-pontosság) magyarázat nélkül jelenik meg; a „44-ből 43” a **hálózati** riasztásokra vonatkozik. A „erős összehasonlítási alap” idézet fordítás (lásd C). |
| 9 | 1.2, 2. bek. | „A szakirodalom is számon tartja …, … rendszerezik” – hiányzik az alany (Jalalvand és szerzőtársai). ⟲ A Jalalvand-cikk számait még ellenőrizni kell. |
| 10 | 1.3 | ⟲ „több esetben … korlátozottan foglalkoznak az értékeléssel” – hivatkozás nélküli állítás. Ugyanitt: „a kockázat esetén a riasztáshoz köthető további a környezet szempontjából releváns sérülékenységek” – hibás szerkezet; „nem egy LLM-t értünk hanem,” → „nem egy LLM-et értünk, hanem”. |
| 11 | 1.1 | A kérdés formájú bekezdésnyitások („Mit is gondolnak erről az elemzők?”, „Mi történik, ha…”) kötetlen hangvételűek. ⟲ |

A 2–6. fejezetben nyelvi hibát nem találtam, amely a leadást akadályozná. A 4–6. fejezet az írási
csomagokra épül. Apróság: a `6_Teszteles.tex` első sorában a megjegyzés „% 5. fejezet”.

---

## G) Egyezés a megvalósítással (amit a DM II. szövege állít, és ami elkészült)

A DM II. tervet ír le, de ahol a megvalósítás már eldőlt, a szöveg ne mondjon mást.

| # | Hol | Eltérés | Javaslat |
| --- | --- | --- | --- |
| 1 | 4.2.3 (és 5.3.3) | A szöveg szerint a semleges 0,5 csak akkor jár, „ha a gép szoftverkészlete nem ismert”. A megvalósításban akkor is, ha a gép ismeretlen, vagy ha a szabály nem köthető szolgáltatáshoz (például karbantartási jelzés). | Egy félmondattal bővíteni. |
| 2 | 6.1 utolsó bek., 5.4 | „a nyilvántartást a hálózat közzétett leírásából állítom össze” – a szerepek és a szolgáltatások onnan valók, az **IP-címek** viszont a riasztások szerkezetéből, rögzített szabályokkal (G1–G9, `results/08_…`). A „címkék megtekintése előtt” a russellmitchellnél pontatlan, mert az adatfeltáráskor (október 1.) a címkéit láttuk. | „…a gépek szerepét és szolgáltatásait a hálózat közzétett leírásából, a címeket a riasztások szerkezetéből, előre rögzített szabályokkal; a fokozatokat a gépek szerepéből, a címkék felhasználása nélkül.” |
| 3 | 6.4 (program tesztelése) | „minden mérés rögzíti … a felhasznált adatfájlok ellenőrzőösszegét” – most a letöltő szkriptek ellenőrzik az MD5-öt, az eredményfájlok fejléce viszont csak a programverziót írja ki. | **A kódot igazítom**: az eredményfájlok fejlécébe bekerül az adatfájlok ellenőrzőösszege. Így a szöveg marad. |
| 4 | 6.3 (plafonhatás) | A zajjal kiegészített AIT-ADS-en (Karner 2026) végzett mérés még nem készült el. | A DM II.-ben tervként maradhat; a DM III.-ig vagy elvégezzük, vagy a szöveg módosul. |
| 5 | 6.3 (statisztika) | A mérés előtt rögzített terv (D29) Holm-korrekciót és a hiányos nyilvántartásnál 20 ismétlést is tartalmaz; a szöveg ezeket nem említi. | Nem kötelező; egy-egy félmondat erősíti a módszertant. |
| 6 | 5.5, 6.4 | A LangGraph-változat egyezésének tesztje még nem készült el. | Terv, a DM III. feladata – a DM II.-ben rendben van. |

---

## H) Teendők a leadásig – összesítve

**A szerzőnek:**
- ❌ konzultációs napló (kitöltés, konzulensi javaslat, aláírás);
- ❌ a belső borítólap törzskönyvi száma;
- ❌ prezentáció;
- ❌ a `ndichu2026` hivatkozás az 1.1-ben;
- ⚠️ az 1. fejezet F/1–11 pontjai;
- ⚠️ a G/1–2 félmondatok;
- ⚠️ a fejezetcímek igazítása (konzulenssel egyeztetve);
- ⚠️ forrásjelölés a táblázatcímekben;
- ⚠️ a fájlnevek és a pontos határidő.

**Claude (kérésre):**
- az `urldate` a 9 internetes forrásnál;
- a kötet és az oldalszámok a 30 cikknél (`api.crossref.org` kell);
- az ellenőrzőösszeg az eredményfájlokban (G/3);
- a prezentáció vázlata (8 perc, kevés szöveg, sok ábra);
- a DM III. konzultációs napló kivétele a DM II. változatból.

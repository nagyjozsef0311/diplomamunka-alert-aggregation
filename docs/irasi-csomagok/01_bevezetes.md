# Írási csomag – 1. fejezet: Bevezetés

2026-10-01 · A szerzőnek szóló **javaslat** (D16): mit érdemes kifejteni, milyen sorrendben, melyik
forrással. Kész mondatot szándékosan nem tartalmaz; a fejezet szövegét a szerző fogalmazza meg.
Ebből a fájlból semmit ne másolj át szó szerint a dolgozatba.

## Mit vár el az útmutató ettől a fejezettől

- Kari útmutató, 3. melléklet, 1. pont: *a megoldandó probléma megfogalmazása, felvétele, a dolgozat
  célja, felépítése*.
- Feladatlap: a probléma (riasztási terhelés a SOC-ban), a cél (agent-alapú, metrika-vezérelt
  riasztás-összevonás), a feladat (szakirodalom, tervezés, megvalósítás, értékelés).
- Terjedelem: a Diplomamunka II. beszámolóban kb. **3 oldal** (`docs/diplomamunka-2.md`), a végleges
  dolgozatban 4–5 oldal.

## Javasolt felépítés (4 rész)

A részek témája javaslat; az alfejezetcímeket a saját szavaiddal add meg.

### 1. A probléma: a riasztások mennyisége és a riasztási fáradtság (kb. 1 oldal)

Kulcspontok, amelyeket érdemes érinteni:

- A behatolásérzékelők (hálózati: Suricata; gépi: Wazuh) sok riasztást adnak; ezek nagy része téves
  vagy kis jelentőségű; az elemzők ideje véges.
- A következmény: a valós támadás elveszhet a zajban; az elemzők kiégnek, „vakon” elnyomó szabályokat
  vezetnek be, vagy csak a súlyosságra hagyatkoznak.
- **Saját tapasztalat:** SOC-mérnökként saját megfigyelésed erős motiváció lehet (milyen arányban téves
  egy tipikus riasztás, mire jut idő egy műszakban). Ha konkrét számot írsz, jelöld, hogy saját
  tapasztalat, vagy hivatkozz forrásra.

Források ehhez:

| Állítás | Forrás (BibTeX-kulcs) | Ellenőrzés |
| --- | --- | --- |
| Az elemzők szemszögéből a riasztások túlnyomó része téves; ez a munkájuk egyik fő nehézsége | Alahmadi és mtsai. 2022, `alahmadi2022` (USENIX Security; a cím: „99% False Positives…”) | Korábbi kutatási jegyzetből – **a pontos megállapítást olvasd el a cikkben** |
| A riasztási fáradtság okai: munkaerőhiány, sok téves riasztás, túlterhelt felületek, nem hatékony eljárásrendek | Tariq és mtsai. 2025, `tariq2025` (ACM Computing Surveys) | Korábbi jegyzetből (`kutatasi_jegyzet_01.md`) – olvasd el |
| A SOC-ok szervezeti és működési problémái | Kokulu és mtsai. 2019, `kokulu2019`; Vielberth és mtsai. 2020, `vielberth2020` | Korábbi jegyzetből |
| Az elemzők elnyomó szabályokat vezetnek be, vagy csak a súlyosság szerint döntenek, és ez vakfoltot okoz; a csak súlyosság szerinti rangsor kevés | Ndichu és mtsai. 2026, `ndichu2026` (arXiv:2605.08316, áttekintés) | **2026-10-01-én ellenőrizve** (alphaXiv: a cikk létezik, a szerzők egyeznek) |
| Hazai, emberi tényezős nézőpont a SOC-csapatokról | Hámornik és Krasznay 2017, `hamornik2017` | Korábbi jegyzetből |

### 2. A meglévő megoldások és a rés (kb. 0,5–1 oldal)

Kulcspontok:

- A riasztások összevonása és rangsorolása régóta kutatott terület (rövid utalás; a részletek a 3.
  fejezetbe tartoznak, itt ne fejtsd ki).
- A legerősebb, környezetet nem használó módszer a kockázatalapú riasztás-pontozás: nyolc adathalmazon
  átlagosan 0,92-es rangsor-pontosság.
- **A rés:** ez a módszer nem veszi figyelembe, mennyire fontos az érintett gép, és van-e rajta a
  támadás által kihasználható sérülékenység. A szakirodalom szerint a gép fontossága és a sérülékenység
  ismert szempont, de a riasztás-rangsorolásban ritkán mérik a hozzáadott értékét.
- Az áttekintések szerint kevés munkát értékelnek valós vagy valósághű környezetben (Ndichu: a 87
  vizsgált tanulmányból 9 közöl éles, terepi eredményt) – ez indokolja a kétpályás (nyilvános adathalmaz
  + saját labor) értékelést.

Források ehhez:

| Állítás | Forrás | Ellenőrzés |
| --- | --- | --- |
| Kockázatalapú riasztás-pontozás, CATS, átlagos rangsor-pontosság 0,92 (szórás 0,09) nyolc adathalmazon | Uetz és mtsai. 2026, `uetz2026rba` (arXiv:2609.02465) | **2026-10-01-én ellenőrizve** (a kivonatban szerepel) |
| A priorizálási szempontok öt csoportja (elemző, riasztás, eszköz, szervezet, külső környezet); 89 cikk alapján | Jalalvand és mtsai. 2024, `jalalvand2024` (ACM Computing Surveys) | Korábbi jegyzetből – olvasd el |
| A 87 vizsgált tanulmányból csak 9 közöl éles SOC-adaton végzett értékelést | Ndichu és mtsai. 2026, `ndichu2026` | **2026-10-01-én ellenőrizve** |

### 3. A dolgozat célja és a kutatási kérdések (kb. 0,5–1 oldal)

Kulcspontok:

- A cél a feladatlap szerint: agent-alapú, metrika-vezérelt riasztás-összevonási modell tervezése,
  megvalósítása és értékelése infrastrukturális, kockázati és monitorozási szempontok alapján.
- Az öt kutatási kérdés (mérőszámok; a környezet ábrázolása; agent-alapú felépítés; a terhelés
  csökkenése; a rangsor minősége) – lásd `docs/kutatasi-eredmenyek.md`. A kérdéseket a saját
  szavaiddal fogalmazd meg.
- Mit **nem** vállal a dolgozat (lehatárolás): nem új behatolásérzékelő, nem gépi tanulásos osztályozó,
  a nyelvi modell nem dönt és nem ad pontszámot (D3, D12).
- A Diplomamunka II.-ben a tervezés és a specifikáció, a III.-ban a megvalósítás és a mérés – ezt egy
  mondatban érdemes jelezni.

Javasolt táblázat (elkészítem, ha kéred): **a kutatási kérdések és a dolgozat fejezetei** – melyik
kérdésre melyik fejezet ad választ. A cellák szövegét te adod meg vagy hagyod jóvá.

### 4. A dolgozat felépítése (kb. 0,5 oldal)

Kulcspontok:

- Fejezetenként egy-két tagmondat arról, mi következik (a `docs/diplomamunka-2.md` vázlata szerint).
- Javasolt ábra (elkészítem, ha kéred): **a dolgozat felépítése** – a fejezetek egymásra épülése
  egyszerű folyamatábrán (elmélet → szakirodalom → specifikáció → terv → tesztelési terv).

## Ábrajavaslatok ehhez a fejezethez

| Ábra | Mit mutat | Forrás az ábra alá |
| --- | --- | --- |
| A riasztások útja a SOC-ban | Suricata és Wazuh → riasztások → elemzői sor; jelölve, hol avatkozik be a dolgozat (összevonás, rangsorolás) | Saját ábra |
| A dolgozat felépítése | A fejezetek sorrendje és kapcsolata | Saját ábra |

Mindkettőt `thesis/img/`-be készíteném vektorgrafikusan (PDF), a te jóváhagyásod után.

## Figyelj rá

- **Rövidítések:** első előfordulásnál írd ki (pl. biztonsági műveleti központ, angolul Security
  Operations Center, SOC), és vedd fel az `acronyms.tex`-be (a `main.tex`-ben a Rövidítések rész
  kommentjét ekkor töröld).
- **Számokat csak forrással** (vagy „saját tapasztalat” jelöléssel).
- **Angol forrásból vett gondolat:** saját szavaiddal, hivatkozással. Szó szerinti idézet csak
  idézőjelben, hivatkozással; saját fordításnál jelöld: „(saját fordítás)”.
- **Hivatkozás LaTeX-ben:** `\cite{uetz2026rba}` → [n]; több forrás egyszerre: `\cite{tariq2025,ndichu2026}`.
- Egy forrást csak akkor hivatkozz, ha legalább a kivonatát és a hivatkozott részt elolvastad.
- A `docs/` mappa szövegeit (kutatási jegyzetek, eredmények) korábban Claude írta: forrásként használd
  őket, de **ne vedd át a megfogalmazásukat**.

## Ha elkészültél

Töltsd fel a zipet (vagy csak a `chapters/1_Bevezetes.tex`-et). Átnézem, és a beszélgetésben jelzem:
formai hibák, hiányzó hivatkozás, rövidítés, ellentmondás a döntésnaplóval. A szövegedet nem írom át.

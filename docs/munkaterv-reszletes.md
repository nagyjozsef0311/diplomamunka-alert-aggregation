# AIT-ADS munkaterv

Oct 1, 2026 · @Csoza

## Cél

December első hetére legyen meg az első mérhető eredmény az AIT-ADS nyilvános riasztás-adathalmazon. Az eredmény azt mutatja meg, mennyit javít a riasztások rangsorán a gépek fontossága és a sérülékenységi információ a kockázatalapú pontozáshoz képest. Ehhez nem kell labor: a riasztások letölthető fájlok, a munka Pythonban, offline folyik.

A végére ez lesz kész:

- egy Python-csomag, amelyben az agentek függvényként vagy modulként működnek (egységesítő, csoportosító, környezet, sérülékenység, rangsoroló) – később ugyanez fut a laborban is;
- egy kis gépnyilvántartás-adatbázis a nyolc AIT-forgatókönyvhöz;
- a két összehasonlítási alap (súlyosság szerinti rangsor és a kockázatalapú pontozás) eredményei;
- a lépésenkénti bővítés első mérési táblázata, amiből a dolgozat értékelési fejezetének első váza lesz.

Utána jön a vegyes (VMware + Docker) labor, ahol ugyanez a kód élő riasztásokon fut, és ott kerül be a nyelvi modelles magyarázó agent is.

## Az adathalmaz

Az AIT-ADS egy kb. 96 MB-os tömörített fájl és egy apró címkefájl. Szabadon felhasználható (CC BY 4.0 licenc), csak hivatkozni kell rá. A munkához két forrásból lehet kiindulni: az eredeti kiadásból, illetve az Uetz-cikk szerzőinek már felcímkézett, átalakított változatából.

| Forrás | Mi van benne | Mire jó |
| --- | --- | --- |
| [Zenodo: AIT Alert Data Set, 1. verzió](https://zenodo.org/record/8263181) | `ait_ads.zip` (96,2 MB) és `labels.csv` (3,7 kB); forgatókönyvenként `<forgatókönyv>_wazuh.json` és `<forgatókönyv>_aminer.json` | A teljes, eredeti adat mind a 8 forgatókönyvre |
| [GitHub: ait-aecid/alert-data-set](https://github.com/ait-aecid/alert-data-set) | A gyártó szkriptek (`analyze.py`, `filter.py`), a címkézés logikája | Pontosabb, eseményszintű címkék készítése, a lépések ellenőrzése |
| [GitHub: CATS (Uetz et al.)](https://github.com/962012d09b/cats) | `ait_wazuh.zip` és `ait_suricata.zip` egységes JSON-sor formátumban, minden riasztás mellett „támadás / nem támadás” címkével | Azonnal használható kiindulás és pontosan összevethető összehasonlítási alap |

A tartalom lényege:

- **Három riasztórendszer van benne, ebből kettő kell nekünk.** A Suricata hálózati riasztásai a Wazuh-fájlokban vannak, mert a Wazuh gyűjtötte őket. Az AMiner-riasztásokat – az Uetz-cikkhez hasonlóan – kihagynám: hiányzik belőlük a gépnév és a súlyosság, és anomáliadetektort nem használunk a laborban sem.
- **Méret:** összesen kb. 2,66 millió riasztás, ebből 86% Wazuh, 12% Suricata. A legkisebb forgatókönyv (russellmitchell) néhány másodperc alatt feldolgozható, ezzel érdemes kezdeni.
- **Címkék:** a `labels.csv` csak a támadási szakaszok kezdetét és végét adja meg. Ami a szakaszba esik, az „támadás”, ami kívül, az „téves riasztás”. Ez durva címkézés: egy támadás alatt véletlenül felbukkanó jóindulatú riasztás is „támadás” lesz. A pontosabb, eseményszintű címkéhez az AIT nyers log-adathalmaza is kell.

**Javaslat:** a CATS-változattal kezdjünk, mert az azonnal használható, és az eredményeink közvetlenül összevethetők az Uetz-cikkével. Utána terjesszük ki a mérést az eredeti adatból mind a 8 forgatókönyvre.

## Lépések hetekre bontva

Kilenc hét, heti kb. 8–10 óra munkával számolva. Minden lépés végén van egy ellenőrizhető „kész” feltétel, így mindig látszik, hol tartasz. Az utolsó hét tartalék is.

| Hét | Feladat | Eredmény | Akkor kész, ha |
| --- | --- | --- | --- |
| 1. (okt. 5–11) | Python-projekt létrehozása verziókezeléssel; a CATS-féle és az eredeti AIT-adat letöltése; ismerkedés az adattal (mezők, riasztástípusok, időtartam) | Egyoldalas adatleírás | Minden használt mező jelentése ismert |
| 2. (okt. 12–18) | **Egységesítő agent:** közös riasztás-formátum (idő, forrás- és cél-IP, gépnév, szabály, súlyosság, sérülékenység-hivatkozás, támadási technika) | Egy modul, amely a Suricata- és a Wazuh-riasztást is átalakítja | A CATS-adatból és az eredetiből ugyanazokat a riasztásokat kapjuk |
| 3. (okt. 19–25) | **Összehasonlítási alapok:** súlyosság szerinti rangsor, majd a CATS lefuttatása a russellmitchell forgatókönyvre | Az első két mérési sor | A saját mérésünk kb. ±0,02-en belül visszaadja a cikk számait |
| 4. (okt. 26–nov. 1) | **Gépnyilvántartás** a russellmitchell forgatókönyvhöz: gépek, zónák, szoftververziók, sérülékenységek | Kis SQLite-adatbázis + a kitöltés leírása | Minden riasztás célpontja egyértelműen géphez köthető |
| 5. (nov. 2–8) | **Környezet- és sérülékenységi agent:** a gép fontossága, zónája, és hogy működhet-e rajta a támadás | Minden riasztás mellé kiszámolt környezeti értékek | Minden riasztásnál van érték vagy dokumentált „ismeretlen” |
| 6. (nov. 9–15) | **Rangsoroló agent:** a súlyok beállítása páros összehasonlítással (te mint szakértő), konzisztencia-ellenőrzés; a lépésenkénti bővítés mérése | Az első teljes eredménytáblázat egy forgatókönyvre | A táblázat minden lépéséhez van rangsor-pontosság és átlagos pontosság |
| 7. (nov. 16–22) | **Csoportosító agent:** időablakos és közös IP-cím/felhasználó alapú csoportok, a csoportok tisztaságának mérése | Csoportosítási eredmények, riasztásszám-csökkenés | Ismert, hányszoros a csökkenés, és hány támadás csúszik át |
| 8. (nov. 23–29) | **Kiterjesztés mind a 8 forgatókönyvre:** a többi 7 gépnyilvántartása sablonból; érzékenységvizsgálat; adatból tanult súlyok összevetésként | Eredmények forgatókönyvenként és átlagban | Minden mérés megismételhető egy paranccsal |
| 9. (nov. 30–dec. 6) | Összegzés és tartalék: ábrák, táblázatok, rövid anyag a konzulensnek | Az értékelési fejezet első vázlata | A konzulens megkapta |

A szakirodalmi fejezetek (1–2.) írása ezzel párhuzamosan, heti egy-két órában mehet.

## Összehasonlítási alapok

A CATS kódja elérhető a GitHubon, így a kockázatalapú pontozást nem kell újra megírni: lefuttatjuk, és ugyanazokat a számokat kapjuk, mint a cikk. A tároló Docker Compose-zal indítható, van benne webes felület és egy kötegelt futtató, amely a súlyokat is képes optimalizálni.

| Alap | Hogyan működik | Honnan van | Várható eredmény |
| --- | --- | --- | --- |
| Rangsor csak súlyosság szerint | A riasztási szabály súlyosságát 0 és 1 közé skálázzuk, ez a pontszám | Saját, néhány sor kód; a CATS-ben is benne van | A cikkben átlagosan 0,72-es rangsor-pontosság |
| Kockázatalapú pontozás (CATS) | Öt részpontszám súlyozott átlaga: súlyosság, halmozódás (1 perces ablak), változatosság (1 órás ablak), ritkaság és szabálytalanság (1 napos ablak) | [CATS tároló](https://github.com/962012d09b/cats), `backend/` és `tools/batch_processor/` | A cikkben átlagosan 0,92 |

A cikk által általános használatra ajánlott súlyok: súlyosság 12%, halmozódás 24%, változatosság 44%, ritkaság 10%, szabálytalanság 10%. Ezt használjuk alapbeállításnak, hogy ne mi „hangoljuk jóra” a vetélytársat.

### Hogyan illesszem be a saját mérőszámaimat?

| Lehetőség | Mellette | Ellene | Döntés |
| --- | --- | --- | --- |
| **Saját részpontszámok új CATS-modulként** (gép fontossága, alkalmazhatóság, megfigyeltség) | Ugyanaz a mérőeszköz és ugyanazok a mérőszámok, mint a cikkben; a cikk kifejezetten erre biztat | Meg kell ismerni a CATS belső felépítését | **Javasolt az értékeléshez** |
| Minden saját kódban, a CATS csak viszonyítási számokat ad | Teljes kontroll | A mérőszámokat külön kell megírni és egyeztetni | Tartalék megoldás |

A két út nem zárja ki egymást. Az agentek saját Python-csomagban élnek, mert ez kell a laborhoz. Az értékeléshez a csomag függvényeit egy vékony CATS-modul hívja meg.

**Figyelni kell:** a tároló jelenleg névtelenített (a cikk bírálata miatt), és nincs megadott licence. A dolgozatban a cikkre és a tárolóra hivatkozni kell, a letöltött változatot pedig érdemes elmenteni, ha a cím később megváltozna.

## Gépnyilvántartás az AIT-ADS-hez

A nyilvántartás az AIT nyers log-adathalmazának leírásából ([Landauer et al. 2023](https://doi.org/10.1109/TDSC.2022.3201582)) építhető fel. Mind a 8 forgatókönyv ugyanazt a hálózatot használja, csak a felhasználói gépek és a levélkiszolgálók száma, valamint az IP-címek térnek el. Ezért egy sablon kell, amit forgatókönyvenként kitöltünk.

| Zóna | Gép (szerep) | Szoftver és verzió a leírás szerint | Javasolt fontosság (1–5) |
| --- | --- | --- | --- |
| Belső háló | Belső webkiszolgáló | WordPress 5.8.2 a sérülékeny wpDiscuz bővítménnyel (CVE-2020-24186, korlátlan fájlfeltöltés) | 5 |
| Belső háló | Fájlmegosztó | Samba 4.5.9 | 5 |
| Belső háló | Felhasználói gépek (3–9 db) | Ubuntu 20.04 | 2 |
| Határterület (DMZ) | VPN-kiszolgáló | OpenVPN 2.4.4 | 4 |
| Határterület (DMZ) | Levelező | Horde Groupware 5.2.17 | 4 |
| Határterület (DMZ) | Felhőtárhely | OwnCloud 10.5.0 | 3 |
| Határterület (DMZ) | Proxy | – | 3 |
| Zónák között | Tűzfal és belső névfeloldó | Shorewall 5.1.12.2 | 4 |
| Internet | Külső névfeloldó, külső levelezők, távoli és külső felhasználók, támadó | MaraDNS 2.0.13, Dnsmasq 2.79 | 1 (nem a cégé) |

A fontossági értékek az én javaslataim a gép szerepe alapján. A dolgozatban egy rövid szabálykészlet indokolja őket (üzleti adat, elérhetőség kifelé, helyettesíthetőség), és ezeket te véglegesíted.

### Így töltjük ki

1. **Gépek és IP-címek:** a Wazuh-riasztásokban szerepel a gépnév, a Suricata-riasztásokban a forrás- és cél-IP. Ezekből forgatókönyvenként kiolvasható, melyik IP melyik gépé. Ellenőrzésnek ott vannak az AIT log-adathalmaz gépenkénti adatai.
2. **Szoftverek:** a fenti táblázatból, a szabványos szoftver-azonosítóval (CPE) kiegészítve.
3. **Sérülékenységek:** a szoftver-azonosítók alapján az amerikai nemzeti sérülékenység-adatbázisból (NVD) kérdezzük le, egy szkripttel, dátummal rögzítve. Az így kapott listát „2022 elején ismert” állapotra szűrjük, mert az adatok akkor készültek.
4. **Megfigyeltség:** az AIT-ben minden gép naplóit feldolgozták, ezért a megfigyeltség itt mindenhol egyforma. Ezt a mérőszámot így csak a laborban lehet érdemben vizsgálni, ezt a dolgozatban őszintén le kell írni.

**Ellenőrizendő:** a wpDiscuz pontos verziószáma (a hibát a 7.0.0–7.0.4 változatok tartalmazzák), illetve a proxy szoftvere. Mindkettő kiolvasható az AIT tesztkörnyezet nyilvános telepítő szkriptjeiből.

## Mérési szabályok

A szabályokat a mérés előtt rögzítjük, hogy az eredményt ne lehessen utólag „szebbre hangolni”. Ez a leggyakoribb módszertani hiba a területen (Arp et al. 2022).

| Szabály | Tartalma | Miért |
| --- | --- | --- |
| Szakértői súlyok előre rögzítve | A páros összehasonlítást a 6. héten kitöltöd, a súlyokat dátummal elmented, és utána már nem változtatod | Így a súlyok nem a tesztadathoz igazodnak |
| Adatból tanult súlyok „egyet kihagyunk” módon | 7 forgatókönyvből tanulunk, a 8.-on mérünk, és ezt mind a nyolccal megismételjük | Így látszik, mennyire általánosíthatók a súlyok |
| Wazuh és Suricata külön is | A gépi (Wazuh) és a hálózati (Suricata) riasztásokat külön és együtt is mérjük | Az Uetz-cikk is külön mérte őket, így összevethető |
| Rangsor-mérőszámok | Rangsor-pontosság (AUROC), átlagos pontosság (AP), valós riasztások aránya a lista első 10%-ában | Az egész rangsort értékelik, nem egy küszöböt |
| Csoportosítási mérőszámok | Riasztásszám-csökkenés, elszalasztott támadások aránya (legfeljebb 2%), csoportok tisztasága | A terhelés csökkenése csak biztonsági korláttal értékes |
| Összesítés | Átlag és szórás a 8 forgatókönyvre; a változatok páros összevetése egyszerű statisztikai próbával (Wilcoxon-próba) | Egyetlen forgatókönyv eredménye lehet véletlen |
| Megismételhetőség | Rögzített szoftververziók, egy parancs futtatja a teljes mérést, az eredmények CSV-be mennek | A bíráló és a konzulens is ellenőrizheti |

A címkék időszakaszon alapulnak (lásd fent). Ha marad idő, az eseményszintű címkékkel is lefuttatjuk a mérést, és megnézzük, mennyire változik az eredmény.

## Kockázatok és nyitott kérdések

A legnagyobb kockázat az, hogy az AIT-ADS-ben kevés olyan hálózati riasztás van, amely konkrét sérülékenységre hivatkozik. A cikk detektorlistája alapján a Suricata itt főleg névfeloldási, TLS- és általános szabályokon jelez, a WordPress-támadást pedig inkább a Wazuh webes szabályai fogják meg. Emiatt az „működhet-e a támadás ezen a gépen” mérőszám itt ritkán szólalhat meg. Az első adatfeltárás (október 1., russellmitchell forgatókönyv) ezt meg is erősítette: a 23 116 Wazuh- és 9 186 Suricata-riasztás közül egyik sem hivatkozik sérülékenység-azonosítóra. A Suricata-riasztásokban gépnév sincs, ott IP-cím alapján kell illeszteni.

| Kockázat | Mi történhet | Kezelése |
| --- | --- | --- |
| Kevés sérülékenységre hivatkozó riasztás | Az alkalmazhatóság alig javít az AIT-ADS-en | Durvább illesztés is: webes támadás WordPresst futtató gépre, port és szolgáltatás szerint. A laborban szándékosan használunk konkrét sérülékenységre írt Suricata-szabályokat. |
| A CATS-tároló címe vagy tartalma változik | A bírálat után átnevezik vagy átalakítják | Most másold le (saját privát másolat), és jegyezd fel a letöltés dátumát |
| Zajos, időszakaszos címkék | A támadás alatti jóindulatú riasztások is „támadásnak” számítanak | A dolgozatban leírjuk; ha marad idő, eseményszintű címkékkel ellenőrzünk |
| A Wazuh-riasztásokban nincs cél-IP | A riasztás nem köthető a gépnyilvántartáshoz | A gépnév (a Wazuh agent neve) alapján illesztjük |
| A CATS belső felépítése bonyolult | Csúszás a 3. és 6. hét körül | Tartalék: a mérőszámokat saját kód számolja, a CATS csak viszonyítási számot ad |
| 8 forgatókönyv kézi nyilvántartása sok munka | Csúszás a 8. héten | Sablon + szkript, amely a riasztásokból kigyűjti a gépneveket és IP-címeket |

Nyitott kérdések:

- [ ] A konzulens jóváhagyja-e az irányt (környezeti információ a kockázatalapú pontozáshoz képest)?
- [ ] Hol éljen a kód: privát GitHub-tárolóban, vagy a saját gépeden?
- [ ] Mikor kezdjük a labor tervezését: a 3. hét után párhuzamosan, vagy az AIT-rész lezárása után?

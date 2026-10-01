# Metrika-katalógus és adathalmazok

A `thesis/forrasok.xlsx` „Metrika-katalógus” és „Adathalmazok” lapjának szöveges változata (2026-09-21-i állapot).
A kódokat (A1, S1, …) csak belső hivatkozásra használjuk; a felhasználónak szóló anyagokban a metrika nevét írjuk ki.

Fontos későbbi pontosítások (2026-10-01):

- A sérülékenységi illeszkedés (V2) az AIT-ADS-en csak szolgáltatás-/termékszintű lehet, mert egyetlen riasztás sem hivatkozik CVE-re. CVE-szintű illesztés: saját labor.
- A V2 súly, nem szűrő: a nem illeszkedő riasztás pontot veszít, de nem tűnik el.
- A megfigyeltség (C1) bizonytalansági jelző, nem büntetés; az AIT-ADS-en mindenhol egyforma, ezért csak a laborban mérhető.

## Metrikák

| Kód | Kategória | Metrika | Definíció | Számítás / skála | Adatforrás | Agent | Forrás | Javaslat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | Riasztás | Súlyosság (severity) | A detektor által adott súlyossági szint | Suricata priority 1–3 / Wazuh rule.level 0–15 → normalizálás [0,1] | Suricata eve.json, Wazuh alerts | Riasztás-feldolgozó | Anuar 2012; Shah 2019; Jalalvand 2024 | Alap – biztosan |
| A2 | Riasztás | Szignatúra megbízhatóság | Az adott szabály/szignatúra korábbi valós-pozitív aránya | TP/(TP+FP) szignatúránként, címkézett előzményből; hiányzó adatnál prior | Címkézett riasztás-előzmény (szimulációból ismert ground truth) | Riasztás-feldolgozó | Alahmadi 2022; Julisch 2003; Alsubhi 2008 (sensor sensitivity) | Alap – biztosan |
| A3 | Riasztás | Gyakoriság / ismétlődés | Azonos (szignatúra, forrás, cél) hármas előfordulása időablakban | count / időablak; log-skálázás | Suricata, Wazuh | Aggregáló | Anuar 2012; Valeur 2004 | Alap – aggregációhoz |
| A4 | Riasztás | Ritkaság (rareness) | Mennyire szokatlan a riasztás a történeti alapvonalhoz képest | 1 − P(szignatúra / eszköz, előzmény) vagy IDF-szerű súly | Riasztás-előzmény | Riasztás-feldolgozó | Jalalvand 2024 (Table 2); Hassan 2019 (NoDoze); Uetz 2026: a ritkaság önmagában NEM jobb a véletlennél | Opcionális – gyenge empirikus támogatás |
| A7 | Riasztás | Halmozódás és változatosság (RBA) | Ugyanazon entitáson rövid időn belül hány és hány különböző szabály jelez | accumulation (1 perc) és variety (1 óra) ablak, háromszög-kernellel | Suricata, Wazuh | Priorizáló | Uetz 2026 (legerősebb két RBA-hipotézis) | Alap – bizonyítottan erős |
| A5 | Riasztás | Több-szenzoros megerősítés | Hány független detektor jelez ugyanarra az eseményre | szenzorok száma (NIDS + HIDS) az aggregált csoportban | Suricata + Wazuh agent | Aggregáló | Valeur 2004 (fúzió); Jalalvand 2024 | Ajánlott |
| A6 | Riasztás | Támadási fázis (ATT&CK / kill chain) | A riasztás mely taktikához tartozik; későbbi fázis = magasabb súly | ATT&CK taktika → ordinális súly | Wazuh rule.mitre mező; Suricata szabály metaadat | Kontextus / korrelációs | Wilkens 2021; Guo 2026 | Ajánlott |
| S1 | Eszköz (CMDB) | Eszközkritikalitás | Az érintett eszköz üzleti fontossága | 1–5 ordinális skála (CMDB mező) | Asset-adatbázis (CMDB) | Kontextus | Porras 2002; Anuar 2012; Jalalvand 2024 | Alap – biztosan |
| S2 | Eszköz (CMDB) | CIA-követelmény | Az eszközön kezelt adat bizalmassági/sértetlenségi/rendelkezésre állási igénye | C, I, A ∈ {alacsony, közepes, magas} → CVSS environmental-szerű súly | CMDB | Kontextus | Jalalvand 2024 (Table 2); Alsubhi 2008 (importance) | Ajánlott |
| S3 | Eszköz (CMDB) | Pótolhatóság / karbantarthatóság | Mennyi idő/költség az eszköz helyreállítása | 1–5 ordinális | CMDB | Kontextus | Anuar 2012 | Opcionális |
| S4 | Eszköz (CMDB) | Kitettség (exposure) | Hálózati zóna: internet felé nyitott / DMZ / belső | zóna → súly (pl. 1.0 / 0.7 / 0.4) | CMDB + hálózati topológia | Kontextus | Ndichu 2026 (asset-context features) | Ajánlott |
| V1 | Sérülékenység | Eszköz sérülékenységi szint | Az eszköz nyitott sérülékenységeinek súlyossága | max(CVSS) vagy súlyozott összeg a nyitott CVE-kre | Wazuh Vulnerability Detector | Sérülékenységi | Jalalvand 2024; Farris 2018 | Alap – biztosan |
| V2 | Sérülékenység | Támadás alkalmazhatósága (applicability) | Illeszkedik-e a riasztott támadás az eszköz tényleges szolgáltatására/OS-ére/CVE-jére | bináris vagy 0/0.5/1 (CVE-egyezés / szolgáltatás-egyezés / nincs egyezés) | Suricata szignatúra CVE-referencia × Wazuh sérülékenység-lista × CMDB szolgáltatások | Sérülékenységi | Valeur 2004 (verifikáció); Alsubhi 2008 (applicability); Porras 2002 (relevance) | Alap – ez a legerősebb FP-szűrő |
| V3 | Sérülékenység | Kihasználhatóság (EPSS / KEV) | Mennyire valószínű a CVE aktív kihasználása | EPSS valószínűség; CISA KEV tagság → bónusz | Külső feed (FIRST EPSS, CISA KEV) | Sérülékenységi | Ndichu 2026 (threat intel); Jalalvand 2024 (exploitability) | Opcionális – külső adat |
| C1 | Monitorozás | Monitorozási lefedettség | Az eszközön/szegmensen hány és milyen érzékelő figyel | eszközönként: (Wazuh agent aktív ? 1:0 + Suricata látja a szegmenst ? 1:0) / 2; alacsony lefedettség → bizonytalansági jelző, nem büntetés | Wazuh agent állapot, Suricata szegmens-lefedettség | Kontextus | Chamkar 2024; Winkler 2025; Virkud 2024 (kritika!) | Alap – egyszerű formában (döntés: 2026-09-21) |
| G1 | Aggregáció | Attribútum-hasonlóság | Két riasztás hasonlósága (IP, port, szignatúra, eszköz) | súlyozott hasonlósági függvény / DBSCAN távolság | Normalizált riasztások | Aggregáló | Valeur 2004; Julisch 2003; Landauer 2022 | Alap – biztosan |
| G2 | Aggregáció | Időbeli közelség | Időablakon belüli összefüggés | Δt küszöb vagy csúszó ablak | Időbélyegek | Aggregáló | Valeur 2004; Landauer 2022 | Alap – biztosan |
| R1 | Összesítő | Kockázati prioritás-score | A meta-riasztás végső prioritása | AHP-súlyozott lineáris kombináció: Σ wᵢ·xᵢ (alternatíva: TOPSIS, fuzzy) | A fenti metrikák | Priorizáló | Anuar 2012 (AHP-RIM); Alsubhi 2008 (fuzzy); Jalalvand 2024 (MCDM) | Alap – a modell magja |
| E1 | Értékelés (K4) | Riasztásszám-csökkenés (ARR/QRR) | Mennyivel kevesebb elem kerül az elemző elé | 1 − (meta-riasztások / nyers riasztások) | Előtte/utána mérés | Értékelés | Ndichu 2026; Landauer 2022 | Alap – biztosan |
| E2 | Értékelés (K5) | Elvesztett valós támadás (FNR) | A csökkentés közben elnyomott valós támadások aránya | elnyomott TP / összes TP (cél < 2%) | Szimulációs ground truth | Értékelés | Ndichu 2026 (FNR budget) | Alap – biztosan |
| E3 | Értékelés (K5) | Rangsor-minőség | A valós incidensek a lista elején vannak-e | AUROC, Average Precision, Precision@k (pl. felső 10%), nDCG@k; baseline-ok: súlyosság szerinti rendezés és RBA (Uetz 2026, CATS) | Ground truth + rangsor | Értékelés | Ndichu 2026; Uetz 2026 | Alap – biztosan |
| E4 | Értékelés (K4) | Becsült elemzői terhelés | Szükséges elemzői idő a sorhoz képest a kapacitáshoz mérve | Σ(elemek × átlagos kezelési idő) / elemzői kapacitás | Előtte/utána + feltételezett kezelési idők | Értékelés | Shah 2019; Tariq 2025 | Ajánlott |
| E5 | Értékelés (K5) | Incidens-rekonstrukció pontossága | A meta-riasztás egy támadási forgatókönyvet fed-e le | klaszter precision/recall, purity a támadási szcenáriókhoz | Szimulációs szcenárió-címkék (6 szcenárió) | Értékelés | Ndichu 2026 (Category III); Landauer 2022 | Ajánlott |

## Adathalmazok

| Adathalmaz | Forrás | Tartalom | Méret | Címkék | Elérhetőség | Illeszkedés | Korlát | Szerep |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIT-ADS | Landauer et al. 2024 | Suricata + Wazuh + AMiner riasztások (JSON) | ~2,6M riasztás, 8 szcenárió, 93 detektor | Támadási fázis címkék időalapon (scan, exploit, exfiltráció) | Nyílt, Zenodo 8263181; kód: github.com/ait-aecid/alert-data-set | Kiváló – ugyanaz a stack; reprodukálható, összehasonlítható | Nincs CMDB → rekonstruálható: 3 zóna, ismert szoftververziók (WordPress 5.8.2, wpDiscuz CVE-2020-24186, Samba 4.5.9, OpenVPN 2.4.4, Horde 5.2.17, OwnCloud 10.5.0), IP-k a „facts” fájlokból | Fő külső benchmark |
| AIT-ADS-A | Karner et al. 2026 | AIT-ADS augmentálva | Zajszint 1–12×, párhuzamos támadások | Hierarchikus csoportcímkék | Nyílt, github.com/ait-aecid/AlertBERT | Jó – robusztussági teszt nagy zajnál | Preprint; csak csoportosítás-címkék | Robusztussági kiegészítés |
| AIT-LDSv2 | Landauer et al. 2023 | Nyers logok + pcap, 8 hálózat | Több napos szimuláció, normál felhasználói viselkedés | Teljes címkézés | Nyílt, Zenodo 5789064 | Jó – visszajátszható saját Suricata/Wazuh szabályokkal | Nagy méret, előfeldolgozás kell | Opcionális: saját riasztás-generálás |
| SOCBED / DEDALE / APT29S2 | Uetz et al. 2026 (COMIDDS) | Sigma, Suricata (és Falco) riasztások | Néhány száztól néhány tízezer riasztásig | Kézzel címkézett igaz/hamis riasztások | Nyílt (CATS artefaktumok, COMIDDS) | Jó – további külső validáció RBA-baseline-nal | Rövid futamidők (SOCBED, APT29S2), eltérő forrásrendszerek | Opcionális: általánosíthatóság |
| Saját homelab | Saját (Docker stack, 6 szcenárió) | Suricata + Wazuh élő riasztások | Tetszőleges | Pontos ground truth az orchestration script időbélyegeiből | Saját | Kiváló – teljes kontextus (CMDB, sérülékenység, lefedettség) szabályozható | Szintetikus háttérforgalom, belső validitás kérdéses | Fő belső kísérlet |
| CPTC-2017/2018 | Nadeem et al. 2021 | Suricata riasztások diákcsapatok pentestjeiből | Csapatonként több ezer riasztás | Nincs benign/támadás szétválasztás | Nyílt | Közepes – csak támadási gráf/szekvencia kísérlethez | Pentest-jellegű, nincs normál forgalom | Nem ajánlott fő adatnak |
| CIC-IDS2017/2018 | Sharafaldin et al. 2018 | Hálózati flow-k/pcap | Nagy | Flow-szintű címkék | Nyílt | Gyenge riasztás-szinten – előbb Suricata-n át kell játszani | Flow-IDS benchmark, nem riasztás-aggregációs | Csak ha a bírálók kérik |
| DARPA 2000 | Lincoln Lab | Pcap | Kicsi | Szcenárió-címkék | Nyílt | Gyenge – elavult, erősen kritizált | 1999–2000-es forgalom | Kerülendő (csak történeti összevetésnél) |

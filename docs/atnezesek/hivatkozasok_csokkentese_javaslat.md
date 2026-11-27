# A hivatkozások csökkentése – javaslat (2026-11-27)

A szerző kérése: legfeljebb 40–45 hivatkozás, ebből legalább 15 lektorált publikáció; a termékeknél
elég a dokumentáció, és minden termék egyszer szerepeljen; a számozás a megjelenés sorrendjében
haladjon; a táblázatokból kikerül a „Példa” oszlop.

**Most:** 80 hivatkozott forrás (52 lektorált, 8 arXiv, 17 webes, 3 jelentés vagy könyv).
**Javaslat:** **45** forrás, ebből **28 lektorált**, 6 arXiv, 2 szabvány vagy útmutató és
9 termékdokumentáció (termékenként egy).

## Megmarad (45)

| Csoport | Források |
| --- | --- |
| Lektorált (28) | alahmadi2022, tariq2025, jalalvand2024, denning1987, axelsson2000, roesch1999snort, gonzalez2021siem, vielberth2020, vermeer2023, valeur2004, landauer2022, julisch2003, vanede2022, anuar2012, porras2002, kruegel2004verification, njogu2012, sommestad2015, wang2024alertpro, hassan2019, bougueroua2021, roy2026agentsoc, arp2022, landauer2023aitlds, landauer2024aitads, shi2024cpe, saaty1990, wooldridge1995 |
| arXiv (6) | uetz2026rba (az összehasonlítási alap), ndichu2026, karner2026alertbert, wei2025cortex, liu2026hesp, wu2023autogen |
| Szabvány, útmutató (2) | scarfone2007nist (NIST SP 800-94), strom2018attack (MITRE ATT&CK) |
| Termékdokumentáció (9) | Suricata, Zeek, Wazuh (szabályszintek), Splunk (kockázatalapú riasztás), Microsoft Sentinel, Elastic Security, LangGraph, Ollama, MCP |

A Snort forrása a saját cikke (roesch1999snort), ez a termék egyetlen hivatkozása.

## Kimarad (35) – és mit érint a szövegben

| Forrás | Hol | Mi történik a szöveggel |
| --- | --- | --- |
| splunkmq2025, microsoftmq2025, googlemq2025 | 2.3 | A Gartner-rangsor mondata kimarad (piaci hír, nem dokumentáció). |
| ciscosplunk2024, paloaltoqradar | 2.3 és a 2.2. táblázat | A felvásárlásokról szóló mondat és a táblázat két megjegyzése kimarad. |
| ossec, wazuhossec | 2.2 | Az OSSEC-ről és a Wazuh eredetéről szóló két mondat forrás nélkül nem maradhat: kimarad, vagy egy mondatba vonva a Wazuh-dokumentációra hivatkozik. |
| paxson1999bro | 2.2 | A Zeek-mondat a dokumentációra hivatkozik. |
| shah2018snort | 2.2 | A Snort–Suricata teljesítmény-összehasonlítás két mondata kimarad. |
| knerler2022mitre, kokulu2019 | 2.4 | A SOC szervezeti formáiról és a nem technikai problémákról szóló 2–3 mondat kimarad, vagy a vielberth2020-ra támaszkodik, ha az is kimondja. |
| chhetri2024 | 2.6, 3. fejezet | A három működési mód mondata kimarad (a tariq2025 hasonló felosztása marad). |
| sadoddin2006, salah2013, mirheidari2013, kotenko2022 | 3.1 | A fogalmi bevezetőben a négy áttekintés helyett a valeur2004 és a landauer2022 marad. |
| wilkens2021, nadeem2021, shittu2015, eckhoff2025 | 3.2 | A többlépcsős korreláció és a gráfalapú kontextus 1–2 mondata rövidül; a „Példa” oszlop egyébként is kikerül. |
| alsubhi2008, alsubhi2011fuzmet, meng2015, chergui2020, liu2022rapid, homayoun2026, guo2026 | 3.3 | A felsorolásokból kikerülnek; a módszercsaládot a megmaradó forrás (anuar2012, njogu2012, sommestad2015, wang2024alertpro, hassan2019) képviseli. |
| yu2005trinetr, taha2010, ismail2025copilot, hmimou2025, abdennebi2026lang, vallabhaneni2026sentinel | 3.4 (és 5.3.5) | Az agentes áttekintés a bougueroua2021, roy2026agentsoc, wei2025cortex, liu2026hesp forrásokra szűkül; a 3.3. táblázat sorai ennek megfelelően csökkennek. |
| chamkar2024 | 4.2.4 | A megfigyelési lefedettség mondata forrás nélkül vagy a vielberth2020-ra támaszkodva. |
| crewaidocs | 5.5 és az 5.3. táblázat | A CrewAI mondata kimarad; a beszélgetésalapú keretrendszereket az AutoGen képviseli. |

**Fontos:** ez a fejezetszövegek tartalmi szűkítése. A kimaradó állításokat nem lehet forrás nélkül
bent hagyni, mert akkor hivatkozás nélküli átvett állítás maradna (plágiumkockázat).

## A számozás sorrendje

A kért megjelenési sorrend azt jelenti, hogy az első hivatkozott forrás az [1], a következő új
forrás a [2], és így tovább; az irodalomjegyzék is ebben a sorrendben áll (biblatex: `sorting=none`).
A kari útmutató 1. melléklete az első szerző szerinti betűrendet *javasolja*, nem írja elő.

---

## Végrehajtva – 2026-11-27 (dolgozat v0.17)

A szerző döntései: a fejezeteket Claude javítja, a 45 forrásos lista marad, **a számozás betűrendes
marad** (az útmutató javaslata szerint), az alap a v0_4. A hivatkozáscsoportokon belül a számok
növekvő sorrendben állnak (`sortcites=true`). Betűrendes számozásnál a szövegben a számok nem
mindig növekvő sorrendben követik egymást (például a [3] után következhet a [41]); ez a
betűrend természetes velejárója.

**Eredmény:** 45 hivatkozott forrás (28 lektorált), a törzsszöveg 40 oldal (korábban 42), a dolgozat
62 PDF-oldal. A `references.bib` a kimaradt bejegyzéseket is megőrzi; az irodalomjegyzékbe csak a
hivatkozottak kerülnek.

### A szövegváltozások (a `git diff` mutatja őket betűre pontosan)

| Fejezet | Változás |
| --- | --- |
| 2.2 Suricata | Kimaradt két mondat: a Snort–Suricata szálkezelés és a teljesítmény-összehasonlítás (shah2018snort). |
| 2.2 Zeek | „Paxson eredetileg … mutatta be [ ], a mai változat azonban” → „…eltérő megközelítést képvisel: elsősorban hálózati forgalomelemző…” |
| 2.2 Gépi eszközök | Kimaradt az OSSEC-mondat; a Wazuh-bekezdés első mondata: „A Wazuh nyílt forráskódú gépi behatolásérzékelő, amely a gépi felismerés mellett a sérülékenységek felismerésére, saját webes felületre és a riasztások központi gyűjtésére is képes, így…” |
| 2.1. táblázat | Kimaradt az OSSEC sora, a Snortnál a „régebbi változatok egyszálúak”, a Wazuhnál az „az OSSEC forkja”. |
| 2.3 SIEM | Kimaradt „A piacot néhány nagy szereplő uralja.” bekezdés (a Gartner-rangsor és a felvásárlások). |
| 2.2. táblázat | Kimaradt az IBM QRadar sora és a Splunknál a „2024 óta a Cisco tulajdona”. |
| 2.4 SOC | Kimaradt a SOC szervezeti formáiról szóló két mondat (knerler2022mitre) és az „Az emberi oldal legalább ilyen fontos…” bekezdés (kokulu2019). |
| 2.6 | „Baruwal Chhetri és szerzőtársai három működési módba rendezik [chhetri2024]” → „Tariq és szerzőtársai három nézőpontba rendezik [tariq2025]” (ugyanez a felosztás az 1.1-ben már Tariqra hivatkozik). |
| 3.1 | Kimaradt a négy korrelációs áttekintésre hivatkozó mondat. |
| 3.2 | „Erre a célra a szakirodalom … javasolt. Közös gyengeségük, hogy” → „Az erre javasolt módszerek közös gyengesége, hogy”; kimaradt az Eckhoff-mondat. |
| 3.1. táblázat | Kikerült a „Példa” oszlop. |
| 3.3 | Kimaradt az Alsubhi-mondat, a „tudásalapú és kontextusalapú szűrők” mondata, a RAPID-mondat és a „legfrissebb irodalomban is megjelennek” mondata. |
| 3.2. táblázat | Kikerült a „Példa” oszlop. |
| 3.4 | Kimaradt a TRINETR- és Taha-mondat, az Ismail-, Hmimou- és Chhetri-mondat, a LanG-mondat („Az AgentSOC hasonló elven” → „Az AgentSOC”) és a SENTINEL-RL-mondat. |
| 3.3. táblázat | Kimaradt a TRINETR, a LanG és a SENTINEL-RL sora. |
| 3.4. táblázat | A szakértői súlyok sorában csak az anuar2012 hivatkozás maradt. |
| 4.2.4 | „A megfigyelési lefedettség a SOC-ok működésének egyik ismert hiányossága [chamkar2024], és a kockázatalapú pontozásra” → „A megfigyelési lefedettség a kockázatalapú pontozásra” |
| 4.2. táblázat | Kikerült a „Példa” oszlop. |
| 5.3.5 | Kimaradt „Ez a felépítés … újabb javaslatokat követi [vallabhaneni2026sentinel].” |
| 5.5 és az 5.3. táblázat | Kimaradt a CrewAI-mondat és a CrewAI sora. |

**Átnézésre javasolt:** a 3.4.2 alfejezet egyetlen rövid bekezdésre zsugorodott; ha akarod, bővítsd
saját mondatokkal, vagy vond össze a 3.4.3-mal.

# Kutatási jegyzet #3 – Agent-alapú architektúra (K3)
2026-09-21 · Feldolgozott források: LanG, CORTEX, AgentSOC, SENTINEL-RL, valamint a klasszikus MAS-irodalom (TRINETR, Taha 2010, Bougueroua 2021)

## 1. Az „agent” fogalmát a dolgozatban definiálni kell
Két irodalmi hagyomány létezik, és a bírálók bármelyikre gondolhatnak:
- **Klasszikus multi-agent rendszerek (MAS) az IDS-ben** (2000–2010): autonóm szoftverágensek végeznek aggregációt, tudásbázis-alapú értékelést és korrelációt.
  - A **TRINETR (Yu et al. 2005)** szinte a dolgozat klasszikus megfelelője: kollaboratív riasztás-aggregáció és a hálózati/host-kontextus alapú értékelés.
  - Taxonómia: Bougueroua et al. 2021.
- **LLM-alapú agentek** (2024–): LanG, CORTEX, AgentSOC, Hmimou 2025.

**Javaslat:** az agentet szerep-specializált, autonóm feldolgozó egységként definiáljuk, amelynek saját bemenete, felelőssége és kimenete van. Az LLM ennek csak egyik lehetséges megvalósítása. Így mindkét hagyomány lefedhető.

## 2. Az irodalom egyértelmű trendje: hibrid felépítés
- **SENTINEL-RL (2026):** a döntés ne az LLM-ben legyen, mert szűk a kontextusablak és hallucinálhat. Az LLM csak narratívát ír, amit egy critic agent ellenőriz.
- **AgentSOC (2026):** az LLM hipotéziseit determinisztikus gráf-validáció szűri (SSE). A kockázati score egyszerű súlyozott képlet: α·Containment − β·Impact.
- **LanG (2026):**
  - a korreláció Louvain-algoritmussal és Bayes-pontozással történik, az LLM csak hipotézist generál;
  - entrópia/konfidencia küszöb véd a hallucináció ellen (a < 0,7 értékek UNKNOWN jelölést kapnak);
  - két kötelező emberi jóváhagyási pont van.
- **CORTEX (2025):**
  - a multi-agent felállás jobb, mint az egy-agentes: az F1 0,66-ról 0,78-ra nőtt, az FPR 24,9%-ról 14,2%-ra csökkent;
  - cserébe kb. 5,7× több tokent használ és kb. 3,4× lassabb;
  - konzervatív szabályt alkalmaz: ha bármelyik ág eszkalál, az egész eset eszkalálódik.

**Következmény a kombinációs módszerre (R1):** a metrika-számítás és a prioritás-score legyen determinisztikus (AHP-súlyozott vagy fuzzy). Az LLM csak magyarázatot és összefoglalót ír a meta-riasztáshoz. Ez tanítás nélkül is védhető, reprodukálható, és illeszkedik a trendhez.

## 3. Javasolt agent-szerepek (a metrika-katalógushoz kötve)

| Agent | Feladat | Metrikák | Típus |
|---|---|---|---|
| Normalizáló | Suricata és Wazuh riasztások közös sémába | – | determinisztikus |
| Aggregáló | Csoportosítás, meta-riasztás | G1, G2, A3, A5 | determinisztikus (DBSCAN / time-delta) |
| Kontextus (CMDB) | Eszköz-kontextus és lefedettség | S1–S4, C1 | determinisztikus |
| Sérülékenységi | Alkalmazhatóság, CVSS | V1, V2, (V3) | determinisztikus |
| Priorizáló | Score számítás | R1 + A1, A2, A4, A6 | determinisztikus (AHP / fuzzy) |
| Magyarázó | Összefoglaló a meta-riasztáshoz | – | LLM (Ollama), critic-kel |
| Orchestrátor | Folyamat-vezérlés, naplózás | – | determinisztikus |

## 4. További értékelési dimenziók (az agent-réteghez)
- Futásidő (latency) és erőforrás-igény agentenként: a CORTEX, a LanG és a SENTINEL-RL is méri.
- Az LLM-magyarázat helyessége: tartalmaz-e a meta-riasztásban nem szereplő IP-t vagy CVE-t (egyszerű hallucináció-ellenőrzés).
- Módszertani buktatók: Arp et al. 2022 (USENIX).

## Nyitott kérdések
- A megvalósítás egyszerű Python-folyamat legyen, vagy agent-keretrendszer (LangGraph, CrewAI, MCP)?
- Kell-e emberi jóváhagyási pont a prototípusba?

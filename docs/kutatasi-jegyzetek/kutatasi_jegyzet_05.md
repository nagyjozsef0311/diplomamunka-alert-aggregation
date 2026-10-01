# Kutatási jegyzet #5 – Milyen keretben fussanak az agentek?

Dátum: 2026-10-01 · Kutatási kérdés: 3. (agent-alapú felépítés) · Döntés: D12

## A kérdés

Három lehetőség volt nyitva:

- külön Python-szolgáltatások (keretrendszer nélkül);
- LangGraph;
- MCP (Model Context Protocol).

## Fő megállapítás

A három lehetőség nem ugyanarra a feladatra való, ezért nem kizárják, hanem kiegészítik egymást.

| | Mi ez | Mire jó nálunk |
| --- | --- | --- |
| Sima Python-modulok | Minden agent egy függvény vagy osztály meghatározott bemenettel és kimenettel | A számolás magja: egységesítés, csoportosítás, környezet, sérülékenység, pontozás |
| LangGraph | Folyamatvezérlő könyvtár: az agentek egy állapotgráf csomópontjai, az élek adják a sorrendet és az elágazást. Van benne ellenőrzési pont (SQLite/PostgreSQL), emberi jóváhagyás és újrajátszás. 1.0: 2025-10-22; 2026 májusában 1.2; MIT-licenc. | A vezérlő agent; a magyarázó agent bekötése (Ollama) |
| MCP | Szabványos csatlakozó, amin át egy nyelvi modell eszközöket és adatokat ér el. Nem vezérlő, csak kiszolgál. A 2026-07-28-i változat állapotmentes magot, formális elavulási szabályokat és erősebb hitelesítést hozott; a Linux Foundation felügyeli. | Csak olvasható hozzáférés a gépnyilvántartáshoz és a sérülékenységi adatokhoz a magyarázó modell számára |

## Mit csinálnak mások?

| Munka | Megvalósítás | Ami nekünk fontos belőle |
| --- | --- | --- |
| CORTEX (Wei és mtsai., 2025, arXiv:2510.00311) | OpenAI Agents SDK + MCP. Minden adatelérés típusos MCP-eszköz, az agentek MCP-munkameneteken át beszélnek, minden MCP-hívást naplóznak. | Pontosabb, mint egyetlen modell (az „intézkedést igényel” osztályon F1 0,66 → 0,78), de kb. 5,7-szer több szöveget dolgoz fel (23 600 token), és kb. 3,4-szer lassabb (152 s riasztásonként). |
| HESP (Liu & Wang, 2026, arXiv:2609.33446) | Kb. 2 900 sor sima Python, csak a standard könyvtárral; helyi modellek Ollamán vagy vLLM-en (Qwen2.5 7B–72B, Llama-3.1 8B/70B) | A kis helyi modellek nem tudják levezényelni a vizsgálatot: rossz lépést választanak, vagy nem állnak meg. Ha a menetet egy modellen kívüli vezérlő tartja, a Qwen2.5-7B ellenőrzött befejezési aránya 0,125-ről 1,000-ra nő. |
| AgentSOC (Roy & Singh, 2026, arXiv:2604.20134) | Sima Python (NetworkX, pandas), keretrendszer nélkül; a nyelvi modell csak hipotézist javasol | A pontozás és az ellenőrzés kiszámítható program; a teljes kör kb. 0,5 s, ennek kb. 95%-át a nyelvi modell viszi el. |

**Tanulság:** a vegyes felépítésünket (D3) a friss irodalom is alátámasztja: a menet és a
pontszám a modellen kívül van, a nyelvi modell csak magyaráz. A keretrendszer ehhez képest másodlagos.
A beszélgetésre épülő keretrendszerekben (CrewAI, AutoGen és társaik) a modell dönti el a
lépéseket, ezért ezeket nem választjuk.

## Döntés (D12): három réteg

1. **Mag – sima Python (1–8. hét):**
   - minden agent egy tesztelhető modul, LangGraph- és MCP-függőség nélkül;
   - az AIT-ADS-mérések tömegesen (pandas) futnak rajta.
2. **Vezérlés – LangGraph (az AIT-mérések után, a laborral együtt):**
   - a modulok csomópontként kerülnek be egy állapotgráfba, és ide kerül a magyarázó agent is;
   - meg kell mutatni, hogy a vezérelt változat ugyanazt a rangsort adja, mint a mag.
3. **Csatlakozó – MCP (opcionális, labor):**
   - a gépnyilvántartás csak olvasható MCP-szolgáltatásként is elérhető lesz;
   - ha kifut az idő, ez a réteg elhagyható.

**Kockázat:** a LangGraphot is meg kell tanulni, és lesz egy átállási lépés.
**Kezelés:** a mag a bemenetét és kimenetét meghatározott formában kapja és adja, így a csomópontok vékony burkolók lesznek.

## A dolgozatban

- **Az „agent” meghatározása:** önálló feladat, saját bemenet és kimenet, egy vezérlő által összehangolva. A nyelvi modell csak az egyik agent egyik eszköze.
- **Ábra:** a LangGraph-gráf képe szolgálhat a felépítés illusztrációjaként.
- **Hivatkozások:** `wei2025cortex`, `liu2026hesp`, `roy2026agentsoc`, `langgraph2025`, `mcp2026spec`.

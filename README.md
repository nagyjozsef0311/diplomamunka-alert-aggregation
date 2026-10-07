# Agent-alapú, metrika-vezérelt IDS riasztásaggregáció SOC környezetben

Diplomamunka – Óbudai Egyetem, Neumann János Informatikai Kar, Kiberbiztonsági mérnöki MSc
Szerző: Nagy József · Intézményi konzulens: Vörösné Dr. Bánáti-Baumann Anna · Beadás: 2027. május 15.

*Agent-Based Metric-Driven IDS Alert Aggregation in SOC Environments – master's thesis repository.*

## Miről szól

A biztonsági műveleti központok (SOC) elemzőit túl sok riasztás terheli. A dolgozat azt vizsgálja,
hogy a riasztások csoportosítása és rangsorolása mennyit javul, ha a kockázatalapú riasztás-pontozás
mellé a környezetről szóló információ is bekerül:

- mennyire fontos az érintett gép,
- van-e rajta olyan sérülékenység, amelyet a támadás kihasználhat,
- mennyire figyeljük a gépet.

A feldolgozást egy-egy feladatra szakosodott agentek végzik. A pontszámot kiszámítható,
megismételhető programrészek adják, a nyelvi modell csak magyarázatot ír.

## A tároló felépítése

| Mappa | Tartalom |
| --- | --- |
| `src/alertagg/` | Az agentek Python-csomagja (egységesítő, csoportosító, környezet, sérülékenységi, rangsoroló, magyarázó) |
| `cmdb/` | A gépnyilvántartás sémája és forgatókönyvenkénti adatai |
| `experiments/` | A mérések futtatói és beállításai – egy parancs = egy mérés |
| `scripts/` | Letöltő és segédszkriptek (AIT-ADS, CATS, sérülékenység-lekérdezés) |
| `data/` | Letöltött adatok – **nem kerül a tárolóba** |
| `results/` | Mérési eredmények (CSV) és ábrák |
| `lab/` | A vegyes (VMware + Docker) labor leírása és fájljai |
| `docs/` | Kutatási jegyzetek, döntésnapló, munkaterv |
| `thesis/` | Forrásjegyzék (`references.bib`, `forrasok.xlsx`) |
| `tests/` | Automatikus tesztek |

## Gyors kezdés

Python 3.11 vagy újabb kell.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python scripts/download_ait_ads.py   # AIT-ADS a data/ait_ads/ mappába (kb. 100 MB)
python scripts/download_cats.py      # CATS kód és átalakított adatok a data/external/cats/ mappába
```

## Felhasznált adatok és külső kód

| Név | Forrás | Licenc | Megjegyzés |
| --- | --- | --- | --- |
| AIT Alert Data Set (AIT-ADS) 1. verzió | [Zenodo 8263181](https://zenodo.org/records/8263181) | CC BY 4.0 | Landauer, Skopik, Wurzenberger (2024), DOI: 10.1145/3675741.3675748 |
| CATS (Cybersecurity Alert Triage Exploration and Evaluation System) | [github.com/962012d09b/cats](https://github.com/962012d09b/cats) | nincs megadva | Uetz et al. (2026), arXiv:2609.02465 – csak letöltjük, nem terjesztjük |

Az adatok és a külső kód nem kerülnek ebbe a tárolóba; a letöltő szkriptek rögzített verziót és
ellenőrzőösszeget használnak, hogy a mérések megismételhetők legyenek.

## Dokumentáció

- `docs/dontesek.md` – döntésnapló: mit és miért választottunk
- `docs/munkaterv.md` – az érvényes ütemterv (D13) és az AIT-ADS munkaterv összefoglalója
- `docs/munkaterv-reszletes.md` – a teljes AIT-ADS munkaterv
- `docs/kutatasi-eredmenyek.md` – döntések kutatási kérdésenként, fogalomtárral
- `docs/metrika-katalogus.md` – mérőszámok és adathalmazok
- `docs/diplomamunka-2.md` – a Diplomamunka II. követelményei, leadandói és a beszámoló fejezetvázlata
- `docs/atadas.md` – feladatlista
- `docs/latex-utmutato.md` – LaTeX-útmutató a dolgozat sablonjához (fejezetek, hivatkozás, ábrák, Overleaf)
- `docs/irasi-csomagok/` – fejezetenkénti javaslatok a szerzőnek (kész mondatok nélkül)
- `CLAUDE.md` – a teljes háttér a Claude Code számára
- `docs/kutatasi-jegyzetek/` – a szakirodalom-kutatás jegyzetei (2026. szeptember)

## Állapot

Folyamatban. A tároló a beadásig privát.

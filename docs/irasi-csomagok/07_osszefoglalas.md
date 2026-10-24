# Írási csomag – Absztrakt, Összefoglalás, Summary

2026-10-24 · D20 szerint: a **kódblokkok** tartalma átvehető (forrásoktól független, saját
megfogalmazás), a blokkokon kívüli „Megjegyzés” sorok neked szólnak.

- **Útmutató, 3. melléklet:** absztrakt magyarul és angolul (a tartalomjegyzék előtt); 11. tartalmi
  összefoglaló és következtetések magyarul, **1500–2500 karakter** (kötelező); 12. ugyanez angolul (kötelező).
- **D24:** a DM II. az 1–6. fejezettel zárul, ezért az összefoglaló utolsó bekezdése a következő félév
  feladatát jelzi. A végleges dolgozatban ezt a bekezdést az eredményekre kell cserélni.
- Hivatkozás és szám szándékosan nincs bennük: az összefoglaló a dolgozatot foglalja össze, a forrásokat
  a fejezetek adják.

| Szöveg | Hová | Hossz (szóközökkel) |
| --- | --- | --- |
| Absztrakt | `main.tex`, az `\section*{ABSZTRAKT}` alatti megjegyzés helyére | 644 karakter |
| Abstract | `main.tex`, az `\section*{ABSTRACT}` alatt | 605 karakter |
| Összefoglalás | `chapters/Osszefoglalas.tex` | **1832 karakter** (az előírás 1500–2500) |
| Summary | `chapters/Summary.tex` | 1782 karakter |

Megjegyzés: ha átírod, a hosszt Overleafben a Menu → Word Count mutatja (szavakban); karakterre a
szöveget egy szövegszerkesztőbe másolva ellenőrizheted. Ha a végleges dolgozatban eredmények is
kerülnek bele, az összefoglaló a 2500 karakteres felső határ felé fog nőni – ezért most van benne tartalék.

---

## Absztrakt

```latex
A dolgozat a biztonsági műveleti központokat terhelő riasztási fáradtság csökkentésével foglalkozik.
Olyan agent-alapú rendszert tervezek, amely a Suricata hálózati és a Wazuh gépi riasztásait csoportosítja és rangsorolja.
A rangsor alapja a nyilvánosan mért legerősebb, tanítás nélküli módszer, a kockázatalapú riasztás-pontozás, amelyet a gép fontosságával, a támadás alkalmazhatóságával és a gép megfigyeltségével egészítek ki.
A mérőszámokat páros összehasonlítással súlyozott összeg vonja össze, a nyelvi modell csak ellenőrzött magyarázatot ír.
A hatást lépésenkénti bővítéssel, nyilvános adathalmazon és laboratóriumi környezetben mérem.
```

## Abstract

```latex
This thesis addresses alert fatigue in security operations centres.
It designs an agent-based system that groups and ranks network alerts from Suricata and host alerts from Wazuh.
The ranking builds on risk-based alert scoring, the strongest publicly evaluated method that needs no training data, and extends it with host importance, attack applicability and monitoring coverage.
The metrics are combined in a weighted sum derived by pairwise comparison, and a language model only writes verified explanations.
The effect is measured step by step on a public alert dataset and in a laboratory environment.
```

---

## Összefoglalás (`chapters/Osszefoglalas.tex`)

```latex
A biztonsági műveleti központok elemzőit a behatolásérzékelő rendszerek nagy mennyiségű riasztással terhelik, amelyeknek csak kis része jelez valódi támadást.
A túlterhelés riasztási fáradtsághoz vezet, amelynek következtében a valódi támadások is rejtve maradhatnak.
A dolgozat célja egy olyan rendszer kidolgozása, amely a hálózati és a gépi behatolásérzékelő riasztásait mérőszámok és a környezetre vonatkozó információ alapján csoportosítja és rangsorolja, együttműködő agentek segítségével.

A szakirodalom áttekintése azt mutatta, hogy a riasztások csoportosítására és rangsorolására javasolt módszerek mindegyike a probléma egy részét oldja meg.
A legerősebb, tanítóadatot nem igénylő módszer, a kockázatalapú riasztás-pontozás kizárólag a riasztások folyamából dolgozik, és nem veszi figyelembe az érintett gép fontosságát, sérülékenységeit és megfigyeltségét.
A környezetet használó módszerek többnyire szűrnek, így a hiányos nyilvántartás miatt valódi támadást is eltávolíthatnak, a nyelvi modellekre épülő megoldások pedig lassúak és nem megismételhetők.

A választott megoldás a kockázatalapú pontozást három környezeti mérőszámmal egészíti ki, amelyek csak a riasztások sorrendjét módosítják, riasztást nem távolítanak el.
A mérőszámokat súlyozott összeggel vonom össze, a súlyokat páros összehasonlítással, a mérés előtt határozom meg.
A tervezett rendszer hét agentből áll; a pontszámot és a sorrendet kiszámítható programrészek adják, a helyben futó nyelvi modell csak ellenőrzött magyarázatot ír.
A hatást lépésenként bővített modellváltozatokkal, egy nyilvános riasztás-adathalmaz nyolc forgatókönyvén és egy saját laboratóriumi környezetben mérem, a torzítás ellen előzetes rögzítéssel és ellenpróbával védekezve.

A következő félév feladata a rendszer megvalósítása, a mérések elvégzése és az eredmények értékelése.
```

Megjegyzés: a negyedik bekezdés („A következő félév feladata…”) csak a DM II.-be kell. A második
bekezdés a 3. fejezet, a harmadik a 4–6. fejezet lényege – ha a fejezetekben valamit módosítasz
(például a megfigyeltség mégsem kerül a pontszámba), ezt itt is igazítsd.

---

## Summary (`chapters/Summary.tex`)

```latex
Analysts in security operations centres receive large numbers of intrusion detection alerts, of which only a small share indicates a real attack.
This overload leads to alert fatigue, in which genuine attacks may go unnoticed.
The aim of this thesis is to design a system that groups and ranks network- and host-based intrusion detection alerts using metrics and information about the monitored environment, with the help of cooperating agents.

The literature review showed that each existing approach to alert grouping and prioritisation addresses only part of the problem.
The strongest method that requires no training data, risk-based alert scoring, relies solely on the alert stream and ignores the importance, vulnerabilities and monitoring coverage of the affected host.
Context-aware methods mostly filter alerts and may therefore discard real attacks when the asset inventory is incomplete, while solutions built on large language models are slow and not reproducible.

The proposed solution extends risk-based scoring with three context metrics that only change the order of alerts and never remove them.
The metrics are combined in a weighted sum whose weights are set by pairwise comparison before any measurement takes place.
The planned system consists of seven agents: the score and the ranking are produced by deterministic components, while a locally hosted language model only writes verified explanations.
The effect will be measured with incrementally extended model variants on eight scenarios of a public alert dataset and in a dedicated laboratory environment, guarding against bias through pre-registration of settings and a control experiment.

The next semester is devoted to implementing the system, carrying out the measurements and evaluating the results.
```

Megjegyzés: a Summary a magyar összefoglaló tartalmi megfelelője, nem szó szerinti fordítása. Brit
helyesírással készült (prioritisation, centres); ha amerikait szeretnél, szólj.

---

## Átvételkor figyelj

- Az absztrakt és az összefoglaló nem ugyanaz: az absztrakt rövid kivonat a dolgozat elején, az
  összefoglaló a végén a tartalmat és a következtetéseket foglalja össze.
- Rövidítést (`\ac{}`) itt nem használtam, mert az absztrakt a rövidítésjegyzék előtt áll, és
  önmagában is érthetőnek kell lennie.

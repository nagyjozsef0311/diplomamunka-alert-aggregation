"""Agent-alapú, metrika-vezérelt IDS riasztásaggregáció – diplomamunka csomag.

Tervezett agentek (lásd docs/dontesek.md):
- egységesítő:     Suricata- és Wazuh-riasztások közös formára hozása
- csoportosító:    összetartozó riasztások csoportokba rendezése
- környezet:       a gép fontossága, zónája, megfigyeltsége a gépnyilvántartásból
- sérülékenységi:  működhet-e a támadás az adott gépen
- rangsoroló:      páros összehasonlítással (AHP) súlyozott pontszám
- magyarázó:       rövid szöveges összefoglaló nyelvi modellel, ellenőrzéssel
"""

__version__ = "0.1.0"

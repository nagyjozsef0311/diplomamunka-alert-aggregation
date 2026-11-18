# Az 1–5. lépés a 8 AIT-ADS forgatókönyvön – forgatókönyvenkénti eredmények

Készült: 2026-11-18 13:45 UTC · kód: `47cfb7a` · terv: `config/elozetes_rogzites/ait_mind8_meresi_terv.yaml` · súlyok (AHP, újranormálva): 4. lépés r = 0.636, g = 0.364; 5. lépés r = 0.535, g = 0.306, a = 0.160 · időköz: 60 perc · címke: időszak-alapú

A teljes táblázat (minden mérőszám, a russellmitchell CATS-címkés változata, az ellenpróbák, a ±20% és a hiányos nyilvántartás sorai): `results/10_ait_mind8_lepes1_5_meres.csv`. A statisztikai összevetés: `results/11_ait_mind8_statisztika.md`.

## Átlagos pontosság (AP) és a 98%-hoz átnézendő listarész

|                                 |   ('ap', 'csoport', 'lepes2') |   ('ap', 'csoport', 'lepes3') |   ('ap', 'csoport', 'lepes4') |   ('ap', 'csoport', 'lepes5') |   ('ap', 'riasztas', 'lepes1') |   ('ap', 'riasztas', 'lepes3') |   ('ap', 'riasztas', 'lepes4') |   ('ap', 'riasztas', 'lepes5') |   ('workload_98', 'csoport', 'lepes2') |   ('workload_98', 'csoport', 'lepes3') |   ('workload_98', 'csoport', 'lepes4') |   ('workload_98', 'csoport', 'lepes5') |   ('workload_98', 'riasztas', 'lepes1') |   ('workload_98', 'riasztas', 'lepes3') |   ('workload_98', 'riasztas', 'lepes4') |   ('workload_98', 'riasztas', 'lepes5') |
|:--------------------------------|------------------------------:|------------------------------:|------------------------------:|------------------------------:|-------------------------------:|-------------------------------:|-------------------------------:|-------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|----------------------------------------:|----------------------------------------:|----------------------------------------:|
| ('suricata', 'russellmitchell') |                         0.202 |                         0.216 |                         0.255 |                         0.298 |                          0.147 |                          0.194 |                          0.225 |                          0.221 |                                  0.985 |                                  0.834 |                                  0.968 |                                  0.987 |                                       1 |                                   0.808 |                                   0.914 |                                   0.914 |
| ('wazuh', 'russellmitchell')    |                         0.985 |                         0.981 |                         0.544 |                         0.544 |                          0.951 |                          0.9   |                          0.592 |                          0.594 |                                  0.425 |                                  0.716 |                                  0.692 |                                  0.692 |                                       1 |                                   0.757 |                                   0.672 |                                   0.668 |

## Riasztások és támadások forgatókönyvenként

| erzekelo   | forgatokonyv    |   riasztas |   tamadas |   azonositott_gep_arany |   a_semleges_arany |
|:-----------|:----------------|-----------:|----------:|------------------------:|-------------------:|
| wazuh      | russellmitchell |      23116 |      8111 |                   1.000 |              0.034 |
| suricata   | russellmitchell |       9186 |       213 |                   1.000 |              0.036 |

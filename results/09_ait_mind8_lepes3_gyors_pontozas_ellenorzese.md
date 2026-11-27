# A gyors kockázati pontszám ellenőrzése a CATS eredeti kódjával

Készült: 2026-11-18 14:43 UTC · kód: `2d73caa` · CATS: 628cf48a

A táblázat riasztásonként a legnagyobb abszolút eltérést adja a két számítás között (részpontszámonként; a pontszámok 0 és 1 közé esnek). A CATS_mp üres, ha az eredeti kód eredménye a gyorsítótárból jött.

| adat                             |   riasztas |   CATS_mp |   gyors_mp |   max_elteres_level |   max_elteres_accumulation |   max_elteres_variety |   max_elteres_rarity |   max_elteres_aperiodicity |
|:---------------------------------|-----------:|----------:|-----------:|--------------------:|---------------------------:|----------------------:|---------------------:|---------------------------:|
| CATS-változat ait_wazuh          |      23116 |     nan   |       4.23 |                   0 |                   1.11e-16 |              4.3e-14  |             1.11e-16 |                   1.11e-16 |
| CATS-változat ait_suricata       |       9186 |     nan   |       1.81 |                   0 |                   1.11e-16 |              1.16e-11 |             2.22e-16 |                   1.11e-16 |
| eredeti russellmitchell wazuh    |      23116 |     286   |       4.85 |                   0 |                   1.11e-16 |              4.3e-14  |             1.11e-16 |                   1.11e-16 |
| eredeti russellmitchell suricata |       9186 |      83.1 |       2.18 |                   0 |                   1.11e-16 |              1.16e-11 |             2.22e-16 |                   1.11e-16 |
| eredeti santos wazuh             |      38289 |     662   |      12.8  |                   0 |                   6.66e-16 |              1.67e-15 |             2.22e-16 |                   1.53e-16 |
| eredeti santos suricata          |      44112 |     858   |     117    |                   0 |                   2.22e-16 |              3.23e-11 |             2.22e-16 |                   2.22e-16 |
| eredeti shaw wazuh               |      35139 |     485   |      10.4  |                   0 |                   1.11e-16 |              4.35e-14 |             2.22e-16 |                   1.11e-16 |
| eredeti shaw suricata            |      16692 |     145   |       1.19 |                   0 |                   1.11e-16 |              1.63e-11 |             2.22e-16 |                   1.11e-16 |
| eredeti wardbeck wazuh           |      39184 |     651   |      13.1  |                   0 |                   2.22e-16 |              1.02e-14 |             2.22e-16 |                   3.33e-16 |
| eredeti wardbeck suricata        |      24510 |     362   |       3.11 |                   0 |                   2.22e-16 |              5.48e-11 |             2.22e-16 |                   1.11e-16 |

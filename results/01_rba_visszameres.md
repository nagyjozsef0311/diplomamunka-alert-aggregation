# 1. mérés – a kockázatalapú pontozás visszamérése (AIT-ADS, russellmitchell)

Készült: 2026-11-17 16:08 UTC · kód: `6139a58` · CATS: `628cf48` · adat: CATS-változat (`ait_wazuh.jsonl`, `ait_suricata.jsonl`)

Oszlopok: rangsor-pontosság (AUROC), átlagos pontosság (AP), a valódi riasztások aránya és várható száma a lista első 10%-ában, a 98%-os találathoz átnézendő listarész, a cikkben közölt AUROC.

| dataset      | variant       |   n_true |   auroc |    ap |   recall_top10 |   true_in_top10 |   workload_98 |   paper_auroc |
|:-------------|:--------------|---------:|--------:|------:|---------------:|----------------:|--------------:|--------------:|
| ait_wazuh    | level         |     7661 |   0.993 | 0.976 |          0.294 |          2253.9 |         0.339 |          0.99 |
| ait_wazuh    | accumulation  |     7661 |   0.999 | 0.999 |          0.302 |          2312   |         0.33  |          1    |
| ait_wazuh    | variety       |     7661 |   1     | 0.999 |          0.302 |          2312   |         0.325 |          1    |
| ait_wazuh    | rarity        |     7661 |   0.071 | 0.21  |          0.076 |           582   |         1     |          0.07 |
| ait_wazuh    | aperiodicity  |     7661 |   0.005 | 0.309 |          0.004 |            33   |         1     |          0.01 |
| ait_wazuh    | pipeline_mean |     7661 |   0.987 | 0.921 |          0.275 |          2109   |         0.334 |               |
| ait_wazuh    | pipeline_loo  |     7661 |   0.971 | 0.858 |          0.242 |          1851   |         0.346 |          0.98 |
| ait_suricata | level         |       44 |   0.806 | 0.615 |          0.651 |            28.6 |         1     |          0.81 |
| ait_suricata | accumulation  |       44 |   0.656 | 0.007 |          0     |             0   |         1     |          0.66 |
| ait_suricata | variety       |       44 |   0.956 | 0.301 |          0.977 |            43   |         0.976 |          0.96 |
| ait_suricata | rarity        |       44 |   0.991 | 0.404 |          1     |            44   |         0.063 |          0.99 |
| ait_suricata | aperiodicity  |       44 |   0.954 | 0.076 |          0.909 |            40   |         0.255 |          0.95 |
| ait_suricata | pipeline_mean |       44 |   0.991 | 0.808 |          0.977 |            43   |         0.29  |               |
| ait_suricata | pipeline_loo  |       44 |   0.987 | 0.8   |          0.977 |            43   |         0.443 |          0.99 |

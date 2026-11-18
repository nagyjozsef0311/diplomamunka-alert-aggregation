# 5. lépés – + a támadás alkalmazhatósága (AIT-ADS, russellmitchell)

Készült: 2026-11-18 12:48 UTC · kód: `42036e1` · dolgozat: 4.2.3, 4.3, 6.2. táblázat, 6.3

Súlyok (AHP, újranormálva): r = 0.535, g = 0.306, a = 0.160 · csoportok időköze: {'ait_suricata': 60, 'ait_wazuh': 60} perc · ellenpróba: a szolgáltatáskészletek 100 véletlen keverése (kezdőértékek 0–99)

## Az alkalmazhatóság eloszlása (riasztásszám, címkék nélkül)

| adathalmaz   |   a=0.25 |   a=0.5 |   a=0.75 |   a=1.0 |
|:-------------|---------:|--------:|---------:|--------:|
| ait_wazuh    |        3 |     776 |    22337 |       0 |
| ait_suricata |     4846 |     328 |     4012 |       0 |

## Eredmények

workload_98: a riasztáslista, csoport_terheles_98: a csoportlista hányad részét kell átnézni a valódi riasztások 98%-áig (kisebb = jobb). Az „ellenproba_aranya” sor: a keverések hány százaléka érte el vagy múlta felül a valódi eredményt.

| adathalmaz   | valtozat                                |   auroc |    ap |   recall_top10 |   true_in_top10 |   workload_98 |   csoport_auroc |   csoport_ap |   csoport_terheles_98 |
|:-------------|:----------------------------------------|--------:|------:|---------------:|----------------:|--------------:|----------------:|-------------:|----------------------:|
| ait_wazuh    | lepes3_kockazati                        |   0.987 | 0.921 |          0.275 |        2109.000 |         0.334 |           0.998 |        0.998 |                 0.034 |
| ait_wazuh    | lepes4_+gep                             |   0.861 | 0.586 |          0.074 |         569.000 |         0.424 |           0.580 |        0.541 |                 0.138 |
| ait_wazuh    | lepes5_+alkalmazhatosag                 |   0.862 | 0.588 |          0.074 |         569.000 |         0.423 |           0.580 |        0.541 |                 0.138 |
| ait_wazuh    | lepes5_erzekenyseg_a-20%                |   0.862 | 0.588 |          0.074 |         569.000 |         0.423 |           0.580 |        0.541 |                 0.138 |
| ait_wazuh    | lepes5_erzekenyseg_a+20%                |   0.863 | 0.589 |          0.074 |         569.000 |         0.423 |           0.580 |        0.541 |                 0.138 |
| ait_wazuh    | ellenproba_atlag_100                    |   0.820 | 0.611 |          0.112 |         855.040 |         0.450 |           0.580 |        0.541 |                 0.138 |
| ait_wazuh    | ellenproba_aranya_ami_jobb_vagy_egyenlo |   0.310 | 0.310 |        nan     |         nan     |         0.370 |         nan     |      nan     |                 1.000 |
| ait_suricata | lepes3_kockazati                        |   0.991 | 0.808 |          0.977 |          43.000 |         0.290 |           0.983 |        0.842 |                 0.114 |
| ait_suricata | lepes4_+gep                             |   0.991 | 0.863 |          0.955 |          42.000 |         0.143 |           0.982 |        0.751 |                 0.101 |
| ait_suricata | lepes5_+alkalmazhatosag                 |   0.944 | 0.838 |          0.864 |          38.000 |         0.459 |           0.929 |        0.864 |                 0.481 |
| ait_suricata | lepes5_erzekenyseg_a-20%                |   0.952 | 0.820 |          0.864 |          38.000 |         0.459 |           0.933 |        0.751 |                 0.418 |
| ait_suricata | lepes5_erzekenyseg_a+20%                |   0.939 | 0.817 |          0.864 |          38.000 |         0.459 |           0.929 |        0.864 |                 0.519 |
| ait_suricata | ellenproba_atlag_100                    |   0.943 | 0.683 |          0.837 |          36.810 |         0.471 |           0.919 |        0.536 |                 0.287 |
| ait_suricata | ellenproba_aranya_ami_jobb_vagy_egyenlo |   0.530 | 0.030 |        nan     |         nan     |         0.440 |         nan     |      nan     |                 0.970 |

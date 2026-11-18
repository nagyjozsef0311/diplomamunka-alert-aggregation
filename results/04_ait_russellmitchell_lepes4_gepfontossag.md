# 4. lépés – kockázati pontszám + gép fontossága (AIT-ADS, russellmitchell)

Készült: 2026-11-18 12:20 UTC · kód: `650abd0` · dolgozat: 4.3, 6.2. táblázat, 6.3

Súlyok (AHP, újranormálva r és g között): r = 0.636, g = 0.364 · gépfontosság: `config/elozetes_rogzites/ait_russellmitchell_gepfontossag_v2.yaml` · ellenpróba: 100 véletlen keverés (rögzített kezdőértékek 0–99)

Oszlopok: rangsor-pontosság (AUROC), átlagos pontosság (AP), a valódi riasztások aránya és várható száma a lista első 10%-ában, a 98%-os találathoz átnézendő listarész (kisebb = jobb). Az „ellenproba_aranya” sor azt adja meg, a keverések hány százaléka érte el vagy múlta felül a valódi gépfontossággal mért eredményt.

| adathalmaz   | valtozat                                |   auroc |    ap |   recall_top10 |   true_in_top10 |   workload_98 |
|:-------------|:----------------------------------------|--------:|------:|---------------:|----------------:|--------------:|
| ait_wazuh    | lepes1_sulyossag                        |   0.993 | 0.976 |          0.294 |          2253.9 |         0.339 |
| ait_wazuh    | lepes3_kockazati                        |   0.987 | 0.921 |          0.275 |          2109   |         0.334 |
| ait_wazuh    | lepes4_kockazati+gep                    |   0.861 | 0.586 |          0.074 |           569   |         0.424 |
| ait_wazuh    | lepes4_erzekenyseg_g-20%                |   0.936 | 0.732 |          0.172 |          1315   |         0.368 |
| ait_wazuh    | lepes4_erzekenyseg_g+20%                |   0.731 | 0.44  |          0.074 |           565   |         0.518 |
| ait_wazuh    | ellenproba_atlag_100                    |   0.726 | 0.655 |          0.154 |          1176.1 |         0.51  |
| ait_wazuh    | ellenproba_aranya_ami_jobb_vagy_egyenlo |   0.57  | 0.57  |                |                 |         0.57  |
| ait_suricata | lepes1_sulyossag                        |   0.806 | 0.615 |          0.651 |            28.6 |         1     |
| ait_suricata | lepes3_kockazati                        |   0.991 | 0.808 |          0.977 |            43   |         0.29  |
| ait_suricata | lepes4_kockazati+gep                    |   0.991 | 0.863 |          0.955 |            42   |         0.143 |
| ait_suricata | lepes4_erzekenyseg_g-20%                |   0.996 | 0.886 |          0.977 |            43   |         0.107 |
| ait_suricata | lepes4_erzekenyseg_g+20%                |   0.985 | 0.856 |          0.955 |            42   |         0.272 |
| ait_suricata | ellenproba_atlag_100                    |   0.796 | 0.469 |          0.689 |            30.3 |         0.728 |
| ait_suricata | ellenproba_aranya_ami_jobb_vagy_egyenlo |   0     | 0.01  |                |                 |         0     |

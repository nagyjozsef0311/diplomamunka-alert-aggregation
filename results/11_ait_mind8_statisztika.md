# A 8 forgatókönyves mérés statisztikai kiértékelése (AIT-ADS, 1–5. lépés)

Készült: 2026-11-18 14:07 UTC · kód: `0e4a614` · forgatókönyvek: 8 · terv: `config/elozetes_rogzites/ait_mind8_meresi_terv.yaml` (D29) · címke: időszak-alapú (D28) · bemenet: `results/10_ait_mind8_lepes1_5_meres.csv`

## 1. Átlag ± szórás a forgatókönyvek között

auroc: rangsor-pontosság; ap: átlagos pontosság; recall_top10: a valódi riasztások aránya a lista első 10%-ában; workload_98 (csoportszinten csoport_terheles_98): a lista hányad részét kell átnézni a valódi riasztások 98%-áig (kisebb = jobb).

### suricata – csoportszint

|                      | auroc         | ap            | recall_top10   | workload_98   | csoport_terheles_98   |
|:---------------------|:--------------|:--------------|:---------------|:--------------|:----------------------|
| 2. csoportosítás     | 0.603 ± 0.155 | 0.064 ± 0.070 | 0.217 ± 0.240  | 0.864 ± 0.211 | 0.534 ± 0.323         |
| 3. kockázati         | 0.560 ± 0.158 | 0.055 ± 0.068 | 0.084 ± 0.073  | 0.810 ± 0.148 | 0.375 ± 0.087         |
| 4. + gép fontossága  | 0.629 ± 0.231 | 0.101 ± 0.106 | 0.287 ± 0.188  | 0.844 ± 0.173 | 0.462 ± 0.282         |
| 5. + alkalmazhatóság | 0.586 ± 0.229 | 0.093 ± 0.097 | 0.308 ± 0.208  | 0.842 ± 0.206 | 0.558 ± 0.257         |

### suricata – riasztásszint

|                      | auroc         | ap            | recall_top10   | workload_98   |
|:---------------------|:--------------|:--------------|:---------------|:--------------|
| 1. súlyosság         | 0.471 ± 0.130 | 0.059 ± 0.043 | 0.125 ± 0.064  | 1.000 ± 0.000 |
| 3. kockázati         | 0.660 ± 0.073 | 0.072 ± 0.058 | 0.179 ± 0.097  | 0.841 ± 0.119 |
| 4. + gép fontossága  | 0.650 ± 0.150 | 0.099 ± 0.067 | 0.221 ± 0.113  | 0.811 ± 0.177 |
| 5. + alkalmazhatóság | 0.640 ± 0.156 | 0.106 ± 0.067 | 0.219 ± 0.106  | 0.814 ± 0.174 |

### wazuh – csoportszint

|                      | auroc         | ap            | recall_top10   | workload_98   | csoport_terheles_98   |
|:---------------------|:--------------|:--------------|:---------------|:--------------|:----------------------|
| 2. csoportosítás     | 0.984 ± 0.017 | 0.976 ± 0.029 | 0.311 ± 0.247  | 0.768 ± 0.192 | 0.064 ± 0.054         |
| 3. kockázati         | 0.930 ± 0.110 | 0.856 ± 0.243 | 0.181 ± 0.223  | 0.833 ± 0.110 | 0.071 ± 0.059         |
| 4. + gép fontossága  | 0.579 ± 0.085 | 0.653 ± 0.344 | 0.048 ± 0.028  | 0.839 ± 0.148 | 0.271 ± 0.362         |
| 5. + alkalmazhatóság | 0.579 ± 0.085 | 0.653 ± 0.344 | 0.048 ± 0.028  | 0.839 ± 0.148 | 0.271 ± 0.362         |

### wazuh – riasztásszint

|                      | auroc         | ap            | recall_top10   | workload_98   |
|:---------------------|:--------------|:--------------|:---------------|:--------------|
| 1. súlyosság         | 0.975 ± 0.022 | 0.949 ± 0.060 | 0.298 ± 0.228  | 0.953 ± 0.055 |
| 3. kockázati         | 0.970 ± 0.027 | 0.907 ± 0.126 | 0.275 ± 0.209  | 0.844 ± 0.063 |
| 4. + gép fontossága  | 0.889 ± 0.075 | 0.706 ± 0.309 | 0.092 ± 0.015  | 0.823 ± 0.111 |
| 5. + alkalmazhatóság | 0.891 ± 0.074 | 0.707 ± 0.308 | 0.092 ± 0.015  | 0.821 ± 0.115 |

## 2. Páros, egyoldali Wilcoxon-próba (H1: az újabb lépés jobb)

javult/romlott: a forgatókönyvek száma; a különbség a „jobb” irányba előjelezve (terhelésnél a csökkenés pozitív); rang_biszerialis: párosított rang-biszeriális korreláció (+1: minden forgatókönyvön javult); p_holm: Holm-korrekció érzékelőnként és mérőszámonként a négy riasztásszintű összevetésre. 8 párnál a legkisebb elérhető p-érték 0,0039.

| erzekelo   | meroszam                           | osszevetes      |   javult |   romlott |   kulonbseg_median |   kulonbseg_atlag |   rang_biszerialis |      p |   p_holm |
|:-----------|:-----------------------------------|:----------------|---------:|----------:|-------------------:|------------------:|-------------------:|-------:|---------:|
| suricata   | auroc                              | lepes3 > lepes1 |        6 |         2 |             0.1687 |            0.1884 |             0.8333 | 0.0195 |   0.0781 |
| suricata   | auroc                              | lepes4 > lepes3 |        5 |         3 |             0.0219 |           -0.0102 |             0.1111 | 0.4219 |   1.0000 |
| suricata   | auroc                              | lepes5 > lepes4 |        0 |         8 |            -0.0076 |           -0.0094 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | auroc                              | lepes5 > lepes3 |        5 |         3 |             0.0192 |           -0.0196 |            -0.0556 | 0.5781 |   1.0000 |
| suricata   | ap                                 | lepes3 > lepes1 |        5 |         3 |             0.0136 |            0.0134 |             0.4444 | 0.1562 |   0.3125 |
| suricata   | ap                                 | lepes4 > lepes3 |        7 |         1 |             0.0299 |            0.0270 |             0.9444 | 0.0078 |   0.0312 |
| suricata   | ap                                 | lepes5 > lepes4 |        4 |         4 |             0.0033 |            0.0064 |             0.4444 | 0.1562 |   0.3125 |
| suricata   | ap                                 | lepes5 > lepes3 |        7 |         1 |             0.0340 |            0.0335 |             0.9444 | 0.0078 |   0.0312 |
| suricata   | recall_top10                       | lepes3 > lepes1 |        6 |         2 |             0.0665 |            0.0546 |             0.5000 | 0.1250 |   0.2500 |
| suricata   | recall_top10                       | lepes4 > lepes3 |        6 |         1 |             0.0453 |            0.0415 |             0.7143 | 0.0547 |   0.1641 |
| suricata   | recall_top10                       | lepes5 > lepes4 |        3 |         4 |            -0.0070 |           -0.0014 |            -0.2857 | 0.7656 |   0.7656 |
| suricata   | recall_top10                       | lepes5 > lepes3 |        6 |         1 |             0.0431 |            0.0401 |             0.8571 | 0.0234 |   0.0938 |
| suricata   | workload_98                        | lepes3 > lepes1 |        8 |         0 |             0.1126 |            0.1591 |             1.0000 | 0.0039 |   0.0156 |
| suricata   | workload_98                        | lepes4 > lepes3 |        4 |         4 |             0.0061 |            0.0297 |             0.3333 | 0.2305 |   0.6914 |
| suricata   | workload_98                        | lepes5 > lepes4 |        0 |         7 |            -0.0012 |           -0.0027 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | workload_98                        | lepes5 > lepes3 |        4 |         4 |             0.0055 |            0.0270 |             0.2778 | 0.2734 |   0.6914 |
| wazuh      | auroc                              | lepes3 > lepes1 |        3 |         5 |            -0.0007 |           -0.0053 |            -0.3333 | 0.8086 |   1.0000 |
| wazuh      | auroc                              | lepes4 > lepes3 |        0 |         8 |            -0.0781 |           -0.0809 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | auroc                              | lepes5 > lepes4 |        8 |         0 |             0.0013 |            0.0012 |             1.0000 | 0.0039 |   0.0156 |
| wazuh      | auroc                              | lepes5 > lepes3 |        0 |         8 |            -0.0772 |           -0.0797 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | ap                                 | lepes3 > lepes1 |        0 |         8 |            -0.0017 |           -0.0420 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | ap                                 | lepes4 > lepes3 |        0 |         8 |            -0.1663 |           -0.2010 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | ap                                 | lepes5 > lepes4 |        8 |         0 |             0.0010 |            0.0012 |             1.0000 | 0.0039 |   0.0156 |
| wazuh      | ap                                 | lepes5 > lepes3 |        0 |         8 |            -0.1650 |           -0.1999 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | recall_top10                       | lepes3 > lepes1 |        1 |         7 |            -0.0005 |           -0.0223 |            -0.7222 | 0.9727 |   1.0000 |
| wazuh      | recall_top10                       | lepes4 > lepes3 |        0 |         8 |            -0.0976 |           -0.1833 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | recall_top10                       | lepes5 > lepes4 |        4 |         1 |             0.0000 |            0.0000 |             0.3333 | 0.3125 |   1.0000 |
| wazuh      | recall_top10                       | lepes5 > lepes3 |        0 |         8 |            -0.0975 |           -0.1832 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | workload_98                        | lepes3 > lepes1 |        8 |         0 |             0.0753 |            0.1091 |             1.0000 | 0.0039 |   0.0156 |
| wazuh      | workload_98                        | lepes4 > lepes3 |        3 |         5 |            -0.0029 |            0.0207 |             0.0556 | 0.4727 |   0.9453 |
| wazuh      | workload_98                        | lepes5 > lepes4 |        8 |         0 |             0.0001 |            0.0021 |             1.0000 | 0.0039 |   0.0156 |
| wazuh      | workload_98                        | lepes5 > lepes3 |        3 |         5 |            -0.0028 |            0.0228 |             0.0556 | 0.4727 |   0.9453 |
| suricata   | terheles_98 (csoport vs. riasztás) | lepes2 > lepes1 |        7 |         0 |             0.3235 |            0.4662 |             1.0000 | 0.0078 |   0.0078 |
| wazuh      | terheles_98 (csoport vs. riasztás) | lepes2 > lepes1 |        8 |         0 |             0.8785 |            0.8883 |             1.0000 | 0.0039 |   0.0039 |

## 3. Ellenpróba (100 keverés forgatókönyvenként)

kevert_AP_>=_valodi: a keverések hányad része érte el vagy múlta felül a valódi nyilvántartással mért AP-t (kicsi = a javulás a környezeti információnak köszönhető).

| erzekelo   | forgatokonyv    | lepes   |   AP_valodi |   AP_kevert_atlag |   kevert_AP_>=_valodi |   kevert_terheles_<=_valodi |
|:-----------|:----------------|:--------|------------:|------------------:|----------------------:|----------------------------:|
| suricata   | fox             | lepes4  |       0.143 |             0.079 |                 0.000 |                       0.120 |
| suricata   | fox             | lepes5  |       0.140 |             0.118 |                 0.130 |                       1.000 |
| wazuh      | fox             | lepes4  |       0.980 |             0.950 |                 0.570 |                       0.590 |
| wazuh      | fox             | lepes5  |       0.980 |             0.968 |                 0.350 |                       0.440 |
| suricata   | harrison        | lepes4  |       0.065 |             0.054 |                 0.020 |                       0.070 |
| suricata   | harrison        | lepes5  |       0.063 |             0.065 |                 0.770 |                       1.000 |
| wazuh      | harrison        | lepes4  |       0.998 |             0.938 |                 0.360 |                       0.420 |
| wazuh      | harrison        | lepes5  |       0.998 |             0.988 |                 0.400 |                       0.400 |
| suricata   | russellmitchell | lepes4  |       0.225 |             0.132 |                 0.040 |                       0.330 |
| suricata   | russellmitchell | lepes5  |       0.221 |             0.193 |                 0.140 |                       1.000 |
| wazuh      | russellmitchell | lepes4  |       0.592 |             0.650 |                 0.570 |                       0.040 |
| wazuh      | russellmitchell | lepes5  |       0.594 |             0.615 |                 0.240 |                       0.710 |
| suricata   | santos          | lepes4  |       0.076 |             0.034 |                 0.010 |                       0.000 |
| suricata   | santos          | lepes5  |       0.087 |             0.067 |                 0.000 |                       1.000 |
| wazuh      | santos          | lepes4  |       0.442 |             0.589 |                 0.610 |                       0.500 |
| wazuh      | santos          | lepes5  |       0.445 |             0.520 |                 0.360 |                       0.750 |
| suricata   | shaw            | lepes4  |       0.010 |             0.015 |                 0.680 |                       0.750 |
| suricata   | shaw            | lepes5  |       0.010 |             0.011 |                 1.000 |                       1.000 |
| wazuh      | shaw            | lepes4  |       0.281 |             0.523 |                 0.640 |                       0.160 |
| wazuh      | shaw            | lepes5  |       0.282 |             0.412 |                 0.420 |                       0.150 |
| suricata   | wardbeck        | lepes4  |       0.095 |             0.052 |                 0.070 |                       0.090 |
| suricata   | wardbeck        | lepes5  |       0.112 |             0.083 |                 0.010 |                       0.450 |
| wazuh      | wardbeck        | lepes4  |       0.396 |             0.604 |                 0.640 |                       0.640 |
| wazuh      | wardbeck        | lepes5  |       0.398 |             0.493 |                 0.440 |                       0.350 |
| suricata   | wheeler         | lepes4  |       0.047 |             0.021 |                 0.080 |                       0.680 |
| suricata   | wheeler         | lepes5  |       0.054 |             0.050 |                 0.380 |                       1.000 |
| wazuh      | wheeler         | lepes4  |       0.981 |             0.914 |                 0.510 |                       0.510 |
| wazuh      | wheeler         | lepes5  |       0.982 |             0.960 |                 0.300 |                       0.380 |
| suricata   | wilson          | lepes4  |       0.132 |             0.075 |                 0.070 |                       0.080 |
| suricata   | wilson          | lepes5  |       0.158 |             0.114 |                 0.190 |                       0.580 |
| wazuh      | wilson          | lepes4  |       0.973 |             0.925 |                 0.610 |                       0.640 |
| wazuh      | wilson          | lepes5  |       0.974 |             0.958 |                 0.380 |                       0.450 |

## 4. ±20%-os súlyváltozás és hiányos nyilvántartás

dAP, dTerheles: a változás a lépés teljes beállításához képest (átlag, legkisebb, legnagyobb a 8 forgatókönyvön); AP_vs_lepes3: a 3. lépéshez képest. A hiányos nyilvántartásnál 20 véletlen ismétlés átlaga.

|                                          |   ('dAP', 'mean') |   ('dAP', 'min') |   ('dAP', 'max') |   ('dTerheles', 'mean') |   ('dTerheles', 'min') |   ('dTerheles', 'max') |   ('AP_vs_lepes3', 'mean') |   ('AP_vs_lepes3', 'min') |   ('AP_vs_lepes3', 'max') |
|:-----------------------------------------|------------------:|-----------------:|-----------------:|------------------------:|-----------------------:|-----------------------:|---------------------------:|--------------------------:|--------------------------:|
| ('suricata', 'lepes4_erzekenyseg_g+20%') |           -0.0009 |          -0.0057 |           0.0007 |                  0      |                 0      |                 0      |                     0.0262 |                   -0.0051 |                    0.0548 |
| ('suricata', 'lepes4_erzekenyseg_g-20%') |            0.0017 |          -0.0022 |           0.0058 |                 -0      |                -0      |                 0      |                     0.0288 |                   -0.0051 |                    0.0663 |
| ('suricata', 'lepes4_hiany20')           |           -0.0024 |          -0.0182 |           0.0041 |                  0.0034 |                -0.0611 |                 0.0418 |                     0.0247 |                   -0.0026 |                    0.0429 |
| ('suricata', 'lepes4_hiany50')           |           -0.0137 |          -0.0355 |           0.0028 |                  0.0336 |                -0.0621 |                 0.2586 |                     0.0133 |                   -0.0051 |                    0.036  |
| ('suricata', 'lepes5_erzekenyseg_a+20%') |           -0.0026 |          -0.0182 |           0.0028 |                  0.0006 |                 0      |                 0.0032 |                     0.0308 |                   -0.0052 |                    0.066  |
| ('suricata', 'lepes5_erzekenyseg_a-20%') |           -0.0013 |          -0.0043 |           0.0006 |                 -0.0003 |                -0.0019 |                 0      |                     0.0321 |                   -0.0052 |                    0.0588 |
| ('suricata', 'lepes5_hiany20')           |           -0.0028 |          -0.0155 |           0.0022 |                  0.0069 |                -0.048  |                 0.0398 |                     0.0307 |                   -0.003  |                    0.0546 |
| ('suricata', 'lepes5_hiany50')           |           -0.017  |          -0.036  |           0.0026 |                  0.0368 |                -0.0493 |                 0.2493 |                     0.0165 |                   -0.0089 |                    0.0399 |
| ('wazuh', 'lepes4_erzekenyseg_g+20%')    |           -0.058  |          -0.1386 |          -0.0047 |                  0.002  |                -0.0002 |                 0.0063 |                    -0.2591 |                   -0.5606 |                   -0.0061 |
| ('wazuh', 'lepes4_erzekenyseg_g-20%')    |            0.0682 |           0.0013 |           0.2246 |                 -0.001  |                -0.0027 |                 0.0001 |                    -0.1328 |                   -0.4098 |                   -0.0001 |
| ('wazuh', 'lepes4_hiany20')              |            0.0264 |          -0.0253 |           0.1258 |                 -0.0001 |                -0.0137 |                 0.0086 |                    -0.1746 |                   -0.4552 |                   -0.0077 |
| ('wazuh', 'lepes4_hiany50')              |            0.0651 |          -0.0373 |           0.2024 |                  0.0109 |                -0.0092 |                 0.038  |                    -0.1359 |                   -0.2894 |                   -0.0174 |
| ('wazuh', 'lepes5_erzekenyseg_a+20%')    |            0.0001 |          -0      |           0.0007 |                  0.0002 |                -0.0006 |                 0.0027 |                    -0.1997 |                   -0.4901 |                   -0.0013 |
| ('wazuh', 'lepes5_erzekenyseg_a-20%')    |           -0.0002 |          -0.0008 |           0      |                  0.0003 |                 0      |                 0.002  |                    -0.2    |                   -0.4904 |                   -0.0013 |
| ('wazuh', 'lepes5_hiany20')              |            0.0241 |          -0.0321 |           0.1251 |                  0.0015 |                -0.0156 |                 0.0192 |                    -0.1758 |                   -0.4543 |                   -0.0106 |
| ('wazuh', 'lepes5_hiany50')              |            0.0605 |          -0.0483 |           0.1987 |                  0.0133 |                -0.0098 |                 0.0507 |                    -0.1394 |                   -0.2914 |                   -0.0248 |

## 5. Tanult súlyok egy-kihagyással kontra AHP-súlyok (5. lépés: r, g, a)

AHP (újranormálva): r = 0.535, g = 0.306, a = 0.160. A tanult súlyok a 7 tanító forgatókönyv átlagos AP-jét maximalizálják a 0,05-ös rácson; a mérés a kihagyott forgatókönyvön.

| erzekelo   | kihagyott       |   w_r |   w_g |   w_a |   tanulo_ap |   ap_tanult |   workload_98_tanult |   ap_ahp |   workload_98_ahp |
|:-----------|:----------------|------:|------:|------:|------------:|------------:|---------------------:|---------:|------------------:|
| suricata   | fox             | 0.550 | 0.300 | 0.150 |       0.101 |       0.141 |                0.909 |    0.140 |             0.909 |
| suricata   | harrison        | 0.600 | 0.250 | 0.150 |       0.113 |       0.063 |                0.721 |    0.063 |             0.721 |
| suricata   | russellmitchell | 0.600 | 0.250 | 0.150 |       0.091 |       0.221 |                0.916 |    0.221 |             0.914 |
| suricata   | santos          | 0.650 | 0.200 | 0.150 |       0.110 |       0.082 |                0.416 |    0.087 |             0.416 |
| suricata   | shaw            | 0.600 | 0.250 | 0.150 |       0.121 |       0.010 |                0.893 |    0.010 |             0.892 |
| suricata   | wardbeck        | 0.600 | 0.200 | 0.200 |       0.107 |       0.095 |                0.871 |    0.112 |             0.870 |
| suricata   | wheeler         | 0.600 | 0.250 | 0.150 |       0.115 |       0.054 |                0.938 |    0.054 |             0.938 |
| suricata   | wilson          | 0.700 | 0.200 | 0.100 |       0.101 |       0.136 |                0.853 |    0.158 |             0.853 |
| wazuh      | fox             | 0.950 | 0.050 | 0.000 |       0.894 |       0.999 |                0.917 |    0.980 |             0.922 |
| wazuh      | harrison        | 0.950 | 0.050 | 0.000 |       0.894 |       1.000 |                0.912 |    0.998 |             0.913 |
| wazuh      | russellmitchell | 0.900 | 0.050 | 0.050 |       0.909 |       0.890 |                0.694 |    0.594 |             0.668 |
| wazuh      | santos          | 0.700 | 0.050 | 0.250 |       0.922 |       0.798 |                0.843 |    0.445 |             0.844 |
| wazuh      | shaw            | 0.800 | 0.000 | 0.200 |       0.945 |       0.639 |                0.796 |    0.282 |             0.614 |
| wazuh      | wardbeck        | 0.750 | 0.050 | 0.200 |       0.914 |       0.852 |                0.853 |    0.398 |             0.862 |
| wazuh      | wheeler         | 0.950 | 0.050 | 0.000 |       0.894 |       0.999 |                0.882 |    0.982 |             0.887 |
| wazuh      | wilson          | 0.950 | 0.050 | 0.000 |       0.894 |       0.998 |                0.849 |    0.974 |             0.857 |

| erzekelo   | meroszam    |   atlag_tanult |   atlag_ahp |   tanult_jobb |   p_ketoldali |
|:-----------|:------------|---------------:|------------:|--------------:|--------------:|
| suricata   | ap          |         0.1002 |      0.1055 |             4 |        0.6406 |
| suricata   | workload_98 |         0.8146 |      0.8140 |             1 |        0.0938 |
| wazuh      | ap          |         0.8969 |      0.7067 |             8 |        0.0078 |
| wazuh      | workload_98 |         0.8432 |      0.8208 |             6 |        0.7422 |

## 6. Címke-érzékenység: russellmitchell, időszak-alapú kontra CATS-címke

|                                    |   ('ap', 'cats') |   ('ap', 'idoszak') |   ('workload_98', 'cats') |   ('workload_98', 'idoszak') |
|:-----------------------------------|-----------------:|--------------------:|--------------------------:|-----------------------------:|
| ('suricata', 'csoport', 'lepes2')  |            0.783 |               0.202 |                     0.113 |                        0.985 |
| ('suricata', 'csoport', 'lepes3')  |            0.842 |               0.216 |                     0.113 |                        0.834 |
| ('suricata', 'csoport', 'lepes4')  |            0.751 |               0.255 |                     0.078 |                        0.968 |
| ('suricata', 'csoport', 'lepes5')  |            0.864 |               0.298 |                     0.625 |                        0.987 |
| ('suricata', 'riasztas', 'lepes1') |            0.615 |               0.147 |                     1     |                        1     |
| ('suricata', 'riasztas', 'lepes3') |            0.808 |               0.194 |                     0.29  |                        0.808 |
| ('suricata', 'riasztas', 'lepes4') |            0.863 |               0.225 |                     0.143 |                        0.914 |
| ('suricata', 'riasztas', 'lepes5') |            0.838 |               0.221 |                     0.459 |                        0.914 |
| ('wazuh', 'csoport', 'lepes2')     |            0.999 |               0.985 |                     0.331 |                        0.425 |
| ('wazuh', 'csoport', 'lepes3')     |            0.998 |               0.981 |                     0.331 |                        0.716 |
| ('wazuh', 'csoport', 'lepes4')     |            0.541 |               0.544 |                     0.611 |                        0.692 |
| ('wazuh', 'csoport', 'lepes5')     |            0.541 |               0.544 |                     0.611 |                        0.692 |
| ('wazuh', 'riasztas', 'lepes1')    |            0.976 |               0.951 |                     0.339 |                        1     |
| ('wazuh', 'riasztas', 'lepes3')    |            0.921 |               0.9   |                     0.334 |                        0.757 |
| ('wazuh', 'riasztas', 'lepes4')    |            0.586 |               0.592 |                     0.424 |                        0.672 |
| ('wazuh', 'riasztas', 'lepes5')    |            0.588 |               0.594 |                     0.423 |                        0.668 |

## 7. Csoportosítás (2. lépés, 60 perc)

tisztasag_fazis: a csoportokban a leggyakoribb támadási lépéshez (vagy a normál forgalomhoz) tartozó riasztások aránya; a russellmitchell a hangoló forgatókönyv.

| erzekelo   | forgatokonyv    |   riasztas |   csoportok |   tetelszam_csokkenes |   tisztasag_fazis |   tisztasag_ketertek |
|:-----------|:----------------|-----------:|------------:|----------------------:|------------------:|---------------------:|
| wazuh      | fox             |     440355 |     70.0000 |                0.9998 |            0.9867 |               0.9980 |
| suricata   | fox             |      11084 |     88.0000 |                0.9921 |            0.9726 |               0.9777 |
| wazuh      | harrison        |     448959 |     45.0000 |                0.9999 |            0.9847 |               0.9955 |
| suricata   | harrison        |      67384 |     66.0000 |                0.9990 |            0.9667 |               0.9667 |
| wazuh      | russellmitchell |      23116 |     29.0000 |                0.9987 |            0.8446 |               0.9822 |
| suricata   | russellmitchell |       9186 |     79.0000 |                0.9914 |            0.9877 |               0.9882 |
| wazuh      | santos          |      38289 |     30.0000 |                0.9992 |            0.8885 |               0.9742 |
| suricata   | santos          |      44112 |     60.0000 |                0.9986 |            0.9910 |               0.9910 |
| wazuh      | shaw            |      35139 |     54.0000 |                0.9985 |            0.9631 |               0.9898 |
| suricata   | shaw            |      16692 |     93.0000 |                0.9944 |            0.9878 |               0.9878 |
| wazuh      | wardbeck        |      39184 |     79.0000 |                0.9980 |            0.9654 |               0.9888 |
| suricata   | wardbeck        |      24510 |    106.0000 |                0.9957 |            0.9920 |               0.9920 |
| wazuh      | wheeler         |     466636 |     32.0000 |                0.9999 |            0.9852 |               0.9995 |
| suricata   | wheeler         |      68629 |     67.0000 |                0.9990 |            0.9902 |               0.9902 |
| wazuh      | wilson          |     495227 |     68.0000 |                0.9999 |            0.9894 |               0.9963 |
| suricata   | wilson          |      65038 |     91.0000 |                0.9986 |            0.9747 |               0.9755 |

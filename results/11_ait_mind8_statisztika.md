# A 8 forgatókönyves mérés statisztikai kiértékelése (AIT-ADS, 1–5. lépés)

Készült: 2026-11-18 13:46 UTC · kód: `47cfb7a` · forgatókönyvek: 1 · terv: `config/elozetes_rogzites/ait_mind8_meresi_terv.yaml` (D29) · címke: időszak-alapú (D28) · bemenet: `results/10_ait_mind8_lepes1_5_meres.csv`

## 1. Átlag ± szórás a forgatókönyvek között

auroc: rangsor-pontosság; ap: átlagos pontosság; recall_top10: a valódi riasztások aránya a lista első 10%-ában; workload_98 (csoportszinten csoport_terheles_98): a lista hányad részét kell átnézni a valódi riasztások 98%-áig (kisebb = jobb).

### suricata – csoportszint

|                      | auroc       | ap          | recall_top10   | workload_98   | csoport_terheles_98   |
|:---------------------|:------------|:------------|:---------------|:--------------|:----------------------|
| 2. csoportosítás     | 0.460 ± nan | 0.202 ± nan | 0.183 ± nan    | 0.985 ± nan   | 0.722 ± nan           |
| 3. kockázati         | 0.577 ± nan | 0.216 ± nan | 0.183 ± nan    | 0.834 ± nan   | 0.430 ± nan           |
| 4. + gép fontossága  | 0.714 ± nan | 0.255 ± nan | 0.465 ± nan    | 0.968 ± nan   | 0.709 ± nan           |
| 5. + alkalmazhatóság | 0.752 ± nan | 0.298 ± nan | 0.574 ± nan    | 0.987 ± nan   | 0.911 ± nan           |

### suricata – riasztásszint

|                      | auroc       | ap          | recall_top10   | workload_98   |
|:---------------------|:------------|:------------|:---------------|:--------------|
| 1. súlyosság         | 0.563 ± nan | 0.147 ± nan | 0.210 ± nan    | 1.000 ± nan   |
| 3. kockázati         | 0.544 ± nan | 0.194 ± nan | 0.221 ± nan    | 0.808 ± nan   |
| 4. + gép fontossága  | 0.725 ± nan | 0.225 ± nan | 0.286 ± nan    | 0.914 ± nan   |
| 5. + alkalmazhatóság | 0.719 ± nan | 0.221 ± nan | 0.272 ± nan    | 0.914 ± nan   |

### wazuh – csoportszint

|                      | auroc       | ap          | recall_top10   | workload_98   | csoport_terheles_98   |
|:---------------------|:------------|:------------|:---------------|:--------------|:----------------------|
| 2. csoportosítás     | 0.990 ± nan | 0.985 ± nan | 0.285 ± nan    | 0.425 ± nan   | 0.138 ± nan           |
| 3. kockázati         | 0.984 ± nan | 0.981 ± nan | 0.285 ± nan    | 0.716 ± nan   | 0.138 ± nan           |
| 4. + gép fontossága  | 0.595 ± nan | 0.544 ± nan | 0.037 ± nan    | 0.692 ± nan   | 0.241 ± nan           |
| 5. + alkalmazhatóság | 0.595 ± nan | 0.544 ± nan | 0.037 ± nan    | 0.692 ± nan   | 0.241 ± nan           |

### wazuh – riasztásszint

|                      | auroc       | ap          | recall_top10   | workload_98   |
|:---------------------|:------------|:------------|:---------------|:--------------|
| 1. súlyosság         | 0.971 ± nan | 0.951 ± nan | 0.280 ± nan    | 1.000 ± nan   |
| 3. kockázati         | 0.958 ± nan | 0.900 ± nan | 0.260 ± nan    | 0.757 ± nan   |
| 4. + gép fontossága  | 0.846 ± nan | 0.592 ± nan | 0.072 ± nan    | 0.672 ± nan   |
| 5. + alkalmazhatóság | 0.847 ± nan | 0.594 ± nan | 0.072 ± nan    | 0.668 ± nan   |

## 2. Páros, egyoldali Wilcoxon-próba (H1: az újabb lépés jobb)

javult/romlott: a forgatókönyvek száma; a különbség a „jobb” irányba előjelezve (terhelésnél a csökkenés pozitív); rang_biszerialis: párosított rang-biszeriális korreláció (+1: minden forgatókönyvön javult); p_holm: Holm-korrekció érzékelőnként és mérőszámonként a négy riasztásszintű összevetésre. 8 párnál a legkisebb elérhető p-érték 0,0039.

| erzekelo   | meroszam                           | osszevetes      |   javult |   romlott |   kulonbseg_median |   kulonbseg_atlag |   rang_biszerialis |      p |   p_holm |
|:-----------|:-----------------------------------|:----------------|---------:|----------:|-------------------:|------------------:|-------------------:|-------:|---------:|
| suricata   | auroc                              | lepes3 > lepes1 |        0 |         1 |            -0.0183 |           -0.0183 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | auroc                              | lepes4 > lepes3 |        1 |         0 |             0.1807 |            0.1807 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | auroc                              | lepes5 > lepes4 |        0 |         1 |            -0.0062 |           -0.0062 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | auroc                              | lepes5 > lepes3 |        1 |         0 |             0.1745 |            0.1745 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | ap                                 | lepes3 > lepes1 |        1 |         0 |             0.0466 |            0.0466 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | ap                                 | lepes4 > lepes3 |        1 |         0 |             0.0311 |            0.0311 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | ap                                 | lepes5 > lepes4 |        0 |         1 |            -0.0040 |           -0.0040 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | ap                                 | lepes5 > lepes3 |        1 |         0 |             0.0271 |            0.0271 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | recall_top10                       | lepes3 > lepes1 |        1 |         0 |             0.0104 |            0.0104 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | recall_top10                       | lepes4 > lepes3 |        1 |         0 |             0.0657 |            0.0657 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | recall_top10                       | lepes5 > lepes4 |        0 |         1 |            -0.0141 |           -0.0141 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | recall_top10                       | lepes5 > lepes3 |        1 |         0 |             0.0516 |            0.0516 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | workload_98                        | lepes3 > lepes1 |        1 |         0 |             0.1925 |            0.1925 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | workload_98                        | lepes4 > lepes3 |        0 |         1 |            -0.1065 |           -0.1065 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | workload_98                        | lepes5 > lepes4 |        0 |         1 |            -0.0004 |           -0.0004 |            -1.0000 | 1.0000 |   1.0000 |
| suricata   | workload_98                        | lepes5 > lepes3 |        0 |         1 |            -0.1069 |           -0.1069 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | auroc                              | lepes3 > lepes1 |        0 |         1 |            -0.0124 |           -0.0124 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | auroc                              | lepes4 > lepes3 |        0 |         1 |            -0.1125 |           -0.1125 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | auroc                              | lepes5 > lepes4 |        1 |         0 |             0.0013 |            0.0013 |             1.0000 | 0.5000 |   1.0000 |
| wazuh      | auroc                              | lepes5 > lepes3 |        0 |         1 |            -0.1112 |           -0.1112 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | ap                                 | lepes3 > lepes1 |        0 |         1 |            -0.0508 |           -0.0508 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | ap                                 | lepes4 > lepes3 |        0 |         1 |            -0.3080 |           -0.3080 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | ap                                 | lepes5 > lepes4 |        1 |         0 |             0.0020 |            0.0020 |             1.0000 | 0.5000 |   1.0000 |
| wazuh      | ap                                 | lepes5 > lepes3 |        0 |         1 |            -0.3060 |           -0.3060 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | recall_top10                       | lepes3 > lepes1 |        0 |         1 |            -0.0203 |           -0.0203 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | recall_top10                       | lepes4 > lepes3 |        0 |         1 |            -0.1876 |           -0.1876 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | recall_top10                       | lepes5 > lepes4 |        0 |         0 |             0.0000 |            0.0000 |             0.0000 | 1.0000 |   1.0000 |
| wazuh      | recall_top10                       | lepes5 > lepes3 |        0 |         1 |            -0.1876 |           -0.1876 |            -1.0000 | 1.0000 |   1.0000 |
| wazuh      | workload_98                        | lepes3 > lepes1 |        1 |         0 |             0.2430 |            0.2430 |             1.0000 | 0.5000 |   1.0000 |
| wazuh      | workload_98                        | lepes4 > lepes3 |        1 |         0 |             0.0850 |            0.0850 |             1.0000 | 0.5000 |   1.0000 |
| wazuh      | workload_98                        | lepes5 > lepes4 |        1 |         0 |             0.0035 |            0.0035 |             1.0000 | 0.5000 |   1.0000 |
| wazuh      | workload_98                        | lepes5 > lepes3 |        1 |         0 |             0.0885 |            0.0885 |             1.0000 | 0.5000 |   1.0000 |
| suricata   | terheles_98 (csoport vs. riasztás) | lepes2 > lepes1 |        1 |         0 |             0.2785 |            0.2785 |             1.0000 | 0.5000 |   0.5000 |
| wazuh      | terheles_98 (csoport vs. riasztás) | lepes2 > lepes1 |        1 |         0 |             0.8621 |            0.8621 |             1.0000 | 0.5000 |   0.5000 |

## 3. Ellenpróba (100 keverés forgatókönyvenként)

kevert_AP_>=_valodi: a keverések hányad része érte el vagy múlta felül a valódi nyilvántartással mért AP-t (kicsi = a javulás a környezeti információnak köszönhető).

| erzekelo   | forgatokonyv    | lepes   |   AP_valodi |   AP_kevert_atlag |   kevert_AP_>=_valodi |   kevert_terheles_<=_valodi |
|:-----------|:----------------|:--------|------------:|------------------:|----------------------:|----------------------------:|
| suricata   | russellmitchell | lepes4  |       0.225 |             0.132 |                 0.040 |                       0.330 |
| suricata   | russellmitchell | lepes5  |       0.221 |             0.193 |                 0.140 |                       1.000 |
| wazuh      | russellmitchell | lepes4  |       0.592 |             0.650 |                 0.570 |                       0.040 |
| wazuh      | russellmitchell | lepes5  |       0.594 |             0.615 |                 0.240 |                       0.710 |

## 4. ±20%-os súlyváltozás és hiányos nyilvántartás

dAP, dTerheles: a változás a lépés teljes beállításához képest (átlag, legkisebb, legnagyobb a 8 forgatókönyvön); AP_vs_lepes3: a 3. lépéshez képest. A hiányos nyilvántartásnál 20 véletlen ismétlés átlaga.

|                                          |   ('dAP', 'mean') |   ('dAP', 'min') |   ('dAP', 'max') |   ('dTerheles', 'mean') |   ('dTerheles', 'min') |   ('dTerheles', 'max') |   ('AP_vs_lepes3', 'mean') |   ('AP_vs_lepes3', 'min') |   ('AP_vs_lepes3', 'max') |
|:-----------------------------------------|------------------:|-----------------:|-----------------:|------------------------:|-----------------------:|-----------------------:|---------------------------:|--------------------------:|--------------------------:|
| ('suricata', 'lepes4_erzekenyseg_g+20%') |           -0.0006 |          -0.0006 |          -0.0006 |                  0      |                 0      |                 0      |                     0.0305 |                    0.0305 |                    0.0305 |
| ('suricata', 'lepes4_erzekenyseg_g-20%') |            0.0052 |           0.0052 |           0.0052 |                  0      |                 0      |                 0      |                     0.0363 |                    0.0363 |                    0.0363 |
| ('suricata', 'lepes4_hiany20')           |           -0.0004 |          -0.0004 |          -0.0004 |                 -0.0099 |                -0.0099 |                -0.0099 |                     0.0306 |                    0.0306 |                    0.0306 |
| ('suricata', 'lepes4_hiany50')           |           -0.0355 |          -0.0355 |          -0.0355 |                 -0.0134 |                -0.0134 |                -0.0134 |                    -0.0044 |                   -0.0044 |                   -0.0044 |
| ('suricata', 'lepes5_erzekenyseg_a+20%') |           -0.0041 |          -0.0041 |          -0.0041 |                  0      |                 0      |                 0      |                     0.023  |                    0.023  |                    0.023  |
| ('suricata', 'lepes5_erzekenyseg_a-20%') |           -0.0038 |          -0.0038 |          -0.0038 |                  0      |                 0      |                 0      |                     0.0233 |                    0.0233 |                    0.0233 |
| ('suricata', 'lepes5_hiany20')           |           -0.0006 |          -0.0006 |          -0.0006 |                 -0.0033 |                -0.0033 |                -0.0033 |                     0.0265 |                    0.0265 |                    0.0265 |
| ('suricata', 'lepes5_hiany50')           |           -0.036  |          -0.036  |          -0.036  |                 -0.0091 |                -0.0091 |                -0.0091 |                    -0.0089 |                   -0.0089 |                   -0.0089 |
| ('wazuh', 'lepes4_erzekenyseg_g+20%')    |           -0.1386 |          -0.1386 |          -0.1386 |                 -0.0002 |                -0.0002 |                -0.0002 |                    -0.4465 |                   -0.4465 |                   -0.4465 |
| ('wazuh', 'lepes4_erzekenyseg_g-20%')    |            0.1329 |           0.1329 |           0.1329 |                 -0.0009 |                -0.0009 |                -0.0009 |                    -0.1751 |                   -0.1751 |                   -0.1751 |
| ('wazuh', 'lepes4_hiany20')              |            0.0335 |           0.0335 |           0.0335 |                 -0.0096 |                -0.0096 |                -0.0096 |                    -0.2744 |                   -0.2744 |                   -0.2744 |
| ('wazuh', 'lepes4_hiany50')              |            0.0773 |           0.0773 |           0.0773 |                  0.0303 |                 0.0303 |                 0.0303 |                    -0.2307 |                   -0.2307 |                   -0.2307 |
| ('wazuh', 'lepes5_erzekenyseg_a+20%')    |            0.0007 |           0.0007 |           0.0007 |                  0      |                 0      |                 0      |                    -0.3053 |                   -0.3053 |                   -0.3053 |
| ('wazuh', 'lepes5_erzekenyseg_a-20%')    |           -0.0001 |          -0.0001 |          -0.0001 |                  0.002  |                 0.002  |                 0.002  |                    -0.3061 |                   -0.3061 |                   -0.3061 |
| ('wazuh', 'lepes5_hiany20')              |            0.0326 |           0.0326 |           0.0326 |                 -0.0084 |                -0.0084 |                -0.0084 |                    -0.2733 |                   -0.2733 |                   -0.2733 |
| ('wazuh', 'lepes5_hiany50')              |            0.0753 |           0.0753 |           0.0753 |                  0.0341 |                 0.0341 |                 0.0341 |                    -0.2307 |                   -0.2307 |                   -0.2307 |

## 5. Tanult súlyok egy-kihagyással kontra AHP-súlyok (5. lépés: r, g, a)

AHP (újranormálva): r = 0.535, g = 0.306, a = 0.160. A tanult súlyok a 7 tanító forgatókönyv átlagos AP-jét maximalizálják a 0,05-ös rácson; a mérés a kihagyott forgatókönyvön.

| erzekelo   | kihagyott   | w_r   | w_g   | w_a   | tanulo_ap   | ap_tanult   | workload_98_tanult   | ap_ahp   | workload_98_ahp   |
|------------|-------------|-------|-------|-------|-------------|-------------|----------------------|----------|-------------------|



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
| wazuh      | russellmitchell |      23116 |     29.0000 |                0.9987 |            0.8446 |               0.9822 |
| suricata   | russellmitchell |       9186 |     79.0000 |                0.9914 |            0.9877 |               0.9882 |

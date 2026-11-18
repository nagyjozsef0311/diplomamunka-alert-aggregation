# 2. lépés – csoportosítás (AIT-ADS, russellmitchell)

Készült: 2026-11-18 12:35 UTC · kód: `dc23189` · dolgozat: 5.3, 6.2. táblázat, 6.3 · időköz-szabály: D26 · **hangoló forgatókönyv, mintán belüli**

## Az időköz kiválasztása (tisztasági küszöb: 0.95)

| adathalmaz   |   idokoz_perc |   tisztasag |   tetelszam_csokkenes |
|:-------------|--------------:|------------:|----------------------:|
| ait_wazuh    |             1 |      0.9990 |                0.9320 |
| ait_wazuh    |             5 |      0.9990 |                0.9794 |
| ait_wazuh    |            15 |      0.9990 |                0.9874 |
| ait_wazuh    |            60 |      0.9990 |                0.9987 |
| ait_suricata |             1 |      0.9998 |                0.8762 |
| ait_suricata |             5 |      0.9995 |                0.9340 |
| ait_suricata |            15 |      0.9995 |                0.9708 |
| ait_suricata |            60 |      0.9995 |                0.9914 |

## Rangsorolás riasztás- és csoportszinten

A csoportszintű sorokban minden riasztás a csoportja pontszámát kapja (4.3). csoport_terheles_98: a csoportok hányad részét kell átnézni a valódi riasztások 98%-áig.

| adathalmaz   | valtozat                           |   idokoz_perc |   auroc |    ap |   recall_top10 |   true_in_top10 |   workload_98 |   csoportok |   tetelszam_csokkenes |   tisztasag |   csoport_terheles_98 |
|:-------------|:-----------------------------------|--------------:|--------:|------:|---------------:|----------------:|--------------:|------------:|----------------------:|------------:|----------------------:|
| ait_wazuh    | lepes1_sulyossag_riasztasszint     |            60 |   0.993 | 0.976 |          0.294 |        2253.924 |         0.339 |     nan     |               nan     |     nan     |               nan     |
| ait_wazuh    | lepes2_csoportositas               |            60 |   0.999 | 0.999 |          0.302 |        2311.697 |         0.331 |      29.000 |                 0.999 |       0.999 |                 0.034 |
| ait_wazuh    | lepes3_kockazati_riasztasszint     |            60 |   0.987 | 0.921 |          0.275 |        2109.000 |         0.334 |     nan     |               nan     |     nan     |               nan     |
| ait_wazuh    | lepes3_kockazati_csoportszint      |            60 |   0.998 | 0.998 |          0.302 |        2311.697 |         0.331 |      29.000 |                 0.999 |       0.999 |                 0.034 |
| ait_wazuh    | lepes4_kockazati+gep_riasztasszint |            60 |   0.861 | 0.586 |          0.074 |         569.000 |         0.424 |     nan     |               nan     |     nan     |               nan     |
| ait_wazuh    | lepes4_kockazati+gep_csoportszint  |            60 |   0.580 | 0.541 |          0.000 |           0.000 |         0.611 |      29.000 |                 0.999 |       0.999 |                 0.138 |
| ait_suricata | lepes1_sulyossag_riasztasszint     |            60 |   0.806 | 0.615 |          0.651 |          28.625 |         1.000 |     nan     |               nan     |     nan     |               nan     |
| ait_suricata | lepes2_csoportositas               |            60 |   0.983 | 0.783 |          0.841 |          37.000 |         0.113 |      79.000 |                 0.991 |       0.999 |                 0.139 |
| ait_suricata | lepes3_kockazati_riasztasszint     |            60 |   0.991 | 0.808 |          0.977 |          43.000 |         0.290 |     nan     |               nan     |     nan     |               nan     |
| ait_suricata | lepes3_kockazati_csoportszint      |            60 |   0.983 | 0.842 |          0.841 |          37.000 |         0.113 |      79.000 |                 0.991 |       0.999 |                 0.114 |
| ait_suricata | lepes4_kockazati+gep_riasztasszint |            60 |   0.991 | 0.863 |          0.955 |          42.000 |         0.143 |     nan     |               nan     |     nan     |               nan     |
| ait_suricata | lepes4_kockazati+gep_csoportszint  |            60 |   0.982 | 0.751 |          1.000 |          44.000 |         0.078 |      79.000 |                 0.991 |       0.999 |                 0.101 |

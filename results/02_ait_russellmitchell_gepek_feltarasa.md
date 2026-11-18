# Gépek és a gépnyilvántartás lefedettsége – AIT-ADS, russellmitchell

Dolgozat: 5.4, 6.1, D25 · **a támadási címkéket ez a lépés nem használja** (6.3) · nyilvántartás: `config/elozetes_rogzites/ait_russellmitchell_gepfontossag.yaml`

## ait_wazuh

Riasztás: 23116 · azonosított érintett gép: 23116 (100.0%) · ismeretlen (semleges 0,5): 0

| erintett_gep    |   riasztas |   fokozat |    g |
|:----------------|-----------:|----------:|-----:|
| mail            |       8365 |         5 | 1.00 |
| intranet-server |       7656 |         4 | 0.75 |
| davey-mail      |       4694 |         2 | 0.25 |
| morris-mail     |       2321 |         2 | 0.25 |
| proxy-server    |         48 |         4 | 0.75 |
| cloud-share     |         11 |         5 | 1.00 |
| inet-firewall   |          5 |         4 | 0.75 |
| vpn             |          5 |         5 | 1.00 |
| internal-share  |          5 |         4 | 0.75 |
| webserver       |          5 |         5 | 1.00 |
| inet-dns        |          1 |         4 | 0.75 |

## ait_suricata

Riasztás: 9186 · azonosított érintett gép: 4176 (45.5%) · ismeretlen (semleges 0,5): 5010

| erintett_gep    |   riasztas |   fokozat |    g |
|:----------------|-----------:|----------:|-----:|
| (ismeretlen)    |       5010 |    nan    | 0.50 |
| vpn             |       1959 |      5.00 | 1.00 |
| webserver       |       1072 |      5.00 | 1.00 |
| mail            |       1039 |      5.00 | 1.00 |
| cloud-share     |         33 |      5.00 | 1.00 |
| intranet-server |         30 |      4.00 | 0.75 |
| internal-share  |         25 |      4.00 | 0.75 |
| inet-dns        |         12 |      4.00 | 0.75 |
| inet-firewall   |          6 |      4.00 | 0.75 |

Leggyakoribb IP-címek az azonosítatlan Suricata-riasztásokban:

| ip            |   előfordulás |
|:--------------|--------------:|
| 192.168.230.4 |          5010 |
| 13.107.21.200 |           108 |
| 52.223.40.198 |            84 |
| 13.107.42.14  |            84 |
| 23.47.209.148 |            76 |
| 91.189.88.142 |            71 |
| 13.107.213.44 |            60 |
| 91.189.88.152 |            54 |

# Az eredeti AIT-ADS formátum és az időszak-alapú címkék – russellmitchell

Dolgozat: 5.3, 6.1 · forrás: Zenodo 8263181 (`russellmitchell_wazuh.json`, `labels.csv`) és a CATS-változat (`ait_wazuh.jsonl`, `ait_suricata.jsonl`, commit 628cf48a)

## 1. Az eredeti fájl összetétele

| rekordfajta                 |   rekord |
|:----------------------------|---------:|
| wazuh                       |    23116 |
| suricata                    |     9186 |
| fast.log-másolat (kihagyva) |     9186 |

| napló (location)                         |   rekord |
|:-----------------------------------------|---------:|
| /var/log/suricata/eve.json               |     9186 |
| /var/log/suricata/fast.log               |     9186 |
| /var/log/apache2/intranet-access.log     |     7625 |
| /var/log/syslog                          |     5635 |
| /var/log/mail.log                        |     4844 |
| /var/log/mail.info                       |     4844 |
| /var/log/auth.log                        |       58 |
| /var/log/audit/audit.log                 |       24 |
| /var/log/apache2/proxy-error-error.log   |       24 |
| /var/log/apache2/proxy-access-access.log |       24 |
| /var/log/user.log                        |       15 |
| /var/log/horde/horde-access-access.log   |        9 |
| /var/log/apache2/intranet-error.log      |        8 |
| /var/log/apache2/other_vhosts_access.log |        6 |

A Suricata minden riasztása kétszer szerepel: szerkezetten (`eve.json`) és a Wazuh saját szabályával feldolgozott szöveges másolatként (`fast.log`). A másolatokat kihagyjuk.

## 2. Egyezés a CATS-változattal

- Egységesített riasztás: 32302 (Suricata 9186, Wazuh 23116); CATS-változat: 32302.
- Csak a CATS-ban: 0; csak az eredetiből: 0 (az illesztés kulcsa a Wazuh-kezelő rekordazonosítója).
- Mezőeltérés: {'hostname': 3}.

| rekord | mező | sajat | CATS | napló |
| --- | --- | --- | --- | --- |
| 1685988669.6810920 | hostname | davey-mail | mail | /var/log/horde/horde-access-access.log |
| 1685988669.6811460 | hostname | davey-mail | mail | /var/log/horde/horde-access-access.log |
| 1685988669.6812020 | hostname | davey-mail | mail | /var/log/horde/horde-access-access.log |

Az eltérés oka: a CATS a Horde-webmail néhány riasztását kézi, időpont- és IP-alapú szabállyal más géphez rendeli; az egységesítő forgatókönyvtől független szabályt használ (a naplósor gépneve, az Apache-napló helye, a Wazuh-ügynök IP-címe).

## 3. Időszak-alapú címke kontra a CATS riasztásonkénti címkéje

Időszak-alapú címke: támadás, ha a riasztás ideje a `labels.csv` valamelyik támadási időszakába esik (zárt időszak). A CATS címkéje az AIT-LDSv2 eseményszintű címkéiből jön (csak a russellmitchellre van ilyen).

| érzékelő   |   riasztás |   CATS: támadás |   időszak: támadás |   mindkettő |   csak időszak (zaj a támadás alatt) |   csak CATS (kimaradna) |   időszak-címke pontossága |   időszak-címke teljessége |
|:-----------|-----------:|----------------:|-------------------:|------------:|-------------------------------------:|------------------------:|---------------------------:|---------------------------:|
| suricata   |       9186 |              44 |                213 |          44 |                                  169 |                       0 |                      0.207 |                      1.000 |
| wazuh      |      23116 |            7661 |               8111 |        7661 |                                  450 |                       0 |                      0.945 |                      1.000 |

### Az időszak-címke többlete fázisonként és szabályonként

| sensor   | fazis         |   riasztás |
|:---------|:--------------|-----------:|
| suricata | cracking      |          1 |
| suricata | dnsteal       |        164 |
| suricata | webshell      |          2 |
| suricata | wpscan        |          2 |
| wazuh    | cracking      |          8 |
| wazuh    | dnsteal       |        383 |
| wazuh    | network_scans |          8 |
| wazuh    | service_scans |         51 |

| sensor   | hostname     | rule_name                                              |   riasztás |
|:---------|:-------------|:-------------------------------------------------------|-----------:|
| wazuh    | mail         | Dovecot Authentication Success.                        |        276 |
| suricata | nan          | SURICATA TLS invalid record/traffic                    |         84 |
| suricata | nan          | SURICATA TLS invalid handshake message                 |         82 |
| wazuh    | davey-mail   | Dovecot Authentication Success.                        |         69 |
| wazuh    | morris-mail  | Dovecot Authentication Success.                        |         30 |
| wazuh    | mail         | ClamAV database update                                 |         18 |
| wazuh    | proxy-server | Apache: Attempt to access forbidden file or directory. |         14 |
| wazuh    | proxy-server | Web server 400 error code.                             |         14 |
| wazuh    | cloud-share  | Web server 400 error code.                             |          5 |
| wazuh    | davey-mail   | Web server 400 error code.                             |          3 |
| wazuh    | davey-mail   | ClamAV database update                                 |          3 |
| wazuh    | mail         | Web server 400 error code.                             |          3 |

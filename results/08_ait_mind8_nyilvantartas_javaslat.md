# A 8 forgatókönyv gépnyilvántartása – JAVASLAT (címkék nélkül)

Dolgozat: 5.4, 6.1, 6.3 · D25, D27 · minta: `config/elozetes_rogzites/ait_russellmitchell_gepfontossag_v2.yaml`, `config/elozetes_rogzites/ait_russellmitchell_alkalmazhatosag.yaml`

## A levezetés szabályai

| # | Szabály | Mire |
| --- | --- | --- |
| G1 | A Wazuh-ügynök IP-címe a naplósor fejlécének gépnevéhez tartozik (D27); az Apache proxy-naplói a `proxy-server`; a `proxy-server` és a `webserver` ugyanazon a gépen, közös címen fut | megnevezett gépek |
| G2 | Gépnév nélküli ügynök: `cloud-access.log` vagy proxy-napló → `webserver` (+ `proxy-server`); `other_vhosts_access.log` → `cloud-share` | webszerver, felhős megosztás |
| G3 | Zónák: az internet a külső levelezők (`*-mail`, kivéve `mail`) /16-os tartománya, az intranet az `intranet-server` /16-os tartománya | zónák |
| G4 | Tűzfal: az a Suricata-érzékelő, amelynek riasztásai legalább 95%-ában ugyanaz az internetzónás cím szerepel; ez a cím a tűzfal külső címe (címfordítás, D25) | `inet-firewall` |
| G5 | A többi megnevezetlen érzékelő/ügynök, amelyből csak `audit.log` vagy semmilyen gépi riasztás nem jön: intranetzónában `internal-share`, máshol `vpn` | belső megosztás, VPN |
| G6 | Ha a gép saját Suricatájának riasztásaiban (legalább 10) a gép ügynökcíme nem szerepel, a gép címe kiegészül azzal a más géphez nem tartozó címmel, amely a riasztások legalább 95%-ában szerepel | a gép hálózaton látható címe |
| G7 | A nem internetzónás, `.1`-re végződő magáncímek (alhálózati átjárók) a tűzfaléi | `inet-firewall` |
| G8 | `inet-dns`: a megnevezett gép címe, és az internetzónás, `.254`-re végződő magáncím a Suricata-riasztásokban | globális DNS |
| G9 | Szerep, zóna, fokozat és szoftverkészlet a szerep szerint, a russellmitchell jóváhagyott értékeivel; a külső levelezők: internet, 1-es fokozat, `[linux, imap, smtp]` | minden gép |

## Ellenőrzés: russellmitchell

A szabályok **pontosan visszaadják** a jóváhagyott nyilvántartás gépeit és címeit.

## fox

| gép | IP-címek | szabály |
| --- | --- | --- |
| cloud-share | 172.17.129.140 | G1 |
| inet-dns | 192.168.255.254 | G8 |
| inet-firewall | 10.35.32.1, 192.168.128.4, 172.17.128.1 | G1, G4, G4 (külső cím), G7 |
| internal-share | 10.35.33.111 | G1 |
| intranet-server | 10.35.35.206 | G1 |
| jonesmorgan-mail | 192.168.131.228 | G1 |
| mail | 172.17.131.81 | G1 |
| miller-mail | 192.168.129.212 | G1 |
| proxy-server | 172.17.130.37 | G1, G2 (a webserver címe) |
| taylorcruz-mail | 192.168.128.170 | G1 |
| vpn | 172.17.130.196 | G1 |
| webserver | 172.17.130.37 | G1, G2 (a proxy-server címe) |
| whittaker-mail | 192.168.128.195 | G1 |


## harrison

| gép | IP-címek | szabály |
| --- | --- | --- |
| cloud-share | 10.237.0.4 | G2 |
| inet-dns | 172.28.255.254 | G8 |
| inet-firewall | 192.168.128.1, 172.28.192.4, 10.237.0.1 | G1, G4, G4 (külső cím), G7 |
| internal-share | 192.168.131.109 | G5 |
| intranet-server | 192.168.131.215 | G1 |
| mail | 10.237.2.255 | G1 |
| proxy-server | 10.237.0.166 | G1 |
| smith-mail | 172.28.192.7 | G1 |
| taylor-mail | 172.28.192.97 | G1 |
| vpn | 10.237.1.238 | G5 |
| webserver | 10.237.0.166 | G2 (a proxy-server címe) |


## santos

| gép | IP-címek | szabály |
| --- | --- | --- |
| cloud-share | 172.21.128.54 | G1 |
| hayes-mail | 10.229.2.25 | G1 |
| inet-dns | 10.229.255.254 | G1, G8 |
| inet-firewall | 10.229.0.4, 172.21.128.1, 192.168.104.1 | G4, G4 (külső cím), G7 |
| internal-share | 192.168.104.218 | G1 |
| intranet-server | 192.168.104.155 | G1 |
| mail | 172.21.131.50 | G1 |
| proxy-server | 172.21.129.224 | G2 (a webserver címe) |
| rogersturnbull-mail | 10.229.0.32 | G1 |
| vpn | 172.21.128.119 | G5 |
| webserver | 172.21.129.224 | G2, G2 (a proxy-server címe) |


## shaw

| gép | IP-címek | szabály |
| --- | --- | --- |
| butcherrowe-mail | 10.70.32.243 | G1 |
| cloud-share | 10.38.242.230, 172.24.249.212 | G2, G6 |
| collinsbecker-mail | 10.70.33.128 | G1 |
| inet-dns | 172.27.183.254, 10.70.63.254 | G1, G8 |
| inet-firewall | 172.27.180.4, 10.70.32.4, 172.24.248.1 | G4, G4 (külső cím), G7 |
| internal-share | 192.168.3.116, 192.168.188.120 | G5, G6 |
| intranet-server | 192.168.188.179 | G1 |
| mail | 10.38.242.195 | G1 |
| proxy-server | 10.38.243.24, 172.24.251.86 | G2 (a webserver címe), G6 |
| smith-mail | 10.70.34.215 | G1 |
| vpn | 172.24.249.224 | G5 |
| webserver | 10.38.243.24, 172.24.251.86 | G2, G2 (a proxy-server címe), G6 |


## wardbeck

| gép | IP-címek | szabály |
| --- | --- | --- |
| cloud-share | 10.132.56.204 | G2 |
| inet-dns | 192.168.127.254 | G8 |
| inet-firewall | 10.132.56.1, 192.168.96.4 | G4, G4 (külső cím), G7 |
| internal-share | 172.21.240.214 | G5 |
| intranet-server | 172.21.241.88 | G1 |
| mail | 10.132.56.171 | G1 |
| proxy-server | 10.132.57.136 | G2 (a webserver címe) |
| smith-mail | 192.168.99.0 | G1 |
| vpn | 10.132.56.81 | G5 |
| walker-mail | 192.168.98.239 | G1 |
| watkins-mail | 192.168.96.99 | G1 |
| webserver | 10.132.57.136 | G2, G2 (a proxy-server címe) |


## wheeler

| gép | IP-címek | szabály |
| --- | --- | --- |
| cloud-share | 10.38.242.230 | G1 |
| fischer-mail | 172.27.181.174 | G1 |
| inet-dns | 172.27.183.254 | G8 |
| inet-firewall | 172.27.180.4, 10.38.242.1, 192.168.0.1 | G1, G4, G4 (külső cím), G7 |
| internal-share | 192.168.3.116 | G1 |
| intranet-server | 192.168.2.114 | G1 |
| khanwood-mail | 172.27.182.4 | G1 |
| mail | 10.38.242.195 | G1 |
| proxy-server | 10.38.243.24 | G1, G2 (a webserver címe) |
| sanchez-mail | 172.27.183.191 | G1 |
| vpn | 10.38.243.125 | G5 |
| webserver | 10.38.243.24 | G1, G2 (a proxy-server címe) |
| williams-mail | 172.27.181.253 | G1 |


## wilson

| gép | IP-címek | szabály |
| --- | --- | --- |
| cloud-share | 10.182.194.196 | G1 |
| inet-dns | 192.168.239.254 | G1, G8 |
| inet-firewall | 10.182.192.1, 192.168.224.4 | G1, G4, G4 (külső cím), G7 |
| internal-share | 172.26.240.200 | G1 |
| intranet-server | 172.26.243.167 | G1 |
| lane-mail | 192.168.226.198 | G1 |
| mail | 10.182.193.181 | G1 |
| proxy-server | 10.182.194.5 | G1, G2 (a webserver címe) |
| vpn | 10.182.193.78 | G1 |
| webserver | 10.182.194.5 | G1, G2 (a proxy-server címe) |
| wilsonahmed-mail | 192.168.224.185 | G1 |


## Az új szabályazonosítók szolgáltatása

A russellmitchellben nem fordultak elő; a megfeleltetés elve azonos (a Suricata protokoll-dekóder jelzése a protokoll szolgáltatása; domain-, TLD-, „hunting” és információs jelzés: `altalanos`).

| érzékelő | szabály | név | szolgáltatás |
| --- | --- | --- | --- |
| wazuh | 31509 | CMS (WordPress or Joomla) login attempt | web |
| wazuh | 31510 | CMS (WordPress or Joomla) brute force attempt | web |
| wazuh | 5403 | First time user executed sudo | linux |
| wazuh | 5551 | PAM: Multiple failed logins in a small period of time | linux |
| suricata | 2001569 | ET SCAN Behavioral Unusual Port 445 traffic | smb |
| suricata | 2029340 | ET INFO TLS Handshake Failure | tls |
| suricata | 2230027 | SURICATA TLS certificate invalid der | tls |
| suricata | 2240001 | SURICATA DNS Unsolicited response | dns |
| suricata | 2011802 | ET DNS DNS Lookup for localhost.DOMAIN.TLD | altalanos |
| suricata | 2014169 | ET DNS Query for .su TLD | altalanos |
| suricata | 2016778 | ET DNS Query to a *.pw domain | altalanos |
| suricata | 2025105 | ET INFO DNS Query for Suspicious .ga Domain | altalanos |
| suricata | 2025109 | ET INFO Suspicious Domain (*.ga) in TLS SNI | altalanos |
| suricata | 2027757 | ET DNS Query for .to TLD | altalanos |
| suricata | 2027758 | ET DNS Query for .cc TLD | altalanos |
| suricata | 2029706 | ET HUNTING Possible COVID-19 Domain in SSL Certificate M2 | altalanos |
| suricata | 2029707 | ET HUNTING Suspicious TLS SNI Request for Possible COVID-19 Domain M1 | altalanos |
| suricata | 2029709 | ET HUNTING Suspicious Domain Request for Possible COVID-19 Domain M1 | altalanos |
| suricata | 2016149 | ET INFO STUN Binding Request | altalanos |
| suricata | 2016150 | ET INFO STUN Binding Response | altalanos |

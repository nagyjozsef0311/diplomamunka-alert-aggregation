# 2. feltárás – a gépek és IP-címek az AIT-ADS russellmitchell forgatókönyvében

Készült: 2026-11-17 · adat: CATS-változat · **a címkéket ebben a lépésben szándékosan nem néztük**
(a gépek fontossági fokozatát a szerző a mérés előtt, a címkék ismerete nélkül rögzíti – D21, 6.3).

## Gépek a Wazuh-riasztásokban (gépnév → a Wazuh-ügynök IP-címe)

| Gépnév | Riasztás | IP-cím | Valószínű szerep (a névből) | Hálózat |
| --- | ---: | --- | --- | --- |
| mail | 8365 | 172.19.130.4 | levelező kiszolgáló | 172.19.x |
| intranet-server | 7656 | 10.143.2.4 | belső webkiszolgáló (intranet) | 10.143.x |
| davey-mail | 4694 | 192.168.231.56 | felhasználói gép (levelezőklienssel) | 192.168.231.x |
| morris-mail | 2321 | 192.168.231.164 | felhasználói gép (levelezőklienssel) | 192.168.231.x |
| proxy-server | 48 | 172.19.130.68 | proxy | 172.19.x |
| webserver | 5 | 172.19.130.68 | webkiszolgáló | 172.19.x |
| cloud-share | 11 | 172.19.130.106 | felhős fájlmegosztás | 172.19.x |
| internal-share | 5 | 10.143.0.103 | belső fájlmegosztás | 10.143.x |
| vpn | 5 | 172.19.131.174 | VPN-átjáró | 172.19.x |
| inet-firewall | 5 | 172.19.128.1 | határtűzfal | 172.19.x |
| inet-dns | 1 | 192.168.231.254 | DNS | 192.168.231.x |

## Suricata

- A Suricata-riasztásokban nincs gépnév, csak forrás- és cél-IP. A leggyakoribb belső címek:
  192.168.230.4 (2601 forrás / 2421 cél), 172.19.130.68, 172.19.130.4, 172.19.131.174 – az utóbbi
  három a fenti táblázat szerint a proxy/webkiszolgáló, a levelező és a VPN.
- A Suricata több gépen futott (a Wazuh-ügynök IP-je szerint: 172.19.128.1, 172.19.130.68,
  172.19.131.174, 172.19.130.106, 10.143.2.4, 10.143.0.103, 172.19.130.4).

## Nyitott kérdések a gépnyilvántartáshoz

1. **172.19.130.68 két néven is szerepel** (proxy-server és webserver): egy gép két szereppel, vagy
   címkiosztási sajátosság? A gépnyilvántartásban egy IP-címhez egy gép kell.
2. **192.168.230.4 nincs a Wazuh-gépek között**, mégis a leggyakoribb Suricata-cím: valószínűleg a
   tűzfal külső oldala vagy címfordítás (NAT). Az AIT-LDSv2 hálózatleírásából kell tisztázni.
3. A hálózati zónák (172.19.x, 10.143.x, 192.168.230–231.x) jelentését az AIT-LDSv2 leírása adja meg;
   a fenti „Hálózat” oszlop csak a címtartomány.

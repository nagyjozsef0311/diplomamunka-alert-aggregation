# AIT-ADS munkaterv – összefoglaló

A részletes, szerkeszthető munkaterv a Claude-projektben van („AIT-ADS munkaterv”); ez a fájl a
tárolóban követhető kivonata. Cél: **december első hetére** mérhető eredmény arról, mennyit javít a
riasztások rangsorán a gépek fontossága és a sérülékenységi információ a kockázatalapú
pontozáshoz képest.

## Hetek

| Hét | Feladat | Akkor kész, ha |
| --- | --- | --- |
| 1. (okt. 5–11) | Projekt, letöltés, ismerkedés az adattal | Minden használt mező jelentése ismert |
| 2. (okt. 12–18) | Egységesítő agent | A CATS-adatból és az eredetiből ugyanazokat a riasztásokat kapjuk |
| 3. (okt. 19–25) | Összehasonlítási alapok (súlyosság, CATS) a russellmitchell forgatókönyvön | A cikk számai kb. ±0,02-en belül visszajönnek |
| 4. (okt. 26–nov. 1) | Gépnyilvántartás a russellmitchell forgatókönyvhöz | Minden riasztás célpontja géphez köthető |
| 5. (nov. 2–8) | Környezet- és sérülékenységi agent | Minden riasztásnál van érték vagy dokumentált „ismeretlen” |
| 6. (nov. 9–15) | Rangsoroló agent, súlyok páros összehasonlítással | Az első teljes eredménytáblázat kész |
| 7. (nov. 16–22) | Csoportosító agent, csoport-tisztaság | Ismert a csökkenés és az átcsúszó támadások aránya |
| 8. (nov. 23–29) | Mind a 8 forgatókönyv, érzékenységvizsgálat, adatból tanult súlyok | Minden mérés egy paranccsal megismételhető |
| 9. (nov. 30–dec. 6) | Összegzés, tartalék, anyag a konzulensnek | Az értékelési fejezet első vázlata kész |

## Első adatfeltárás (2026-10-01, CATS-változat, russellmitchell forgatókönyv)

| | Wazuh | Suricata |
| --- | --- | --- |
| Riasztások száma | 23 116 | 9 186 |
| Ebből támadáshoz tartozik | 7 661 (33%) | 44 (0,5%) |
| Különböző szabályok | 20 | 13 |
| Gépnév a riasztásban | van (pl. `intranet-server`, `mail`, `proxy-server`) | nincs – IP-cím alapján kell illeszteni |
| Sérülékenység-azonosítóra (CVE) hivatkozó riasztás | 0 | 0 |

**Következmény:** a „működhet-e a támadás ezen a gépen” mérőszám az AIT-ADS-en nem CVE-egyezéssel,
hanem durvább, szolgáltatás- és termékszintű illesztéssel számolható (pl. webes támadás WordPresst
futtató gépre). A CVE-szintű illesztést a laborban, célzott Suricata-szabályokkal vizsgáljuk.

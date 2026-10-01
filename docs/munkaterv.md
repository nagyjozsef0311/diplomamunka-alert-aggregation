# Munkaterv – összefoglaló

**2026-10-01 óta érvényes: a D13 szerinti ütemezés** (lent, első táblázat). A Diplomamunka II.
leadásáig (2026. december, a szorgalmi időszak utolsó napja) az írás az elsődleges, a kód addig
megy, amíg a beszámolóba érdemi „első eredményt” ad. Követelmények: `docs/diplomamunka-2.md`.

## Ütemezés a Diplomamunka II. leadásáig (D13)

Heti kb. 8–10 órával számolva, ennek kb. fele írás, fele kód. A fejezetszámok a
`docs/diplomamunka-2.md` vázlatára utalnak.

| Hét | Írás (`thesis/`) | Kód | Akkor kész, ha |
| --- | --- | --- | --- |
| 1. (okt. 5–11) | LaTeX-váz a kari sablonból; 1. fejezet vázlata | Környezet, letöltés, adatfeltárás | A PDF lefordul; minden használt mező jelentése ismert |
| 2. (okt. 12–18) | 2. fejezet (IDS, SOC, riasztási fáradtság) | Egységesítő agent | A CATS-adatból és az eredetiből ugyanazok a riasztások jönnek ki |
| 3. (okt. 19–25) | 2. fejezet kész; 3. fejezet eleje | Összehasonlítási alapok: súlyosság szerinti rangsor és a CATS visszamérése (russellmitchell) | A cikk számai kb. ±0,02-en belül visszajönnek |
| 4. (okt. 26–nov. 1) | 3. fejezet: módszerek, összehasonlító táblázat | Gépnyilvántartás a russellmitchell forgatókönyvhöz | Minden riasztás célpontja géphez köthető |
| 5. (nov. 2–8) | 3. fejezet kész | Környezet- és sérülékenységi agent (egyszerű változat) | Minden riasztásnál van érték vagy dokumentált „ismeretlen” |
| 6. (nov. 9–15) | 4. fejezet: mérőszámrendszer és agent-modell | Rangsoroló agent; a szakértői súlyok rögzítése páros összehasonlítással | A súlyok dátummal elmentve, a következetességi arány 0,1 alatt |
| 7. (nov. 16–22) | 5. és 6. fejezet: felépítés, eszközválasztás, tesztkörnyezet | Első eredménytáblázat egy forgatókönyvre (3–5. lépcső) | Rangsor-pontosság és átlagos pontosság minden lépcsőhöz |
| 8. (nov. 23–29) | 7. és 8. fejezet: értékelési módszertan, első eredmények, ütemterv a III. félévre | Ábrák a beszámolóhoz | Megvan a teljes, legalább 30 oldalas vázlat |
| 9. (nov. 30–dec. 6) | A teljes vázlat a konzulensnek; javítások | Tartalék | A konzulens visszajelzett |
| 10. (dec. 7–a leadás napja) | Végleges beszámoló; feladatlap PDF-ben; aláírt konzultációs napló; zip a megadott nevekkel | – | Feltöltve a Moodle-be |
| Vizsgaidőszak (2027. jan.) | 8 perces előadás, diasor, próbaelőadás | – | Megtartva a bizottság előtt |

**A Diplomamunka III.-ra (2027. jan.–máj. 15.) marad:** csoportosító agent; mind a 8 forgatókönyv;
érzékenységvizsgálat és adatból tanult súlyok; LangGraph-vezérlés és magyarázó agent; a labor;
az eredmény- és értékelési fejezetek. Leadás: 2027. május 15., 16:00.

## Az eredeti, 9 hetes AIT-ADS terv (D7, 2026-10-01; a D13 felváltja)


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

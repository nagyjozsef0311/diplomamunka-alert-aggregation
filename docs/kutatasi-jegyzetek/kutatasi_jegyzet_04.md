# Kutatási jegyzet #4 – Kontextus-reprezentáció (K2)
2026-09-21 · Források: Uetz 2026, Eckhoff 2025, Kruegel 2004, Njogu 2012, Sommestad & Franke 2015, SEPSES 2019, AIT-LDSv2

## 1. A legfontosabb új forrás a dolgozat pozicionálásához
**Uetz et al. (2026, Fraunhofer FKIE): „Can Risk-Based Alerting Mitigate Cybersecurity Alert Fatigue?”**
- Ez a risk-based alerting (RBA) első szisztematikus értékelése.
- Öt kockázati hipotézist vizsgál: súlyosság, halmozódás, változatosság, ritkaság, periodicitás.
- Nyílt eszközzel dolgozik (CATS), 8 adathalmazon, köztük az AIT-ADS Wazuh- és Suricata-riasztásain.
- Eredmények:
  - a kombinált modell átlagos AUROC értéke 0,92, szemben a csak súlyosság szerinti 0,72-vel;
  - a ritkaság és a periodicitás önmagában **nem jobb a véletlennél**.
- **A cikk kifejezetten kizárja az eszköz-kontextust** (üzleti kritikalitás, sérülékenység), mert az „nem összevethető”.

**Ezért a dolgozat hozzájárulása pontosan megfogalmazható:** az RBA-baseline-ra (CATS) ráépített **eszköz-, sérülékenységi és lefedettségi metrikák mennyivel javítanak** az AIT-ADS-en és a homelabon. Ez egy tiszta, mérhető és újszerű kutatási kérdés (K1 + K5).

## 2. A kontextus-reprezentáció lehetséges módjai

| Megközelítés | Előny | Hátrány | Forrás |
|---|---|---|---|
| **Relációs CMDB (SQL)** | Egyszerű, gyors, jól illeszthető a Wazuh inventoryhoz | Gyenge többlépéses kapcsolat-lekérdezésben | Anuar 2012, Njogu 2012 |
| Tudásgráf (Neo4j / RDF) | CVE–CWE–CPE–ATT&CK láncok bejárhatók | Több munka, túlzás lehet egy protot. | SEPSES 2019, Sikos 2023, Shi 2024 |
| Riasztás-gráf (pivot IP/user) | Aggregációhoz kiváló | Nem eszköz-kontextus | Eckhoff 2025 |
| Szabványos séma (OCSF, STIX 2.1) | Interoperábilis | Nagy, bonyolult | ellenőrizendő (nem akadémiai) |

**Javaslat:** relációs CMDB (PostgreSQL vagy SQLite) a CPE mint illesztési kulcs köré. A riasztás-csoportosításhoz Eckhoff-féle pivot-gráf. A tudásgráf a „továbbfejlesztési lehetőségek” közé kerül.

## 3. Javasolt minimális CMDB-séma

```
asset(asset_id, hostname, ip[], zone{internet|dmz|intranet},
      role, criticality 1–5, conf, integ, avail {L|M|H},
      replaceability 1–5, os_cpe)
service(asset_id, port, proto, product, version, cpe)
vulnerability(asset_id, cve, cvss_base, epss?, kev?, source='wazuh_vd'|'manual', first_seen)
coverage(asset_id, wazuh_agent_active bool, suricata_segment_visible bool, last_seen)
signature_ref(sig_id, source{suricata|wazuh}, cve[], attack_technique[])
```

- **A V2 (alkalmazhatóság) számítása:** riasztás cél-IP → `asset` → `service` (port) → a riasztás CVE-referenciája (Suricata `reference:cve,...`) ∩ `vulnerability.cve`.
  - Találat esetén 1.
  - Ha csak a szolgáltatás vagy a termék egyezik: 0,5.
  - Egyébként 0.
  - Ez a Kruegel/Vigna-féle alert verification és a Njogu 2012 egyszerűsített változata.
- **Figyelem:** Sommestad & Franke (2015) szerint a kontextus-szűrés korlátozottan hatékony, ha a sérülékenységi adat hiányos. A V2 ezért **ne szűrjön, csak súlyozzon**, mert a téves negatívok (FNR) kockázata nagyobb.

## 4. Kontextus rekonstruálása az AIT-ADS-hez (AIT-LDSv2 alapján, ellenőrizve)
- **Zónák:**
  - intranet: felhasználói gépek, intranet szerver (WordPress 5.8.2), Samba 4.5.9 fájlmegosztó;
  - DMZ: OpenVPN 2.4.4, proxy, Horde 5.2.17 levelező, OwnCloud 10.5.0;
  - internet: DNS, külső levelezők, támadó.
- **Kihasznált sérülékenység:** wpDiscuz plugin, **CVE-2020-24186** (korlátlan fájlfeltöltés → webshell).
- **IP-címek:** szcenáriónként a „facts” gyűjtésből; az AIT-LDSv2 repóból kinyerhetők.
- **A CMDB így kézzel felépíthető:**
  - kb. 15–40 eszköz szcenáriónként;
  - a kritikalitást a szerepkör adja: intranet szerver és fájlmegosztó = 5, levelező = 4, felhasználói gép = 2;
  - a sérülékenységek az ismert verziókból NVD-lekérdezéssel állíthatók elő.

## 5. Frissített baseline-sor (az ablációhoz)

| Változat | Leírás |
|---|---|
| B0 | Nyers riasztások |
| B1 | Csak súlyosság szerinti rangsor |
| B2 | Time-delta csoportosítás (Landauer 2022) / Eckhoff-féle gráf-csoportosítás |
| **B3** | **RBA (Uetz 2026, CATS): súlyosság + halmozódás + változatosság** |
| M1 | B3 + eszközmetrikák (S1–S4) |
| M2 | M1 + sérülékenység (V1–V2) |
| M3 | M2 + lefedettség (C1) = teljes modell, AHP-súlyokkal |

Mérőszámok:
- AUROC, Average Precision, Precision a felső 10%-ban (Uetz 2026);
- ARR/QRR és FNR (Ndichu 2026);
- csoport-tisztaság (Eckhoff 2025).

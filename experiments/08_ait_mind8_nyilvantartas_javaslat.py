#!/usr/bin/env python3
"""A 7 új AIT-ADS forgatókönyv gépnyilvántartásának és szoftverkészletének JAVASLATA (címkék nélkül).

Dolgozat: 5.4 (gépnyilvántartás), 6.1, 6.3 (előzetes rögzítés), D25, D27. A gépek szerepe, zónája,
fokozata és szoftverkészlete a russellmitchellre jóváhagyott nyilvántartással AZONOS szabályokból jön;
csak a gépnevek és az IP-címek forgatókönyvfüggők. Az AIT-LDSv2 forgatókönyvenkénti „facts” adatai
ebből a környezetből nem érhetők el, ezért a címeket a riasztások szerkezetéből vezetjük le, rögzített
szabályokkal (lásd ``SZABALYOK``). A TÁMADÁSI CÍMKÉKET (labels.csv) A SZKRIPT NEM OLVASSA.

Ellenőrzés: a szabályoknak a russellmitchellen vissza kell adniuk a jóváhagyott nyilvántartás
(``ait_russellmitchell_gepfontossag_v2.yaml``) IP-címeit.

Futtatás:
    python experiments/08_ait_mind8_nyilvantartas_javaslat.py            # csak a javaslat (results/)
    python experiments/08_ait_mind8_nyilvantartas_javaslat.py --rogzites # JÓVÁHAGYÁS UTÁN: YAML-ok
                                                                         # a config/elozetes_rogzites/-be
Eredmény: results/08_ait_mind8_nyilvantartas_javaslat.md
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import pandas as pd
import yaml

from alertagg.egysegesito import AIT_FORGATOKONYVEK, load_ait_wazuh_json

ROOT = Path(__file__).resolve().parents[1]
AIT = ROOT / "data" / "ait_ads"
CFG = ROOT / "config" / "elozetes_rogzites"
RM_GEPEK = CFG / "ait_russellmitchell_gepfontossag_v2.yaml"
RM_ALK = CFG / "ait_russellmitchell_alkalmazhatosag.yaml"
NEV = "08_ait_mind8_nyilvantartas_javaslat"
KI_MD = ROOT / "results" / f"{NEV}.md"
UJ = [f for f in AIT_FORGATOKONYVEK if f != "russellmitchell"]

SZABALYOK = """\
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
"""

# A russellmitchell jóváhagyott szerepei (gepfontossag_v2) – a külső levelezők sablonja külön.
KULSO_LEVELEZO = {"zona": "internet", "szerep": "külső levelezőkiszolgáló", "fokozat": 1}

# Az új szabályazonosítók szolgáltatása (a russellmitchellben nem fordultak elő). Elv, a russellmitchell
# megfeleltetésével azonosan: a Suricata protokoll-dekóder jelzése (SURICATA <protokoll> …) a protokoll
# szolgáltatása; a domain- és TLD-alapú figyelmeztetés, a „hunting” és az információs jelzés
# „altalanos”; a webes CMS-bejelentkezés „web”; a PAM/sudo „linux”; a 445-ös port „smb”.
UJ_SZABALYOK = {
    "wazuh": {
        "31509": ("web", "CMS (WordPress or Joomla) login attempt"),
        "31510": ("web", "CMS (WordPress or Joomla) brute force attempt"),
        "5403": ("linux", "First time user executed sudo"),
        "5551": ("linux", "PAM: Multiple failed logins in a small period of time"),
    },
    "suricata": {
        "2001569": ("smb", "ET SCAN Behavioral Unusual Port 445 traffic"),
        "2029340": ("tls", "ET INFO TLS Handshake Failure"),
        "2230027": ("tls", "SURICATA TLS certificate invalid der"),
        "2240001": ("dns", "SURICATA DNS Unsolicited response"),
        "2011802": ("altalanos", "ET DNS DNS Lookup for localhost.DOMAIN.TLD"),
        "2014169": ("altalanos", "ET DNS Query for .su TLD"),
        "2016778": ("altalanos", "ET DNS Query to a *.pw domain"),
        "2025105": ("altalanos", "ET INFO DNS Query for Suspicious .ga Domain"),
        "2025109": ("altalanos", "ET INFO Suspicious Domain (*.ga) in TLS SNI"),
        "2027757": ("altalanos", "ET DNS Query for .to TLD"),
        "2027758": ("altalanos", "ET DNS Query for .cc TLD"),
        "2029706": ("altalanos", "ET HUNTING Possible COVID-19 Domain in SSL Certificate M2"),
        "2029707": ("altalanos", "ET HUNTING Suspicious TLS SNI Request for Possible COVID-19 Domain M1"),
        "2029709": ("altalanos", "ET HUNTING Suspicious Domain Request for Possible COVID-19 Domain M1"),
        "2016149": ("altalanos", "ET INFO STUN Binding Request"),
        "2016150": ("altalanos", "ET INFO STUN Binding Response"),
    },
}


def _p16(ip: str) -> str:
    return ".".join(ip.split(".")[:2])


def _privat(ip: str) -> bool:
    a, b = (int(x) for x in ip.split(".")[:2])
    return a == 10 or (a == 172 and 16 <= b <= 31) or (a == 192 and b == 168)


def levezetes(forgatokonyv: str) -> tuple[dict[str, dict], list[str]]:
    """A gépek (név → {ip: [...], bizonyíték: [...]}) és a megjegyzések egy forgatókönyvre."""
    df = load_ait_wazuh_json(AIT / f"{forgatokonyv}_wazuh.json", forgatokonyv)
    df["ugynok"] = df["raw"].map(lambda r: r["ugynok_ip"])
    df["naplo"] = df["raw"].map(lambda r: (r["features"].get("event_source") or "").split("/")[-1])
    w, s = df[df.sensor == "wazuh"], df[df.sensor == "suricata"]
    gepek: dict[str, dict] = {}
    megj: list[str] = []

    def add(nev: str, ip: str | None, biz: str) -> None:
        g = gepek.setdefault(nev, {"ip": [], "bizonyitek": []})
        if ip and ip not in g["ip"]:
            g["ip"].append(ip)
        if biz not in g["bizonyitek"]:
            g["bizonyitek"].append(biz)

    # G1 – megnevezett gépek
    for (ip, host), _ in w.groupby(["ugynok", "hostname"]):
        add(host, ip, "G1")
    megnevezett_ugynok = set(w.dropna(subset=["hostname"])["ugynok"])
    # G3 – zónák
    kulso = [n for n in gepek if n.endswith("-mail") and n != "mail"]
    inet = {_p16(ip) for n in kulso for ip in gepek[n]["ip"]}
    intra = {_p16(ip) for ip in gepek.get("intranet-server", {}).get("ip", [])}
    # érzékelőnként: a riasztások legalább 95%-ában szereplő cím(ek)
    allando: dict[str, list[str]] = {}
    for ip, g in s.groupby("ugynok"):
        if len(g) < 10:
            continue
        c = Counter()
        for a, b in zip(g["src_ip"], g["dst_ip"], strict=True):
            for x in {a, b} - {None}:
                c[x] += 1
        allando[ip] = [x for x, n in c.items() if n >= 0.95 * len(g)]
    # G4 – tűzfal
    for ip, cimek in allando.items():
        kulso_cim = [x for x in cimek if _privat(x) and _p16(x) in inet]
        if kulso_cim:
            add("inet-firewall", ip, "G4")
            for x in kulso_cim:
                add("inet-firewall", x, "G4 (külső cím)")
    tuzfal_ip = set(gepek.get("inet-firewall", {}).get("ip", []))
    # G2, G5 – megnevezetlen ügynökök és érzékelők
    jeloltek = (set(w["ugynok"]) | set(s["ugynok"])) - megnevezett_ugynok - tuzfal_ip
    for ip in sorted(jeloltek - {None}):
        naplok = set(w.loc[w.ugynok == ip, "naplo"])
        if naplok & {"cloud-access.log", "proxy-access-access.log", "proxy-error-error.log"}:
            add("webserver", ip, "G2")
        elif "other_vhosts_access.log" in naplok:
            add("cloud-share", ip, "G2")
        elif naplok <= {"audit.log"}:
            nev = "internal-share" if _p16(ip) in intra else "vpn"
            add(nev, ip, "G5")
        else:
            megj.append(f"Besorolatlan ügynök/érzékelő: {ip} (naplók: {sorted(naplok)})")
    # a proxy-server és a webserver ugyanazon a gépen, közös címen fut (G1/G2)
    for a, b in (("webserver", "proxy-server"), ("proxy-server", "webserver")):
        if a in gepek:
            for ip in list(gepek[a]["ip"]):
                add(b, ip, f"G2 (a {a} címe)")
    # G6 – a gép hálózaton látható címe, ha a saját Suricatája az ügynök címét nem látja
    foglalt = {ip for g in gepek.values() for ip in g["ip"]}
    for nev, g in list(gepek.items()):
        if nev == "inet-firewall":
            continue
        for ip in list(g["ip"]):
            cimek = allando.get(ip, [])
            if ip in cimek:
                continue
            for x in cimek:
                if x not in foglalt and _privat(x) and _p16(x) not in inet:
                    add(nev, x, "G6")
                    if nev in ("webserver", "proxy-server"):
                        add("proxy-server" if nev == "webserver" else "webserver", x, "G6")
    # G7, G8 – átjárók és globális DNS
    minden_cim = {x for x in pd.concat([s["src_ip"], s["dst_ip"]]).dropna().unique() if _privat(x)}
    for x in sorted(minden_cim):
        if x.endswith(".1") and _p16(x) not in inet:
            add("inet-firewall", x, "G7")
        if x.endswith(".254") and _p16(x) in inet:
            add("inet-dns", x, "G8")
    for kotelezo in ["mail", "intranet-server", "internal-share", "vpn", "webserver", "cloud-share",
                     "inet-firewall", "inet-dns"]:
        if kotelezo not in gepek:
            megj.append(f"Nem azonosítható: {kotelezo}")
    return gepek, megj


def nyilvantartas(forgatokonyv: str, gepek: dict[str, dict]) -> tuple[dict, dict]:
    """A gépfontossági és az alkalmazhatósági YAML tartalma (G9)."""
    rm = yaml.safe_load(RM_GEPEK.read_text(encoding="utf-8"))
    rm_alk = yaml.safe_load(RM_ALK.read_text(encoding="utf-8"))
    szerep = {g["nev"]: g for g in rm["gepek"]}
    sorrend = [g["nev"] for g in rm["gepek"] if not (g["nev"].endswith("-mail") and g["nev"] != "mail")]
    lista, keszlet = [], {}
    for nev in sorrend + sorted(n for n in gepek if n not in sorrend):
        if nev not in gepek:
            continue
        minta = szerep.get(nev, KULSO_LEVELEZO)
        lista.append({"nev": nev, "ip": gepek[nev]["ip"], "zona": minta["zona"],
                      "szerep": minta["szerep"], "fokozat": minta["fokozat"]})
        keszlet[nev] = rm_alk["szoftverkeszlet"].get(nev, ["linux", "imap", "smtp"])
    szabalyok = {f: dict(rm_alk["szabalyok"][f]) for f in ("wazuh", "suricata")}
    for f, uj in UJ_SZABALYOK.items():
        for sid, (sz, _) in uj.items():
            szabalyok[f].setdefault(sid, sz)
    gep_cfg = {"forgatokonyv": forgatokonyv, "jovahagyta": None, "jovahagyas_datuma": None,
               "szabalyok": "results/08_ait_mind8_nyilvantartas_javaslat.md (G1–G9)",
               "minta": str(RM_GEPEK.relative_to(ROOT)), "gepek": lista, "kozos_ip_szabaly": "max"}
    alk_cfg = {"forgatokonyv": forgatokonyv, "allapot": "javaslat", "jovahagyta": None,
               "jovahagyas_datuma": None, "minta": str(RM_ALK.relative_to(ROOT)),
               "szoftverkeszlet": keszlet, "szabalyok": szabalyok}
    return gep_cfg, alk_cfg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rogzites", action="store_true",
                    help="JÓVÁHAGYÁS UTÁN: a YAML-ok kiírása a config/elozetes_rogzites/-be")
    ap.add_argument("--jovahagyas-datuma")
    args = ap.parse_args()

    sorok = ["# A 8 forgatókönyv gépnyilvántartása – JAVASLAT (címkék nélkül)", "",
             ("Dolgozat: 5.4, 6.1, 6.3 · D25, D27 · minta: "
             f"`{RM_GEPEK.relative_to(ROOT)}`, `{RM_ALK.relative_to(ROOT)}`"), "",
             "## A levezetés szabályai", "", SZABALYOK]

    # ellenőrzés a russellmitchellen
    rm_gepek, rm_megj = levezetes("russellmitchell")
    rm = {g["nev"]: set(g["ip"]) for g in yaml.safe_load(RM_GEPEK.read_text())["gepek"]}
    elt = {n: (sorted(rm.get(n, set())), sorted(rm_gepek.get(n, {}).get("ip", [])))
           for n in set(rm) | set(rm_gepek)
           if rm.get(n, set()) != set(rm_gepek.get(n, {}).get("ip", []))}
    sorok += ["## Ellenőrzés: russellmitchell", "",
              ("A szabályok **pontosan visszaadják** a jóváhagyott nyilvántartás gépeit és címeit."
               if not elt else f"Eltérés a jóváhagyott nyilvántartástól (jóváhagyott, levezetett): {elt}"),
              ""] + [f"- {m}" for m in rm_megj]

    osszes = {}
    for f in UJ:
        gepek, megj = levezetes(f)
        osszes[f] = gepek
        sorok += [f"## {f}", "", "| gép | IP-címek | szabály |", "| --- | --- | --- |"]
        for nev in sorted(gepek):
            sorok.append(f"| {nev} | {', '.join(gepek[nev]['ip'])} | "
                         f"{', '.join(gepek[nev]['bizonyitek'])} |")
        sorok += [""] + [f"- **{m}**" for m in megj] + [""]

    sorok += ["## Az új szabályazonosítók szolgáltatása", "",
              ("A russellmitchellben nem fordultak elő; a megfeleltetés elve azonos (a Suricata "
              "protokoll-dekóder jelzése a protokoll szolgáltatása; domain-, TLD-, „hunting” és "
              "információs jelzés: `altalanos`)."), "", "| érzékelő | szabály | név | szolgáltatás |",
              "| --- | --- | --- | --- |"]
    for f, uj in UJ_SZABALYOK.items():
        sorok += [f"| {f} | {sid} | {n} | {sz} |" for sid, (sz, n) in uj.items()]
    sorok.append("")
    KI_MD.write_text("\n".join(sorok), encoding="utf-8")
    print("\n".join(sorok))

    if args.rogzites:
        if not args.jovahagyas_datuma:
            raise SystemExit("A rögzítéshez add meg a --jovahagyas-datuma értékét.")
        for f, gepek in osszes.items():
            gep_cfg, alk_cfg = nyilvantartas(f, gepek)
            for c in (gep_cfg, alk_cfg):
                c["jovahagyta"], c["jovahagyas_datuma"] = "szerző", args.jovahagyas_datuma
            alk_cfg["allapot"] = "jovahagyva"
            fej = (f"# ELŐZETES RÖGZÍTÉS – AIT-ADS {f}. Levezetve: experiments/{NEV}.py (G1–G9),\n"
                   "# a russellmitchell jóváhagyott szabályaival; A TÁMADÁSI CÍMKÉKET NEM NÉZTÜK (6.3).\n")
            for nev, c in ((f"ait_{f}_gepfontossag.yaml", gep_cfg),
                           (f"ait_{f}_alkalmazhatosag.yaml", alk_cfg)):
                (CFG / nev).write_text(fej + yaml.safe_dump(c, allow_unicode=True, sort_keys=False),
                                       encoding="utf-8")
        print(f"[rögzítve] {len(osszes)} forgatókönyv -> {CFG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

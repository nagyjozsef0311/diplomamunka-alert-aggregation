"""Gépnyilvántartás: a környezeti információ relációs tárolója (5. fejezet, 5.4; 5.2. ábra).

Öt tábla, a dolgozat adatmodellje szerint:

* ``gep``                – név, IP-cím(ek), zóna, szerep, fontossági fokozat (1–5)
* ``megfigyeltseg``      – fut-e gépi érzékelő a gépen, látja-e a hálózati érzékelő
* ``szoftver``           – a gépen futó termékek szabványos szoftverazonosítóval (CPE)
* ``serulekenyseg``      – ismert sérülékenységek (CVE) és az érintett szoftverazonosítók
* ``szabaly_hivatkozas`` – melyik érzékelőszabály melyik sérülékenységre vagy termékre vonatkozik

A tárolás SQLite (D12, 5.5): egyetlen fájl vagy memóriabeli adatbázis. A gépek és fokozataik az
előzetesen rögzített YAML-fájlból töltődnek be (``config/elozetes_rogzites/``).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml

SEMA = """
CREATE TABLE gep (
    nev TEXT PRIMARY KEY,
    zona TEXT,
    szerep TEXT,
    fokozat INTEGER NOT NULL CHECK (fokozat BETWEEN 1 AND 5)
);
CREATE TABLE gep_ip (
    ip TEXT NOT NULL,
    gep TEXT NOT NULL REFERENCES gep(nev),
    PRIMARY KEY (ip, gep)
);
CREATE TABLE megfigyeltseg (
    gep TEXT PRIMARY KEY REFERENCES gep(nev),
    gepi_erzekelo INTEGER NOT NULL,
    halozati_erzekelo INTEGER NOT NULL
);
CREATE TABLE szoftver (
    gep TEXT NOT NULL REFERENCES gep(nev),
    cpe TEXT NOT NULL,
    termek TEXT,
    verzio TEXT,
    port INTEGER,
    szolgaltatas TEXT,
    PRIMARY KEY (gep, cpe)
);
CREATE TABLE serulekenyseg (
    cve TEXT NOT NULL,
    cvss REAL,
    erintett_cpe TEXT NOT NULL,
    PRIMARY KEY (cve, erintett_cpe)
);
CREATE TABLE szabaly_hivatkozas (
    forras TEXT NOT NULL,
    szabaly_id TEXT NOT NULL,
    cve TEXT,
    termek TEXT,
    szolgaltatas TEXT
);
"""


class Gepnyilvantartas:
    """A gépnyilvántartás lekérdezései. Csak olvasásra szolgál a mérések alatt."""

    def __init__(self, conn: sqlite3.Connection, kozos_ip_szabaly: str = "max") -> None:
        self.conn = conn
        if kozos_ip_szabaly not in {"max", "min"}:
            raise ValueError("A közös IP-cím szabálya 'max' vagy 'min' lehet.")
        self.kozos_ip_szabaly = kozos_ip_szabaly

    # --- betöltés -------------------------------------------------------------------------------
    @classmethod
    def from_yaml(cls, path: str | Path, db_path: str | Path = ":memory:",
                  megfigyeltseg_alapertek: tuple[bool, bool] = (True, True)) -> Gepnyilvantartas:
        """Betöltés az előzetesen rögzített YAML-fájlból.

        :param megfigyeltseg_alapertek: (gépi érzékelő, hálózati érzékelő) azoknál a gépeknél,
            amelyeknél a fájl nem ad meg mást. Az AIT-ADS-en minden gép naplóit feldolgozták
            (6.1), ezért ott mindkettő igaz.
        """
        cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        conn = sqlite3.connect(str(db_path))
        conn.executescript(SEMA)
        for g in cfg["gepek"]:
            conn.execute("INSERT INTO gep VALUES (?, ?, ?, ?)",
                         (g["nev"], g.get("zona"), g.get("szerep"), int(g["fokozat"])))
            for ip in g.get("ip", []):
                conn.execute("INSERT INTO gep_ip VALUES (?, ?)", (ip, g["nev"]))
            m = g.get("megfigyeltseg", {})
            conn.execute("INSERT INTO megfigyeltseg VALUES (?, ?, ?)",
                         (g["nev"], int(m.get("gepi", megfigyeltseg_alapertek[0])),
                          int(m.get("halozati", megfigyeltseg_alapertek[1]))))
        conn.commit()
        return cls(conn, cfg.get("kozos_ip_szabaly", "max"))

    # --- lekérdezések ---------------------------------------------------------------------------
    def gepnevek(self) -> list[str]:
        return [r[0] for r in self.conn.execute("SELECT nev FROM gep ORDER BY nev")]

    def gep_ip_alapjan(self, ip: str | None) -> str | None:
        """Az IP-címhez tartozó gép neve; közös IP-címnél a szabály (max/min fokozat) dönt."""
        if not ip:
            return None
        order = "DESC" if self.kozos_ip_szabaly == "max" else "ASC"
        row = self.conn.execute(
            "SELECT g.nev FROM gep_ip i JOIN gep g ON g.nev = i.gep WHERE i.ip = ? "
            f"ORDER BY g.fokozat {order}, g.nev LIMIT 1", (ip,)).fetchone()
        return row[0] if row else None

    def ismert_gep(self, nev: str | None) -> bool:
        return bool(nev) and self.conn.execute(
            "SELECT 1 FROM gep WHERE nev = ?", (nev,)).fetchone() is not None

    def fokozat(self, nev: str | None) -> int | None:
        row = self.conn.execute("SELECT fokozat FROM gep WHERE nev = ?", (nev,)).fetchone()
        return row[0] if row else None

    def lefedettseg(self, nev: str | None) -> float | None:
        """A teljesülő megfigyelési feltételek aránya (0, 0,5 vagy 1), 4.2.4."""
        row = self.conn.execute(
            "SELECT gepi_erzekelo, halozati_erzekelo FROM megfigyeltseg WHERE gep = ?",
            (nev,)).fetchone()
        return (row[0] + row[1]) / 2 if row else None

    def fokozatok(self) -> dict[str, int]:
        return dict(self.conn.execute("SELECT nev, fokozat FROM gep"))

    # --- szoftverkészlet és szabályhivatkozások (4.2.3, 5. lépés) -------------------------------
    def alkalmazhatosag_betoltese(self, path: str | Path) -> None:
        """A gépek szolgáltatásainak és a szabályok szolgáltatás-hivatkozásainak betöltése az
        előzetesen rögzített YAML-fájlból a ``szoftver`` és a ``szabaly_hivatkozas`` táblába.

        Az AIT-ADS-en a szoftverkészlet szolgáltatás-kategóriákként ismert (pl. ``web``, ``imap``);
        ezeket a ``szoftver`` tábla ``szolgaltatas`` oszlopa tárolja, a CPE helyén
        ``szolgaltatas:<kategória>`` azonosítóval. CVE-szintű adat a laborban kerül a táblákba.
        """
        cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        if cfg.get("allapot") != "jovahagyva":
            raise ValueError(f"A megfeleltetés nincs jóváhagyva (allapot: {cfg.get('allapot')}).")
        for gep, szolg in cfg["szoftverkeszlet"].items():
            if not self.ismert_gep(gep):
                raise ValueError(f"Ismeretlen gép a szoftverkészletben: {gep}")
            for sz in szolg:
                self.conn.execute(
                    "INSERT INTO szoftver (gep, cpe, szolgaltatas) VALUES (?, ?, ?)",
                    (gep, f"szolgaltatas:{sz}", sz))
        for forras, szabalyok in cfg["szabalyok"].items():
            for szabaly_id, sz in szabalyok.items():
                self.conn.execute(
                    "INSERT INTO szabaly_hivatkozas (forras, szabaly_id, szolgaltatas) "
                    "VALUES (?, ?, ?)", (forras, str(szabaly_id), sz))
        self.conn.commit()

    def szolgaltatasok(self, gep: str | None) -> set[str] | None:
        """A gépen futó szolgáltatások; ``None``, ha a gép szoftverkészlete nem ismert."""
        rows = [r[0] for r in self.conn.execute(
            "SELECT szolgaltatas FROM szoftver WHERE gep = ?", (gep,))]
        return set(rows) if rows else None

    def szabaly_szolgaltatasa(self, forras: str, szabaly_id: str) -> str | None:
        row = self.conn.execute(
            "SELECT szolgaltatas FROM szabaly_hivatkozas WHERE forras = ? AND szabaly_id = ?",
            (forras, str(szabaly_id))).fetchone()
        return row[0] if row else None

    def gep_cve_i(self, gep: str | None) -> set[str]:
        """A gépen futó szoftverek ismert sérülékenységei (CPE-n keresztül)."""
        return {r[0] for r in self.conn.execute(
            "SELECT DISTINCT v.cve FROM szoftver s JOIN serulekenyseg v "
            "ON v.erintett_cpe = s.cpe WHERE s.gep = ?", (gep,))}

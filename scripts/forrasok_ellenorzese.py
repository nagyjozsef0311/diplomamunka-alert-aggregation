#!/usr/bin/env python3
"""A references.bib forrásainak ellenőrzése: Crossref (DOI), arXiv (preprint), webes források (URL).

Minden forrásnál lekéri a metaadatokat, és összeveti a bejegyzéssel: cím, első szerző családneve,
megjelenési év. Folyóiratcikknél kiírja, ha a Crossref szerint van kötet-, szám- vagy oldaladat, de a
bejegyzésből hiányzik. Webes forrásnál azt ellenőrzi, hogy az URL elérhető-e (HTTP 200).

A szkript csak olvas és jelent; a --javit kapcsolóval
  * pótolja a hiányzó kötet-, szám- és oldaladatokat a Crossrefből (meglévőt nem ír felül),
  * a sikeresen ellenőrzött tételeknél az ``urldate`` mezőt az ellenőrzés napjára állítja
    (az „utoljára megtekintve” dátum így a tényleges ellenőrzés napja).
Eltérést (cím, szerző, év) nem javít automatikusan: azokat a jelentés sorolja fel.

Használat:
    python scripts/forrasok_ellenorzese.py [--javit] [--bib thesis/references.bib]
Jelentés: docs/atnezesek/forrasok_ellenorzese_<dátum>.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "thesis-reference-check/1.0 (python-requests)"}
ATOM = "{http://www.w3.org/2005/Atom}"


def bejegyzesek(t: str) -> list[dict]:
    out = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", t, re.DOTALL):
        typ, key, body = m.groups()
        mezok = {}
        for fm in re.finditer(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", body, re.MULTILINE):
            mezok[fm.group(1).lower()] = fm.group(2)
        out.append({"typ": typ.lower(), "key": key.strip(), "f": mezok, "raw": m.group(0)})
    return out


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\\[a-zA-Z]+|[{}\\]", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def hasonlo(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def elso_csaladnev(author: str) -> str:
    a = author.split(" and ")[0].strip().strip("{}")
    return norm(a.split(",")[0] if "," in a else a.split()[-1])


def crossref(doi: str) -> dict | None:
    r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=30)
    if r.status_code != 200:
        return None
    m = r.json()["message"]
    ev = None
    for k in ("published-print", "published-online", "issued", "published"):
        if m.get(k, {}).get("date-parts"):
            ev = m[k]["date-parts"][0][0]
            break
    return {
        "title": (m.get("title") or [""])[0],
        "first": norm((m.get("author") or [{}])[0].get("family", "")),
        "year": ev,
        "container": (m.get("container-title") or [""])[0],
        "volume": m.get("volume"), "issue": m.get("issue"), "page": m.get("page"),
        "article": m.get("article-number"),
    }


def arxiv(aid: str) -> dict | None:
    r = requests.get(f"https://export.arxiv.org/api/query?id_list={aid}", headers=UA, timeout=30)
    if r.status_code != 200:
        return None
    e = ET.fromstring(r.text).find(f"{ATOM}entry")
    if e is None or e.find(f"{ATOM}title") is None:
        return None
    nev = e.find(f"{ATOM}author/{ATOM}name").text
    return {"title": " ".join(e.find(f"{ATOM}title").text.split()),
            "first": norm(nev.split()[-1]), "year": int(e.find(f"{ATOM}published").text[:4])}


def url_ok(url: str) -> int:
    try:
        r = requests.get(url, headers=UA, timeout=30, allow_redirects=True)
        return r.status_code
    except requests.RequestException as exc:
        return f"hiba: {type(exc).__name__}"


def ellenoriz(b: dict, elfogadott: set[str] = frozenset()) -> dict:
    f = b["f"]
    res = {"key": b["key"], "forras": None, "ok": False, "megjegyzes": [], "potol": {}}
    doi = f.get("doi")
    ax = re.search(r"arXiv:(\d{4}\.\d{4,5})", f.get("journal", "") + f.get("howpublished", ""))
    try:
        if doi:
            res["forras"] = "Crossref"
            m = crossref(doi)
            if m is None:
                res["megjegyzes"].append("a DOI nem található a Crossrefben")
                return res
        elif ax:
            res["forras"] = "arXiv"
            m = arxiv(ax.group(1))
            if m is None:
                res["megjegyzes"].append("az arXiv-azonosító nem található")
                return res
        elif f.get("url"):
            res["forras"] = "URL"
            code = url_ok(f["url"])
            res["ok"] = code == 200
            if not res["ok"]:
                res["megjegyzes"].append(f"az URL nem érhető el ({code})")
            return res
        else:
            res["megjegyzes"].append("nincs DOI, arXiv-azonosító vagy URL")
            return res
    except requests.RequestException as exc:
        res["megjegyzes"].append(f"lekérési hiba: {type(exc).__name__}")
        return res
    h = hasonlo(f.get("title", ""), m["title"])
    if h < 0.85:
        res["megjegyzes"].append(f"cím eltér ({h:.2f}): „{m['title']}”")
    if f.get("author") and m["first"] and elso_csaladnev(f["author"]) not in m["first"] \
            and m["first"] not in elso_csaladnev(f["author"]):
        res["megjegyzes"].append(f"első szerző eltér: {m['first']}")
    if m.get("year") and f.get("year") and str(m["year"]) != f["year"].strip():
        res["megjegyzes"].append(f"év eltér: {m['year']}")
    if res["forras"] == "Crossref" and b["typ"] in ("article", "inproceedings", "incollection"):
        if b["typ"] == "article" and m.get("volume") and not f.get("volume"):
            res["potol"]["volume"] = m["volume"]
        if b["typ"] == "article" and m.get("issue") and not f.get("number"):
            res["potol"]["number"] = m["issue"]
        if m.get("page") and not f.get("pages") and not f.get("eid"):
            res["potol"]["pages"] = m["page"].replace("-", "--")
        elif m.get("article") and not f.get("pages") and not f.get("eid"):
            res["potol"]["eid"] = m["article"]
    if res["megjegyzes"] and b["key"] in elfogadott:
        res["megjegyzes"] = [f"kézzel elfogadva: {m}" for m in res["megjegyzes"]]
        res["ok"] = True
        return res
    res["ok"] = not res["megjegyzes"]
    return res


def javit(t: str, b: dict, res: dict, nap: str) -> str:
    raw = b["raw"]
    uj = raw
    for mezo, ertek in res["potol"].items():
        uj = re.sub(r"\n\}$", f",\n  {mezo} = {{{ertek}}}\n}}", uj)
    if res["ok"]:
        if re.search(r"^\s*urldate\s*=", uj, re.MULTILINE):
            uj = re.sub(r"(urldate\s*=\s*\{)[^}]*(\})", rf"\g<1>{nap}\g<2>", uj)
        else:
            uj = re.sub(r"\n\}$", f",\n  urldate = {{{nap}}}\n}}", uj)
    uj = uj.replace(",,", ",")
    return t.replace(raw, uj)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", type=Path, default=ROOT / "thesis" / "references.bib")
    ap.add_argument("--javit", action="store_true")
    ap.add_argument("--elfogadott", default="",
                    help="vesszővel elválasztott kulcsok, amelyek eltérését kézzel átnéztük és elfogadtuk")
    args = ap.parse_args()
    nap = dt.datetime.now(dt.UTC).date().isoformat()
    t = args.bib.read_text(encoding="utf-8")
    bs = bejegyzesek(t)
    eredmeny = []
    for b in bs:
        res = ellenoriz(b, set(filter(None, args.elfogadott.split(","))))
        eredmeny.append(res)
        print(f"{'OK ' if res['ok'] else '!! '}{b['key']:<28} {res['forras'] or '-':<9} "
              f"{'; '.join(res['megjegyzes'])} {res['potol'] or ''}", flush=True)
        if args.javit:
            t = javit(t, b, res, nap)
        time.sleep(0.3)
    if args.javit:
        args.bib.write_text(t, encoding="utf-8")
    ok = sum(r["ok"] for r in eredmeny)
    sorok = [f"# A források ellenőrzése – {nap}", "",
             (f"Szkript: `scripts/forrasok_ellenorzese.py`{' --javit' if args.javit else ''} · "
              f"tételek: {len(eredmeny)} · rendben: {ok} · eltérés vagy hiba: {len(eredmeny) - ok}"),
             "", "| kulcs | forrás | rendben | megjegyzés | pótolt mező |", "| --- | --- | --- | --- | --- |"]
    for r in eredmeny:
        sorok.append(f"| {r['key']} | {r['forras'] or '–'} | {'igen' if r['ok'] else '**nem**'} | "
                     f"{'; '.join(r['megjegyzes'])} | "
                     f"{', '.join(f'{k}={v}' for k, v in r['potol'].items())} |")
    ki = ROOT / "docs" / "atnezesek" / f"forrasok_ellenorzese_{nap}.md"
    ki.write_text("\n".join(sorok) + "\n", encoding="utf-8")
    print(f"\n[jelentés] {ki.relative_to(ROOT)} · rendben: {ok}/{len(eredmeny)}")


if __name__ == "__main__":
    main()

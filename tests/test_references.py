"""A thesis/references.bib ellenőrzése: a LaTeX különleges karakterei (%, &) csak \\-rel szerepelhetnek.

Egy védtelen % az egész irodalomjegyzéket tönkreteszi (a sor többi részét megjegyzésnek veszi).
Az url és doi mezők kivételek, ott a biblatex maga kezeli ezeket.
"""

import re
from pathlib import Path

BIB = Path(__file__).resolve().parents[1] / "thesis" / "references.bib"


def test_no_unescaped_special_characters():
    hibak = []
    for n, line in enumerate(BIB.read_text(encoding="utf-8").splitlines(), start=1):
        # url/doi mező, illetve a bejegyzéseken kívüli megjegyzéssor (%-kal kezdődik) rendben van
        if re.match(r"\s*(url|doi)\s*=", line) or line.startswith("%"):
            continue
        if re.search(r"(?<!\\)[%&]", line):
            hibak.append(f"{n}: {line.strip()}")
    assert not hibak, "Védtelen % vagy & a references.bib-ben:\n" + "\n".join(hibak)


def test_braces_balanced_per_entry():
    text = BIB.read_text(encoding="utf-8")
    for key, body in re.findall(r"@\w+\{([^,]+),(.*?)\n\}", text, re.S):
        assert body.count("{") == body.count("}"), f"Zárójelhiba: {key}"

# A dolgozat változatai

Minden Overleafbe átvitt változat egy sort kap. Az exportált zip neve: `diplomamunka_<változat>.zip`
(`scripts/export_overleaf.sh <változat>`). A „Commit” oszlop a git-tárolóbeli állapotot azonosítja.

| Változat | Dátum | Commit | Mi változott |
| --- | --- | --- | --- |
| v0.1 | 2026-10-01 | 9c3c333 | Az eredeti kari sablon, javítások nélkül (a személyes előlapok helyén jelzőoldal) |
| v0.2 | 2026-10-01 | b870891 | Formai javítások a kari útmutató szerint: margó (fent 40, lent 25, kívül 25, kötésoldalon 35 mm), 1,5-es sorköz, oldalszám fent a lap közepén 20 mm-re, fejezetcím középre igazítva; irodalomjegyzék az első szerző szerint betűrendben, URL és „utoljára megtekintve” dátum; Összefoglalás és Summary fejezet, Mellékletek és Rövidítések helye (kikommentezve, amíg üres); a DM4-es konzultációs napló, a mintafejezet, a mintakép, a minta-hivatkozások és -rövidítések törölve |
| v0.3 | 2026-10-01 | b41fa8c | Javítás: az Overleaf a template.tex-et fordította fő fájlként („no legal \\end found”); a dokumentumosztály megadása átkerült a main.tex elejére, így feltöltéskor a main.tex lesz a fő fájl |

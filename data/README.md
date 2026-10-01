# data/

Ide kerülnek a letöltött adatok. A mappa tartalma (ezen a fájlon kívül) nem kerül a tárolóba.

| Almappa | Mi kerül bele | Hogyan |
| --- | --- | --- |
| `ait_ads/` | AIT-ADS eredeti riasztásai és `labels.csv` | `python scripts/download_ait_ads.py` |
| `external/cats/` | A CATS kódja rögzített commiton | `python scripts/download_cats.py` |
| `external/cats_datasets/` | Az AIT-ADS felcímkézett, CATS-formátumú változata (Wazuh, Suricata) | ugyanez a szkript |

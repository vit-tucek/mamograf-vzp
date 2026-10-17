# Data: stručný přehled

Všechna data pro notebooky jsou v [`data/`](data/), každý soubor zabalený zvlášť jako `<soubor>.zip`.
Notebooky je čtou přímo ze zipů (`utils/nacteni.py`), nic se nestahuje. Velké zdrojové sady nejsou v gitu,
jen jejich okresní agregáty; přepočítává je `utils/priprava_dat.py` ze složky `sources/`.
Podrobný popis (sloupce, úpravy, kódy výkonů) je v [`docs/ZDROJE_DAT.md`](docs/ZDROJE_DAT.md).

Okresy jsou všude kódy **LAU 1** (`CZ0201` Benešov), Praha je jeden okres `CZ0100`.

| Soubor | Obsah | Zdroj | Členění | Roky |
|---|---|---|---|---|
| `uzis_pps_mamografie.csv` | screeningové mamografie (počet vyšetření) | ÚZIS PPS-01-02 | okres **bydliště** × 5leté věkové skupiny | 2010–2024 |
| `uzis_pps_prevence_zeny45.csv` | preventivní prohlídky u praktika + kapitační populace, ženy 45+ | ÚZIS PPS-08-04 (agregát) | okres **pracoviště** praktika × věk | 2011–2024 |
| `csu_zeny_okresy.csv` | ženy 45+ (střední stav), jmenovatel pokrytí | ČSÚ OBY02D | okres × 5leté skupiny | 2010–2024 |
| `csu_obyvatele_kraje.csv` | obyvatelé ČR a krajů podle pohlaví a věku (jen kontrola) | ČSÚ OBY02D | kraj | 2025 |
| `csu_kovariaty_okresy.csv` | 24 socioekonomických ukazatelů (nezaměstnanost, dávky, vzdělání, ceny bytů…) | ČSÚ DataStat, SLDB 2021 | okres | 2024 / 2021 |
| `nrhzs_ukazatele_okresy.csv` | 12 ukazatelů z vykázaných výkonů (gyn. prevence, cytologie, test OK, nemocnost) | ÚZIS NR-04-86 (agregát) | okres **pacienta** | 2019–2024 |
| `nrhzs_mamografie_toky.csv` | screeningové mamografie: okres bydliště → okres zařízení | ÚZIS NR-04-86 (agregát) | dvojice okresů | 2019–2024 |
| `uzis_nrhzs_vykony_metodika.pdf` | metodika sady NR-04-86 | ÚZIS | – | – |
| `uzis_chripka_proockovanost.xlsx` | proočkovanost proti chřipce (vše a 65+) | ÚZIS NR-28-02 | okres × sezóna | 2010/11–2025/26 |
| `mzcr_covid_davky_zeny45_orp.csv` | dávky vakcíny proti covidu, ženy 45+ | MZ ČR (agregát) | ORP bydliště | kumulativně od 12/2020 |
| `volby_ps2025_okresy.csv` | volby do PS 2025, % hlasů stran | dodaný soubor | okres | 2025 |
| `mamocz_pracoviste.csv` | 75 akreditovaných mamografických pracovišť se souřadnicemi obce | mamo.cz + RÚIAN | pracoviště | 9/2026 |
| `ruian_okresy.geojson` | hranice okresů (zjednodušené ~200 m) | ČÚZK RÚIAN | okres | 9/2026 |
| `ruian_obce_okresy.csv` | převodník obec → okres | ČÚZK RÚIAN | obec | 9/2026 |
| `ruian_orp_okresy.csv` | převodník ORP → okres | ČÚZK RÚIAN | ORP | 10/2026 |
| `nrhzs_mamografie_icz.csv` | screeningové mamografie po IČZ: okres zařízení × okres pacientky | ÚZIS NR-04-86 (agregát) | IČZ × dvojice okresů | 2019–2024 |
| `nrhzs_gyn_icz.csv` | preventivní gynekologické prohlídky (63050) po IČZ | ÚZIS NR-04-86 (agregát) | IČZ × okres zařízení | 2019–2024 |
| `nrpzs_gyn_okresy.csv` | ordinace registrujících gynekologů (místa péče) | ÚZIS NRPZS NR-01-06 (agregát) | okres | stav 10/2026 |
| `mamocz_pracoviste_historie.csv` | počet akreditovaných pracovišť | mamo.cz přes web.archive.org (agregát) | okres × rok | 2008–2019, 2026 |
| `mamocz_cekaci_doby.csv` | objednací lhůta pracoviště ve dnech (419 údajů) | mamo.cz přes web.archive.org | pracoviště × snímek | 2013–2019 |
| `nor_c50_kraje.csv` | karcinom prsu u žen: incidence podle stadia, úmrtí | ÚZIS NOR NR-07-01, NR-07-02 (agregát) | kraj × rok × 5leté věk. skupina | 1977–2024 |

## Na co si dát pozor

- **Dva geografické klíče:** mamografie je podle bydliště, prevence u praktika podle sídla praktika.
- **NR-04-86 nemá pohlaví ani věk** a nemocnost je dolní odhad z hlavních diagnóz.
- **Okres zařízení v NR-04-86 je okres, kde se výkon vykazuje.** U řetězců (EUC, AGEL, Medicon) je to
  sídlo, ne místo pracoviště, takže „dojížďka“ v 7 okresech vychází uměle 100 %
  (`notebooks/mamograf_analyza.ipynb`, kap. 3.1).
- **Praha chybí v covidových datech** (bydliště v Praze je v sadě MZ „nezařazeno“).
- **ÚZIS vynechává nulové buňky** (např. 85+ v malých okresech 2010–2011).
- **NRPZS je průřez**: obsahuje jen dnes fungující místa péče, zaniklé ordinace v něm nejsou.
- **NOR v otevřených datech nemá okresy**, jen kraje; neznámé stadium 2–8 % podle kraje.
- **Historie pracovišť** chybí pro roky 2012, 2014 a 2020–2025 (snímky webu nejsou nebo seznam neobsahují).
  Objednací lhůty jsou jen v snímcích 2013–2019 a jsou to údaje, které pracoviště sama hlásila.

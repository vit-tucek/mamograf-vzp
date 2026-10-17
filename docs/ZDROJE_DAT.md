# Zdroje dat

Všechna data, která notebook `mamograf_exploration.ipynb` potřebuje, jsou v `data/`,
každý soubor zabalený zvlášť jako `data/<soubor>.zip` (dohromady asi 1,3 MB).
První buňka notebooku je rozbalí vedle sebe do `data/` (`unzip -n` rozbalí jen
soubory, které tam ještě nejsou). Rozbalené soubory git ignoruje, v repozitáři
jsou jen zipy.

Velké zdrojové sady v repozitáři nejsou, jsou v něm jen jejich **okresní agregáty**.
Agregáty ze zdrojových sad počítá skript `utils/priprava_dat.py`, notebook pracuje
jen s nimi. Zdrojové sady patří do složky `sources/` pod původními názvy (git ji
ignoruje). Skript je potřeba spustit, jen když se mají agregáty přepočítat:

    python utils/priprava_dat.py

Přepočítá a znovu zabalí všechny agregáty (asi 3 minuty, kroky jde vybrat přes `--jen`). Ověřili jsme, že
dává bajt po bajtu shodné soubory jako ty v repozitáři.

Data stažená z API (ČSÚ, RÚIAN, mamo.cz) jsou v `data/` jako cache. Když soubor
smažete, notebook ho stáhne znovu (výsledek se pak může lišit podle aktuálního
stavu zdroje).

Kódy okresů jsou všude **LAU 1 / okres podle ČSÚ** (např. `CZ0201` Benešov).
Praha je jeden okres `CZ0100`.

## Přehled

| Soubor v `data/` (v repozitáři jako `.zip`) | Obsah | Zdroj | Agregováno? |
|---|---|---|---|
| `uzis_pps_mamografie.csv` | screeningové mamografie, rok × okres bydliště × věk | ÚZIS, PPS-01-02 | ne |
| `uzis_pps_prevence_zeny45.csv` | preventivní prohlídky u praktika, ženy 45+ | ÚZIS, PPS-08-04 | **ano** |
| `uzis_chripka_proockovanost.xlsx` | proočkovanost proti chřipce, okresy × sezóny | ÚZIS, NR-28-02 | ne |
| `mzcr_covid_davky_zeny45_orp.csv` | dávky vakcíny proti covidu, ženy 45+, ORP bydliště | MZ ČR, `ockovani-zakladni-prehled` | **ano** |
| `nrhzs_ukazatele_okresy.csv` | 12 ukazatelů z vykázaných výkonů, rok × okres | ÚZIS, NR-04-86 | **ano** |
| `nrhzs_mamografie_toky.csv` | screeningové mamografie, okres bydliště → okres zařízení | ÚZIS, NR-04-86 | **ano** |
| `uzis_nrhzs_vykony_metodika.pdf` | metodický popis sady NR-04-86 | ÚZIS | – |
| `csu_zeny_okresy.csv` | ženy podle okresu a pětiletých skupin, 2010–2024 | ČSÚ DataStat API, OBY02D | ne (stažený výřez) |
| `csu_obyvatele_kraje.csv` | obyvatelé ČR a krajů podle pohlaví a věku, 2025 | ČSÚ, OBY02D | ne |
| `csu_kovariaty_okresy.csv` | socioekonomické ukazatele okresů | ČSÚ DataStat API, 15 sad | **ano** (sestaveno) |
| `volby_ps2025_okresy.csv` | výsledky voleb do PS 2025 po okresech | dodaný soubor | ne |
| `ruian_okresy.geojson` | hranice okresů | ČÚZK RÚIAN | ne (zjednodušeno) |
| `ruian_obce_okresy.csv` | převodník obec → okres | ČÚZK RÚIAN | ne |
| `ruian_orp_okresy.csv` | převodník ORP → okres | ČÚZK RÚIAN | ne |
| `mamocz_pracoviste.csv` | akreditovaná mamografická pracoviště se souřadnicemi | mamo.cz + RÚIAN | ne (geokódováno) |
| `nrhzs_mamografie_icz.csv`, `nrhzs_gyn_icz.csv` | mamografie a gyn. prevence po IČZ | ÚZIS, NR-04-86 | **ano** |
| `nrpzs_gyn_okresy.csv` | ordinace registrujících gynekologů po okresech | ÚZIS, NRPZS NR-01-06 | **ano** |
| `nor_c50_kraje.csv` | karcinom prsu: incidence podle stadia, úmrtí, kraje | ÚZIS, NOR NR-07-01/02 | **ano** |
| `mamocz_pracoviste_historie.csv` | počet pracovišť po okresech a letech | mamo.cz přes web.archive.org | **ano** |
| `mamocz_cekaci_doby.csv` | objednací lhůty pracovišť 2013–2019 | mamo.cz přes web.archive.org | **ano** (extrahováno) |

Zdrojové sady, které jsou jen lokálně v `sources/` (původní názvy, v repozitáři nejsou;
stáhnout ze zdrojů uvedených níže):

| Soubor | Velikost | Z něj vzniká |
|---|---|---|
| `Otevrena-data-PPS-08-04-preventivni-prohlidky-pokryti-kapitace.csv` | 15 MB | `uzis_pps_prevence_zeny45.csv` |
| `ockovani-zakladni-prehled.csv` | 49 MB | `mzcr_covid_davky_zeny45_orp.csv` |
| `Otevrena-data-NR-04-86-vykony-icz-okres-diagnoza.csv.gz` | 2,3 GB (19 GB rozbalený) | `nrhzs_*.csv` |
| `Otevrena-data-OIS-12-03-ciselnik-mkn-10-cz.csv` | 14 MB | nic, jen jsme v něm ověřili význam diagnóz |
| `Otevrena-data-NR-01-06-nrpzs-mista-poskytovani-zdravotnich-sluzeb.csv` | 28 MB | `nrpzs_gyn_okresy.csv` |
| `Otevrena-data-NR-07-01-novotvary-incidence-prevalence-regiony.csv.gz`, `…NR-07-02-novotvary-mortalita-regiony.csv.gz` | 35 MB | `nor_c50_kraje.csv` |
| `wayback_mamo/*.html` | 1 MB | `mamocz_pracoviste_historie.csv`, `mamocz_cekaci_doby.csv` |

---

## ÚZIS: Program prevence a screeningu

Otevřená data ÚZIS ČR, katalog na [nzip.cz/data](https://www.nzip.cz/data).

### `uzis_pps_mamografie.csv` (PPS-01-02)

Počet screeningových mamografických vyšetření podle roku, pohlaví, pětileté věkové
skupiny a **okresu bydliště** pojištěnky. Roky 2010–2024, 10 392 řádků.
Sloupce: `rok, pohlavi, vek_kod, vek_nazev, okres_lau_kod, okres_nazev, kraj_nuts_kod,
kraj_nazev, pocet_vysetreni`. Původně `Otevrena-data-PPS-01-02-mamografie-screeningova-vysetreni-pocet.csv`,
obsah beze změny.

### `uzis_pps_prevence_zeny45.csv` (agregát PPS-08-04)

Preventivní prohlídky u praktického lékaře: počet vyšetřených a kapitační populace
podle roku, pohlaví, věku a **okresu pracoviště praktického lékaře** (ne bydliště).
Roky 2011–2024.

**Úprava:** zdrojová sada je navíc členěná podle velikosti kapitace praktika
(`kapitace_skupina`). Tu jsme sečetli a ponechali jen ženy ve věku 45+. Ostatní
sloupce i hodnoty jsou shodné se zdrojem. Zdroj:
`Otevrena-data-PPS-08-04-preventivni-prohlidky-pokryti-kapitace.csv`.

### `uzis_chripka_proockovanost.xlsx` (NR-28-02)

Datový souhrn ÚZIS *Přehled proočkovanosti u vybraných vakcín v rámci krajů
a okresů ČR*, stav k 1. 9. 2026. Notebook čte listy `Chřipka` (celá populace)
a `Chřipka_65` (65+): demografii, počet vakcinovaných a proočkovanost za sezóny
2010/11–2025/26 (sezóna = září až září). Zdroj ÚZIS: NRHZS (hrazená očkování)
a od 2023 také e-vakcinace ISIN (i nehrazená), proto je v roce 2023 zlom v řadě.
Původně `Datovy-souhrn-NR-28-02-proockovanost-chripka-kraje-okresy-2026-01.xlsx`,
obsah beze změny.

## ÚZIS: Národní registr hrazených zdravotních služeb (NR-04-86)

Sada *Výkony zdravotní péče vykázané v rámci veřejného zdravotního pojištění dle
IČZ, okresu zdravotnického zařízení, okresu pacienta a hlavní diagnózy*, verze
2026-01, [nzip.cz/data/2629](https://www.nzip.cz/data/2629-vykony-icz-okresdiagnoza-otevrena-data).
Popis je v `uzis_nrhzs_vykony_metodika.pdf`.

Zdroj má 334 mil. řádků: rok (2019–2024) × kód výkonu × hlavní diagnóza (MKN-10,
3 znaky) × IČZ × okres zařízení × okres pacienta, s počtem výkonů, pacientů
a kontaktů. **Neobsahuje pohlaví ani věk.** Agregujeme ho přes DuckDB přímo nad
`.gz` (funkce `agreguj_nrhzs` v `utils/priprava_dat.py`). Okres „neuvedeno“ (`CZ0999`)
vynecháváme, pražské obvody `CZ0101–CZ010A` slučujeme do `CZ0100`.

### `nrhzs_ukazatele_okresy.csv`

Dlouhý formát `ukazatel, rok, lau, hodnota`, okres = **okres bydliště pacienta**:

| `ukazatel` | Co je `hodnota` | Kódy |
|---|---|---|
| `vykony` | všechny vykázané výkony (množství) | všechny |
| `gyn_prevence` | pacientky s preventivní gynekologickou prohlídkou | výkon 63050 |
| `cytologie` | pacientky s cytologií děložního čípku | výkon 63417 |
| `toks` | pacienti s testem na okultní krvácení (dolní odhad) | výkony 15118, 15119, 15120 |
| `diag_prs` | diagnostická zobrazovací vyšetření prsu (množství) | výkony 89xxx kromě 89223 a 89814, dg. C50, D05, D24, N60–N64, R92 |
| `rakovina_prs` | pacientky s rakovinou prsu (dolní odhad) | dg. C50, D05 |
| `nezhoubne_prs` | pacientky s nezhoubným nálezem prsu (dolní odhad) | dg. D24, N60–N64, R92 |
| `diabetes` | pacienti s diabetem (dolní odhad) | dg. E10–E14 |
| `hypertenze` | pacienti s hypertenzí (dolní odhad) | dg. I10–I13, I15 |
| `chopn` | pacienti s CHOPN (dolní odhad) | dg. J44 |
| `deprese` | pacienti s depresí (dolní odhad) | dg. F32, F33 |
| `obezita` | pacienti s obezitou (dolní odhad) | dg. E66 |

**Dolní odhad:** jeden pacient má během roku řadu různých výkonů a počty pacientů
se přes výkony sčítat nedají. Bereme proto v každém roce a okrese ten výkon,
který má s danou diagnózou nejvíc pacientů. Diagnóza se navíc počítá jen tam, kde
je vykázaná jako hlavní, takže hypertenze, deprese a obezita jsou výrazně
podhodnocené. Ukazatele slouží ke srovnání okresů mezi sebou, ne jako odhad
prevalence.

**Kódy výkonů** jsme určili z dat, ne z číselníku výkonů: 89223 se vykazuje
s dg. Z12 a jeho počty sedí s PPS-01-02 (2024: 775 tis. proti 787 tis.), 89814 má
shodné počty jako 89223, 63050 je nejčastější gynekologický výkon s dg. Z01, 63417
je z poloviny s dg. Z01 a 15118–15120 mají shodné složení diagnóz (čtvrtina Z12).
Význam diagnóz jsme ověřili v číselníku MKN-10-CZ (ÚZIS OIS-12-03). **Názvy
výkonů je potřeba ověřit v číselníku zdravotních výkonů MZ ČR.**

### `nrhzs_mamografie_toky.csv`

Screeningové mamografie (výkon 89223) podle roku, okresu bydliště (`z_lau`)
a okresu zařízení (`cil_lau`), sloupec `mnozstvi` = počet výkonů. Z toho notebook
počítá **měřenou dojížďku**: podíl mamografií rezidentek okresu provedených
v jiném okrese.

## MZ ČR: očkování proti covidu

### `mzcr_covid_davky_zeny45_orp.csv` (agregát)

Zdroj: otevřená data MZ ČR o covidu-19 ([onemocneni-aktualne.mzcr.cz/api/v2/covid-19](https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19)),
sada `ockovani-zakladni-prehled.csv`. Ve zdroji je počet dávek podle kraje očkování,
ORP bydliště, vakcíny, pořadí dávky, věkové skupiny a pohlaví.

**Úprava:** ponechány jen ženy ve věkových skupinách 45–49 až 80+, sečteno přes
vakcíny a kraje očkování. Sloupce: `orp_bydliste, orp_bydliste_kod, poradi_davky,
vekova_skupina, pohlavi, pocet_davek`. Bydliště v Praze je ve zdroji v kategorii
„nezařazení“ (`orp_bydliste_kod = 0`) spolu s neznámým bydlištěm, proto Praha
v covidových ukazatelích chybí. Kategorii „cizinci“ notebook vynechává.

## ČSÚ

### `csu_zeny_okresy.csv`

Výřez z [DataStat API ČSÚ](https://data.csu.gov.cz), sada **OBY02D**: ženy, střední
stav k 1. 7., pětileté věkové skupiny 45+, okresy, 2010–2024. Prahu API
v okresním členění nevrací, proto je doplněná z krajské úrovně. Slouží jako
jmenovatel mamografického pokrytí. Staženo 22. 9. 2026.

### `csu_obyvatele_kraje.csv`

Export sady **OBY02D**: počet obyvatel ČR a krajů podle pohlaví a pětiletých
skupin k 1. 1., 1. 7. a 31. 12. 2025. V notebooku jen jako kontrolní součet.
Původně `Počet obyvatel podle pohlaví a pětiletých věkových skupin k 1. 1., 1. 7. a 31. 12..csv`.

### `csu_kovariaty_okresy.csv` (sestaveno)

77 okresů × 24 ukazatelů stažených z DataStat API v kap. 8 notebooku, vesměs za
rok 2024:

| Sada | Ukazatele |
|---|---|
| OBY02D | obyvatelé celkem, ženy celkem |
| NEZ01 | podíl nezaměstnaných žen |
| CIZ001 | ženy s cizím občanstvím (k 31. 12.) |
| SZB02 | dávky SSP a příspěvek na bydlení (tis. Kč) |
| SZB08 | invalidní důchody žen (součet tří stupňů) |
| CEN0402 | kupní ceny bytů a domů, Kč/m² (2022–2024) |
| RSO08 | hustota zalidnění |
| OBY02F | průměrný věk žen, podíl žen 65+ |
| OBY04K | podíl úmrtí žen na novotvary |
| OBY06 | migrační saldo |
| SLDZOB01, 03, 04, 11, 13 | sčítání 2021 na úrovni obcí, sečtené na okresy: velikost obcí, rodinný stav, vzdělání, bydlení mimo byty, ekonomická aktivita |

Hodnoty ze sčítání jsou sečtené z obcí přes `ruian_obce_okresy.csv`. Staženo
22. 9. 2026.

## Ostatní

### `volby_ps2025_okresy.csv`

Výsledky voleb do Poslanecké sněmovny 2025 po okresech, % platných hlasů pro
strany ANO, SPOLU, STAN, Piráti, SPD, AUTO (Motoristé), Stačilo!, PŘÍSAHA,
Generace, ČR1 a ostatní. Středníkový CSV s desetinnou čárkou, názvy okresů končí
neviditelnou mezerou U+200B. Původně `cz_0_okres.csv`. **Přesný zdroj souboru je
potřeba doplnit.**

### `ruian_okresy.geojson`, `ruian_obce_okresy.csv`, `ruian_orp_okresy.csv`

ČÚZK, RÚIAN přes [ArcGIS REST](https://ags.cuzk.cz/arcgis/rest/services/RUIAN/MapServer):
- **okresy:** vrstva 15 (Okres), Praha doplněná z vrstvy 12 (Obec). Geometrie
  zjednodušené na zhruba 200 m (`maxAllowableOffset = 0.003`). Staženo 22. 9. 2026.
- **obce:** vrstva 12, převodník kódu obce na okres (6 258 obcí). Staženo 22. 9. 2026.
- **ORP:** vrstva 14 (ORP nese kód okresu) spojená s vrstvou 15, 205 ORP bez
  Prahy. Staženo 3. 10. 2026.

### `mamocz_pracoviste.csv`

Seznam 75 akreditovaných mamografických screeningových pracovišť z
[mamo.cz/centra](https://www.mamo.cz/centra/), stažený 22. 9. 2026. Adresy jsme
geokódovali na úroveň obce přes RÚIAN (souřadnice = těžiště obce). Sloupce:
`pracoviste, adresa, psc, mesto, kraj, obec, kraj_nuts, obec_lau, obec_kraj, lon, lat`.

---

## Data pro rozšiřující analýzy (`mamograf_rozsireni.ipynb`)

Tyto agregáty počítá `utils/priprava_dat.py` (kroky `nrhzs_icz`, `nrpzs`, `nor`,
`centra_historie`, např. `python utils/priprava_dat.py --jen nrpzs nor`). Zdroje jsou v `sources/`
pod původními názvy; adresy stahování jsou z Národního katalogu otevřených dat (data.gov.cz).

### `nrhzs_mamografie_icz.csv`, `nrhzs_gyn_icz.csv` (NR-04-86 po IČZ)

Stejný zdroj jako `nrhzs_*_okresy.csv`
([datanzis.uzis.gov.cz](https://datanzis.uzis.gov.cz/data/NR-04-NRHZS/NR-04-86/Otevrena-data-NR-04-86-vykony-icz-okres-diagnoza.csv.gz),
verze 2026-02), ale bez sčítání přes IČZ. Mamografie (89223): `rok, ICZ, okres_ICZ, okres_pacient,
mnozstvi`; gynekologie (63050): `rok, ICZ, okres_ICZ, mnozstvi, pacienti`. Okres „neuvedeno“
vynecháváme, Prahu slučujeme. **Kontrola:** součet mamografií po IČZ se přesně shoduje
s `nrhzs_mamografie_toky.csv`. Jeden kód IČZ řetězce může vykazovat za víc fyzických pracovišť;
notebook to řeší heuristikou (kap. 1).

### `nrpzs_gyn_okresy.csv` (NRPZS)

Národní registr poskytovatelů zdravotních služeb, sada NR-01-06 *Místa poskytování zdravotních
služeb* ([datanzis.uzis.gov.cz](https://datanzis.uzis.gov.cz/data/NR-01-NRPZS/NR-01-06/Otevrena-data-NR-01-06-nrpzs-mista-poskytovani-zdravotnich-sluzeb.csv)),
staženo 9. 10. 2026. Bereme místa s druhem zařízení „Samostatná ordinace PL – gynekologa“
(1 629 míst), sloupce `lau, gyn_ordinace, gyn_poskytovatele`. Registr obsahuje jen fungující
místa, je to tedy průřez.

### `nor_c50_kraje.csv` (Národní onkologický registr)

ÚZIS NR-07-01 *Incidence a prevalence novotvarů v regionech* a NR-07-02 *Mortalita na novotvary
v regionech* (individuální záznamy, staženo 9. 10. 2026). Bereme ženy s dg. C50. Sloupce
`ukazatel (incidence | umrti), rok, kraj, vek, stadium, n`. Věk je kód ÚZIS `66AAABBB`
(pásmo AAA–BBB let), stadium `1–4`, `X` neznámé, `Y` nestanovitelné. Okresy v otevřených datech nejsou.

### `mamocz_pracoviste_historie.csv` (mamo.cz přes web.archive.org)

Počet akreditovaných pracovišť po okresech a letech. Roky 2008–2019 ze snímků stránky
`index.php?pg=mamograficky-screening--centra--seznam` ve web.archive.org (jeden snímek za rok,
ve `sources/wayback_mamo/`; chybí 2012 a 2014), rok 2026 z `mamocz_pracoviste.csv`. Pracoviště se
páruje na okres přes obec z řádku s PSČ. Novější web (od 2020) má seznam na jiné stránce, kterou
archiv neobsahuje. Seznam uvádí akreditaci, ne provoz.

### `mamocz_cekaci_doby.csv` (mamo.cz přes web.archive.org)

Ze stejných snímků (krok `cekaci_doby` v `utils/priprava_dat.py`). Snímky 2013, 2015–2019 uváděly u každého
pracoviště objednací lhůtu („N dní“) a datum údaje („[údaj z 15.12.2018]“): 419 údajů, 67–73 pracovišť
na snímek. Sloupce `snimek, datum, lau, obec, ulice, psc, cekani_dni, text`; „bez objednání“ = 0 dní,
„neuvedeno“ = prázdné (jednou). Lhůty hlásila pracoviště sama; nejsou to měřená data.

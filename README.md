# Mamografický screening: okresy ČR a data VZP

Analýzy k výzvě VZP *Od pozvánky k mamografu* (Rakathon 2026) ve třech částech:

1. **Data VZP** (`notebooks/vzp_*.ipynb`): kdo po adresné pozvánce přijde na mamograf. CatBoost a model
   hazardu, akční segmenty, přechody mezi nimi, návrhy experimentů a prezentace.
2. **Okresy ČR** (`notebooks/mamograf_*.ipynb`): pokrytí screeningem podle okresů z veřejných dat.
3. **Literatura a koncept:** rešerše v [`PAPERS.md`](PAPERS.md) a [`docs/interventions.md`](docs/interventions.md),
   souhrn zjištění v [`docs/ZJISTENI.md`](docs/ZJISTENI.md), koncept systému cílené prevence
   v [`docs/vzp_system/system.pptx`](docs/vzp_system/system.pptx).

Repozitář vznikl vyčleněním z `mamograf-data-exploration`, kde zůstal framework `mamoframe`
(syntetická data, ekonomický model, optimalizace, notebooky `00`–`10` a `99_den_D`). Odkazy na něj
v textech jsou jen textové.

## Data VZP

Data hackathonu jsou v [`data_vzp/Rakhaton2026.csv.gz`](data_vzp/) (1 344 556 adresných pozvánek
2020–2024 pro 508 527 žen pojištěných u VZP nepřetržitě 2015–2025; popis sloupců
v [`data_vzp/Rakathon_Datove_rozhrani.md`](data_vzp/Rakathon_Datove_rozhrani.md)). Notebooky
ukazují jen agregáty.

| Notebook | Obsah |
|---|---|
| [`vzp_basic_stats`](notebooks/vzp_basic_stats.ipynb) | základní přehledy: ženy podle územních pracovišť, měsíce od posledního screeningu |
| [`vzp_catboost_shap`](notebooks/vzp_catboost_shap.ipynb) | CatBoost pro účast do 3, 6 a 12 měsíců, vysvětlení SHAP |
| [`vzp_hazard`](notebooks/vzp_hazard.ipynb) | diskrétní model přežití (hazard): jeden CatBoost místo tří modelů |
| [`vzp_final`](notebooks/vzp_final.ipynb) | finální model hazardu: každá žena váží stejně, pásma jako pořadová čísla |
| [`vzp_segmentation`](notebooks/vzp_segmentation.ipynb) | vývoj akčních segmentů (pravidla v [`config/`](config/), verze 1 a 2) |
| [`vzp_segment_transitions`](notebooks/vzp_segment_transitions.ipynb) | přechody mezi segmenty od pozvánky k pozvánce |
| [`vzp_segmentation_final`](notebooks/vzp_segmentation_final.ipynb) | finální segmentace: 11 segmentů, strom, test na roce 2024, přechody, experimenty (podklad prezentace) |
| [`vzp_segmentation_final_alt`](notebooks/vzp_segmentation_final_alt.ipynb) | alternativní verze: early stopping, graf šesti skupin, experimenty E1–E7 podle velikosti vzorku |

**Hlavní zjištění** (podrobně v [`docs/vzp_segmentace/slides.md`](docs/vzp_segmentace/slides.md)):

- **11 pravidel stačí.** Účast segmentu z let 2020–2023 seřadí ženy pozvané v roce 2024 s AUROC 0,807
  (do 12 měsíců); plný model hazardu z 19 sloupců má 0,837.
- **Účast se mezi segmenty liší 25×**, od 2–5 % (zkřížený dopis, odpojené, opakovaně nereagující)
  po 60 % (první pozvánka, v kontaktu se zdravotnictvím).
- **V roce 2024 nepřišlo 207 tisíc žen**; 59 % z nich chodí ke gynekologovi nebo na jinou prevenci.
- **Segmenty bez screeningu jsou lepkavé** (zůstává 56–83 % žen) a **první pozvánka je rozcestí**.

**Prezentace** (PowerPoint generuje `build_slides.js` vedle nich, společný vzhled v
[`docs/pptx_theme.js`](docs/pptx_theme.js)):

- [`docs/vzp_segmentace/slides.pptx`](docs/vzp_segmentace/slides.pptx): segmentace pozvaných žen (zdroj `slides.md`);
- [`docs/vzp_system/system.pptx`](docs/vzp_system/system.pptx): koncept systému cílené prevence,
  vysvětlitelný model účasti (EBM) a bayesovský model upliftu.
- [`docs/vzp_pitch/pitch_3min.pptx`](docs/vzp_pitch/pitch_3min.pptx): tříminutový pitch na šabloně W&P (generuje
  `build_pitch.py` v Pythonu); závěrečný slajd zvlášť v [`zaver.pptx`](docs/vzp_pitch/zaver.pptx).

## Okresy ČR

Explorační analýza v notebooku [`mamograf_exploration.ipynb`](notebooks/mamograf_exploration.ipynb),
revize jejích závěrů v [`mamograf_analyza.ipynb`](notebooks/mamograf_analyza.ipynb) a rozšiřující
analýzy s novými daty v [`mamograf_rozsireni.ipynb`](notebooks/mamograf_rozsireni.ipynb).
Zkoumá, jaký podíl žen 45+ v jednotlivých okresech chodí na screeningovou mamografii
a na preventivní prohlídky u praktického lékaře, jak se okresy liší a co ty rozdíly
vysvětluje: dostupnost pracovišť, socioekonomická struktura, očkování, čerpání
zdravotní péče a nemocnost.

Analýza je **ekologická**: jednotkou je okres (77 okresů), ne jednotlivá žena.
Z toho, jak se chová okres, nelze usuzovat na chování konkrétních žen.

### Hlavní zjištění

- **Pokrytí:** za dva roky (2023–2024) absolvovalo screeningovou mamografii 55 %
  žen 45+. Okresy se liší 1,7krát, od 40 % (Jeseník) po 67 % (Třebíč). Pokrytí je
  stabilní kolem 60 % do 74 let, pak prudce klesá (75–79 let 49 %, 85+ 10 %).
- **Preventivní prohlídka u praktika a mamografie spolu nesouvisejí** (r = 0,12).
  Okres, kde ženy chodí na prevenci k praktikovi, není okresem, kde chodí na
  mamograf.
- **Souvisí s ní ale jiná preventivní vyšetření.** Nejsilnější ze všech
  ukazatelů jsou preventivní gynekologické prohlídky (r = 0,46), následuje test
  na okultní krvácení (0,40) a cytologie děložního čípku (0,37). Všechny tři
  obstojí i po korekci na mnohonásobné testování. Kde ženy chodí na jedno
  preventivní vyšetření, chodí i na ostatní.
- **Dostupnost hraje menší roli.** Vzdálenost k nejbližšímu pracovišti s pokrytím
  nesouvisí. Měřený podíl žen, které jezdí na mamograf do jiného okresu, souvisí
  slabě (r = −0,30) a korekci těsně nepřežije.
- **Socioekonomické ukazatele** (vzdělání, nezaměstnanost, dávky, ceny bydlení,
  volby…) a **očkování** proti chřipce i covidu jednotlivě pokrytí nevysvětlují.
- Zhruba **pětina rozdílů mezi okresy leží mezi kraji**, což ukazuje spíš na
  organizaci péče (zvací systém pojišťoven, kapacity, praxe gynekologů) než na
  složení obyvatelstva.

Vícerozměrný model explorace (kap. 8.4) má 22 prediktorů na 77 okresů a je
přeučený. Nahrazuje ho model v revizním notebooku (níže).

### Revize závěrů (`mamograf_analyza.ipynb`)

Revizní notebook bere zjištění explorace a testuje je přísněji: věkově
standardizované pokrytí, permutační test role krajů, kapacita v dosahu (2SFCA),
model s křížovou validací, prostorová závislost a panel s pevnými efekty.

- **Platí a jsou posílená:** prevence u praktika s mamografií nesouvisí, a to ani
  v čase uvnitř okresů. S mamografií jde **preventivní chování u gynekologa**:
  průřezově (r = 0,46), v modelu (index prevence je nejsilnější prediktor) i v
  panelu. Když v okrese přibude gynekologických prohlídek o 1 %, přibude
  mamografií asi o 0,4 % (p = 0,001, drží i bez covidových let).
- **Dostupnost:** kapacita pracovišť v dosahu (2SFCA, 20–45 km) s pokrytím
  nesouvisí. Souvisí ale, **jestli má okres vlastní pracoviště** (asi +1,3 p. b.)
  a jaký podíl žen jezdí na mamograf jinam (r = −0,33).
- **Opravená data:** sedm okresů s akreditovaným pracovištěm (Benešov, Tachov,
  Teplice, Česká Lípa, Jeseník, Vsetín, Bruntál) mělo v NRHZS „dojížďku“ 100 %,
  protože řetězce vykazují výkony v okrese sídla. Vztah dojížďky s pokrytím po
  jejich vyřazení drží.
- **Role krajů:** pro pokrytí 45+ celkem je podíl rozdílů mezi kraji (22 %) jen o
  málo vyšší, než dá náhoda (17 %, permutační p ≈ 0,2), tedy **neprůkazný**.
  U žen **50–69 let** ale leží mezi kraji třetina rozdílů (p < 0,01). Regionální
  organizace péče se projevuje u jádra cílové skupiny.
- **Věková skladba** rozdíly mezi okresy nevysvětluje (standardizace posune pořadí
  v průměru o 2–3 místa). Záporný efekt průměrného věku v modelu explorace je
  artefakt přeučeného modelu.
- **Model:** model explorace vysvětlí na trénovacích datech 68 % rozptylu, mimo
  vzorek 24 %. Model s 9 prediktory podle kauzálního schématu (bez důsledků
  screeningu, jako je léčená rakovina prsu) vysvětlí mimo vzorek 29 %.
  Socioekonomika sama asi 7 %.
- **Prostor a čas:** pokrytí je prostorově shlukované (Moran I = 0,20), takže
  *p* hodnoty explorace jsou optimistické. Okresy se sbližují: variační
  koeficient mezi nimi klesl z 21 % (2010) na 8 % (2024).

Souhrnná tabulka „původní závěr → nový odhad → stav“ je v kap. 7 revizního notebooku.

### Rozšiřující analýzy (`mamograf_rozsireni.ipynb`)

Nová data: výkony NRHZS po jednotlivých IČZ, registr poskytovatelů (NRPZS), historické seznamy
pracovišť mamo.cz (web.archive.org) a Národní onkologický registr (NOR).

- **Dojížďka po opravě:** jeden kód IČZ řetězce vykazuje za víc pracovišť. Po rozdělení mají
  sporné okresy dojížďku 5–19 %, jen Jeseník (51 %) a Bruntál (44 %) zůstávají vysoko. Vztah
  dojížďky s nižším pokrytím drží (r = −0,30).
- **Kapacita:** počet pracovišť v dosahu s pokrytím nesouvisí. Provedená vyšetření v dosahu ano
  (r ≈ 0,3), ale ta jsou z velké části samo pokrytí, takže kapacitu od zájmu data neoddělí.
- **Objednací lhůty** (archiv mamo.cz 2013–2019, 419 údajů, hlásila je pracoviště sama): každému
  okresu jsme přiřadili lhůtu, kterou jeho ženy zažívají (lhůty pracovišť vážené tím, kam ženy z okresu
  jezdí). Okresy s dlouhými lhůtami mají nižší pokrytí (r ≈ −0,35; po zohlednění modelu M3 asi
  −1,1 p. b. na každých +8 dní, tj. na směrodatnou odchylku). Když se ale lhůta v okrese prodlouží,
  pokrytí neklesne. Souvislost tedy spíš odráží trvalé vlastnosti okresů (chronický nedostatek
  kapacity, organizace péče, chudoba; lhůta souvisí s nezaměstnaností žen, r = 0,38) než přímý účinek
  čekání; příčinu tato data neurčí.
- **Gynekologové:** hustota ordinací registrujících gynekologů s pokrytím nesouvisí (r = 0,05).
  Gynekologický kanál je otázka toho, co gynekologové dělají, ne kolik jich je.
- **Otevření pracoviště:** síť je od 2008 skoro beze změny (66 → 75 pracovišť). V Teplicích se po
  otevření pracoviště (2016) zavřel odstup od zbytku kraje o 2,2 p. b. (placebo p ≈ 0,09); jediný
  případ, slabý doklad.
- **Pojišťovny:** okresní ani krajská data o pojištěncích podle pojišťovny nejsou otevřená.
- **Stadium při diagnóze:** podíl karcinomů prsu ve stadiu III–IV u žen 45–74 klesl z 29 % (1995)
  na 13 % (2024), z velké části už před startem programu. Mezi kraji vztah s pokrytím nevidíme.
- **Přesnost:** small-area model (Fay–Herriot) posune okresní odhady nejvýš o 0,9 p. b.; rozdíly
  mezi okresy jsou skutečné, ne šum malých čísel.
- **Pod očekáváním** modelu jsou Frýdek-Místek, Jičín, Jeseník, Bruntál a Semily, **nad** ním
  Kroměříž, Olomouc, Pardubice, Česká Lípa, Beroun a Třebíč: kandidáti na kvalitativní srovnání.

### Podskupiny (`mamograf_podskupiny.ipynb`)

Hledá vztahy, které celek skrývá: sken 897 testů (ukazatel × věkové pásmo nebo typ okresu) s korekcí
Benjamini–Hochberg přes všechny testy, replikací 2014–2018 → 2020–2024 a testem interakce.

- **Dostupnost je problém žen 75+.** Vzdálenost k pracovišti s pokrytím v celku nesouvisí (r = −0,18),
  u žen 80+ silně (r ≈ −0,5); totéž vlastní pracoviště, dojížďka a podíl velkých měst. Interakce s věkem
  75+ je průkazná i po korekci. Většina z 20 průkazných interakcí měří jeden rozměr: město vs. venkov.
- **Podíl cizinek** souvisí s nižším pokrytím u žen 45–59 a s vyšším u 85+; v celku se to částečně ruší.
- **Změny v čase** (prevence u praktika, objednací lhůty) nepůsobí po korekci v žádném věkovém pásmu.
- **Pro experiment VZP:** předregistrovat interakci intervence × věk 75+ × vzdálenost; ostatní podskupiny
  jen exploračně. Vše je ekologické; na individuálních datech VZP to jde ověřit přímo.

### Co explorační notebook dělá

| Kapitola | Obsah |
|---|---|
| 1 · Nastavení | rozbalení dat, cesty, barvy a společný vzhled grafů |
| 2 · Lokální data ÚZIS | načtení mamografií a preventivních prohlídek, sjednocení věkových pásem |
| 3 · Doplňkové zdroje | jmenovatel (ženy v okresech, ČSÚ), hranice okresů (RÚIAN), seznam mamografických pracovišť (mamo.cz) |
| 4 · Metriky pokrytí | pokrytí mamografií za 1 a 2 roky, pokrytí prevencí, panel 2010–2024 |
| 5 · Kam ženy jezdí na mamograf | gravitační model dojížďky k pracovištím (odhad, v kap. 8 nahrazen měřením) |
| 6 · Mapy okresů | interaktivní mapa pokrytí podle věkových pásem, animace 2011–2024, mapa pracovišť |
| 7 · Korelace prevence × mamograf | celkově i po věkových pásmech, citlivostní testy |
| 8 · Socioekonomický kontext | ukazatele ČSÚ a sčítání 2021, volby 2025, výkony zdravotní péče (NRHZS); mapa, korelace s korekcí BH, regresní model, vážení počtem žen, model po věkových pásmech |
| 9 · Očkování | chřipka před covidem a po něm, covid (1. a 3. dávka); korelace a mapa |
| 10 · Korelační matice | všech 54 proměnných v jedné matici |
| 11 · Co z toho plyne | souhrnná čísla |
| 12 · Metodické poznámky | omezení dat a metod |

Každá mapa ukazuje i polohu mamografických pracovišť. Všechny grafy jsou
interaktivní (Plotly) a ukládají se také jako samostatné HTML.

Revizní notebook `mamograf_analyza.ipynb` má kapitoly: 0 kontrola shody s explorací,
1 věková standardizace, 2 role krajů, 3 dostupnost a kapacita (2SFCA), 4 model
podle kauzálního schématu, 5 prostorová závislost, 6 panel 2010–2024, 7 revize
závěrů. Data načítá přes `utils/nacteni.py`, výstupy ukládá do `outputs/analyza/`.

## Jak spustit

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/
```

Na Windows se prostředí aktivuje `.venv\Scripts\activate`. Pak spustit všechny
buňky. První buňka explorace rozbalí data z `data/*.zip` (potřebuje příkaz
`unzip`). Revizní notebook čte zipy přímo a `unzip` nepotřebuje. Každý běh trvá
zhruba minutu a nepotřebuje internet, protože data z API jsou v repozitáři jako
cache.

Notebooky `vzp_*` čtou `data_vzp/Rakhaton2026.csv.gz` přímo (pandas gzip rozbalí sám) a potřebují
`catboost` a `pyyaml`; učení modelu hazardu trvá desítky minut. Výstupy ukládají do `outputs/<notebook>/`.

Prezentace se přegenerují přes Node.js a [pptxgenjs](https://www.npmjs.com/package/pptxgenjs):

```bash
npm install pptxgenjs
node docs/vzp_segmentace/build_slides.js
node docs/vzp_system/build_slides.js
```

## Struktura repozitáře

| Cesta | Obsah | V gitu |
|---|---|---|
| `README.md` | tento soubor: zjištění a orientace | ano |
| [`DATA.md`](DATA.md) | stručný přehled dat v `data/` | ano |
| [`PAPERS.md`](PAPERS.md) | literatura: hlavní poznatky z článků, klíče `[KLÍČ]` | ano |
| `papers/people/`, `papers/methods/` | PDF volně dostupných článků (`<KLÍČ>.pdf`): studie o ženách, intervencích a nákladech / metodika (statistika, ML, design experimentů) | ano |
| `data/*.zip` | veřejná okresní data pro notebooky `mamograf_*`, každý soubor zvlášť | ano |
| `data_vzp/` | data hackathonu VZP (`Rakhaton2026.csv.gz`) a jejich popis | ano |
| `data/` (rozbalené), `sources/` | rozbalená data; velké zdrojové sady | ne |
| `notebooks/vzp_*.ipynb` | analýzy dat VZP (tabulka výše) | ano |
| `notebooks/mamograf_exploration.ipynb` | explorační notebook | ano |
| `notebooks/mamograf_analyza.ipynb` | revize závěrů explorace | ano |
| `notebooks/mamograf_rozsireni.ipynb` | rozšiřující analýzy s novými daty | ano |
| `notebooks/mamograf_podskupiny.ipynb` | podskupiny, ve kterých se skrývá účinek | ano |
| `config/segments_vzp*.yaml` | pravidla akčních segmentů (verze 1 a 2) | ano |
| `utils/` | načtení dat (`nacteni.py`), společné analytické kroky (`analyza.py`), vzhled grafů (`vzhled.py`), přepočet agregátů (`priprava_dat.py`), velikost vzorku (`power.py`) | ano |
| `docs/vzp_segmentace/`, `docs/vzp_system/`, `docs/vzp_pitch/` | prezentace (`.md`, `.pptx`, grafy a generátory), tříminutový pitch | ano |
| `docs/sources/` | prezentace týmu v41 (57 slajdů, šablona pitche) a její textový výpis | ano |
| `docs/ZDROJE_DAT.md` | původ a zpracování veřejných dat | ano |
| `docs/interventions.md` | intervence seřazené podle očekávaného účinku: proč fungují, důkazy, jak je otestovat | ano |
| `docs/ZJISTENI.md` | souhrn zjištění k 15. 10.: okresní data, literatura, ekonomika, framework na syntetice | ano |
| `docs/rakathon-mamograf-research-brief.md`, `docs/gemini_deep_research.md`, `docs/missing_papers.md` | research brief, rešerše Gemini, chybějící články | ano |
| `outputs/` | výstupy notebooků: HTML grafy, PNG a CSV | ne |

Notebooky `mamograf_*` pracují jen s daty v `data/`. Velké zdrojové sady jsou v repozitáři
jen jako okresní agregáty; skript `utils/priprava_dat.py` je potřeba jen tehdy,
když se agregáty mají přepočítat ze zdrojových dat. Podrobnosti o datech, jejich
původu a o tom, jak jsme je agregovali, jsou v [`ZDROJE_DAT.md`](docs/ZDROJE_DAT.md).

## Hlavní omezení okresní analýzy

- **Dva různé geografické klíče:** mamografie je podle okresu bydliště, preventivní
  prohlídky podle okresu pracoviště praktika (s kapitační populací jako
  jmenovatelem).
- **Výkony NRHZS nemají pohlaví ani věk,** ukazatele z nich platí pro celou
  populaci okresu. Kódy výkonů jsme určili z dat, ne z číselníku, a je potřeba je
  ověřit.
- **Nemocnost je dolní odhad** z hlavních diagnóz, vhodný jen ke srovnání okresů
  mezi sebou.
- **Praha chybí v covidových ukazatelích,** protože v datech MZ nemá vlastní ORP.
- **Dvouleté pokrytí** může ženu vyšetřenou dva roky po sobě započítat dvakrát.

- **Okres zařízení v NRHZS** je u řetězců okres sídla, ne pracoviště (viz kap. 3.1
  revizního notebooku).

Úplný seznam je v kap. 12 explorace a kap. 8 revizního notebooku.

# Co zatím víme: zjištění k 15. 10. 2026

Souhrn všeho, co projekt zatím zjistil k výzvě VZP *Od pozvánky k mamografu*: z veřejných okresních
dat, z literatury, z ekonomického modelu a z frameworku `mamoframe` nad syntetickými daty. Každé
zjištění má značku, odkud pochází a jak moc mu věřit. Framework, ekonomický model a jejich notebooky
zůstaly v původním repozitáři `mamograf-data-exploration`; odkazy na ně jsou níže jen textové.
Analýzy skutečných dat VZP jsou v notebookách `notebooks/vzp_*.ipynb` a v prezentaci `docs/vzp_segmentace/`.

| Značka | Zdroj | Co z něj lze vyvodit |
|---|---|---|
| **[okresy]** | veřejná data ČR (ÚZIS, NRHZS, ČSÚ, mamo.cz), 77 okresů | vzorce mezi okresy; *ekologické*, ne chování jednotlivých žen |
| **[literatura]** | studie v [`PAPERS.md`](../PAPERS.md) a [`interventions.md`](interventions.md) | účinky a prediktory jinde; přenos do ČR je úsudek |
| **[model]** | ekonomický kohortový model, parametry z literatury | řád hodnot a citlivost; parametry s příznakem „ověřit“ |
| **[syntetika]** | framework nad syntetickými daty | **ověřuje postup, ne realitu**; čísla nejsou odhady pro VZP |

## Deset hlavních závěrů

1. **Mamografii dělá „preventivní habitus“, ne lékař prvního kontaktu.** Kde ženy chodí na
   preventivní gynekologii, cytologii a test na okultní krvácení, chodí i na mamograf; prevence u
   praktika s mamografií nesouvisí. [okresy, literatura]
2. **Nejsilnější prediktor účasti je minulá účast.** Kdo chodil, chodí dál; kdo vynechal první
   pozvánku, chodí méně i později. [literatura]
3. **Dostupnost je problém hlavně žen 75+** a odlehlých okresů (Jeseník, Bruntál). V celku vzdálenost
   s pokrytím nesouvisí. [okresy]
4. **Okresy s dlouhými objednacími lhůtami mají nižší účast** (r ≈ −0,35), ale prodloužení lhůty
   v okrese účast nesnižuje: jde spíš o trvalé vlastnosti okresů než o účinek čekání. [okresy]
5. **Socioekonomika okresu vysvětluje málo** (asi 7 % rozdílů mimo vzorek); víc dělá organizace péče
   v kraji, u žen 50–69 let třetina rozdílů. [okresy]
6. **Nejlépe doložené intervence jsou jednoduché:** pevný termín místo otevřené pozvánky (pro VZP
   odhad +10 až +19 p. b.), navigace po telefonu (+5 až +12), SMS (+2 až +5). AI a personalizované
   zprávy zatím nemají doklad o vlivu na chování. [literatura]
7. **Jedna dodatečná mamografie ve věku 50–69 stojí asi 215–245 tis. Kč na QALY**, hluboko pod prahem
   SÚKL. Po 80 letech převáží škody. [model]
8. **Riziko neúčasti ≠ přínos intervence.** Oslovit nejrizikovější ženy dá méně než náhodný výběr;
   cílit se má podle upliftu × hodnoty − nákladu. [syntetika, literatura]
9. **První milion korun udělá většinu práce** (levné SMS a notifikace); po reformě 7/2026 ale omezí
   přínos kapacita center. [syntetika]
10. **Bez experimentu se plán přeceňuje.** Alokace podle literatury slibuje víc, než dodá; pilot s
    randomizací a aktualizací účinků po segmentech výsledek zlepší a zpřesní. [syntetika]

## 1. Okresní data ČR [okresy]

Podrobnosti a grafy: [`README.md`](../README.md), notebooky
[`mamograf_exploration`](../notebooks/mamograf_exploration.ipynb),
[`mamograf_analyza`](../notebooks/mamograf_analyza.ipynb),
[`mamograf_rozsireni`](../notebooks/mamograf_rozsireni.ipynb),
[`mamograf_podskupiny`](../notebooks/mamograf_podskupiny.ipynb).

**Kolik žen chodí**
- Za 2023–2024 absolvovalo screeningovou mamografii **55 % žen 45+**; okresy od 40 % (Jeseník) po
  67 % (Třebíč).
- Pokrytí je kolem 60 % až do 74 let, pak prudce klesá (75–79 let 49 %, 85+ 10 %).
- Věková skladba rozdíly mezi okresy nevysvětluje (standardizace posune pořadí o 2–3 místa).
- Okresy se sbližují: variační koeficient klesl z 21 % (2010) na 8 % (2024).
- Rozdíly jsou skutečné, ne šum malých čísel (small-area model posune odhady nejvýš o 0,9 p. b.).

**S čím pokrytí souvisí**
- **Preventivní gynekologie** je nejsilnější korelát (r = 0,46). Platí i v čase uvnitř okresů: o 1 %
  víc gynekologických prohlídek jde s asi 0,4 % víc mamografií (p = 0,001, i bez covidových let).
- **Test na okultní krvácení** (r = 0,40) a **cytologie** (r = 0,37) také; prevence u **praktika**
  ne (r = 0,12), ani v čase.
- **Hustota gynekologických ordinací** s pokrytím nesouvisí (r = 0,05): záleží na tom, co gynekologové
  dělají, ne kolik jich je.
- Socioekonomické ukazatele, volby a očkování proti chřipce či covidu jednotlivě pokrytí nevysvětlují.
  Model s 9 prediktory podle kauzálního schématu vysvětlí mimo vzorek 29 % rozdílů, socioekonomika
  sama asi 7 %.

**Dostupnost a kapacita**
- Vzdálenost k nejbližšímu pracovišti ani kapacita pracovišť v dosahu (2SFCA) s pokrytím v celku
  nesouvisí.
- Souvisí to, **jestli má okres vlastní pracoviště** (asi +1,3 p. b.), a podíl žen, které jezdí do
  jiného okresu (r ≈ −0,30 po opravě dat).
- **Objednací lhůty.** Každému okresu jsme přiřadili lhůtu, kterou jeho ženy zažívají: lhůty
  pracovišť z archivu mamo.cz (2013–2019, údaje hlásila pracoviště sama), vážené tím, kam ženy z okresu
  na mamograf jezdí. Okresy s dlouhými lhůtami mají nižší pokrytí (r ≈ −0,35; po zohlednění
  socioekonomiky a dostupnosti asi −1,1 p. b. na každých +8 dní). Když se ale lhůta v okrese
  prodlouží, pokrytí neklesne. Souvislost tedy spíš odráží trvalé vlastnosti okresů (chronický
  nedostatek kapacity, organizace péče, chudoba) než přímý účinek čekání; příčinu tato data neurčí.
- Otevření pracoviště v Teplicích (2016) zmenšilo odstup od kraje o 2,2 p. b. (placebo p ≈ 0,09):
  jediný případ, slabý doklad.

**Podskupiny**
- **Dostupnost je problém žen 75+:** u žen 80+ vzdálenost souvisí s pokrytím silně (r ≈ −0,5);
  interakce s věkem 75+ obstojí i po korekci na 897 testů. Většina průkazných interakcí měří jeden
  rozměr: město vs. venkov.
- Podíl cizinek souvisí s nižším pokrytím u žen 45–59 a s vyšším u 85+.
- Pro experiment VZP: **předregistrovat interakci intervence × věk 75+ × vzdálenost**.

**Kraje, prostor, výsledky**
- U žen 45+ celkem leží mezi kraji 22 % rozdílů, jen o málo víc než náhoda (17 %); u **žen 50–69 let
  třetina** (p < 0,01): regionální organizace péče se projevuje u jádra cílové skupiny.
- Pokrytí je prostorově shlukované (Moran I = 0,20), *p* hodnoty prostých korelací jsou proto
  optimistické.
- Podíl karcinomů prsu ve stadiu III–IV u žen 45–74 klesl z 29 % (1995) na 13 % (2024), z velké části
  už před startem programu; mezi kraji vztah s pokrytím nevidíme.
- **Pod očekáváním** modelu: Frýdek-Místek, Jičín, Jeseník, Bruntál, Semily; **nad ním**: Kroměříž,
  Olomouc, Pardubice, Česká Lípa, Beroun, Třebíč. Kandidáti na kvalitativní srovnání.

**Datové pasti**
- Řetězce vykazují výkony v okrese sídla: sedm okresů s vlastním pracovištěm mělo v NRHZS „dojížďku“
  100 %. Po rozdělení IČZ na pracoviště je dojížďka 5–19 %, jen Jeseník (51 %) a Bruntál (44 %) vysoko.
- Výkon 89814 se vykazuje se screeningovou mamografií 89223; počítat ho zvlášť by mamografie
  zdvojnásobilo.

## 2. Literatura [literatura]

Podrobnosti: [`PAPERS.md`](../PAPERS.md) (Část I lidé, Část II metodika) a
[`interventions.md`](interventions.md) (20 intervencí seřazených podle přínosu pro VZP).

**Kdo nechodí**
- Předchozí účast je nejsilnější prediktor (metaanalýza 66 studií: OR 3,3); ženy na první pozvánce
  chodí nejméně (OR 0,22). `[MOTTRAM2021]`
- Neúčast zvyšují dávky a důchod, narození v cizině, život bez partnera, nájem, bez auta,
  vzdálenost nad 20 km, multimorbidita a duševní nemoci; vzdělání má vliv ve tvaru U.
  `[DK_2024]`, `[DK_2012]`, `[DK_MULTIMORB2015]`
- Kdo nechodí na screening děložního čípku, má 2,8× vyšší pravděpodobnost neúčasti i u prsu.
  `[DK_CERV_BREAST]`
- Část neúčastnic má mamografii jinde (v německém RCT 51,5 % z nich). `[DE_PHONE2023]`

**Co zvyšuje účast** (odhad přínosu pro VZP navíc k dnešnímu zvaní, ne čísla ze studií)

| Intervence | Pro VZP (p. b.) | Proč |
|---|---|---|
| Pevný termín místo otevřené pozvánky | +10 až +19 | NHS: 49 % → 68 % účast; větší účinek u chudších `[NHS_TIMED2026]` |
| Balíček (připomínka + navigace + odstranění bariéry) | +8 až +18 | metaanalýzy, nejlépe u znevýhodněných `[LOWINCOME2013]` |
| Navigace po telefonu | +5 až +12 | CPSTF medián +12 p. b. `[CPSTF_NAV]` |
| Doprava, mobilní jednotka, večerní termíny | +5 až +15 lokálně | CPSTF medián +17,7 p. b. `[CPSTF_STRUCT]` |
| Seznamy žen po termínu pro lékaře | +2 až +6 | audit a zpětná vazba `[CPSTF_AF]` |
| SMS s odkazem na objednání | +2 až +5 | RCT v NHS i USA `[NHS_SMS2015]`, `[PENN_OUTREACH2024]` |
| AI / LLM zprávy | 0 až +2 navíc | zvedají záměr, ne chování `[LLM_HPV2025]`, `[RISKMSG_CRC2025]` |
| Finanční pobídky, masová média, návštěvy doma | ~0 | `[US_INCENTIVE2015]`, `[CPSTF_MASSMEDIA]` |

**Metodika**
- Vysvětlitelný model (SHAP, aditivní modely) je standard; pro cílení se odhaduje heterogenní
  účinek (meta-learnery, causal forest), ne riziko. `[METALEARNERS2019]`, `[CAUSAL_FOREST2018]`
- Účinek ověřovat pevně randomizovaným experimentem s chráněnou kontrolou, ne adaptivní
  randomizací `[ADAPTIVE_RAND2015]`; změnu pravidel (žádanka 7/2026) přerušenou časovou řadou
  `[ITS_GUIDELINE2022]`.

## 3. Ekonomika jedné dodatečné mamografie [model]

Model posunu stadia s Markovovou kohortou (`mamoframe/econ`, notebook
`05_ekonomika_qaly` v původním repozitáři `mamograf-data-exploration`); průměrné parametry, práh SÚKL
1,2 mil. Kč/QALY (reálně ~0,78 mil. Kč v cenách 2026).

| Věk | QALY na 1 000 mamografií | Kč na mamografii (vč. léčby) | Kč/QALY | Mamografií na 1 odvrácené úmrtí |
|---|---|---|---|---|
| 45–49 | 3,5 | 1 125 | 325 tis. | 3 535 |
| 50–54 | 4,3 | 1 048 | 244 tis. | 2 448 |
| 55–59 | 4,3 | 1 000 | 233 tis. | 2 071 |
| 60–64 | 4,3 | 934 | 216 tis. | 1 662 |
| 65–69 | 3,8 | 902 | 239 tis. | 1 492 |
| 70–74 | 2,7 | 949 | 357 tis. | 1 564 |
| 75–79 | 1,4 | 1 076 | 757 tis. | 1 912 |
| 80–84 | 0,4 | 1 280 | 3,2 mil. | 2 845 |
| 85+ | −0,3 | 1 536 | škodí | 5 818 |

- **Shoda s EUROSCREEN:** bez předpokladu, že 30 % žen by přišlo samo, vychází 1 odvrácené úmrtí na
  1 040–1 710 mamografií ve věku 50–69; EUROSCREEN udává 1 100–1 400.
- **Screening sám sebe nezaplatí**, pokud je léčba metastatického onemocnění levná (starší český zdroj,
  123 tis. Kč/rok). Při nákladech moderní léčby (~1,5 mil. Kč/rok) se dodatečná mamografie ve věku
  65–74 zaplatí sama a ve věku 55–74 klesnou Kč/QALY pod polovinu.
- Nejvíc výsledek ovlivňuje, kolik žen by přišlo i bez intervence, doba preklinické fáze, incidence a
  podíl overdiagnóz (tornádo v notebooku 05). Parametry s příznakem „ověřit“ jsou v
  `config/econ_params.yaml` v původním repozitáři `mamograf-data-exploration`.

## 4. Framework nad syntetickými daty [syntetika]

Syntetická data jsou kalibrovaná na okresní data ÚZIS a znají „pravý“ účinek intervencí, takže na nich
jde ověřit, jestli postup funguje. **Čísla nejsou odhady pro VZP.** Notebooky
`00`–`10` v původním repozitáři `mamograf-data-exploration`.

- **Model:** AUC 0,86, kalibrace dobrá. Splajnová logistická regrese je skoro stejně přesná jako
  LightGBM (AUC 0,857 vs. 0,861), takže stačí vysvětlitelný model. „Počet pozvánek“ je silný
  prediktor, ale marker, ne příčina (pojišťovna zve ty, kdo nechodí).
- **Riziko ≠ uplift:** pevný termín pro 20 % nejrizikovějších žen přinese 32 dodatečných mamografií na
  1 000 oslovených, náhodný výběr 83, cílení podle upliftu z priorů 137, dokonalá znalost 181.
- **Rozpočet:** první milion korun (levné SMS a notifikace) přinese asi 70 % přínosu pětimilionové
  kampaně; další peníze jdou do dražšího kontaktu.
- **Kapacita:** volná kapacita center (~10 %) se zaplní až kolem 15–20 mil. Kč; **po reformě 7/2026**
  (odhad +5–8 p. b.) ale hned a kampaň nemá kam ženy poslat. S rozšířením kapacity o 30 % se kampaň
  opět vyplatí.
- **Rovnost:** podmínka „≥ 30 % přínosu pro ženy, které nikdy nebyly“ stojí při malém rozpočtu asi
  40 % vyšetření, od 5 mil. Kč skoro nic.
- **Experiment:** alokace podle literatury slibuje 21,7 tis. dodatečných mamografií a dodá 17,5 tis.;
  po pilotu a bayesovské aktualizaci účinků po segmentech dodá 20,3 tis. a slib odpovídá skutečnosti
  (strop při dokonalé znalosti 23,4 tis.). Individuální uplift modely z pilotu o tisících žen na
  rameno jsou zatím příliš hlučné; segmentový posterior je spolehlivější.
- **Velikost experimentu:** na rozdíl 3 p. b. stačí asi 3–4 tisíce žen na rameno; úzkým místem je
  logistika a kapacita, ne síla testu. Intervence přes praktiky randomizovat po praxích.
- **SMS:** česká diakritika vynutí kódování UCS-2, takže skoro každá zpráva stojí 2 SMS; bez diakritiky 1.

## 5. Co rozhodnou až data VZP

| Otázka | Proč je otevřená | Jak ji data VZP rozhodnou |
|---|---|---|
| Platí „preventivní habitus“ i u jednotlivých žen? | okresní data jsou ekologická | model rizika: příspěvek gynekologie, cytologie, TOKS |
| Jak velký je skutečný účinek dnešní pozvánky? | literatura měří proti „žádné pozvánce“ | graf reakce na pozvánku v `mamoframe profile`, přirozené experimenty v načasování |
| Je vzdálenost bariéra jen pro ženy 75+? | okresní interakce, ne jednotlivci | podskupiny v modelu i v experimentu |
| Kolik vypadlých žen chodí jinam (samoplátci, diagnostika)? | v Německu polovina neúčastnic | diagnostické mamografie ve výkonech |
| Jaký je návyk po první mamografii? | v modelu prior 0,55 | podíl žen, které přijdou v dalším kole |
| Kolik stojí kanály a jaká je kapacita center? | v konfiguraci jsou odhady | otázky na mentory (runbook) |

## Kde je co

- Analýzy dat VZP: notebooky `notebooks/vzp_*.ipynb`, prezentace [`vzp_segmentace/`](vzp_segmentace/), koncept systému [`vzp_system/`](vzp_system/)
- Framework `mamoframe`, postup pro den D a ekonomický model: původním repozitáři `mamograf-data-exploration`
- Data a jejich původ: [`DATA.md`](../DATA.md), [`ZDROJE_DAT.md`](ZDROJE_DAT.md)

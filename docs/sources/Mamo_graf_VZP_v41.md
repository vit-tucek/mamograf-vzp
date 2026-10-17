# Mámo, graf! VZP v41: text všech slajdů

Textový výpis `Mamo_graf_VZP_v41.pptx` (57 slajdů): texty, tabulky, data grafů a poznámky řečníka.
Obrázky nejsou zahrnuty. Pořadí shape odpovídá souboru.

## Slajd 1

- Mámo, graf! / Od pozvánky k mamografu
- Rakathon 2026 · výzva Všeobecné zdravotní pojišťovny ČR · návrh řešení

> Poznámky: 15 s. Představit název a výzvu. Tým na dalším slajdu, ve 3minutové verzi přeskočit.

## Slajd 2

- TÝM
- Kdo za návrhem stojí
- Spojujeme data science, analýzu dat z veřejného zdravotnictví a byznysovou praxi. Segmentaci a datově řízenou komunikaci jsme už nasazovali u klientů.
- Jakub Weiner
- BI stratég a hlavní analytik
- Přes 12 let datových projektů, dříve KPMG a Data Mind. Lektor Data Science na Masarykově univerzitě a Associate Fellow Centra pro studium demokracie.
- Michaela Pejšová
- Data Scientist · ML+AI
- Od datového inženýrství po strojové učení a optimalizace. Velkým jazykovým modelům se věnuje pátým rokem. Informatika (AI a Data Science) na FEL ČVUT.
- Vít Tuček
- Data Scientist · ML+AI
- Ph.D. z Matematického ústavu UK, po postdoktorském pobytu v Záhřebu. Ve W&P strojové učení a implementace AI do automatizace.
- JR
- Jakub Rambousek
- IT stratég a AI expert
- Přes 10 let IT projektů od průmyslového softwaru po e-commerce. Řízení vývoje, datová analytika a AI automatizace.

> Poznámky: 15 s. Fotku Jakuba Rambouska doplnit z WP_Intro_prezentace_v3.pptx (v podkladech chyběla). Ve 3minutové verzi slajd přeskočit nebo přesunout do přílohy.

## Slajd 3

- SHRNUTÍ
- Naše odpovědi na zadání VZP
- Zadání: předpovědět, kdo nedorazí, najít příčiny, rozdělit klientky do využitelných skupin, navrhnout cílenou podporu a experiment, který ověří, zda zvýšila účast.
- 1
- Predikce
- Vysvětlitelný model určí, kdo po pozvánce nepřijde (AUC 0,83).
- 2
- Příčiny
- S věkem mizí gynekolog, tedy hlavní cesta k mamografu. Praktik ho nenahrazuje a oslovení dopisem přestává fungovat.
- 3
- Segmenty
- Ženy dělíme do sedmi segmentů podle vztahu k prevenci a stavu ve zvaní. 59 % žen, které nepřišly, zdravotnickým systémem prochází a jsou tedy dosažitelné.
- 4
- Podpora
- Obratem lze zavést úpravy do systému a kanálů zvaní, souběžně pilotovat snadné objednání a zapojení lékařů.
- 5
- Experiment
- Ženy uvnitř segmentů náhodně rozdělíme proti dnešnímu dopisu; výsledek změříme z vykázaných výkonů VZP.

> Poznámky: 40 s. Pět karet odpovídá pěti částem zadání a pořadí slajdů. 3minutová verze: slajdy 3, 6, 8, 9, 13 a 14.

## Slajd 4

- Architektura systému
- Monitoring a experimenty / vyhodnocení celého systému, plánování a řízení pokusů
- Provoz / dosah a odezva kanálů, účast podle segmentů a regionů
- Ekonomika / náklady, cena za vyšetření navíc, ICER / NMB, dopad na rozpočet
- Zdraví / záchyt v časnějším stadiu, odvrácená úmrtí, QALY, vytížení kapacit
- Experimenty / design, randomizace, kontrolní skupina, vyhodnocení, rozšíření
- Komunikace VZP ↔ klient / Ven: dopis, e-mail, aplikace VZP (push, rezervace), SMS, telefonát / navigace, předrezervovaný termín / Zpět: odezva, rezervace termínu, odhlášení, preference kanálu, odpovědi v dotaznících
- Komunikace VZP ↔ poskytovatelé / Ven: seznamy klientů pro praktiky a specialisty, objednání u poskytovatele / Zpět: vykázané výkony (výsledek: přišel / nepřišel, nález), volné kapacity
- Model v VZP
- Zdravotní rizika / jaké nemoci a jak moc hrozí (z historie péče)
- Pravděpodobnost účasti / přijde klient k prevenci sám, bez zásahu?
- Uplift intervencí / o kolik účast zvýší každá intervence
- Optimalizace: kdo dostane co, kdy a jakým kanálem, v mezích rozpočtu, kapacit a rovnosti
- intervence
- odezva
- seznamy
- výkony
- predikce, rozhodnutí
- výsledky pokusů

> Poznámky: Uprostřed je model, který pro každého klienta počítá tři věci: zdravotní rizika (z historie péče, diagnóz, léků), pravděpodobnost, že k prevenci přijde sám, a uplift, tedy o kolik účast zvýší každá intervence (dopis, e-mail, push, SMS, telefonát nebo navigace, předrezervovaný termín, oslovení přes praktika nebo specialistu). Optimalizace z toho sestaví plán: kdo dostane co, kdy a kterým kanálem, v mezích rozpočtu, kapacit a požadavků na rovnost.  Vlevo komunikace s klienty: výstupem jsou intervence, vstupem odezva, rezervace a odhlášení. Vpravo poskytovatelé: seznamy klientů a objednávání, zpět vykázané výkony, které jsou zároveň výsledkem (přišel / nepřišel) pro učení modelu.  Nahoře monitoring: provoz, ekonomika (náklady, cena za vyšetření navíc, ICER a čistý peněžní přínos, dopad na rozpočet) a zdravotní výsledky (stadium při záchytu, odvrácená úmrtí, QALY, kapacity). Součástí je plánování a řízení experimentů s trvalou kontrolní skupinou; jejich výsledky se vracejí do modelu jako aktualizované odhady účinků.

## Slajd 5

- Aplikace VZP: přímý kanál a zpětná vazba
- Co aplikace doručí
- 1
- Rezervace jedním klepnutím / předrezervovaný termín: potvrdit, přesunout, uvolnit; uvolněné termíny se vrací poskytovateli
- 2
- Dotazník bariér → cílený krok / „Co vám brání?“ → navigace telefonem, večerní termín, doprava, vysvětlení „bez žádanky“
- 3
- Přehled prevence / vše, co klienta čeká: screeningy, preventivní prohlídky, očkování na jednom místě
- 4
- Připomínky a obsah / stejné zprávy jako SMS a dopis, zdarma, s rezervací na jedno klepnutí a variantami k testování
- Co se vrací do VZP / Důvody, proč klient nepřišel: znaky pro segmentaci a model upliftu / Zkušenost po vyšetření: kvalita poskytovatelů, návyk / Dosažitelnost kanálů: komu co funguje, omezení pro optimalizaci / Platforma pro pokusy: levná randomizace, zaznamenané přiřazení, signály za dny
- Pozor: uživatelé aplikace jsou výběr: chodí častěji a nejtěžší segmenty zastihne aplikace nejméně, takže výsledky platí jen pro ně a dopis, SMS ani telefon nenahradí. Krátké a řídké dotazníky (únava, zkreslení odpovědí), souhlas s využitím odpovědí (GDPR). Výsledek měřit vykázaným výkonem, ne kliknutím.

> Poznámky: Aplikace VZP má mezi klienty dobrý dosah (zhruba 700 tisíc uživatelů; aktivita a podíl v cílových skupinách zatím nejsou známé) a VZP ji chce rozvíjet jako přímý kanál včetně zpětné vazby. Samotná push notifikace je slabá intervence: ve studii ze Singapuru na ni kliklo jen 4 % adresátek. Hodnota aplikace je jinde. Zaprvé jako levný kanál pro intervence, které fungují: předrezervovaný termín, který klient jedním klepnutím potvrdí, přesune nebo uvolní (uvolněné termíny se vracejí poskytovateli, což snižuje hlavní náklad předrezervace); dotazník bariér, podle jehož odpovědi následuje cílený krok (navigace telefonem jen tam, kde ji telefonát vyřeší); přehled všech preventivních programů na jednom místě; levné varianty zpráv. Zadruhé jako zdroj zpětné vazby: důvody neúčasti jako znaky pro model upliftu, zkušenost po vyšetření pro sledování kvality, dosažitelnost kanálů a platforma pro průběžné randomizované pokusy. Pozor na samovýběr uživatelů, zkreslení a únavu z dotazníků a na souhlas s využitím odpovědí.

## Slajd 6

- Model pravděpodobnosti účasti: vysvětlitelný (EBM)
- logit p(x) = β0 + Σ fj(xj) + Σ fij(xi, xj)     Explainable Boosting Machine: zobecněný aditivní model s vybranými interakcemi, učený boostingem
- *Graf: Měsíce od poslední prevence* (kategorie: 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60)
  - Měsíce od poslední prevence: 0.6, 0.55, 0.42, 0.22, 0.02, -0.18, -0.36, -0.5, -0.6, -0.66, -0.69
- *Graf: Kontakty se zdravotnictvím za rok* (kategorie: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12)
  - Kontakty se zdravotnictvím za rok: -0.62, -0.34, -0.14, 0.02, 0.13, 0.21, 0.26, 0.31, 0.33, 0.34
- *Graf: Věk* (kategorie: 45, 50, 55, 60, 65, 70, 75)
  - Věk: -0.28, -0.06, 0.12, 0.22, 0.24, 0.12, -0.12
- Jak číst / Každá křivka je příspěvek jednoho znaku k logitu. Predikce klienta je jejich součet, takže je přesně vidět, proč vyšla. Křivky jsou ilustrativní.
- Skleněná skříňka: model je přímo čitelný, rozklad predikce je přesný (ne dodatečná aproximace jako SHAP nad černou skříňkou). / Přesnost na tabulkových datech blízko gradient boostingu, dobře kalibrované pravděpodobnosti pro optimalizaci a ekonomiku. / Kontrola: monotónní omezení, úprava křivek s lékaři, kontrola férovosti podle regionů a skupin. / Regulace: vysvětlení pro klienta, lékaře i regulátora (GDPR čl. 22, AI Act). / Prior pro uplift: logit EBM je výchozí bod modelu účinku intervencí (další snímek).
- Zvážené alternativy: logit se splajny (málo pružný), skórkarta (méně přesná), GBM + SHAP (jen dodatečné vysvětlení; zůstává jako měřítko ceny vysvětlitelnosti).

> Poznámky: Pro pravděpodobnost účasti doporučuji Explainable Boosting Machine (InterpretML): zobecněný aditivní model s vybranými dvojicovými interakcemi, učený boostingem. Každý znak má vlastní křivku, kterou lze číst, ověřit s lékaři a případně upravit. Predikce jednoho klienta se přesně rozloží na příspěvky znaků. Přesnost bývá blízko gradient boostingu a pravděpodobnosti jsou dobře kalibrované, což potřebuje optimalizace i ekonomika. Lze vynutit monotónnost (čím déle od poslední prevence, tím nižší pravděpodobnost) a zkontrolovat férovost. Pro různé horizonty (3, 6, 12 měsíců) buď jeden model na horizont, nebo diskrétní model v čase. GBM se SHAP necháváme jako měřítko: ukáže, kolik přesnosti nás vysvětlitelnost stojí. Křivky na snímku jsou ilustrativní, ne z dat.

## Slajd 7

- Model upliftu: bayesovský, s modelem účasti jako priorem
- Model účasti (EBM) / f(x): výchozí logit klienta, prior pro uplift
- Literatura / β (průměrný účinek intervence): prior z metaanalýz
- Bayesovský hierarchický model / logit P(účast | x, k) = f(x) + βk + gk(x) / τk(x) = σ(f + βk + gk) − σ(f) / gk(x): rozdíly v účinku mezi klienty na stejných znacích jako EBM, prior smrštěný k nule. Uplift je malý u těch, kdo přijdou vždy nebo nikdy, největší uprostřed.
- Randomizované pokusy / zaznamenaná pravděpodobnost přiřazení → posterior
- Rozhodnutí / τ × zdravotní přínos − náklad, v mezích rozpočtu, kapacit a rovnosti
- průzkum ~10 %
- Později, s dostatkem dat: DR-learner + causal forest
- Proč randomizace / Data VZP ukážou, kdo přichází, ale ne kdo přijde díky intervenci: kanály nikdy nebyly přidělené náhodně. Uplift se proto učí z pokusů.
- Vyhodnocení / Qini / AUUC a kalibrace upliftu po decilech, hodnota pravidla cílení off-policy (DR), trvalá kontrolní skupina.
- Rizika / Negativní uplift („sleeping dogs“), pořadí kanálů (dopis → SMS → telefonát), posun v čase, férovost.

> Poznámky: Klíčové omezení: bohatá data VZP (roky vykázané péče, diagnózy, léky, registrace, historie prevence, dřívější pozvánky a odezvy, dosažitelnost kanálů, region) dobře předpovídají, kdo přijde. Neřeknou ale, kdo přijde díky intervenci, protože kanály nebyly přidělované náhodně. Uplift naučený jen z historie by byl zkreslený.  Proto: (1) každá kampaň randomizuje a zaznamenává pravděpodobnost přiřazení; trvalý podíl průzkumu (např. 10 %) a Thompson sampling; libovolné pravidlo cílení lze pak vyhodnotit offline. (2) Jádrem je bayesovský hierarchický model na škále logitu: f(x) je logit z modelu účasti (EBM) jako pevný offset a prior, β_k průměrný účinek intervence s priorem z literatury, g_k(x) rozdíly mezi klienty na stejných znacích jako EBM, smrštěné k nule (horseshoe, částečné sdílení). Před prvním pokusem je prior upliftu plně dán EBM a literaturou; každý pokus posune posterior. Uplift zůstává vysvětlitelný. (3) Až bude randomizovaných dat dost: víceramenný DR-learner na gradient boostingu (EBM jako model kontrolního ramene), causal forest pro intervaly spolehlivosti, při velkých datech vícehlavá neuronová síť. (4) Cílí se na zdravotní hodnotu, ne na samotnou účast: τ_k(x) krát zdravotní přínos vyšetření pro daného klienta minus náklad, v mezích rozpočtu, kapacit a rovnosti. (5) Vyhodnocení: Qini / AUUC, kalibrace upliftu, DR off-policy hodnota pravidla, trvalá kontrolní skupina. (6) Rizika: negativní uplift, pořadí a kombinace kanálů (později dynamický režim / kontextový bandit), posun v čase, férovost.

## Slajd 8

- Postup zavedení
- 1
- Priory / model účasti (EBM) a účinky intervencí z literatury
- 2
- Pilotní pokus / víceramenná RCT po segmentech, levně i v aplikaci VZP, zaznamenané pravděpodobnosti přiřazení
- 3
- První model upliftu / bayesovský posterior: kdo na co reaguje
- 4
- Cílení s průzkumem / optimalizace podle zdravotní hodnoty, ~10 % průzkum, trvalá kontrolní skupina
- 5
- Učení dokola / pravidelné přeučení, vyhodnocení v monitoringu, rozhodnutí o rozšíření
- Monitoring běží od prvního dne: provoz, ekonomika a zdravotní výsledky, vždy proti kontrolní skupině.

> Poznámky: Začneme s tím, co máme: model účasti z historických dat a účinky intervencí z literatury. Pilotní pokus s několika rameny po segmentech dá první posterior. Pak cílíme podle zdravotní hodnoty, s trvalým průzkumem a kontrolní skupinou, a model pravidelně přeučujeme. Monitoring sleduje provoz, ekonomiku a zdravotní výsledky od začátku.

## Slajd 9

- Otázka a data
- 1 344 556
- pozvánek 2020–2024
- 508 527
- žen nepřetržitě pojištěných
- 256 466
- žen v testovacím roce 2024
- Otázka / Kdo po adresné pozvánce přijde na mamograf a kdo ne? Kde jsou ženy, které nechodí, a jak je oslovit?
- Data / Pozvánky VZP 2020–2024 pro ženy nepřetržitě pojištěné 2015–2025. Účast = mamografie do 3, 6 a 12 měsíců po pozvánce.
- Segmentační model / 11 srozumitelných pravidel nad sloupci VZP. Pozvánka patří do prvního segmentu, jehož pravidlo platí.
- Poctivé ověření / Model „naučený“ na letech 2020–2023 (účast segmentu) a otestovaný na roce 2024 (256 466 žen).

## Slajd 10

- Segmentační model: 11 segmentů jako rozhodovací strom
- Tři rozměry / Historie screeningu, kontakt se zdravotnictvím a prevencí a počet nevyslyšených pozvánek.
- 25×
- Tolikrát se liší účast mezi listy stromu (2–60 %).

## Slajd 11

- Kde jsou ženy? (2024: 207 tisíc nepřišlo)
- 56 % nepřišlých je ve čtyřech segmentech s účastí 3–10 %. Největší je „jiná prevence, opakovaně nereaguje“: 56,8 tis. žen. / 59 % nepřišlých chodí ke gynekologovi nebo na jinou prevenci, takže je lze oslovit přes lékaře. / Nejslibnější střed: gynekolog, zvaná málokrát (22,7 tis. nepřišlých, účast 27 %) a jiná prevence, zvaná málokrát (25,7 tis., 13 %).

## Slajd 12

- Uvnitř segmentů: kde má smysl individuální cílení
- Široký rozptyl / První pozvánky, vypadlé a ženy u gynekologa. Tam má smysl cílit podle modelu (AUROC uvnitř 0,63–0,79).
- Úzký a nízký rozptyl / Nereagující, odpojené a ženy bez prevence. 90 % z nich má predikci pod 15 %, podskupina, která by chodila, v nich není.

## Slajd 13

- Hlavní tok: pět největších segmentů
- 1. pozvánka (57 % přijde) → gynekolog / jiná prevence, zvaná málokrát (26 % / 12 %) → jiná prevence, nereaguje (4 %, 74 % zůstává).
- Zpětná hrana z „nereaguje“ chybí: co se nezíská brzy, už se skoro nezíská.

## Slajd 14

- Hlavní zjištění (1/2)
- 1
- 11 pravidel stačí. AUROC 0,807 na roce 2024 proti 0,837 plného modelu. Segmenty jsou stabilní v čase.
- 2
- Účast se liší 25×: 60 % u první pozvánky v kontaktu se zdravotnictvím, 2–5 % u zkřížených dopisů, odpojených a opakovaně nereagujících.
- 3
- 59 % nepřišlých chodí ke gynekologovi nebo na jinou prevenci. Jsou dosažitelné jinou cestou než dopisem.
- 4
- Zkřížené dopisy: 7 600 dopisů ročně (3 %) jde ženám, které screening měly 0–1 měsíc předem.

## Slajd 15

- Hlavní zjištění (2/2)
- 5
- Segmenty bez screeningu jsou „lepkavé“. Ve stejném segmentu zůstává 56–83 % žen. Každý rok sestoupí 9–15 % „zvaných málokrát“ do „opakovaně nereaguje“.
- 6
- První pozvánka je rozcestí. Přijde 57 % žen v kontaktu se zdravotnictvím, ale jen 31–36 % žen s málo kontakty. Z nich je 13 % příští rok odpojených.
- 7
- Model uvnitř segmentu pomůže jen tam, kde je rozptyl: u první pozvánky, vypadlých a žen u gynekologa.
- 8
- Intervenovat co nejdřív v toku: první pozvánka a „zvaná málokrát“, dokud žena nesestoupí.

## Slajd 16

- Návrhy experimentů (1/2)

| # | Segment (2024) | Intervence | Účast 12M | MDE* |
|---|---|---|---|---|
| 1 | Dopis se minul (7 600) | Ověřit screening těsně před odesláním, dopis odložit | 2 % | procesní změna |
| 2 | 1. pozvánka, málo kontaktů (7 100) | SMS / telefonát navíc k dopisu | 36 % | 3,2 p. b. |
| 3 | 1. pozvánka, v kontaktu (30 300) | Lepší dopis: informace, sociální norma, předvyplněný termín | 60 % | 1,6 p. b. |
| 4 | Gynekolog, zvaná málokrát (31 100) | Seznam pacientek gynekologovi, žádanka při prohlídce (klastrová RCT) | 27 % | 1,4 p. b.** |

- * nejmenší zjistitelný rozdíl při rozdělení ročníku segmentu napůl (α = 0,05, síla 80 %) · ** bez design efektu klastrů

## Slajd 17

- Návrhy experimentů (2/2)

| # | Segment (2024) | Intervence | Účast 12M | MDE* |
|---|---|---|---|---|
| 5 | Gynekolog, opakovaně nereaguje (19 900) | Objednání přímo v ordinaci místo dopisu | 10 % | 1,2 p. b. |
| 6 | Jiná prevence, opakovaně nereaguje (59 900) | 3 ramena: dopis / praktik / bez dopisu (non-inferiorita) | 5 % | 0,5 p. b. |
| 7 | Vypadlá 3–4 roky (16 200) | Připomínka s konkrétním termínem (implementation intention) | 39 % | 2,2 p. b. |

- Společné výstupy: účast do 3 / 6 / 12 měsíců, sestup do horšího segmentu při další pozvánce, náklad na získanou mamografii. Randomizace uvnitř segmentu s rozvrstvením podle územního pracoviště, analýza ITT.

## Slajd 18

- Návrhy experimentů v aplikaci VZP

| # | Zásah (jen uživatelky aplikace) | Cílové ženy za rok | Výchozí účast | MDE* při 10 / 20 / 30 % v aplikaci |
|---|---|---|---|---|
| A1 | Rezervace v aplikaci: předrezervovaný termín, potvrzení jedním klepnutím (1. pozvánky, vypadlé 3–4 roky) | 53 600 | 34,5 % (6M) | 3,7 / 2,6 / 2,1 p. b. |
| A2 | Push vs SMS × odkaz na rezervaci, faktoriál 2 × 2 (všechny segmenty kromě zkříženého dopisu) | 248 900 | 19,7 % | 1,4 / 1,0 / 0,8 p. b. |
| A3 | Dotazník bariér → cílený další krok, ženy bez účasti do 3 měsíců („zvaná málokrát“, vypadlé 4–5+ let) | 67 600 | 14,8 % (3.–12. měsíc) | 2,5 / 1,8 / 1,4 p. b. |

- * nejmenší účinek, který pokus spolehlivě odhalí, když polovina uživatelek aplikace v cílových segmentech za rok dostane zásah a polovina zůstane kontrolou (α = 0,05, síla 80 %). Podíl uživatelek aplikace mezi pozvanými ženami zatím neznáme.
- Samotná push je slabá (0 až +1 p. b.); aplikace má smysl jako levný kanál pro předrezervaci a navigaci a jako zdroj důvodů neúčasti. / Výsledky platí jen pro uživatelky aplikace; nejtěžší segmenty zastihne nejméně.

## Slajd 19

- PROBLÉM
- Starší ženy chodí po pozvánce méně, výskyt přitom roste
- Po pozvánce VZP přijde do 12 měsíců 32 % zvaných žen ve věku 45–49 let a 10 % v 70–74 letech. Ženy od 75 let data VZP neobsahují, výskyt karcinomu prsu přitom vrcholí v 75–79 letech.
- *Graf: Účast po pozvánce VZP (sloupce, %) a nové případy na 100 tis. žen (čára)* (kategorie: 45–49, 50–54, 55–59, 60–64, 65–69, 70–74, 75–79, 80–84, 85+)
  - Účast do 12 měsíců po pozvánce VZP (%): 31.9, 14.3, 12.3, 11.5, 10.4, 9.7, , , 
  - Nové případy na 100 tis. žen: 192, 194, 210, 250, 305, 356, 367, 300, 239
- 15,5 % vs. 0,7 %
- karcinomů ve stadiu IV u žen, které na screeningu nikdy nebyly, a u žen v pravidelném screeningu
- ≈ 8 000
- nových případů karcinomu prsu ročně; ženy 70+ tvoří 38 % z nich
- Pozdní záchyt znamená náročnější léčbu i horší prognózu.
- Zdroj: data VZP pro Rakathon 2026, pozvánky 2024 (účast); SVOD/NOR a ČSÚ (incidence 2020–2024); ÚZIS (stadia 2015–2017); naše analýza

> Poznámky: 45 s. Účast: podíl zvaných žen s vykázanou mamografií do 12 měsíců po pozvánce VZP v roce 2024 (vzp_final.ipynb, buňka 14): 45–49 let 31,9 %, 50–54 14,3 %, 55–59 12,3 %, 60–64 11,5 %, 65–69 10,4 %, 70–74 9,7 %. Skupinu 40–44 let (9 361 žen, 57,8 %) neukazujeme, incidence pro ni v grafu není. Skok mezi 45–49 a 50–54 je z velké části efekt první pozvánky, ne jen věku. Data VZP obsahují jen zvané ženy mimo doporučený interval, celou populaci popisuje pokrytí ÚZIS. Incidence: nové případy C50 na 100 tis. žen, průměr 2020–2024. Stadia: Evaluační zpráva ÚZIS 2022, obr. 18, ze známých stadií.

## Slajd 20

- PŘEDPOVĚĎ
- Kdo nepřijde, předpovíme vysvětlitelným modelem
- Model jsme naučili na pozvánkách VZP z let 2020–2023 a ověřili na roce 2024. Data obsahovala 1,34 mil. pozvánek pro 508 tis. žen.
- AUC 0,83
- schopnost seřadit ženy podle šance, že přijdou (test na roce 2024)
- 67 % vs. 2 %
- účast v horním a dolním decilu skóre
- 58 %
- všech účastí přinese horních 20 % pozvánek podle skóre
- Proč logistická regrese
- Složitější model (gradient boosting) přidá jen 0,005 AUC. / Bodovou kartu VZP spočítá v SQL nebo v Excelu, bez nového IT. / Model přežití s vysvětlením SHAP potvrzuje stejné faktory.
- Na co si dát pozor
- Model říká, kdo přijde, ne komu intervence pomůže. To ukáže až experiment. / Kalibraci je potřeba pravidelně přepočítávat.
- Zdroj: data VZP pro Rakathon 2026, pozvánky 2020–2024; naše analýza

> Poznámky: 60 s. Logistická regrese: AUC 0,830 (12 měsíců), boosting 0,836. Bodová karta AUC 0,828. Kalibrace 2024: předpověď 17,5 % vs. skutečnost 19,2 %. Uvnitř segmentů AUC 0,63–0,74. Zdroje: docs/RAKATHON_MODEL.md, notebooks/vzp_final.ipynb.

## Slajd 21

- HLAVNÍ PŘÍČINY
- S věkem mizí gynekologická prevence; praktik na mamograf neposílá
- Mezi ženami, které VZP zve, klesá s věkem podíl těch s preventivní prohlídkou u gynekologa ze 61 % na 15 %. Prevence u praktika zůstává kolem 40 %, s účastí ale nesouvisí.
- *Graf: Podíl zvaných žen s preventivní prohlídkou podle věku (%), 2024* (kategorie: 45–49, 50–54, 55–59, 60–64, 65–69, 70–74)
  - Gynekologická prevence za 24 měsíců: 60.9, 37.8, 27, 19.8, 16, 14.8
  - Prevence u praktika za 24 měsíců: 42.8, 41.6, 42.2, 40.2, 42.3, 42.4
- 1,4–1,6×
- vyšší šance přijít u žen s gynekologickou prevencí, v každém věku
- 1,0×
- šance u žen s prevencí u praktika: praktik je dnes na mamograf zjevně neposílá
- 0 Kč
- dostává gynekolog za účast pacientek na mamografickém screeningu
- Zdroj: data VZP pro Rakathon 2026, pozvánky 2024; úhradová metodika VZP pro gynekology 2026; naše analýza

> Poznámky: 60 s. Poměry šancí po věkových pásmech: gynekologická prevence OR 1,43–1,62, prevence u praktika 0,96–1,07 (rakathon_model.ipynb). Úhrady: měsíční agregovaná úhrada 118 Kč (VZP 120 Kč) za ženu s preventivní prohlídkou za 24 měsíců, bonus 4 Kč (VZP 5 Kč) při 45 % prohlídek; mamografický screening v úhradě gynekologa samostatně není, kolorektální ano (Metodika pro PZS – úhrady gynekologie 2026, s. 3, 8, 11 a 20).

## Slajd 22

- HLAVNÍ PŘÍČINY
- Po každé další pozvánce přijde méně žen
- Po první pozvánce přijde do roka polovina žen, po osmé nebo další jen 5 %. Ženám, které vypadly z rytmu, chodí pozvánka pozdě.
- *Graf: Účast do 12 měsíců podle pořadí pozvánky (%), pozvánky 2024* (kategorie: 1., 2., 3., 4., 5., 6., 7., 8. a další)
  - Účast do 12 měsíců (%): 52.7, 32.1, 24.4, 18.4, 14.8, 12.9, 9.9, 5.3
- 46 %
- žen, které v roce 2024 nepřišly, dostalo už osmou nebo další pozvánku
- 41 % vs. 25 %
- návrat vypadlých žen při pozvánce 25–36, resp. 49–60 měsíců po poslední mamografii
- 95 %
- vypadlých žen dnes dostane pozvánku až 3–5 let po poslední mamografii
- Zdroj: data VZP pro Rakathon 2026, pozvánky 2020–2024; naše analýza

> Poznámky: 45 s. Účast podle pořadí pozvánky je popis, ne příčina: opakovaně zvané ženy jsou ty, které nechodí. Pro VZP z toho plyne, že další stejný dopis přináší málo. Návrat vypadlých je pozorovací srovnání, ověří ho experiment s dřívější pozvánkou.

## Slajd 23

- SKUPINY KLIENTEK
- Většinu žen, které nepřišly, lze oslovit jinak než dopisem
- Segmenty stojí jen na polích v poskytnutých datech, a jsou vzájemně výlučné. Účast se mezi nimi liší víc než dvacetinásobně.

| Segment | Ženy 2024 | Účast do 12m od pozvání | Nepřišlo | Kanál |
|---|---|---|---|---|
| A nedávno vyšetřená | 7 600 | 2 % | 7 418 | nezvat, ověřit výkony před odesláním |
| B první pozvánka | 37 460 | 55 % | 16 820 | dopis s pevným termínem, SMS |
| C vypadlá z rytmu | 28 577 | 33 % | 19 111 | dřívější připomínka s termínem |
| D bez screeningu, chodí ke gynekologovi | 51 047 | 21 % | 40 573 | gynekolog |
| E bez screeningu, jiná prevence | 89 351 | 8 % | 82 559 | praktik, zubař, jiný screening |
| F jen léčebná péče | 28 368 | 5 % | 26 977 | ošetřující lékaři |
| G mimo péči | 14 063 | 2 % | 13 743 | nejdřív ověřit kontakt |
| Celkem | 256 466 | 19 % | 207 201 |  |

- 59 %
- žen, které nepřišly, patří do segmentů D a E: chodí ke gynekologovi nebo na jinou prevenci
- AUC 0,80
- samotné segmenty seřadí ženy skoro stejně dobře jako celý model
- Zdroj: data VZP pro Rakathon 2026, pozvánky 2024; naše analýza

> Poznámky: 60 s. Segmenty jsou stabilní pět let a shlukování je potvrzuje. Jemnější verze s 11 segmenty dělí D a E podle počtu pozvánek (config/segments_vzp_v2.yaml). Překryv: ženy 65+ v okrese bez mamocentra mají nižší šanci přijít (OR ≈ 0,83).

## Slajd 24

- NÁVRHY
- Šest skupin opatření a podklady, ze kterých vycházejí
- U každé skupiny uvádíme, co navrhujeme a co ji podporuje v datech VZP, v literatuře a v rozhovorech s experty. Úplné citace jsou v příloze.

| Opatření | Data VZP | Literatura | Rozhovor s expertem |
|---|---|---|---|
| Chytřejší zvaní nezvat nedávno vyšetřené, dřívější připomínka vypadlým, SMS, nový dopis | 7 600 dopisů ročně jde ženám těsně po screeningu; 95 % vypadlých dostane pozvánku až po 3–5 letech; po 8. a další pozvánce přijde 5 % | poštovní připomínka +2,7 p. b. (Allgood a kol., 2016); SMS 59 → 64 % (Kerrison a kol., 2015); připomínka dlouhodobým neúčastnicím +6,4 p. b. (Ferrari a kol., 2026) | dopisy často končí v koši (I. Duškov, VZP), jeden stojí 40Kč |
| Snadné objednání pevný termín místo otevřené pozvánky, víkendové a večerní termíny | segmenty B a C: 66 tis. zvaných žen ročně, z nich 36 tis. nepřišlo | pevný termín 49 → 68 % (Li a kol., 2026); druhý pevný termín 12 → 22 % (Allgood a kol., 2017); víkendy využívají hlavně mladší ženy (Rossi a kol., 2024) | víkendové termíny pro komunitu charedi v Izraeli (L. Hamplová); prevence v lednu, mamograf až v červnu (P. Adámková, Hlas Onko) |
| Lékař jako kanál seznamy žen bez mamografie, srovnání lékařů, upozornění v EZ kartě, bonus | gynekologická prevence zvyšuje šanci přijít 1,4–1,6×, prevence u praktika ne (1,0×); gynekolog za mamografii pacientek nedostává nic (metodika VZP 2026) | audit a zpětná vazba lékařům jsou účinné (Brouwers a kol., 2011); připomínky lékařům zlepšují dodržování doporučení (Ricci-Cabello a kol., 2023); dopis s podpisem praktika +5,8 p. b. (Hewitson a kol., 2011) | upozornění v informačním systému lékaře; férové srovnání lékařů s ostatními (P. Hroboň) |
| Úpravy aplikace Moje VZP: připomínka, objednání | kanály ani používání aplikace data VZP neobsahují | push notifikaci prokliklo 4,1 % žen (Lee a kol., 2026) | – |
| Dostupnost v regionech doprava a pojízdný mamograf pro 65+ v okresech bez centra | okres bez centra snižuje šanci přijít od 50 let (0,82–0,91×, nejvíc v 65–69), ve 45–49 ne; pro přesné cílení potřebujeme okres bydliště a data obcí | nejistá doprava snižuje šanci na mamografii (OR 0,59; Pohl a kol., 2025); pojízdný mamograf v primární péči (Ziegler a kol., 2026) | program v Chorvatsku, kterým se lze inspirovat |
| Plošné nástroje kampaň, finanční pobídka; zatím neřešit | plošná pobídka 500 Kč vychází na ≈ 30 500 Kč za mamografii navíc (při +1 p. b.), cílená na F a G na ≈ 2 500 Kč | masová média bez průkazného účinku (Community Guide); malé finanční pobídky bez průkazného účinku (Merrick a kol., 2015) | – |

- Zdroj: data VZP pro Rakathon 2026; PAPERS.md; zápis rozhovorů (docs/CALL_STRATEGIE_261010.md); docs/PREZENTACE.md

## Slajd 25

- NÁVRHY
- Šest skupin opatření podle náročnosti a dopadu
- Začínáme chytřejším zvaním: je levné, VZP ho zvládne sama a uspořené dopisy financují dražší kanály.
- Levné a účinné
- Účinné, náročné
- Doplňky a testy
- Zatím neřešit
- Dopad na účast →
- Náročnost: IT, partneři, úhrady, cena →
- Chytřejší zvaní / načasování, SMS, lepší dopis
- Snadné objednání / pevný termín, víkendy
- Úpravy aplikace / Moje VZP: připomínka, objednání
- Lékař jako kanál / gynekolog, praktik, upozornění
- Dostupnost v regionech / doprava, pojízdný mamograf
- Plošné nástroje / kampaň, finanční pobídka
- Postup zavedení
- Hned: chytřejší zvaní (klíč rozesílky, SMS, nový dopis) / Pilot: snadné objednání a lékař jako kanál s partnerskými centry a praxemi / Lokálně: dostupnost jen tam, kde je problém (65+ v okresech bez centra) / Ne: plošná kampaň a pobídka mají v literatuře minimální účinek
- Zdroj: náš úsudek z dat VZP a literatury (docs/interventions.md)

> Poznámky: 45 s. Poloha je kvalitativní. Dopad = mamografie navíc mezi zvanými ženami (rozpětí z literatury × velikost segmentů 2024): snadné objednání ≈ 6,5–12,5 tis. ročně, lékař jako kanál ≈ 3–8 tis., chytřejší zvaní jednotky tisíc, dostupnost stovky, plošné nástroje 0–2,5 tis. Úpravy aplikace: odhad zatím nemáme, umístění v matici je rozhodnutí týmu. Odhady se nesčítají.

## Slajd 26

- CÍLENÁ PODPORA
- Hlavní opatření pro zvolené segmenty
- Vybíráme segmenty B–E: dohromady 81 % pozvánek a 77 % žen, které nepřišly. U každého existuje dosažitelný kanál a opatření s doloženým účinkem.

| Segment | Hlavní opatření | Skupina opatření | Účinek (p. b.) |
|---|---|---|---|
| B první pozvánka | pevný termín už v první pozvánce, SMS připomínka | Snadné objednání | +10 až +19 |
| C vypadlá z rytmu | připomínka s termínem ve 25.–36. měsíci místo po 3–5 letech | Chytřejší zvaní | +2 až +6 |
| D gynekolog | seznam žen bez mamografie pro gynekologa, objednání v ordinaci, bonus | Lékař jako kanál | +2 až +6 |
| E jiná prevence | praktik jako nový kanál: seznam žen, upozornění při preventivní prohlídce | Lékař jako kanál | +2 až +6 |
| A nedávno vyšetřená | nezvat, ověřit výkony těsně před odesláním (≈ 7 600 dopisů ročně) | Chytřejší zvaní | úspora |
| 65+ v okrese bez centra | doprava, pojízdný mamograf, termín v sousedním okrese | Dostupnost v regionech | lokálně +5 až +15 |

- F a G zatím nevybíráme: nízká účast i nejistý účinek. Rozpětí účinku pochází z literatury a udává přírůstek oproti dnešnímu dopisu; skutečný účinek ověří experiment.

> Poznámky: 60 s. Rozpětí: docs/interventions.md (pevný termín #1, telefon #7, seznamy a zpětná vazba lékařům #6, strukturální bariéry #4). U C stojí návrh i na naší analýze: návrat 41 % po 25–36 měsících vs. 25 % po 49–60 měsících.

## Slajd 27

- UKÁZKA
- Ukázka dopisů pro tři segmenty
- B první pozvánka: co mě čeká
- D, E bez screeningu: vyvrácení mýtů
- C vypadlá z rytmu: pomoc s překážkami
- Návrhy dopisů k revizi; fakta v dopisech ověříme se zdravotním garantem VZP

> Poznámky: 30 s. Před finální verzí: krok 1 „zajděte za gynekologem“ nahradit „žádanku vystaví praktik, gynekolog, nebo přímo centrum“; přidat variantu s pevným termínem; sjednotit „jen pár minut“ a „asi čtvrt hodiny“; doplnit zdroje k „1 z 10 žen“ a „99 % přežití“; podpis ředitele bez jména, pokud nemáme souhlas.

## Slajd 28

- EXPERIMENT
- Experiment ověří účinek proti dnešnímu dopisu
- Ženy v segmentech B–E náhodně rozdělíme do ramen. Kontrolní skupina dostane dnešní dopis, takže měříme přínos oproti současné praxi.
- Segmenty B–E / ženy, které VZP zve
- Náhodné rozdělení / ženy; u lékařů po praxích
- Kontrola / dnešní dopis
- Rameno 1 / nový dopis podle segmentu
- Rameno 2 / pevný termín + SMS
- Rameno 3 / lékař jako kanál
- Výsledek / vykázaná mamografie do 6 měsíců, data VZP
- 3–9 tis. žen
- na rameno odhalí rozdíl +2 až +3 p. b.
- Předregistrace
- hypotézy, sledovaný ukazatel a analýza stanovené předem
- Podle přidělení
- vyhodnocení všech žen v rameni (ITT)
- Pilot s VZP
- v rámci řízeného vstupu inovací

> Poznámky: 60 s. Podskupiny dané předem: věk × vzdálenost k centru. Pravidlo zastavení: objednací lhůta v partnerských centrech nad dohodnutou mez. Doplňkově přirozené experimenty: varianty dopisů 3/4/7/8, klíč rozesílky, reforma 7/2026.

## Slajd 29

- DOPAD
- Co může přinést plošné nasazení: odhad finančního modelu
- První tři čísla jsou změřená na ženách, které VZP pozvala v roce 2024. Další tři jsou odhad finančního modelu pro 1,5 mil. klientek VZP 45+ za roky 2027–2031; obě populace zatím nepropojujeme.
- 256 466
- žen pozvala VZP v roce 2024
- →
- 207 201
- z nich nepřišlo do 12 měsíců
- →
- 159 063
- z nich v segmentech B–E
- ≈ 291 tis.
- vyšetření navíc za 2027–2031
- →
- ≈ 1 600
- dříve zachycených nádorů, ≈ 190 odvrácených úmrtí
- →
- ≈ 156 mil. Kč
- čistý přínos za 5 let, z toho 34 mil. Kč za dopisy
- Rozhodující nejistota
- Výsledek stojí na ceně léčby stadia IV, v modelu 3 mil. Kč na pacientku (odhad týmu). Pod ≈ 1,9 mil. Kč vychází první vyšetření navíc finančně zhruba na nulu a přínosem zůstávají zachráněné životy.
- Na čem výpočet stojí
- Digitální kaskáda (push, e-mail, SMS, RCS) přivede ročně o 6 p. b. víc z ≈ 614 tis. žen bez prevence (konzervativně 3, optimisticky 10). Model počítá s návratem 80 %, data VZP dávají u žen dříve bez screeningu 60–70 %.
- Zdroj: data VZP pro Rakathon 2026; finanční model (docs/Financial_model, 16. 10. 2026); audit čísel (docs/AUDIT_CISEL.md)

> Poznámky: 45 s. Čísla 4–6 jsou ze základního scénáře finančního modelu (docs/Financial_model, 16. 10. 2026): kaskáda bez PPC 291 346 vyšetření za 2027–2031, 1 605 dříve zachycených nádorů, ≈ 190 odvrácených úmrtí do 5 let, čistý přínos 156 mil. Kč včetně 34 mil. Kč úspory za dopisy (bez ní ≈ 122 mil. Kč). Rozpětí konzervativní–optimistický: 154–462 tis. vyšetření včetně PPC, 86–237 mil. Kč. Model nestojí na kohortě zvaných žen 2024 a nepoužívá účinky z dolní meze literatury; most mezi oběma populacemi chybí (AUDIT_CISEL.md, kap. 4). Předpoklady 1,5 mil. klientek a 614 tis. žen bez prevence jsou odhady.

## Slajd 30

- Nabízíme VZP pilot
- Pilot segmentů B–E s randomizací v rámci řízeného vstupu inovací VZP / Model, segmenty a návrh experimentu předáme včetně kódu a dokumentace / Zkušenosti ze zdravotnictví, z data science i z byznysu
- Jakub Weiner / jakub@weiner.cz · +420 602 307 893 · www.weinerpartners.cz

> Poznámky: 20 s. Poděkování mentorům jen se souhlasem; jména doplnit sem, pokud ho dostaneme.

## Slajd 31

- PŘÍLOHA
- Přehled zvažovaných intervencí a jejich očekávaného účinku
- Účinek je přírůstek oproti dnešnímu dopisu podle literatury; přenos do ČR je náš úsudek a skutečný účinek ověří experiment.

| Skupina opatření | Intervence | Pro koho | Účinek (p. b.) |
|---|---|---|---|
| Chytřejší zvaní | nezvat nedávno vyšetřené, ověřit výkony před odesláním | A | úspora 7 600 dopisů |
|   | dřívější připomínka s termínem ve 25.–36. měsíci | C | +2 až +6 |
|   | nový dopis: vyvrácení mýtů, přerušení zvyku, „bez žádanky“, podpis lékaře | všechny zvané | +1 až +4 |
|   | SMS připomínka s odkazem na objednání | ženy s mobilním číslem | +2 až +5 |
|   | zprávy upravené AI pro minisegmenty | varianty dopisu a SMS | 0 až +2 |
| Snadné objednání | pevný termín místo otevřené pozvánky | B, C | +10 až +19 |
|   | víkendové a večerní termíny | pracující ženy (B, C) | neměřeno |
|   | elektronická žádanka | všechny zvané | bez odhadu |
| Lékař jako kanál | seznamy žen bez mamografie a zpětná vazba lékařům | D, E | +2 až +6 |
|   | upozornění pro lékaře v EZ kartě | E, F | +1 až +5 |
|   | bonus lékařům za mamografický screening | gynekologové, praktici | 0 až +2 |
| Úpravy aplikace | push v Moje VZP a úpravy aplikace | uživatelky aplikace | push 0 až +1 |
| Dostupnost v regionech | doprava a pojízdný mamograf | 65+ v okresech bez centra | lokálně +5 až +15 |
| Plošné nástroje | mediální kampaň, influenceři, pacientské organizace | všechny ženy | ≈ 0 |
|   | finanční pobídka ženám | všechny ženy, případně F, G | 0 až +1 |
| Zatím nezařazeno | telefonická navigace: objednat a vyřešit překážku | F, G | +5 až +12 |
|   | balíček prevence (více screeningů najednou) | E | −2 až +3 |
|   | ověření pobytu v ČR, komunitní práce | G | bez odhadu |

- Zdroj: docs/PREZENTACE.md, kap. 7–11; docs/interventions.md; naše analýza
- Potřebujeme lepší popis jednotlivých intervencí i s odkazy na literaturu (příklady z cizích zemí: například Chorvatsko a transport)

## Slajd 32

- PŘÍLOHA
- Data VZP a jejich omezení
- Co data jsou
- 1 344 556 adresných pozvánek VZP (dopisy 3, 4, 7 a 8) z let 2020–2024 pro 508 527 žen nepřetržitě pojištěných 2015–2025.
- Koho obsahují
- jen ženy, které VZP zvala, tedy ženy mimo doporučený interval; ženy 40–74 let, bez 75+ a bez nově pojištěných.
- Co měříme
- účast do 3, 6 a 12 měsíců od pozvánky; výkony zahrnují i doplňující snímky a ultrazvuk.
- Region
- územní pracoviště VZP, ne okres; okresní ukazatele lze napojit jen přibližně.
- Co chybí
- kategorie plátce, okres bydliště, registrující lékař, typ a znění dopisu, kanály, pozvánky po 7/2026.
- Zdroj: data VZP pro Rakathon 2026 a rozhraní dat; docs/RAKATHON_MODEL.md

## Slajd 33

- PŘÍLOHA
- Návrat po mamografii podle segmentu
- Sledujeme ženy, které přišly po pozvánce z 1. pololetí 2020, do konce roku 2024. Návrat znamená spíše „do zhruba 3 let“, protože VZP znovu zve až po 36 a více měsících.

| Skupina (segment pozvánky, po které přišla) | Žen | Návrat: dolní – horní mez |
|---|---|---|
| všechny, které přišly | 24 267 | 73–80 % |
| B první pozvánka | 12 066 | 86–89 % |
| C vypadlá z rytmu | 3 968 | 64–74 % |
| D–G dříve bez screeningu | 8 175 | 60–70 % |
| z toho D gynekolog | 4 717 | 67–75 % |
| z toho E jiná prevence | 2 819 | 51–64 % |
| z toho F, G | 639 | 46–61 % |

- 60–70 %
- návrat u žen dříve bez screeningu (D–G); u žen po první pozvánce 86–89 %
- Zdroj: data VZP pro Rakathon 2026; docs/AUDIT_CISEL.md, kap. 5.3

## Slajd 34

- PŘÍLOHA
- Otázky pro VZP a data, která by pilot potřeboval
- Data
- typ a znění dopisu (přirozený experiment) / kategorie plátce jako zástupný ukazatel socioekonomické situace / okres bydliště místo územního pracoviště / pseudonym registrujícího praktika a gynekologa / dostupné kanály: Moje VZP, telefon / pozvánky po 7/2026 (reforma bez žádanky)
- Ekonomika
- náklady léčby karcinomu prsu podle stadia / úhrada výkonu 89223 a doplňujících vyšetření / náklady kanálů a rozpočet na kampaň / kapacita a objednací lhůty mamocenter
- Systém
- úhradový mechanismus praktiků a možnost bonusu za mamografický screening / jak VZP zve dnes: otevřená pozvánka, kanály, frekvence / počet aktivních uživatelů aplikace Moje VZP

## Slajd 35

- SKUPINY KLIENTEK
- Většinu žen, které nepřišly, lze oslovit jinak než dopisem
- Segmenty stojí jen na polích v poskytnutých datech, a jsou vzájemně výlučné. Účast se mezi nimi liší víc než dvacetinásobně.

| Segment | Ženy 2024 | Účast do 12m od pozvání | Nepřišlo | Kanál |
|---|---|---|---|---|
| A nedávno vyšetřená | 7 600 | 2 % | 7 418 | nezvat, ověřit výkony před odesláním |
| B první pozvánka | 37 460 | 55 % | 16 820 | dopis s pevným termínem, SMS |
| C vypadlá z rytmu | 28 577 | 33 % | 19 111 | dřívější připomínka s termínem |
| D bez screeningu, chodí ke gynekologovi | 51 047 | 21 % | 40 573 | gynekolog |
| E bez screeningu, jiná prevence | 89 351 | 8 % | 82 559 | praktik, zubař, jiný screening |
| F jen léčebná péče | 28 368 | 5 % | 26 977 | ošetřující lékaři |
| G mimo péči | 14 063 | 2 % | 13 743 | nejdřív ověřit kontakt |
| Celkem | 256 466 | 19 % | 207 201 |  |

- 59 %
- žen, které nepřišly, patří do segmentů D a E: chodí ke gynekologovi nebo na jinou prevenci
- AUC 0,80
- samotné segmenty seřadí ženy skoro stejně dobře jako celý model
- Zdroj: data VZP pro Rakathon 2026, pozvánky 2024; naše analýza

> Poznámky: 60 s. Segmenty jsou stabilní pět let a shlukování je potvrzuje. Jemnější verze s 11 segmenty dělí D a E podle počtu pozvánek (config/segments_vzp_v2.yaml). Překryv: ženy 65+ v okrese bez mamocentra mají nižší šanci přijít (OR ≈ 0,83).

## Slajd 36

- NÁVRHY
- Šest skupin opatření podle náročnosti a dopadu
- Začínáme chytřejším zvaním: je levné, VZP ho zvládne sama a uspořené dopisy financují dražší kanály.
- Levné a účinné
- Účinné, náročné
- Doplňky a testy
- Zatím neřešit
- Dopad na účast →
- Náročnost: IT, partneři, úhrady, cena →
- Chytřejší zvaní / načasování, SMS, lepší dopis
- Snadné objednání / pevný termín, víkendy
- Úpravy aplikace / Moje VZP: připomínka, objednání
- Lékař jako kanál / gynekolog, praktik, upozornění
- Dostupnost v regionech / doprava, pojízdný mamograf
- Plošné nástroje / kampaň, finanční pobídka
- Postup zavedení
- Hned: chytřejší zvaní (klíč rozesílky, SMS, nový dopis) / Pilot: snadné objednání a lékař jako kanál s partnerskými centry a praxemi / Lokálně: dostupnost jen tam, kde je problém (65+ v okresech bez centra) / Ne: plošná kampaň a pobídka mají v literatuře minimální účinek
- Zdroj: náš úsudek z dat VZP a literatury (docs/interventions.md)

> Poznámky: 45 s. Poloha je kvalitativní. Dopad = mamografie navíc mezi zvanými ženami (rozpětí z literatury × velikost segmentů 2024): snadné objednání ≈ 6,5–12,5 tis. ročně, lékař jako kanál ≈ 3–8 tis., chytřejší zvaní jednotky tisíc, dostupnost stovky, plošné nástroje 0–2,5 tis. Úpravy aplikace: odhad zatím nemáme, umístění v matici je rozhodnutí týmu. Odhady se nesčítají.

## Slajd 37

- CÍLENÁ PODPORA
- Hlavní opatření pro zvolené segmenty
- Vybíráme segmenty B–E: dohromady 81 % pozvánek a 77 % žen, které nepřišly. U každého existuje dosažitelný kanál a opatření s doloženým účinkem.

| Segment | Hlavní opatření | Skupina opatření | Účinek (p. b.) |
|---|---|---|---|
| B první pozvánka | pevný termín už v první pozvánce, SMS připomínka | Snadné objednání | +10 až +19 |
| C vypadlá z rytmu | připomínka s termínem ve 25.–36. měsíci místo po 3–5 letech | Chytřejší zvaní | +2 až +6 |
| D gynekolog | seznam žen bez mamografie pro gynekologa, objednání v ordinaci, bonus | Lékař jako kanál | +2 až +6 |
| E jiná prevence | praktik jako nový kanál: seznam žen, upozornění při preventivní prohlídce | Lékař jako kanál | +2 až +6 |
| A nedávno vyšetřená | nezvat, ověřit výkony těsně před odesláním (≈ 7 600 dopisů ročně) | Chytřejší zvaní | úspora |
| 65+ v okrese bez centra | doprava, pojízdný mamograf, termín v sousedním okrese | Dostupnost v regionech | lokálně +5 až +15 |

- F a G zatím nevybíráme: nízká účast i nejistý účinek. Rozpětí účinku pochází z literatury a udává přírůstek oproti dnešnímu dopisu; skutečný účinek ověří experiment.

> Poznámky: 60 s. Rozpětí: docs/interventions.md (pevný termín #1, telefon #7, seznamy a zpětná vazba lékařům #6, strukturální bariéry #4). U C stojí návrh i na naší analýze: návrat 41 % po 25–36 měsících vs. 25 % po 49–60 měsících.

## Slajd 38

- UKÁZKA
- Ukázka dopisů pro tři segmenty
- B první pozvánka: co mě čeká
- D, E bez screeningu: vyvrácení mýtů
- C vypadlá z rytmu: pomoc s překážkami
- Návrhy dopisů k revizi; fakta v dopisech ověříme se zdravotním garantem VZP

> Poznámky: 30 s. Před finální verzí: krok 1 „zajděte za gynekologem“ nahradit „žádanku vystaví praktik, gynekolog, nebo přímo centrum“; přidat variantu s pevným termínem; sjednotit „jen pár minut“ a „asi čtvrt hodiny“; doplnit zdroje k „1 z 10 žen“ a „99 % přežití“; podpis ředitele bez jména, pokud nemáme souhlas.

## Slajd 39

- UKÁZKA
- Ukázka navrhovaných úprav aplikace Moje VZP
- [snímek obrazovky]
- [popis úpravy]
- [snímek obrazovky]
- [popis úpravy]
- [snímek obrazovky]
- [popis úpravy]
- Návrhy úprav k revizi

## Slajd 40

- EXPERIMENT
- Experiment ověří účinek proti dnešnímu dopisu
- Ženy v segmentech B–E náhodně rozdělíme do ramen. Kontrolní skupina dostane dnešní dopis, takže měříme přínos oproti současné praxi.
- Segmenty B–E / ženy, které VZP zve
- Náhodné rozdělení / ženy; u lékařů po praxích
- Kontrola / dnešní dopis
- Rameno 1 / nový dopis podle segmentu
- Rameno 2 / pevný termín + SMS
- Rameno 3 / lékař jako kanál
- Výsledek / vykázaná mamografie do 6 měsíců, data VZP
- 3–9 tis. žen
- na rameno odhalí rozdíl +2 až +3 p. b.
- Předregistrace
- hypotézy, sledovaný ukazatel a analýza stanovené předem
- Podle přidělení
- vyhodnocení všech žen v rameni (ITT)
- Pilot s VZP
- v rámci řízeného vstupu inovací

> Poznámky: 60 s. Podskupiny dané předem: věk × vzdálenost k centru. Pravidlo zastavení: objednací lhůta v partnerských centrech nad dohodnutou mez. Doplňkově přirozené experimenty: varianty dopisů 3/4/7/8, klíč rozesílky, reforma 7/2026.

## Slajd 41

- DOPAD
- Co může přinést plošné nasazení: odhad finančního modelu
- První tři čísla jsou změřená na ženách, které VZP pozvala v roce 2024. Další tři jsou odhad finančního modelu pro 1,5 mil. klientek VZP 45+ za roky 2027–2031; obě populace zatím nepropojujeme.
- 256 466
- žen pozvala VZP v roce 2024
- →
- 207 201
- z nich nepřišlo do 12 měsíců
- →
- 159 063
- z nich v segmentech B–E
- ≈ 291 tis.
- vyšetření navíc za 2027–2031
- →
- ≈ 1 600
- dříve zachycených nádorů, ≈ 190 odvrácených úmrtí
- →
- ≈ 156 mil. Kč
- čistý přínos za 5 let, z toho 34 mil. Kč za dopisy
- Rozhodující nejistota
- Výsledek stojí na ceně léčby stadia IV, v modelu 3 mil. Kč na pacientku (odhad týmu). Pod ≈ 1,9 mil. Kč vychází první vyšetření navíc finančně zhruba na nulu a přínosem zůstávají zachráněné životy.
- Na čem výpočet stojí
- Digitální kaskáda (push, e-mail, SMS, RCS) přivede ročně o 6 p. b. víc z ≈ 614 tis. žen bez prevence (konzervativně 3, optimisticky 10). Model počítá s návratem 80 %, data VZP dávají u žen dříve bez screeningu 60–70 %.
- Zdroj: data VZP pro Rakathon 2026; finanční model (docs/Financial_model, 16. 10. 2026); audit čísel (docs/AUDIT_CISEL.md)

> Poznámky: 45 s. Čísla 4–6 jsou ze základního scénáře finančního modelu (docs/Financial_model, 16. 10. 2026): kaskáda bez PPC 291 346 vyšetření za 2027–2031, 1 605 dříve zachycených nádorů, ≈ 190 odvrácených úmrtí do 5 let, čistý přínos 156 mil. Kč včetně 34 mil. Kč úspory za dopisy (bez ní ≈ 122 mil. Kč). Rozpětí konzervativní–optimistický: 154–462 tis. vyšetření včetně PPC, 86–237 mil. Kč. Model nestojí na kohortě zvaných žen 2024 a nepoužívá účinky z dolní meze literatury; most mezi oběma populacemi chybí (AUDIT_CISEL.md, kap. 4). Předpoklady 1,5 mil. klientek a 614 tis. žen bez prevence jsou odhady.

## Slajd 42

- Nabízíme VZP pilot
- Pilot segmentů B–E s randomizací v rámci řízeného vstupu inovací VZP / Model, segmenty a návrh experimentu předáme včetně kódu a dokumentace / Zkušenosti ze zdravotnictví, z data science i z byznysu; téma nás zajímá
- Jakub Weiner / jakub@weiner.cz · +420 602 307 893 · www.weinerpartners.cz

> Poznámky: 20 s. Poděkování mentorům jen se souhlasem; jména doplnit sem, pokud ho dostaneme.

## Slajd 43

- PŘÍLOHA
- Přehled zvažovaných intervencí a jejich očekávaného účinku
- Účinek je přírůstek oproti dnešnímu dopisu podle literatury; přenos do ČR je náš úsudek a skutečný účinek ověří experiment.

| Skupina opatření | Intervence | Pro koho | Účinek (p. b.) |
|---|---|---|---|
| Chytřejší zvaní | nezvat nedávno vyšetřené, ověřit výkony před odesláním | A | úspora 7 600 dopisů |
|   | dřívější připomínka s termínem ve 25.–36. měsíci | C | +2 až +6 |
|   | nový dopis: vyvrácení mýtů, přerušení zvyku, „bez žádanky“, podpis lékaře | všechny zvané | +1 až +4 |
|   | SMS připomínka s odkazem na objednání | ženy s mobilním číslem | +2 až +5 |
|   | zprávy upravené AI pro minisegmenty | varianty dopisu a SMS | 0 až +2 |
| Snadné objednání | pevný termín místo otevřené pozvánky | B, C | +10 až +19 |
|   | víkendové a večerní termíny | pracující ženy (B, C) | neměřeno |
|   | elektronická žádanka | všechny zvané | bez odhadu |
| Lékař jako kanál | seznamy žen bez mamografie a zpětná vazba lékařům | D, E | +2 až +6 |
|   | upozornění pro lékaře v EZ kartě | E, F | +1 až +5 |
|   | bonus lékařům za mamografický screening | gynekologové, praktici | 0 až +2 |
| Úpravy aplikace | push v Moje VZP a úpravy aplikace | uživatelky aplikace | push 0 až +1 |
| Dostupnost v regionech | doprava a pojízdný mamograf | 65+ v okresech bez centra | lokálně +5 až +15 |
| Plošné nástroje | mediální kampaň, influenceři, pacientské organizace | všechny ženy | ≈ 0 |
|   | finanční pobídka ženám | všechny ženy, případně F, G | 0 až +1 |
| Zatím nezařazeno | telefonická navigace: objednat a vyřešit překážku | F, G | +5 až +12 |
|   | balíček prevence (více screeningů najednou) | E | −2 až +3 |
|   | ověření pobytu v ČR, komunitní práce | G | bez odhadu |

- Zdroj: docs/PREZENTACE.md, kap. 7–11; docs/interventions.md; naše analýza

## Slajd 44

- Praktik vs. gynekolog
- Účast do 12 měsíců po pozvánce, %
- *Graf: Graf účasti* (kategorie: 45–49, 50–54, 55–59, 60–64, 65–69, 70–74)
  - Ženy jen u praktika: 15.1, 10.8, 10.2, 10.2, 9.9, 9.2
  - Ženy po gynekologické prevenci: 42.7, 22.6, 23.2, 24.3, 24.8, 22.9
- Kdyby praktik doporučoval jako gynekolog
- Ženy jen u praktika: 10,6 % → 25,7 %
- 61,2 %  →  64,3 %
- celková docházka žen 45–74 let (+3,1 p. b.)
- +33 776
- žen navíc na mamografu ročně
- Zdroj: zvané klientky VZP 2020–2024 (Rakathon 2026), ČSÚ a ÚZIS 2024 · horní odhad

> Poznámky: Ženy, které chodí na prevenci jen k praktikovi, přicházejí na mamograf po pozvánce v 9,2–15,1 % případů, ženy po gynekologické prevenci v 22,6–42,7 %. Kdyby praktici doporučovali mamograf stejně aktivně, účast žen jen u praktika by vzrostla z 10,6 % na 25,7 % a celková dvouletá docházka žen 45–74 let z 61,2 % na 64,3 %, tedy asi 33 776 žen navíc ročně v celé ČR. Všechny věkové skupiny vycházejí ze stejných let (pozvánky 2020–2024), počty žen a pokrytí z ČSÚ a ÚZIS 2024. Jde o horní mez: předpokládá, že praktik plně nahradí gynekologa, a část rozdílu tvoří to, že ke gynekologovi chodí ženy, které o zdraví víc dbají. Konzervativní odhad (upravené poměry šancí z logistické regrese na pozvánkách 2020–2022) dává asi 10 660 žen navíc ročně a docházku 62,2 %.

## Slajd 45

- Kolik karcinomů odhalíme včas navíc
- Podíl nových případů karcinomu prsu podle věku, %
- screening 45–74: 66,8 % případů
- *Graf: Graf incidence* (kategorie: 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85+)
  - Podíl případů: 0, 0.3, 1.3, 2.9, 5.7, 10.7, 8.8, 8.9, 9.8, 13.3, 15.3, 12.4, 6.3, 4.2
- ZA ROK NAVÍC
- +33 776
- vyšetření / na mamografu
- 192
- karcinomů / odhalených včas

| Věk | Vyšetření | Karcinomy |
|---|---|---|
| 45–49 | 6 815 | 22 |
| 50–54 | 4 202 | 14 |
| 55–59 | 4 961 | 22 |
| 60–64 | 5 119 | 29 |
| 65–69 | 6 161 | 45 |
| 70–74 | 6 519 | 60 |
| Celkem | 33 776 | 192 |

- Konzervativně: 10 660 vyšetření, 60 karcinomů
- Zdroj: SVOD 2020–2024 (C50), ÚZIS – Evaluační zpráva 2022, výpočet z dat VZP

> Poznámky: Dvě třetiny všech nových karcinomů prsu (66,8 %) vznikají ve věku 45–74 let. Aktivní doporučení praktika by přivedlo zhruba 33 776 vyšetření navíc ročně. Každé násobíme mírou záchytu ze všech screeningových vyšetření v daném věku (ÚZIS, Evaluační zpráva 2022, rok 2021: 3,3–9,2 na 1 000). Vychází asi 192 karcinomů odhalených navíc ročně, nejvíc ve věku 70–74 (60) a 65–69 (45). Konzervativní scénář, tedy jen efekt doporučení po odečtení toho, že ke gynekologovi chodí ženy dbalejší o zdraví, dává 10 660 vyšetření a 60 karcinomů ročně. Citlivost: s mírou záchytu prvního vyšetření ženy by to bylo 387 karcinomů. Jde o horní mez z pozorovacích dat, ne výsledek pilotu.

## Slajd 46

- Doprava: okresy bez mamografu
- Dvouleté pokrytí mamografem, %; pod věkem rozdíl v p. b. (* statisticky průkazný)
- mimo cílovou skupinu
- *Graf: Graf pokrytí* (kategorie: 45–49
+0,6, 50–54
+0,3, 55–59
+0,9, 60–64
+1,3, 65–69
+2,4*, 70–74
+3,2*, 75–79
+5,3*, 80–84
+6,9*, 85+
+4,0*)
  - Okresy bez mamografického pracoviště: 61.4, 62.1, 60.2, 61.6, 61.8, 57.9, 45.9, 26.3, 7.2
  - Po vyřešení dopravy: 61.9, 62.4, 61.1, 62.9, 64.3, 61.1, 51.1, 33.2, 11.2
- Kdyby doprava nebyla překážkou

|  | Pokrytí ČR | Mamografie |
|---|---|---|
| Ženy 45–74 | 61,2 % → 61,5 % | +3 212 |
| Ženy 75+ | 34,8 % → 35,9 % | +3 498 |
| Celkem 45+ | 55,4 % → 55,8 % | +6 710 |

- +6 710
- mamografií navíc ročně, z toho 3 212 u žen 45–74
- V okresech bez pracoviště (477 743 žen 45–74): 60,9 % → 62,2 %. Efekt průkazný od 65 let.
- Zdroj: ČSÚ a ÚZIS 2024, srovnání s okresy téhož kraje s mamografickým pracovištěm

> Poznámky: Akreditované mamografické pracoviště nemá 24 ze 77 okresů. Ženy v těchto okresech mají nižší dvouleté pokrytí než ženy v okresech téhož kraje s pracovištěm (srovnání uvnitř kraje, vážené počtem žen). Rozdíl roste s věkem: ve věku 45–64 je malý (0,3–1,3 p. b.) a statisticky neprůkazný, od 65 let průkazný (65–69 o 2,4 p. b., 70–74 o 3,2 p. b.) a po 75 letech největší (4–7 p. b.). Kdyby doprava nebyla překážkou, přibylo by ročně 3 212 mamografií u žen 45–74 a 3 498 u žen 75+, celkem 6 710. Na úrovni celé ČR (stejný základ jako u praktika) by se pokrytí žen 45–74 zvýšilo z 61,2 % na 61,5 %, žen 75+ z 34,8 % na 35,9 % a všech žen 45+ z 55,4 % na 55,8 %. Ženám 75+ doprava pomůže nejvíc, jejich výchozí pokrytí je nízké. V samotných okresech bez pracoviště by pokrytí žen 45–74 vzrostlo z 60,9 % na 62,2 %. Jde o horní mez: předpokládá, že doprava odstraní celý rozdíl mezi okresy.

## Slajd 47

- Kolik karcinomů přinese doprava
- Karcinomy odhalené navíc za rok podle věku
- 45–74: 22 karcinomů
- 75+: dalších 43
- *Graf: Graf karcinomů* (kategorie: 45–49, 50–54, 55–59, 60–64, 65–69, 70–74, 75–79, 80–84, 85+)
  - Karcinomy navíc: 1, 0.5, 1.4, 2.4, 6.3, 10.6, 19.7, 15.8, 7.1
- ZA ROK NAVÍC
- Ženy 45–74
- Včetně žen 75+
- +3 212
- +6 710
- mamografií
- 22
- 65
- karcinomů odhalených včas

| Věk | Mamografie | Karcinomy |
|---|---|---|
| 45–64 | 1 196 | 5,3 |
| 65–69 | 865 | 6,3 |
| 70–74 | 1 152 | 10,6 |
| 75+ | 3 498 | 43 |

- Pro srovnání: praktik přinese 192
- Zdroj: ČSÚ a ÚZIS 2024, ÚZIS – Evaluační zpráva 2022, výpočet z dat VZP

> Poznámky: Mamografie navíc z vyřešené dopravy násobíme stejnou mírou záchytu jako u praktiků (všechna screeningová vyšetření, 3,3–9,2 na 1 000, u 75+ 12,2). U žen 45–74 vychází 3 212 mamografií a asi 22 karcinomů ročně, z toho 17 ve věku 65–74. Ženy 75+ přidají 3 498 mamografií a 43 karcinomů, celkem tedy 6 710 mamografií a 65 karcinomů ročně. Ženy 75+ jsou mimo cílovou skupinu screeningu, ale doprava jim pomůže nejvíc. I včetně nich je doprava zhruba třikrát menší páka než doporučení praktikem (192 karcinomů u žen 45–74). Obě opatření se mohou doplňovat: praktik doporučí, doprava umožní dojet.

## Slajd 48

- APLIKACE PRO LÉKAŘE
- Lékař se jen zapojí, oslovení běží jeho jménem automaticky
- Administrace napojená na Moje VZP ve stejném vizuálu. Lékař vidí, koho program oslovil, kdo přišel a kolik mu VZP za zapojení zaplatí.
- Zdroj: návrh administrace pro lékaře (prompt pro vývoj, 16. 10. 2026); čísla v ukázce jsou ilustrační
- 1
- Zapojí se jedním přepínačem
- souhlas se zasíláním zpráv jeho jménem, společný provoz s VZP
- 2
- VZP oslovuje jeho pacientky
- kaskáda push, e-mail a RCS podle dat VZP, bez práce v ordinaci
- 3
- Vidí výsledky a platby
- osloveno, žádanky, vyšetřeno, konverze a příjem od VZP za rok
- Proč to lékaře zajímá: gynekolog dnes za účast pacientek na mamografu nedostává nic (slajd 6), praktik na mamograf neposílá.
- Přehled · MUDr. Jana Ukázková
- Zapojeno od 1. 3. 2027
- Mamograf
- 412
- osloveno
- 128
- vyšetřeno
- 31 %
- konverze
- Co nejdříve
- Příjem od VZP za rok: sazba VZP – doplnit

> Poznámky: Prototyp: Next.js, design tokeny převzaté z veřejné aplikace a webu VZP (font Source Sans, šedé pozadí, bílé karty s barevným pruhem), bez loga. Stavy pacientky: Pozvána, Žádanka vystavena, Využijte žádanku, Vyšetřena, Po termínu, Odhlášena. Příjem lékaře se počítá z vykázaných výkonů VZP; sazbu bonusu za zapojení musí stanovit VZP.

## Slajd 49

- KASKÁDA
- Digitální kaskáda přivede 44–71 tisíc vyšetření navíc ročně
- Odhad pro ≈ 614 tis. klientek VZP 45+ bez splněné prevence a 443 tis. žen, které chodí pravidelně. Od roku 2029 se na druhé kolo vracejí ženy aktivované v roce 2027.
- Zdroj: finanční model (16. 10. 2026); VZP 2025–2026; datový audit mamografického screeningu 2023; naše analýza
- *Graf: Vyšetření navíc podle roku a scénáře* (kategorie: 2027, 2028, 2029, 2030, 2031)
  - Konzervativní: 22850, 22320, 36542, 35602, 34691
  - Základní: 45700, 43534, 70973, 67296, 63843
  - Optimistický: 74690, 68616, 112277, 102459, 93630
- ZA 2027–2031, ZÁKLADNÍ SCÉNÁŘ
- ≈ 291 tis.
- vyšetření navíc (152–452 tis.)
- ≈ 100 Kč
- náklad komunikace na jedno vyšetření navíc
- 3,36 Kč vs. 40 Kč
- jedna vlna kaskády na ženu vs. jeden dopis; kaskáda osloví 3,5× víc žen za 38 % ceny dopisů

> Poznámky: Scénáře: ženy bez prevence přivedeme o 3 / 6 / 10 p. b. ročně, návratnost pravidelných zvýšíme o 1 / 2 / 3 p. b. Základní scénář odpovídá odhadu komise MZ (+5 až 8 p. b.); SMS připomínka v britském screeningu zvýšila účast z 60 na 72 %. Model počítá s návratem 80 % aktivovaných žen; data VZP ze slajdu 34 dávají u žen dříve bez screeningu 60–70 %, takže od roku 2029 je odhad spíše horní.

## Slajd 50

- FINANČNÍ VYJÁDŘENÍ
- Včasné oslovení ušetří na léčbě víc, než stojí screening
- Dříve zachycený nádor ušetří v průměru 407 tis. Kč (léčba 119 tis. místo 526 tis. Kč). Od úspory odečítáme mamograf, doplňující vyšetření, příspěvek 1 000 Kč a overdiagnózu.
- Zdroj: finanční model (16. 10. 2026); datový audit screeningu 2023; náklady léčby podle stadia: odhad týmu
- *Graf: Základní scénář, mil. Kč ročně* (kategorie: 2027, 2028, 2029, 2030, 2031)
  - Ušetřená léčba: 110.7, 105.1, 153.9, 145.7, 138.1
  - Screening, recall, příspěvek, overdiagnóza: 83.3, 79.2, 122.1, 115.7, 109.7
  - Čistý přínos: 27.5, 26, 31.8, 30, 28.4
- 1 605
- nádorů zachycených dříve, ve stadiu 0–I místo II–IV (840–2 485)
- ≈ 189
- odvrácených úmrtí do 5 let od diagnózy (99–292)
- +654 mil. Kč
- ušetřená léčba za 2027–2031, po nákladech na screening čistě +144 mil. Kč
- Rozhodující nejistota: cena léčby IV. stadia. Pod ≈ 1,9 mil. Kč vychází první vyšetření navíc finančně na nulu.

> Poznámky: Náklady léčby: stadium 0–I 5 tis. Kč, II–III 300 tis. Kč, IV 3 mil. Kč (odhad, nahradit daty VZP). Podíl I. stadia 75 % ve screeningu vs. 28,5 % mimo něj (NOR, audit 2023). Záchyt 7/1 000 v prvním kole, 5/1 000 v dalších; recall 15,6 % a 4,9 %; 10 % overdiagnóza. Úspora se počítá v roce záchytu, skutečně nastane o 1–3 roky později. Hranice vyrovnanosti: léčba IV. stadia ≈ 1,9 mil. Kč.

## Slajd 51

- PŘEHLED
- Program ušetří VZP za pět let čistě 86–237 milionů Kč
- Součet všech položek modelu za 2027–2031. Kladná čísla jsou úspora, záporná náklad; PPC počítáme za jeden rok experimentu.
- Zdroj: finanční model (16. 10. 2026); VZP 2025–2026; datový audit mamografického screeningu 2023; naše analýza

| Položka (2027–2031) | Konzervativní | Základní | Optimistický |
|---|---|---|---|
| Ušetřená léčba díky dřívějšímu záchytu | +342 mil. Kč | +654 mil. Kč | +1 012 mil. Kč |
| Screening, recall, příspěvek 1 000 Kč, overdiagnóza | −267 mil. Kč | −510 mil. Kč | −790 mil. Kč |
| Digitální kaskáda (push, e-mail, SMS, RCS) | −22 mil. Kč | −21 mil. Kč | −20 mil. Kč |
| Úspora za dopisy, které kaskáda nahradí | +33 mil. Kč | +34 mil. Kč | +35 mil. Kč |
| Čistý přínos programu | +86 mil. Kč | +156 mil. Kč | +237 mil. Kč |
| PPC experiment (1 rok, 5 mil. Kč) | −3,6 mil. Kč | −1,6 mil. Kč | +1,9 mil. Kč |
| Čistý přínos včetně PPC | +82 mil. Kč | +154 mil. Kč | +239 mil. Kč |
| Vyšetření navíc (kaskáda + PPC) | 154 000 | 296 000 | 462 000 |
| Nádory zachycené dříve | ≈ 853 | ≈ 1 637 | ≈ 2 548 |
| Odvrácená úmrtí do 5 let | ≈ 100 | ≈ 193 | ≈ 299 |


> Poznámky: Čistý přínos programu = ušetřená léčba − náklady screeningu − komunikace + úspora za dopisy. Úspora za dopisy: dnes ≈ 300 800 dopisů ročně × 40 Kč = 12 mil. Kč; při náhradě kaskádou zůstává 10 % dopisů pro ženy bez digitálního kontaktu. Komunikace je spočítaná pro kaskádu se SMS (3 segmenty × 0,70 Kč), po úpravě rozestupů se změní v řádu jednotek mil. Kč. Platby lékařům doplníme po dodání sazby VZP.

## Slajd 52

- AUTOMATIZACE
- Kaskáda oslovení běží sama, zastaví ji žádanka nebo mamograf
- Spouští ji data VZP, zprávy odcházejí jménem registrujícího lékaře. Kanál bez kontaktu se přeskočí.
- Zdroj: návrh automatizace (16. 10. 2026); úhrada screeningu 1× za 2 roky od 45 let (VZP, 24. 6. 2026)
- Spouštěč / žena 45+, 700 dní od posledního mamografu
- Kaskáda A: pozvánka na mamograf
- Den 0 / Push v Moje VZP
- Den 14 / E-mail
- Den 30 / E-mail připomínka
- Den 60 / RCS zpráva
- Lékař vykázal žádanku?
- ano
- ne: za 6 měsíců znovu kaskáda A
- Pauza 6 měsíců / žádanka platí 1 rok
- Mamograf vykázán?
- ne
- Kaskáda B: využijte žádanku / stejné kanály a rozestupy; pak znovu pauza a kontrola
- ano
- Připsat lékaři do statistiky / další spouštěč za 700 dní
- Pravidla: jen Po–Pá 9–18 h mimo svátky · vykázaný mamograf kaskádu kdykoli ukončí · 5 % žen jako kontrolní skupina · nevyužitá žádanka po roce vrací ženu do kaskády A

> Poznámky: Rozestupy kroků: push den 0, e-mail den 14, e-mail den 30, RCS den 60 (úprava týmu 16. 10.). Zda kaskádu doplnit SMS, je otevřené; finanční model zatím počítá s SMS. Spouštěč 700 dní: VZP hradí screening až 730 dní od posledního vyšetření, pozvánka měsíc předem nechá ženu objednat se na termín po vzniku nároku. Odesílání jen Po–Pá 9–18 h, mimo státní svátky. 5 % žen tvoří náhodnou kontrolní skupinu bez kaskády.

## Slajd 53

- PPC EXPERIMENT
- Kampaň s influencery jen jako test, rozpočet se uvolňuje po fázích
- Literatura dává plošným kampaním malý účinek (slajd 9). Proto 5 mil. Kč ročně nasadíme jako geo test na 77 okresech a dál pokračujeme jen při prokázaném dopadu.
- Zdroj: návrh PPC experimentu (16. 10. 2026); ceny tvůrců jsou odhad k ověření nabídkami
- Fáze 0 · měsíc 1–2
- Příprava
- 0,3 mil. Kč
- měření v Moje VZP, rozdělení okresů, výběr 6–8 tvůrců
- Fáze 1 · měsíc 3–5
- Geo test intenzity
- 1,5 mil. Kč
- kontrola / nízká / vysoká intenzita, ženy 45–74
- Fáze 2 · měsíc 6–8
- Počet tvůrců
- 1,2 mil. Kč
- 2 vs. 6 tvůrců, persona „pošli to mámě“
- Fáze 3 · měsíc 9–12
- Škálování
- 2,0 mil. Kč
- celá ČR, 20 % okresů jako kontrola
- Brána před fází 3: jedno vyšetření navíc stojí méně než ≈ 690 Kč, jinak zbytek rozpočtu jde do kaskády

| Scénář | Náklad na vyšetření navíc | Vyšetření navíc | Nádory dříve | Finančně za rok |
|---|---|---|---|---|
| Konzervativní | 2 500 Kč | 2 000 | ≈ 13 | −3,6 mil. Kč |
| Základní | 1 000 Kč | 5 000 | ≈ 32 | −1,6 mil. Kč |
| Optimistický | 500 Kč | 10 000 | ≈ 63 | +1,9 mil. Kč |


> Poznámky: Jednotka testu jsou okresy (77), ne kraje: 14 krajů nedává dost síly. Skupiny: kontrola, nízká intenzita (≈ 1 Kč na ženu 45+ měsíčně), vysoká (≈ 3 Kč). Obsah tvůrců jako partnerské reklamy cílené do testovacích okresů; organické příspěvky hodnotíme časovou řadou. Persony: známé ženy 45+, lékařky a lékaři, ženy po léčbě, tvůrci s mladším publikem s výzvou „pošli to mámě“ (např. profily typu tady_je_stepancio, po ověření statistik publika). Cílení jen věk, pohlaví, lokalita; seznamy klientek VZP do Mety nenahráváme. Hlavní metrika: objednávky přes Moje VZP na 100 tis. žen 45+, potvrzení vykázanými mamografy.

## Slajd 54

- PŘÍLOHA
- Návrat po mamografii podle segmentu
- Sledujeme ženy, které přišly po pozvánce z 1. pololetí 2020, do konce roku 2024. Návrat znamená spíše „do zhruba 3 let“, protože VZP znovu zve až po 36 a více měsících.

| Skupina (segment pozvánky, po které přišla) | Žen | Návrat: dolní – horní mez |
|---|---|---|
| všechny, které přišly | 24 267 | 73–80 % |
| B první pozvánka | 12 066 | 86–89 % |
| C vypadlá z rytmu | 3 968 | 64–74 % |
| D–G dříve bez screeningu | 8 175 | 60–70 % |
| z toho D gynekolog | 4 717 | 67–75 % |
| z toho E jiná prevence | 2 819 | 51–64 % |
| z toho F, G | 639 | 46–61 % |

- 60–70 %
- návrat u žen dříve bez screeningu (D–G); u žen po první pozvánce 86–89 %
- Zdroj: data VZP pro Rakathon 2026; docs/AUDIT_CISEL.md, kap. 5.3

## Slajd 55

- PŘÍLOHA
- Otázky pro VZP a data, která by pilot potřeboval
- Data
- typ a znění dopisu (přirozený experiment) / kategorie plátce jako zástupný ukazatel socioekonomické situace / okres bydliště místo územního pracoviště / pseudonym registrujícího praktika a gynekologa / dostupné kanály: Moje VZP, telefon / pozvánky po 7/2026 (reforma bez žádanky)
- Ekonomika
- náklady léčby karcinomu prsu podle stadia / úhrada výkonu 89223 a doplňujících vyšetření / náklady kanálů a rozpočet na kampaň / kapacita a objednací lhůty mamocenter
- Systém
- úhradový mechanismus praktiků a možnost bonusu za mamografický screening / jak VZP zve dnes: otevřená pozvánka, kanály, frekvence / počet aktivních uživatelů aplikace Moje VZP

## Slajd 56

- PŘÍLOHA
- Citovaná literatura a dokumenty

| Citace na slajdu | Úplná citace |
|---|---|
| Allgood a kol., 2016 | Allgood PC, Maxwell AJ, Hudson S et al. A randomised trial of the effect of postal reminders on attendance for breast screening. British Journal of Cancer, 2016. |
| Allgood a kol., 2017 | Allgood PC, Maroni R, Hudson S et al. Effect of second timed appointments for non-attenders of breast cancer screening in England: a randomised controlled trial. The Lancet Oncology, 2017. |
| Brouwers a kol., 2011 | Brouwers MC, De Vito C, Bahirathan L et al. What implementation interventions increase cancer screening rates? A systematic review. Implementation Science, 2011. |
| Community Guide | Community Preventive Services Task Force. Cancer Screening: Mass Media Targeting Clients – Breast Cancer. The Community Guide (thecommunityguide.org). |
| Ferrari a kol., 2026 | Ferrari A, Goossens M, Van Bos L et al. Improving participation in breast cancer screening through a tailored reminder letter: a randomized controlled trial tackling socioeconomic inequities. International Journal for Equity in Health, 2026 (v tisku). |
| Hewitson a kol., 2011 | Hewitson P, Ward AM, Heneghan C et al. Primary care endorsement letter and a patient leaflet to improve participation in colorectal cancer screening: results of a factorial randomised trial. British Journal of Cancer, 2011. |
| Kerrison a kol., 2015 | Kerrison RS, Shukla H, Cunningham D et al. Text-message reminders increase uptake of routine breast screening appointments: a randomised controlled trial in a hard-to-reach population. British Journal of Cancer, 2015. |
| Lee a kol., 2026 | Lee SC, Lucky SS, Zhu J et al. Pragmatic Interventions to Boost Surveillance Mammogram Uptake Among an Overdue Population: A Randomized Clinical Trial. JAMA Internal Medicine, 2026. |
| Li a kol., 2026 | Li SJ, Brentnall AR, Cookson J et al. The effect of different combinations of open invitations and timed appointments on breast screening attendance: service evaluation of invitation strategies in the NHS Breast Screening Programme. British Journal of Cancer, 2026. |
| Merrick a kol., 2015 | Merrick EL, Hodgkin D, Horgan CM et al. Testing novel patient financial incentives to increase breast cancer screening. The American Journal of Managed Care, 2015. |
| metodika VZP 2026 | VZP ČR. Metodika pro PZS – úhrady ambulantní gynekologie 2026, verze 1.6, platná k 27. 1. 2026. |
| Pohl a kol., 2025 | Pohl AL, Aderonmu AA, Grab JD et al. Transportation Insecurity, Social Support, and Adherence to Cancer Screening. JAMA Network Open, 2025. |
| Ricci-Cabello a kol., 2023 | Ricci-Cabello I, Carvallo-Castañeda D, Vásquez-Mejía A et al. Characteristics and impact of interventions to support healthcare providers’ compliance with guideline recommendations for breast cancer: a systematic literature review. Implementation Science, 2023. |
| Rossi a kol., 2024 | Rossi J, Mullen LA, Oluyemi ET et al. Patient Utilization of Weekend and Evening Appointments for Screening Mammography: An 8-Year Observational Cohort Study. Journal of the American College of Radiology, 2024. |
| Ziegler a kol., 2026 | Ziegler AM, Harold P, Tumiel-Berhalter LM. Implementing mobile mammography in primary care: a community-based Reach, Effectiveness, Adoption, Implementation, and Maintenance (RE-AIM) evaluation. Translational Behavioral Medicine, 2026. |

- Zdroj: PAPERS.md; papers/

## Slajd 57

- PŘÍLOHA
- Data VZP a jejich omezení
- Co data jsou
- 1 344 556 adresných pozvánek VZP (dopisy 3, 4, 7 a 8) z let 2020–2024 pro 508 527 žen nepřetržitě pojištěných 2015–2025.
- Koho obsahují
- jen ženy, které VZP zvala, tedy ženy mimo doporučený interval; ženy 40–74 let, bez 75+ a bez nově pojištěných.
- Co měříme
- účast do 3, 6 a 12 měsíců od pozvánky; výkony zahrnují i doplňující snímky a ultrazvuk.
- Region
- územní pracoviště VZP, ne okres; okresní ukazatele lze napojit jen přibližně.
- Co chybí
- kategorie plátce, okres bydliště, registrující lékař, typ a znění dopisu, kanály, pozvánky po 7/2026.
- Zdroj: data VZP pro Rakathon 2026 a rozhraní dat; docs/RAKATHON_MODEL.md

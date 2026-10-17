# Literatura: hlavní poznatky

Rešerše pro analýzu okresů, analýzy dat VZP a framework `mamoframe` (výzva VZP *Od pozvánky k mamografu*).
Každý zdroj má klíč `[KLÍČ]`. Poznámka „použito:“ odkazuje na notebooky a konfiguraci frameworku, které zůstaly
v původním repozitáři `mamograf-data-exploration`.
Literatura je rozdělená na dvě části: [**Část I. Lidé**](#cast-lide) (co víme o ženách, nemoci, intervencích, nákladech a českém programu) a [**Část II. Metodika**](#cast-metodika) (statistika, strojové učení, kauzální odhady, design experimentů). PDF volně dostupných článků jsou v [`papers/people/`](papers/people/) a [`papers/methods/`](papers/methods/) pod názvem `<KLÍČ>.pdf`; placené zdroje mají jen odkaz.

**Stupeň důkazu:** **A** = RCT nebo metaanalýza RCT u mamografie · **B** = RCT u jiného screeningu nebo
kvazi-experiment u mamografie · **C** = observační, modelová studie, odhad.

> Metadata (autoři, rok, časopis) jsou ověřená přes Europe PMC a arXiv (10/2026). Proti původní rešerši
> jsou opravené tři chyby: prohozené odkazy u `[MST_NORWAY2005]`/`[MST_KOREA2023]`, studie `[ML_SPAIN2021]`
> je z Koreje a přehled simulačních modelů má vlastní klíč `[SIM_MODELS2021]`.

## Co z toho plyne

- **Minulé chování a „preventivní habitus“ dominují.** Kdo chodí na jinou prevenci (děložní čípek, gynekolog),
  chodí i na mamograf (`[DK_CERV_BREAST]`, okresní data v README). Neúčast dále předpovídají dávky, důchod,
  komorbidity a migrace (`[DK_2024]`, `[DK_2012]`); vzdělání má vliv ve tvaru U.
- **Nejlépe doložené intervence jsou levné:** pevný termín místo otevřené pozvánky (+12–19 p. b.,
  `[NHS_TIMED2026]`, `[LONDON_OPEN2022]`, `[NHS_2ND_TIMED2017]`), připomínky včetně SMS (OR ~1,8,
  `[META_UNDERSERVED2025]`, `[CRC_BEHAV2025]`) a doporučení od lékaře (+6 p. b., `[GP_ENDORSE2011]`).
  U znevýhodněných skupin jsou účinky větší.
- **AI a personalizace zatím nemají doklad o vlivu na chování:** LLM zprávy zvyšují záměr, ale ne víc než
  dobré materiály, a personalizované riziko účast nezvýšilo (`[LLM_HPV2025]`, `[LLM_CRC2025]`,
  `[RISKMSG_CRC2025]`). Ve frameworku mají prior se středem 0 a musí se ověřit experimentem.
- **Přínos screeningu:** 7–9 odvrácených úmrtí na 1 000 žen za 10 kol (50–69), tj. asi 1 úmrtí na
  1 100–1 400 mamografií, za cenu 4 overdiagnóz (`[EUROSCREEN2012]`). Připomínky stojí desítky USD na
  dodatečně vyšetřenou ženu (`[CE_REVIEW2024]`), navigace stovky (`[NAVIGATION_ECON2024]`).
- **Priory převádíme do log-OR:** uplift jednotlivce σ(logit p₀ + log OR) − p₀ je největší kolem p₀ ≈ 0,5.
  Riziko neúčasti ≠ uplift: nejrizikovější ženy často reagují na levné kanály nejméně.
- **Metodika (Část II):** vysvětlení modelu přes SHAP a aditivní modely (EBM) je standard; pro cílení se neodhaduje riziko, ale heterogenní účinek (meta-learnery, causal forest) a jeho kalibrace. Účinek se ověřuje pevně randomizovaným experimentem s chráněnou kontrolou, ne adaptivní randomizací (`[ADAPTIVE_RAND2015]`); změny pravidel bez randomizace (žádanka 7/2026) přerušenou časovou řadou (`[ITS_GUIDELINE2022]`).

<a id="cast-lide"></a>

## Část I. Lidé: co víme o ženách, nemoci a intervencích

Empirické studie a dokumenty: kdo na screening chodí a kdo ne, co účast zvyšuje, jak reagují na zprávy, přirozený průběh nemoci, náklady a užitky, český program. PDF jsou v [`papers/people/`](papers/people/).

### I.1 Kontext v ČR

#### `[CZ_INVITE2019]` Evaluation of the personalized invitation of Czech citizens to screening programs

Ngo O, Chloupková R, Ambrožová M et al. 2019. *Casopis lekaru ceskych*. · [odkaz](https://pubmed.ncbi.nlm.nih.gov/31416323/) · stupeň **C** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Adresné zvaní pojišťovnami od 2014: za 4 roky přes 6 mil. pozvánek (~3 mil. osob).
- Účast po 1. pozvánce: prs 22,3 %, kolorektum 21,7 %, děložní čípek 15,5 %.
- Účinek s opakovaným zvaním klesá; velká část pozvaných stále nepřijde.

#### `[CZ_TRENDS2011]` Breast cancer screening in the Czech Republic: time trends in performance indicators during the first seven years of the organised programme

Majek O, Danes J, Skovajsova M et al. 2011. *BMC public health*. · [odkaz](https://doi.org/10.1186/1471-2458-11-288) · PDF: [`papers/people/CZ_TRENDS2011.pdf`](papers/people/CZ_TRENDS2011.pdf) · stupeň **C** · použito: `05_ekonomika_qaly.ipynb`, `econ_params.yaml`

- Program od 2002 (síť akreditovaných center); registr 2,08 mil. epizod 2002–2008.
- Pokrytí 45–69 let 2007–08: 51 %. Incidence roste, ale s větším podílem časných stadií; mortalita se stabilizuje.

### I.2 Kdo nechodí: prediktory neúčasti

#### `[MANDRIK2021]` Systematic reviews as a "lens of evidence": Determinants of participation in breast cancer screening

Mandrik O, Tolma E, Zielonke N et al. 2021. *Journal of medical screening*. · [odkaz](https://doi.org/10.1177/0969141320930743) · stupeň **A** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Přehled 31 přehledů: účast 16–90 % podle programu.
- Pomáhají levné intervence: pozvánka, informace, opakované připomínky, **pevný termín**, výzva od zdravotníka, blízkost centra.
- Složité intervence (poradenství tváří v tvář, návštěvy doma, média) nedoporučuje bez dalších důkazů. Opakovaná účast je vysoká (> 62 %).

#### `[DK_2024]` Non-participation in breast screening in Denmark: Sociodemographic determinants

von Euler-Chelpin M, Napolitano G, Lynge E et al. 2024. *BMC public health*. · [odkaz](https://doi.org/10.1186/s12889-024-19547-x) · PDF: [`papers/people/DK_2024.pdf`](papers/people/DK_2024.pdf) · stupeň **C**

- Dánsko (196 tis. žen, 86 % účast): nejsilnější prediktory neúčasti jsou dávky (OR 3,7), důchod (3,1), narození mimo DK (2,0), svobodné (2,0), komorbidita (1,6).
- Vzdělání má vliv ve tvaru U (nejnižší neúčast u bakalářek, OR 0,64).

#### `[DK_2012]` Identifying specific non-attending groups in breast cancer screening--population-based registry study of participation and socio-demography

Jensen LF, Pedersen AF, Andersen B et al. 2012. *BMC cancer*. · [odkaz](https://doi.org/10.1186/1471-2407-12-518) · PDF: [`papers/people/DK_2012.pdf`](papers/people/DK_2012.pdf) · stupeň **C** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- 1. kolo v regionu Střední Dánsko (149 tis. žen, účast 78,9 %).
- Neúčast: vyšší věk, imigrantky, nízký příjem, nezaměstnanost, svobodné, nájem, bez auta, **vzdálenost > 20 km**.
- Neúčastnice nejsou homogenní: aktivní odmítnutí vs. pasivní nedostavení se liší profilem.

#### `[DK_CERV_BREAST]` Strong association between cervical and breast cancer screening behaviour among Danish women; A register-based cohort study

Larsen SH, Virgilsen LF, Kristiansen BK et al. 2018. *Preventive medicine reports*. · [odkaz](https://doi.org/10.1016/j.pmedr.2018.10.017) · PDF: [`papers/people/DK_CERV_BREAST.pdf`](papers/people/DK_CERV_BREAST.pdf) · stupeň **C**

- Ženy bez screeningu děložního čípku mají 2,8× vyšší pravděpodobnost neúčasti na screeningu prsu.
- Podporuje „preventivní habitus“: stejný vzorec, jaký vidíme po okresech u gynekologické prevence (README).

#### `[MALTA2019]` Predicting reattendance to the second round of the Maltese national breast screening programme: an analytical descriptive study

Marmarà D, Marmarà V, Hubbard G. 2019. *BMC public health*. · [odkaz](https://doi.org/10.1186/s12889-019-6507-9) · PDF: [`papers/people/MALTA2019.pdf`](papers/people/MALTA2019.pdf) · stupeň **C** · použito: `05_ekonomika_qaly.ipynb`, `econ_params.yaml`

- Malý vzorek (100 žen). Účast ve 2. kole souvisí hlavně s vnímanou ohrožeností a znalostí intervalu, ne se socioekonomikou.

#### `[NL_2022]` Factors determining non-attendance in breast cancer screening among women in the Netherlands: a national study

Gong J, Kampadellis G, Kong Q et al. 2023. *Health promotion international*. · [odkaz](https://doi.org/10.1093/heapro/daac009) · stupeň **C**

- Průzkum 1 227 neúčastnic v NL: důvody jsou overdiagnóza, falešně negativní výsledek, záření, bolest.
- Názor lékaře a oportunní screening tyto obavy zesilují; ženy, které nikdy nebyly, odmítají častěji.

#### `[ML_SPAIN2021]` Predicting Participation in Cancer Screening Programs with Machine Learning

Donghyun Kim. 2021. *arXiv*. · [odkaz](https://arxiv.org/abs/2101.11614) · PDF: [`papers/people/ML_SPAIN2021.pdf`](papers/people/ML_SPAIN2021.pdf) · stupeň **C**

- **Pozor: studie je z Jižní Koreje, ne ze Španělska** (klíč ponechán kvůli kompatibilitě).
- Gradient boosting predikuje účast na národním screeningu s AUC 0,87.

#### `[ML_INTERSECT2024]` Intersectional analysis of inequalities in self-reported breast cancer screening attendance using supervised machine learning and PROGRESS-Plus framework

Pedrós Barnils N, Schüz B. 2023. *Frontiers in public health*. · [odkaz](https://doi.org/10.3389/fpubh.2023.1332277) · PDF: [`papers/people/ML_INTERSECT2024.pdf`](papers/people/ML_INTERSECT2024.pdf) · stupeň **C**

- Španělsko, EHIS 2020: XGBoost (AUC 0,79); nejdůležitější je **region**, pak vzdělání, věk, rodinný stav.
- Intersekcionální skupiny (PROGRESS-Plus) odhalí kombinace s nejnižší účastí.

#### `[PA_2025]` Multilevel Predictive Study of Breast Cancer Screening Patterns in Pennsylvania, 2021-2022

Brogan C, Tuan WJ. 2025. *Journal of primary care & community health*. · [odkaz](https://doi.org/10.1177/21501319251391008) · PDF: [`papers/people/PA_2025.pdf`](papers/people/PA_2025.pdf) · stupeň **C**

- Pensylvánie, 21,5 tis. žen 50–74: víceúrovňový model (osoba, praxe, sousedství).
- Menšiny a vyšší index deprivace oblasti (ADI) snižují dodržování screeningu.

### I.3 Co zvyšuje účast: intervence

#### `[META_UNDERSERVED2025]` Advancing Mammographic Screening Among Underserved Groups: A Systematic Review and Meta-Analysis of Intervention Strategies to Increase Breast Cancer Screening Uptake

Ferrari A, Jael Herrera D, Van De Veerdonk W et al. 2025. *Public health reviews*. · [odkaz](https://doi.org/10.3389/phrs.2025.1607873) · PDF: [`papers/people/META_UNDERSERVED2025.pdf`](papers/people/META_UNDERSERVED2025.pdf) · stupeň **A** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- 44 RCT, 161 tis. žen: intervence vs. běžná péče OR 1,55 (1,39–1,73); u znevýhodněných OR 1,81 (1,43–2,28).
- U znevýhodněných nejlépe fungují připomínky, telefonáty, navigace a kulturně přizpůsobený přístup.

#### `[LOWINCOME2013]` Interventions to increase the uptake of mammography amongst low income women: a systematic review and meta-analysis

Gardner MP, Adams A, Jeffreys M. 2013. *PloS one*. · [odkaz](https://doi.org/10.1371/journal.pone.0055574) · PDF: [`papers/people/LOWINCOME2013.pdf`](papers/people/LOWINCOME2013.pdf) · stupeň **A**

- 21 RCT u nízkopříjmových žen: intervence zvyšují účast o 8,9 p. b. (7,3–10,4).
- Nejúčinnější jsou kombinované intervence a ty, které zlepšují přístup.

#### `[MAILED_REMINDER1997]` MAILED_REMINDER1997

metadata neověřena · [odkaz](https://www.sciencedirect.com/science/article/abs/pii/S0749379797000032) · stupeň **A** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Metaanalýza poštovních připomínek: mírný pozitivní účinek. (Abstrakt neověřen přes Europe PMC.)

#### `[NHS_TIMED2026]` The effect of different combinations of open invitations and timed appointments on breast screening attendance: service evaluation of invitation strategies in the NHS Breast Screening Programme

Li SJ, Brentnall AR, Cookson J et al. 2026. *British journal of cancer*. · [odkaz](https://doi.org/10.1038/s41416-026-03436-8) · PDF: [`papers/people/NHS_TIMED2026.pdf`](papers/people/NHS_TIMED2026.pdf) · stupeň **B** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- NHS, 18 tis. žen kvazi-randomizovaných: účast 49,1 % (otevřená/otevřená) → 67,9 % (pevný/pevný termín).
- Efekt je ve všech kvintilech deprivace; u nejchudších 41 % → 63 %.

#### `[NHS_2ND_TIMED2017]` Effect of second timed appointments for non-attenders of breast cancer screening in England: a randomised controlled trial

Allgood PC, Maroni R, Hudson S et al. 2017. *The Lancet. Oncology*. · [odkaz](https://doi.org/10.1016/s1470-2045(17)30340-6) · PDF: [`papers/people/NHS_2ND_TIMED2017.pdf`](papers/people/NHS_2ND_TIMED2017.pdf) · stupeň **A** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- RCT: druhý **pevný termín** pro neúčastnice 1. termínu zvyšuje účast oproti dopisu s telefonním číslem.

#### `[LONDON_OPEN2022]` Did the use of open invitations in place of timed appointment invitations reduce the uptake of breast screening in the London region during the COVID-19 recovery?

Hudson SM, Binysh K, Duffy SW. 2023. *Journal of medical screening*. · [odkaz](https://doi.org/10.1177/09691413221127583) · stupeň **B** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Přirozený experiment v Londýně (covid): pevný termín 60,6 % vs. otevřená pozvánka 53,1 % účasti.

#### `[GP_ENDORSE2011]` Primary care endorsement letter and a patient leaflet to improve participation in colorectal cancer screening: results of a factorial randomised trial

Hewitson P, Ward AM, Heneghan C et al. 2011. *British journal of cancer*. · [odkaz](https://doi.org/10.1038/bjc.2011.255) · PDF: [`papers/people/GP_ENDORSE2011.pdf`](papers/people/GP_ENDORSE2011.pdf) · stupeň **B** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Faktoriální RCT (kolorektum): doporučující dopis praktika +5,8 p. b., srozumitelný leták +6,0 p. b., bez interakce.

#### `[CRC_BEHAV2025]` Behavioral Interventions Improve Mailed Colorectal Cancer Screening Among Overdue Patients in a Randomized Trial

Mehta SJ, Nadella P, Shaw PA et al. 2026. *Clinical gastroenterology and hepatology : the official clinical practice journal of the American Gastroenterological Association*. · [odkaz](https://doi.org/10.1016/j.cgh.2025.09.015) · stupeň **B**

- Faktoriální RCT (5 244 pacientů po termínu, FIT poštou): **SMS připomínky +6,6 p. b.** (21,2 % vs. 14,6 %).
- Výrazná krabička místo obálky nepomohla (−0,2 p. b.).

#### `[NAVIGATION_ECON2024]` Breast and Cervical Cancer Screenings: A Systematic Economic Review of Patient Navigation Services

Chattopadhyay SK, Pillai A, Reynolds J et al. 2024. *American journal of preventive medicine*. · [odkaz](https://doi.org/10.1016/j.amepre.2024.06.005) · stupeň **A/C** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Pacientská navigace u screeningu prsu: náklad na osobu 109–10 245 USD, na dodatečně vyšetřenou 154–740 USD.
- Náklady na QALY 3 852–39 159 USD (vše pod 50 tis. USD).

#### `[CERV_IMMIGRANT2023]` Interventions to increase cervical screening uptake among immigrant women: A systematic review and meta-analysis

Alam Z, Cairns JM, Scott M et al. 2023. *PloS one*. · [odkaz](https://doi.org/10.1371/journal.pone.0281976) · PDF: [`papers/people/CERV_IMMIGRANT2023.pdf`](papers/people/CERV_IMMIGRANT2023.pdf) · stupeň **B**

- Imigrantky, screening děložního čípku: komunitní, jazykově a kulturně přizpůsobené intervence účast zvyšují.

### I.4 AI a personalizované zprávy

#### `[LLM_HPV2025]` Large Language Model Chatbot Conversations vs Public Health Materials and Parental HPV Vaccination Intentions: A Randomized Clinical Trial

Sehgal NKR, Rai S, Tonneau M et al. 2026. *JAMA network open*. · [odkaz](https://doi.org/10.1001/jamanetworkopen.2026.16822) · PDF: [`papers/people/LLM_HPV2025.pdf`](papers/people/LLM_HPV2025.pdf) · stupeň **A** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- RCT: rozhovor s LLM chatbotem zvýšil záměr očkovat proti HPV oproti žádné intervenci, **ne oproti běžným materiálům**.
- Účinek do 45 dní vyprchal. Měří záměr, ne chování.

#### `[LLM_CRC2025]` Effects of Static and Conversational AI-Generated Messages on Colorectal Cancer Screening Intent: a Randomized Clinical Trial

Neil K. R. Sehgal, Manuel Tonneau, Andy SL Tan et al. 2025. *arXiv*. · [odkaz](https://arxiv.org/abs/2507.08211) · PDF: [`papers/people/LLM_CRC2025.pdf`](papers/people/LLM_CRC2025.pdf) · stupeň **B** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- RCT (915 dospělých bez screeningu): AI zprávy zvýšily záměr udělat test stolice o 12,9–13,8 bodu vs. 7,5 u expertních materiálů.
- Chatbot nebyl lepší než jedna statická AI zpráva. Vliv na skutečný screening neznámý.

#### `[RISKMSG_CRC2025]` Effect of Personalized Risk Messages on Uptake of Colorectal Cancer Screening : A Randomized Controlled Trial

Schwartz PH, Perkins SM, Rawl SM et al. 2025. *Annals of internal medicine*. · [odkaz](https://doi.org/10.7326/ANNALS-24-03144) · stupeň **A** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- Faktoriální RCT: personalizovaná informace o riziku pacientovi ani lékaři **nezvýšila** účast na screeningu kolorekta.

### I.5 Ekonomika a přirozený průběh nemoci

#### `[CE_REVIEW2024]` Evaluation of the Cost-Effectiveness of Evidence-Based Interventions to Increase Female Breast and Cervical Cancer Screens: A Systematic Review

Phillips V, Franco Montoya D, Adams EK. 2024. *Cancers*. · [odkaz](https://doi.org/10.3390/cancers16061134) · PDF: [`papers/people/CE_REVIEW2024.pdf`](papers/people/CE_REVIEW2024.pdf) · stupeň **A/C**

- 11 studií nákladové efektivity intervencí CPSTF: průměrný ICER u prsu 545 USD na dodatečně vyšetřenou ženu.
- Nejlevnější jsou připomínky a recall systémy pro ženy už v péči (průměr ~41 USD).

#### `[SMS_CALD2025]` Cost-Effectiveness of Text Messaging to Reengage Culturally and Linguistically Diverse Communities to Breast Cancer Screening: A Modeling Study

Lal A, Mudford E, Elsworth J et al. 2026. *Value in health regional issues*. · [odkaz](https://doi.org/10.1016/j.vhri.2025.101150) · stupeň **C** · použito: `04_intervence_dukazy.ipynb`, `interventions.yaml`

- SMS v mateřském jazyce pro ženy po termínu (Victoria, AU): objednání 12,7 % vs. 8,2 % u anglické SMS.
- 1,24 AUD na osobu, ~1 595 AUD/QALY.

#### `[MST_NORWAY2005]` Estimating mean sojourn time and screening test sensitivity in breast cancer mammography screening: new results

Weedon-Fekjaer H, Vatten LJ, Aalen OO et al. 2005. *Journal of medical screening*. · [odkaz](https://doi.org/10.1258/096914105775220732) · stupeň **C** · použito: `econ_params.yaml`

- Norsko (395 tis. žen): MST 6,1 roku (50–59) a 7,9 roku (60–69), citlivost 58 % a 73 %.
- Při započtení HRT klesá MST na 3,9–5,0 roku a citlivost roste na 75–85 %.

#### `[MST_KOREA2023]` Estimating Age-Specific Mean Sojourn Time of Breast Cancer and Sensitivity of Mammographic Screening by Breast Density among Korean Women

Choi E, Suh M, Jung SY et al. 2023. *Cancer research and treatment*. · [odkaz](https://doi.org/10.4143/crt.2021.962) · PDF: [`papers/people/MST_KOREA2023.pdf`](papers/people/MST_KOREA2023.pdf) · stupeň **C** · použito: `econ_params.yaml`

- Korea: MST nejkratší u mladších (40–49: ~2,0 roku, 50–59: ~2,5 roku), citlivost klesá s hustotou prsu.

#### `[MST_NIJMEGEN2019]` Test sensitivity of mammography and mean sojourn time over 40 years of breast cancer screening in Nijmegen (The Netherlands)

Aarts A, Duffy SW, Geurts S et al. 2019. *Journal of medical screening*. · [odkaz](https://doi.org/10.1177/0969141318814869) · stupeň **C** · použito: `econ_params.yaml`

- 40 let screeningu v Nijmegenu: citlivost mamografie a MST v čase (abstrakt nedostupný přes Europe PMC).

#### `[EUROSCREEN2012]` Summary of the evidence of breast cancer service screening outcomes in Europe and first estimate of the benefit and harm balance sheet

Paci E, EUROSCREEN Working Group. 2012. *Journal of medical screening*. · [odkaz](https://doi.org/10.1258/jms.2012.012077) · stupeň **C** · použito: `econ_params.yaml`

- Na 1 000 žen screenovaných 50–69 let (sledovaných do 79): **7–9 odvrácených úmrtí**, 4 overdiagnózy, 170 falešně pozitivních bez invazivního a 30 s invazivním vyšetřením.
- Snížení mortality u pozvaných 25–31 %, u screenovaných 38–48 %. Overdiagnóza 6,5 %.
- Navazující článek: Paci 2014, CEBP, [doi](https://doi.org/10.1158/1055-9965.EPI-13-0320).

#### `[UTIL_KAUR2022]` A Systematic Literature Review of Health Utility Values in Breast Cancer

Kaur MN, Yan J, Klassen AF et al. 2022. *Medical decision making : an international journal of the Society for Medical Decision Making*. · [odkaz](https://doi.org/10.1177/0272989X211065471) · stupeň **C** · použito: `econ_params.yaml`

- 79 studií užitků u karcinomu prsu (většinou EQ-5D): pokročilé stadium 0,08–0,82, časné výrazně výš; velký rozptyl mezi studiemi.

#### `[UTIL_STAGE2021]` Health state utility values by cancer stage: a systematic literature review

Pourrahmat MM, Kim A, Kansal AR et al. 2021. *The European journal of health economics : HEPAC : health economics in prevention and care*. · [odkaz](https://doi.org/10.1007/s10198-021-01335-8) · PDF: [`papers/people/UTIL_STAGE2021.pdf`](papers/people/UTIL_STAGE2021.pdf) · stupeň **C** · použito: `econ_params.yaml`

- Užitky klesají se stadiem u všech nádorů; největší pokles mezi stadiem I–III a IV.

### I.6 Veřejná mikrodata

#### `[SHARE]` Who gets a mammogram amongst European women aged 50-69 years?

Wuebker A. 2012. *Health economics review*. · [odkaz](https://doi.org/10.1186/2191-1991-2-6) · PDF: [`papers/people/SHARE.pdf`](papers/people/SHARE.pdf) · stupeň **C** · použito: `09_verejna_mikrodata.ipynb`, `microdata.py`

- SHARE, ženy 50–69 v Evropě: mamografii častěji podstupují vzdělanější, s partnerem, mladší, zdravější a s kvalitnějším lékařem.

### I.7 Ostatní zdroje (weby, úřední dokumenty, data)

| Klíč | Co z něj bereme | Odkaz |
|---|---|---|
| `[CZ_PROGRAM]` | Pravidla programu: od 45 let, bez horní hranice, jednou za 2 roky, plně hrazeno; 75 center. | [odkaz](https://www.mamo.cz/) |
| `[VZP_2026]` | Od 1. 7. 2026 screening bez žádanky (odhad +5–8 p. b.); VZP 442 tis. klientek ročně, 59 tis. léčených, > 3,6 mld. Kč/rok. | [odkaz](https://www.vzp.cz/o-nas/aktuality/zeny-od-45-let-budou-mit-jednodussi-cestu-na-mamograficky-screening) |
| `[UZIS_SVOD2022]` | 7 918 nových C50 (2022), 144,5/100 tis. žen, téměř 80 % ve stadiu I–II. | [odkaz](https://www.svod.cz/incidence) |
| `[OECD_CZ2023]` | OECD/EU profil nádorových onemocnění ČR 2023. | [odkaz](https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/02/eu-country-cancer-profile-czech-republic-2023_42c64a42/c37fd099-en.pdf) · [PDF](papers/people/OECD_CZ2023.pdf) |
| `[COMMUNITY_GUIDE]` | CPSTF: připomínky klientkám doporučeny se silnými důkazy. | [odkaz](https://thecommunityguide.org/findings/cancer-screening-client-reminders-breast-cancer.html) |
| `[COMMUNITY_GUIDE_ECON]` | Telefonická připomínka ~0,35 USD/ženu; 7,89–1 149 USD na dodatečnou mamografii. | [odkaz](https://stacks.cdc.gov/view/cdc/260495/cdc_260495_DS1.pdf) |
| `[REPEAT_META]` | Intervence pro opakovanou účast: mírný účinek (NCBI Bookshelf). | [odkaz](https://www.ncbi.nlm.nih.gov/books/NBK78582/) |
| `[SUKL_WTP]` | Práh ochoty platit SÚKL ~1,2 mil. Kč/QALY (2017), reálně ~0,78 mil. Kč v cenách 2026. Postup SÚKL je v PDF. | [odkaz](https://sukl.gov.cz/wp-content/uploads/2024/06/05-A-SP-CAU-028-Postup_pro_posuzovani_analyzy_nakladove_efektivity-17012022.pdf) · [PDF](papers/people/SUKL_WTP.pdf) |
| `[CZ_STAGE_COST]` | Náklady léčby podle stadia (I 51 tis. – IV 123 tis. Kč); pro dnešní léčbu stadia IV silně podhodnocené. | [odkaz](https://zdravi.euro.cz/clanek/postgradualni-medicina-priloha/farmakoekonomicke-aspekty-karcinomu-prsu-447772) |
| `[SAMOPLATCE]` | Samoplátecký ceník EUC (mamografie ~1 200 Kč); úhradu výkonu 89223 ověřit ve vyhlášce. | [odkaz](https://euc.cz/media/4927/cen%C3%ADk-samopl%C3%A1tc%C5%AF-od-1-1-2023.pdf) · [PDF](papers/people/SAMOPLATCE.pdf) |
| `[SURV_STAGE_CZ]` | Pětileté přežití podle stadia: I ~90 %, II 86–91 %, III 54–67 %, IV ~20 %. | [odkaz](https://www.rakovinaprsu.cz/o-rakovine-prsu/stadia-onemocneni/) |
| `[EHIS]` | European Health Interview Survey 2019: mamografie za 2 roky (EU 66 % u 50–69); mikrodata na smlouvu. | [odkaz](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=European_health_interview_survey_-_methodology) |
| `[BRFSS]` | US BRFSS (`LLCP2022.XPT`): veřejná mikrodata, jen na nácvik metod. | [odkaz](https://www.cdc.gov/brfss/annual_data/annual_2022.html) |
| `[REPO]` | Vlastní okresní analýza tohoto repozitáře (README, `notebooks/mamograf_analyza.ipynb`). | [odkaz](README.md) |

### I.8 Zdroje research briefu

Zdroje z [`docs/rakathon-mamograf-research-brief.md`](docs/rakathon-mamograf-research-brief.md); číslo v hranatých
závorkách je číslo v briefu. Zdroje, které už jsou výše, tu nejsou znovu: [12] = `[DK_2012]`, [19] = `[ML_INTERSECT2024]`,
[20] = `[ML_SPAIN2021]`, [29] = `[NHS_2ND_TIMED2017]`, [35] = `[META_UNDERSERVED2025]` (jeho PDF je v `papers/people/`).
Metodické zdroje briefu ([21]–[28], [39], [40], [42], [43], [45], [46]) jsou v [Části II](#cast-metodika).
Weby a tiskové zprávy [1–5], [8], [9], [41], [44] a [47] jsou jen v briefu.

| Brief | Klíč | Zdroj | Hlavní poznatek | PDF |
|---|---|---|---|---|
| [6] | `[NZIP_POKRYTI2024]` | [odkaz](https://www.nzip.cz/data/koncepce2025/k02-p04.pdf) | ÚZIS/NZIP: pokrytí žen 45–69 mamografickým screeningem 2023–2024 po okresech; ČR 59,9 %, od 73,6 % (Třebíč) po 45,8 % (Cheb). | [PDF](papers/people/NZIP_POKRYTI2024.pdf) |
| [7] | `[AMBROZOVA2023]` | [odkaz](https://preview-mamo.iba.muni.cz/res/file/datovy-audit-prezentace/2023/12-ambrozova-veverkova.pdf) | Dotazník 71 center (2023): 36 vlastní pozvánky neposílá; zvoucí centra mají o ~10 p. b. vyšší návrat v dalším kole (75,4 vs. 65,3 %), observačně. | [PDF](papers/people/AMBROZOVA2023.pdf) |
| [10] | `[MOTTRAM2021]` | [Factors associated with attendance at screening for breast cancer: a systematic review and meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC8634222/). Mottram R, Knerr WL, Gallacher D et al. 2021. *BMJ open*. | Metaanalýza 66 studií: nejsilnější je předchozí účast (OR 3,32), první pozvánka OR 0,22, falešně pozitivní recall OR 0,77, bez auta OR 0,33–0,43, venkov vs. město bez rozdílu. | [PDF](papers/people/MOTTRAM2021.pdf) |
| [11] | `[DK_MULTIMORB2015]` | [Non-participation in breast cancer screening for women with chronic diseases and multimorbidity: a population-based cohort study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4623919). Jensen LF, Pedersen AF, Andersen B et al. 2015. *BMC cancer*. | Dánsko: těžká multimorbidita zvyšuje neúčast (prevalence ratio 1,53); chronické a duševní nemoci jsou bariéra. | [PDF](papers/people/DK_MULTIMORB2015.pdf) |
| [13] | `[DK_MIGRANT2012]` | [Participation in mammography screening among migrants and non-migrants in Denmark](https://medicaljournalssweden.se/actaoncologica/article/view/28475). Kristiansen M, Thorsted BL, Krasnik A et al. 2012. *Acta oncologica (Stockholm, Sweden)*. | Dánsko: migrantky chodí méně; chybějící kontakt s praktikem či zubařem snižuje účast. | – |
| [14] | `[NI_INTERMITTENT2014]` | [Do women who intermittently attend breast screening differ from those who attend every invitation and those who never attend?](https://doi.org/10.1177/0969141314533677). Coyle C, Kinnear H, Rosato M et al. 2014. *Journal of medical screening*. | Severní Irsko: ženy chodící občas se sociálně liší od těch, které nechodí nikdy; neúčastnice nejsou jedna skupina. | – |
| [15] | `[DE_PHONE2023]` | [Reasons for Non-Attendance in the German National Mammography Screening Program: Which Barriers Can Be Overcome Using Telephone Counseling?-A Randomized Controlled Trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC9818884/). Fochler S, Weitmann K, Domin M et al. 2022. *Healthcare (Basel, Switzerland)*. | RCT, venkovské Německo: telefonické poradenství podle bariéry pomohlo u ztracených dopisů a nevhodných termínů (45,9 vs. 28,6 % mezi zastiženými), ne u žen, které se cítí zdravé nebo se screenují jinde; 51,5 % neúčastnic uvedlo vyšetření prsu jinde. | [PDF](papers/people/DE_PHONE2023.pdf) |
| [16] | `[SE_FIRST2025]` | [First mammography screening participation and breast cancer incidence and mortality in the subsequent 25 years: population based cohort study](https://doi.org/10.1136/bmj-2025-085029). Ma Z, He W, Zhang Y et al. 2025. *BMJ (Clinical research ed.)*. | Stockholm: 32,1 % žen vynechalo první pozvánku a i později chodily méně; BMJ k článku připojil vyjádření znepokojení (expression of concern). | – |
| [17] | `[US_PROVIDER2018]` | [Multi-level Influences on Breast Cancer Screening in Primary Care](https://doi.org/10.1007/s11606-018-4560-1). Onega T, Tosteson TD, Weiss J et al. 2018. *Journal of General Internal Medicine*. | Po očištění o pacientky: 41 % zbývající variability mezi praktickými lékaři připadá na jednotlivé lékaře uvnitř praxe, 35 % na zdravotní systémy, 24 % na praxe (ověřeno v článku). | [PDF](papers/people/US_PROVIDER2018.pdf) |
| [18] | `[QC_DISTANCE2013]` | [Geographic access to mammography screening centre and participation of women in the Quebec Breast Cancer Screening Programme](https://jech.bmj.com/content/67/10/861). St-Jacques S, Philibert MD, Langlois A et al. 2013. *Journal of epidemiology and community health*. | Quebec (834 tis. žen): účast o 6,3 p. b. nižší ve vzdálenosti 50–75 km a o 9,8 p. b. nad 75 km; práh roste od měst k venkovu. | – |
| [30] | `[NHS_POSTAL2016]` | [A randomised trial of the effect of postal reminders on attendance for breast screening](https://pmc.ncbi.nlm.nih.gov/articles/PMC5154292). Allgood PC, Maxwell AJ, Hudson S et al. 2016. *British journal of cancer*. | RCT (22 828 žen, SZ Anglie): poštovní připomínka +4,0 p. b. do 30 dní, +2,7 p. b. do 180 dní; u starších dřívějších neúčastnic po 180 dnech bez efektu. | [PDF](papers/people/NHS_POSTAL2016.pdf) |
| [31] | `[NHS_SMS2015]` | [Text-message reminders increase uptake of routine breast screening appointments: a randomised controlled trial in a hard-to-reach population](https://wrap.warwick.ac.uk/73445/). Kerrison RS, Shukla H, Cunningham D et al. 2015. *British journal of cancer*. | RCT (2 240 prvních pozvánek, Londýn): SMS 48 h před termínem 59,1 → 64,4 % (ITT), i když číslo mělo jen 41 %; asi 3× víc předem zrušených termínů. | [PDF](papers/people/NHS_SMS2015.pdf) |
| [32] | `[PENN_OUTREACH2024]` | [Behavioral Interventions to Improve Breast Cancer Screening Outreach: Two Randomized Clinical Trials](https://www.healthday.com/healthpro-news/womens-health/text-message-outreach-can-help-increase-mammogram-completion-rates). Mehta SJ, Rhodes C, Linn KA et al. 2024. *JAMA internal medicine*. | Dvě RCT (24 632 žen, Penn): SMS +2,1 a +2,5 p. b. za 3 měsíce; odstranění kroku žádanky 12,7 → 15,4 %; dopis od vlastního lékaře bez efektu. | – |
| [33] | `[SG_OVERDUE2026]` | [Pragmatic Interventions to Boost Surveillance Mammogram Uptake Among an Overdue Population: A Randomized Clinical Trial](https://doi.org/10.1001/jamainternmed.2025.5873). Lee SC, Lucky SS, Zhu J et al. 2026. *JAMA internal medicine*. | RCT (9 000 žen po termínu, Singapur): objednací linka 13,8 vs. 11,2 % (po korekci neprůkazné), loterie 3 209 USD na mamografii navíc, video −0,4 p. b.; push notifikace prokliklo 4,1 %. | – |
| [34] | `[US_INCENTIVE2015]` | [Testing novel patient financial incentives to increase breast cancer screening](https://scholarworks.brandeis.edu/esploro/outputs/journalArticle/Testing-novel-patient-financial-incentives-to/9924086293001921). Merrick EL, Hodgkin D, Horgan CM et al. 2015. *The American journal of managed care*. | RCT (4 427 žen, Tufts): malé finanční pobídky a loterie bez průkazného efektu. | – |
| [36] | `[COCHRANE_RISK2003]` | [Effects of communicating individual risks in screening programmes: Cochrane systematic review](https://www.bmj.com/content/327/7417/703). Edwards A, Unigwe S, Elwyn G et al. 2003. *BMJ (Clinical research ed.)*. | Cochrane, 13 RCT (10 u mamografie): sdělení individuálního rizika zvyšuje účast (OR 1,5; 1,11–2,03), ale není jasné, zda jde o informované rozhodnutí. | [PDF](papers/people/COCHRANE_RISK2003.pdf) |
| [37] | `[PROCAS2022]` | [Does receiving high or low breast cancer risk estimates produce a reduction in subsequent breast cancer screening attendance? Cohort study](https://doaj.org/article/b1795daf1c81462d9367ba104d78c031). French DP, McWilliams L, Howell A et al. 2022. *Breast (Edinburgh, Scotland)*. | Kohorta PROCAS (26 668 žen): sdělené vysoké riziko zvýšilo návrat (89,2 vs. 78,8 %), sdělené nízké riziko účast mírně snížilo (85,6 vs. 86,4 %). | [PDF](papers/people/PROCAS2022.pdf) |
| [38] | `[WISDOM2025]` | [odkaz](https://www.nih.gov/news-events/nih-research-matters/testing-risk-based-breast-cancer-screening) | RCT WISDOM: screening podle rizika (geny, rodinná anamnéza, hustota prsu) vs. roční screening. (Brief cituje shrnutí NIH; článek neověřen.) | – |

### I.9 Zdroje z Gemini Deep Research a doporučení CPSTF

Výběr ze zdrojů v [`docs/gemini_deep_research.md`](docs/gemini_deep_research.md) (číslo v hranatých závorkách je
číslo tamní reference). Metadata jsou ověřená přes Europe PMC, čísla ze shrnutí CPSTF přímo na stránkách
Community Guide (10/2026). Vynechané: [5] je už `[LOWINCOME2013]`; [7], [8], [9], [13] a [22] jsou weby nebo video;
[1], [2], [12], [24] (LMIC nebo slabší než stávající metaanalýzy), [18], [19] a [21] (mimo téma účasti).
Metodické zdroje [10] (RE-AIM) a [23] (přerušená časová řada) jsou v [Části II](#cast-metodika).

| Ref. | Klíč | Zdroj | Hlavní poznatek | PDF |
|---|---|---|---|---|
| [3] | `[COCHRANE_INVITE2001]` | [Strategies for increasing women participation in community breast cancer screening](https://doi.org/10.1002/14651858.CD002943). Bonfill X, Marzo M, Pladevall M et al. 2001. *The Cochrane database of systematic reviews*. | Cochrane, 16 RCT v populačních programech: zvací dopis OR 1,66 (1,43–1,92), poštou zaslané edukační materiály OR 2,81, dopis + telefonát OR 2,53, telefonát OR 1,94, školení + přímé připomínky OR 2,46; návštěvy doma bez efektu (OR 1,06), pozvánka na více vyšetření najednou spíš škodí (OR 0,62, neprůkazné). Studie z let před 2000. | – |
| [15] | `[IMPL_SCREEN2011]` | [What implementation interventions increase cancer screening rates? a systematic review](https://doi.org/10.1186/1748-5908-6-111). Brouwers MC, De Vito C, Bahirathan L et al. 2011. *Implementation science : IS*. | Aktualizace přehledů (66 nových RCT 2004–2010, prs, čípek, kolorektum): účinné jsou připomínky klientům, malá média a audit se zpětnou vazbou lékařům; individuální edukace a odstraňování strukturálních bariér také; pobídky klientům a lékařům, masová média, skupinová edukace a snížení spoluúčasti nemají dost důkazů. | [PDF](papers/people/IMPL_SCREEN2011.pdf) |
| [16] | `[HIT_DECAID2022]` | [Mammography and Decision Aid Use for Breast Cancer Screening in Older Women](https://doi.org/10.1016/j.amepre.2022.04.014). Ross RL, Rubio K, Rodriguez HP. 2022. *American journal of preventive medicine*. | Medicare, 439 684 žen 65–74 let v 1 236 praxích (observační): pokročilé IT funkce praxe (upozornění na prošlé vyšetření, objednávky) OR 1,19 (p = 0,04) pro mamografii; rutinní používání rozhodovacích pomůcek OR 0,95 (p = 0,21). | [PDF](papers/people/HIT_DECAID2022.pdf) |
| [17] | `[PROVIDER_CPG2023]` | [Characteristics and impact of interventions to support healthcare providers' compliance with guideline recommendations for breast cancer: a systematic literature review](https://doi.org/10.1186/s13012-023-01267-2). Ricci-Cabello I, Carvallo-Castañeda D, Vásquez-Mejía A et al. 2023. *Implementation science : IS*. | 35 studií, 24 intervencí na podporu dodržování doporučení v péči o karcinom prsu (nejčastěji počítačová podpora rozhodování); jistota důkazů podle GRADE většinou nízká až střední. Týká se celé péče, ne jen screeningu. | [PDF](papers/people/PROVIDER_CPG2023.pdf) |
| [11] | `[MMU_PRIMARY2026]` | [Implementing mobile mammography in primary care: a community-based Reach, Effectiveness, Adoption, Implementation, and Maintenance (RE-AIM) evaluation](https://doi.org/10.1093/tbm/ibag062). Ziegler AM, Harold P, Tumiel-Berhalter LM. 2026. *Translational behavioral medicine*. | Mobilní mamograf v 6 praxích primární péče (2013–2019), hodnocení RE-AIM: předvídatelný rozvrh a objednání termínu přímo v ordinaci vedly k vyšší dokončenosti a udržitelnosti než spoléhání na oslovování pacientek. | [PDF](papers/people/MMU_PRIMARY2026.pdf) |
| [20] | `[CHILE_LONGTERM2022]` | [Long-term Mammography Utilization after an Initial Randomized Intervention Period by all Underserved Chilean Women in the Clinics](https://doi.org/10.3390/cancers14153734). Puschel K, Rioseco A, Soto G et al. 2022. *Cancers*. | Chile, 10 let po RCT v klinice pro ženy s nízkým SES: pokrytí mamografií zůstalo vyšší než ve srovnávacích klinikách se středním SES (36,2 vs. 30,1 a 19,4 %); příklad hodnocení udržitelnosti (RE-AIM). | [PDF](papers/people/CHILE_LONGTERM2022.pdf) |
| [6] | `[BLACK_AFRICAN2026]` | [Interventions to Improve Breast Screening Uptake for Black African Women in High Income Countries: A Systematic Review](https://doi.org/10.1007/s40615-026-02999-9). Nwadinigwe U, Itua I, Keyworth C et al. 2026. *Journal of racial and ethnic health disparities*. | 12 studií z USA u černošských žen afrického původu: 11 účinných; nejslibnější je individuální podpora nebo navigace s technikou řešení problémů (behaviour change technique). | [PDF](papers/people/BLACK_AFRICAN2026.pdf) |

**Shrnutí CPSTF (Community Guide), mediány absolutního zvýšení mamografie proti běžné péči, převážně USA**
([4], [9], [14] Gemini). Pozor: v organizovaném programu, který už zve dopisem, budou přírůstky menší.

| Klíč | Zjištění | Zdroj |
|---|---|---|
| `[CPSTF_CHW]` | Komunitní zdravotní pracovníci: medián +12,7 p. b. (35 studií); při současném zvýšení poptávky i dostupnosti +18,5 p. b.; s tlumočením +30,2 p. b. (4 studie). | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-interventions-engaging-community-health-workers-breast-cancer.html) |
| `[CPSTF_STRUCT]` | Odstranění strukturálních bariér (mobilní mamograf, delší ordinační doba, objednání, doprava): medián +17,7 p. b. (IQI 11,5–30,5). | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-reducing-structural-barriers-clients-breast-cancer.html) |
| `[COMMUNITY_GUIDE]` | Připomínky klientkám: medián +14,0 p. b. (IQI 2,0–24,0) proti žádné intervenci, ale jen **+5,0 p. b. (IQI 1,6–6,7) navíc k jiným intervencím**. | [Community Guide](https://thecommunityguide.org/findings/cancer-screening-client-reminders-breast-cancer.html) |
| `[CPSTF_NAV]` | Pacientská navigace: medián +12,0 p. b. | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-patient-navigation-services-to-increase-breast-cancer-screening.html) |
| `[CPSTF_AF]` | Audit a zpětná vazba lékařům: medián +13,0 p. b. (IQI 5,5–21,8) pro screening prsu, čípku a kolorekta dohromady. | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-provider-assessment-and-feedback-breast-cancer.html) |
| `[CPSTF_PROVREM]` | Připomínky a recall systémy pro lékaře: mamografie medián kolem +10 p. b.; účinek s časem slábne. | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-provider-reminder-and-recall-systems-breast-cancer.html) |
| `[CPSTF_SMALLMEDIA]` | Malá média (letáky, brožury, videa): medián +7,0 p. b. (IQI 0,3–13,2). | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-small-media-targeting-clients-breast-cancer.html) |
| `[CPSTF_MASSMEDIA]` | Masová média: mamografie −2,4 p. b., neprůkazné; nedostatek důkazů. | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-mass-media-targeting-clients-breast-cancer.html) |
| `[CPSTF_PROVINC]` | Pobídky lékařům: medián +1,7 p. b. (IQI 0,1–3,6), nedostatek důkazů. | [Community Guide](https://www.thecommunityguide.org/findings/cancer-screening-provider-incentives-breast-cancer.html) |

<a id="cast-metodika"></a>

## Část II. Metodika: jak to měřit, modelovat a ověřit

Zdroje, jejichž hodnota pro nás je postup: vysvětlitelné modely, kauzální odhady a cílení, design a vyhodnocení experimentů, simulační modely. Studie, které metodou zjišťují něco o ženách (např. `[ML_SPAIN2021]`, `[ML_INTERSECT2024]`, `[PA_2025]`, odhady doby preklinické fáze `[MST_*]`), jsou v Části I. PDF jsou v [`papers/methods/`](papers/methods/).

### II.1 Predikce a vysvětlitelnost modelů

#### `[ML_TITB2011]` Predicting breast screening attendance using machine learning techniques

Baskaran V, Guergachi A, Bali RK et al. 2011. *IEEE transactions on information technology in biomedicine : a publication of the IEEE Engineering in Medicine and Biology Society*. · [odkaz](https://doi.org/10.1109/titb.2010.2103954) · PDF: [`papers/methods/ML_TITB2011.pdf`](papers/methods/ML_TITB2011.pdf) · stupeň **C**

- Hybridní neuronová síť na 13 letech dat: přesnost ~80 %, ale specificita jen 40–50 %.

| Klíč | Zdroj | Hlavní poznatek | PDF | Původ |
|---|---|---|---|---|
| `[EBM_GA2M2013]` | [odkaz](https://doi.org/10.1145/2487575.2487579) | GA²M: zobecněný aditivní model s párovými interakcemi, přesnost blízko black-box modelům při plné interpretovatelnosti (základ EBM). | – | brief [21] |
| `[INTERPRETML2019]` | [InterpretML: A Unified Framework for Machine Learning Interpretability](https://arxiv.org/abs/1909.09223). Harsha Nori, Samuel Jenkins, Paul Koch et al. 2019. *arXiv*. | Knihovna InterpretML s Explainable Boosting Machine: glass-box model, tvarové funkce lze vykreslit. | [PDF](papers/methods/INTERPRETML2019.pdf) | brief [22] |
| `[SHAP2017]` | [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874). Scott Lundberg, Su-In Lee. 2017. *arXiv*. | SHAP: jednotný rámec vysvětlení predikcí přes Shapleyho hodnoty. | [PDF](papers/methods/SHAP2017.pdf) | brief [23] |
| `[TREESHAP2020]` | [From Local Explanations to Global Understanding with Explainable AI for Trees](https://doi.org/10.1038/s42256-019-0138-9). Lundberg SM, Erion G, Chen H et al. 2020. *Nature machine intelligence*. | TreeSHAP: přesné SHAP a SHAP interakční hodnoty pro stromové modely v polynomiálním čase; od lokálních vysvětlení ke globálnímu porozumění. | [PDF](papers/methods/TREESHAP2020.pdf) | brief [24] |
| `[SAGE2020]` | [Understanding Global Feature Contributions With Additive Importance Measures](https://arxiv.org/abs/2004.00668). Ian Covert, Scott Lundberg, Su-In Lee. 2020. *arXiv*. | SAGE: Shapleyho rozklad ztrátové funkce; ukazuje, které proměnné přinášejí přesnost, ne jen na co model spoléhá. | [PDF](papers/methods/SAGE2020.pdf) | brief [25] |
| `[SHAP_DEPENDENT2021]` | [Explaining individual predictions when features are dependent: More accurate approximations to Shapley values](https://arxiv.org/abs/1903.10464). Kjersti Aas, Martin Jullum, Anders Løland. 2019. *arXiv*. | SHAP při závislých proměnných: intervenční SHAP opouští datovou varietu, podmíněný připisuje zástupným proměnným. | [PDF](papers/methods/SHAP_DEPENDENT2021.pdf) | brief [26] |
| `[SOBOL_SHAPLEY2014]` | [odkaz](https://doi.org/10.1137/130936233) | Vztah Sobolových indexů a Shapleyho hodnot (citlivost založená na rozptylu). | – | brief [27] |
| `[SHAPLEY_EFFECTS2016]` | [odkaz](https://doi.org/10.1137/15M1048070) | Shapleyho efekty pro globální citlivostní analýzu se závislými vstupy; výpočetně náročné. | – | brief [28] |
| `[TABPFN2025]` | [Accurate predictions on small data with a tabular foundation model](https://doi.org/10.1038/s41586-024-08328-6). Hollmann N, Müller S, Purucker L et al. 2025. *Nature*. | TabPFN: transformer předtrénovaný na syntetických datech, predikce na malých tabulkách jedním průchodem bez ladění. | [PDF](papers/methods/TABPFN2025.pdf) | brief [42] |
| `[TABPFN25_2025]` | [TabPFN-2.5: Advancing the State of the Art in Tabular Foundation Models](https://arxiv.org/abs/2511.08667). Léo Grinsztajn, Klemens Flöge, Oscar Key et al. 2025. *arXiv*. | TabPFN-2.5: do 50 000 řádků a 2 000 proměnných, lepší než laděné stromové modely na TabArena; váhy jen pro nekomerční výzkum. | [PDF](papers/methods/TABPFN25_2025.pdf) | brief [43] |

### II.2 Kauzální odhady, uplift a cílení

#### `[UPLIFT_COST]` Uplift Modeling for Multiple Treatments with Cost Optimization

Zhenyu Zhao, Totte Harinen. 2019. *arXiv*. · [odkaz](https://arxiv.org/abs/1908.05372) · PDF: [`papers/methods/UPLIFT_COST.pdf`](papers/methods/UPLIFT_COST.pdf) · stupeň **C**

- Uplift modely pro více intervencí s různými náklady (Uber), včetně produkčního nasazení.

#### `[HTE_CALIB]` Calibration Error for Heterogeneous Treatment Effects

Yizhe Xu, Steve Yadlowsky. 2022. *arXiv*. · [odkaz](https://arxiv.org/abs/2203.13364) · PDF: [`papers/methods/HTE_CALIB.pdf`](papers/methods/HTE_CALIB.pdf) · stupeň **C**

- Míra kalibrace odhadů heterogenních účinků (analog ECE), dvojitě robustní odhad.

| Klíč | Zdroj | Hlavní poznatek | PDF | Původ |
|---|---|---|---|---|
| `[UPLIFT_SURVEY]` | [odkaz](https://www.researchgate.net/publication/366788754) | Přehled uplift modelování a heterogenních účinků (T/S/X-learner, causal forest, Qini). | [PDF](papers/methods/UPLIFT_SURVEY.pdf) | seznam zdrojů |
| `[UPLIFT_POLICY]` | [odkaz](https://www.researchgate.net/publication/378498108) | Spojení upliftu a HTE pro cílení (Guse et al.). | – | seznam zdrojů |
| `[CAUSAL_FOREST2018]` | [Estimation and Inference of Heterogeneous Treatment Effects using Random Forests](https://doi.org/10.1080/01621459.2017.1319839). Stefan Wager, Susan Athey. 2015. *arXiv*. | Causal forest: odhad a inference heterogenních účinků léčby náhodnými lesy. | [PDF](papers/methods/CAUSAL_FOREST2018.pdf) | brief [39] |
| `[METALEARNERS2019]` | [Metalearners for estimating heterogeneous treatment effects using machine learning](https://doi.org/10.1073/pnas.1804597116). Künzel SR, Sekhon JS, Bickel PJ et al. 2019. *Proceedings of the National Academy of Sciences of the United States of America*. | Meta-learnery (S-, T-, X-learner) pro heterogenní účinky; X-learner je silný při nevyvážených skupinách. | [PDF](papers/methods/METALEARNERS2019.pdf) | brief [40] |

### II.3 Design a vyhodnocení experimentů a změn pravidel

#### `[TEMPO2023]` Increasing uptake of FIT colorectal screening: protocol for the TEMPO randomised controlled trial testing a suggested deadline and a planning tool

Robb KA, Kotzur M, Young B et al. 2023. *BMJ open*. · [odkaz](https://doi.org/10.1136/bmjopen-2022-066136) · PDF: [`papers/methods/TEMPO2023.pdf`](papers/methods/TEMPO2023.pdf) · stupeň **B**

- Protokol 2×4 faktoriálního RCT (40 tis. osob, FIT): navržený termín vrácení testu × plánovací nástroj.
- Vzor pro faktoriální design experimentu ve frameworku.

| Klíč | Zdroj | Hlavní poznatek | PDF | Původ |
|---|---|---|---|---|
| `[BAYES_TRIALS2006]` | [Bayesian clinical trials](https://doi.org/10.1038/nrd1927). Berry DA. 2006. *Nature reviews. Drug discovery*. | Berry: argumenty pro bayesovské klinické studie (průběžné učení, rozhodování). | – | brief [45] |
| `[ADAPTIVE_RAND2015]` | [Statistical controversies in clinical research: scientific and ethical problems with adaptive randomization in comparative clinical trials](https://doi.org/10.1093/annonc/mdv238). Thall P, Fox P, Wathen J. 2015. *Annals of oncology : official journal of the European Society for Medical Oncology*. | Kritika response-adaptivní randomizace: zkreslení a nižší efektivita; pro hodnocení raději pevná alokace s chráněnou kontrolou. | [PDF](papers/methods/ADAPTIVE_RAND2015.pdf) | brief [46] |
| `[ITS_GUIDELINE2022]` | [Changes in mammography screening in Ontario and Alberta following national guideline dissemination: an interrupted time series analysis](https://doi.org/10.12688/f1000research.55004.2). Fahim C, Wiebe N, Nisenbaum R et al. 2022. *F1000Res*. | Přerušená časová řada, Ontario a Alberta 2008–2014: po kanadském doporučení z 2011 klesla mamografie hlavně u žen 40–49 let. Vzor pro vyhodnocení změny pravidel bez randomizace (u nás zrušení žádanky 7/2026). | [PDF](papers/methods/ITS_GUIDELINE2022.pdf) | Gemini [23] |
| `[REAIM2013]` | [The RE-AIM framework: a systematic review of use over time](https://doi.org/10.2105/AJPH.2013.301299). Gaglio B, Shoup JA, Glasgow RE. 2013. *American journal of public health*. | Systematický přehled použití rámce RE-AIM (71 studií 1999–2010): dosah, účinek, přijetí, implementace a udržitelnost se vykazují nejednotně. | – | Gemini [10] |

### II.4 Simulační modely screeningu

#### `[SIM_MODELS2021]` Cancer screening simulation models: a state of the art review

Bespalov A, Barchuk A, Auvinen A et al. 2021. *BMC medical informatics and decision making*. · [odkaz](https://doi.org/10.1186/s12911-021-01713-5) · PDF: [`papers/methods/SIM_MODELS2021.pdf`](papers/methods/SIM_MODELS2021.pdf) · stupeň **C**

- Přehled 263 simulačních modelů screeningu: nejčastěji kohortové (41 %) a individuální Markovovy modely (34 %).
- Podklad pro volbu jednoduchého kohortového modelu ve frameworku. (V původní rešerši byl odkaz chybně u `[EUROSCREEN2012]`.)

| Klíč | Zdroj | Hlavní poznatek | PDF | Původ |
|---|---|---|---|---|
| `[CISNET]` | [odkaz](https://cisnet.cancer.gov/resources/model-registry/breast-models/MISCAN.html) | Modely CISNET/MISCAN-Fadia nejsou open source; framework staví vlastní kohortový model. | – | seznam zdrojů |

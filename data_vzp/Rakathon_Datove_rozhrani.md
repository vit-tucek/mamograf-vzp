**RAKATHON 2026**

_Datové rozhraní k vybíraným atributům a labelům — verze k 29. 9. 2026_

# **1\. Účel dokumentu**

Tento dokument popisuje datové rozhraní datasetu, který vychází z Přílohy B zadání výzvy Rakathon 2026. Dokument slouží jako referenční popis pro každého, kdo s výstupním datasetem dále pracuje.

# **2\. Granularita datasetu a vstupní podmínky**

Jeden řádek datasetu = jedno adresné pozvání jedné klientky na mamografický screening k danému datu (T0). Jedna klientka (RC) může mít v datasetu více řádků (max 5), pokud byla v různých obdobích pozvána opakovaně (odpovídá definici z Přílohy B: "Jeden řádek datasetu"). Jako zdroj těchto sloupců slouží data z aplikace Adresně zvaní. Vybírají se pozvání, která se týkají pouze mamografického screeningu tedy dopisy (3,4,7,8) za období 2020 – 2024, jedná se **cca 1 504 546** záznamů. Tato vstupní kohorta je pak filtrována, tak že jsou vyřazeny pojištěnci, kteří nebyli v období **01.01.2015 -31.12.2025** permanentně pojištění u VZP, počet se sníží o 159 535 záznamů a pracuje se tedy s 1 345 011 záznamy. Byly smazány potencionálně nebezpečné kombinace dat, což jsou řádky, kde invitation_date, age_band, vzp_territorial_area, person_id vrátí pouze 1 řádek (455 řádků). Finální počet záznamů je tedy **1 344 556** záznamů v datasetu. z toho je **508 527** unikátních rodných čísel.

|     | Sloupce, které se předávají   |
| --- | ----------------------------- |
|     | Sloupce, které se nepředávají |

# **3\. Klíčové a identifikační sloupce**

| **Sloupec**                | **Popis**                                          | **Referenční čas** | **Poznámka**                                                                         |
| -------------------------- | -------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------ |
| INVITATION_ID              | Náhodné/technické číslo pozvánky                   |                    |                                                                                      |
| RC                         | Rodné číslo / identifikátor klientky               | —                  | Odpovídá person_id z Přílohy B; nutno nahradit náhodným ID                           |
| PERSON_ID                  | Náhodně vygenerované 15 -místné číslo              |                    | Nelze odvodit zpět RČ                                                                |
| INVITATION_DATE            | Datum odeslání adresné pozvánky na screening (T0)  | T0                 | Referenční čas pro všechny prediktory i labely; odpovídá invitation_date z Přílohy B |
| PRIOR_INVITATION_COUNT     | Počet pozvánek                                     |                    |                                                                                      |
| INVITATION_SEQUENCE        | Pořadové číslo pozvánky                            |                    |                                                                                      |
| MONTHS_LAST_INVITATION     | Počet měsíců od poslední pozvánky                  |                    |                                                                                      |
| HEALTHCARE_CONTACT_12M_CNT | Počet kontaktů se zdravotnictvím za (T0-12 měsíců) |                    | Počítá se, jako součet počtu unikátních Ičz v jednom dni                             |
| FIRST_INVITATION           | První pozvánka - A/N                               |                    |                                                                                      |

# **4\. Demografické a regionální atributy**

| **Sloupec**          | **Popis**                                                              | **Zdroj**                                                      | **Poznámka**                                                                                            |
| -------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| AGE                  | Věk klientky ke dni pozvánky (T0),                                     |                                                                |                                                                                                         |
| AGE_BAND             | Věkové pásmo odvozené z AGE: < 25 let, potom po 5 letech a nakonec 75+ | odvozeno z AGE                                                 | Pozvánky se posílají v průběhu měsíce, kdy má pojištenec narozeniny                                     |
| VZP_TERRITORIAL_AREA | Přibližná lokalita bydliště – název územního pracoviště VZP            | D_UZEMNI_PRACOVISTE (přes D_POJISTENEC.POJ_UP_KOD), jen platná | Technická aproximace atributu „region" z Přílohy B; NENÍ administrativní okres ČR – viz upozornění níže |

# **5\. Délka pojištění**

| **Sloupec**              | **Popis**                                                               | **Umístění**                          | **Poznámka**                                                             |
| ------------------------ | ----------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------ |
| INSURANCE_DURATION_YEARS | Délka pojištění u VZP k T0 v celých letech vzhledem k T0                | RAK_POZVANKY.INSURANCE_DURATION_YEARS | Příloha B: insurance_duration.                                           |
| INSURANCE_DURATION_BAND  | Pásmo délky pojištění u VZP: &lt;2, 2-5, &gt;5 let                      | odvozeno z INSURANCE_DURATION_YEARS   | Příloha B: insurance_duration, hranice pásem přímo dle zadání            |
| INSURANCE_DURATION_DAYS  | Pomocný/kontrolní sloupec – totéž co INSURANCE_DURATION_YEARS, ve dnech |                                       | Není přímo v Příloze B – bonus pro kontrolu výpočtu a jemnější rozlišení |

# **6\. Registrace u lékaře (praktik / gynekolog)**

| **Sloupec**            | **Popis**                                                                           | **Zdroj**                         | **Poznámka**                                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| GP_REGISTERED          | A/N – zda měla klientka k T0 platnou registraci u praktického lékaře (ODB 001, 002) |                                   |                                                                                                              |
| REG_DURATION           | Kolik let trvá aktuální registrace u praktika k T0                                  |                                   |                                                                                                              |
| GP_REG_DURATION_BAND   | Pásmo délky registrace u praktika: &lt;2, 2-5, &gt;5 let                            | odvozeno z GP_REG_DURATION_YEARS  | Příloha B: registration_duration ('Agregovaně'); hranice pásem převzaty z insurance_duration pro konzistenci |
| GYN_REGISTERED_FLAG    | A/N – zda měla klientka k T0 platnou registraci u gynekologa (ODB 603, 604)         |                                   |                                                                                                              |
| GYN_REG_DURATION_YEARS | Kolik let trvá aktuální registrace u gynekologa k T0                                |                                   |                                                                                                              |
| GYN_REG_DURATION_BAND  | Pásmo délky registrace u gynekologa: &lt;2, 2-5, &gt;5 let                          | odvozeno z GYN_REG_DURATION_YEARS | Stejná logika jako GP_REG_DURATION_BAND                                                                      |

# **7\. Prediktory (B3 – Historie screeningu, B4 – Preventivní chování)**

| **Sloupec**                | **Popis**                                                             | **Okno / Čas**           | **Kódy ZP (TZP_KOD)**                                                                 | **Poznámka**                                                                                                 |
| -------------------------- | --------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| PRIOR_SCREEN_COUNT_5Y      | Počet kvalifikujících mamografických screeningů za 5 let              | Před T0 (–60 měsí, T0)   | 89178,89223,89225,89314,89510,89814                                                   | Klíčový behaviorální ukazatel (Příloha B: prior_screen_count_5y)                                             |
| MONTHS_SINCE_LAST_SCREEN   | Počet měsíců od posledního mamografického screeningu k T0             | Před T0 (-60 měsíců)     | 89178,89223,89225,89314,89510,89814                                                   | NULL, pokud screening nikdy neproběhl – viz NEVER_SCREENED_BEFORE_FLAG (Příloha B: months_since_last_screen) |
| NEVER_SCREENED_BEFORE_FLAG | A/N – zda klientka nikdy před T0 neabsolvovala mamografický screening | Před T0 (-60 měsíců)     | 89178,89223,89225,89314,89510,89814                                                   | Doplňkový atribut k ošetření chybějící hodnoty MONTHS_SINCE_LAST_SCREEN                                      |
| GP_PREVENTION_24M_CNT      | Počet preventivních prohlídek u praktického lékaře                    | Před T0 (–24 měsíců, T0) | 01021, 01022                                                                          | Příloha B: gp_prevention_24m                                                                                 |
| GYN_PREVENTION_24M_CNT     | Počet preventivních prohlídek u gynekologa                            | Před T0 (–24 měsíců, T0) | 63050,63021                                                                           | Příloha B: gyn_prevention_24m                                                                                |
| OTHER_SCREENING_36M_CNT    | Počet účastí na jiném screeningovém programu                          | Před T0 (–36 měsíců, T0) | 15105,15107,15118,15119,15120,15121,95198,<br><br>95199,95201,95202,95203,15101,15103 | Příloha B: other_screening_36m                                                                               |
| DENTAL_PREVENTION_24M_CNT  | Počet preventivních stomatologických prohlídek                        | Před T0 (–24 měsíců, T0) | 00946,<br><br>00901                                                                   |                                                                                                              |

# **8\. Labely (cílové proměnné)**

| **Sloupec**        | **Popis**                                         | **Okno / Čas**       | **Kódy ZP (TZP_KOD)**               | **Poznámka** |
| ------------------ | ------------------------------------------------- | -------------------- | ----------------------------------- | ------------ |
| SCREENING_3M_FLAG  | A/N – screeningový výkon vykázán do 90 dnů od T0  | Po T0 (T0, +90 dní)  | 89178,89223,89225,89314,89510,89814 |              |
| SCREENING_6M_FLAG  | A/N – screeningový výkon vykázán do 180 dnů od T0 | Po T0 (T0, +180 dní) | 89178,89223,89225,89314,89510,89814 |              |
| SCREENING_12M_FLAG | A/N – screeningový výkon vykázán do 365 dnů od T0 | Po T0 (T0, +365 dní) | 89178,89223,89225,89314,89510,89814 |              |

# **9\. Vazba na Přílohu B — kontext**

Pro úplnost: Příloha B definuje širší sadu potenciálních atributů (regionální dostupnost, socioekonomický kontext, kanál komunikace apod.), z nichž tento dataset pokrývá sekce B3 (Historie screeningu), B4 (Preventivní chování), zjednodušenou aproximaci demografie/regionu, registraci u lékaře (registration_duration) a definované labely. Ostatní sekce Přílohy B (dostupnost péče v regionu, digitální kanál, kontext praktika) zatím nejsou do výběru zahrnuty a je možné je doplnit obdobným postupem v navazujících iteracích.
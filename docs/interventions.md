# Interventions to increase mammography screening: ranked by expected uplift

Every way we know of to raise screening attendance, ordered from the largest to the smallest
**expected uplift for VZP**. Each entry says why it should work, what the literature measured and
how to test it robustly in the field. Citation keys like `[NHS_TIMED2026]` point to
[`PAPERS.md`](../PAPERS.md); the PDFs are in [`papers/people/`](../papers/people/) (studies of women, interventions and costs) and
[`papers/methods/`](../papers/methods/) (statistics, ML, trial design).

**What "expected uplift" means here.** The absolute increase in the share of *targeted* women with
a screening mammogram (code 89223 or 89178) within 90–180 days, **on top of current Czech
practice**. VZP already sends invitation letters, and since 1 July 2026 women may go without a
referral. Many published effects are measured against no invitation at all, often in US settings
without an organised programme, so the expected range for VZP is usually well below the
literature figure. The ranking uses the midpoint of that range. It is a judgement from the evidence
below, not a measurement, and the field tests exist to replace it with VZP's own numbers.

Uplift also depends on the group: it is largest for women who are undecided (baseline around 50 %)
and smallest for women who always come or never come [`[NHS_POSTAL2016]`](../PAPERS.md),
[`[DE_PHONE2023]`](../PAPERS.md). The ranking ignores cost; cost per additional woman screened is
given where known.

**Used by the framework.** Fourteen of these interventions are in the catalogue of the `mamoframe`
framework (`config/interventions.yaml` in the original repository `mamograf-data-exploration`), with
their range from this table (`expected_uplift_pp`). The prior on the log-odds of attendance is the range midpoint at a reference
baseline of 30 %, with the range read as about ±1 standard deviation. The optimiser then weighs
these priors against cost, reach and centre capacity, so its order differs from this ranking.

## Summary

| # | Intervention | Expected uplift for VZP (pp) | Strongest evidence | Cost | Best for |
|---|---|---|---|---|---|
| 1 | Pre-booked appointment instead of an open invitation | +10 to +19 | RCT + quasi-RCT, mammography | low per woman, needs held slots | lapsed, first-time invitees |
| 2 | Multicomponent package (reminder + navigation + barrier removal) | +8 to +18 | meta-analyses, CPSTF | high | hard-to-reach segments |
| 3 | Patient navigation by phone (book, solve the woman's barrier) | +5 to +12 | CPSTF, RCTs | high | never-screened, long-lapsed |
| 4 | Remove structural barriers locally (mobile unit, transport, evening slots) | +5 to +15 locally, ~0 elsewhere | CPSTF, cohort, repo | high, local | remote districts (Jeseník, Bruntál) |
| 5 | Language- and culture-tailored outreach for migrant women | +3 to +8 in the group | RCTs, meta-analyses | low | women with foreign language of correspondence |
| 6 | Overdue lists and audit & feedback to gynaecologists and GPs | +2 to +6 | CPSTF, reviews, repo | low | women with a registering doctor |
| 7 | Telephone reminder (short call, no full navigation) | +2 to +6 | Cochrane, RCT | medium | lapsed |
| 8 | SMS reminder with a booking link | +2 to +5 | RCTs | very low | anyone with a mobile number |
| 9 | Point-of-care prompt for any doctor (EZ karta, practice software) | +1 to +5 | CPSTF, observational | medium (IT) | women in contact with care |
| 10 | Better letter: content, problem-solving, "no referral needed" | +1 to +4 | RCTs, Cochrane | very low | all invitees |
| 11 | New fixed screening centre | +1 to +2 in the district | repo | very high | districts without a centre |
| 12 | Bundled prevention visit (several screenings in one go) | −2 to +3 | Cochrane (mixed) | medium | women due for several screenings |
| 13 | Incentives for doctors (bonus, pay per detected cancer) | 0 to +2 | CPSTF, reviews | medium | – |
| 14 | AI- or LLM-tailored messages | 0 to +2 | RCTs on intent only | low | as message variants in 8 or 10 |
| 15 | App push (Moje VZP) alone | 0 to +1 | RCT | very low | digital users, always with SMS |
| 16 | Financial incentives for women (vouchers, lotteries, bonus) | 0 to +1 | RCTs, reviews | medium | – |
| 17 | Mass media campaign | ~0 | CPSTF | high | – |
| 18 | Home visits | ~0 | Cochrane | high | – |
| 19 | Personal cancer-risk messages from claims data | ≤ 0 | RCTs, cohort | low | none (send real high-risk women to a doctor) |
| 20 | Decision aids | ≤ 0 for uptake | observational, RCT | low | informed choice, not uptake |

Two further levers are not interventions but **choices of whom to target**; they multiply the
effect of everything above (see *Targeting* at the end).

---

## 1. Pre-booked appointment instead of an open invitation

**Why it should work.** It changes the default. With an open invitation the woman has to decide,
find a centre, call and book; each step loses women. A booked slot turns screening into an
appointment she only has to keep or move. It removes the planning step that intention-to-act
research identifies as the main gap between wanting to go and going.

**Evidence on the effect size.**
- NHS service evaluation, 17,965 women, quasi-randomised: attendance 49.1 % with open/open
  invitations vs 67.9 % with timed/timed (+18.8 pp); among the most deprived 41.1 % → 63.3 %
  [`[NHS_TIMED2026]`](../PAPERS.md).
- RCT of a second timed appointment for non-attenders (n ≈ 26,000): about +10 pp over a letter
  with a phone number [`[NHS_2ND_TIMED2017]`](../PAPERS.md).
- London natural experiment during COVID recovery: 60.6 % vs 53.1 % (+7.5 pp)
  [`[LONDON_OPEN2022]`](../PAPERS.md).
- Fixed appointments are among the few low-cost interventions supported across reviews
  [`[MANDRIK2021]`](../PAPERS.md).
- Czech caveat: centres run their own booking, so this needs partner centres that hold slots.
  VZP plans to link centre booking with Moje VZP [`[VZP_2026]`](../PAPERS.md).

**How to test it.** Individually randomised trial within the lapsed and first-invitation segments,
at partner centres that agree to hold slots. Arms: current letter vs booked slot + SMS vs booked
slot + SMS + call to non-responders at week 6. Primary outcome: screening claim within 90 days
(ITT), secondary at 180 days. Also measure no-shows, advance cancellations and slot use. Stop rule:
waiting time at partner centres (third next available slot) above an agreed limit.

## 2. Multicomponent package for hard-to-reach segments

**Why it should work.** Non-attendance has several causes at once. A reminder fixes forgetting,
but not transport or fear; navigation fixes logistics, but only if the woman is reached. Combining
demand (reminder, information) with access (booking, transport) closes several gaps at the same
time.

**Evidence on the effect size.**
- Community health worker programmes that raised both demand and access: median +18.5 pp, more
  than single-focus ones [`[CPSTF_CHW]`](../PAPERS.md).
- Low-income women, 21 RCTs: +8.9 pp overall, combined interventions most effective
  [`[LOWINCOME2013]`](../PAPERS.md).
- Cochrane: combinations of effective strategies "can have an important effect"
  [`[COCHRANE_INVITE2001]`](../PAPERS.md); 44 RCTs in underserved groups: OR 1.81
  [`[META_UNDERSERVED2025]`](../PAPERS.md).

**How to test it.** A factorial trial (for example reminder × navigation, 2 × 2) inside the
never-screened and long-lapsed segments, so the package effect and each component's share are
estimated together. ITT on claims at 90 and 180 days, cost per additional woman screened.

## 3. Patient navigation by phone

**Why it should work.** A person calls, finds out what stops this woman (no referral, can't get
there, fear after a past recall, didn't know she is entitled), and fixes it on the spot: books the
slot, arranges transport, explains. It targets the barrier instead of repeating the message.

**Evidence on the effect size.**
- Patient navigation: median +12.0 pp [`[CPSTF_NAV]`](../PAPERS.md); community health workers:
  +12.7 pp, +30.2 pp when they also translate [`[CPSTF_CHW]`](../PAPERS.md).
- German RCT of barrier-specific phone counselling: 45.9 % vs 28.6 %, but among women reached,
  not ITT. It helped with missed letters and bad dates, not with women who felt healthy or were
  screened elsewhere [`[DE_PHONE2023]`](../PAPERS.md).
- Singapore RCT (9,000 overdue women): a scheduling hotline gave 13.8 % vs 11.2 %, not significant
  after correction; about 212 USD per extra mammogram [`[SG_OVERDUE2026]`](../PAPERS.md).
- Cost: 154–740 USD per additional woman screened; 3,852–39,159 USD per QALY
  [`[NAVIGATION_ECON2024]`](../PAPERS.md).
- Most evidence is American and in underserved groups; in a Czech ITT design, where many women
  cannot be reached by phone, expect the lower end.

**How to test it.** Individually randomised within the never-screened-disconnected, long-lapsed
and access-constrained segments; target by predicted uplift, not by risk. Report ITT and,
separately, the effect among women reached (complier average causal effect), plus the reach rate
and cost per extra screen.

## 4. Remove structural barriers locally

**Why it should work.** Where travel, opening hours or booking are the real obstacle, no message
helps. A mobile unit, transport, evening or weekend slots or easy online booking remove the
obstacle itself.

**Evidence on the effect size.**
- Reducing structural barriers: median +17.7 pp (IQI 11.5–30.5) [`[CPSTF_STRUCT]`](../PAPERS.md).
- Quebec: participation 6.3 pp lower at 50–75 km and 9.8 pp lower beyond 75 km; the drop starts
  far out, so distance matters only in the tail [`[QC_DISTANCE2013]`](../PAPERS.md). Danish
  registry: distance over 20 km and no car predict non-attendance [`[DK_2012]`](../PAPERS.md).
- A mobile unit worked best with predictable schedules and pre-booking in the practice
  [`[MMU_PRIMARY2026]`](../PAPERS.md).
- **Our district data say the effect will be local.** Centres within reach (2SFCA) are unrelated to
  coverage, but districts with their own centre have about +1.3 pp and districts where more women
  travel out have lower coverage (r = −0.30). Jeseník (51 %) and Bruntál (44 %) still send about
  half of their women elsewhere (`notebooks/mamograf_rozsireni.ipynb`, kap. 1). Outside such areas
  expect little.
- **Access matters for women 75+, not for 45–74.** Distance to the nearest centre is unrelated to
  coverage overall (r = −0.18) and at 45–74, but strongly related at 80+ (r ≈ −0.5); the age
  interaction survives correction for 47 tested indicators and replicates across two periods
  (`notebooks/mamograf_podskupiny.ipynb`). So target transport and mobile units at older women in
  remote areas.
- **Waiting times go with coverage, cause unclear.** Districts whose women face longer booking waits
  (self-reported by centres on mamo.cz, 2013–2019, weighted by where each district's women go) have
  lower coverage (r ≈ −0.35; about −1.1 pp per +8 days after the M3 model). But when a district's wait
  gets longer, its coverage does not fall (`notebooks/mamograf_rozsireni.ipynb`, kap. 1.2). The link
  more likely reflects lasting district traits (chronic capacity shortage, organisation of care,
  deprivation) than an effect of waiting itself. Shortening waits is therefore not a proven lever, but
  waiting time stays a guardrail for every demand-raising intervention.

**How to test it.** Place-based, so randomise places, not women. Pre-register the interaction
intervention × age 75+ × distance as the primary subgroup hypothesis: a stepped-wedge rollout of mobile
unit visits or transport across municipalities far from a centre, or difference-in-differences
against matched districts. Evening slots: cluster-randomise centres to offer them and mention them
in the invitation. Outcome: screening rate among resident women, from claims.

## 5. Language- and culture-tailored outreach for migrant women

**Why it should work.** Women who do not read Czech well may not understand the letter, the
entitlement or how to book. Messages in their language, ideally from someone from their community,
remove that barrier.

**Evidence on the effect size.**
- Australian in-language SMS to overdue women: bookings 12.7 % vs 8.2 % with English SMS, about
  1,595 AUD per QALY [`[SMS_CALD2025]`](../PAPERS.md).
- Community health workers with translation: +30.2 pp (4 studies) [`[CPSTF_CHW]`](../PAPERS.md);
  problem-solving navigation most promising for Black African women in high-income countries
  [`[BLACK_AFRICAN2026]`](../PAPERS.md); immigrant women and cervical screening
  [`[CERV_IMMIGRANT2023]`](../PAPERS.md).
- Migrant status is one of the strongest predictors of non-attendance (OR 2.0)
  [`[DK_2024]`](../PAPERS.md). In Prague 24 % of women are foreign nationals (repo).

**How to test it.** Randomise the language version (Czech vs Czech + Ukrainian or Vietnamese) among
women whose correspondence language or insurance history suggests it. Use such markers only to add
support, never to withhold it. ITT on claims.

## 6. Overdue lists and audit & feedback to gynaecologists and GPs

**Why it should work.** In Czechia the gynaecologist is the main route to mammography. Our district
data show the strongest link with preventive gynaecological visits (r = 0.46), and within districts
over time 1 % more gynaecological prevention goes with about 0.4 % more mammograms
(`notebooks/mamograf_analyza.ipynb`). What the doctor does matters more than how many doctors there
are (density r = 0.05). A list of the doctor's own overdue women, with a fair comparison to similar
practices, prompts action where the referral normally happens.

**Evidence on the effect size.**
- Audit and feedback to providers: median +13.0 pp across breast, cervical and colorectal
  screening [`[CPSTF_AF]`](../PAPERS.md); effective for all three cancers
  [`[IMPL_SCREEN2011]`](../PAPERS.md).
- After adjusting for patients, 41 % of variation between providers sits with individual doctors
  [`[US_PROVIDER2018]`](../PAPERS.md).
- But a letter signed by the woman's own clinician did not help in the Penn trial (11.4 % vs
  12.5 %) [`[PENN_OUTREACH2024]`](../PAPERS.md), while a GP endorsement letter raised colorectal
  screening by 5.8 pp [`[GP_ENDORSE2011]`](../PAPERS.md). The doctor's action counts, not the
  signature.
- VZP already pays a bonus when at least 35 % of a gynaecologist's registered women 45+ are
  screened, so practice-level rates exist inside VZP.

**How to test it.** Cluster-randomised by practice, because the intervention acts through the
doctor; inflate the sample by the design effect 1 + (m − 1) × ICC. Alternative: stepped-wedge by
kraj. Outcome: share of the practice's registered women 45+ screened within 6 months. Adjust the
comparison for area deprivation and practice age mix, shrink small practices (empirical Bayes) and
keep the rates internal; no public league tables.

## 7. Telephone reminder

**Why it should work.** A call is harder to ignore than a letter and lets the woman ask a question
or book at once. Without full navigation it is cheaper, but it fixes only simple barriers.

**Evidence on the effect size.**
- Cochrane: phone call OR 1.94, letter + phone call OR 2.53, both against no intervention
  [`[COCHRANE_INVITE2001]`](../PAPERS.md).
- Against an existing letter the gain is smaller: the Singapore scheduling hotline gave +2.6 pp,
  not significant [`[SG_OVERDUE2026]`](../PAPERS.md).

**How to test it.** An arm in the trial for item 1 or 3 (call to non-responders at week 6).
Report ITT and the reach rate.

## 8. SMS reminder with a booking link

**Why it should work.** Cheap and immediate; it reminds the woman when she can act and, with a
link, shortens the way to booking. Effective for women who already intend to go.

**Evidence on the effect size.**
- SMS 48 hours before a booked appointment: 59.1 % → 64.4 % ITT, although only 41 % had a number;
  advance cancellations about tripled [`[NHS_SMS2015]`](../PAPERS.md).
- Two Penn RCTs (24,632 women): +2.1 and +2.5 pp at 3 months [`[PENN_OUTREACH2024]`](../PAPERS.md);
  text reminders for overdue colorectal FIT: 21.2 % vs 14.6 % [`[CRC_BEHAV2025]`](../PAPERS.md).
- Client reminders add a median +5.0 pp on top of other interventions [`[COMMUNITY_GUIDE]`](../PAPERS.md).

**How to test it.** Individually randomised, large and cheap; combine it factorially with message
content (item 10) and app push (item 15). The ceiling is the share of women with a mobile number
on file, so record reachability.

## 9. Point-of-care prompt for any doctor

**Why it should work.** Most women who skip screening still see a doctor for something else. If any
doctor, or any imaging department, sees "overdue for screening" when the woman comes in, the
reminder comes from a trusted person at a moment when she is already in care (the Carebot idea in
the team strategy document).

**Evidence on the effect size.**
- Provider reminder and recall systems: mammography about +10 pp, fading over time
  [`[CPSTF_PROVREM]`](../PAPERS.md).
- Practices with advanced IT functions (overdue alerts, order sets): OR 1.19 for mammography,
  observational [`[HIT_DECAID2022]`](../PAPERS.md).
- Czech caveat: the EZ karta shows the entitlement to the woman but does not alert anyone; the
  expected effect depends on how much IT VZP and practice software vendors can change.

**How to test it.** Stepped-wedge rollout by practice or by software vendor; or, where the software
allows, randomise per patient whether the flag is shown. Outcome: screening within 90 days after a
contact with care.

## 10. Better letter: content and the "no referral needed" message

**Why it should work.** Many women do not know they can go without a referral since July 2026, do
not know where to go, or fear the result. A letter that answers these points (where, how to book,
that no referral is needed, what happens after) removes misinformation at almost no cost.

**Evidence on the effect size.**
- Postal reminder a few days before the appointment: +4.0 pp at 30 days, +2.7 pp at 180 days; no
  lasting effect among older previous non-attenders [`[NHS_POSTAL2016]`](../PAPERS.md).
- Small media: median +7.0 pp [`[CPSTF_SMALLMEDIA]`](../PAPERS.md); mailed educational material
  OR 2.81 against no intervention [`[COCHRANE_INVITE2001]`](../PAPERS.md).
- Removing the order step raised attendance from 12.7 % to 15.4 % in Penn
  [`[PENN_OUTREACH2024]`](../PAPERS.md). VZP expects +5–8 pp from the July 2026 rule itself
  [`[VZP_2026]`](../PAPERS.md), but that estimate has no control group.
- Czech personalised invitations since 2014: 22.3 % attended after a first invitation, with less
  effect after repeated letters [`[CZ_INVITE2019]`](../PAPERS.md); VZP's monthly screening volume rose
  only about 5 % before vs after, with no control group (research brief, ref. 5).

**How to test it.** Randomised letter variants inside VZP's existing monthly mailing (A/B or
factorial: no-referral message yes/no × problem-solving insert yes/no). For the policy change
itself, an interrupted time series [`[ITS_GUIDELINE2022]`](../PAPERS.md) or a
difference-in-differences comparing women just under and just over 45, or VZP with other insurers.

## 11. New fixed screening centre

**Why it should work.** A centre in the district is visible and "ours"; women hear about it and
need not travel.

**Evidence on the effect size.**
- Districts with their own centre have about +1.3 pp higher coverage (repo, cross-sectional). In
  Teplice the 2–3 pp gap to the rest of the kraj closed after its first centre opened in 2016
  (+2.2 pp, placebo p ≈ 0.09, one case) (`notebooks/mamograf_rozsireni.ipynb`, kap. 3).
- Centres within 20–45 km are unrelated to coverage, so the gain comes from presence in the
  district, not from capacity.

**How to test it.** Openings cannot be randomised. Use synthetic control or difference-in-differences
around each opening, with VZP's monthly claims by municipality, as in the Teplice case study.

## 12. Bundled prevention visit

**Why it should work.** Women who use one preventive service tend to use the others (cervical and
breast screening behaviour are strongly linked [`[DK_CERV_BREAST]`](../PAPERS.md)). One visit for
several screenings saves time and uses the same moment of motivation.

**Evidence on the effect size.** Mixed. Inviting women to several examinations at once with
educational material went the wrong way in the Cochrane review (OR 0.62, not significant)
[`[COCHRANE_INVITE2001]`](../PAPERS.md); complex messages may overload. No trial of a true
one-stop visit in a European programme was found.

**How to test it.** A pilot RCT among women due for both cervical and breast screening: offer a
same-day slot vs separate invitations. Outcome: completion of each screening within 90 days.

## 13. Incentives for doctors

**Why it should work.** Paying for the outcome should make doctors care about it.

**Evidence on the effect size.** Provider incentives: median +1.7 pp (IQI 0.1–3.6), insufficient
evidence [`[CPSTF_PROVINC]`](../PAPERS.md), [`[IMPL_SCREEN2011]`](../PAPERS.md). VZP's bonus already
exists. Paying per detected cancer, an idea from the team call, rewards finding cancers rather
than screening the right women and invites overdiagnosis.

**How to test it.** If VZP changes the bonus: cluster-randomise practices to the new bonus, or an
interrupted time series around the change.

## 14. AI- or LLM-tailored messages

**Why it should work.** Messages written for a segment's barriers and language might persuade
better than one generic text.

**Evidence on the effect size.** So far only intention, not behaviour: an LLM chatbot raised HPV
vaccination intent but not more than standard materials, and the effect faded within 45 days
[`[LLM_HPV2025]`](../PAPERS.md); AI messages raised colorectal screening intent more than expert
materials, with no data on actual screening [`[LLM_CRC2025]`](../PAPERS.md).

**How to test it.** Only as message variants inside the SMS or letter trials (items 8, 10), with
the effect prior centred on zero and outcomes from claims, not from intent surveys.

## 15. App push (Moje VZP) alone

**Why it should work.** Free and immediate for women who use the app.

**Evidence on the effect size.** In the Singapore trial only 4.1 % of pushes were clicked
[`[SG_OVERDUE2026]`](../PAPERS.md). VZP reports about 700,000 app users, with unknown activity
(team call).

**How to test it.** A cheap arm in the SMS factorial (push vs SMS vs both), limited to app users.

## 16. Financial incentives for women

**Why it should work.** A reward should tip women who are almost decided.

**Evidence on the effect size.** Small cash incentives and lotteries had no significant effect
(4,427 women) [`[US_INCENTIVE2015]`](../PAPERS.md); a lottery cost 3,209 USD per extra mammogram
[`[SG_OVERDUE2026]`](../PAPERS.md); client incentives lack evidence [`[IMPL_SCREEN2011]`](../PAPERS.md).

**How to test it.** The cheap version is free: mention VZP's existing 1,000 CZK prevention bonus
in the reminder or not (two-arm A/B). Do not build vouchers or gifts before that result.

## 17. Mass media campaign

**Why it should work.** Raises awareness and social norms at scale.

**Evidence on the effect size.** Mammography −2.4 pp, not significant; insufficient evidence
[`[CPSTF_MASSMEDIA]`](../PAPERS.md), [`[IMPL_SCREEN2011]`](../PAPERS.md).

**How to test it.** Only geo-randomised: run the campaign in randomly chosen regional media markets
and compare claims with the others (difference-in-differences).

## 18. Home visits

**Why it should work.** Personal contact at home reaches women who do not read letters.

**Evidence on the effect size.** In high-income settings with registries, no effect over mail or
phone (OR 1.06) [`[COCHRANE_INVITE2001]`](../PAPERS.md); they work mainly where no registry or
invitation system exists. Not recommended for VZP.

**How to test it.** Not worth a trial in Czechia.

## 19. Personal cancer-risk messages from claims data

**Why it should work.** Telling a woman her risk is high should motivate her.

**Evidence on the effect size.**
- With real risk data, risk feedback raises attendance (Cochrane OR 1.5)
  [`[COCHRANE_RISK2003]`](../PAPERS.md), and high-risk feedback raised next-round return to 89.2 %
  vs 78.8 % [`[PROCAS2022]`](../PAPERS.md).
- But being told the risk is low slightly lowered attendance [`[PROCAS2022]`](../PAPERS.md),
  personalised risk messages did not raise colorectal screening [`[RISKMSG_CRC2025]`](../PAPERS.md),
  and claims data cannot support a real risk score (no genes, family history or breast density).
- Use risk differently: route women with high-risk markers (past biopsy, high-risk screening code
  89178) to a doctor for proper assessment, and weight targeting by age-specific incidence.

**How to test it.** Not as a message. The referral route for high-risk markers can be tested as a
practice-level arm (item 6) with clinical outcomes.

## 20. Decision aids

**Why it should work.** They do not aim to raise uptake; they support an informed choice about
benefits and harms (false positives, overdiagnosis).

**Evidence on the effect size.** Practice use of decision aids was not associated with mammography
(OR 0.95) [`[HIT_DECAID2022]`](../PAPERS.md); a French decision-aid trial (DECIDEO) lowered
attendance (research brief, ref. 10).

**How to test it.** Measure informed choice and attendance together; agree with VZP in advance
that the goal is informed uptake, not uptake at any price.

---

## Targeting: whom to address first

These choices are not interventions, but they decide how much any intervention can achieve.

- **Newly eligible women (45–46).** A first invitation is the weakest moment (OR 0.22 for attending
  compared with previous attenders) [`[MOTTRAM2021]`](../PAPERS.md), and women who skip their first
  invitation keep attending less later [`[SE_FIRST2025]`](../PAPERS.md). Apply items 1, 8 and 10 here
  first.
- **Uplift, not risk.** The women least likely to come are often the least persuadable. Allocate
  interventions by predicted uplift × age-specific incidence, net of cost, keep a random holdout so
  the targeting itself stays testable (research brief).
- **Women 75+ far from a centre.** The only subgroup where an effect hidden in the whole
  population is clear in our data (access; see item 4). Measure women's distance from the
  municipality of residence in VZP data rather than relying on district averages.
- **Practices and districts below expectation.** Districts with coverage below what their
  population predicts (Frýdek-Místek, Jičín, Jeseník, Bruntál, Semily;
  `notebooks/mamograf_rozsireni.ipynb`, kap. 7) are the first candidates for items 4 and 6.

## How to test robustly: shared rules

- **Outcome from claims, not surveys:** screening claim 89223 or 89178 within 90 days of first
  contact (primary) and 180 days (secondary), any breast imaging, and return at the next round.
- **A current-practice control arm in every segment.** The 2014 Czech letter programme had none,
  so its effect is still unknown [`[CZ_INVITE2019]`](../PAPERS.md).
- **Randomise at the level where the intervention acts:** individual women for messages and
  booked slots; practices for doctor interventions; municipalities or districts for mobile units
  and transport; geography for media.
- **Stratify by segment × kraj, analyse intention-to-treat**, adjust for the model's pre-treatment
  risk score, and pre-register the primary contrasts and the decision rule (for example: scale an
  arm if P(lift > 1 pp) > 0.95 and cost per extra screen is below VZP's threshold).
- **Size.** About 3,000–9,000 women per arm detect +2 to +3 pp; +5 pp needs about 700–1,600 per
  arm (research brief, Experiment design).
- **Guardrails:** waiting time at partner centres, no-shows and opt-outs, and the deprivation gap.
- **When randomisation is impossible** (new centres, policy changes): interrupted time series
  [`[ITS_GUIDELINE2022]`](../PAPERS.md), difference-in-differences or synthetic control with
  untreated districts as comparison.
- **Evaluate beyond the effect:** reach, adoption by centres and practices, delivery fidelity and
  maintenance over later rounds (RE-AIM [`[REAIM2013]`](../PAPERS.md); a ten-year follow-up example
  in [`[CHILE_LONGTERM2022]`](../PAPERS.md)).

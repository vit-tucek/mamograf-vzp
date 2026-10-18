"""Impact numbers for pitch v2: what is at stake for VZP and what our measures bring.

    python docs/vzp_pitch/dopad.py      (prints the table; build_pitch_v2.py imports compute())

Population: VZP clients aged 45–74 who miss screening, estimated as the national number of women 45–74
without a screening mammography in two years (ČSÚ, ÚZIS) × VZP's share of insured persons, 56,7 %
(MZ ČR, Hodnocení vývoje systému v. z. p. v roce 2023: 6 159 982 of 10,87 mil.; the share of state-insured
persons is similar at all insurers, 53,7–58,7 %, so VZP's age structure is close to the average). This is a
lower bound: a woman screened twice in two years counts twice in the ÚZIS numbers.

Sources and assumptions (all per year):
- women 45–74: ČSÚ, mid-year 2024 (data/csu_zeny_okresy.csv.zip);
- screening mammographies 45–74 in 2023 + 2024: ÚZIS PPS-01-02 (data/uzis_pps_mamografie.csv.zip);
- breast cancers (C50) in women 45–74 and deaths: NOR 2024 (data/nor_c50_kraje.csv.zip);
- stage at diagnosis outside vs inside screening: stage I 28,5 % vs 75 % (NOR, screening audit 2023),
  stage IV 15,5 % in never-screened vs 0,7 % in regularly screened women (ÚZIS evaluation report 2022);
- per extra screening exam (team's financial model, base scenario 16. 10. 2026: 291 346 exams,
  1 605 cancers found earlier, 189 deaths averted within 5 years of diagnosis, 654 M Kč treatment saved,
  510 M Kč screening, recall, 1 000 Kč contribution and overdiagnosis): 5,51 earlier cancers and 0,649 deaths
  per 1 000 exams, net +494 Kč per exam. Holds with stage IV treatment ≈ 3 M Kč; below ≈ 1,9 M Kč ≈ 0;
- QALY: stage-shift model, 3,82 QALY per 1 000 extra mammographies at ages 45–74 (docs/ZJISTENI.md, kap. 3);
- ceiling: every unscreened VZP client screened once per two years (unscreened / 2 exams a year);
- targeted measures: pre-booked slot in B + C (+10 to +19 p. b.) and doctor as a channel in D + E (+2 to +6 p. b.),
  computed on the 2024 VZP invitations (66 037 and 140 398 women) and scaled to the VZP population by
  unscreened VZP clients / 2024 non-attenders, i.e. the same segment mix and effects;
- mass SMS reminder (upside scenario): all unscreened VZP clients, +2 to +5 p. b. (docs/interventions.md, item 8).
  It reaches the same women as the targeted measures, so the two are not additive.
"""
import io
import zipfile
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "data"
AGES = ["45-49", "50-54", "55-59", "60-64", "65-69", "70-74"]

VZP_SHARE = 6_159_982 / 10_870_000            # MZ ČR, Hodnocení v. z. p. 2023 (56,7 %)
PER_1000 = {"cancers": 1605 / 291_346 * 1000, "deaths": 189 / 291_346 * 1000, "qaly": 3.82}
NET_KC_PER_EXAM = (654e6 - 510e6) / 291_346
STAGE_OUT = {"I": 0.285, "II–III": 1 - 0.285 - 0.155, "IV": 0.155}      # outside screening / never screened
STAGE_IN = {"I": 0.75, "II–III": 1 - 0.75 - 0.007, "IV": 0.007}        # found by screening / regularly screened
VZP_2024 = {"invited": 256_466, "not_came": 207_201, "B_E_not_came": 159_063,
            "B_C": 37_460 + 28_577, "D_E": 51_047 + 89_351}
SMS_EFFECT = (0.02, 0.05)


def _csv(name, **kw):
    with zipfile.ZipFile(DATA / f"{name}.csv.zip") as z:
        return pd.read_csv(io.BytesIO(z.read(z.namelist()[0])), **kw)


def metrics(exams):
    """Per-year metrics for a number of extra screening exams."""
    return {"exams": exams,
            "cancers": exams * PER_1000["cancers"] / 1000,
            "deaths": exams * PER_1000["deaths"] / 1000,
            "qaly": exams * PER_1000["qaly"] / 1000,
            "net_kc": exams * NET_KC_PER_EXAM}


def compute():
    z = _csv("csu_zeny_okresy")
    z["vek"] = z["Věkové skupiny (pětileté)"].str.replace(" ", "")
    women = z[(z.Rok == 2024) & z.vek.isin(AGES)].Hodnota.sum()
    m = _csv("uzis_pps_mamografie")
    m = m[m.vek_nazev.str[:5].str.replace("–", "-").isin(AGES) & m.rok.isin([2023, 2024])]
    screens_2y = m.pocet_vysetreni.sum()
    coverage = screens_2y / women
    unscreened = women - screens_2y
    n = _csv("nor_c50_kraje", dtype={"stadium": str})
    inc = n[(n.ukazatel == "incidence") & (n.rok == 2024)]
    inc = inc[inc.vek.map(lambda c: 45 <= int(str(c)[2:5]) <= 70)]
    cancers_45_74 = inc.n.sum()
    deaths = n[(n.ukazatel == "umrti") & (n.rok == 2024)].n.sum()

    vzp_unscreened = unscreened * VZP_SHARE
    vzp_ceiling = metrics(vzp_unscreened / 2)                     # each screened once per two years
    cancers_check = cancers_45_74 * (1 - coverage) * VZP_SHARE     # incidence-based cross-check
    scale = vzp_unscreened / VZP_2024["not_came"]                  # same segment mix as the 2024 non-attenders
    ours = {k: metrics(scale * (VZP_2024["B_C"] * eff_bc + VZP_2024["D_E"] * eff_de))
            for k, (eff_bc, eff_de) in {"low": (0.10, 0.02), "high": (0.19, 0.06)}.items()}
    sms = {k: metrics(vzp_unscreened * e) for k, e in zip(("low", "high"), SMS_EFFECT)}
    return {"women": women, "coverage": coverage, "unscreened": unscreened, "vzp_share": VZP_SHARE,
            "vzp_unscreened": vzp_unscreened, "vzp_be": vzp_unscreened * VZP_2024["B_E_not_came"] / VZP_2024["not_came"],
            "scale": scale, "cancers_45_74": cancers_45_74, "deaths_all": deaths, "cancers_check": cancers_check,
            "vzp_ceiling": vzp_ceiling, "ours": ours, "sms": sms,
            "share_of_ceiling": tuple(ours[k]["exams"] / vzp_ceiling["exams"] for k in ("low", "high"))}


if __name__ == "__main__":
    r = compute()
    print(f"women 45–74 (ČSÚ 2024): {r['women']:,.0f}; two-year coverage {r['coverage']:.1%}; unscreened ≥ {r['unscreened']:,.0f}")
    print(f"VZP share {r['vzp_share']:.1%} → unscreened VZP clients ≥ {r['vzp_unscreened']:,.0f} "
          f"(of them in B–E ≈ {r['vzp_be']:,.0f}); scale vs 2024 non-attenders {r['scale']:.2f}")
    print(f"cancers check (NOR 45–74 × unscreened share × VZP share): {r['cancers_check']:,.0f}")
    for name, m in [("ceiling", r["vzp_ceiling"]), ("ours low", r["ours"]["low"]), ("ours high", r["ours"]["high"]),
                    ("SMS low", r["sms"]["low"]), ("SMS high", r["sms"]["high"])]:
        print(f"{name:10s} exams {m['exams']:>9,.0f}  cancers earlier {m['cancers']:>6,.0f}  deaths {m['deaths']:>5,.1f}  "
              f"QALY {m['qaly']:>6,.0f}  net {m['net_kc'] / 1e6:>6,.1f} M Kč")
    lo, hi = r["share_of_ceiling"]
    print(f"targeted measures = {lo:.1%}–{hi:.1%} of the ceiling")

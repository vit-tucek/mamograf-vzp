"""Načtení dat pro notebook mamograf_analyza.ipynb.

Port načítacích kroků z mamograf_exploration.ipynb (kap. 2–4, 8.0, 8 a 9), jen
nad lokální cache v data/: nic se nestahuje. Soubory se čtou buď rozbalené
z data/<soubor>, nebo přímo ze zipu data/<soubor>.zip (příkaz unzip není potřeba).
Chybí-li cache, je potřeba nejdřív spustit explorační notebook.
"""
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
ROK = 2024                       # referenční rok
ROKY_V = range(ROK - 4, ROK + 1)  # okno pro průřezové ukazatele (2020–2024)

BANDS = ["45–49", "50–54", "55–59", "60–64", "65–69", "70–74", "75–79", "80–84", "85+"]
TOTAL = "45+ celkem"
BAND_ORDER = [TOTAL] + BANDS

UZIS_TO_BAND = {f"{a}–{a+4} let": f"{a}–{a+4}" for a in range(45, 85, 5)}
UZIS_TO_BAND.update({"85–89 let": "85+", "90 let a více": "85+", "85 let a více": "85+"})
CSU_TO_BAND = {f"{a} - {a+4}": f"{a}–{a+4}" for a in range(45, 85, 5)}
CSU_TO_BAND.update({"85 - 89": "85+", "90 - 94": "85+", "95 a více": "85+"})


def _bajty(nazev):
    f = DATA / nazev
    if f.exists():
        return f.read_bytes()
    z = DATA / f"{nazev}.zip"
    if not z.exists():
        raise FileNotFoundError(f"{nazev}: chybí v data/ i jako zip; "
                                "spusťte nejdřív mamograf_exploration.ipynb")
    with zipfile.ZipFile(z) as zf:
        return zf.read(nazev)


def csv(nazev, **kw):
    """CSV z data/, rozbalené nebo přímo ze zipu."""
    return pd.read_csv(io.BytesIO(_bajty(nazev)), **kw)


# ---------------------------------------------------------------- panel pokrytí

def _s_total(df, cols):
    """Přidá souhrnný řádek 45+ celkem."""
    t = df.groupby(["rok", "lau"], as_index=False)[cols].sum()
    t["band"] = TOTAL
    return pd.concat([df, t], ignore_index=True)


def panel():
    """Panel rok × okres × věkové pásmo (kap. 2–4 explorace).

    Vrací (D, OKRES, KRAJ): D má počty žen (ČSÚ), mamografií, preventivních
    prohlídek a kapitační populace a z nich mamo_1y, mamo_2y, prev [%]."""
    mamo = csv("uzis_pps_mamografie.csv")
    mamo = mamo[mamo.vek_nazev.isin(UZIS_TO_BAND)].copy()
    mamo["band"] = mamo.vek_nazev.map(UZIS_TO_BAND)
    mamo = (mamo.rename(columns={"okres_lau_kod": "lau"})
                .groupby(["rok", "lau", "okres_nazev", "kraj_nazev", "band"], as_index=False)
                ["pocet_vysetreni"].sum())

    prev = csv("uzis_pps_prevence_zeny45.csv")
    prev = prev[(prev.pohlavi == "Z") & (prev.icz_okres_kod != "CZ9999")
                & prev.vek_nazev.isin(UZIS_TO_BAND)].copy()
    prev["band"] = prev.vek_nazev.map(UZIS_TO_BAND)
    prev = (prev.rename(columns={"icz_okres_kod": "lau"})
                .groupby(["rok", "lau", "band"], as_index=False)
                [["populace", "pocet_vysetrenych"]].sum())

    pop = csv("csu_zeny_okresy.csv").rename(
        columns={"Uz3A": "lau", "Rok": "rok", "Věkové skupiny (pětileté)": "vek",
                 "Hodnota": "zeny"})
    pop["band"] = pop.vek.map(CSU_TO_BAND)
    pop = pop.groupby(["rok", "lau", "band"], as_index=False)["zeny"].sum()

    OKRES = dict(zip(mamo.lau, mamo.okres_nazev))
    KRAJ = dict(zip(mamo.lau, mamo.kraj_nazev))

    m = _s_total(mamo[["rok", "lau", "band", "pocet_vysetreni"]], ["pocet_vysetreni"])
    p = _s_total(prev, ["populace", "pocet_vysetrenych"])
    z = _s_total(pop, ["zeny"])
    D = (z.merge(m, on=["rok", "lau", "band"], how="left")
          .merge(p, on=["rok", "lau", "band"], how="left")
          .sort_values(["lau", "band", "rok"]))
    D["mamo_predchozi"] = D.groupby(["lau", "band"])["pocet_vysetreni"].shift(1)
    D["mamo_1y"] = 100 * D.pocet_vysetreni / D.zeny
    D["mamo_2y"] = 100 * (D.pocet_vysetreni + D.mamo_predchozi) / D.zeny
    D["prev"] = 100 * D.pocet_vysetrenych / D.populace
    D["kapitace_index"] = D.populace / D.zeny
    D["okres"] = D.lau.map(OKRES)
    D["kraj"] = D.lau.map(KRAJ)
    D["band"] = pd.Categorical(D.band, BAND_ORDER, ordered=True)
    return D.reset_index(drop=True), OKRES, KRAJ


# ---------------------------------------------------------------- geometrie

def _area(ring):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:])) / 2


def _fix_winding(geom):
    """Vnější prstenec po směru hodinových ručiček, díry proti (Plotly/d3-geo)."""
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for k, ring in enumerate(poly):
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            if (_area(ring) < 0) != (k == 0):
                ring.reverse()


def centroid(geom):
    """Plošně vážené těžiště (Multi)Polygonu ve stupních."""
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    A = cx = cy = 0.0
    for poly in polys:
        ring, a, sx, sy = poly[0], 0.0, 0.0, 0.0
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            cr = x1 * y2 - x2 * y1
            a, sx, sy = a + cr, sx + (x1 + x2) * cr, sy + (y1 + y2) * cr
        if a:
            A += abs(a / 2); cx += abs(a / 2) * sx / (3 * a); cy += abs(a / 2) * sy / (3 * a)
    return cx / A, cy / A


def geo():
    """Hranice okresů (RÚIAN) s opravenou orientací a těžiště okresů."""
    GEO = json.loads(_bajty("ruian_okresy.geojson").decode("utf-8"))
    for ft in GEO["features"]:
        ft["id"] = ft["properties"]["nutslau"][:6]
        _fix_winding(ft["geometry"])
    return GEO, {ft["id"]: centroid(ft["geometry"]) for ft in GEO["features"]}


def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0
    f1, f2 = np.radians(lat1), np.radians(lat2)
    a = (np.sin((f2 - f1) / 2) ** 2
         + np.cos(f1) * np.cos(f2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2)
    return 2 * R * np.arcsin(np.sqrt(a))


def pracoviste():
    """Akreditovaná mamografická pracoviště (mamo.cz, geokódovaná na obec)."""
    centra = csv("mamocz_pracoviste.csv")
    assert centra.obec_lau.notna().all(), "pracoviště bez okresu"
    return centra


def nejblizsi(CENTROID, centra):
    """Vzdálenost z těžiště okresu k nejbližší obci s pracovištěm."""
    cile = centra.groupby(["obec", "obec_lau", "lon", "lat"]).size().rename("n").reset_index()
    rows = []
    for lau, (lon, lat) in CENTROID.items():
        d = haversine(lon, lat, cile.lon.values, cile.lat.values)
        i = int(np.argmin(d))
        rows.append({"lau": lau, "nej_obec": cile.obec.iloc[i], "nej_km": float(d[i]),
                     "vlastni_pracoviste": lau in set(cile.obec_lau)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- NRHZS

def nrhzs():
    """Agregáty NR-04-86 (kap. 8.0 explorace).

    Vrací (nr, toky): nr v dlouhém formátu ukazatel × rok × lau, toky
    screeningových mamografií z_lau → cil_lau po letech."""
    return csv("nrhzs_ukazatele_okresy.csv"), csv("nrhzs_mamografie_toky.csv")


def vykony(nr, toky):
    """Průměr ukazatelů NRHZS za 2020–2024 + měřená dojížďka (podíl mimo okres)."""
    NR = (nr[nr.rok.isin(ROKY_V)]
          .pivot_table(index="lau", columns="ukazatel", values="hodnota", aggfunc="mean")
          .rename(columns={"vykony": "vykony_n", "gyn_prevence": "gyn_prevence_n",
                           "cytologie": "cytologie_n", "toks": "toks_n",
                           "diag_prs": "diag_prs_n"}))
    t = toky[toky.rok.isin(ROKY_V)].groupby(["z_lau", "cil_lau"], as_index=False).mnozstvi.sum()
    t["podil"] = t.mnozstvi / t.groupby("z_lau").mnozstvi.transform("sum")
    doma = t[t.z_lau == t.cil_lau].set_index("z_lau").podil
    VYK = (NR.assign(dojizdka_mamo_pct=100 * (1 - doma.reindex(NR.index).fillna(0)))
             .rename_axis("lau").reset_index())
    assert len(VYK) == 77, f"{len(VYK)} okresů"
    return VYK


# ---------------------------------------------------------------- kovariáty

POPIS = {
    "vs_zeny_pct":                 ("vysokoškolačky, ženy 15+", "%"),
    "zakl_vzd_zeny_pct":           ("jen základní vzdělání, ženy 15+", "%"),
    "nezam_zeny_pct":              ("podíl nezaměstnaných žen", "%"),
    "mimo_pracovni_silu_zeny_pct": ("ženy mimo pracovní sílu", "%"),
    "davky_ssp_Kc_obyv":           ("dávky SSP na obyvatele", "Kč"),
    "prisp_bydleni_Kc_obyv":       ("příspěvek na bydlení na obyvatele", "Kč"),
    "invalid_duchod_zeny_pct":     ("příjemkyně invalidního důchodu", "%"),
    "mimo_byty_pct":               ("osoby mimo byty a bez domova", "%"),
    "cizinky_pct":                 ("ženy s cizím občanstvím", "%"),
    "cena_byt_Kc_m2":              ("kupní cena bytů", "Kč/m²"),
    "cena_dum_Kc_m2":              ("kupní cena domů", "Kč/m²"),
    "hustota_obyv_km2":            ("hustota zalidnění", "obyv./km²"),
    "prumerny_vek_zeny":           ("průměrný věk žen", "let"),
    "podil_65plus_zeny":           ("ženy 65+", "%"),
    "vdovy_rozvedene_pct":         ("vdovy a rozvedené", "%"),
    "migrace_na_1000":             ("migrační saldo", "na 1 000 obyv."),
    "umrti_novotvary_zeny_pct":    ("úmrtí žen na novotvary", "%"),
    "obce_0_pct":                  ("obyvatelé obcí do 499 obyv.", "%"),
    "obce_1_pct":                  ("obyvatelé obcí 500–1 999 obyv.", "%"),
    "obce_2_pct":                  ("obyvatelé obcí 2 000–9 999 obyv.", "%"),
    "obce_3_pct":                  ("obyvatelé obcí 10 000–49 999 obyv.", "%"),
    "obce_4_pct":                  ("obyvatelé obcí 50 000+ obyv.", "%"),
    "ma_mamocentrum":              ("okres má mamografické pracoviště", "0/1"),
    "vzdalenost_km":               ("vzdálenost k nejbližšímu pracovišti", "km"),
    "dojizdka_mamo_pct":           ("mamografie mimo okres bydliště (měřeno)", "%"),
    "gyn_prevence_pct":            ("preventivní gynekologická prohlídka za rok", "% žen"),
    "vykony_na_obyv":              ("zdravotní výkony na obyvatele za rok", "výkonů"),
    "diag_prs_na100":              ("diagnostické zobrazení prsu", "na 100 žen"),
    "nezhoubne_prs_na1000":        ("nezhoubné nálezy prsu", "na 1 000 žen"),
    "rakovina_prs_na1000":         ("léčená rakovina prsu", "na 1 000 žen"),
    "cytologie_pct":               ("cytologie děložního čípku za rok", "% žen"),
    "toks_pct":                    ("test na okultní krvácení za rok", "% obyv."),
    "diabetes_pct":                ("diabetes (dolní odhad)", "% obyv."),
    "hypertenze_pct":              ("hypertenze (dolní odhad)", "% obyv."),
    "chopn_pct":                   ("CHOPN (dolní odhad)", "% obyv."),
    "deprese_pct":                 ("deprese (dolní odhad)", "% obyv."),
    "obezita_pct":                 ("obezita (dolní odhad)", "% obyv."),
    "volby_ANO_pct":               ("volby 2025: ANO", "%"),
    "volby_SPOLU_pct":             ("volby 2025: SPOLU", "%"),
    "volby_STAN_pct":              ("volby 2025: STAN", "%"),
    "volby_Piráti_pct":            ("volby 2025: Piráti", "%"),
    "volby_SPD_pct":               ("volby 2025: SPD", "%"),
    "volby_AUTO_pct":              ("volby 2025: Motoristé", "%"),
    "volby_Stačilo_pct":           ("volby 2025: Stačilo!", "%"),
}
STRANY = ["ANO", "SPOLU", "STAN", "Piráti", "SPD", "AUTO", "Stačilo!"]


def kovariaty(D, OKRES, VYK, NEJ):
    """Okresní tabulka X (kap. 8 explorace): pokrytí průměrované za 2020–2024,
    kovariáty ČSÚ a SLDB, výkony NRHZS, volby a dostupnost."""
    KOV = csv("csu_kovariaty_okresy.csv")
    KOV["cizinky_pct"] = 100 * KOV.cizinky_pocet / KOV.zeny_celkem
    KOV["davky_ssp_Kc_obyv"] = 1000 * KOV.davky_ssp_tisKc / KOV.obyvatel
    KOV["prisp_bydleni_Kc_obyv"] = 1000 * KOV.prisp_bydleni_tisKc / KOV.obyvatel
    KOV["invalid_duchod_zeny_pct"] = 100 * KOV.invalidni_duchody_zeny / KOV.zeny_celkem
    KOV["migrace_na_1000"] = 1000 * KOV.migracni_saldo / KOV.obyvatel

    KOV = KOV.merge(VYK, on="lau", how="left")
    KOV["gyn_prevence_pct"] = 100 * KOV.gyn_prevence_n / KOV.zeny_celkem
    KOV["vykony_na_obyv"] = KOV.vykony_n / KOV.obyvatel
    KOV["diag_prs_na100"] = 100 * KOV.diag_prs_n / KOV.zeny_celkem
    KOV["nezhoubne_prs_na1000"] = 1000 * KOV.nezhoubne_prs / KOV.zeny_celkem
    KOV["rakovina_prs_na1000"] = 1000 * KOV.rakovina_prs / KOV.zeny_celkem
    KOV["cytologie_pct"] = 100 * KOV.cytologie_n / KOV.zeny_celkem
    KOV["toks_pct"] = 100 * KOV.toks_n / KOV.obyvatel
    for s in ("diabetes", "hypertenze", "chopn", "deprese", "obezita"):
        KOV[f"{s}_pct"] = 100 * KOV[s] / KOV.obyvatel

    # volby: středník, desetinná čárka, BOM, názvy okresů končí U+200B
    volby = csv("volby_ps2025_okresy.csv", sep=";", decimal=",", encoding="utf-8-sig")
    volby.columns = [c.strip() for c in volby.columns]
    volby["okres"] = volby[volby.columns[0]].str.replace("​", "", regex=False).str.strip()
    volby = volby[volby.okres != "Celkem"]
    volby["lau"] = volby.okres.map({v: k for k, v in OKRES.items()})
    assert volby.lau.notna().all(), f"nespárované okresy: {volby[volby.lau.isna()].okres.tolist()}"
    volby = volby.rename(columns={s: f"volby_{s.rstrip('!')}_pct" for s in STRANY})
    KOV = KOV.merge(volby[["lau"] + [f"volby_{s.rstrip('!')}_pct" for s in STRANY]],
                    on="lau", how="left")

    POKR = (D[(D.band == TOTAL) & D.rok.isin(ROKY_V)]
            .groupby("lau", as_index=False)[["mamo_2y", "prev"]].mean())
    d = D[(D.rok == ROK) & (D.band == TOTAL)][["lau", "okres", "kraj", "zeny"]]
    X = (POKR.merge(KOV, on="lau").merge(d, on="lau")
             .merge(NEJ[["lau", "nej_km", "vlastni_pracoviste"]], on="lau"))
    X["ma_mamocentrum"] = X.vlastni_pracoviste.astype(int)
    X["vzdalenost_km"] = X.nej_km
    assert len(X) == 77
    return X


# ---------------------------------------------------------------- očkování

PRED_COVID = ["2017-2018", "2018-2019", "2019-2020"]
PO_COVIDU = ["2022-2023", "2023-2024", "2024-2025"]
COV_45 = ["45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]


def _chripka(list_, NA_LAU):
    raw = pd.read_excel(io.BytesIO(_bajty("uzis_chripka_proockovanost.xlsx")),
                        sheet_name=list_, header=None)
    h = raw.index[raw[0] == "územní celek"][0]
    sezona = raw.iloc[h].ffill()
    sl = [j for j in raw.columns if raw.iloc[h + 1, j] == "proočkovanost vakcinovaných (%)"]
    t = raw.iloc[h + 2:, [0] + sl]
    t.columns = ["uzemi"] + [sezona[j].replace("sezóna ", "") for j in sl]
    t["lau"] = t.uzemi.replace({"Hl. m. Praha": "Praha"}).map(NA_LAU)
    t = t.dropna(subset=["lau"]).set_index("lau").drop(columns="uzemi")
    assert len(t) == 77, f"{list_}: spárováno {len(t)} okresů"
    return 100 * t.astype(float)


def ockovani(D, OKRES):
    """Proočkovanost proti chřipce (před/po covidu) a covidu (ženy 45+) po okresech."""
    NA_LAU = {v: k for k, v in OKRES.items()}
    OCK = pd.DataFrame(index=sorted(OKRES))
    for list_, kl in [("Chřipka_65", "chripka65"), ("Chřipka", "chripka")]:
        t = _chripka(list_, NA_LAU)
        OCK[f"{kl}_pred"] = t[PRED_COVID].mean(axis=1)
        OCK[f"{kl}_po"] = t[PO_COVIDU].mean(axis=1)

    ORP = csv("ruian_orp_okresy.csv")
    ORP["kraj"] = ORP.lau.str[:5]
    cov = csv("mzcr_covid_davky_zeny45_orp.csv")
    cov = cov[(cov.pohlavi == "Z") & cov.vekova_skupina.isin(COV_45)
              & (cov.orp_bydliste_kod > 0) & (cov.orp_bydliste != "cizinci")].copy()
    cov["kraj"] = "CZ0" + cov.orp_bydliste_kod.astype(int).astype(str).str[:2]
    cov = cov.merge(ORP, left_on=["orp_bydliste", "kraj"], right_on=["orp", "kraj"], how="left")
    assert cov.lau.notna().all(), "ORP bez okresu"
    davky = cov.pivot_table(index="lau", columns="poradi_davky", values="pocet_davek",
                            aggfunc="sum")
    zeny21 = D[(D.rok == 2021) & (D.band == TOTAL)].set_index("lau").zeny
    OCK["covid_1_zeny45"] = 100 * davky[1] / zeny21
    OCK["covid_3_zeny45"] = 100 * davky[3] / zeny21
    return OCK.rename_axis("lau").reset_index()


# ---------------------------------------------------------------- rozšíření (mamograf_rozsireni)

def nrhzs_icz():
    """Screeningové mamografie po IČZ (rok × IČZ × okres zařízení × okres pacienta)
    a preventivní gynekologie po IČZ (rok × IČZ × okres zařízení)."""
    return (csv("nrhzs_mamografie_icz.csv", dtype={"ICZ": str}),
            csv("nrhzs_gyn_icz.csv", dtype={"ICZ": str}))


def gyn_okresy():
    """Ordinace registrujících gynekologů po okresech (NRPZS, průřez 10/2026)."""
    return csv("nrpzs_gyn_okresy.csv")


def centra_historie():
    """Počet akreditovaných pracovišť po okresech a letech (mamo.cz 2008–2019 z web.archive.org, 2026)."""
    return csv("mamocz_pracoviste_historie.csv")


def cekaci_doby():
    """Objednací lhůty akreditovaných pracovišť (mamo.cz přes web.archive.org, 2013–2019):
    jeden řádek na pracoviště a snímek, sloupec `cekani_dni`, datum údaje `datum`."""
    t = csv("mamocz_cekaci_doby.csv")
    t["rok"] = t.datum.str[:4].astype(int)
    return t


def nor_c50():
    """Karcinom prsu u žen (NOR): incidence podle roku dg., kraje, věku a stadia; úmrtí podle roku a kraje.
    Věk je kód ÚZIS 66AAABBB (pásmo AAA–BBB let)."""
    t = csv("nor_c50_kraje.csv", dtype={"vek": str, "stadium": str})
    t["vek_od"] = t.vek.str[2:5].astype(int)
    return t


def vse():
    """Všechno najednou: slovník s D, OKRES, KRAJ, GEO, CENTROID, centra, NEJ,
    nr, toky, VYK, X, OCK."""
    D, OKRES, KRAJ = panel()
    GEO, CENTROID = geo()
    assert set(CENTROID) == set(D.lau), "geometrie a data si neodpovídají"
    centra = pracoviste()
    NEJ = nejblizsi(CENTROID, centra)
    nr, toky = nrhzs()
    VYK = vykony(nr, toky)
    X = kovariaty(D, OKRES, VYK, NEJ)
    OCK = ockovani(D, OKRES)
    return dict(D=D, OKRES=OKRES, KRAJ=KRAJ, GEO=GEO, CENTROID=CENTROID, centra=centra,
                NEJ=NEJ, nr=nr, toky=toky, VYK=VYK, X=X, OCK=OCK)

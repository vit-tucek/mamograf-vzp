"""Přepočet okresních agregátů v data/ z velkých zdrojových sad v sources/.

Notebook mamograf_exploration.ipynb pracuje jen s agregáty v data/ (v repozitáři
zabalené jako data/<soubor>.zip). Tento skript je potřeba spustit jen tehdy, když
se mají agregáty přepočítat, např. z nové verze zdrojových sad. Zdrojové sady
(viz docs/ZDROJE_DAT.md) patří do sources/ pod původními názvy (git ji ignoruje).

    python utils/priprava_dat.py            # přepočítá a zabalí všechny agregáty
    python utils/priprava_dat.py --bez-zip  # jen přepočítá, nezabalí
    python utils/priprava_dat.py --jen nrhzs_icz  # jen vybrané kroky

Výkony NRHZS (2,3 GB gz) se agregují přes DuckDB přímo nad .gz, asi 2 minuty.
"""
import sys
import zipfile
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
SOURCES = BASE / "sources"

F_PREV_RAW = SOURCES / "Otevrena-data-PPS-08-04-preventivni-prohlidky-pokryti-kapitace.csv"
F_COVID_RAW = SOURCES / "ockovani-zakladni-prehled.csv"
F_VYKONY_RAW = SOURCES / "Otevrena-data-NR-04-86-vykony-icz-okres-diagnoza.csv.gz"

F_PREV = DATA / "uzis_pps_prevence_zeny45.csv"
F_COVID = DATA / "mzcr_covid_davky_zeny45_orp.csv"
F_NRHZS = DATA / "nrhzs_ukazatele_okresy.csv"
F_TOKY = DATA / "nrhzs_mamografie_toky.csv"

VEK_45_UZIS = ([f"{a}–{a+4} let" for a in range(45, 85, 5)]
               + ["85–89 let", "90 let a více", "85 let a více"])
VEK_45_COVID = ["45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]

# kódy výkonů NR-04-86 určené z dat (diagnózy a objemy), viz docs/ZDROJE_DAT.md
KOD_MAMO_SCR = "89223"    # screeningová mamografie (dg. Z12, počty sedí s PPS-01-02)
KOD_MAMO_DOPL = "89814"   # vykazuje se spolu s 89223 (shodné počty), do diagnostiky nepatří
KOD_GYN_PREV = "63050"    # preventivní gynekologická prohlídka (dg. Z01)
KOD_CYTOLOGIE = "63417"   # cytologie děložního čípku (z poloviny dg. Z01)
KODY_TOKS = ["15118", "15119", "15120"]   # test na okultní krvácení (dg. Z12)
SKUP_DG = {"rakovina_prs": ["C50", "D05"],
           "nezhoubne_prs": ["D24", "N60", "N61", "N62", "N63", "N64", "R92"],
           "diabetes": ["E10", "E11", "E12", "E13", "E14"],
           "hypertenze": ["I10", "I11", "I12", "I13", "I15"],
           "chopn": ["J44"], "deprese": ["F32", "F33"], "obezita": ["E66"]}


def prevence():
    """PPS-08-04: jen ženy 45+, kapitační skupiny sečtené."""
    r = pd.read_csv(F_PREV_RAW)
    klic = [c for c in r.columns if c not in ("kapitace_skupina", "populace", "pocet_vysetrenych")]
    (r[(r.pohlavi == "Z") & r.vek_nazev.isin(VEK_45_UZIS)]
       .groupby(klic, as_index=False)[["populace", "pocet_vysetrenych"]].sum()
       .to_csv(F_PREV, index=False))
    return [F_PREV]


def covid():
    """Očkování proti covidu: jen ženy 45+, sečteno přes vakcíny a kraje očkování."""
    r = pd.read_csv(F_COVID_RAW, usecols=["orp_bydliste", "orp_bydliste_kod", "poradi_davky",
                                          "vekova_skupina", "pohlavi", "pocet_davek"])
    (r[(r.pohlavi == "Z") & r.vekova_skupina.isin(VEK_45_COVID)]
       .groupby(["orp_bydliste", "orp_bydliste_kod", "poradi_davky", "vekova_skupina",
                 "pohlavi"], as_index=False).pocet_davek.sum()
       .to_csv(F_COVID, index=False))
    return [F_COVID]


def praha(s):
    """NRHZS člení Prahu na obvody CZ0101–CZ010A, ostatní data ji mají jako celek."""
    return s.where(~s.str.startswith("CZ010"), "CZ0100")


def dolni_odhad(t, klic):
    """Pacienti, dolní odhad: v každém roce a okrese výkon s nejvíce pacienty
    (součet přes výkony by téhož pacienta započítal několikrát)."""
    return t.groupby(klic + ["kod"]).pacienti.sum().groupby(klic).max()


def agreguj_nrhzs(vk, tk, dg):
    """Hrubé souhrny z DuckDB → malé okresní agregáty."""
    for t in (vk, tk, dg):
        t.drop(t.index[t.okres_pacient == "CZ0999"], inplace=True)   # neuvedeno
        t["lau"] = praha(t.okres_pacient)
    k = ["rok", "lau"]
    u = {"vykony": vk.groupby(k).mnozstvi.sum(),
         "gyn_prevence": vk[vk.kod == KOD_GYN_PREV].groupby(k).pacienti.sum(),
         "cytologie": vk[vk.kod == KOD_CYTOLOGIE].groupby(k).pacienti.sum(),
         "toks": dolni_odhad(vk[vk.kod.isin(KODY_TOKS)], k)}
    for s in SKUP_DG:
        u[s] = dolni_odhad(dg[dg.skupina == s], k)
    prs = dg.skupina.isin(["rakovina_prs", "nezhoubne_prs"])
    zobr = dg.kod.str.startswith("89") & ~dg.kod.isin([KOD_MAMO_SCR, KOD_MAMO_DOPL])
    u["diag_prs"] = dg[prs & zobr].groupby(k).mnozstvi.sum()
    ukaz = pd.concat(u, names=["ukazatel"]).rename("hodnota").reset_index()
    tk = tk[(tk.kod == KOD_MAMO_SCR) & (tk.okres_ICZ != "CZ0999")]
    toky = (tk.assign(cil_lau=praha(tk.okres_ICZ))
              .groupby(["rok", "lau", "cil_lau"], as_index=False).mnozstvi.sum()
              .rename(columns={"lau": "z_lau"}))
    return ukaz, toky


def nrhzs():
    """NR-04-86 (334 mil. řádků): tři průchody DuckDB nad .gz, pak agregace v pandas."""
    import duckdb
    src = (f"read_csv('{F_VYKONY_RAW}', header=true, columns={{"
           "'rok':'INTEGER','kod':'VARCHAR','diagnoza':'VARCHAR','ICZ':'VARCHAR',"
           "'okres_ICZ':'VARCHAR','okres_pacient':'VARCHAR','mnozstvi':'DOUBLE',"
           "'pocet_pacientu':'BIGINT','pocet_kontaktu':'BIGINT'})")
    sumy = "sum(mnozstvi) AS mnozstvi, sum(pocet_pacientu) AS pacienti"
    skupina = "CASE " + " ".join(
        f"WHEN diagnoza IN ({', '.join(repr(x) for x in dg)}) THEN '{s}'"
        for s, dg in SKUP_DG.items()) + " END"
    con = duckdb.connect()
    ukaz, toky = agreguj_nrhzs(
        con.execute(f"SELECT rok, okres_pacient, kod, {sumy} FROM {src} GROUP BY ALL").df(),
        con.execute(f"SELECT rok, kod, okres_pacient, okres_ICZ, {sumy} FROM {src} "
                    f"WHERE kod = '{KOD_MAMO_SCR}' GROUP BY ALL").df(),
        con.execute(f"SELECT rok, okres_pacient, {skupina} AS skupina, kod, {sumy} "
                    f"FROM {src} WHERE skupina IS NOT NULL GROUP BY ALL").df())
    ukaz.to_csv(F_NRHZS, index=False)
    toky.to_csv(F_TOKY, index=False)
    return [F_NRHZS, F_TOKY]


F_MAMO_ICZ = DATA / "nrhzs_mamografie_icz.csv"
F_GYN_ICZ = DATA / "nrhzs_gyn_icz.csv"


def nrhzs_icz():
    """NR-04-86 po jednotlivých IČZ: screeningová mamografie (rok × IČZ × okres zařízení ×
    okres pacienta) a preventivní gynekologie (rok × IČZ × okres zařízení). Jeden průchod DuckDB."""
    import duckdb
    src = (f"read_csv('{F_VYKONY_RAW}', header=true, columns={{"
           "'rok':'INTEGER','kod':'VARCHAR','diagnoza':'VARCHAR','ICZ':'VARCHAR',"
           "'okres_ICZ':'VARCHAR','okres_pacient':'VARCHAR','mnozstvi':'DOUBLE',"
           "'pocet_pacientu':'BIGINT','pocet_kontaktu':'BIGINT'})")
    t = duckdb.connect().execute(
        f"SELECT rok, kod, ICZ, okres_ICZ, okres_pacient, sum(mnozstvi) AS mnozstvi, "
        f"sum(pocet_pacientu) AS pacienti FROM {src} "
        f"WHERE kod IN ('{KOD_MAMO_SCR}', '{KOD_GYN_PREV}') GROUP BY ALL").df()
    t = t[(t.okres_ICZ != "CZ0999") & (t.okres_pacient != "CZ0999")].copy()
    t["okres_ICZ"], t["okres_pacient"] = praha(t.okres_ICZ), praha(t.okres_pacient)
    k = ["rok", "ICZ", "okres_ICZ"]
    (t[t.kod == KOD_MAMO_SCR].groupby(k + ["okres_pacient"], as_index=False).mnozstvi.sum()
       .sort_values(k + ["okres_pacient"]).to_csv(F_MAMO_ICZ, index=False))
    (t[t.kod == KOD_GYN_PREV].groupby(k, as_index=False)[["mnozstvi", "pacienti"]].sum()
       .sort_values(k).to_csv(F_GYN_ICZ, index=False))
    return [F_MAMO_ICZ, F_GYN_ICZ]


F_NRPZS_RAW = SOURCES / "Otevrena-data-NR-01-06-nrpzs-mista-poskytovani-zdravotnich-sluzeb.csv"
F_NOR_RAW = SOURCES / "Otevrena-data-NR-07-01-novotvary-incidence-prevalence-regiony.csv.gz"
F_NOR_UMRTI_RAW = SOURCES / "Otevrena-data-NR-07-02-novotvary-mortalita-regiony.csv.gz"
WAYBACK = SOURCES / "wayback_mamo"          # roční snímky seznamu center z web.archive.org

F_GYN_OKRESY = DATA / "nrpzs_gyn_okresy.csv"
F_NOR = DATA / "nor_c50_kraje.csv"
F_CENTRA_HIST = DATA / "mamocz_pracoviste_historie.csv"


def nrpzs():
    """NRPZS: ordinace registrujících gynekologů (samostatné ordinace PL-gynekologa) po okresech.
    Registr obsahuje jen místa, která dnes fungují, proto je to průřez k datu stažení."""
    r = pd.read_csv(F_NRPZS_RAW, low_memory=False, dtype={"ZZ_okres_kod": str})
    g = r[r.ZZ_druh_nazev == "Samostatná ordinace PL - gynekologa"].dropna(subset=["ZZ_okres_kod"])
    g = g.drop_duplicates("ZZ_misto_poskytovani_ID").assign(lau=lambda t: praha(t.ZZ_okres_kod))
    (g.groupby("lau").agg(gyn_ordinace=("ZZ_misto_poskytovani_ID", "size"),
                          gyn_poskytovatele=("poskytovatel_ICO", "nunique"))
      .reset_index().to_csv(F_GYN_OKRESY, index=False))
    return [F_GYN_OKRESY]


def nor():
    """NOR: karcinom prsu (C50) u žen podle roku diagnózy, kraje, věku a stadia + úmrtí podle roku úmrtí."""
    r = pd.read_csv(F_NOR_RAW, dtype=str,
                    usecols=["pohlavi", "kraj_kod", "diagnoza_kod", "stadium", "rok_dg", "vek_kategorie_kod_dg"])
    r = r[(r.diagnoza_kod == "C50") & (r.pohlavi == "2")]
    inc = (r.groupby(["rok_dg", "kraj_kod", "vek_kategorie_kod_dg", "stadium"]).size().rename("n")
             .reset_index().rename(columns={"rok_dg": "rok", "kraj_kod": "kraj", "vek_kategorie_kod_dg": "vek"})
             .assign(ukazatel="incidence"))
    m = pd.read_csv(F_NOR_UMRTI_RAW, dtype=str)
    m = m[(m.diagnoza_kod == "C50") & (m.pohlavi == "2")]
    um = (m.groupby(["umrti_rok", "kraj_kod", "umrti_vek_kategorie_kod"]).size().rename("n").reset_index()
            .rename(columns={"umrti_rok": "rok", "kraj_kod": "kraj", "umrti_vek_kategorie_kod": "vek"})
            .assign(stadium="", ukazatel="umrti"))
    pd.concat([inc, um])[["ukazatel", "rok", "kraj", "vek", "stadium", "n"]].to_csv(F_NOR, index=False)
    return [F_NOR]


F_CEKANI = DATA / "mamocz_cekaci_doby.csv"


def _snimky_mamocz():
    """Snímky seznamu pracovišť mamo.cz 2008–2019 jako řádky textu: (rok snímku, řádky).
    Nový web (od 2020) má seznam na jiné stránce, kterou snímky neobsahují."""
    import html
    import re
    for f in sorted(WAYBACK.glob("*.html")):
        rok = int(f.name[:4])
        if rok > 2019:
            continue
        b = f.read_bytes()
        m = re.search(rb'charset=["\']?([\w-]+)', b)
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ",
                   b.decode(m.group(1).decode() if m else "utf-8", errors="replace"), flags=re.S)
        yield rok, [s.strip() for s in html.unescape(re.sub(r"<[^>]+>", "\n", t)).splitlines() if s.strip()]


def _obec_lau():
    """Obec pracoviště → okres; aktuální seznam + obce, které v něm už nejsou."""
    sys.path.insert(0, str(BASE))
    from utils import nacteni
    centra = nacteni.csv("mamocz_pracoviste.csv")
    m = dict(zip(centra.obec, centra.obec_lau))
    m.update({"Plzeň": "CZ0323", "Nové Město n. M.": "CZ0635", "Vrchlabí": "CZ0525"})
    return m, centra


def _mesto(s):
    import re
    return re.sub(r"^(Praha|Ostrava|Brno|Plzeň).*", r"\1", re.sub(r"\s*\d+$", "", s))


def centra_historie():
    """Počet akreditovaných pracovišť po okresech a letech ze snímků mamo.cz (2008–2019, web.archive.org)
    a z aktuálního seznamu (data/mamocz_pracoviste.csv). Pracoviště se páruje přes obec z PSČ řádku."""
    import re
    obec_lau, centra = _obec_lau()
    rows = []
    for rok, lines in _snimky_mamocz():
        for i, s in enumerate(lines[:-1]):
            if re.fullmatch(r"\d{3} ?\d{2}", s) and re.match(r"^[A-ZÁ-Ž]", lines[i + 1]):
                rows.append({"rok": rok, "lau": obec_lau.get(_mesto(lines[i + 1]))})
    h = pd.DataFrame(rows)
    assert h.lau.notna().all(), "obec bez okresu"
    h = pd.concat([h, pd.DataFrame({"rok": 2026, "lau": centra.obec_lau})])
    h.groupby(["rok", "lau"]).size().rename("pracovist").reset_index().to_csv(F_CENTRA_HIST, index=False)
    return [F_CENTRA_HIST]


def cekaci_doby():
    """Objednací lhůty pracovišť ze snímků mamo.cz (2013–2019): u každého pracoviště řádek „N dní“
    a „[údaj z D.M.RRRR]“, za nimi ulice, PSČ a obec. „bez objednání“ = 0 dní, „neuvedeno“ = prázdné."""
    import re
    obec_lau, _ = _obec_lau()
    rows = []
    for rok, lines in _snimky_mamocz():
        for i, s in enumerate(lines):
            d = re.fullmatch(r"\[údaj z (\d{1,2})\.(\d{1,2})\.(\d{4})\]", s)
            if not d:
                continue
            w = lines[i - 1]
            m = re.fullmatch(r"(\d+) (?:dní|dny|den)", w)
            dni = int(m.group(1)) if m else (0 if w == "bez objednání" else None)
            j = next(k for k in range(i + 1, i + 6) if re.fullmatch(r"\d{3} ?\d{2}", lines[k]))
            obec = _mesto(lines[j + 1])
            rows.append({"snimek": rok, "datum": f"{d.group(3)}-{int(d.group(2)):02d}-{int(d.group(1)):02d}",
                         "lau": obec_lau.get(obec), "obec": obec, "ulice": lines[j - 1],
                         "psc": lines[j].replace(" ", ""), "cekani_dni": dni, "text": w})
    t = pd.DataFrame(rows)
    assert t.lau.notna().all(), "obec bez okresu"
    assert len(t) > 400, len(t)
    t.to_csv(F_CEKANI, index=False)
    return [F_CEKANI]


def zabal(f):
    """data/<soubor> → data/<soubor>.zip (v repozitáři jsou jen zipy)."""
    with zipfile.ZipFile(f.with_name(f.name + ".zip"), "w", zipfile.ZIP_DEFLATED,
                         compresslevel=9) as z:
        z.write(f, arcname=f.name)


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    kroky = (prevence, covid, nrhzs, nrhzs_icz, nrpzs, nor, centra_historie, cekaci_doby)
    if "--jen" in sys.argv:                      # např. --jen nrhzs_icz
        kroky = [k for k in kroky if k.__name__ in sys.argv]
    for krok in kroky:
        for f in krok():
            if "--bez-zip" not in sys.argv:
                zabal(f)
            print(f"{f.relative_to(BASE)}: {f.stat().st_size / 1e6:.2f} MB")

"""Společné analytické kroky revizního a rozšiřujícího notebooku (mamograf_analyza, mamograf_rozsireni).

Věková standardizace pokrytí, test role krajů (permutace, ICC), prostorová dostupnost 2SFCA,
sousedství okresů a Moranovo I, křížová validace lineárních modelů a VIF.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.spatial import cKDTree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut, RepeatedKFold, cross_val_predict
from statsmodels.stats.outliers_influence import variance_inflation_factor

from utils import nacteni as nac

JADRO = ["50–54", "55–59", "60–64", "65–69"]
PREV3 = ["gyn_prevence_pct", "cytologie_pct", "toks_pct"]
DUSLEDKY = ["rakovina_prs_na1000", "nezhoubne_prs_na1000", "diag_prs_na100"]
M1 = ["vs_zeny_pct", "nezam_zeny_pct", "prisp_bydleni_Kc_obyv", "cizinky_pct", "obce_0_pct", "obce_4_pct"]


# ------------------------------------------------------------ věková standardizace

def pasma(D, roky=nac.ROKY_V):
    """Pokrytí po okresech a pásmech z počtů sečtených za roky (dvouleté okno mamografie)."""
    B = D[(D.band != nac.TOTAL) & D.rok.isin(roky)].copy()
    B["band"] = B.band.astype(str)
    B["mamo_2y_n"] = B.pocet_vysetreni + B.mamo_predchozi
    P = (B.groupby(["lau", "band"])
          .agg(mamo=("mamo_2y_n", "sum"), zeny=("zeny", "sum"),
               prev=("pocet_vysetrenych", "sum"), kapitace=("populace", "sum"))
          .reset_index())
    P["m"] = 100 * P.mamo / P.zeny
    P["p"] = 100 * P.prev / P.kapitace
    return P


def standard(P):
    """Věková skladba žen 45+ celé ČR (váhy pásem)."""
    w = P.groupby("band").zeny.sum().reindex(nac.BANDS)
    return w / w.sum()


def standardizuj(P, col, w, pasma_=nac.BANDS):
    ww = w[pasma_] / w[pasma_].sum()
    return P.pivot(index="lau", columns="band", values=col)[pasma_].mul(ww).sum(axis=1)


def pokryti(D, laus):
    """Tabulka S: hrubé, standardizované a 50–69 pokrytí mamografií, standardizovaná prevence u PL."""
    P = pasma(D)
    w = standard(P)
    S = pd.DataFrame({
        "m_hruby": P.groupby("lau").mamo.sum() / P.groupby("lau").zeny.sum() * 100,
        "m_std": standardizuj(P, "m", w),
        "m_5069": standardizuj(P, "m", w, JADRO),
        "p_std": standardizuj(P, "p", w),
    }).reindex(laus)
    return S, P, w


def rocni_std(D, w):
    """Roční věkově standardizované pokrytí mamografií (m1) a prevencí (p1) po okresech."""
    B = D[D.band != nac.TOTAL].copy()
    B["band"] = B.band.astype(str)
    B["m1"] = 100 * B.pocet_vysetreni.fillna(0) / B.zeny     # ÚZIS nulové buňky vynechává
    B["p1"] = 100 * B.pocet_vysetrenych / B.populace
    R = B.pivot_table(index=["lau", "rok"], columns="band", values=["m1", "p1"])
    return pd.DataFrame({c: R[c][nac.BANDS].mul(w).sum(axis=1, min_count=len(nac.BANDS))
                         for c in ("m1", "p1")}).reset_index()


def prev_index(X):
    """Index preventivního chování: průměr z-skóre gynekologie, cytologie a testu OK."""
    return X[PREV3].apply(lambda c: (c - c.mean()) / c.std()).mean(axis=1)


# ------------------------------------------------------------ kraje

def eta2(y, g):
    y = np.asarray(y, float)
    a = pd.DataFrame({"y": y, "g": g}).groupby("g").y.agg(["mean", "count"])
    return ((a["mean"] - y.mean()) ** 2 * a["count"]).sum() / ((y - y.mean()) ** 2).sum()


def icc_anova(y, g):
    '''ANOVA odhad vnitrotřídní korelace pro nevyvážené skupiny (záporný = 0).'''
    y = np.asarray(y, float)
    df = pd.DataFrame({"y": y, "g": g}); a = df.groupby("g").y
    n, k, ni = len(y), a.ngroups, a.count()
    msb = (ni * (a.mean() - y.mean()) ** 2).sum() / (k - 1)
    msw = ((y - a.transform("mean")) ** 2).sum() / (n - k)
    n0 = (n - (ni ** 2).sum() / n) / (k - 1)
    return max((msb - msw) / (msb + (n0 - 1) * msw), 0)


def kraj_test(y, kraje, rng, n_perm=5000):
    obs = eta2(y, kraje)
    nul = np.array([eta2(y, rng.permutation(kraje)) for _ in range(n_perm)])
    return {"η²": obs, "η² náhodou": nul.mean(), "p (permutace)": (1 + (nul >= obs).sum()) / (n_perm + 1),
            "ICC": icc_anova(y, kraje)}


# ------------------------------------------------------------ dostupnost (2SFCA)

def utlum(d, d0):
    w = (np.exp(-0.5 * (d / d0) ** 2) - np.exp(-0.5)) / (1 - np.exp(-0.5))
    return np.where(d <= d0, w, 0.0)


def sfca(dist, poptavka, d0, nabidka=None, nasobek=1e5):
    """2SFCA: dist = matice okres × pracoviště [km], poptávka = ženy v okresech,
    nabídka = kapacita pracovišť (výchozí 1 za pracoviště)."""
    s = np.ones(dist.shape[1]) if nabidka is None else np.asarray(nabidka, float)
    f = utlum(dist, d0)
    pj = np.asarray(poptavka, float) @ f
    rj = np.divide(s, pj, out=np.zeros_like(s, dtype=float), where=pj > 0)
    a = f @ rj
    assert np.isclose((a * np.asarray(poptavka, float)).sum(), s[pj > 0].sum())
    return nasobek * a


# ------------------------------------------------------------ prostor

def sousedstvi(GEO, laus, tol=0.004, min_bodu=2):
    '''Okresy jsou sousedé, když mají aspoň dva vrcholy hranice blíž než tol (°).
    Hranice jsou zjednodušené zvlášť pro každý okres, proto ne přesná shoda.'''
    body = {}
    for ft in GEO["features"]:
        g = ft["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        body[ft["id"]] = np.vstack([np.asarray(r) for p in polys for r in p])
    stromy = {l: cKDTree(body[l]) for l in laus}
    W = np.zeros((len(laus), len(laus)))
    for i, a in enumerate(laus):
        for j in range(i + 1, len(laus)):
            d, _ = stromy[laus[j]].query(body[a], distance_upper_bound=tol)
            if np.isfinite(d).sum() >= min_bodu:
                W[i, j] = W[j, i] = 1
    assert (W.sum(1) > 0).all(), "okres bez souseda"
    return W


def moran(y, W, rng, n_perm=999):
    WR = W / W.sum(1, keepdims=True)
    z = np.asarray(y, float) - np.mean(y)
    stat = lambda v: len(v) / WR.sum() * (v @ WR @ v) / (v @ v)
    I = stat(z)
    nul = np.array([stat(rng.permutation(z)) for _ in range(n_perm)])
    return I, (1 + (nul >= I).sum()) / (n_perm + 1), nul.mean()


# ------------------------------------------------------------ modely

def cv_r2(Z, y, n_rep=50):
    '''R² mimo vzorek: opakovaná 5násobná křížová validace (50×) a leave-one-out.'''
    Z, yv = np.asarray(Z, float), np.asarray(y, float)
    sst = ((yv - yv.mean()) ** 2).sum()
    ss = np.zeros(n_rep)
    for i, (tr, te) in enumerate(RepeatedKFold(n_splits=5, n_repeats=n_rep, random_state=0).split(Z)):
        m = LinearRegression().fit(Z[tr], yv[tr])
        ss[i // 5] += ((yv[te] - m.predict(Z[te])) ** 2).sum()
    loo = cross_val_predict(LinearRegression(), Z, yv, cv=LeaveOneOut())
    return 1 - ss.mean() / sst, 1 - ((yv - loo) ** 2).sum() / sst


def vif(df, cols):
    Z = sm.add_constant(df[cols].values)
    return pd.Series([variance_inflation_factor(Z, i) for i in range(1, Z.shape[1])], index=cols)


def ols_std(y, df, cols, cov_type="HC3"):
    '''OLS se standardizovanými prediktory (β = p. b. na 1 SD).'''
    Z = (df[cols] - df[cols].mean()) / df[cols].std()
    return sm.OLS(np.asarray(y, float), sm.add_constant(Z.values)).fit(cov_type=cov_type), Z


# ------------------------------------------------------------ small-area model (Fay–Herriot)

def fay_herriot(y, v, Xm, W, kraje):
    '''Fay–Herriot s prostorovým (Leroux CAR) a krajským náhodným efektem, odhad REML.

    y = Xβ + s + k + e;  s ~ N(0, σ_s² Q(λ)⁻¹), Q = λ(diag(W1) − W) + (1 − λ)I;
    k ~ N(0, σ_k²) po krajích;  e ~ N(0, v) se známým výběrovým rozptylem v.
    Vrací vyhlazené odhady θ = Xβ + s + k, jejich směrodatnou chybu (MSE g1 + g2,
    bez nejistoty parametrů rozptylu), β, parametry a „očekávanou“ hodnotu Xβ.'''
    from scipy.optimize import minimize
    y, v = np.asarray(y, float), np.asarray(v, float)
    Xm = np.c_[np.ones(len(y)), np.asarray(Xm, float)] if Xm is not None else np.ones((len(y), 1))
    Z = pd.get_dummies(pd.Series(kraje)).values.astype(float)
    L = np.diag(W.sum(1)) - W
    n = len(y)

    def G_of(th):
        s2, lam, k2 = np.exp(th[0]), 1 / (1 + np.exp(-th[1])), np.exp(th[2])
        Q = lam * L + (1 - lam) * np.eye(n)
        return s2 * np.linalg.inv(Q) + k2 * Z @ Z.T

    def nll(th):
        Vm = G_of(th) + np.diag(v)
        Vi = np.linalg.inv(Vm)
        XtVi = Xm.T @ Vi
        A = XtVi @ Xm
        beta = np.linalg.solve(A, XtVi @ y)
        r = y - Xm @ beta
        return 0.5 * (np.linalg.slogdet(Vm)[1] + np.linalg.slogdet(A)[1] + r @ Vi @ r)

    s0 = np.log(max(np.var(y) - v.mean(), 1e-3) / 2)
    opt = min((minimize(nll, np.array([s0, l0, s0]), method="Nelder-Mead",
                        options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-8}) for l0 in (-2.0, 0.0, 2.0)),
              key=lambda o: o.fun)
    G = G_of(opt.x)
    Vi = np.linalg.inv(G + np.diag(v))
    A = Xm.T @ Vi @ Xm
    beta = np.linalg.solve(A, Xm.T @ Vi @ y)
    ocek = Xm @ beta
    theta = ocek + G @ Vi @ (y - ocek)
    B = Xm - G @ Vi @ Xm
    mse = np.diag(G - G @ Vi @ G + B @ np.linalg.solve(A, B.T))
    par = {"σ_s²": np.exp(opt.x[0]), "λ": 1 / (1 + np.exp(-opt.x[1])), "σ_k²": np.exp(opt.x[2])}
    return theta, np.sqrt(mse), beta, par, ocek

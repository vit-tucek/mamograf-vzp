"""Sample size and power: analytic two-proportion formula with design effect, and a
generic simulation helper. Used by notebooks/vzp_segmentation_final.ipynb."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def analytic_n(p0: float, delta: float, alpha: float = 0.05, power: float = 0.8, ratio: float = 1.0,
               icc: float = 0.0, cluster_size: float = 1.0, n_comparisons: int = 1) -> dict:
    """Women per arm to detect p0 → p0+delta (two-sided), Bonferroni over comparisons,
    inflated by the design effect 1 + (m − 1)·ICC for cluster randomisation."""
    a = alpha / n_comparisons
    p1 = p0 + delta
    za, zb = stats.norm.ppf(1 - a / 2), stats.norm.ppf(power)
    pbar = (p0 + ratio * p1) / (1 + ratio)
    n0 = ((za * np.sqrt(pbar * (1 - pbar) * (1 + 1 / ratio)) + zb * np.sqrt(p0 * (1 - p0) + p1 * (1 - p1) / ratio))
          / delta) ** 2
    deff = 1 + (cluster_size - 1) * icc
    return {"n_kontrola": int(np.ceil(n0 * deff)), "n_intervence": int(np.ceil(n0 * deff * ratio)),
            "design_effect": deff, "alpha_na_srovnani": a}


def mde(n_per_arm: int, p0: float, alpha: float = 0.05, power: float = 0.8, icc: float = 0.0,
        cluster_size: float = 1.0) -> float:
    """Minimal detectable absolute difference (percentage points / 100)."""
    lo, hi = 1e-4, 0.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if analytic_n(p0, mid, alpha, power, icc=icc, cluster_size=cluster_size)["n_kontrola"] > n_per_arm:
            lo = mid
        else:
            hi = mid
    return hi


def power_curve(p0: float, deltas, n_grid, alpha: float = 0.05, icc: float = 0.0, cluster_size: float = 1.0
                ) -> pd.DataFrame:
    rows = []
    za = stats.norm.ppf(1 - alpha / 2)
    deff = 1 + (cluster_size - 1) * icc
    for d in deltas:
        p1 = p0 + d
        for n in n_grid:
            ne = n / deff
            se = np.sqrt(p0 * (1 - p0) / ne + p1 * (1 - p1) / ne)
            rows.append({"delta_pp": 100 * d, "n_na_rameno": n,
                         "sila": float(stats.norm.cdf(abs(d) / se - za))})
    return pd.DataFrame(rows)


def simulate_power(simulate_fn, analyze_fn, n_sims: int = 200, seed: int = 0) -> dict:
    """Generic simulation: simulate_fn(rng) → data; analyze_fn(data) → p-value.
    Returns rejection rate (power under an effect, type-I error under the null)."""
    rng = np.random.default_rng(seed)
    p = np.array([analyze_fn(simulate_fn(rng)) for _ in range(n_sims)])
    return {"zamitnuti": float((p < 0.05).mean()), "n_sims": n_sims}

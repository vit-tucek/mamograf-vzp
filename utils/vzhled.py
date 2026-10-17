"""Společný vzhled grafů (převzato z kap. 1 notebooku mamograf_exploration.ipynb)."""
import pandas as pd

# ---- barevné role (validovaná paleta, jeden odstín pro sekvenční škálu) ----
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6",
       "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
BLUES = [[i / (len(SEQ) - 1), c] for i, c in enumerate(SEQ)]

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
S1, S2 = "#2a78d6", "#eb6834"        # kategoriální sloty 1 a 2

# divergentní škála: červená (−) · neutrální šedá (0) · modrá (+), stejně kroků na rameni
DIV = [[0.00, "#7a1f1f"], [0.20, "#b93434"], [0.35, "#e34948"], [0.47, "#f3c7c4"],
       [0.50, "#f0efec"],
       [0.53, "#cde2fb"], [0.65, "#3987e5"], [0.80, "#1c5cab"], [1.00, "#0d366b"]]

FONT = dict(family="system-ui, -apple-system, Segoe UI, sans-serif",
            size=13, color=INK)


def layout(title, subtitle="", **kw):
    """Společné chrome pro všechny grafy: tenké linky, potlačená mřížka."""
    head = f"<b>{title}</b>"
    if subtitle:
        head += f'<br><span style="font-size:12px;color:{INK2}">{subtitle}</span>'
    base = dict(
        title=dict(text=head, x=0.01, xanchor="left", font=dict(size=17)),
        font=FONT, paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        margin=dict(l=40, r=20, t=80, b=50),
        hoverlabel=dict(bgcolor="white", bordercolor=AXIS,
                        font=dict(family=FONT["family"], size=12.5)),
        xaxis=dict(gridcolor=GRID, zeroline=False, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=GRID, zeroline=False, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(color=MUTED)),
    )
    base.update(kw)
    return base


# Rámec mapy: pevný výřez ČR je spolehlivější než fitbounds.
CR_LON, CR_LAT = [12.05, 18.90], [48.50, 51.10]


def mapa_geo(fig, right=0.92):
    fig.update_geos(fitbounds=False, visible=False, projection_type="mercator",
                    lonaxis_range=CR_LON, lataxis_range=CR_LAT, bgcolor=SURFACE,
                    domain=dict(x=[0, right], y=[0, 1]))


def skala(nazev, suffix=" %"):
    return dict(title=dict(text=nazev, side="top", font=dict(size=11, color=INK2)),
                thickness=12, len=0.72, x=0.97, xanchor="left", y=0.5,
                outlinewidth=0, ticksuffix=suffix,
                tickfont=dict(size=11, color=MUTED))


def cz(x, dec=1):
    """Číslo česky: desetinná čárka, mezera po tisících."""
    if pd.isna(x):
        return "–"
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")

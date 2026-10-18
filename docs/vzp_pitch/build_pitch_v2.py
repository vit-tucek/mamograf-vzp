"""Builds pitch v2 (stakes → solution → model → channels → result) on the v41 template, in two variants:

    python docs/vzp_pitch/build_pitch_v2.py        → pitch_v2.pptx        (7 segments A–G)
    python docs/vzp_pitch/build_pitch_v2.py 11     → pitch_v2_11seg.pptx  (11 segments)

The stakes and our result are based on VZP data (2024 invitations) and come from dopad.py (per-exam ratios of
the team's financial model, QALY from the stage-shift model); national ČSÚ, ÚZIS and NOR figures appear only
in the speaker notes as context. See dopad.py's docstring for every assumption.
"""
import sys

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import dopad
from pitch_common import (BLUE, BODY, CORAL, HERE, INK, LAYOUT, LIGHT, LILAC, LINE, MUTED, NAVY, PALE, SEGMENTS_NOTES,
                          WHITE, X0, XW, arrow, badges, box, channels_table, content_slide, new_deck, rgb,
                          segments_slide, set_notes, source, text)

SEG = int(sys.argv[1]) if len(sys.argv) > 1 else 7
assert SEG in (7, 11)
OUT = HERE / ("pitch_v2.pptx" if SEG == 7 else "pitch_v2_11seg.pptx")

R = dopad.compute()
CEIL, NAT, LO, HI = R["vzp_ceiling"], R["ceiling"], R["ours"]["low"], R["ours"]["high"]
VZP = dopad.VZP_2024


def cz(x, nd=0):
    """Czech number: space as thousands separator, comma as decimal separator."""
    return f"{x:,.{nd}f}".replace(",", " ").replace(".", ",")


def rnd(x, step):
    return round(x / step) * step


prs = new_deck()

# ---------------------------------------------------------------- 0 · cover (5 s)
s = prs.slides.add_slide(LAYOUT["TITUL"])
text(s, X0, 2.35, 9.5, 1.9, ["Mámo, graf!", "Od pozvánky k mamografu"], size=40, color=WHITE)
text(s, X0, 4.4, 9.5, 0.4, "Co je ve hře, jak to získat a kolik přineseme · Rakathon 2026 · výzva VZP", size=14,
     color="DAD8F2")
text(s, X0, 5.15, 3.2, 0.3, "Každé číslo stojí na třech zdrojích:", size=12, color="DAD8F2")
badges(s, ["Data VZP", "Literatura", "E-commerce"], x_left=X0 + 3.25, y=5.17)
set_notes(s, "5 s. Dobrý den, jsme Mámo, graf! z Weiner & Partners.")

# ---------------------------------------------------------------- 1 · what is at stake (40 s)
unscr = rnd(R["unscreened"], 10_000)
cancers = rnd(CEIL["cancers"], 100)
came = 1 - VZP["not_came"] / VZP["invited"]
s = content_slide(prs, "CO JE VE HŘE", f"U {cz(VZP['not_came'] / 1000)} tisíc pozvaných žen, které nepřišly, se nádory najdou pozdě",
                  f"V roce 2024 VZP adresně pozvala {cz(VZP['invited'])} žen, hlavně ty, které na screening dlouho nepřišly, "
                  f"a ženy zvané poprvé. Do 12 měsíců jich přišlo {cz(came * 100)} %. Kdyby přišly všechny, screening by ročně "
                  f"našel asi {cz(cancers)} karcinomů prsu dřív.")
badges(s, ["Data VZP", "Literatura"])
fun = [(cz(VZP["invited"]), "žen VZP v roce 2024 adresně pozvala (nechodí na screening nebo zvané poprvé)", NAVY),
       (f"{cz(came * 100)} %", "přišlo do 12 měsíců", BLUE),
       (cz(VZP["not_came"]), "žen nepřišlo", CORAL)]
y = 2.3
for i, (v, d, col) in enumerate(fun):
    box(s, X0, y, 3.35, 1.2)
    text(s, X0 + 0.2, y + 0.1, 2.95, 0.45, v, size=22, color=col, bold=True)
    text(s, X0 + 0.2, y + 0.58, 2.95, 0.6, d, size=10, color=BODY)
    if i < 2:
        a = arrow(s, X0 + 1.52, y + 1.22, 0.3)
        a.rotation = 90
    y += 1.5
cd = CategoryChartData()
cd.categories = ["dnes, bez screeningu", "při screeningu"]
cd.add_series("stadium I", (dopad.STAGE_OUT["I"] * 100, dopad.STAGE_IN["I"] * 100))
cd.add_series("stadium II–III", (dopad.STAGE_OUT["II–III"] * 100, dopad.STAGE_IN["II–III"] * 100))
cd.add_series("stadium IV", (dopad.STAGE_OUT["IV"] * 100, dopad.STAGE_IN["IV"] * 100))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED_100, Inches(4.45), Inches(2.25), Inches(4.35), Inches(4.2), cd)
ch = gf.chart
ch.has_title = True
ch.chart_title.text_frame.text = f"Stadium při diagnóze, ≈ {cz(cancers)} nádorů ročně (%)"
tp = ch.chart_title.text_frame.paragraphs[0]
tp.runs[0].font.size = Pt(11)
tp.runs[0].font.bold = False
tp.runs[0].font.color.rgb = rgb(BODY)
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(9.5)
ch.legend.font.color.rgb = rgb(BODY)
plot = ch.plots[0]
plot.gap_width = 45
plot.overlap = 100
plot.has_data_labels = True
plot.data_labels.number_format = '0.0'
plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.CENTER
plot.data_labels.font.size = Pt(10)
for ser, col, fg in zip(plot.series, (NAVY, LIGHT, CORAL), (WHITE, INK, WHITE)):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = rgb(col)
    dl = ser.data_labels                       # series-level labels replace the plot-level ones
    dl.show_value = ser.name != "stadium IV"   # 0,7 % is too thin for a label; stage IV goes in the note below
    dl.number_format = '0.0'
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.CENTER
    dl.font.color.rgb = rgb(fg)
    dl.font.size = Pt(10)
ch.value_axis.visible = False
ch.value_axis.has_major_gridlines = False
ch.category_axis.tick_labels.font.size = Pt(10)
ch.category_axis.tick_labels.font.color.rgb = rgb(BODY)
ch.category_axis.format.line.color.rgb = rgb(LINE)
text(s, 4.45, 6.47, 4.35, 0.25, f"stadium IV: {cz(dopad.STAGE_OUT['IV'] * 100, 1)} % → {cz(dopad.STAGE_IN['IV'] * 100, 1)} %",
     size=9.5, color=CORAL, bold=True, align=PP_ALIGN.CENTER)
box(s, 9.05, 2.25, 3.43, 4.45, fill=PALE)
text(s, 9.25, 2.35, 3.05, 0.55, ["**Kdyby přišly všechny**", "teoretický strop, ročně"], size=11, color=NAVY)
ceil = [(f"≈ {cz(cancers)}", "nádorů zachycených dřív"),
        (f"≈ {cz(rnd(CEIL['deaths'], 5))}", "odvrácených úmrtí (do 5 let od diagnózy)"),
        (f"≈ {cz(rnd(CEIL['qaly'], 10))}", "let života ve zdraví (QALY)"),
        (f"≈ {cz(rnd(CEIL['net_kc'] / 1e6, 10))} mil. Kč", "čistá úspora (léčba IV. stadia 3 mil. Kč)")]
for i, (v, d) in enumerate(ceil):
    yy = 3.0 + i * 0.92
    text(s, 9.25, yy, 3.05, 0.42, v, size=19, color=CORAL, bold=True)
    text(s, 9.25, yy + 0.42, 3.05, 0.42, d, size=9.5, color=BODY)
source(s, "Zdroj: data VZP pro Rakathon 2026, pozvánky 2024; stadia: audit screeningu 2023, ÚZIS 2022; finanční model týmu (docs/vzp_pitch/dopad.py)")
set_notes(s, (
    f"40 s. V roce 2024 VZP adresně pozvala {cz(VZP['invited'] / 1000)} tisíc žen, které na screening dlouho nepřišly nebo byly zvané poprvé, a {cz(VZP['not_came'] / 1000)} "
    f"tisíc z nich do roka nepřišlo. Kdyby přišly, screening by u nich ročně našel asi {cz(cancers)} karcinomů prsu dřív. Bez "
    "screeningu je v prvním stadiu necelá třetina nádorů, ve screeningu tři čtvrtiny. Kdyby přišly všechny, šlo by ročně o asi "
    f"{cz(rnd(CEIL['deaths'], 5))} odvrácených úmrtí, {cz(rnd(CEIL['qaly'], 10))} let života ve zdraví a {cz(rnd(CEIL['net_kc'] / 1e6, 10))} "
    "milionů korun čisté úspory. To je teoretický strop. "
    f"(Výpočet v docs/vzp_pitch/dopad.py, jedno vyšetření na ženu ročně. Kontext, nečíst: celostátně je {cz(R['women'] / 1e6, 2)} mil. "
    f"žen 45–74, za dva roky přišlo {cz(R['coverage'] * 100)} %, tedy nejméně {cz(unscr / 1000)} tisíc žen bez screeningu a asi "
    f"{cz(rnd(NAT['cancers'], 100))} nádorů ročně (ČSÚ, ÚZIS, NOR). Čistá úspora platí při ceně léčby IV. stadia 3 mil. Kč, pod "
    "1,9 mil. Kč vychází nula; náklady modelu zahrnují příspěvek 1 000 Kč na vyšetření, ověřit s týmem. Robustní metrika: "
    "0,26 mil. Kč za QALY.)"))

# ---------------------------------------------------------------- 2 · our solution (30 s)
s = content_slide(prs, "NAŠE ŘEŠENÍ", "Tři zdroje, segmentace klientek a nové měřitelné kanály",
                  "Každý zdroj odpovídá na jinou otázku. Dohromady určí, koho oslovit, čím a jak poznáme, že to funguje.")
inputs = [("Literatura", "Vědecká literatura", "co funguje: účinky intervencí z randomizovaných studií a metaanalýz"),
          ("Data VZP", "Statistický model", "kdo přijde: 1,34 mil. pozvánek VZP, vysvětlitelný model s AUC 0,83"),
          ("E-commerce", "Praxe z e-commerce", "jak doručit a změřit: kaskády zpráv, A/B testy, měření přírůstku")]
for i, (kind, h, d) in enumerate(inputs):
    y = 2.3 + i * 1.5
    box(s, X0, y, 3.9, 1.3)
    text(s, X0 + 0.2, y + 0.15, 2.4, 0.35, h, size=13, color=NAVY, bold=True)
    badges(s, [kind], x_right=X0 + 3.9 - 0.15, y=y + 0.16)
    text(s, X0 + 0.2, y + 0.58, 3.5, 0.65, d, size=10.5, color=BODY)
arrow(s, 4.95, 4.05, 0.45, color=BLUE)
box(s, 5.6, 3.15, 3.0, 2.1, fill=NAVY, line=None)
text(s, 5.8, 3.35, 2.6, 0.45, "Segmentace klientek", size=15, color=WHITE, bold=True)
text(s, 5.8, 3.85, 2.6, 1.3, f"{SEG} skupin podle vztahu k prevenci a stavu ve zvaní; pravidla nad poli VZP, ověřená na roce 2024",
     size=11, color="E6E4F7")
arrow(s, 8.8, 4.05, 0.45, color=BLUE)
box(s, 9.45, 3.15, 3.03, 2.1, fill=PALE)
text(s, 9.65, 3.35, 2.65, 0.45, "Nové měřitelné kanály", size=15, color=NAVY, bold=True)
text(s, 9.65, 3.85, 2.65, 1.3, "pevný termín, SMS, lékař, Moje VZP; každý s kontrolní skupinou a výsledkem z vykázaných výkonů",
     size=11, color=INK)
source(s, "Zdroj: docs/interventions.md a PAPERS.md; data VZP pro Rakathon 2026; zkušenost týmu z e-commerce")
set_notes(s, (
    "30 s. Naše řešení stojí na třech zdrojích. Z vědecké literatury víme, která opatření fungují a jak moc. Statistický model nad "
    "1,34 milionu pozvánek VZP ukáže, kdo přijde a kdo ne. Z e-commerce přinášíme způsob práce: segmentaci podle chování, "
    "automatické kaskády zpráv a A/B testy. Výsledkem je segmentace klientek a pro každý segment nový kanál, jehož účinek "
    "změříme proti kontrolní skupině."))

# ---------------------------------------------------------------- 3 · model (35 s)
s = segments_slide(prs, SEG)
set_notes(s, SEGMENTS_NOTES[SEG])

# ---------------------------------------------------------------- 4 · channels (35 s)
s = content_slide(prs, "NOVÉ KANÁLY", "Každý segment dostane kanál a opatření, které lze změřit",
                  "Opatření vybíráme z literatury podle toho, co ženě v segmentu brání; účinek ověříme proti kontrolní skupině.")
badges(s, ["Literatura", "E-commerce"])
channels_table(s, SEG)
box(s, 8.75, 2.25, 3.73, 4.06, fill=PALE)
text(s, 8.95, 2.4, 3.35, 0.35, "Jak měříme", size=13, color=CORAL, bold=True)
text(s, 8.95, 2.85, 3.35, 3.35, [
    "kontrolní skupina u každého kanálu: dostane dnešní dopis",
    "výsledek z vykázaných mamografií, ne z kliknutí",
    "A/B test jako v e-commerce: rozšíříme jen to, co prokazatelně funguje",
    "cena za mamografii navíc pro každý kanál"], size=12, color=INK, space_after=10, bullets=True)
source(s, "Zdroj: rozpětí účinku z RCT a metaanalýz (docs/interventions.md), přenos do ČR je náš úsudek; data VZP 2024")
set_notes(s, (
    "35 s. Každý segment dostane kanál, kterým ho zastihneme, a opatření, které podle studií funguje. Prvním pozvaným a vypadlým "
    "pevný termín místo otevřené pozvánky: plus deset až devatenáct bodů. Ženám u gynekologa nebo praktika oslovení přes lékaře. "
    "Nedávno vyšetřeným dopis neposíláme. Každý kanál je měřitelný: kontrolní skupina dostane dnešní dopis a výsledek čteme "
    "z vykázaných mamografií."))

# ---------------------------------------------------------------- 5 · result (40 s)
lo_k, hi_k = LO["exams"] / 1000, HI["exams"] / 1000
s = content_slide(prs, "NÁŠ VÝSLEDEK", f"Cílenými kanály získáme {cz(lo_k)}–{cz(hi_k)} tisíc mamografií ročně",
                  "Počítáme jen s ženami, které VZP v roce 2024 pozvala a nepřišly, a s rozpětím účinku ze studií. "
                  "Skutečný účinek ověří pilot.")
badges(s, ["Data VZP", "Literatura"])
steps = [("207 tis.", "pozvaných žen nepřišlo (VZP 2024)", CORAL),
         ("159 tis.", "z nich v segmentech B–E s kanálem s doloženým účinkem", NAVY),
         (f"+{cz(lo_k)}–{cz(hi_k)} tis.", "mamografií navíc ročně", BLUE)]
bw, gap = 3.55, 0.49
for i, (v, d, col) in enumerate(steps):
    x = X0 + i * (bw + gap)
    box(s, x, 2.25, bw, 1.3)
    text(s, x + 0.2, 2.35, bw - 0.4, 0.5, v, size=22, color=col, bold=True)
    text(s, x + 0.2, 2.88, bw - 0.4, 0.6, d, size=10.5, color=BODY)
    if i < 2:
        arrow(s, x + bw + 0.09, 2.75, 0.31)
mets = [(f"{cz(LO['cancers'])}–{cz(HI['cancers'])}", "nádorů zachycených dřív ročně"),
        (f"{cz(LO['deaths'])}–{cz(HI['deaths'])}", "odvrácených úmrtí ročně"),
        (f"{cz(LO['qaly'])}–{cz(HI['qaly'])}", "let života ve zdraví (QALY) ročně"),
        (f"+{cz(LO['net_kc'] / 1e6, 1)}–{cz(HI['net_kc'] / 1e6, 1)} mil.", "Kč čisté úspory ročně")]
mw, mg = 2.75, 0.21
for i, (v, d) in enumerate(mets):
    x = X0 + i * (mw + mg)
    box(s, x, 3.8, mw, 1.25, fill=PALE)
    text(s, x + 0.18, 3.9, mw - 0.36, 0.5, v, size=18, color=NAVY, bold=True)
    text(s, x + 0.18, 4.42, mw - 0.36, 0.55, d, size=10.5, color=BODY)
lo_s, hi_s = R["share_of_vzp_ceiling"]
box(s, X0, 5.3, XW, 1.4, fill=WHITE)
text(s, X0 + 0.25, 5.42, 7.2, 1.2, [
    f"**{cz(lo_s * 100)}–{cz(hi_s * 100)} % teoretického stropu**, jen z cílených kanálů v segmentech B–E. Plošná digitální kaskáda "
    "podle finančního modelu přinese 156 mil. Kč čistě za 2027–2031.",
    "Úspora platí při léčbě IV. stadia za 3 mil. Kč; nákladová efektivita 0,26 mil. Kč za QALY (práh SÚKL 1,2 mil.)."],
    size=10.5, color=BODY, space_after=4)
box(s, 8.35, 5.42, 3.95, 1.16, fill=NAVY, line=None)
text(s, 8.55, 5.5, 3.6, 1.0, ["**Nabízíme VZP pilot s randomizací**", "model, segmenty i kód předáme · jakub@weiner.cz"],
     size=11, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, space_after=3)
source(s, "Zdroj: data VZP 2024; docs/interventions.md; finanční model týmu 16. 10. 2026; model posunu stadia (docs/vzp_pitch/dopad.py)")
set_notes(s, (
    f"40 s. Náš výsledek. Z 207 tisíc žen, které v roce 2024 nepřišly, je 159 tisíc v segmentech B až E, kde máme kanál s doloženým "
    f"účinkem. Podle rozpětí ze studií získáme {cz(lo_k)} až {cz(hi_k)} tisíc mamografií ročně. To je {cz(LO['cancers'])} až "
    f"{cz(HI['cancers'])} nádorů zachycených dřív, {cz(LO['deaths'])} až {cz(HI['deaths'])} odvrácených úmrtí, {cz(LO['qaly'])} až "
    f"{cz(HI['qaly'])} let života ve zdraví a {cz(LO['net_kc'] / 1e6)} až {cz(HI['net_kc'] / 1e6)} milionů korun čisté úspory ročně. "
    "Plošná digitální kaskáda by podle finančního modelu přinesla víc. Nabízíme VZP pilot s randomizací, model i kód předáme. "
    "Děkujeme. (Mamografie navíc: B+C 66 037 žen × 10–19 p. b., D+E 140 398 žen × 2–6 p. b.; metriky na 1 000 vyšetření "
    "z finančního modelu a modelu posunu stadia, viz dopad.py.)"))

prs.save(OUT)
print("written", OUT, len(prs.slides), "slides")

"""Builds the 3-minute final pitch (6 slides) on the v41 deck's own template, in two variants:

    python docs/vzp_pitch/build_pitch.py        → pitch_3min.pptx        (7 segments A–G)
    python docs/vzp_pitch/build_pitch.py 11     → pitch_3min_11seg.pptx  (11 segments, A–G split further)

The template is docs/sources/Mamo_graf_VZP_v41.pptx: its slides are dropped and new ones are added
from its layouts "TITUL" and "OBSAH", so the pitch keeps the W&P look (Poppins, navy palette, logo,
footers). Numbers and where they come from:
- 2024 invitations: 256 466 women, 49 265 came within 12 months (19 %), 207 201 did not; attendance by
  invitation order 52,7 → 5,3 %; 46 % of non-attenders got their 8th+ invitation; preventive gynaecology
  63 % (45–49) → 17 % (70–74) of all women invited in 2024. All from data_vzp/Rakhaton2026.csv.gz.
- Segments A–G: A screening < 24 months ago, B first invitation, C screening within 5 years,
  D preventive gynaecology (24 months), E other prevention (other screening 36 m., dentist or GP check-up
  24 m.), F at least one healthcare contact in 12 months, G none. Score = segment attendance 2020–2023,
  AUC on 2024 = 0,789. Logistic regression AUC 0,83 is the team's model from the v41 deck.
- 11 segments: config/segments_vzp_v2.yaml and notebooks/vzp_segmentation_final.ipynb (2024 table in
  outputs/vzp_segmentation_final/segmenty_2024.csv); AUC of the segment score on 2024 = 0,807.
- Effect ranges: docs/interventions.md. Extra mammographies, QALY and costs: see docs/vzp_pitch/build_slides.js.
"""
import sys

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.util import Inches, Pt

from pitch_common import (BLUE, BODY, CORAL, HERE, INK, LINE, NAVY, PALE, WHITE, X0, MUTED, LAYOUT, SEGMENTS_NOTES,
                          arrow, badges, box, channels_table, content_slide, new_deck, rgb, segments_slide, set_notes,
                          source, stat, text)

SEG = int(sys.argv[1]) if len(sys.argv) > 1 else 7
assert SEG in (7, 11)
OUT = HERE / ("pitch_3min.pptx" if SEG == 7 else "pitch_3min_11seg.pptx")

prs = new_deck()

# ---------------------------------------------------------------- 1 · title (10 s)
s = prs.slides.add_slide(LAYOUT["TITUL"])
text(s, X0, 2.35, 9.5, 1.9, ["Mámo, graf!", "Od pozvánky k mamografu"], size=40, color=WHITE)
text(s, X0, 4.4, 9.5, 0.4, "Komu, čím a s jakým dopadem · Rakathon 2026 · výzva VZP", size=14, color="DAD8F2")
text(s, X0, 5.15, 3.2, 0.3, "Každé číslo stojí na třech zdrojích:", size=12, color="DAD8F2")
badges(s, ["Data VZP", "Literatura", "E-commerce"], x_left=X0 + 3.25, y=5.17)
set_notes(s, (
    "10 s. Dobrý den, jsme tým Mámo, graf! z Weiner & Partners. Za tři minuty ukážeme, komu, čím a s jakým dopadem "
    "pomoci k mamografu. Každé číslo stojí na datech VZP, na vědecké literatuře a na naší zkušenosti z e-commerce."))

# ---------------------------------------------------------------- 2 · problem (25 s)
s = content_slide(prs, "PROBLÉM", "Každý rok 207 tisíc pozvaných žen na mamograf nepřijde",
                  "V roce 2024 VZP pozvala 256 466 žen, do 12 měsíců přišlo 19 %. S každou další pozvánkou účast klesá; "
                  "další stejný dopis přináší málo.")
badges(s, ["Data VZP"])
cd = CategoryChartData()
cd.categories = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8. a další"]      # pořadí pozvánky
cd.add_series("Účast do 12 měsíců (%)", (52.7, 32.1, 24.4, 18.4, 14.8, 12.9, 9.9, 5.3))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(X0), Inches(2.3), Inches(7.9), Inches(4.4), cd)
ch = gf.chart
ch.has_legend = False
ch.has_title = True
ch.chart_title.text_frame.text = "Účast do 12 měsíců podle pořadí pozvánky, 2024 (%)"
tp = ch.chart_title.text_frame.paragraphs[0]
tp.runs[0].font.size = Pt(11)
tp.runs[0].font.bold = False
tp.runs[0].font.color.rgb = rgb(BODY)
plot = ch.plots[0]
plot.gap_width = 55
plot.has_data_labels = True
plot.data_labels.number_format = "0.0"
plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(10)
plot.data_labels.font.color.rgb = rgb(INK)
ser = plot.series[0]
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = rgb(BLUE)
pt = ser.points[0]
pt.format.fill.solid()
pt.format.fill.fore_color.rgb = rgb(NAVY)
ch.value_axis.visible = False
ch.value_axis.has_major_gridlines = False
ch.category_axis.tick_labels.font.size = Pt(10)
ch.category_axis.tick_labels.font.color.rgb = rgb(BODY)
ch.category_axis.format.line.color.rgb = rgb(LINE)
stat(s, 9.05, 2.3, 3.43, 1.35, "207 201", "žen do 12 měsíců nepřišlo, 81 % pozvaných", color=CORAL)
stat(s, 9.05, 3.8, 3.43, 1.35, "46 %", "nepřišlých dostalo už osmou nebo další pozvánku", color=NAVY)
stat(s, 9.05, 5.3, 3.43, 1.4, "63 % → 17 %", "žen s preventivní gynekologií ve věku 45–49 vs. 70–74 let", color=BLUE)
source(s, "Zdroj: data VZP pro Rakathon 2026, pozvánky 2024 (256 466 žen); naše analýza")
set_notes(s, (
    "25 s. V roce 2024 VZP pozvala 256 tisíc žen a 207 tisíc z nich do roka nepřišlo. Po první pozvánce přijde polovina žen, "
    "po osmé jen pět procent, a téměř polovina nepřišlých už osmou pozvánku dostala. Další stejný dopis tedy nepomůže. "
    "A s věkem mizí preventivní gynekologie, hlavní cesta k mamografu: ze 63 na 17 procent."))

# ---------------------------------------------------------------- 3 · where the segments come from (35 s)
s = segments_slide(prs, SEG)
set_notes(s, SEGMENTS_NOTES[SEG])

# ---------------------------------------------------------------- 4 · how we use them (35 s)
s = content_slide(prs, "JAK SEGMENTY POUŽÍVÁME", "Každý segment dostane svůj kanál a opatření",
                  "Opatření vybíráme z literatury podle toho, co ženě v segmentu brání. Z e-commerce víme, jak je doručit a změřit.")
badges(s, ["Literatura", "E-commerce"])
channels_table(s, SEG)
box(s, 8.75, 2.25, 3.73, 4.06, fill=PALE)
text(s, 8.95, 2.4, 3.35, 0.35, "Co přinášíme z e-commerce", size=13, color=CORAL, bold=True)
text(s, 8.95, 2.85, 3.35, 3.35, [
    "segmentace podle chování, ne podle demografie",
    "automatické kaskády zpráv spuštěné událostí",
    "A/B test s kontrolní skupinou u každé změny",
    "měříme přírůstek (uplift), ne kliknutí",
    "cena za konverzi → cena za mamografii navíc"], size=12, color=INK, space_after=10, bullets=True)
source(s, "Zdroj: rozpětí účinku z RCT a metaanalýz (docs/interventions.md), přenos do ČR je náš úsudek; data VZP 2024")
set_notes(s, (
    "35 s. Jak je používáme? Každý segment dostane kanál, kterým ho zastihneme, a opatření, které podle studií funguje. "
    "Prvním pozvaným a vypadlým pevný termín místo otevřené pozvánky: v anglických studiích plus deset až devatenáct bodů. Ženám "
    "u gynekologa nebo praktika oslovení přes lékaře. Nedávno vyšetřeným dopis neposíláme vůbec. Z e-commerce přinášíme "
    "způsob práce: automatické kaskády zpráv, A/B test s kontrolní skupinou u každé změny a měření skutečného přírůstku, "
    "ne kliknutí."))

# ---------------------------------------------------------------- 5 · how we estimate impact (40 s)
s = content_slide(prs, "DOPAD", "Dopad počítáme ve třech krocích a ověříme ho experimentem",
                  "Každý krok má svůj zdroj: kolik žen je v segmentu, o kolik víc jich podle studií přijde a co to znamená "
                  "pro zdraví a náklady.")
KOLIK = ("pozvaných ročně v segmentech B–E: B+C 66 tis., D+E 140 tis." if SEG == 7 else
         "pozvaných ročně v B1–E2: 1. pozvánky a vypadlé 66 tis., gynekolog a jiná prevence 140 tis.")
steps = [("Kolik žen", "206 tis.", KOLIK, "Data VZP", NAVY),
         ("O kolik víc přijde", "+2–19 p. b.", "rozpětí účinku opatření z randomizovaných studií a metaanalýz", "Literatura", BLUE),
         ("Mamografie navíc", "9–21 tis.", "ročně: dolní a horní mez rozpětí účinku", None, NAVY),
         ("Zdraví a náklady", "36–80 QALY", "a 5–11 odvrácených úmrtí ročně; 0,26 mil. Kč za QALY (práh SÚKL 1,2 mil.)", "Literatura", CORAL)]
bw, gap = 2.62, 0.38
for i, (h, v, d, kind, col) in enumerate(steps):
    x = X0 + i * (bw + gap)
    box(s, x, 2.3, bw, 2.25)
    text(s, x + 0.2, 2.42, bw - 0.4, 0.3, f"{i + 1} · {h}", size=11, color=MUTED, bold=True)
    text(s, x + 0.2, 2.78, bw - 0.4, 0.5, v, size=22, color=col, bold=True)
    text(s, x + 0.2, 3.35, bw - 0.4, 0.8, d, size=10.5, color=BODY)
    if kind:
        badges(s, [kind], x_left=x + 0.2, y=4.15)
    if i < 3:
        arrow(s, x + bw + 0.05, 3.28, 0.28)
box(s, X0, 4.8, 6.35, 1.9, fill=PALE)
text(s, X0 + 0.2, 4.92, 4.6, 0.3, "Ověření experimentem", size=12, color=NAVY, bold=True)
badges(s, ["E-commerce"], x_right=X0 + 6.35 - 0.15, y=4.94)
text(s, X0 + 0.2, 5.3, 5.95, 1.35,
     "Ženy v segmentech B–E náhodně rozdělíme: kontrola dostane dnešní dopis, ramena nová opatření. Výsledek měříme "
     "vykázanými mamografiemi a vyhodnotíme podle přidělení. Jako A/B test v e-commerce: rozšíříme jen to, co prokazatelně funguje.",
     size=10.5, color=INK)
box(s, 7.45, 4.8, 5.03, 1.9, fill=WHITE)
text(s, 7.65, 4.92, 4.65, 0.3, "Čistý přínos v hodnotě zdraví", size=12, color=NAVY, bold=True)
text(s, 7.65, 5.25, 4.65, 0.5, "34–75 mil. Kč ročně", size=20, color=CORAL, bold=True)
text(s, 7.65, 5.8, 4.65, 0.85,
     "při prahu 1,2 mil. Kč za QALY. Horní scénář finančního modelu digitální kaskády: 86–237 mil. Kč čistě za 2027–2031.",
     size=10, color=BODY)
source(s, "Zdroj: data VZP 2024; docs/interventions.md; model posunu stadia (docs/ZJISTENI.md, věk 45–74); finanční model 16. 10. 2026")
set_notes(s, (
    "40 s. Jak odhadujeme dopad? Ve třech krocích. Vezmeme počet žen v segmentu z dat VZP, v segmentech B až E jich je 206 tisíc. "
    "Vynásobíme rozpětím účinku z randomizovaných studií. Vyjde devět až jednadvacet tisíc mamografií navíc ročně. Model posunu "
    "stadia z toho udělá 36 až 80 let života ve zdraví a pět až jedenáct odvrácených úmrtí ročně, za 260 tisíc korun na rok ve "
    "zdraví, hluboko pod prahem SÚKL. A protože literatura je jen odhad, ověříme to experimentem proti dnešnímu dopisu, přesně "
    "jako A/B test. (Výpočet: B+C 66 037 žen × 10–19 p. b. a D+E 140 398 žen × 2–6 p. b.; 3,82 QALY na 1 000 mamografií, "
    "993 Kč na mamografii včetně léčby, 1 945 mamografií na odvrácené úmrtí.)"))

# ---------------------------------------------------------------- 6 · close (30 s)
s = prs.slides.add_slide(LAYOUT["TITUL"])
text(s, X0, 1.25, 7.8, 0.8, "Co přinášíme VZP", size=34, color=WHITE)
cols = [("Máme", ["1,34 mil. pozvánek a okresní data ČR", "vysvětlitelný model účasti (AUC 0,83)",
                  f"{SEG} segmentů z dat, ověřených na roce 2024", "opatření z literatury pro každý segment"]),
        ("Nabízíme", ["pilot v segmentech B–E s randomizací", "pevný termín + SMS a lékař jako kanál",
                      "Moje VZP: rezervace, dotazník bariér", "model, segmenty i kód předáme"]),
        ("Přineseme", ["9–21 tis. mamografií navíc ročně", "36–80 QALY a 5–11 odvrácených úmrtí ročně",
                       "0,26 mil. Kč za QALY", "34–75 mil. Kč ročně v hodnotě zdraví"])]
cw, cg = 2.45, 0.2           # three columns end at x ≈ 8.6, left of the layout's decorative shapes
for i, (h, items) in enumerate(cols):
    x = X0 + i * (cw + cg)
    text(s, x, 2.3, cw, 0.4, h, size=16, color=WHITE, bold=True)
    text(s, x, 2.8, cw, 2.7, items, size=11.5, color="E6E4F7", space_after=7, bullets=True)
text(s, X0, 5.55, 10.0, 0.75, ["Jakub Weiner", "jakub@weiner.cz · +420 602 307 893 · www.weinerpartners.cz"], size=13,
     color=WHITE, bold=True)
set_notes(s, (
    "30 s. Shrnuto: máme model, " + ("sedm" if SEG == 7 else "jedenáct") + " segmentů a opatření pro každý z nich. Nabízíme VZP pilot s randomizací v segmentech B až E "
    "v rámci řízeného vstupu inovací; model, segmenty i návrh experimentu předáme včetně kódu. Výsledkem může být až dvacet "
    "tisíc mamografií ročně navíc a desítky let života ve zdraví. Děkujeme."))

prs.save(OUT)
print("written", OUT, len(prs.slides), "slides")

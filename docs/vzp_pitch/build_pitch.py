"""Builds pitch_3min.pptx: the 3-minute final pitch (6 slides), on the v41 deck's own template.

    python docs/vzp_pitch/build_pitch.py        (needs python-pptx)

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
- Effect ranges: docs/interventions.md. Extra mammographies, QALY and costs: see docs/vzp_pitch/build_slides.js.
"""
import copy
import re
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
TEMPLATE = HERE.parent / "sources" / "Mamo_graf_VZP_v41.pptx"
OUT = HERE / "pitch_3min.pptx"

NAVY, BLUE, LIGHT, CORAL, LILAC = "003B7A", "3D7CC9", "A9C6EA", "D27869", "7A78C3"
INK, BODY, MUTED, LINE, PALE, WHITE = "230F3C", "4A4458", "8A8597", "DEDCEC", "F7F6FB", "FFFFFF"
BADGE = {"Data VZP": NAVY, "Literatura": BLUE, "E-commerce": CORAL}
X0, XW = 0.85, 11.63          # content left edge and width (as in v41)


def nb(s):
    """Czech typography as in v41: non-breaking spaces before units, inside numbers, after one-letter words."""
    s = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", s)
    s = re.sub(r" (%|p\. b\.|tis\.|mil\.|Kč|let|měs\.)", "\u00a0\\1", s)
    s = re.sub(r"(?<![\w])([vkszouaiVKSZOUAI]) ", "\\1\u00a0", s)
    return s.replace("p. b.", "p.\u00a0b.")


def rgb(h):
    return RGBColor.from_string(h)


def plain(shape):
    """Drop the theme style python-pptx adds to auto shapes (outline, shadow), so fill and line are ours."""
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)
    return shape


def text(slide, x, y, w, h, content, size=13, color=BODY, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space_after=0, bullets=False):
    """Text box; content is a string or a list of paragraphs; **bold** marks bold runs."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = content if isinstance(content, list) else [content]
    for i, ptext in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        if bullets:
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(int(Inches(0.18))))
            pPr.set("indent", str(-int(Inches(0.18))))
            bu = pPr.makeelement(qn("a:buChar"), {"char": "•"})
            pPr.append(bu)
        for j, part in enumerate(re.split(r"(\*\*[^*]+\*\*)", nb(ptext))):
            if not part:
                continue
            r = p.add_run()
            r.text = part[2:-2] if part.startswith("**") else part
            r.font.size = Pt(size)
            r.font.bold = bold or part.startswith("**")
            r.font.color.rgb = rgb(color)
    return tb


def box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=0.06):
    s = plain(slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)))
    s.adjustments[0] = radius
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(0.75)
    else:
        s.line.fill.background()
    return s


def badges(slide, kinds, x_right=X0 + XW, y=0.5, x_left=None):
    """Source badges (Data VZP / Literatura / E-commerce): right-aligned on the kicker row, or from x_left."""
    widths = [0.25 + 0.085 * len(k) for k in kinds]
    x = x_left if x_left is not None else x_right - sum(widths) - 0.08 * (len(kinds) - 1)
    for k, w in zip(kinds, widths):
        b = box(slide, x, y, w, 0.27, fill=BADGE[k], line=None, radius=0.5)
        tf = b.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = k
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = rgb(WHITE)
        x += w + 0.08


def stat(slide, x, y, w, h, value, desc, color=NAVY, kind=None):
    box(slide, x, y, w, h)
    text(slide, x + 0.22, y + 0.12, w - 0.44, 0.55, value, size=22, color=color, bold=True)
    text(slide, x + 0.22, y + 0.66, w - 0.44, h - 0.78, desc, size=10.5, color=BODY)


def source(slide, s):
    text(slide, 2.30, 6.88, 9.30, 0.30, s, size=9, color=MUTED)


def table(slide, x, y, w, col_w, rows, row_h=0.36, size=10.5, bold_rows=(), highlight_col=None):
    gf = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows)))
    tbl = gf.table
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        tbl.rows[i].height = Inches(row_h)
        for j, val in enumerate(r):
            c = tbl.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.08)
            c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(NAVY if i == 0 else (PALE if i % 2 == 0 else WHITE))
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 or (highlight_col is not None and j == 1) else PP_ALIGN.RIGHT
            for part in re.split(r"(\*\*[^*]+\*\*)", nb(str(val))):
                if not part:
                    continue
                run = p.add_run()
                run.text = part[2:-2] if part.startswith("**") else part
                run.font.size = Pt(size)
                run.font.bold = i == 0 or i in bold_rows or part.startswith("**")
                run.font.color.rgb = rgb(WHITE if i == 0 else INK)
    return gf


def arrow(slide, x, y, w=0.3):
    a = plain(slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(0.3)))
    a.fill.solid()
    a.fill.fore_color.rgb = rgb(LIGHT)
    a.line.fill.background()


def set_notes(slide, note):
    ns = slide.notes_slide
    if ns.notes_text_frame is None:
        ns.shapes._spTree.append(copy.deepcopy(NOTES_BODY))
    tf = ns.notes_text_frame
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    tf.text = note


def content_slide(prs, kicker, title, intro=None):
    s = prs.slides.add_slide(LAYOUT["OBSAH"])
    for ph in s.placeholders:
        if ph.placeholder_format.idx == 101:
            ph.text_frame.text = kicker
        elif ph.placeholder_format.idx == 102:
            ph.text_frame.text = nb(title)
    if intro:
        text(s, X0, 1.62, XW, 0.5, intro, size=13, color=BODY)
    return s


# ---------------------------------------------------------------- template
prs = Presentation(TEMPLATE)
# the template's notes master has no body placeholder, so new notes slides would have no text frame:
# keep a copy of the notes body placeholder from an existing slide and reuse it
NOTES_BODY = copy.deepcopy(next(sh for sh in prs.slides[0].notes_slide.placeholders
                                if sh.placeholder_format.type == 2)._element)
ids = prs.slides._sldIdLst
for sid in list(ids):
    prs.part.drop_rel(sid.rId)
    ids.remove(sid)
LAYOUT = {l.name: l for l in prs.slide_layouts}

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
s = content_slide(prs, "ODKUD SEGMENTY", "Tři otázky nad daty VZP rozdělí ženy do sedmi skupin",
                  "Pravidla stojí jen na polích, která VZP poskytla. Pořadí otázek je priorita: žena patří do první skupiny, "
                  "jejíž podmínka platí.")
badges(s, ["Data VZP"])
qs = [("1 · Historie screeningu", ["**A** screening před méně než 24 měs.", "**B** první pozvánka", "**C** screening v posledních 5 letech"]),
      ("2 · Prevence", ["**D** preventivní gynekologie", "**E** jiná prevence: zubař, praktik, jiný screening"]),
      ("3 · Kontakt se zdravotnictvím", ["**F** aspoň jedna návštěva lékaře za rok", "**G** žádný kontakt"])]
y = 2.25
for q, items in qs:
    h = 0.55 + 0.3 * len(items)
    box(s, X0, y, 4.35, h, fill=PALE)
    text(s, X0 + 0.2, y + 0.14, 4.0, 0.3, q, size=12, color=NAVY, bold=True)
    text(s, X0 + 0.2, y + 0.5, 4.0, h - 0.55, items, size=11, color=INK, space_after=3)
    y += h + 0.2
table(s, 5.45, 2.25, 7.03, [3.13, 1.3, 1.3, 1.3], [
    ["Segment", "Ženy 2024", "Účast 12 měs.", "Nepřišlo"],
    ["A nedávno vyšetřená", "7 600", "2 %", "7 418"],
    ["B první pozvánka", "37 460", "55 %", "16 820"],
    ["C vypadlá z rytmu", "28 577", "33 %", "19 111"],
    ["D bez screeningu, gynekolog", "51 047", "21 %", "40 573"],
    ["E bez screeningu, jiná prevence", "89 351", "8 %", "82 559"],
    ["F jen léčebná péče", "28 368", "5 %", "26 977"],
    ["G mimo péči", "14 063", "2 %", "13 743"],
    ["Celkem", "256 466", "19 %", "207 201"],
], row_h=0.34, bold_rows=(8,))
box(s, 5.45, 5.5, 7.03, 0.95, fill=WHITE)
text(s, 5.65, 5.6, 6.65, 0.8, [
    "**Ověřeno na novém roce:** pravidla z let 2020–2023, test na 2024. Samotné segmenty seřadí ženy s AUC 0,79, "
    "celý vysvětlitelný model 0,83.",
    "Segmenty jsou stabilní pět let; jemnější verze s 11 segmenty slouží k cílení."], size=10.5, color=BODY, space_after=3)
source(s, "Zdroj: data VZP pro Rakathon 2026, pozvánky 2020–2024; naše analýza")
set_notes(s, (
    "35 s. Odkud segmenty? Ze tří otázek nad daty, která VZP poskytla. Zaprvé historie screeningu: nedávno vyšetřená, první "
    "pozvánka, nebo vypadla z rytmu. Zadruhé, chodí na jinou prevenci, ke gynekologovi nebo k zubaři a praktikovi? Zatřetí, je "
    "vůbec v kontaktu se zdravotnictvím? Tak vznikne sedm skupin s účastí od 2 do 55 procent. Pravidla jsme stanovili na letech "
    "2020 až 2023 a otestovali na roce 2024: segmenty seřadí ženy skoro stejně dobře jako celý model. "
    "(AUC segmentů 0,789 je přepočet z dat; AUC 0,83 logistické regrese je model týmu z prezentace v41.)"))

# ---------------------------------------------------------------- 4 · how we use them (35 s)
s = content_slide(prs, "JAK SEGMENTY POUŽÍVÁME", "Každý segment dostane svůj kanál a opatření",
                  "Opatření vybíráme z literatury podle toho, co ženě v segmentu brání. Z e-commerce víme, jak je doručit a změřit.")
badges(s, ["Literatura", "E-commerce"])
table(s, X0, 2.25, 7.65, [2.1, 3.95, 1.6], [
    ["Segment", "Kanál a opatření", "Účinek (p. b.)"],
    ["A nedávno vyšetřená", "nezvat, ověřit výkony těsně před odesláním", "úspora 7 600 dopisů"],
    ["B první pozvánka", "pevný termín v pozvánce + SMS připomínka", "**+10 až +19**"],
    ["C vypadlá z rytmu", "dřívější připomínka s termínem (25.–36. měsíc)", "+2 až +6"],
    ["D gynekolog", "seznam žen bez mamografie pro gynekologa, objednání v ordinaci", "+2 až +6"],
    ["E jiná prevence", "praktik jako nový kanál: seznam žen, upozornění při prohlídce", "+2 až +6"],
    ["F, G", "zatím ne: nízká účast a nejistý účinek", "–"],
], row_h=0.58, highlight_col=1)
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
    "Prvním pozvaným pevný termín místo otevřené pozvánky: v anglických studiích plus deset až devatenáct bodů. Ženám "
    "u gynekologa nebo praktika oslovení přes lékaře. Nedávno vyšetřeným dopis neposíláme vůbec. Z e-commerce přinášíme "
    "způsob práce: automatické kaskády zpráv, A/B test s kontrolní skupinou u každé změny a měření skutečného přírůstku, "
    "ne kliknutí."))

# ---------------------------------------------------------------- 5 · how we estimate impact (40 s)
s = content_slide(prs, "DOPAD", "Dopad počítáme ve třech krocích a ověříme ho experimentem",
                  "Každý krok má svůj zdroj: kolik žen je v segmentu, o kolik víc jich podle studií přijde a co to znamená "
                  "pro zdraví a náklady.")
steps = [("Kolik žen", "206 tis.", "pozvaných ročně v segmentech B–E: B+C 66 tis., D+E 140 tis.", "Data VZP", NAVY),
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
                  "7 segmentů z dat, ověřených na roce 2024", "opatření z literatury pro každý segment"]),
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
    "30 s. Shrnuto: máme model, sedm segmentů a opatření pro každý z nich. Nabízíme VZP pilot s randomizací v segmentech B až E "
    "v rámci řízeného vstupu inovací; model, segmenty i návrh experimentu předáme včetně kódu. Výsledkem může být až dvacet "
    "tisíc mamografií ročně navíc a desítky let života ve zdraví. Děkujeme."))

prs.save(OUT)
print("written", OUT, len(prs.slides), "slides")

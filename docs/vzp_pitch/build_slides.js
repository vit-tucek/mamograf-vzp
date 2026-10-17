// Builds zaver.pptx: the closing slide of the pitch (what we did, what next, what it brings to VZP).
//   NODE_PATH=<folder with node_modules/pptxgenjs> node docs/vzp_pitch/build_slides.js
//
// Numbers on the slide:
// - extra mammographies per year: literature effect ranges (docs/interventions.md) × 2024 segment sizes
//   for disjoint groups: pre-booked slot in B + C (66 037 women, +10 to +19 p. b.) and doctor as a channel
//   in D + E (140 398 women, +2 to +6 p. b.) → 9 412–20 971 per year;
// - QALY, deaths averted and cost per extra mammography: stage-shift model, ages 45–74
//   (docs/ZJISTENI.md, kap. 3): 3,82 QALY per 1 000 mammographies, 993 Kč per mammography incl.
//   treatment, 1 945 mammographies per death averted → 36–80 QALY and 5–11 deaths a year,
//   ≈ 0,26 mil. Kč per QALY; net monetary benefit at the SÚKL threshold 1,2 mil. Kč/QALY 34–75 mil. Kč a year.
const path = require("path");
const pptxgen = require("pptxgenjs");
const { THEME, GEOM, applyTheme, defineLayouts, md, paras } = require("../pptx_theme");

const OUT = path.join(__dirname, "zaver.pptx");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Mámo, graf!: co jsme udělali a co přineseme VZP";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const { W, M, CW, TOP } = GEOM;
defineLayouts(pres, "Mámo, graf! · Rakathon 2026");

const s = pres.addSlide({ masterName: "Tmavy" });
s.addText("Co jsme udělali, co dál a co to přinese VZP", { placeholder: "title" });

const gap = 0.3, cw = (CW - 2 * gap) / 3, y = TOP, h = 4.85;
const panel = (i, name) => {
  const x = M + i * (cw + gap);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h, rectRadius: 0.08, fill: { color: C.background1, transparency: 88 },
    line: { type: "none" }, objectName: name });
  return x;
};
const head = (x, n, t) => {
  s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.25, w: 0.55, h: 0.55, fill: { color: C.accent2 }, line: { type: "none" },
    objectName: `cislo_${n}` });
  s.addText(String(n), { x: x + 0.25, y: y + 0.25, w: 0.55, h: 0.55, align: "center", valign: "middle", fontSize: 18, bold: true,
    color: C.background1, fontFace: THEME.headFontFace, margin: 0, isTextBox: true, objectName: `cislo_${n}_text` });
  s.addText(t, { x: x + 0.95, y: y + 0.25, w: cw - 1.15, h: 0.55, valign: "middle", fontSize: 18, bold: true, color: C.background1,
    margin: 0, isTextBox: true, objectName: `nadpis_${n}` });
};
const list = (x, items, name) => s.addText(
  paras(items, { fontSize: 13, color: C.background1 }, { bullet: { indent: 14 }, paraSpaceAfter: 7 }),
  { x: x + 0.25, y: y + 1.0, w: cw - 0.5, h: h - 1.2, valign: "top", margin: 0, isTextBox: true, objectName: name });

// 1 · what we did
let x = panel(0, "udelali");
head(x, 1, "Co jsme udělali");
list(x, [
  "**1,34 mil. pozvánek** VZP 2020–2024 (508 tis. žen) a okresní data ČR",
  "**Model účasti** (CatBoost, AUC 0,84 na roce 2024) a jeho vysvětlení",
  "**11 akčních segmentů** z jednoduchých pravidel, stabilních v čase (AUC 0,81)",
  "**Příčiny:** s věkem mizí gynekolog, praktik na mamograf neposílá, další dopis přináší málo",
  "**Intervence z literatury** a návrhy experimentů s výpočtem velikosti, včetně aplikace Moje VZP",
], "udelali_text");

// 2 · what next
x = panel(1, "dal");
head(x, 2, "Co můžeme dál");
list(x, [
  "**Pilot s randomizací** v segmentech B–E v rámci řízeného vstupu inovací",
  "**Předrezervovaný termín + SMS** pro první pozvánky a vypadlé ženy",
  "**Lékař jako kanál:** seznamy žen bez mamografie pro gynekology a praktiky",
  "**Moje VZP:** rezervace jedním klepnutím, dotazník bariér",
  "**Model upliftu** a cílení podle zdravotní hodnoty, monitoring ekonomiky a QALY",
], "dal_text");

// 3 · what it brings (economics + QALY)
x = panel(2, "prinos");
head(x, 3, "Co to přinese VZP");
const stats = [
  ["9–21 tis.", "mamografií navíc ročně z cílených opatření v B–E"],
  ["36–80 QALY", "a 5–11 odvrácených úmrtí ročně"],
  ["0,26 mil. Kč", "za QALY (práh SÚKL 1,2 mil.): vysoce nákladově efektivní"],
  ["34–75 mil. Kč", "ročně čistý přínos v hodnotě zdraví; navíc 7 600 zbytečných dopisů méně"],
];
stats.forEach(([v, l], i) => {
  const yy = y + 0.95 + i * 0.92;
  s.addText(v, { x: x + 0.25, y: yy, w: cw - 0.5, h: 0.48, fontSize: 24, bold: true, color: C.accent3, fontFace: THEME.headFontFace,
    margin: 0, isTextBox: true, objectName: `prinos_${i + 1}` });
  s.addText(l, { x: x + 0.25, y: yy + 0.46, w: cw - 0.5, h: 0.45, fontSize: 11.5, color: C.background1, margin: 0, isTextBox: true,
    objectName: `prinos_${i + 1}_popis` });
});

// call to action + source
s.addText(md("**Nabízíme VZP pilot:** model, segmenty a návrh experimentu předáme i s kódem a dokumentací.",
  { fontSize: 16, color: C.background1 }), { x: M, y: y + h + 0.15, w: CW, h: 0.4, margin: 0, isTextBox: true, objectName: "vyzva" });
s.addText("Odhady: účinky z literatury × segmenty 2024; QALY a náklady z modelu posunu stadia (45–74 let). "
  + "Horní scénář finančního modelu digitální kaskády: 86–237 mil. Kč čistě za 2027–2031. Obojí ověří pilot.",
  { x: M, y: y + h + 0.55, w: CW, h: 0.35, fontSize: 10, color: C.accent3, margin: 0, isTextBox: true, objectName: "zdroj" });

s.addNotes("Co jsme udělali: analyzovali jsme 1,34 mil. pozvánek VZP z let 2020–2024 pro 508 tisíc žen a okresní data ČR. "
  + "Model CatBoost předpoví účast s AUC 0,84 na roce 2024, jedenáct segmentů z jednoduchých pravidel 0,81 a jsou stabilní v čase. "
  + "Příčiny: s věkem mizí gynekologická prevence, praktik na mamograf neposílá a každý další stejný dopis přináší méně.\n\n"
  + "Co dál: pilot s randomizací v segmentech B–E, předrezervovaný termín se SMS, lékař jako kanál, rezervace a dotazník bariér "
  + "v Moje VZP, model upliftu a monitoring ekonomiky a zdravotních výsledků.\n\n"
  + "Co to přinese: předrezervovaný termín v segmentech B a C (66 tisíc žen, +10 až +19 p. b.) a lékař jako kanál v D a E (140 tisíc žen, "
  + "+2 až +6 p. b.) dávají 9,4–21 tisíc mamografií navíc ročně; skupiny se nepřekrývají, takže se sčítají. Podle modelu posunu stadia "
  + "(3,8 QALY na 1 000 mamografií ve věku 45–74, asi 1 odvrácené úmrtí na 1 950 mamografií, 990 Kč na mamografii včetně léčby) je to "
  + "36–80 QALY a 5–11 odvrácených úmrtí ročně, asi 0,26 mil. Kč za QALY proti prahu SÚKL 1,2 mil. Kč. Čistý peněžní přínos v hodnotě "
  + "zdraví je 34–75 mil. Kč ročně (při reálném prahu 0,78 mil. Kč 19–42 mil.). Finanční model digitální kaskády počítá s +6 p. b. "
  + "u žen bez prevence a dává čistou úsporu 86–237 mil. Kč za 2027–2031; to je horní scénář, který musí ověřit pilot.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT);
  console.log("written", OUT);
})();

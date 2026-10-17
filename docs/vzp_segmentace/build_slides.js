// Builds slides.pptx from the content of slides.md (same folder).
//   NODE_PATH=<folder with node_modules/pptxgenjs> node docs/vzp_segmentace/build_slides.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { THEME, GEOM, applyTheme, defineLayouts, md, paras } = require("../pptx_theme");

const DIR = __dirname;
const OUT = path.join(DIR, "slides.pptx");
const img = (f) => path.join(DIR, f);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 × 7.5 in
pres.title = "Od pozvánky k mamografu: segmenty pozvaných žen";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const { W, M, CW, TOP } = GEOM;
const FOOT = "Data VZP 2020–2024 · segmentace pozvaných žen";

defineLayouts(pres, FOOT);

// ---------- helpers ----------
function slide(title, section, master = "Obsah") {
  const s = pres.addSlide({ masterName: master, sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  return s;
}
function picture(s, file, x, y, w, h) {
  s.addImage({ path: img(file), x, y, w, h, objectName: file });
}
// picture fitted into a box, keeping aspect ratio (ratio = width / height), aligned top-left
function fit(s, file, ratio, x, y, bw, bh) {
  let w = bw, h = bw / ratio;
  if (h > bh) { h = bh; w = bh * ratio; }
  picture(s, file, x, y, w, h);
  return { w, h };
}
function card(s, x, y, w, h, name, fill = C.background2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { type: "none" },
    rectRadius: 0.08, objectName: name });
}
function bullets(s, items, x, y, w, h, opts = {}) {
  s.addText(paras(items, { fontSize: opts.fontSize || 16, color: C.text1 }, { bullet: { indent: 18 }, paraSpaceAfter: 10 }),
    { x, y, w, h, valign: "top", margin: 0, isTextBox: true, objectName: opts.name || "body" });
}
function textCard(s, x, y, w, h, head, body, name) {
  card(s, x, y, w, h, name);
  s.addText([
    { text: head, options: { bold: true, fontSize: 16, color: C.accent1, breakLine: true, paraSpaceAfter: 6 } },
    ...md(body, { fontSize: 14, color: C.text1 }),
  ], { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: h - 0.3, valign: "top", margin: 0, isTextBox: true, objectName: name + "_text" });
}
function numbered(s, n, x, y, w, h, body) {
  card(s, x, y, w, h, `zjisteni_${n}`);
  s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.25, w: 0.6, h: 0.6, fill: { color: C.accent1 }, line: { type: "none" },
    objectName: `cislo_${n}` });
  s.addText(String(n), { x: x + 0.25, y: y + 0.25, w: 0.6, h: 0.6, align: "center", valign: "middle", fontSize: 20, bold: true,
    color: C.background1, margin: 0, isTextBox: true, fontFace: THEME.headFontFace });
  s.addText(md(body, { fontSize: 18, color: C.text1 }), { x: x + 1.1, y: y + 0.2, w: w - 1.3, h: h - 0.4, valign: "top",
    margin: 0, isTextBox: true, objectName: `zjisteni_${n}_text` });
}

// ---------- slides ----------
// 1 · title
pres.addSection({ title: "Úvod" });
{
  const s = pres.addSlide({ masterName: "Titulni", sectionTitle: "Úvod" });
  s.addText("Od pozvánky k mamografu: segmenty pozvaných žen", { placeholder: "title" });
  s.addText([
    { text: "Data VZP 2020–2024 · 1 344 556 pozvánek · 508 527 žen", options: { bold: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Segmentační model s 11 pravidly, jeho ověření na roce 2024, přechody mezi segmenty a návrhy experimentů.",
      options: { breakLine: true, paraSpaceAfter: 18 } },
    { text: "Zdroj: notebooks/vzp_segmentation_final.ipynb", options: { fontSize: 12 } },
  ], { placeholder: "body" });
}

// 2 · question and data
{
  const s = slide("Otázka a data", "Úvod");
  const stats = [["1 344 556", "pozvánek 2020–2024"], ["508 527", "žen nepřetržitě pojištěných"], ["256 466", "žen v testovacím roce 2024"]];
  stats.forEach(([v, l], i) => {
    const x = M + i * (CW / 3);
    s.addText(v, { x, y: TOP, w: CW / 3 - 0.3, h: 0.8, fontSize: 40, bold: true, color: C.accent1, margin: 0, isTextBox: true,
      fontFace: THEME.headFontFace, objectName: `stat_${i}` });
    s.addText(l, { x, y: TOP + 0.8, w: CW / 3 - 0.3, h: 0.35, fontSize: 13, color: C.accent4, margin: 0, isTextBox: true,
      objectName: `stat_${i}_popis` });
  });
  const cw = (CW - 0.3) / 2, ch = 1.75, y0 = 2.95;
  textCard(s, M, y0, cw, ch, "Otázka", "**Kdo po adresné pozvánce přijde na mamograf a kdo ne?** Kde jsou ženy, které nechodí, a jak je oslovit?", "karta_otazka");
  textCard(s, M + cw + 0.3, y0, cw, ch, "Data", "Pozvánky VZP 2020–2024 pro ženy nepřetržitě pojištěné 2015–2025. Účast = mamografie do 3, 6 a 12 měsíců po pozvánce.", "karta_data");
  textCard(s, M, y0 + ch + 0.25, cw, ch, "Segmentační model", "**11 srozumitelných pravidel** nad sloupci VZP. Pozvánka patří do prvního segmentu, jehož pravidlo platí.", "karta_model");
  textCard(s, M + cw + 0.3, y0 + ch + 0.25, cw, ch, "Poctivé ověření", "Model „naučený“ na letech 2020–2023 (účast segmentu) a **otestovaný na roce 2024** (256 466 žen).", "karta_overeni");
}

// 3 · tree
pres.addSection({ title: "Segmentační model" });
{
  const s = slide("Segmentační model: 11 segmentů jako rozhodovací strom", "Segmentační model");
  const { w } = fit(s, "strom_segmentu.png", 1604 / 1457, M, TOP, 7.0, 5.6);
  const x = M + w + 0.4, tw = W - M - x;
  textCard(s, x, TOP, tw, 1.9, "Tři rozměry",
    "**Historie screeningu**, **kontakt se zdravotnictvím a prevencí** a **počet nevyslyšených pozvánek**.", "karta_rozmery");
  s.addText("25×", { x, y: TOP + 2.3, w: tw, h: 1.1, fontSize: 60, bold: true, color: C.accent2, margin: 0, isTextBox: true,
    fontFace: THEME.headFontFace, objectName: "stat_25x" });
  s.addText("Tolikrát se liší účast mezi listy stromu (2–60 %).", { x, y: TOP + 3.4, w: tw, h: 0.8, fontSize: 16,
    color: C.text1, margin: 0, isTextBox: true, objectName: "stat_25x_popis" });
}

// 4 · validation on 2024
{
  const s = slide("Model z let 2020–2023 platí i v roce 2024", "Segmentační model");
  const { h } = fit(s, "segmenty_predikce_2024.png", 2170 / 829, M, TOP, CW, 3.75);
  const y = TOP + h + 0.25;
  const hdr = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent1 } } });
  s.addTable([
    [hdr("2024, do 12 měsíců"), hdr("AUROC"), hdr("log-loss")],
    [{ text: "11 segmentů (účast 2020–2023)" }, { text: "0,807", options: { bold: true } }, { text: "0,387" }],
    [{ text: "plný model hazardu (19 sloupců)" }, { text: "0,837" }, { text: "0,362" }],
  ], { x: M, y, w: 5.6, colW: [3.4, 1.1, 1.1], fontSize: 13, color: C.text1, border: { type: "solid", pt: 0.5, color: "D9C4CD" },
    fill: { color: C.background1 }, rowH: 0.36, margin: 0.05, objectName: "tabulka_auroc" });
  bullets(s, [
    "Segmenty nesou **asi 90 % rozlišovací síly** plného modelu.",
    "V 8 z 11 segmentů sedí předpověď do ±1,3 p. b. Účast roste u 1. pozvánky s málo kontakty (+5,1 p. b.) a u vypadlých 3–4 roky (+4,6 p. b.).",
  ], M + 6.0, y, CW - 6.0, 7.0 - y - 0.1, { fontSize: 15, name: "komentar" });
}

// 5 · where non-attenders are
pres.addSection({ title: "Kde jsou nepřišlé ženy" });
{
  const s = slide("Kde jsou ženy, které nepřišly (2024: 207 tisíc)", "Kde jsou nepřišlé ženy");
  const { w } = fit(s, "segmenty_mapa.png", 1234 / 762, M, TOP, 7.3, 5.6);
  const x = M + w + 0.4, tw = W - M - x;
  bullets(s, [
    "**56 %** nepřišlých je ve čtyřech segmentech s účastí 3–10 %. Největší je „jiná prevence, opakovaně nereaguje“: 56,8 tis. žen.",
    "**59 %** nepřišlých chodí ke gynekologovi nebo na jinou prevenci, takže je lze oslovit přes lékaře.",
    "Nejslibnější střed: **gynekolog, zvaná málokrát** (22,7 tis. nepřišlých, účast 27 %) a **jiná prevence, zvaná málokrát** (25,7 tis., 13 %).",
  ], x, TOP, tw, 5.5, { fontSize: 15 });
}

// 6 · spread within segments
{
  const s = slide("Uvnitř segmentů: kde má smysl individuální cílení", "Kde jsou nepřišlé ženy");
  const { h } = fit(s, "segmenty_rozptyl.png", 1692 / 662, M, TOP, CW, 3.9);
  const y = TOP + h + 0.25, cw = (CW - 0.3) / 2, ch = 6.95 - y;
  textCard(s, M, y, cw, ch, "Široký rozptyl",
    "První pozvánky, vypadlé a ženy u gynekologa. Tam má smysl **cílit podle modelu** (AUROC uvnitř 0,63–0,79).", "karta_siroky");
  textCard(s, M + cw + 0.3, y, cw, ch, "Úzký a nízký rozptyl",
    "Nereagující, odpojené a ženy bez prevence. **90 % z nich má predikci pod 15 %**, podskupina, která by chodila, v nich není.", "karta_uzky");
}

// 7 · transition matrix
pres.addSection({ title: "Přechody mezi segmenty" });
{
  const s = slide("Přechodová matice: co následuje po pozvánce", "Přechody mezi segmenty");
  const { w } = fit(s, "prechodova_matice.png", 1954 / 1124, M, TOP, 9.6, 5.6);
  const x = M + w + 0.35, tw = W - M - x;
  textCard(s, x, TOP, tw, 3.0, "Jak číst",
    "Pozvánky 2020–2023. **Řádek** = segment, **sloupce** = přišla / segment další pozvánky / bez další pozvánky.", "karta_jak_cist");
}

// 8 · transition graph
{
  const s = slide("Přechody jako graf", "Přechody mezi segmenty");
  const { w } = fit(s, "graf_prechodu.png", 1839 / 1235, M, TOP, 8.4, 5.65);
  const x = M + w + 0.35, tw = W - M - x, ch = 1.7;
  textCard(s, x, TOP, tw, ch, "Horní patro", "1. pozvánka, vypadlé: **přijde 25–57 %**.", "karta_horni");
  textCard(s, x, TOP + ch + 0.25, tw, ch, "Střední patro", "„Zvaná málokrát“: polovina zůstává, **12–26 % přijde**.", "karta_stredni");
  textCard(s, x, TOP + 2 * (ch + 0.25), tw, ch, "Dolní patro",
    "Nereagující, odpojené, bez prevence: uzavřený okruh, zůstává 49–74 %, **přijde 3–9 %**.", "karta_dolni");
}

// 9 · main flow
{
  const s = slide("Hlavní tok: pět největších segmentů", "Přechody mezi segmenty");
  const { w } = fit(s, "graf_prechodu_top5.png", 1495 / 1006, M, TOP, 8.4, 5.65);
  const x = M + w + 0.35, tw = W - M - x;
  card(s, x, TOP, tw, 2.6, "karta_tok");
  s.addText(md("**1. pozvánka** (57 % přijde) → **gynekolog / jiná prevence, zvaná málokrát** (26 % / 12 %) → **jiná prevence, nereaguje** (4 %, 74 % zůstává).",
    { fontSize: 16, color: C.text1 }), { x: x + 0.2, y: TOP + 0.2, w: tw - 0.4, h: 2.2, valign: "top", margin: 0, isTextBox: true,
    objectName: "karta_tok_text" });
  s.addText("Zpětná hrana z „nereaguje“ chybí: co se nezíská brzy, už se skoro nezíská.", { x, y: TOP + 2.9, w: tw, h: 1.3,
    fontSize: 16, italic: true, color: C.accent2, margin: 0, isTextBox: true, objectName: "pointa" });
}

// 10–11 · findings
pres.addSection({ title: "Zjištění" });
const FINDINGS = [
  "**11 pravidel stačí.** AUROC 0,807 na roce 2024 proti 0,837 plného modelu. Segmenty jsou stabilní v čase.",
  "**Účast se liší 25×:** 60 % u první pozvánky v kontaktu se zdravotnictvím, 2–5 % u zkřížených dopisů, odpojených a opakovaně nereagujících.",
  "**59 % nepřišlých chodí ke gynekologovi nebo na jinou prevenci.** Jsou dosažitelné jinou cestou než dopisem.",
  "**Zkřížené dopisy:** 7 600 dopisů ročně (3 %) jde ženám, které screening měly 0–1 měsíc předem.",
  "**Segmenty bez screeningu jsou „lepkavé“.** Ve stejném segmentu zůstává 56–83 % žen. Každý rok sestoupí 9–15 % „zvaných málokrát“ do „opakovaně nereaguje“.",
  "**První pozvánka je rozcestí.** Přijde 57 % žen v kontaktu se zdravotnictvím, ale jen 31–36 % žen s málo kontakty. Z nich je 13 % příští rok odpojených.",
  "**Model uvnitř segmentu pomůže jen tam, kde je rozptyl:** u první pozvánky, vypadlých a žen u gynekologa.",
  "**Intervenovat co nejdřív v toku:** první pozvánka a „zvaná málokrát“, dokud žena nesestoupí.",
];
[0, 1].forEach((part) => {
  const s = slide(`Hlavní zjištění (${part + 1}/2)`, "Zjištění");
  const cw = (CW - 0.3) / 2, ch = 2.55;
  FINDINGS.slice(4 * part, 4 * part + 4).forEach((t, i) => {
    numbered(s, 4 * part + i + 1, M + (i % 2) * (cw + 0.3), TOP + Math.floor(i / 2) * (ch + 0.3), cw, ch, t);
  });
});

// 12–13 · experiments
pres.addSection({ title: "Experimenty" });
const EXP_HDR = ["#", "Segment (2024)", "Intervence", "Účast 12M", "MDE*"];
const EXPS = [
  [["1", "Dopis se minul (7 600)", "Ověřit screening těsně před odesláním, dopis odložit", "2 %", "procesní změna"],
   ["2", "1. pozvánka, málo kontaktů (7 100)", "SMS / telefonát navíc k dopisu", "36 %", "3,2 p. b."],
   ["3", "1. pozvánka, v kontaktu (30 300)", "Lepší dopis: informace, sociální norma, předvyplněný termín", "60 %", "1,6 p. b."],
   ["4", "Gynekolog, zvaná málokrát (31 100)", "Seznam pacientek gynekologovi, žádanka při prohlídce (klastrová RCT)", "27 %", "1,4 p. b.**"]],
  [["5", "Gynekolog, opakovaně nereaguje (19 900)", "Objednání přímo v ordinaci místo dopisu", "10 %", "1,2 p. b."],
   ["6", "Jiná prevence, opakovaně nereaguje (59 900)", "3 ramena: dopis / praktik / **bez dopisu** (non-inferiorita)", "5 %", "0,5 p. b."],
   ["7", "Vypadlá 3–4 roky (16 200)", "Připomínka s konkrétním termínem (implementation intention)", "39 %", "2,2 p. b."]],
];
EXPS.forEach((rows, part) => {
  const s = slide(`Návrhy experimentů (${part + 1}/2)`, "Experimenty");
  const hdr = EXP_HDR.map((t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent1 } } }));
  const body = rows.map((r, i) => r.map((t, j) => ({ text: md(t), options: {
    fill: { color: i % 2 ? C.background1 : C.background2 }, align: j >= 3 ? "center" : "left", bold: j === 0 } })));
  s.addTable([hdr, ...body], { x: M, y: TOP, w: CW, colW: [0.5, 3.6, 5.4, 1.2, 1.433], fontSize: 14, color: C.text1,
    border: { type: "solid", pt: 0.5, color: "D9C4CD" }, rowH: 0.62, valign: "middle", margin: 0.08,
    objectName: `tabulka_experimenty_${part + 1}` });
  const yb = TOP + 0.5 + rows.length * 0.75 + 0.35;
  if (part === 0) {
    s.addText("* nejmenší zjistitelný rozdíl při rozdělení ročníku segmentu napůl (α = 0,05, síla 80 %) · ** bez design efektu klastrů",
      { x: M, y: yb, w: CW, h: 0.4, fontSize: 11, color: C.accent4, margin: 0, isTextBox: true, objectName: "poznamka" });
  } else {
    card(s, M, yb, CW, 1.55, "karta_vystupy");
    s.addText(md("**Společné výstupy:** účast do 3 / 6 / 12 měsíců, **sestup do horšího segmentu** při další pozvánce, náklad na získanou mamografii. Randomizace uvnitř segmentu s rozvrstvením podle územního pracoviště, analýza ITT.",
      { fontSize: 15, color: C.text1 }), { x: M + 0.25, y: yb + 0.15, w: CW - 0.5, h: 1.25, valign: "middle", margin: 0,
      isTextBox: true, objectName: "karta_vystupy_text" });
  }
});

// 14 · limitations (dark)
pres.addSection({ title: "Omezení" });
{
  const s = slide("Omezení", "Omezení", "Tmavy");
  const items = [
    "Segmenty popisují, **kdo přijde, ne kdo přijde díky intervenci**. Páky jsou hypotézy pro experiment.",
    "„Bez screeningu“ = bez kódu za 5 let. Přechod „vypadlá 4–5+ let“ → bez screeningu je zčásti artefakt tohoto okna.",
    "Účast do 12 měsíců u pozvánek z konce roku 2023 se pozoruje až v roce 2024. Přísně oddělené učení by muselo končit rokem 2022.",
    "V datech nejsou nově pojištěné ženy ani ženy 75+. Územní pracoviště není okres.",
  ];
  const cw = (CW - 0.3) / 2, ch = 2.55;
  items.forEach((t, i) => {
    const x = M + (i % 2) * (cw + 0.3), y = TOP + Math.floor(i / 2) * (ch + 0.3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, fill: { color: C.background1, transparency: 88 },
      line: { type: "none" }, rectRadius: 0.08, objectName: `omezeni_${i + 1}` });
    s.addText(md(t, { fontSize: 19, color: C.background1 }), { x: x + 0.3, y: y + 0.25, w: cw - 0.6, h: ch - 0.5, valign: "top",
      margin: 0, isTextBox: true, objectName: `omezeni_${i + 1}_text` });
  });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT);
  console.log("written", OUT);
})();

// Builds system.pptx: concept of a targeted-prevention system for VZP (general, any screening program).
//   NODE_PATH=<folder with node_modules/pptxgenjs> node docs/vzp_system/build_slides.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { THEME, GEOM, applyTheme, defineLayouts, md, paras } = require("../pptx_theme");

const OUT = path.join(__dirname, "system.pptx");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Systém cílené prevence VZP";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const HEX = THEME.colors;
const { W, M, CW, TOP } = GEOM;
defineLayouts(pres, "Koncept · systém cílené prevence VZP");

// ---------- helpers ----------
function slide(title, section, master = "Obsah") {
  const s = pres.addSlide({ masterName: master, sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  return s;
}
function box(s, x, y, w, h, name, fill = C.background2, line = null) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill },
    line: line ? { color: line, width: 1, dashType: "dash" } : { type: "none" }, objectName: name });
}
function text(s, runs, x, y, w, h, name, opts = {}) {
  s.addText(runs, { x, y, w, h, margin: 0, valign: "top", isTextBox: true, objectName: name, ...opts });
}
// heading + body runs inside a box
function card(s, x, y, w, h, name, head, body, { fill = C.background2, fg = C.text1, hd = C.accent1, size = 13, pad = 0.18 } = {}) {
  box(s, x, y, w, h, name, fill);
  const runs = [{ text: head, options: { bold: true, fontSize: size + 3, color: hd, breakLine: true, paraSpaceAfter: 4 } }];
  if (Array.isArray(body)) {
    runs.push(...paras(body, { fontSize: size, color: fg }, { paraSpaceAfter: 3 }));
  } else {
    runs.push(...md(body, { fontSize: size, color: fg }));
  }
  text(s, runs, x + pad, y + pad * 0.8, w - 2 * pad, h - 1.6 * pad, name + "_text");
}
// axis-aligned arrow from (x1, y1) to (x2, y2), optional label beside its middle
function arrow(s, x1, y1, x2, y2, name, label, { color = HEX.accent4, both = false, lx = 0.08, ly = -0.32, lw = 2.2 } = {}) {
  const back = x2 < x1 || y2 < y1;
  const line = { color, width: 2 };
  if (both) { line.beginArrowType = "triangle"; line.endArrowType = "triangle"; }
  else if (back) line.beginArrowType = "triangle";
  else line.endArrowType = "triangle";
  s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    line, objectName: name });
  if (label) {
    text(s, label, (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, lw, 0.3, name + "_popis",
      { fontSize: 11, italic: true, color: C.accent4 });
  }
}
const sub = (t, o = {}) => ({ text: t, options: { ...o, subscript: true } });
const r = (t, o = {}) => ({ text: t, options: o });

// ---------- 1 · title ----------
pres.addSection({ title: "Úvod" });
{
  const s = pres.addSlide({ masterName: "Titulni", sectionTitle: "Úvod" });
  s.addText("Systém cílené prevence VZP", { placeholder: "title" });
  s.addText([
    { text: "Model pro každého klienta: zdravotní rizika, pravděpodobnost účasti a účinek intervencí",
      options: { bold: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Komunikace s klienty a poskytovateli · monitoring ekonomiky a zdravotních výsledků · experimenty",
      options: { breakLine: true, paraSpaceAfter: 18 } },
    { text: "Koncept pro libovolný preventivní program nebo screening", options: { fontSize: 13 } },
  ], { placeholder: "body" });
  s.addNotes("Koncept je obecný: platí pro mamografický, kolorektální i cervikální screening, očkování nebo preventivní prohlídky. "
    + "Jádrem je model, který pro každého klienta odhadne, co se mu zdravotně hrozí, jestli k prevenci přijde sám "
    + "a o kolik účast zvýší jednotlivé intervence. Kolem něj je komunikace s klienty a poskytovateli a nad tím monitoring a experimenty.");
}

// ---------- 2 · architecture ----------
pres.addSection({ title: "Systém" });
{
  const s = slide("Architektura systému", "Systém");
  // top band: monitoring and experiments
  const yT = TOP, hT = 1.5;
  box(s, M, yT, CW, hT, "monitoring", C.background2);
  text(s, [r("Monitoring a experimenty", { bold: true, fontSize: 16, color: C.accent1, breakLine: true }),
    r("vyhodnocení celého systému, plánování a řízení pokusů", { fontSize: 12, color: C.accent4 })],
    M + 0.2, yT + 0.15, 2.3, hT - 0.3, "monitoring_nadpis");
  const views = [
    ["Provoz", "dosah a odezva kanálů, účast podle segmentů a regionů"],
    ["Ekonomika", "náklady, cena za vyšetření navíc, ICER / NMB, dopad na rozpočet"],
    ["Zdraví", "záchyt v časnějším stadiu, odvrácená úmrtí, QALY, vytížení kapacit"],
    ["Experimenty", "design, randomizace, kontrolní skupina, vyhodnocení, rozšíření"],
  ];
  const vx0 = M + 2.65, vw = (CW - 2.65 - 0.15 - 3 * 0.15) / 4;
  views.forEach(([h, b], i) => card(s, vx0 + i * (vw + 0.15), yT + 0.15, vw, hT - 0.3, `pohled_${i + 1}`, h, b,
    { fill: C.background1, size: 12, pad: 0.14 }));

  // three columns
  const yC = yT + hT + 0.55, hC = 6.95 - yC;
  const wSide = 3.35, xL = M, xR = W - M - wSide, xMid = xL + wSide + 0.75, wMid = xR - 0.75 - xMid;
  card(s, xL, yC, wSide, hC, "klient", "Komunikace VZP ↔ klient", [
    "**Ven:** dopis, e-mail, aplikace VZP (push, rezervace), SMS, telefonát / navigace, předrezervovaný termín",
    "**Zpět:** odezva, rezervace termínu, odhlášení, preference kanálu, odpovědi v dotaznících",
  ], { size: 14 });
  card(s, xR, yC, wSide, hC, "poskytovatele", "Komunikace VZP ↔ poskytovatelé", [
    "**Ven:** seznamy klientů pro praktiky a specialisty, objednání u poskytovatele",
    "**Zpět:** vykázané výkony (výsledek: přišel / nepřišel, nález), volné kapacity",
  ], { size: 14 });
  // model in the middle
  box(s, xMid, yC, wMid, hC, "model", C.accent1);
  text(s, [r("Model v VZP", { bold: true, fontSize: 18, color: C.background1 })], xMid + 0.2, yC + 0.12, wMid - 0.4, 0.4, "model_nadpis");
  const parts = [
    ["Zdravotní rizika", "jaké nemoci a jak moc hrozí (z historie péče)"],
    ["Pravděpodobnost účasti", "přijde klient k prevenci sám, bez zásahu?"],
    ["Uplift intervencí", "o kolik účast zvýší každá intervence"],
  ];
  const pw = wMid - 0.4, ph = 0.64;
  parts.forEach(([h, b], i) => {
    const py = yC + 0.58 + i * (ph + 0.08);
    box(s, xMid + 0.2, py, pw, ph, `model_cast_${i + 1}`, C.background1);
    text(s, [r(h, { bold: true, fontSize: 13, color: C.accent1, breakLine: true }), r(b, { fontSize: 11.5, color: C.text1 })],
      xMid + 0.35, py + 0.05, pw - 0.3, ph - 0.08, `model_cast_${i + 1}_text`);
  });
  const oy = yC + 0.58 + 3 * (ph + 0.08);
  box(s, xMid + 0.2, oy, pw, 6.95 - 0.15 - oy, "optimalizace", C.accent2);
  text(s, [r("Optimalizace: ", { bold: true, fontSize: 12.5, color: C.background1 }),
    r("kdo dostane co, kdy a jakým kanálem, v mezích rozpočtu, kapacit a rovnosti", { fontSize: 12, color: C.background1 })],
    xMid + 0.35, oy + 0.08, pw - 0.3, 6.95 - 0.25 - oy, "optimalizace_text", { valign: "middle" });

  // arrows between columns and model
  const a1 = yC + 1.0, a2 = yC + 2.55;
  arrow(s, xMid, a1, xL + wSide, a1, "sip_kl_ven", [r("intervence", { align: "center" })], { lx: -0.5, lw: 1.0 });
  arrow(s, xL + wSide, a2, xMid, a2, "sip_kl_zpet", [r("odezva", { align: "center" })], { lx: -0.5, lw: 1.0 });
  arrow(s, xMid + wMid, a1, xR, a1, "sip_po_ven", [r("seznamy", { align: "center" })], { lx: -0.5, lw: 1.0 });
  arrow(s, xR, a2, xMid + wMid, a2, "sip_po_zpet", [r("výkony", { align: "center" })], { lx: -0.5, lw: 1.0 });
  // model <-> monitoring
  const mx1 = xMid + wMid * 0.3, mx2 = xMid + wMid * 0.7;
  arrow(s, mx1, yC, mx1, yT + hT, "sip_mon_nahoru", [r("predikce, rozhodnutí")], { lx: -2.25, ly: -0.15, lw: 2.15 });
  arrow(s, mx2, yT + hT, mx2, yC, "sip_mon_dolu", [r("výsledky pokusů")], { lx: 0.1, ly: -0.15, lw: 2.0 });

  s.addNotes("Uprostřed je model, který pro každého klienta počítá tři věci: zdravotní rizika (z historie péče, diagnóz, léků), "
    + "pravděpodobnost, že k prevenci přijde sám, a uplift, tedy o kolik účast zvýší každá intervence (dopis, e-mail, push, SMS, "
    + "telefonát nebo navigace, předrezervovaný termín, oslovení přes praktika nebo specialistu). Optimalizace z toho sestaví plán: "
    + "kdo dostane co, kdy a kterým kanálem, v mezích rozpočtu, kapacit a požadavků na rovnost.\n\n"
    + "Vlevo komunikace s klienty: výstupem jsou intervence, vstupem odezva, rezervace a odhlášení. Vpravo poskytovatelé: "
    + "seznamy klientů a objednávání, zpět vykázané výkony, které jsou zároveň výsledkem (přišel / nepřišel) pro učení modelu.\n\n"
    + "Nahoře monitoring: provoz, ekonomika (náklady, cena za vyšetření navíc, ICER a čistý peněžní přínos, dopad na rozpočet) "
    + "a zdravotní výsledky (stadium při záchytu, odvrácená úmrtí, QALY, kapacity). Součástí je plánování a řízení experimentů "
    + "s trvalou kontrolní skupinou; jejich výsledky se vracejí do modelu jako aktualizované odhady účinků.");
}

// ---------- 3 · VZP app ----------
{
  const s = slide("Aplikace VZP: přímý kanál a zpětná vazba", "Systém");
  const wL = 7.05, xR = M + wL + 0.35, wR = W - M - xR, yB = 5.75;
  text(s, [r("Co aplikace doručí", { bold: true, fontSize: 16, color: C.accent1 })], M, TOP, wL, 0.35, "dorucit_nadpis");
  const items = [
    ["Rezervace jedním klepnutím", "předrezervovaný termín: potvrdit, přesunout, uvolnit; uvolněné termíny se vrací poskytovateli"],
    ["Dotazník bariér → cílený krok", "„Co vám brání?“ → navigace telefonem, večerní termín, doprava, vysvětlení „bez žádanky“"],
    ["Přehled prevence", "vše, co klienta čeká: screeningy, preventivní prohlídky, očkování na jednom místě"],
    ["Připomínky a obsah", "stejné zprávy jako SMS a dopis, zdarma, s rezervací na jedno klepnutí a variantami k testování"],
  ];
  const cw = (wL - 0.25) / 2, ch = (yB - 0.25 - (TOP + 0.5) - 0.25) / 2;
  items.forEach(([h, b], i) => {
    const x = M + (i % 2) * (cw + 0.25), y = TOP + 0.5 + Math.floor(i / 2) * (ch + 0.25);
    box(s, x, y, cw, ch, `aplikace_${i + 1}`);
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, fill: { color: C.accent2 }, line: { type: "none" },
      objectName: `aplikace_${i + 1}_cislo` });
    text(s, [r(String(i + 1), { bold: true, fontSize: 16, color: C.background1, fontFace: THEME.headFontFace })],
      x + 0.2, y + 0.2, 0.5, 0.5, `aplikace_${i + 1}_cislo_text`, { align: "center", valign: "middle" });
    text(s, [r(h, { bold: true, fontSize: 15, color: C.accent1, breakLine: true, paraSpaceAfter: 4 }),
      r(b, { fontSize: 13, color: C.text1 })], x + 0.85, y + 0.2, cw - 1.05, ch - 0.35, `aplikace_${i + 1}_text`);
  });
  // what comes back
  box(s, xR, TOP, wR, yB - 0.25 - TOP, "zpet", C.accent1);
  text(s, [r("Co se vrací do VZP", { bold: true, fontSize: 16, color: C.background1, breakLine: true, paraSpaceAfter: 8 }),
    ...paras([
      "**Důvody, proč klient nepřišel:** znaky pro segmentaci a model upliftu",
      "**Zkušenost po vyšetření:** kvalita poskytovatelů, návyk",
      "**Dosažitelnost kanálů:** komu co funguje, omezení pro optimalizaci",
      "**Platforma pro pokusy:** levná randomizace, zaznamenané přiřazení, signály za dny",
    ], { fontSize: 15, color: C.background1 }, { bullet: { indent: 14 }, paraSpaceAfter: 14 })],
    xR + 0.25, TOP + 0.2, wR - 0.5, yB - 0.25 - TOP - 0.35, "zpet_text");
  // caveats
  box(s, M, yB, CW, 6.95 - yB, "pozor", C.background2);
  text(s, [r("Pozor: ", { bold: true, fontSize: 13.5, color: C.accent1 }),
    r("uživatelé aplikace jsou výběr: chodí častěji a nejtěžší segmenty zastihne aplikace nejméně, takže výsledky "
      + "platí jen pro ně a dopis, SMS ani telefon nenahradí. Krátké a řídké dotazníky (únava, zkreslení odpovědí), souhlas "
      + "s využitím odpovědí (GDPR). Výsledek měřit vykázaným výkonem, ne kliknutím.", { fontSize: 13, color: C.text1 })],
    M + 0.25, yB + 0.15, CW - 0.5, 6.95 - yB - 0.3, "pozor_text", { valign: "middle" });

  s.addNotes("Aplikace VZP má mezi klienty dobrý dosah (zhruba 700 tisíc uživatelů; aktivita a podíl v cílových skupinách zatím "
    + "nejsou známé) a VZP ji chce rozvíjet jako přímý kanál včetně zpětné vazby. Samotná push notifikace je slabá intervence: "
    + "ve studii ze Singapuru na ni kliklo jen 4 % adresátek. Hodnota aplikace je jinde. Zaprvé jako levný kanál pro intervence, které "
    + "fungují: předrezervovaný termín, který klient jedním klepnutím potvrdí, přesune nebo uvolní (uvolněné termíny se vracejí "
    + "poskytovateli, což snižuje hlavní náklad předrezervace); dotazník bariér, podle jehož odpovědi následuje cílený krok "
    + "(navigace telefonem jen tam, kde ji telefonát vyřeší); přehled všech preventivních programů na jednom místě; levné "
    + "varianty zpráv. Zadruhé jako zdroj zpětné vazby: důvody neúčasti jako znaky pro model upliftu, zkušenost po vyšetření "
    + "pro sledování kvality, dosažitelnost kanálů a platforma pro průběžné randomizované pokusy. Pozor na samovýběr uživatelů, "
    + "zkreslení a únavu z dotazníků a na souhlas s využitím odpovědí.");
}

// ---------- 4 · explainable attendance model ----------
pres.addSection({ title: "Modely" });
{
  const s = slide("Model pravděpodobnosti účasti: vysvětlitelný (EBM)", "Modely");
  // formula banner
  box(s, M, TOP, CW, 0.7, "vzorec", C.accent1);
  text(s, [r("logit p(x) = β", { color: C.background1 }), sub("0", { color: C.background1 }), r(" + Σ f", { color: C.background1 }),
    sub("j", { color: C.background1 }), r("(x", { color: C.background1 }), sub("j", { color: C.background1 }),
    r(") + Σ f", { color: C.background1 }), sub("ij", { color: C.background1 }), r("(x", { color: C.background1 }),
    sub("i", { color: C.background1 }), r(", x", { color: C.background1 }), sub("j", { color: C.background1 }),
    r(")", { color: C.background1 }),
    r("     Explainable Boosting Machine: zobecněný aditivní model s vybranými interakcemi, učený boostingem",
      { color: C.accent3, fontSize: 13 })],
    M + 0.25, TOP + 0.1, CW - 0.5, 0.5, "vzorec_text", { fontSize: 18, valign: "middle", bold: false });

  // illustrative shape functions
  const yG = TOP + 0.95, gw = 3.05, gh = 2.15, gx = [M, M + gw + 0.2];
  const curves = [
    ["Měsíce od poslední prevence", ["0", "6", "12", "18", "24", "30", "36", "42", "48", "54", "60"],
      [0.6, 0.55, 0.42, 0.22, 0.02, -0.18, -0.36, -0.5, -0.6, -0.66, -0.69]],
    ["Kontakty se zdravotnictvím za rok", ["0", "1", "2", "3", "4", "5", "6", "8", "10", "12"],
      [-0.62, -0.34, -0.14, 0.02, 0.13, 0.21, 0.26, 0.31, 0.33, 0.34]],
    ["Věk", ["45", "50", "55", "60", "65", "70", "75"], [-0.28, -0.06, 0.12, 0.22, 0.24, 0.12, -0.12]],
  ];
  curves.forEach(([title, labels, values], i) => {
    const x = gx[i % 2], y = yG + Math.floor(i / 2) * (gh + 0.2);
    s.addChart(pres.charts.LINE, [{ name: title, labels, values }], {
      x, y, w: gw, h: gh, objectName: `tvarova_funkce_${i + 1}`,
      showTitle: true, title, titleFontSize: 12, titleColor: HEX.accent4, titleFontFace: "+mn-lt",
      chartColors: [HEX.accent1], lineSize: 2, lineSmooth: true, lineDataSymbol: "none", showLegend: false,
      catAxisLabelFontSize: 9, valAxisLabelFontSize: 9, catAxisLabelColor: HEX.accent4, valAxisLabelColor: HEX.accent4,
      catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", valAxisLabelFormatCode: "0.0",
      valGridLine: { color: "E3D5DB", size: 0.5 }, catGridLine: { style: "none" }, catAxisLineShow: false,
      valAxisMinVal: -0.8, valAxisMaxVal: 0.8, valAxisMajorUnit: 0.4,
    });
  });
  // fourth cell: how to read
  card(s, gx[1], yG + gh + 0.2, gw, gh, "jak_cist", "Jak číst",
    "Každá křivka je **příspěvek jednoho znaku k logitu**. Predikce klienta je jejich součet, takže je **přesně** vidět, proč vyšla. Křivky jsou ilustrativní.",
    { size: 12 });

  // right column: why EBM
  const xR = M + 2 * gw + 0.55, wR = W - M - xR;
  text(s, paras([
    "**Skleněná skříňka:** model je přímo čitelný, rozklad predikce je přesný (ne dodatečná aproximace jako SHAP nad černou skříňkou).",
    "**Přesnost** na tabulkových datech blízko gradient boostingu, **dobře kalibrované pravděpodobnosti** pro optimalizaci a ekonomiku.",
    "**Kontrola:** monotónní omezení, úprava křivek s lékaři, kontrola férovosti podle regionů a skupin.",
    "**Regulace:** vysvětlení pro klienta, lékaře i regulátora (GDPR čl. 22, AI Act).",
    "**Prior pro uplift:** logit EBM je výchozí bod modelu účinku intervencí (další snímek).",
  ], { fontSize: 14, color: C.text1 }, { bullet: { indent: 16 }, paraSpaceAfter: 8 }), xR, yG, wR, 4.3, "proc_ebm");
  text(s, md("**Zvážené alternativy:** logit se splajny (málo pružný), skórkarta (méně přesná), GBM + SHAP (jen dodatečné vysvětlení; zůstává jako měřítko ceny vysvětlitelnosti).",
    { fontSize: 11, color: C.accent4 }), xR, 6.15, wR, 0.75, "alternativy");

  s.addNotes("Pro pravděpodobnost účasti doporučuji Explainable Boosting Machine (InterpretML): zobecněný aditivní model s vybranými "
    + "dvojicovými interakcemi, učený boostingem. Každý znak má vlastní křivku, kterou lze číst, ověřit s lékaři a případně upravit. "
    + "Predikce jednoho klienta se přesně rozloží na příspěvky znaků. Přesnost bývá blízko gradient boostingu a pravděpodobnosti "
    + "jsou dobře kalibrované, což potřebuje optimalizace i ekonomika. Lze vynutit monotónnost (čím déle od poslední prevence, "
    + "tím nižší pravděpodobnost) a zkontrolovat férovost. Pro různé horizonty (3, 6, 12 měsíců) buď jeden model na horizont, "
    + "nebo diskrétní model v čase. GBM se SHAP necháváme jako měřítko: ukáže, kolik přesnosti nás vysvětlitelnost stojí. "
    + "Křivky na snímku jsou ilustrativní, ne z dat.");
}

// ---------- 5 · uplift model ----------
{
  const s = slide("Model upliftu: bayesovský, s modelem účasti jako priorem", "Modely");
  const y1 = TOP, hA = 1.3, y2 = y1 + hA + 0.25, wA = 3.0;
  const xC = M + wA + 0.65, wC = 4.55, hC = 2 * hA + 0.25, xD = xC + wC + 0.65, wD = W - M - xD;
  card(s, M, y1, wA, hA, "prior_ebm", "Model účasti (EBM)", "f(x): výchozí logit klienta, **prior pro uplift**", { size: 12.5 });
  card(s, M, y2, wA, hA, "prior_literatura", "Literatura", [
    "β (průměrný účinek intervence): prior z metaanalýz",
  ], { size: 12.5 });
  // central Bayesian box
  box(s, xC, y1, wC, hC, "bayes", C.accent1);
  const wh = { color: C.background1 };
  text(s, [
    r("Bayesovský hierarchický model", { bold: true, fontSize: 16, color: C.background1, breakLine: true, paraSpaceAfter: 6 }),
    r("logit P(účast | x, k) = f(x) + β", { ...wh, fontSize: 18 }), sub("k", { ...wh, fontSize: 18 }), r(" + g", { ...wh, fontSize: 18 }),
    sub("k", { ...wh, fontSize: 18 }), r("(x)", { ...wh, fontSize: 18, breakLine: true, paraSpaceAfter: 4 }),
    r("τ", { ...wh, fontSize: 18 }), sub("k", { ...wh, fontSize: 18 }), r("(x) = σ(f + β", { ...wh, fontSize: 18 }), sub("k", { ...wh, fontSize: 18 }),
    r(" + g", { ...wh, fontSize: 18 }), sub("k", { ...wh, fontSize: 18 }), r(") − σ(f)", { ...wh, fontSize: 18, breakLine: true, paraSpaceAfter: 12 }),
    r("g", { color: C.accent3, fontSize: 13.5 }), sub("k", { color: C.accent3, fontSize: 13.5 }),
    r("(x): rozdíly v účinku mezi klienty na stejných znacích jako EBM, prior smrštěný k nule. Uplift je malý u těch, kdo přijdou "
      + "vždy nebo nikdy, největší uprostřed.", { color: C.accent3, fontSize: 13.5 }),
  ], xC + 0.25, y1 + 0.18, wC - 0.5, hC - 0.3, "bayes_text");
  card(s, xD, y1, wD, hA, "experimenty", "Randomizované pokusy", "zaznamenaná pravděpodobnost přiřazení → **posterior**", { size: 12.5 });
  card(s, xD, y2, wD, hA, "rozhodnuti", "Rozhodnutí", "τ × zdravotní přínos − náklad, v mezích rozpočtu, kapacit a rovnosti", { size: 12.5 });
  // arrows
  arrow(s, M + wA, y1 + hA / 2, xC, y1 + hA / 2, "sip_ebm");
  arrow(s, M + wA, y2 + hA / 2, xC, y2 + hA / 2, "sip_lit");
  arrow(s, xD, y1 + hA / 2, xC + wC, y1 + hA / 2, "sip_exp");
  arrow(s, xC + wC, y2 + hA / 2, xD, y2 + hA / 2, "sip_rozh");
  arrow(s, xD + wD / 2, y2, xD + wD / 2, y1 + hA, "sip_pruzkum", [r("průzkum ~10 %")], { lx: 0.1, ly: -0.15, lw: 1.6 });
  // later stage
  const yL = y1 + hC + 0.2;
  box(s, xC, yL, wC, 0.55, "pozdeji", C.background1, HEX.accent4);
  text(s, md("**Později, s dostatkem dat:** DR-learner + causal forest", { fontSize: 12, color: C.accent4 }),
    xC + 0.15, yL + 0.08, wC - 0.3, 0.4, "pozdeji_text", { valign: "middle" });

  // bottom cards
  const yB = yL + 0.8, hB = 6.95 - yB, wB = (CW - 2 * 0.25) / 3;
  card(s, M, yB, wB, hB, "proc_randomizace", "Proč randomizace",
    "Data VZP ukážou, **kdo přichází**, ale ne **kdo přijde díky intervenci**: kanály nikdy nebyly přidělené náhodně. Uplift se proto učí z pokusů.", { size: 12.5 });
  card(s, M + wB + 0.25, yB, wB, hB, "vyhodnoceni", "Vyhodnocení",
    "Qini / AUUC a kalibrace upliftu po decilech, hodnota pravidla cílení off-policy (DR), **trvalá kontrolní skupina**.", { size: 12.5 });
  card(s, M + 2 * (wB + 0.25), yB, wB, hB, "rizika", "Rizika",
    "Negativní uplift („sleeping dogs“), pořadí kanálů (dopis → SMS → telefonát), posun v čase, férovost.", { size: 12.5 });

  s.addNotes("Klíčové omezení: bohatá data VZP (roky vykázané péče, diagnózy, léky, registrace, historie prevence, dřívější pozvánky "
    + "a odezvy, dosažitelnost kanálů, region) dobře předpovídají, kdo přijde. Neřeknou ale, kdo přijde díky intervenci, protože "
    + "kanály nebyly přidělované náhodně. Uplift naučený jen z historie by byl zkreslený.\n\n"
    + "Proto: (1) každá kampaň randomizuje a zaznamenává pravděpodobnost přiřazení; trvalý podíl průzkumu (např. 10 %) a Thompson "
    + "sampling; libovolné pravidlo cílení lze pak vyhodnotit offline. (2) Jádrem je bayesovský hierarchický model na škále logitu: "
    + "f(x) je logit z modelu účasti (EBM) jako pevný offset a prior, β_k průměrný účinek intervence s priorem z literatury, "
    + "g_k(x) rozdíly mezi klienty na stejných znacích jako EBM, smrštěné k nule (horseshoe, částečné sdílení). Před prvním pokusem je "
    + "prior upliftu plně dán EBM a literaturou; každý pokus posune posterior. Uplift zůstává vysvětlitelný. (3) Až bude randomizovaných "
    + "dat dost: víceramenný DR-learner na gradient boostingu (EBM jako model kontrolního ramene), causal forest pro intervaly "
    + "spolehlivosti, při velkých datech vícehlavá neuronová síť. (4) Cílí se na zdravotní hodnotu, ne na samotnou účast: "
    + "τ_k(x) krát zdravotní přínos vyšetření pro daného klienta minus náklad, v mezích rozpočtu, kapacit a rovnosti. "
    + "(5) Vyhodnocení: Qini / AUUC, kalibrace upliftu, DR off-policy hodnota pravidla, trvalá kontrolní skupina. "
    + "(6) Rizika: negativní uplift, pořadí a kombinace kanálů (později dynamický režim / kontextový bandit), posun v čase, férovost.");
}

// ---------- 6 · roadmap ----------
pres.addSection({ title: "Postup" });
{
  const s = slide("Postup zavedení", "Postup", "Tmavy");
  const steps = [
    ["Priory", "model účasti (EBM) a účinky intervencí z literatury"],
    ["Pilotní pokus", "víceramenná RCT po segmentech, levně i v aplikaci VZP, zaznamenané pravděpodobnosti přiřazení"],
    ["První model upliftu", "bayesovský posterior: kdo na co reaguje"],
    ["Cílení s průzkumem", "optimalizace podle zdravotní hodnoty, ~10 % průzkum, trvalá kontrolní skupina"],
    ["Učení dokola", "pravidelné přeučení, vyhodnocení v monitoringu, rozhodnutí o rozšíření"],
  ];
  const gap = 0.25, sw = (CW - 4 * gap) / 5, y = TOP + 0.45, h = 3.6;
  steps.forEach(([head, body], i) => {
    const x = M + i * (sw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: sw, h, rectRadius: 0.08, fill: { color: C.background1, transparency: 88 },
      line: { type: "none" }, objectName: `krok_${i + 1}` });
    s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.3, w: 0.7, h: 0.7, fill: { color: C.accent2 }, line: { type: "none" },
      objectName: `krok_${i + 1}_cislo` });
    text(s, [r(String(i + 1), { bold: true, fontSize: 22, color: C.background1, fontFace: THEME.headFontFace })],
      x + 0.25, y + 0.3, 0.7, 0.7, `krok_${i + 1}_cislo_text`, { align: "center", valign: "middle" });
    text(s, [r(head, { bold: true, fontSize: 17, color: C.background1, breakLine: true, paraSpaceAfter: 6 }),
      r(body, { fontSize: 14, color: C.accent3 })], x + 0.25, y + 1.25, sw - 0.5, h - 1.45, `krok_${i + 1}_text`);
    if (i < steps.length - 1) {
      arrow(s, x + sw + 0.02, y + 0.65, x + sw + gap - 0.02, y + 0.65, `sip_krok_${i + 1}`, null, { color: HEX.accent3 });
    }
  });
  text(s, md("**Monitoring běží od prvního dne:** provoz, ekonomika a zdravotní výsledky, vždy proti kontrolní skupině.",
    { fontSize: 16, color: C.background1 }), M, y + h + 0.45, CW, 0.5, "monitoring_pointa");
  s.addNotes("Začneme s tím, co máme: model účasti z historických dat a účinky intervencí z literatury. Pilotní pokus "
    + "s několika rameny po segmentech dá první posterior. Pak cílíme podle zdravotní hodnoty, s trvalým průzkumem a kontrolní "
    + "skupinou, a model pravidelně přeučujeme. Monitoring sleduje provoz, ekonomiku a zdravotní výsledky od začátku.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT);
  console.log("written", OUT);
})();

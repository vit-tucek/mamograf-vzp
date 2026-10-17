// Shared theme for the project's PowerPoint decks (docs/*/build_slides.js).
// pptxgenjs sets only the theme fonts; applyTheme() writes the palette into ppt/theme/*.xml,
// so scheme colors (pres.SchemeColor.*) resolve to these values instead of Office blue.
// Needs pptxgenjs (and the jszip it ships with) on NODE_PATH.
const fs = require("fs");

const THEME = {
  name: "Mamograf",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "262626", lt1: "FFFFFF", dk2: "5B2A45", lt2: "F7EEF2",
    accent1: "5B2A45", accent2: "2A9D8F", accent3: "E9C9D3", accent4: "3D4F5C",
    accent5: "B5838D", accent6: "8DBDB5", hlink: "2A9D8F", folHlink: "5B2A45",
  },
};
const SLOTS = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"];

async function applyTheme(file, theme = THEME) {
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const parts = Object.keys(zip.files).filter((p) => /^ppt\/theme\/theme\d+\.xml$/.test(p));
  for (const p of parts) {
    let xml = await zip.file(p).async("string");
    for (const k of SLOTS) {
      const re = new RegExp(`<a:${k}>[\\s\\S]*?</a:${k}>`);
      if (!re.test(xml)) throw new Error(`${p}: slot ${k} not found`);
      xml = xml.replace(re, `<a:${k}><a:srgbClr val="${theme.colors[k]}"/></a:${k}>`);
    }
    xml = xml.replace(/<a:clrScheme name="[^"]*"/, `<a:clrScheme name="${theme.name}"`);
    zip.file(p, xml);
  }
  // pptxgenjs 4.0.1 writes an <a:pPr> after every run of a multi-run paragraph. That is invalid
  // OOXML (pPr must come first) and the stray <a:buNone/> in it drops the paragraph's bullet.
  for (const p of Object.keys(zip.files).filter((f) => /^ppt\/slides\/slide\d+\.xml$/.test(f))) {
    const xml = await zip.file(p).async("string");
    zip.file(p, xml.replace(/(<\/a:r>)<a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g, "$1"));
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

// "text with **bold** parts" -> pptxgenjs runs
function md(s, base = {}) {
  return s.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map((t) =>
    t.startsWith("**") ? { text: t.slice(2, -2), options: { ...base, bold: true } } : { text: t, options: { ...base } });
}

// list of markdown strings -> runs, one paragraph each. Paragraph options (bullet, spacing) go on
// the first run only: pptxgenjs starts a new paragraph at every run that carries `bullet`.
function paras(items, base = {}, para = {}) {
  const out = [];
  items.forEach((s, i) => {
    const runs = md(s, base);
    Object.assign(runs[0].options, para);
    if (i < items.length - 1) runs[runs.length - 1].options.breakLine = true;
    out.push(...runs);
  });
  return out;
}

// Slide geometry shared by the decks (LAYOUT_WIDE, 13.333 × 7.5 in)
const GEOM = { W: 13.333, M: 0.6, CW: 13.333 - 1.2, TOP: 1.35 };

// Layouts: "Titulni" (dark title slide), "Obsah" (white, title only), "Tmavy" (dark, title only).
// Footer text and slide number live on the layouts.
function defineLayouts(pres, foot) {
  const C = pres.SchemeColor, { W, M, CW } = GEOM;
  pres.defineSlideMaster({
    title: "Titulni",
    background: { color: C.accent1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 2.0, w: CW, h: 1.6, fontSize: 40, bold: true,
        color: C.background1, valign: "bottom", align: "left" }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: M, y: 3.8, w: CW, h: 2.2, fontSize: 18,
        color: C.accent3, valign: "top", align: "left" }, text: "" } },
    ],
  });
  for (const [title, bg, fg, muted] of [["Obsah", C.background1, C.accent1, C.accent4], ["Tmavy", C.accent1, C.background1, C.accent3]]) {
    pres.defineSlideMaster({
      title,
      background: { color: bg },
      objects: [
        { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: CW, h: 0.8, fontSize: 30, bold: true,
          color: fg, valign: "middle", align: "left", margin: 0 }, text: "" } },
        { text: { text: foot, options: { x: M, y: 7.05, w: 8, h: 0.3, fontSize: 10, color: muted, margin: 0 } } },
      ],
      slideNumber: { x: W - M - 0.6, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: muted, align: "right" },
    });
  }
}

module.exports = { THEME, GEOM, applyTheme, defineLayouts, md, paras };

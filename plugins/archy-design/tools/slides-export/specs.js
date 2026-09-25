// Specs for the Archy deck layouts, in canvas px (1920 x 1080).
//
// Written as a module rather than 14 JSON files so the parts that are identical by
// construction - the Rulers frame, the Meta line, the three-part header - are written
// and verified ONCE. That mirrors how the design system actually works: CLAUDE.md says
// to derive a new light layout by duplicating `03 · Metrics`, not by rebuilding it.
//
// Every coordinate here was read out of Paper (get_children returns worldX/worldY, so
// Paper has already resolved the flex layout), not derived by eye.

// ---------------------------------------------------------------- palettes

// Rules on a coloured ground are --color-white at opacity 0.3 in Paper. Pre-blended to a
// solid hex here on purpose: relying on fill transparency surviving the Slides import is
// one more thing that can drift, and the blend is exact.
const LIGHT = {
  bg: "FFFFFF",
  rule: "EEEEEE",
  eyebrow: "013DF5",
  h1: "00004E",
  h2: "666666",
  metaText: "AAAAAA",
  metaDiv: "CCCCCC",
  body: "666666",
  label: "00004E",
  stat: "013DF5",
};

const DARK = {
  bg: "00004E",
  rule: "4D4D83", // white 0.3 over 00004E
  eyebrow: "66BFFF",
  h1: "FFFFFF",
  h2: "CCEAFF",
  metaText: "CCEAFF",
  metaDiv: "66BFFF",
  body: "CCEAFF",
  label: "FFFFFF",
  stat: "66BFFF",
};

const BLUE = {
  bg: "013DF5",
  rule: "4D77F8", // white 0.3 over 013DF5
  eyebrow: "66BFFF",
  h1: "FFFFFF",
  h2: "66BFFF", // on the bright blue the 200 is too close to white to read as a second tone
  metaText: "CCEAFF",
  metaDiv: "66BFFF",
  body: "CCEAFF",
};

// `Capture Full-bleed` sits on the image slot itself. The slot is --color-neutral
// (#666666) rather than a pale grey so the white type and the white-at-0.3 Rulers read on
// it; on a pale slot they vanish and the template previews as broken.
const SLOT = {
  bg: "666666",
  rule: "949494", // white 0.3 over 666666
  eyebrow: "FFFFFF",
  h1: "FFFFFF",
  h2: "FFFFFF",
  metaText: "FFFFFF",
  metaDiv: "C2C2C2", // white 0.6 over 666666
  body: "FFFFFF",
};

// ---------------------------------------------------------------- fonts

const ONEST = "Onest SemiBold";
const ONEST_REG = "Onest";
const INTER = "Inter";
const INTER_MED = "Inter Medium";
const INTER_SEMI = "Inter SemiBold";

// ---------------------------------------------------------------- helpers

const rect = (layer, x, y, w, h, fill) => ({ type: "rect", layer, x, y, w, h, fill });

const rulerH = (y, c, x = 0, w = 1920) => rect("Ruler H", x, y, w, 2, c.rule);
const rulerV = (x, y, h, c) => rect("Ruler V", x, y, 2, h, c.rule);

const text = (layer, x, y, w, h, t, o = {}) => ({
  type: "text",
  layer,
  x,
  y,
  w,
  h,
  text: t,
  font: o.font || INTER,
  size: o.size,
  line: o.line,
  color: o.color,
  ...(o.track ? { track: o.track } : {}),
  ...(o.upper ? { upper: true } : {}),
  ...(o.align ? { align: o.align } : {}),
});

// The Meta line's five nodes sit at the same x on every artboard: it is right-aligned to
// the trim at 1824 and its content is identical everywhere, so the flex result is too.
//
// These five x values are READ OUT OF PAPER, not derived. They were 1416 / 1580 / 1606 /
// 1772 / 1798 for a while - arithmetic from "1824 minus a measured content width of 408"
// - and Paper actually resolves the row three pixels further left, at 1413 / 1577 / 1603 /
// 1769 / 1795. Three pixels is invisible on one slide; the meta is on all fifty-five, so
// it was a consistent 3px drift across the whole deck against the design it copies.
const meta = (c) => [
  text("Meta Slot", 1413, 96, 164, 22, "Confidential", {
    font: INTER_MED, size: 18, line: 22, track: 0.05, color: c.metaText, upper: true }),
  text("Meta Divider 1", 1577, 96, 26, 22, "|", { size: 18, line: 22, color: c.metaDiv }),
  text("Meta Archy", 1603, 96, 166, 22, "Archy © 2026", {
    font: INTER_MED, size: 18, line: 22, track: 0.05, color: c.metaText, upper: true }),
  text("Meta Divider 2", 1769, 96, 26, 22, "|", { size: 18, line: 22, color: c.metaDiv }),
  // "NN" is a placeholder: build.js substitutes the real number from the slide index,
  // so the page number is never a hand-maintained value that goes stale on a reorder.
  text("Meta Page", 1795, 96, 26, 22, "NN", {
    font: INTER_MED, size: 18, line: 22, track: 0.05, color: c.metaText }),
];

const eyebrow = (t, c) =>
  text("Eyebrow", 96, 92, 400, 24, t, {
    font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: c.eyebrow, upper: true });

// The two-tone headline: ONE text box, one coloured run per line, explicit break between
// them. See README - the two stacked nodes in Paper are a Paper limitation, not the
// design. Single line spacing (60/70 is 1.167x, single lands ~1.2x and reads better).
const headline = (l1, l2, c) => ({
  type: "text",
  layer: "Headline",
  x: 96, y: 144, w: 1728, h: 140,
  runs: [{ text: l1, color: c.h1 }, { text: l2, color: c.h2 }],
  font: ONEST, size: 60, line: "single", track: -0.02,
});

// Two lines that must break at a fixed point but share one colour (04's column titles).
const lines = (layer, x, y, w, h, arr, o) => ({
  type: "text",
  layer, x, y, w, h,
  runs: arr.map((t) => ({ text: t, color: o.color })),
  font: o.font, size: o.size, line: o.line,
  ...(o.track ? { track: o.track } : {}),
});

// The standard light Rulers frame: three full-bleed caps plus column verticals.
const lightFrame = (cols, c = LIGHT, vTop = 344, vH = 714) => [
  rulerH(20, c), rulerH(344, c), rulerH(1056, c),
  ...cols.map((x) => rulerV(x, vTop, vH, c)),
];

// ---------------------------------------------------------------- Statement

const statement = {
  name: "Statement",
  canvas: { w: 1920, h: 1080 },
  background: BLUE.bg,
  items: [
    // No 344 rule: there is no header band on a statement slide, only the two caps.
    rulerH(20, BLUE), rulerH(1056, BLUE),
    eyebrow("Positioning", BLUE),
    ...meta(BLUE),
    // Same two-run device as a headline, but the Cover-title tier is set SOLID at
    // 128/128 - single would open it to ~1.2x and push the copy off the composition.
    { type: "text", layer: "Statement", x: 210, y: 310, w: 1500, h: 256,
      runs: [
        { text: "The operating system", color: BLUE.h1 },
        { text: "for dental practices.", color: BLUE.h2 },
      ],
      font: ONEST, size: 128, line: 128, track: -0.02, align: "center" },
    rect("Ruler V", 959, 610, 2, 64, BLUE.rule),
    text("Lead", 460, 718, 1000, 40, "We own the record. Automate the work. Move the money.",
      { font: INTER_MED, size: 30, line: 40, color: "E6F4FF", align: "center" }),
    text("Body", 460, 778, 1000, 68,
      "AI teammates run the front office, the back office, and the revenue, so the practice can stay focused on the patient.",
      { size: 22, line: 34, color: BLUE.body, align: "center" }),
  ],
};

// ---------------------------------------------------------------- Metrics 2×2

// The reference light layout. Cells use a 52px inline padding, not the 40 the later
// grids settled on, so its value/label/body lane sits at x 148 rather than 136.
const PROBLEM = [
  [148, 394, "XX%", "of dental practices run on a server-based PMS",
    "Server-based incumbents and most cloud competitors require practices to purchase X to X bolted-on solutions to run their business."],
  [1012, 394, "XX%", "name staffing their #1 challenge",
    "With XX% of practices short a front desk in 2025, administrative staffing has become one of dentistry's most urgent problems."],
  [148, 749, "XX%", "of collections goes to staff payroll",
    "Archy is not automating the chair. We're automating everything around it that costs revenue without producing it."],
  [1012, 749, "XX%", "of revenue lost to billing leakage",
    "Claim denials have climbed to ~XX% and XX% are never appealed \u2014 revenue that walks out the door."],
];

const metrics = {
  name: "Metrics 2×2",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    rulerH(700, LIGHT),
    eyebrow("The problem", LIGHT),
    headline("Dental practices run on decades-old server-based software",
      "and drown in administrative work.", LIGHT),
    ...meta(LIGHT),
    ...PROBLEM.flatMap(([x, y, v, l, b], i) => [
      text(`Cell ${i + 1} Value`, x, y, 700, 84, v,
        { font: ONEST, size: 80, line: 84, track: -0.02, color: LIGHT.stat }),
      text(`Cell ${i + 1} Label`, x, y + 98, 700, 38, l,
        { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
      text(`Cell ${i + 1} Body`, x, y + 150, 700, 96, b,
        { size: 22, line: 32, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Columns 4-up

const COLUMNS_DATA = [
  ["01", ["Staffing", "shortage"],
    "Dentists cite staffing as their #1 problem to solve. We see significant interest in using AI to fill the gaps for roles they cannot hire."],
  ["02", ["AI", "inflection"],
    "Admin and clinical work can finally be automated, not just digitized. We own the data and the workflow, so we can automate both."],
  ["03", ["Legacy", "displacement"],
    "XX%+ of the market still sits on legacy server-based software. AI accelerates the interest in moving off legacy providers."],
  ["04", ["Generational", "displacement"],
    "Practice ownership is shifting to a younger cohort raised on cloud-native, AI-native tools. They are displacing incumbents who spent 20 years building for a generation heading for the exits."],
];

const columns4up = {
  name: "Columns 4-up",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 527, 959, 1391, 1822]),
    eyebrow("Why now", LIGHT),
    headline("Four curves are converging", "in our favor at the same time.", LIGHT),
    ...meta(LIGHT),
    ...COLUMNS_DATA.flatMap(([n, title, body], i) => {
      const x = 136 + i * 432;
      return [
        text(`Col ${i + 1} Number`, x, 394, 352, 96, n,
          { font: ONEST, size: 96, line: 96, track: -0.02, color: LIGHT.stat }),
        lines(`Col ${i + 1} Title`, x, 504, 352, 76, title,
          { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
        text(`Col ${i + 1} Body`, x, 594, 352, 260, body,
          { size: 22, line: 32, color: LIGHT.body }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Comparison Table

const ROWS_DATA = [
  ["01", "Insurance Verification", "2H 2026", false,
    "Front desk calls each payer, logs into XX+ portals, and transcribes benefits by hand.",
    "AI agent verifies benefits pre-visit and flags coverage gaps for review."],
  ["02", "Claim Submission", "2027", false,
    "Biller reviews codes, attaches documentation, and submits claims.",
    "Archy's RCM operator submits with AI validation catching missing docs and coding errors."],
  ["03", "Payment Posting", "AI-first today", true,
    "Biller matches each EOB to a claim, posts payments and adjustments.",
    "Auto-parses ERAs and EOBs, posts payments and flags exceptions."],
  ["04", "Insurance Follow-up", "2027", false,
    "Biller pulls aging reports, calls payers, and writes and mails appeal letters manually.",
    "Archy's operator manages follow-up with AI drafting denial-specific appeals."],
  ["05", "Patient Follow-up", "2027", false,
    "Mail paper statements, staff calls patients on balances, and negotiates payment plans.",
    "Multi-channel outreach: SMS, email, and AI voice/text with a self-serve payment portal."],
];

const comparisonTable = {
  name: "Comparison Table",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 623, 1223, 1822]),
    // Row separators are inset to the content column: they belong to the rows band, not
    // to the artboard, and the full-bleed rules already cap that band.
    ...[395, 527, 659, 791, 923].map((y) => rulerH(y, LIGHT, 96, 1728)),
    eyebrow("RCM lifecycle", LIGHT),
    headline("How each stage is done today,", "and how Archy will do it with AI.", LIGHT),
    ...meta(LIGHT),
    text("Label Stage", 136, 360, 400, 22, "Stage",
      { font: INTER_MED, size: 18, line: 22, track: 0.05, color: LIGHT.metaText, upper: true }),
    text("Label Today", 664, 360, 400, 22, "Today",
      { font: INTER_MED, size: 18, line: 22, track: 0.05, color: LIGHT.metaText, upper: true }),
    text("Label With Archy", 1264, 360, 400, 22, "With Archy AI",
      { font: INTER_MED, size: 18, line: 22, track: 0.05, color: LIGHT.stat, upper: true }),
    ...ROWS_DATA.flatMap(([n, title, timing, live, today, archy], i) => {
      const b = 396 + i * 132;
      return [
        text(`Row ${i + 1} No`, 136, b + 33, 60, 38, n,
          { font: ONEST, size: 30, line: 38, track: -0.02, color: LIGHT.stat }),
        text(`Row ${i + 1} Title`, 216, b + 33, 368, 38, title,
          { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
        text(`Row ${i + 1} Timing`, 216, b + 77, 368, 22, timing, {
          font: INTER_MED, size: 18, line: 22, track: 0.05, upper: true,
          color: live ? LIGHT.stat : LIGHT.body }),
        text(`Row ${i + 1} Today`, 664, b + 34, 520, 64, today,
          { size: 22, line: 32, color: LIGHT.body }),
        text(`Row ${i + 1} Archy`, 1264, b + 34, 520, 64, archy,
          { size: 22, line: 32, color: LIGHT.label }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Big Number

const POINTS = [
  [407, 457, "The wallet",
    "Practices pay X to XX% of insurance collections to outsourced billers, a wallet no PMS has ever captured."],
  [628.5, 678.5, "Why us, natively",
    "Competitors bolt onto someone else's record and are displaced the moment a practice switches systems. Our RCM lives inside the record we also sell."],
  [881.5, 931.5, "Pilot proof",
    "XX% auto-posting rate · XX days reduction in A/R · XX% clean-claim rate · X practices live on the full-service pilot at X.X% of collections."],
];

const bigNumber = {
  name: "Big Number",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...lightFrame([96, 959, 1822], DARK),
    rulerH(582, DARK, 960, 864),
    rulerH(819, DARK, 960, 864),
    eyebrow("The largest bet", DARK),
    headline("Revenue cycle is the biggest prize in dental,",
      "and we are the only one built to win it natively.", DARK),
    ...meta(DARK),
    text("Hero Value", 136, 497, 784, 300, "3x+",
      { font: ONEST, size: 320, line: 300, track: -0.02, color: DARK.stat }),
    text("Hero Caption", 136, 821, 640, 126,
      "what we earn in software from the same practice is what they already pay for billing.",
      { size: 30, line: 42, color: DARK.body }),
    ...POINTS.flatMap(([ty, by, title, body], i) => [
      text(`Point ${i + 1} Title`, 1000, ty, 784, 38, title,
        { font: ONEST, size: 30, line: 38, color: DARK.label }),
      text(`Point ${i + 1} Body`, 1000, by, 784, 96, body,
        { size: 22, line: 32, color: DARK.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Metrics 3-up

const TRACTION = [
  ["$XXM", "CARR", "X.Xx YoY \u2014 landed $X.Xm ahead of H1 plan"],
  ["$XXM", "ARR", "X.Xx YoY, X.Xx YoY ending 2026"],
  ["$XXk", "Avg new location ARR", "June new deals, up from $XX.Xk in 2025"],
  ["XXX", "Contracted locations", "+XX MoM"],
  ["XXX", "Live locations", "+XX MoM"],
  ["XXX", "New customers in H1", "vs. plan of XXX"],
];

// A footer band shrinks the content band and adds one more full-bleed rule; the
// 20 / 344 / 1056 caps never move. Column verticals stop at the extra rule (h 614).
const footerFrame = (cols) => [
  rulerH(20, LIGHT), rulerH(344, LIGHT), rulerH(958, LIGHT), rulerH(1056, LIGHT),
  rulerH(651, LIGHT),
  ...cols.map((x) => rulerV(x, 344, 614, LIGHT)),
];

const footerLine = (t) =>
  text("Footer Takeaway", 96, 992, 1728, 32, t,
    { font: INTER_MED, size: 22, line: 32, color: LIGHT.label });

const metrics3up = {
  name: "Metrics 3-up",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...footerFrame([96, 671, 1247, 1822]),
    eyebrow("Traction", LIGHT),
    headline("Compounding fast,", "and ahead of plan.", LIGHT),
    ...meta(LIGHT),
    ...TRACTION.flatMap(([v, l, m], i) => {
      const x = 136 + (i % 3) * 576;
      const b = i < 3 ? 346 : 651;
      return [
        text(`Stat ${i + 1} Value`, x, b + 60.5, 496, 84, v,
          { font: ONEST, size: 80, line: 84, track: -0.02, color: LIGHT.stat }),
        text(`Stat ${i + 1} Label`, x, b + 158.5, 496, 24, l,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.label, upper: true }),
        text(`Stat ${i + 1} Meta`, x, b + 188.5, 496, 56, m,
          { size: 20, line: 28, color: LIGHT.body }),
      ];
    }),
    footerLine("Consistent conversion of ~XX% CARR to ARR conversion QoQ since 1Q2025."),
  ],
};

// ---------------------------------------------------------------- Numbered rows

const GTM = [
  ["01", "Demand Capture", "Win the Hand Raisers",
    "Multiple channels reliably capture demand from dentists already in-market evaluating their existing PMS, so Archy is top of mind.",
    "XX% of demos come from dental conferences, paid search and social \u2014 our demand capture engine."],
  ["02", "Demand Generation", "Pull Forward Demand",
    "For practices not yet in-market we have established multiple outbound channels. Direct mail and cold outbound reach practices before they'd naturally start looking.",
    "Our direct mail campaigns (coffee bags) reinforce the message and accelerate the renewal timeline."],
  ["03", "Startups", "Win the Next Generation",
    "De novo practices are the market's future installed base, and newer dentists face fewer switching costs to adopting AI agents.",
    "Our 1-year discount for new practices, plus a startup education course, drive early-life acquisition."],
];

const numberedRows = {
  name: "Numbered rows",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 335, 815, 1822]),
    rulerH(582, LIGHT, 96, 1728),
    rulerH(818, LIGHT, 96, 1728),
    eyebrow("Go to market", LIGHT),
    headline("A repeatable motion plus a", "demand engine that compounds.", LIGHT),
    ...meta(LIGHT),
    ...GTM.flatMap(([n, title, sub, p1, p2], i) => {
      const b = [346, 583, 819][i];
      const h = [237, 236, 237][i];
      const ord = b + (h - 96) / 2;
      const ttl = b + (h - 78) / 2;
      const par = b + (h - 148) / 2;
      return [
        text(`Row ${i + 1} Ordinal`, 96, ord, 240, 96, n,
          { font: ONEST, size: 96, line: 96, track: -0.02, color: LIGHT.stat, align: "center" }),
        text(`Row ${i + 1} Title`, 376, ttl, 400, 38, title,
          { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
        text(`Row ${i + 1} Subtitle`, 376, ttl + 40, 400, 38, sub,
          { font: ONEST_REG, size: 30, line: 38, color: LIGHT.body }),
        text(`Row ${i + 1} Para 1`, 856, par, 928, 64, p1,
          { size: 22, line: 32, color: LIGHT.body }),
        text(`Row ${i + 1} Para 2`, 856, par + 84, 928, 64, p2,
          { size: 22, line: 32, color: LIGHT.body }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Split stats

const EFFICIENCY_STATS = [
  ["XX months", "CAC payback", "June 2026"],
  ["Xx ARR/OTE", "Ramped rep performance", "2Q 2026 \u2014 XX ramped AEs"],
  ["+X.XX", "Best sales month ever", "$X.XM new ARR sold in June 2026 vs. $X.XM in June 2025"],
];

const EFFICIENCY_CLAIMS = [
  [606, "XX day close", "High velocity sales motion",
    "XX% of deals are closed in under XX days, so pipeline converts inside a single quarter."],
  [832, "$1m top reps", "High performers close over $1m per year",
    "X AEs in 2025 each sold $XM+ of new ARR in their first year as an AE. We ended 2025 with X AEs, and X are on track to sell $XM+."],
];

const splitStats = {
  name: "Split stats",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    rulerH(20, LIGHT), rulerH(344, LIGHT), rulerH(604, LIGHT), rulerH(1056, LIGHT),
    rulerH(830, LIGHT, 96, 1728),
    ...[96, 671, 1247, 1822].map((x) => rulerV(x, 344, 262, LIGHT)),
    ...[96, 479, 1822].map((x) => rulerV(x, 606, 452, LIGHT)),
    eyebrow("Efficiency", LIGHT),
    headline("Growth that", "pays for itself.", LIGHT),
    ...meta(LIGHT),
    ...EFFICIENCY_STATS.flatMap(([v, l, m], i) => {
      const x = 136 + i * 576;
      return [
        text(`Stat ${i + 1} Value`, x, 384, 496, 84, v,
          { font: ONEST, size: 80, line: 84, track: -0.02, color: LIGHT.stat }),
        text(`Stat ${i + 1} Label`, x, 480, 496, 24, l,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.label, upper: true }),
        text(`Stat ${i + 1} Meta`, x, 510, 496, 56, m,
          { size: 20, line: 28, color: LIGHT.body }),
      ];
    }),
    ...EFFICIENCY_CLAIMS.flatMap(([b, v, title, body], i) => [
      // Value and title share one padding-top so their line boxes land on one lane.
      text(`Claim ${i + 1} Value`, 136, b + 56, 304, 96, v,
        { font: ONEST, size: 40, line: 48, track: -0.02, color: LIGHT.label }),
      text(`Claim ${i + 1} Title`, 520, b + 56, 1264, 38, title,
        { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
      text(`Claim ${i + 1} Body`, 520, b + 104, 1264, 64, body,
        { size: 22, line: 32, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Bars

// Five bars in 976: width 128, gap 84 (5*128 + 4*84 = 976).
// Max bar height = 560 (plot) − 30 (value label) − 24 (year label) − 16 (two 8px gaps).
const BAR_MAX = 490;

// [value, value label, year label, is forecast].
//
// Bar heights are DERIVED from the values, never authored. That is what makes real
// numbers a one-line change: replace the values and the labels beside them, and the
// geometry follows in proportion. The tallest bar always lands on BAR_MAX, so the plot
// stays full whatever the magnitudes are.
//
// The values below are placeholder magnitudes chosen to reproduce the heights on the
// Paper artboard exactly (98 / 172 / 294 / 392 / 490).
const BARS = [
  [10,   "$XM", "2024A", false],
  [17.5, "$XM", "2025A", false],
  [30,   "$XM", "2026E", true],
  [40,   "$XM", "2027E", true],
  [50,   "$XM", "2028E", true],
];

const BAR_PEAK = Math.max(...BARS.map(([v]) => v));
// Integer heights: a fractional bar height is the sub-pixel defect the Figma checklist
// flags, arrived at by arithmetic instead of by dragging.
const barHeight = (v) => Math.round((v / BAR_PEAK) * BAR_MAX);

const PROJECTIONS = [
  [346, 236, "2026E CARR", "$XM", "~X.Xx current ARR"],
  [584, 235, "2027E CARR", "$XM", "X.Xx YoY"],
  [821, 235, "2028E CARR", "$XM", "X.Xx YoY"],
];

const bars = {
  name: "Bars",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 1151, 1822]),
    rulerH(582, LIGHT, 1152, 672),
    rulerH(819, LIGHT, 1152, 672),
    // The axis is a Ruler at the bar baseline, spanning the whole chart column so it
    // meets that column's verticals.
    rulerH(976, LIGHT, 96, 1056),
    eyebrow("3-year plan", LIGHT),
    headline("Newly launched AI products", "accelerate growth of a fast-scaling base.", LIGHT),
    ...meta(LIGHT),
    // Legend is not optional: the actual/plan split is meaningless without it.
    rect("Legend Swatch Actual", 136, 398, 14, 14, "CCEAFF"),
    text("Legend Label Actual", 160, 394, 200, 22, "Actual",
      { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: LIGHT.body, upper: true }),
    rect("Legend Swatch Plan", 272, 398, 14, 14, LIGHT.stat),
    text("Legend Label Plan", 296, 394, 200, 22, "Plan",
      { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: LIGHT.stat, upper: true }),
    ...BARS.flatMap(([value, label, year, plan], i) => {
      const x = 136 + i * 212;
      const n = barHeight(value);
      return [
        text(`Bar ${year} Value`, x, 938 - n, 128, 30, label,
          { font: ONEST, size: 24, line: 30, color: plan ? LIGHT.stat : LIGHT.body, align: "center" }),
        rect(`Bar ${year} Column`, x, 976 - n, 128, n, plan ? LIGHT.stat : "CCEAFF"),
        text(`Bar ${year} Year`, x, 984, 128, 24, year,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.body, upper: true, align: "center" }),
      ];
    }),
    ...PROJECTIONS.flatMap(([b, h, label, value, delta], i) => {
      const top = b + (h - 116) / 2;
      return [
        text(`Proj ${i + 1} Label`, 1192, top, 592, 24, label,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.body, upper: true }),
        text(`Proj ${i + 1} Value`, 1192, top + 32, 300, 84, value,
          { font: ONEST, size: 80, line: 84, track: -0.02, color: LIGHT.stat }),
        // Baseline-aligned beside the value, not pushed to the far edge of the row.
        text(`Proj ${i + 1} Delta`, 1383, top + 79.5, 401, 28, delta,
          { size: 20, line: 28, color: LIGHT.body }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Cover

const PRESENTERS = [
  [96, "Jonathan Rat", "CEO & Co-founder"],
  [390, "Sarah Payne", "COO"],
  [647, "Sven Beer", "Head of Finance"],
];

const cover = {
  name: "Cover",
  canvas: { w: 1920, h: 1080 },
  background: BLUE.bg,
  items: [
    // Two caps and one full-height vertical - a spine, not a box. Adding the 96/1824
    // pair would close it. The vertical is the one rule in the system positioned by its
    // gutter to the meta block rather than by a column boundary: its right edge lands at
    // 1317, exactly 96 - the page margin - clear of the meta's left edge, which Paper
    // resolves to 1413. That edge is a measured flex result, so it moves if the optional
    // meta slot's copy changes; re-check the clearance, do not treat 1315 as sacred.
    rulerH(20, BLUE), rulerH(1056, BLUE),
    rect("Ruler V Divider", 1315, 20, 2, 1038, BLUE.rule),
    ...meta(BLUE),
    // Break forced so the title cannot reflow off the two-line composition.
    { type: "text", layer: "Title", x: 96, y: 150, w: 1100, h: 256,
      runs: [
        { text: "Investor", color: BLUE.h1 },
        { text: "Presentation", color: BLUE.h1 },
      ],
      font: ONEST, size: 128, line: 128, track: -0.02 },
    text("Date", 96, 442, 500, 56, "July 2026",
      { font: ONEST_REG, size: 48, line: 56, color: BLUE.body }),
    ...PRESENTERS.flatMap(([x, name, role], i) => [
      text(`Presenter ${i + 1} Name`, x, 872, 300, 38, name,
        { font: ONEST, size: 30, line: 38, color: BLUE.h1 }),
      text(`Presenter ${i + 1} Role`, x, 918, 300, 24, role,
        { font: INTER_MED, size: 20, line: 24, track: 0.05, color: BLUE.body, upper: true }),
    ]),
    { type: "image", layer: "Archy Wordmark", src: "assets/archy-wordmark.png",
      x: 1464, y: 856, w: 360, h: 140 },
  ],
};

// ---------------------------------------------------------------- Quotes

const QUOTES = [
  [136, "We're not spending our days filled with mundane tasks, doing data entry. Everything's just automated with Archy.",
    "Dr. Thomas DeChellis", "DeChellis & Stonestreet Dentistry"],
  [712, "Writing clinical notes used to be the part of my day I'd put off. Archy Scribe has cut that time in half, and the quality of my notes has improved.",
    "Dr. Lauren Koch", "Avondale Dental Studio"],
];

const RETENTION_STATS = [
  [445.5, "X.X%", "Monthly logo churn", "Trailing 12-month average"],
  [800.5, "XX", "NPS", "First half of 2026"],
];

const quotes = {
  name: "Quotes",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 1247, 1822]),
    rulerH(700, LIGHT, 1248, 576),
    eyebrow("Retention", LIGHT),
    headline("Practices love Archy,", "and the numbers back it up.", LIGHT),
    ...meta(LIGHT),
    ...QUOTES.flatMap(([x, quote, name, practice], i) => [
      // The quote mark is 80px type in a 28px line box in Paper - deliberately tight.
      // This is the one item whose vertical placement could not be checked locally.
      text(`Quote ${i + 1} Mark`, x, 394, 200, 28, "“",
        { font: ONEST, size: 80, line: 28, color: LIGHT.stat }),
      text(`Quote ${i + 1} Text`, x, 442, 496, 312, quote,
        { font: ONEST_REG, size: 36, line: 52, color: LIGHT.label }),
      { type: "ellipse", layer: `Quote ${i + 1} Portrait`,
        x, y: 936, w: 72, h: 72, fill: "CCEAFF" },
      text(`Quote ${i + 1} Name`, x + 92, 941, 400, 30, name,
        { font: ONEST, size: 24, line: 30, color: LIGHT.label }),
      text(`Quote ${i + 1} Practice`, x + 92, 975, 400, 28, practice,
        { size: 20, line: 28, color: LIGHT.stat }),
    ]),
    ...RETENTION_STATS.flatMap(([y, v, l, m], i) => [
      text(`Stat ${i + 1} Value`, 1288, y, 496, 84, v,
        { font: ONEST, size: 80, line: 84, track: -0.02, color: LIGHT.stat }),
      text(`Stat ${i + 1} Label`, 1288, y + 98, 496, 24, l,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.label, upper: true }),
      text(`Stat ${i + 1} Meta`, 1288, y + 128, 496, 28, m,
        { size: 20, line: 28, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Team grid

const TEAM = [
  ["Jonathan Rat", "CEO & Co-Founder"], ["Benjamin Kolin", "CTO & Co-Founder"],
  ["Sarah Payne", "COO"], ["Jonathan Stolter", "VP, Sales"],
  ["Sven Beer", "Head of Finance"], ["Dan Henig", "VP, Customer Experience"],
  ["Andrew Bernstein", "Head of Marketing"], ["Janelle Lopez", "VP, People"],
  ["Ellery Fink", "Head of Onboarding"], ["Deirdre Norris", "VP, Product"],
  ["Chad Wozniak", "Sales Director"], ["Laura Mozur", "Head of Support"],
  ["Chase Rowley", "Sales Director"],
];

const teamGrid = {
  name: "Team grid",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 527, 959, 1391, 1822]),
    // Row separators are full-bleed here, matching the graph-paper reading of a grid.
    rulerH(522, LIGHT), rulerH(699, LIGHT), rulerH(876, LIGHT),
    eyebrow("The team", LIGHT),
    headline("The leadership team", "scaling Archy.", LIGHT),
    ...meta(LIGHT),
    // 13 people in 16 slots: the ragged last row is the real state of the template.
    ...TEAM.flatMap(([name, role], i) => {
      const x = 136 + (i % 4) * 432;
      const y = 390.5 + Math.floor(i / 4) * 177;
      return [
        { type: "ellipse", layer: `Person ${i + 1} Portrait`,
          x, y, w: 88, h: 88, fill: "CCEAFF" },
        text(`Person ${i + 1} Name`, x + 108, y + 16, 244, 30, name,
          { font: ONEST, size: 24, line: 30, color: LIGHT.label }),
        text(`Person ${i + 1} Role`, x + 108, y + 50, 244, 22, role,
          { font: INTER_MED, size: 18, line: 22, color: LIGHT.body }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Product grid

// [name, pill width (measured in Paper), pill label, shipped?, body, icon]
const PRODUCTS = [
  ["Archy Scribe", 81, "GA", true,
    "Clinical documentation. SOAP notes written inside the chart, no copy-paste between tabs.", "icon-scribe"],
  ["Archy Revenue", 81, "GA", true,
    "Revenue cycle. Claims, posting, and collections, with AI validation before submission.", "icon-revenue"],
  ["Archy AI Imaging", 241, "GA & FDA-cleared", true,
    "AI-assisted radiologic review inside the imaging suite, part of the clinical foundation.", "icon-imaging"],
  ["Archy Verify", 134, "H2 2026", false,
    "Insurance verification. Eligibility and benefits checked automatically before the patient sits down.", "icon-verify"],
  ["Archy Insight", 101, "2027", false,
    "Analytics agent surfacing revenue opportunities and practice KPIs on request.", "icon-insight"],
  ["Archy Connect", 101, "2027", false,
    "Omni-channel patient communication across chat, SMS, voice and online scheduling.", "icon-connect"],
];

const productGrid = {
  name: "Product grid",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...footerFrame([96, 671, 1247, 1822]),
    eyebrow("Product", LIGHT),
    headline("Meet the AI teammates.", "Built as a platform, works like a teammate.", LIGHT),
    ...meta(LIGHT),
    ...PRODUCTS.flatMap(([name, pw, label, live, body, icon], i) => {
      const x = 136 + (i % 3) * 576;
      const b = i < 3 ? 386 : 691; // rows at 346 / 651, plus the cell's 40 padding
      return [
        text(`Product ${i + 1} Name`, x, b + 1, 456, 38, name,
          { font: ONEST, size: 30, line: 38, color: LIGHT.stat }),
        // Hugeicons run at 40px on a slide, not 32 - 32 reads timid next to a 30px title.
        { type: "image", layer: `Product ${i + 1} Icon`, src: `assets/${icon}.png`,
          x: x + 456, y: b, w: 40, h: 40 },
        // The Status pill earns its place because it carries state: shipped vs roadmap.
        { type: "pill", layer: `Product ${i + 1} Status`,
          x, y: b + 54, w: pw, h: 34, fill: live ? "E6F4FF" : "F7F7F7" },
        { type: "ellipse", layer: `Product ${i + 1} Dot`,
          x: x + 16, y: b + 66, w: 10, h: 10, fill: live ? LIGHT.stat : "AAAAAA" },
        text(`Product ${i + 1} Label`, x + 36, b + 60, 300, 22, label,
          { font: INTER_SEMI, size: 18, line: 22, track: 0.05, upper: true,
            color: live ? LIGHT.stat : LIGHT.body }),
        text(`Product ${i + 1} Body`, x, b + 102, 496, 96, body,
          { size: 22, line: 32, color: LIGHT.body }),
      ];
    }),
    footerLine("50% of June deals included the Clinical suite. Customers are buying AI teammates, not just the platform."),
  ],
};

// ---------------------------------------------------------------- Matrix

const ANCHORS = [
  [346, "Where we started", "$XB", DARK.h1,
    "Practice management software, the market Archy was built in."],
  [642, "Where we are going", "$XXXB+", DARK.stat,
    "In annual flow through U.S. dental practices Archy can now address."],
];

const POOLS = [
  ["icon-pms", "$XB", "Practice Mgmt Software", "Archy's core platform. Where we started."],
  ["icon-payments", "$XXB+", "Patient Payments", "Out-of-pocket flow. Processing plus patient financing take."],
  ["icon-insurance", "$XXB+", "Insurance Payments", "Insurer and government flow. Archy Revenue RCM, % of collections."],
  ["icon-staffing", "$XXB+", "Staffing & Services", "Admin labor plus outsourced agencies. Archy Connect and Verify."],
  ["icon-financing", "$XB+", "Practice Financing", "Annual originations. Secondary lending economics."],
  ["icon-hardware", "$XB+", "Hardware & Supplies", "Equipment and consumables. Sensors (Imaging) plus supplies."],
];

const matrix = {
  name: "Matrix",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    rulerH(20, DARK), rulerH(344, DARK), rulerH(936, DARK), rulerH(1056, DARK),
    rulerH(640, DARK, 96, 1728),
    ...[96, 575, 991, 1407, 1822].map((x) => rulerV(x, 344, 594, DARK)),
    eyebrow("Market", DARK),
    headline("Archy's US TAM is expanding",
      "from software into the whole dental economy.", DARK),
    ...meta(DARK),
    ...ANCHORS.flatMap(([b, label, value, colour, caption], i) => [
      text(`Anchor ${i + 1} Label`, 136, b + 44, 400, 22, label,
        { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: DARK.eyebrow, upper: true }),
      text(`Anchor ${i + 1} Value`, 136, b + 78, 400, 96, value,
        { font: ONEST, size: 96, line: 96, track: -0.02, color: colour }),
      text(`Anchor ${i + 1} Caption`, 136, b + 186, 400, 64, caption,
        { size: 22, line: 32, color: DARK.body }),
    ]),
    ...POOLS.flatMap(([icon, value, title, body], i) => {
      const x = 608 + (i % 3) * 416;
      const b = i < 3 ? 346 : 642;
      return [
        { type: "image", layer: `Pool ${i + 1} Icon`, src: `assets/${icon}.png`,
          x, y: b + 74, w: 40, h: 40 },
        // Right-aligned across the head so every value shares a lane.
        text(`Pool ${i + 1} Value`, x, b + 70, 352, 48, value,
          { font: ONEST, size: 40, line: 48, track: -0.02, color: DARK.stat, align: "right" }),
        text(`Pool ${i + 1} Title`, x, b + 130, 352, 30, title,
          { font: ONEST, size: 24, line: 30, color: DARK.label }),
        // Fixed height so a one-line body cannot pull the lane off the other cells.
        text(`Pool ${i + 1} Body`, x, b + 172, 352, 52, body,
          { size: 18, line: 26, color: DARK.body }),
      ];
    }),
    // blue-tint-200 at 0.6 over the navy ground, pre-blended.
    text("Footnote", 96, 971, 1728, 52,
      "Sources: ADA Health Policy Institute (2024 U.S. national dental expenditure $189B; out-of-pocket and private-insurance shares); Grand View Research (U.S. dental equipment and consumables ~$17.5B, 2024); industry PMS market estimates. Staffing and financing pools are Archy internal estimates. Figures shown are gross annual flow; Archy revenue is a take-rate captured on each pool.",
      { size: 18, line: 26, color: "7A8CB8" }),
  ],
};

// ---------------------------------------------------------------- chart helpers

// Every chart in the library shares one baseline. That is what makes two chart slides
// read as the same system when you page between them.
const CHART_BASE = 976;

// A legend key. Squares for area marks (bars, stacks); a 20 × 4 segment for a line -
// a square swatch beside a line chart describes the wrong mark.
const keySquare = (x, fill, label, colour) => [
  rect("Legend Swatch", x, 398, 14, 14, fill),
  text("Legend Label", x + 24, 394, 300, 22, label,
    { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: colour, upper: true }),
];
const keyLine = (x, fill, label, colour) => [
  rect("Legend Swatch", x, 403, 20, 4, fill),
  text("Legend Label", x + 30, 394, 300, 22, label,
    { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: colour, upper: true }),
];

// A period label under a mark, centred in that mark's own column.
const periodLabel = (layer, x, w, t, colour) =>
  text(layer, x, 984, w, 24, t,
    { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: colour, upper: true });

// A value label above a mark, 8px clear of it.
const valueLabel = (layer, x, w, top, t, colour) =>
  text(layer, x, top, w, 30, t,
    { font: ONEST, size: 24, line: 30, color: colour, align: "center" });

// ---------------------------------------------------------------- Line / Area

// Full-width plot: many periods need horizontal room, which is exactly what separates
// this from `Bars`. 8 points on columns of 206 (1648 / 8), each point at its column's
// centre - 239 + 206n. Spreading them edge-to-edge gives a pitch of 235.43 and
// sub-pixel positions.
const LINE_MAX = 490;
const LINE_DATA = [
  [8,    "1Q25", false], [11,   "2Q25", false], [14, "3Q25", false], [18, "4Q25", false],
  [23,   "1Q26", false], [30,   "2Q26", false], [38, "3Q26E", true], [50, "4Q26E", true],
];
const LINE_PEAK = Math.max(...LINE_DATA.map(([v]) => v));
const linePt = (i) => [
  239 + i * 206,
  CHART_BASE - Math.round((LINE_DATA[i][0] / LINE_PEAK) * LINE_MAX),
];
const LINE_PTS = LINE_DATA.map((_, i) => linePt(i));
const LINE_SPLIT = 5; // last actual index; the segment after it is forecast

const lineArea = {
  name: "Line / Area",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 1822]),
    rulerH(CHART_BASE, LIGHT, 96, 1728),
    eyebrow("ARR growth", LIGHT),
    headline("Compounding every quarter,", "with no month of decline.", LIGHT),
    ...meta(LIGHT),
    ...keyLine(136, "66BFFF", "Actual", LIGHT.body),
    ...keyLine(278, LIGHT.stat, "Plan", LIGHT.stat),
    // Area wash first so the stroke and markers sit on top of it.
    { type: "polygon", layer: "Area", x: 239, y: 486, w: 1442, h: 490,
      fill: "F3F9FF",
      points: [...LINE_PTS, [1681, CHART_BASE], [239, CHART_BASE]] },
    ...LINE_PTS.slice(0, -1).map((p, i) => ({
      type: "line", layer: `Segment ${i + 1}`,
      x1: p[0], y1: p[1], x2: LINE_PTS[i + 1][0], y2: LINE_PTS[i + 1][1],
      color: i < LINE_SPLIT ? "66BFFF" : LIGHT.stat, width: 4,
    })),
    ...LINE_PTS.map(([x, y], i) => ({
      type: "ellipse", layer: `Marker ${i + 1}`,
      x: x - 6, y: y - 6, w: 12, h: 12,
      fill: i <= LINE_SPLIT ? "66BFFF" : LIGHT.stat,
    })),
    valueLabel("Value First", 136, 206, LINE_PTS[0][1] - 38, "$XM", LIGHT.body),
    valueLabel("Value Last", 1578, 206, LINE_PTS[7][1] - 38, "$XM", LIGHT.stat),
    ...LINE_DATA.map(([, label, plan], i) =>
      periodLabel(`Period ${label}`, 136 + i * 206, 206, label,
        plan ? LIGHT.stat : LIGHT.body)),
  ],
};

// ---------------------------------------------------------------- Horizontal Bars

// For a ranking whose category names are too long to sit under a vertical bar. The axis
// is the VERTICAL Ruler at 672; there is no horizontal axis on this one.
const RANK_MAX = 1040;
const RANK = [
  [34, "Dental conferences", true],
  [26, "Paid search", false],
  [18, "Paid social", false],
  [14, "Direct mail", false],
  [8,  "Referral", false],
];
const RANK_PEAK = Math.max(...RANK.map(([v]) => v));

const horizontalBars = {
  name: "Horizontal Bars",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 1822]),
    eyebrow("Demand capture", LIGHT),
    headline("Conferences and search do the work,", "and both compound.", LIGHT),
    ...meta(LIGHT),
    ...RANK.flatMap(([v, label, lead], i) => {
      const b = 346 + i * 142;
      const w = Math.round((v / RANK_PEAK) * RANK_MAX);
      return [
        text(`Row ${i + 1} Label`, 136, b + 52, 496, 38, label,
          { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
        rect(`Row ${i + 1} Bar`, 673, b + 47, w, 48, lead ? LIGHT.stat : "CCEAFF"),
        text(`Row ${i + 1} Value`, 693 + w, b + 56, 120, 30, "XX%",
          { font: ONEST, size: 24, line: 30, color: lead ? LIGHT.stat : LIGHT.body }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Stacked Bars

// Composition over time. Three steps of the same blue, so the split reads as one
// quantity divided rather than three unrelated series. Segment heights come from
// CUMULATIVE boundaries, not from scaling each segment: rounding each one independently
// lets the parts drift off the total.
const STACK_MAX = 490;
const STACK = [
  [[8, 0, 0],   "2024A", false],
  [[12, 4, 1],  "2025A", false],
  [[18, 8, 4],  "2026E", true],
  [[22, 12, 6], "2027E", true],
  [[26, 16, 8], "2028E", true],
];
const STACK_PEAK = Math.max(...STACK.map(([segs]) => segs.reduce((a, b) => a + b, 0)));
const STACK_FILLS = [LIGHT.stat, "66BFFF", "CCEAFF"];

const stackedBars = {
  name: "Stacked Bars",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 1822]),
    rulerH(CHART_BASE, LIGHT, 96, 1728),
    eyebrow("Revenue mix", LIGHT),
    headline("The platform brings them in,", "the AI teammates grow them.", LIGHT),
    ...meta(LIGHT),
    ...keySquare(136, LIGHT.stat, "Platform", LIGHT.body),
    ...keySquare(298, "66BFFF", "Clinical", LIGHT.body),
    ...keySquare(445, "CCEAFF", "Revenue", LIGHT.body),
    ...STACK.flatMap(([segs, label, plan], i) => {
      const x = 136 + i * 372;
      const px = (v) => Math.round((v / STACK_PEAK) * STACK_MAX);
      let cum = 0;
      const rects = segs.flatMap((s, k) => {
        const from = px(cum);
        cum += s;
        const to = px(cum);
        return to === from ? [] : [rect(`Stack ${label} ${k + 1}`,
          x, CHART_BASE - to, 160, to - from, STACK_FILLS[k])];
      });
      const total = px(segs.reduce((a, b) => a + b, 0));
      return [
        ...rects,
        valueLabel(`Total ${label}`, x, 160, CHART_BASE - total - 38, "$XM",
          plan ? LIGHT.stat : LIGHT.body),
        periodLabel(`Period ${label}`, x, 160, label, plan ? LIGHT.stat : LIGHT.body),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Waterfall

// A bridge from A to B. The peak scales to 440, NOT 490: the tallest point is the middle
// step and its label sits above it inside the plot - at 490 that label lands at y −20.
const FALL_MAX = 440;
const FALL = [
  ["2025 ARR",  30, "anchor"],
  ["New",       14, "up"],
  ["Expansion",  8, "up"],
  ["Churn",     -2, "down"],
  ["2026 ARR",  50, "anchor"],
];
const FALL_PEAK = 52; // highest cumulative the bridge reaches
const fallPx = (v) => Math.round((v / FALL_PEAK) * FALL_MAX);
const FALL_FILL = { anchor: LIGHT.stat, up: "66BFFF", down: "E23B7B" };
const FALL_TEXT = { anchor: LIGHT.body, up: "66BFFF", down: "E23B7B" };

const waterfall = {
  name: "Waterfall",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 1822]),
    rulerH(CHART_BASE, LIGHT, 96, 1728),
    eyebrow("ARR bridge", LIGHT),
    headline("New business carries the year,", "and churn barely registers.", LIGHT),
    ...meta(LIGHT),
    ...keySquare(136, "66BFFF", "Increase", LIGHT.body),
    ...keySquare(289, "E23B7B", "Decrease", LIGHT.body),
    ...(() => {
      const out = [];
      let cum = 0;
      const levels = [];
      FALL.forEach(([label, v, kind], i) => {
        const x = 136 + i * 362;
        let top, bottom;
        if (kind === "anchor") { top = fallPx(i === 0 ? v : 50); bottom = 0; }
        else if (kind === "up") { bottom = fallPx(cum); cum += v; top = fallPx(cum); }
        else { top = fallPx(cum); cum += v; bottom = fallPx(cum); }
        if (kind === "anchor" && i === 0) cum = v;
        out.push(rect(`Step ${label}`, x, CHART_BASE - top, 200, top - bottom,
          FALL_FILL[kind]));
        // A decrease labels BELOW its bar: above, it collides with the step before it,
        // and hanging down is also what the quantity does.
        const labelTop = kind === "down"
          ? CHART_BASE - bottom + 8
          : CHART_BASE - top - 38;
        const sign = kind === "up" ? "+$XM" : kind === "down" ? "−$XM" : "$XM";
        out.push(valueLabel(`Value ${label}`, x, 200, labelTop, sign, FALL_TEXT[kind]));
        out.push(periodLabel(`Period ${label}`, x, 200, label,
          i === 4 ? LIGHT.stat : LIGHT.body));
        if (i < 4) levels.push([x + 200, CHART_BASE - (kind === "down" ? bottom : top)]);
      });
      // Connectors are what make five bars read as a bridge instead of an odd column chart.
      levels.forEach(([x, y], i) =>
        out.push(rect(`Connector ${i + 1}`, x, y, 162, 2, LIGHT.rule)));
      return out;
    })(),
  ],
};

// ---------------------------------------------------------------- Chart + Hero Number

// The chart supports; one figure is the headline. Its plot sits in the 864-wide right
// column, so the peak scales to 400 - labels need more air at that width.
const HERO_MAX = 400;
const HERO_BARS = [
  [10, "2024A", false], [17.5, "2025A", false], [30, "2026E", true],
  [40, "2027E", true], [50, "2028E", true],
];
const HERO_PEAK = Math.max(...HERO_BARS.map(([v]) => v));

const chartHero = {
  name: "Chart + Hero Number",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    rulerH(CHART_BASE, LIGHT, 960, 864),
    eyebrow("Efficiency", LIGHT),
    headline("Every dollar in comes back,", "and then some.", LIGHT),
    ...meta(LIGHT),
    ...keySquare(1000, "CCEAFF", "Actual", LIGHT.body),
    ...keySquare(1136, LIGHT.stat, "Plan", LIGHT.stat),
    text("Hero Value", 136, 500, 784, 232, "3.2x",
      { font: ONEST, size: 240, line: 232, track: -0.02, color: LIGHT.stat }),
    text("Hero Caption", 136, 780, 640, 84,
      "return on every dollar of sales and marketing, improving each quarter.",
      { size: 30, line: 42, color: LIGHT.body }),
    ...HERO_BARS.flatMap(([v, label, plan], i) => {
      const x = 1000 + i * 172;
      const h = Math.round((v / HERO_PEAK) * HERO_MAX);
      return [
        rect(`Bar ${label}`, x, CHART_BASE - h, 96, h, plan ? LIGHT.stat : "CCEAFF"),
        valueLabel(`Value ${label}`, x, 96, CHART_BASE - h - 38, "$XM",
          plan ? LIGHT.stat : LIGHT.body),
        periodLabel(`Period ${label}`, x, 96, label, plan ? LIGHT.stat : LIGHT.body),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Two Charts

// A pair of related series. A sub-title over each plot replaces the legend, and both
// share the one axis Ruler across the full content column - that shared baseline is what
// makes them read as a pair rather than two charts that happen to sit together.
const PAIR_MAX = 380;
const PAIR = [
  [136, "CARR, $M", [12, 20, 32, 45]],
  [1000, "Live locations", [180, 260, 380, 520]],
];
const PAIR_YEARS = ["2024", "2025", "2026", "2027"];

const twoCharts = {
  name: "Two Charts",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    rulerH(CHART_BASE, LIGHT, 96, 1728),
    eyebrow("Traction", LIGHT),
    headline("Revenue and customers,", "compounding together.", LIGHT),
    ...meta(LIGHT),
    ...PAIR.flatMap(([ox, subtitle, values], p) => {
      const peak = Math.max(...values);
      return [
        text(`Subtitle ${p + 1}`, ox, 394, 784, 24, subtitle,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.body,
            upper: true }),
        ...values.flatMap((v, i) => {
          const x = ox + i * 216;
          const h = Math.round((v / peak) * PAIR_MAX);
          const last = i === values.length - 1;
          const t = p === 0 ? "$XM" : "XXX";
          return [
            rect(`Plot ${p + 1} Bar ${i + 1}`, x, CHART_BASE - h, 136, h,
              last ? LIGHT.stat : "CCEAFF"),
            valueLabel(`Plot ${p + 1} Value ${i + 1}`, x, 136, CHART_BASE - h - 38, t,
              last ? LIGHT.stat : LIGHT.body),
            periodLabel(`Plot ${p + 1} Period ${i + 1}`, x, 136, PAIR_YEARS[i],
              last ? LIGHT.stat : LIGHT.body),
          ];
        }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Before / After

// Both panels are mirror-identical but for colour, so both inset 40 from their own
// vertical - left text at 136, right at 1000. Items are written to fit one line each at
// 30/38, which is what keeps the two columns pairing up row for row.
const CONTRAST = [
  [136, "Today", LIGHT.metaText, LIGHT.body,
    ["Front desk calls every payer", "Claims coded and submitted by hand",
     "Appeals typed one at a time", "Staff chases every balance"]],
  [1000, "With Archy", LIGHT.stat, LIGHT.label,
    ["Benefits verified before the visit", "AI validation before submission",
     "Appeals drafted automatically", "Self-serve portal collects"]],
];

const beforeAfter = {
  name: "Before / After",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    eyebrow("Revenue cycle", LIGHT),
    headline("What billing looks like today,", "and what it looks like with Archy.", LIGHT),
    ...meta(LIGHT),
    ...CONTRAST.flatMap(([x, label, labelColour, itemColour, items], p) => [
      text(`Panel ${p + 1} Label`, x, 394, 784, 24, label,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: labelColour, upper: true }),
      ...items.map((t, i) =>
        text(`Panel ${p + 1} Item ${i + 1}`, x, 458 + i * 94, 784, 38, t,
          { font: ONEST, size: 30, line: 38, color: itemColour })),
    ]),
  ],
};

// ---------------------------------------------------------------- Competitive Table

// Criteria column 576 + four vendor columns of 288. Presence is a dot and absence is
// nothing at all - that needs no legend, and it means Archy reads as a solid column while
// the competitors are sparse, which is the whole argument of the slide.
const VENDOR_X = [808, 1096, 1384, 1672]; // dot centres: Archy, Legacy, Cloud, RCM
const CRITERIA = [
  ["Cloud-native system of record", [true, false, true, false]],
  ["AI clinical documentation", [true, false, false, false]],
  ["Revenue cycle inside the record", [true, false, false, false]],
  ["Insurance verification agent", [true, false, false, true]],
  ["Single vendor, single login", [true, false, true, false]],
];

const competitiveTable = {
  name: "Competitive Table",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 959, 1247, 1535, 1822]),
    ...[415, 543, 671, 799, 927].map((y) => rulerH(y, LIGHT, 96, 1728)),
    eyebrow("Landscape", LIGHT),
    headline("Everyone bolts onto someone else's record.", "We are the record.", LIGHT),
    ...meta(LIGHT),
    text("Head Capability", 136, 369.5, 496, 22, "Capability",
      { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: LIGHT.metaText, upper: true }),
    ...["Archy", "Legacy PMS", "Cloud PMS", "RCM tool"].map((v, i) =>
      text(`Head ${v}`, 692 + i * 288, 365.5, 248, 30, v,
        { font: ONEST, size: 24, line: 30, align: "center",
          color: i === 0 ? LIGHT.stat : LIGHT.body })),
    ...CRITERIA.flatMap(([label, marks], r) => {
      const y = 417 + r * 128;
      return [
        text(`Row ${r + 1} Criterion`, 136, y + 48, 496, 32, label,
          { font: INTER_MED, size: 22, line: 32, color: LIGHT.label }),
        ...marks.flatMap((on, c) => on
          ? [{ type: "ellipse", layer: `Row ${r + 1} Mark ${c + 1}`,
               x: VENDOR_X[c], y: y + 56, w: 16, h: 16,
               fill: c === 0 ? LIGHT.stat : "AAAAAA" }]
          : []),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Positioning 2×2

// The axes ARE Rulers, at the midpoints of the plot. Direction is carried by two corner
// labels rather than by axis titles, which avoids rotated type entirely - the site has no
// rotations, and a rotated label would also have to survive the pptx export.
const PLOTS = [
  ["Archy", 1480, 460, 32, 30, 38, LIGHT.stat, LIGHT.stat],
  ["RCM point tools", 380, 520, 20, 24, 30, "AAAAAA", LIGHT.body],
  ["Cloud PMS", 1200, 860, 20, 24, 30, "AAAAAA", LIGHT.body],
  ["Legacy server PMS", 280, 900, 20, 24, 30, "AAAAAA", LIGHT.body],
];

const positioning = {
  name: "Positioning 2×2",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    rulerH(700, LIGHT, 96, 1728),
    eyebrow("Positioning", LIGHT),
    headline("Owning the record is the moat,", "and only one of us has it.", LIGHT),
    ...meta(LIGHT),
    text("Axis Label Origin", 136, 1006, 600, 22, "Bolted on · Digitized",
      { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: LIGHT.metaText, upper: true }),
    text("Axis Label Target", 1184, 366, 600, 22, "Owns the record · AI-native",
      { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: LIGHT.metaText,
        upper: true, align: "right" }),
    ...PLOTS.flatMap(([label, x, y, dot, size, line, dotColour, textColour]) => [
      { type: "ellipse", layer: `Plot ${label} Dot`,
        x, y: y + (line - dot) / 2, w: dot, h: dot, fill: dotColour },
      text(`Plot ${label} Label`, x + dot + 16, y, 500, line, label,
        { font: ONEST, size, line, color: textColour }),
    ]),
  ],
};

// ---------------------------------------------------------------- Showcase

// A template carries an image SLOT, never a real capture - the same principle as the
// placeholder portrait circles in Quotes and Team grid. #EEEEEE is the site's own
// hairline grey and reads unmistakably as "a block goes here".
const SLOT_FILL = "EEEEEE";

const captureSlot = (x, y, w, h, colour = LIGHT.metaText) => [
  rect("Capture Slot", x, y, w, h, SLOT_FILL),
  text("Slot Label", x, y + (h - 24) / 2, w, 24, "Capture",
    { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: colour,
      upper: true, align: "center" }),
];

// Source slide 17. No 1056 cap: the image runs past it, and a Ruler cutting across an
// image reads as a scratch.
const captureBleedBottom = {
  name: "Capture Bleed Bottom",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    rulerH(20, LIGHT), rulerH(344, LIGHT),
    eyebrow("Migration platform", LIGHT),
    headline("Every migration,", "tracked.", LIGHT),
    ...meta(LIGHT),
    ...captureSlot(96, 346, 1728, 734),
  ],
};

const splitCopyImage = {
  name: "Split Copy / Image",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    // No 1824 vertical: the capture bleeds off the right trim, so there is no right edge.
    ...lightFrame([96, 959]),
    eyebrow("Platform", LIGHT),
    headline("One record,", "every workflow.", LIGHT),
    ...meta(LIGHT),
    ...captureSlot(960, 346, 960, 710),
    text("Lead", 136, 394, 784, 120,
      "Scheduling, charting, imaging, claims and payments run off one record, so nothing has to be reconciled between tabs.",
      { font: ONEST, size: 30, line: 40, color: LIGHT.label }),
    ...[
      "No bolted-on vendors to reconcile at month end.",
      "One login for the whole practice, front office to chair.",
      "Every AI teammate reads and writes the same chart.",
    ].map((t, i) =>
      text(`Point ${i + 1}`, 136, 562 + i * 72, 784, 32, t,
        { size: 22, line: 32, color: LIGHT.body })),
  ],
};

// Source slide 16. A bento is tiles with GUTTERS, not a ruled grid - ruled cells would
// read as a table of pictures. The headline sits in two merged cells as a tile of type.
const BENTO_TILES = [
  [96, 150], [534, 150], [972, 150], [1410, 150],
  [972, 460], [1410, 460],
  [96, 770], [534, 770], [972, 770], [1410, 770],
];

const bentoGrid = {
  name: "Bento Grid",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    // No header band: the headline lives inside the grid.
    rulerH(20, LIGHT), rulerH(1056, LIGHT),
    ...meta(LIGHT),
    ...BENTO_TILES.map(([x, y], i) => rect(`Tile ${i + 1}`, x, y, 414, 286, SLOT_FILL)),
    eyebrow("Platform", LIGHT),
    { type: "text", layer: "Headline", x: 96, y: 559, w: 852, h: 144,
      runs: [
        { text: "The future of dental software", color: LIGHT.h1 },
        { text: "is here.", color: LIGHT.h2 },
      ],
      font: ONEST, size: 60, line: "single", track: -0.02 },
  ],
};

const captureCentred = {
  name: "Capture Centred",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 1822]),
    eyebrow("Migration platform", LIGHT),
    headline("Every migration,", "tracked.", LIGHT),
    ...meta(LIGHT),
    ...captureSlot(360, 400, 1200, 560),
    text("Caption", 360, 992, 1200, 32,
      "Every migration tracked in one dashboard, from kickoff to go-live.",
      { size: 22, line: 32, color: LIGHT.body }),
  ],
};

const captureFullBleed = {
  name: "Capture Full-bleed",
  canvas: { w: 1920, h: 1080 },
  background: SLOT.bg,
  items: [
    // The slot goes FIRST so everything else sits on top of it. Added last it hides the
    // Rulers, the Meta and the eyebrow.
    rect("Capture Slot", 0, 0, 1920, 1080, SLOT.bg),
    text("Slot Label", 0, 528, 1920, 24, "Capture",
      { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: SLOT.body,
        upper: true, align: "center" }),
    // No 344 cap: there is no header band, and a rule across the image reads as a scratch.
    rulerH(20, SLOT), rulerH(1056, SLOT),
    eyebrow("Migration platform", SLOT),
    ...meta(SLOT),
    text("Caption", 96, 940, 1200, 40, "The front office, running itself.",
      { font: ONEST, size: 30, line: 40, color: SLOT.body }),
  ],
};


// ================================================================ Phase D
//
// Fourteen layouts added after the first twenty-eight, on the same four bases as
// everything else: Cover for the spine layouts, Statement for the blue full-bleed ones,
// Metrics 2×2 for every light grid. Coordinates read out of Paper, not derived.

// ---------------------------------------------------------------- Section Divider

// The section number IS the eyebrow, so there is no separate one - and the title is
// left-aligned, which is what keeps it from reading as a second Statement.
const sectionDivider = {
  name: "Section Divider",
  canvas: { w: 1920, h: 1080 },
  background: BLUE.bg,
  items: [
    rulerH(20, BLUE), rulerH(1056, BLUE),
    ...meta(BLUE),
    text("Section Number", 96, 380, 600, 160, "04",
      { font: ONEST, size: 160, line: 160, track: -0.02, color: BLUE.h2 }),
    text("Section Title", 96, 580, 1500, 128, "Go to market",
      { font: ONEST, size: 128, line: 128, track: -0.02, color: BLUE.h1 }),
  ],
};

// ---------------------------------------------------------------- Closing

// Derived from the Cover so it shares its spine - the 1335 vertical and the wordmark in
// the right column. That is what makes the two read as bookends of the same deck.
const closing = {
  name: "Closing",
  canvas: { w: 1920, h: 1080 },
  background: BLUE.bg,
  items: [
    rulerH(20, BLUE), rulerH(1056, BLUE),
    rect("Ruler V Divider", 1315, 20, 2, 1038, BLUE.rule),
    ...meta(BLUE),
    text("Title", 96, 150, 1100, 128, "Thank you.",
      { font: ONEST, size: 128, line: 128, track: -0.02, color: BLUE.h1 }),
    text("Contact Name", 96, 872, 500, 38, "Jonathan Rat",
      { font: ONEST, size: 30, line: 38, color: BLUE.h1 }),
    text("Contact Detail", 96, 918, 700, 24, "jonathan@archy.com • archy.com",
      { font: INTER_MED, size: 20, line: 24, track: 0.05, color: BLUE.metaText, upper: true }),
    { type: "image", layer: "Archy Wordmark", src: "assets/archy-wordmark.png",
      x: 1464, y: 856, w: 360, h: 140 },
  ],
};

// ---------------------------------------------------------------- Quote Statement

// One quote at Statement scale. Left-aligned, unlike the centred Statement, so the two
// blue full-bleed layouts do not read as the same slide twice.
const quoteStatement = {
  name: "Quote Statement",
  canvas: { w: 1920, h: 1080 },
  background: BLUE.bg,
  items: [
    rulerH(20, BLUE), rulerH(1056, BLUE),
    eyebrow("Retention", BLUE),
    ...meta(BLUE),
    // 120px glyph in a 40px line box - the same deliberately tight setting as Quotes.
    text("Quote Mark", 96, 300, 200, 40, "“",
      { font: ONEST, size: 120, line: 40, color: BLUE.h2 }),
    text("Quote", 96, 380, 1500, 384,
      "We're not spending our days filled with mundane tasks, doing data entry. Everything's just automated with Archy.",
      { font: ONEST_REG, size: 72, line: 96, color: BLUE.h1 }),
    text("Attribution Name", 96, 820, 900, 38, "Dr. Thomas DeChellis",
      { font: ONEST, size: 30, line: 38, color: BLUE.h1 }),
    text("Attribution Practice", 96, 866, 900, 32, "DeChellis & Stonestreet Dentistry",
      { size: 24, line: 32, color: BLUE.h2 }),
  ],
};

// ---------------------------------------------------------------- Agenda

// Eight sections, two columns of four. Ordinal in a fixed 60px slot so every title
// starts on the same lane whatever the number is.
const AGENDA = [
  ["01", "The problem"], ["02", "Why now"], ["03", "Product"], ["04", "RCM lifecycle"],
  ["05", "Retention"], ["06", "Traction"], ["07", "Go to market"], ["08", "The team"],
];

const agenda = {
  name: "Agenda",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    // Inset to the content column, not full-bleed: these separate rows inside one band.
    rulerH(522, LIGHT, 96, 1728), rulerH(699, LIGHT, 96, 1728), rulerH(876, LIGHT, 96, 1728),
    eyebrow("Contents", LIGHT),
    headline("What we'll cover,", "in eight sections.", LIGHT),
    ...meta(LIGHT),
    ...AGENDA.flatMap(([no, title], i) => {
      const x = i < 4 ? 136 : 1000;
      const y = 415 + (i % 4) * 177;
      return [
        text(`Item ${no} No`, x, y, 60, 38, no,
          { font: ONEST, size: 30, line: 38, color: LIGHT.stat }),
        text(`Item ${no} Title`, x + 80, y, 680, 38, title,
          { font: ONEST, size: 30, line: 38, color: LIGHT.label }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Logo Wall

// A logo slot is a filled rect plus a centred label, the same construction as an image
// slot in Showcase - a template carries the slot, never a real mark.
const logoSlot = (x, y, layer = "Logo Slot") => [
  rect(layer, x, y, 240, 80, SLOT_FILL),
  text("Slot Label", x, y + 29, 240, 22, "Logo",
    { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: LIGHT.metaText,
      upper: true, align: "center" }),
];

const logoWall = {
  name: "Logo Wall",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 527, 959, 1391, 1822]),
    rulerH(522, LIGHT), rulerH(699, LIGHT), rulerH(876, LIGHT),
    eyebrow("Customers", LIGHT),
    headline("Practices that switched,", "and stayed.", LIGHT),
    ...meta(LIGHT),
    // 16 slots, each centred in its 432 × 177 cell.
    ...Array.from({ length: 16 }, (_, i) =>
      logoSlot(192 + (i % 4) * 432, 394 + Math.floor(i / 4) * 178, `Logo Slot ${i + 1}`)
    ).flat(),
  ],
};

// ---------------------------------------------------------------- Hero Testimonial

// One vertical and two caps: a spine, like the Cover. The portrait column and the quote
// column are what the rule separates, so there is nothing for outer verticals to do.
const heroTestimonial = {
  name: "Hero Testimonial",
  canvas: { w: 1920, h: 1080 },
  background: BLUE.bg,
  items: [
    rulerH(20, BLUE), rulerH(1056, BLUE),
    rect("Ruler V Divider", 640, 20, 2, 1038, BLUE.rule),
    eyebrow("Customer voice", BLUE),
    ...meta(BLUE),
    { type: "ellipse", layer: "Portrait", x: 136, y: 360, w: 240, h: 240, fill: "CCEAFF" },
    text("Attribution Name", 136, 660, 460, 38, "Dr. Anna Weiss",
      { font: ONEST, size: 30, line: 38, color: BLUE.h1 }),
    text("Attribution Practice", 136, 706, 460, 32, "Weiss Family Dental • Portland, OR",
      { size: 24, line: 32, color: BLUE.h2 }),
    text("Quote Mark", 704, 340, 200, 40, "“",
      { font: ONEST, size: 120, line: 40, color: BLUE.h2 }),
    text("Quote", 704, 420, 1088, 320,
      "We ran three systems and a fax machine. Archy replaced all of it in a fortnight, and my front desk got two hours a day back.",
      { font: ONEST_REG, size: 60, line: 80, color: BLUE.h1 }),
  ],
};

// ---------------------------------------------------------------- Case Study

// The left column is a real flex column in Paper (gap 56) rather than four pinned
// blocks: pinning the first body to three lines when the copy runs to two opens a gap
// between two pieces of text that should be tight. The y values here are the resolved
// result of that flex, read back out of Paper.
const CASE_STATS = [
  [406, "6 weeks", "To full migration"],
  [644, "9 to 4 days", "Claims turnaround"],
  [881, "+1 site", "Opened with no new admin"],
];

const caseStudy = {
  name: "Case Study",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    // Segments spanning the right column only - the three stats are inside one cell.
    rulerH(582, LIGHT, 960, 864), rulerH(819, LIGHT, 960, 864),
    eyebrow("Case study", LIGHT),
    headline("Four locations, two systems,", "one platform.", LIGHT),
    ...meta(LIGHT),
    ...logoSlot(136, 394),
    text("Context Label", 136, 530, 784, 24, "The practice",
      { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.metaText, upper: true }),
    text("Context Body", 136, 566, 784, 64,
      "Four locations running two different PMS installs, paper charts at one site, and a claims backlog of nine weeks.",
      { size: 22, line: 32, color: LIGHT.body }),
    text("Result Label", 136, 686, 784, 24, "What changed",
      { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.metaText, upper: true }),
    text("Result Body", 136, 722, 784, 96,
      "One system across all four sites in six weeks. Claims now clear in four days, and the group opened its fifth location without adding a single admin hire.",
      { size: 22, line: 32, color: LIGHT.body }),
    ...CASE_STATS.flatMap(([y, v, l], i) => [
      text(`Stat ${i + 1} Value`, 1000, y, 784, 84, v,
        { font: ONEST, size: 80, line: 84, track: -0.02, color: LIGHT.stat }),
      text(`Stat ${i + 1} Label`, 1000, y + 92, 784, 24, l,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.body, upper: true }),
    ]),
  ],
};

// ---------------------------------------------------------------- Team 3-up

const FOUNDERS = [
  [136, "Jonathan Rat", "Co-founder & CEO",
    "Built and sold a practice-management platform to 900 clinics. Ten years inside dental operations before that."],
  [712, "Maya Okonkwo", "Co-founder & CTO",
    "Led imaging and claims infrastructure at a top-three PMS vendor. Shipped the first cloud charting stack in the category."],
  [1288, "Daniel Ferreira", "Chief Revenue Officer",
    "Scaled two vertical SaaS companies from $4M to $60M ARR, both selling into owner-operated clinics."],
];

const team3up = {
  name: "Team 3-up",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 1247, 1822]),
    eyebrow("Founders", LIGHT),
    headline("The team that has done this,", "twice before.", LIGHT),
    ...meta(LIGHT),
    ...FOUNDERS.flatMap(([x, name, role, bio], i) => [
      { type: "ellipse", layer: `Member ${i + 1} Portrait`,
        x, y: 394, w: 200, h: 200, fill: "CCEAFF" },
      text(`Member ${i + 1} Name`, x, 640, 496, 38, name,
        { font: ONEST, size: 30, line: 38, track: -0.01, color: LIGHT.label }),
      text(`Member ${i + 1} Role`, x, 686, 496, 24, role,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: LIGHT.stat, upper: true }),
      text(`Member ${i + 1} Bio`, x, 734, 496, 96, bio,
        { size: 22, line: 32, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Press & Investors

// Two bands split by one full-bleed Ruler. The label sits in the first column of the
// four-column grid and the three slots in the other three, so the row is ruled rather
// than boxed.
const VALIDATION = [
  [346, "Investors", "$100M raised to date"],
  [702, "Press", "Selected coverage, 2025\u201426"],
];

const pressInvestors = {
  name: "Press & Investors",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 527, 959, 1391, 1822]),
    rulerH(700, LIGHT),
    eyebrow("Validation", LIGHT),
    headline("Backed by the funds that know this market,",
      "covered by the press that watches it.", LIGHT),
    ...meta(LIGHT),
    ...VALIDATION.flatMap(([band, label, note], i) => [
      text(`Band ${i + 1} Label`, 136, band + 138, 352, 38, label,
        { font: ONEST, size: 30, line: 38, track: -0.01, color: LIGHT.label }),
      text(`Band ${i + 1} Note`, 136, band + 184, 352, 32, note,
        { size: 22, line: 32, color: LIGHT.body }),
      ...[624, 1056, 1488].flatMap((x, j) =>
        logoSlot(x, band + 137, `Band ${i + 1} Logo Slot ${j + 1}`)),
    ]),
  ],
};

// ---------------------------------------------------------------- Columns 2-up

// Two wide columns, so the title steps up to the 40/48 tier. Titles carry a forced break
// - a one-line title beside a two-line one drops off the body's shared lane.
const TWO_UP = [
  [136, "01", ["Every clinical record", "in one chart"],
    "Charting, imaging, perio and treatment plans share one record, so a hygienist never leaves the chair to look something up. No sync, no second login, no version of the truth living on a server in the back office."],
  [1000, "02", ["Revenue that closes", "itself"],
    "Claims are coded from the chart, scrubbed before they leave, and reconciled against the deposit when they land. The front desk stops chasing payers and starts scheduling the next visit."],
];

const columns2up = {
  name: "Columns 2-up",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 959, 1822]),
    eyebrow("How it works", LIGHT),
    headline("Two things change on day one,", "and everything else follows.", LIGHT),
    ...meta(LIGHT),
    ...TWO_UP.flatMap(([x, no, title, body], i) => [
      text(`Column ${i + 1} Ordinal`, x, 394, 784, 96, no,
        { font: ONEST, size: 96, line: 96, track: -0.02, color: LIGHT.stat }),
      lines(`Column ${i + 1} Title`, x, 530, 784, 96, title,
        { font: ONEST, size: 40, line: 48, track: -0.02, color: LIGHT.label }),
      text(`Column ${i + 1} Body`, x, 666, 784, 96, body,
        { size: 22, line: 32, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Columns 3-up

const THREE_UP = [
  [136, "01", ["Land a single", "location"],
    "Owner-operated clinics buy in weeks, not quarters, and they migrate themselves over a weekend."],
  [712, "02", ["Expand across", "the group"],
    "One site proves the model, and the remaining locations follow inside two quarters at no new sales cost."],
  [1288, "03", ["Own the whole", "workflow"],
    "Payments, insurance and financing attach on top of the chart, and each one raises revenue per clinic."],
];

const columns3up = {
  name: "Columns 3-up",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 1247, 1822]),
    eyebrow("Go to market", LIGHT),
    headline("One clinic at a time,", "then the whole group.", LIGHT),
    ...meta(LIGHT),
    ...THREE_UP.flatMap(([x, no, title, body], i) => [
      text(`Column ${i + 1} Ordinal`, x, 394, 496, 96, no,
        { font: ONEST, size: 96, line: 96, track: -0.02, color: LIGHT.stat }),
      lines(`Column ${i + 1} Title`, x, 526, 496, 76, title,
        { font: ONEST, size: 30, line: 38, track: -0.01, color: LIGHT.label }),
      text(`Column ${i + 1} Body`, x, 634, 496, 96, body,
        { size: 22, line: 32, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Icon List

// Five rows of 142 in the 710 band, separated by full-bleed Rulers ON the boundaries -
// the Rulers frame is an overlay, so the rows keep their full height.
// The icon (40), the 30/38 title and the 22/32 body are offset by 45 / 46 / 49 so their
// three line boxes share one optical centre. Guessing one number for all three puts the
// icon a few pixels off the title's baseline, which is visible at this scale.
const SURFACES = [
  ["icon-scribe", "Charting",
    "Perio, restorative and treatment plans in one record, dictated or tapped."],
  ["icon-imaging", "Imaging",
    "Sensors and pan units write straight to the chart, with no bridge software."],
  ["icon-revenue", "Claims",
    "Coded from the chart, scrubbed before submission, reconciled on deposit."],
  ["icon-verify-royal", "Insurance",
    "Eligibility and benefits verified before the patient walks in the door."],
  ["icon-insight-royal", "Reporting",
    "Production, collections and chair utilisation per provider, per location."],
];

const iconList = {
  name: "Icon List",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 1822]),
    rulerH(488, LIGHT), rulerH(630, LIGHT), rulerH(772, LIGHT), rulerH(914, LIGHT),
    eyebrow("The platform", LIGHT),
    headline("Five surfaces, one record,", "no integrations to maintain.", LIGHT),
    ...meta(LIGHT),
    ...SURFACES.flatMap(([icon, title, body], i) => {
      const row = 346 + i * 142;
      return [
        { type: "image", layer: `Row ${i + 1} Icon`, src: `assets/${icon}.png`,
          x: 136, y: row + 45, w: 40, h: 40 },
        text(`Row ${i + 1} Title`, 200, row + 46, 431, 38, title,
          { font: ONEST, size: 30, line: 38, track: -0.01, color: LIGHT.label }),
        text(`Row ${i + 1} Body`, 711, row + 49, 1073, 32, body,
          { size: 22, line: 32, color: LIGHT.body }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Timeline

// The axis is --color-neutral-lighter, one step darker than a Ruler, and it is the only
// place in the system where that happens. At --color-light-border it is the same weight
// as the column verticals it crosses, so nothing tells you which line is the timeline.
// Marks sit at the content edge of their column, not centred in it, so every label
// left-aligns to the same lane as the eyebrow and the headline do.
const MILESTONES = [
  [136, "Q1 2025", false, "Charting GA",
    "Perio, restorative and treatment plans in one record."],
  [568, "Q4 2025", false, "Revenue cycle",
    "Claims scrubbing and posting attached to the chart."],
  [1000, "Q2 2026", true, "Insurance",
    "Eligibility, benefits and card-present payments."],
  [1432, "Q1 2027", true, "Multi-site",
    "Group reporting and cross-location scheduling."],
];

const timeline = {
  name: "Timeline",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 527, 959, 1391, 1822]),
    rect("Ruler H Axis", 96, 664, 1728, 2, "CCCCCC"),
    eyebrow("Milestones", LIGHT),
    headline("Where we have been,", "and where this goes.", LIGHT),
    ...meta(LIGHT),
    // Same actual/plan colour split as the charts: shipped is blue-tint-200 with neutral
    // labels, planned is royal blue. The claim is identical, so the coding is too.
    ...MILESTONES.flatMap(([x, period, planned, title, body], i) => [
      text(`Milestone ${i + 1} Period`, x, 584, 360, 38, period,
        { font: ONEST, size: 30, line: 38, track: -0.01,
          color: planned ? LIGHT.stat : LIGHT.body }),
      { type: "ellipse", layer: `Milestone ${i + 1} Mark`,
        x, y: 655, w: 20, h: 20, fill: planned ? LIGHT.stat : "CCEAFF" },
      text(`Milestone ${i + 1} Title`, x, 704, 360, 38, title,
        { font: ONEST, size: 30, line: 38, track: -0.01, color: LIGHT.label }),
      text(`Milestone ${i + 1} Body`, x, 750, 360, 64, body,
        { size: 22, line: 32, color: LIGHT.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Roadmap

// Three phases, four items each, items separated by Rulers inset to their own column.
// No Status pill: the pill has two states and a roadmap has three, so the timeframe
// carries the state in its colour instead - royal / neutral / neutral-light.
// Items are centred in their 100px row rather than sitting at its top, so each Ruler
// falls equidistant between the two items it separates.
const PHASES = [
  [136, "Shipping now", "013DF5", "The record",
    ["Charting, perio and treatment plans", "Imaging capture and storage",
     "Scheduling and recall", "Claims submission and posting"]],
  [712, "Next twelve months", "666666", "The money",
    ["Eligibility and benefits checks", "Card-present payments at the chair",
     "Patient financing", "Automated denials work queue"]],
  [1288, "Beyond 2027", "AAAAAA", "The group",
    ["Cross-location scheduling", "Group-level revenue reporting",
     "Staffing and labour planning", "Hardware and supply procurement"]],
];

const roadmap = {
  name: "Roadmap",
  canvas: { w: 1920, h: 1080 },
  background: LIGHT.bg,
  items: [
    ...lightFrame([96, 671, 1247, 1822]),
    ...PHASES.flatMap(([x]) =>
      [660, 760, 860].map((y) => ({ ...rulerH(y, LIGHT, x, 496), layer: "Ruler Item" }))),
    eyebrow("Roadmap", LIGHT),
    headline("The record first, the money second,", "the group last.", LIGHT),
    ...meta(LIGHT),
    ...PHASES.flatMap(([x, when, whenColour, title, items], i) => [
      text(`Phase ${i + 1} Timeframe`, x, 394, 496, 24, when,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: whenColour, upper: true }),
      text(`Phase ${i + 1} Title`, x, 440, 496, 48, title,
        { font: ONEST, size: 40, line: 48, track: -0.02, color: LIGHT.label }),
      ...items.map((it, j) =>
        text(`Phase ${i + 1} Item ${j + 1}`, x, 594 + j * 100, 496, 32, it,
          { size: 22, line: 32, color: LIGHT.body })),
    ]),
  ],
};


// ================================================================ The dark set
//
// Thirteen layouts on --color-dark-background. The header inversion on a dark ground is a
// FIXED mapping in CLAUDE.md, which means a dark version of an existing layout is a free
// recolour - and a recolour is not a layout. So every one of these is a distribution that
// does not exist on light, and each is a slide whose job is to be a BEAT in the deck
// rather than a page of information. That is what a dark ground is for here, and it is
// why `Big Number` and `Matrix` were dark long before this set existed.
//
// The ground is flat --color-dark-background, not the dark gradient CLAUDE.md defines for
// posters: pptxgenjs supports no gradient fills, so a gradient ground would have to go in
// as a background image on every slide and stop being an editable shape. `Capture +
// Scrim` is the one place a raster is unavoidable, and it is one image rather than
// thirteen.

// Two caps and nothing else - used by the layouts with no header band at all.
const darkCaps = () => [rulerH(20, DARK), rulerH(1056, DARK)];

// ---------------------------------------------------------------- Manifesto

// Three claims set solid at the Cover-title tier, in the LOWER two thirds. Everything
// else in the library starts its content at 344; this one leaves that whole band empty
// and lets the void carry the weight, which only works on a dark ground.
const MANIFESTO = [
  ["We own the record.", DARK.h1],
  ["We automate the work.", DARK.h1],
  ["We move the money.", DARK.stat],
];

const manifesto = {
  name: "Manifesto",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...darkCaps(),
    eyebrow("What we are", DARK),
    ...meta(DARK),
    ...MANIFESTO.map(([t, colour], i) =>
      text(`Line ${i + 1}`, 96, 560 + i * 148, 1728, 128, t,
        { font: ONEST, size: 128, line: 128, track: -0.02, color: colour })),
  ],
};

// ---------------------------------------------------------------- The Ask

// Anchored to the top AND the bottom with a deliberate void between them: copy above the
// 800 Ruler, the use-of-funds band below it. The three figures sit at 96 / 672 / 1248 -
// the column boundaries themselves, not a cell's 40px inset - because there are no
// verticals for them to sit inside.
const USE_OF_FUNDS = [
  [96, "45%", "Engineering & product"],
  [672, "35%", "Go to market"],
  [1248, "20%", "Runway & operations"],
];

const theAsk = {
  name: "The Ask",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...darkCaps(),
    rulerH(800, DARK),
    eyebrow("The ask", DARK),
    ...meta(DARK),
    { type: "text", layer: "Headline", x: 96, y: 320, w: 1728, h: 192,
      runs: [
        { text: "We're raising $60M", color: DARK.h1 },
        { text: "to reach 6,000 clinics.", color: DARK.h2 },
      ],
      font: ONEST, size: 96, line: 96, track: -0.02 },
    text("Lead", 96, 572, 1100, 80,
      "Two years of runway at the current burn, and the last raise before Archy is default-alive.",
      { size: 30, line: 40, color: DARK.body }),
    ...USE_OF_FUNDS.flatMap(([x, v, l], i) => [
      text(`Split ${i + 1} Value`, x, 866, 500, 84, v,
        { font: ONEST, size: 80, line: 84, track: -0.02, color: DARK.stat }),
      text(`Split ${i + 1} Label`, x, 964, 500, 24, l,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: DARK.body, upper: true }),
    ]),
  ],
};

// ---------------------------------------------------------------- Number Full-bleed

// 480/440 - the largest type in the deck, 1.5x `Big Number`'s 320 and 3.75x the Cover
// title. It does not literally bleed off the trim (a five-glyph figure at 480 measures
// ~1330 of the 1728 column) but it is the whole slide, which is the point. No header
// band: a headline would compete with it.
const numberFullBleed = {
  name: "Number Full-bleed",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...darkCaps(),
    eyebrow("Scale", DARK),
    ...meta(DARK),
    text("Hero Value", 96, 380, 1728, 440, "6,000",
      { font: ONEST, size: 480, line: 440, track: -0.02, color: DARK.stat }),
    text("Hero Caption", 96, 880, 1200, 80,
      "practices on Archy by the end of 2027 \u2014 one in twenty in the United States.",
      { size: 30, line: 40, color: DARK.body }),
  ],
};

// ---------------------------------------------------------------- Two Numbers

// One full-height vertical and two peers. Both values are --color-blue-tint-300: the
// "secondary value goes light-text" exception applies to a value sitting BESIDE a primary
// one, and these two are being compared, not ranked.
const TWO_NUMBERS = [
  [96, "$4.2B", "Spent every year on software, payments and financing by US dental practices."],
  [1000, "0.3%", "Of it captured today by the largest cloud-native vendor in the category."],
];

const twoNumbers = {
  name: "Two Numbers",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...darkCaps(),
    rect("Ruler V Divider", 959, 20, 2, 1038, DARK.rule),
    eyebrow("The gap", DARK),
    ...meta(DARK),
    ...TWO_NUMBERS.flatMap(([x, v, claim], i) => [
      text(`Half ${i + 1} Value`, x, 340, 768, 240, v,
        { font: ONEST, size: 240, line: 240, track: -0.02, color: DARK.stat }),
      text(`Half ${i + 1} Claim`, x, 620, 768, 120, claim,
        { font: ONEST, size: 30, line: 40, track: -0.01, color: DARK.h1 }),
    ]),
  ],
};

// ---------------------------------------------------------------- Cohort Curves

// The same plot geometry as `Line / Area` - 8 columns of 206, marks at 239 + 206n, the
// shared baseline at CHART_BASE - but three series from one origin instead of one.
//
// **On a dark ground the series steps are sky-blue-400 / blue-tint-300 / blue-tint-200.**
// --color-royal-blue-500 is the forecast colour on light and it DISAPPEARS against navy,
// the exact inverse of blue-tint-200 vanishing against white. Newest cohort is brightest.
//
// The axis starts at 85%, not 0: at full scale three curves between 88 and 100 are one
// thick line. The legend row carries that as a right-aligned note, which is where chart
// metadata belongs.
const COHORTS = [
  ["0095FF", "2024 cohort \u2014 88%", [486, 617, 715, 780, 813, 845, 845, 878]],
  ["66BFFF", "2025 cohort \u2014 92%", [486, 584, 649, 682, 715, 715, 747, 747]],
  ["CCEAFF", "2026 cohort \u2014 96%", [486, 551, 584, 617, 617]],
];

const COHORT_PERIODS = ["M0", "M3", "M6", "M9", "M12", "M18", "M24", "M30"];

// A polyline as N `line` items. build.js has no polyline primitive and does not need one:
// the segments are what a drawn chart is made of, and they stay real shapes in Slides.
const polyline = (layer, ys, colour) =>
  ys.slice(0, -1).map((y, i) => ({
    type: "line", layer: `${layer} ${i + 1}`,
    x1: 239 + i * 206, y1: y, x2: 239 + (i + 1) * 206, y2: ys[i + 1],
    color: colour, width: 4,
  }));

const cohortCurves = {
  name: "Cohort Curves",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...lightFrame([96, 1822], DARK),
    rulerH(CHART_BASE, DARK, 96, 1728),
    eyebrow("Retention by cohort", DARK),
    headline("Every cohort retains better", "than the one before it.", DARK),
    ...meta(DARK),
    ...COHORTS.flatMap(([colour, label], i) => keyLine(136 + i * 300, colour, label, DARK.body)),
    text("Axis Note", 1384, 394, 400, 22, "Axis starts at 85%",
      { font: INTER, size: 18, line: 22, track: 0.05, color: DARK.body,
        upper: true, align: "right" }),
    ...COHORTS.flatMap(([colour, , ys], i) => polyline(`Cohort ${i + 1}`, ys, colour)),
    ...COHORT_PERIODS.map((p, i) => periodLabel(`Period ${i + 1}`, 136 + i * 206, 206, p, DARK.body)),
  ],
};

// ---------------------------------------------------------------- Market Sizing

// Three blocks nested from a shared bottom-left corner rather than concentrically, so the
// three legend rows to the right can sit on their own lanes. Blue gets brighter as the
// market narrows - the reverse of a heat map, and it puts the accent on the reachable one.
//
// **Nested rectangles encode AREA, so the geometry is derived by scaling both dimensions
// by sqrt(ratio) - never by eye.** The first version was drawn by hand and put SOM at 11%
// of TAM's area when the data says 4.3%: a chart misrepresenting its own numbers, and the
// same defect CLAUDE.md's rule about data-derived bar heights exists to prevent.
//
// **Each block is labelled in place, at its own top-left with a 24px inset.** The first
// fix was a swatch beside each legend row, and a swatch is the wrong device here: it is
// what you reach for when a mark is too small or too numerous to name (a bar in a series),
// and there are exactly three blocks, all big enough to hold their tier. A label inside
// the mark needs no decoding at all - and once the block is named the swatch has no job
// left, so it came back out. Two keys for one mapping is noise.
//
// The share of TAM lives in the note, so the ratio the whole slide is about is stated in
// words as well as in area.
const MARKET_BLOCK = { w: 784, h: 560, x: 136, bottom: 960 };

// [value, legend row y, tier, value label, block fill, ink on that fill, note]
// The ink inverts on the two lightest fills, same rule as `Cost Stack`'s segments.
const MARKET = [
  [4.2, 370, "TAM", "$4.2B", "0000C9", DARK.h1,
    "Every dollar US practices spend on software, payments and financing."],
  [1.6, 608, "SAM", "$1.6B", "013DF5", DARK.h1,
    "38% of TAM \u2014 cloud-ready single- and multi-location practices in our footprint."],
  [0.18, 845, "SOM", "$180M", "66BFFF", "00004E",
    "4% of TAM \u2014 reachable at current sales capacity by the end of 2028."],
];

const MARKET_TAM = MARKET[0][0];
const marketBlock = (v) => {
  const s = Math.sqrt(v / MARKET_TAM);
  const w = Math.round(MARKET_BLOCK.w * s);
  const h = Math.round(MARKET_BLOCK.h * s);
  return { w, h, y: MARKET_BLOCK.bottom - h };
};

const marketSizing = {
  name: "Market Sizing",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...lightFrame([96, 959, 1822], DARK),
    rulerH(582, DARK, 960, 864), rulerH(819, DARK, 960, 864),
    eyebrow("Market", DARK),
    headline("A $4.2B market where the", "leader holds almost none of it.", DARK),
    ...meta(DARK),
    // Largest first: each block sits on top of the one that contains it.
    ...MARKET.map(([v, , label, , fill]) => {
      const b = marketBlock(v);
      return rect(`${label} Block`, MARKET_BLOCK.x, b.y, b.w, b.h, fill);
    }),
    // Then the tier names on top of all three, each on its own block's exposed corner.
    ...MARKET.map(([v, , label, , , ink]) => {
      const b = marketBlock(v);
      return text(`${label} Label`, MARKET_BLOCK.x + 24, b.y + 24, b.w - 48, 38, label,
        { font: ONEST, size: 30, line: 38, track: -0.01, color: ink });
    }),
    ...MARKET.flatMap(([, y, label, v, , , note], i) => [
      text(`Tier ${i + 1} Label`, 1000, y, 784, 24, label,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: DARK.body, upper: true }),
      text(`Tier ${i + 1} Value`, 1000, y + 32, 784, 84, v,
        { font: ONEST, size: 80, line: 84, track: -0.02, color: DARK.stat }),
      text(`Tier ${i + 1} Note`, 1000, y + 124, 784, 64, note,
        { size: 22, line: 32, color: DARK.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Platform Stack

// Four full-width horizontal bands of UNEQUAL height, which nothing else in the library
// does - every other grid divides its band evenly. The foundation gets 230 against the
// other three at 160, and its label steps up to 40/48 in the accent. That is the whole
// argument of the slide expressed as geometry rather than as a caption.
const LAYERS = [
  [346, 160, "Surfaces", "Charting, imaging, scheduling, front desk, patient app", false],
  [506, 160, "AI teammates", "Scribe, claims review, eligibility, denials, recall", false],
  [666, 160, "Workflow engine", "The events every one of those agents reads and writes", false],
  [826, 230, "The record", "One patient chart. No integrations, no sync, no second source of truth.", true],
];

const platformStack = {
  name: "Platform Stack",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    rulerH(20, DARK), rulerH(344, DARK), rulerH(1056, DARK),
    rulerV(96, 344, 714, DARK), rulerV(1822, 344, 714, DARK),
    // One vertical at 608: the boundary between the label lane and the contents, and the
    // only column boundary this layout has.
    rulerV(608, 344, 714, DARK),
    rulerH(506, DARK), rulerH(666, DARK), rulerH(826, DARK),
    eyebrow("Architecture", DARK),
    headline("Four layers, and only one", "of them is the moat.", DARK),
    ...meta(DARK),
    ...LAYERS.flatMap(([row, h, label, contents, base], i) => [
      text(`Layer ${i + 1} Label`, 96, row + (base ? 91 : 61), 480, base ? 48 : 38, label,
        { font: ONEST, size: base ? 40 : 30, line: base ? 48 : 38,
          track: base ? -0.02 : -0.01, color: base ? DARK.stat : DARK.h1 }),
      text(`Layer ${i + 1} Contents`, 648, row + (base ? 99 : 64), 1176, 32, contents,
        { size: 22, line: 32, color: DARK.body }),
    ]),
  ],
};

// ---------------------------------------------------------------- Key-value rows

// Label left, value right-aligned into its own lane past the 1247 vertical. Nothing else
// in the library right-aligns anything, and that lane is the whole device: a terms sheet
// is read down the values, not across the rows.
const TERMS = [
  ["Round", "Series B"],
  ["Raising", "$60M"],
  ["Pre-money valuation", "$540M"],
  ["Committed to date", "$38M"],
  ["Target close", "March 2027"],
];

const keyValueRows = {
  name: "Key-value rows",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...lightFrame([96, 1247, 1822], DARK),
    rulerH(488, DARK), rulerH(630, DARK), rulerH(772, DARK), rulerH(914, DARK),
    eyebrow("Terms", DARK),
    headline("The round,", "on one page.", DARK),
    ...meta(DARK),
    ...TERMS.flatMap(([k, v], i) => {
      const y = 398 + i * 142;
      return [
        text(`Row ${i + 1} Key`, 136, y, 1000, 38, k,
          { font: ONEST, size: 30, line: 38, track: -0.01, color: DARK.h1 }),
        text(`Row ${i + 1} Value`, 1288, y, 536, 38, v,
          { font: ONEST, size: 30, line: 38, track: -0.01, color: DARK.stat, align: "right" }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- The Wedge

// The library's only RADIAL composition - everything else is columnar. Six satellites
// converge on one core through two hairline buses, which is the engineering-drawing
// reading of the Rulers taken to its end: the rules are the relationship, so no satellite
// is the banned "element floating with no relationship to anything around it".
const SATELLITES = [
  [96, 400, "Server-based PMS"], [96, 640, "Imaging bridge"], [96, 880, "Claims clearinghouse"],
  [1504, 400, "Payments terminal"], [1504, 640, "Eligibility portal"], [1504, 880, "Phones and fax"],
];

const theWedge = {
  name: "The Wedge",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    rulerH(20, DARK), rulerH(344, DARK), rulerH(1056, DARK),
    eyebrow("Consolidation", DARK),
    headline("Six contracts, six logins,", "six places the data breaks.", DARK),
    ...meta(DARK),
    // The buses sit ON the core's own edges, so no extra segment is needed to reach it.
    rect("Bus Left", 748, 460, 2, 480, DARK.rule),
    rect("Bus Right", 1170, 460, 2, 480, DARK.rule),
    ...[459, 699, 939].flatMap((y, i) => [
      rect(`Lead L${i + 1}`, 416, y, 332, 2, DARK.rule),
      rect(`Lead R${i + 1}`, 1172, y, 332, 2, DARK.rule),
    ]),
    ...SATELLITES.flatMap(([x, y, name], i) => [
      rect(`Satellite ${i + 1}`, x, y, 320, 120, "000484"),
      text(`Satellite ${i + 1} Name`, x, y + 44, 320, 32, name,
        { size: 24, line: 32, color: DARK.h1, align: "center" }),
    ]),
    rect("Core", 750, 591, 420, 220, "013DF5"),
    // The wordmark, not the word. On the royal-blue core it is white - the same
    // treatment as the Cover; only a white or light ground turns it royal blue.
    // 252 x 98 is the mark's native ink, and it is exactly 18:7, so the integer scales
    // are 18k x 7k. That matters here: at 260 x 101 the flex column centred its content
    // at y 41.5 and put both children on sub-pixel positions.
    { type: "image", layer: "Archy Wordmark", src: "assets/archy-wordmark.png",
      x: 834, y: 634, w: 252, h: 98 },
    text("Core Sub", 750, 744, 420, 24, "One record",
      { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: DARK.body,
        upper: true, align: "center" }),
  ],
};

// ---------------------------------------------------------------- Cost Stack

// Two HORIZONTAL stacked bars - `Stacked Bars` is five vertical bars of three segments
// over time, and `Horizontal Bars` is five single bars. This is two bars whose subject is
// the difference between them, and horizontal is the only orientation where five segments
// are wide enough to name themselves inline.
//
// Five blue steps on navy: primary-blue-600 → royal-blue-500 → sky-blue-400 →
// blue-tint-300 → blue-tint-200. The last two are light enough that their labels invert
// to --color-blue-tint-800.
const COST_TODAY = [
  [0, 532, "0000C9", "PMS", DARK.h1],
  [532, 177, "013DF5", "Imaging", DARK.h1],
  [709, 399, "0095FF", "Claims", DARK.h1],
  [1108, 487, "66BFFF", "Payments", "00004E"],
  [1595, 133, "CCEAFF", "Phones", "00004E"],
];

const costStack = {
  name: "Cost Stack",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    rulerH(20, DARK), rulerH(344, DARK), rulerH(1056, DARK),
    // Footer band: the takeaway earns it because it says what the bars do not.
    rulerH(958, DARK),
    eyebrow("Cost of ownership", DARK),
    headline("Five vendors collapse into one,", "and the bill collapses with them.", DARK),
    ...meta(DARK),
    text("Bar 1 Title", 96, 400, 1728, 38, "Today · $3,900 per location, per month",
      { font: ONEST, size: 30, line: 38, track: -0.01, color: DARK.h1 }),
    ...COST_TODAY.flatMap(([dx, w, fill, label, colour], i) => [
      rect(`Segment ${i + 1}`, 96 + dx, 460, w, 120, fill),
      text(`Segment ${i + 1} Label`, 96 + dx, 509, w, 22, label,
        { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: colour,
          upper: true, align: "center" }),
    ]),
    text("Bar 2 Title", 96, 660, 1728, 38, "With Archy · $1,450 per location, per month",
      { font: ONEST, size: 30, line: 38, track: -0.01, color: DARK.h1 }),
    rect("Bar Archy", 96, 720, 642, 120, "013DF5"),
    text("Bar Archy Label", 96, 769, 642, 22, "Archy \u2014 one contract",
      { font: INTER_SEMI, size: 18, line: 22, track: 0.05, color: DARK.h1,
        upper: true, align: "center" }),
    text("Takeaway", 96, 992, 1728, 32,
      "One contract, one login, one bill \u2014 and 63% less per location every month.",
      { font: INTER_MED, size: 22, line: 32, color: DARK.h1 }),
  ],
};

// ---------------------------------------------------------------- Proof Stack

// Three full-width bands each pairing a figure with the sentence behind it. `Quotes` puts
// two long quotes beside a stats column; this interleaves the two content types band by
// band, so every number arrives with its evidence attached.
const PROOF_BANDS = [
  [346, 237, "94%", "Gross revenue retention",
    "“We looked at switching back after month three and could not find a reason to.”",
    "Dr. Thomas DeChellis · DeChellis & Stonestreet"],
  [585, 234, "11 days", "Median time to go live",
    "“We closed on a Friday and charted on Monday. I had budgeted a month for it.”",
    "Dr. Lauren Koch · Avondale Dental Studio"],
  [821, 235, "2.4 hrs", "Saved per day, per front desk",
    "“My front desk stopped staying late. That is the whole review.”",
    "Dr. Anna Weiss · Weiss Family Dental"],
];

const proofStack = {
  name: "Proof Stack",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...lightFrame([96, 1822], DARK),
    rulerV(608, 344, 714, DARK),
    rulerH(583, DARK), rulerH(819, DARK),
    eyebrow("Proof", DARK),
    headline("Three numbers,", "and the sentence behind each.", DARK),
    ...meta(DARK),
    ...PROOF_BANDS.flatMap(([band, h, v, l, quote, who], i) => {
      const statTop = band + Math.round((h - 122) / 2);
      const quoteTop = band + Math.round((h - 116) / 2);
      return [
        text(`Band ${i + 1} Value`, 96, statTop, 480, 84, v,
          { font: ONEST, size: 80, line: 84, track: -0.02, color: DARK.stat }),
        text(`Band ${i + 1} Label`, 96, statTop + 98, 480, 24, l,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: DARK.body, upper: true }),
        text(`Band ${i + 1} Quote`, 648, quoteTop, 1176, 80, quote,
          { font: ONEST_REG, size: 30, line: 40, color: DARK.h1 }),
        text(`Band ${i + 1} Attribution`, 648, quoteTop + 92, 1176, 24, who,
          { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: DARK.body, upper: true }),
      ];
    }),
  ],
};

// ---------------------------------------------------------------- Capture + Scrim

// The first slide layout to use the `BK Fade`, which CLAUDE.md calls mandatory wherever
// bleed art's own edge falls inside the canvas - here the art runs to the trim, so the
// fade exists to make the copy legible rather than to hide an edge.
//
// **It is the one raster in the whole library.** pptxgenjs supports no gradient fills, so
// the scrim goes in as a PNG that `build-assets.py` generates: transparent at the top,
// fully --color-dark-background by 65% of its height. The slot below it and the type above
// it stay real shapes.
const captureScrim = {
  name: "Capture + Scrim",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    // Slot first, then the scrim, then everything else - a full-bleed slot added last
    // covers the Rulers, the Meta and the eyebrow.
    rect("Capture Slot", 0, 0, 1920, 1080, "666666"),
    text("Slot Label", 0, 528, 1920, 24, "Capture",
      { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: "FFFFFF",
        upper: true, align: "center" }),
    { type: "image", layer: "BK Fade", src: "assets/bk-fade-dark.png",
      x: 0, y: 400, w: 1920, h: 680 },
    // No 344 cap: there is no header band, and a rule across an image reads as a scratch.
    ...darkCaps(),
    eyebrow("Product", DARK),
    ...meta(DARK),
    { type: "text", layer: "Headline", x: 96, y: 760, w: 1300, h: 140,
      runs: [
        { text: "Every chair, every provider,", color: DARK.h1 },
        { text: "one schedule.", color: DARK.h2 },
      ],
      font: ONEST, size: 60, line: "single", track: -0.02 },
    text("Body", 96, 932, 1100, 64,
      "Six locations on one calendar, with no double-booking and no phone call to confirm it.",
      { size: 22, line: 32, color: DARK.body }),
  ],
};

// ---------------------------------------------------------------- Screen Trio

// Three tall 260 × 520 slots - a portrait aspect nothing else in Showcase has (`Bento
// Grid` is landscape tiles, `Split Copy / Image` one wide slot).
//
// **On a dark ground a slot fills --color-neutral (#666666), not #EEEEEE.** The pale slot
// is the light-ground rule; on navy three #EEEEEE slabs dominate the slide and read as
// the subject rather than as placeholders. Same reasoning as the full-bleed slot.
const SCREENS = [
  [254, "Front desk"], [830, "Chairside"], [1406, "Owner dashboard"],
];

const screenTrio = {
  name: "Screen Trio",
  canvas: { w: 1920, h: 1080 },
  background: DARK.bg,
  items: [
    ...lightFrame([96, 671, 1247, 1822], DARK),
    eyebrow("The product", DARK),
    headline("One record, three places", "the practice touches it.", DARK),
    ...meta(DARK),
    ...SCREENS.flatMap(([x, caption], i) => [
      rect(`Screen ${i + 1}`, x, 400, 260, 520, "666666"),
      text(`Screen ${i + 1} Slot Label`, x, 648, 260, 24, "Capture",
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: "FFFFFF",
          upper: true, align: "center" }),
      text(`Screen ${i + 1} Caption`, x, 952, 260, 24, caption,
        { font: INTER_SEMI, size: 20, line: 24, track: 0.05, color: DARK.body,
          upper: true, align: "center" }),
    ]),
  ],
};

// ----------------------------------------------------------------

// Grouped by the seven library categories, matching the Paper page each layout lives on.
// The exporter reads `categories` so the generated deck comes out grouped the same way.
const categories = {
  Frames: {
    cover, statement, manifesto, agenda, sectionDivider, quoteStatement, theAsk, closing,
  },
  Numbers: {
    bigNumber, numberFullBleed, twoNumbers, metrics, metrics3up, splitStats,
  },
  Charts: {
    bars, lineArea, cohortCurves, horizontalBars, stackedBars, waterfall,
    chartHero, twoCharts, marketSizing,
  },
  Lists: {
    columns2up, columns3up, columns4up, numberedRows, iconList, productGrid,
    platformStack, keyValueRows, timeline, roadmap,
  },
  Comparisons: {
    comparisonTable, matrix, theWedge, beforeAfter, competitiveTable, costStack,
    positioning,
  },
  Proof: {
    quotes, heroTestimonial, proofStack, caseStudy, logoWall, teamGrid, team3up,
    pressInvestors,
  },
  Showcase: {
    captureBleedBottom, splitCopyImage, bentoGrid, captureCentred, captureScrim,
    screenTrio, captureFullBleed,
  },
};

module.exports = {
  cover, statement, metrics, columns4up, comparisonTable, quotes, teamGrid,
  bigNumber, productGrid, metrics3up, numberedRows, splitStats, bars, matrix,
  beforeAfter, competitiveTable, positioning,
  lineArea, horizontalBars, stackedBars, waterfall, chartHero, twoCharts,
  captureBleedBottom, splitCopyImage, bentoGrid, captureCentred, captureFullBleed,
  sectionDivider, closing, quoteStatement, agenda,
  logoWall, heroTestimonial, caseStudy, team3up, pressInvestors,
  columns2up, columns3up, iconList, timeline, roadmap,
  manifesto, theAsk, numberFullBleed, twoNumbers, cohortCurves, marketSizing,
  platformStack, keyValueRows, theWedge, costStack, proofStack, captureScrim, screenTrio,
};
module.exports.categories = categories;
module.exports.LIGHT = LIGHT;
module.exports.DARK = DARK;
module.exports.BLUE = BLUE;
module.exports.helpers = { rect, rulerH, rulerV, text, lines, meta, eyebrow, headline, lightFrame, footerFrame, footerLine };
module.exports.fonts = { ONEST, ONEST_REG, INTER, INTER_MED, INTER_SEMI };

import { existsSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(dirname(fileURLToPath(import.meta.url)));

const failures = [];

function read(relativePath) {
  return readFileSync(join(repoRoot, relativePath), "utf8");
}

function sha256(relativePath) {
  return createHash("sha256").update(readFileSync(join(repoRoot, relativePath))).digest("hex");
}

function expect(condition, message) {
  if (!condition) failures.push(message);
}

function expectFile(relativePath) {
  expect(existsSync(join(repoRoot, relativePath)), `${relativePath} exists`);
}

function section(content, heading) {
  const start = content.indexOf(heading);
  if (start === -1) return "";
  const rest = content.slice(start + heading.length);
  const nextHeading = rest.search(/\n## /);
  return nextHeading === -1 ? rest : rest.slice(0, nextHeading);
}

function expectOrdered(content, headings, relativePath) {
  let cursor = -1;
  for (const heading of headings) {
    const next = content.indexOf(heading);
    expect(next > cursor, `${relativePath} contains ${heading} in the expected order`);
    cursor = next;
  }
}

const trackingExamples = [
  "references/examples/beispiel-ausgabe-lp1-4.md",
  "references/examples/beispiel-ausgabe-lp5.md",
  "references/examples/beispiel-ausgabe-bim.md",
];

const requiredTailHeadings = [
  "## Aufstellvermerk zum Dokument",
  "## Nachträgliche Anmerkungen zum Dokument",
  "## Anlagen",
  "## Kennzeichnungen im Dokument",
];

for (const examplePath of trackingExamples) {
  expectFile(examplePath);
  const content = read(examplePath);
  expect(!content.includes("_Aufstellvermerk_:"), `${examplePath} does not use the old one-line Aufstellvermerk`);
  expectOrdered(content, requiredTailHeadings, examplePath);

  const kennzeichnungen = section(content, "## Kennzeichnungen im Dokument");
  for (const status of [
    "aktuell/fortgeschrieben",
    "aktuell/angemerkt",
    "überschritten",
    "erledigt",
  ]) {
    expect(kennzeichnungen.includes(status), `${examplePath} documents Kennzeichnung row '${status}'`);
  }
}

const lp5 = read("references/examples/beispiel-ausgabe-lp5.md");
const lp5Kennzeichnungen = section(lp5, "## Kennzeichnungen im Dokument");
const lp5StatusRows = lp5Kennzeichnungen
  .split("\n")
  .filter((line) => /^\| (aktuell\/fortgeschrieben|aktuell\/angemerkt|überschritten|erledigt)\s+\|/.test(line));
expect(lp5StatusRows.length === 4, "LP5 example has exactly the four Kennzeichnung status rows");

expectFile("references/examples/beispiel-transkript-bim.txt");
expectFile("references/examples/beispiel-ausgabe-bim.md");
expectFile("references/examples/beispiel-transkript-eba-interview.txt");
expectFile("references/examples/beispiel-ausgabe-eba-interview.md");
expectFile("references/categories/metadaten-konvention.md");

const readme = read("README.md");
expect(readme.includes("beispiel-transkript-bim.txt"), "README lists the BIM transcript example");
expect(readme.includes("beispiel-ausgabe-bim.md"), "README lists the BIM output example");
expect(readme.includes("beispiel-transkript-eba-interview.txt"), "README lists the EBA interview transcript example");
expect(readme.includes("beispiel-ausgabe-eba-interview.md"), "README lists the EBA interview output example");
expect(readme.includes("Projekt-Nr. 000"), "README documents raw transcript metadata fallbacks");

const bim = read("references/examples/beispiel-ausgabe-bim.md");
expect(bim.includes("### BIM-Koordination JF-07"), "BIM output names the BIM JF variant");
for (const dk of ["1", "2", "3", "4", "5", "6", "7", "8"]) {
  const headerRegex = new RegExp(`^\\| ${dk}\\s+\\| – \\| –\\s+\\| \\*\\*`, "m");
  expect(headerRegex.test(bim), `BIM output contains D/K header ${dk}`);
}
expect(!/^\| 0[1-8]\s+\| – \| –\s+\| \*\*/m.test(bim), "BIM output uses single-digit BIM D/K headers");

const lp14Template = read("references/templates/protokoll-lp1-4.md");
const bimSchema = lp14Template.slice(
  lp14Template.indexOf("Wenn ein BIM-Koordinations-JF protokolliert wird"),
  lp14Template.indexOf("## LN-Konvention"),
);
expect(bimSchema.includes("| 1   | Organisation |"), "LP1-4 template documents BIM D/K as single digits");
expect(!bimSchema.includes("| 01  | Organisation |"), "LP1-4 template no longer documents BIM D/K with leading zero");

const validator = read("agents/protokoll-validator.md");
expect(validator.includes("### 0. Format-Erkennung"), "validator requires format detection before checks");
expect(validator.includes("`gespraechsnotiz`"), "validator documents Gesprächsnotiz format");
expect(validator.includes("`protokoll-einfach`"), "validator documents Protokoll-einfach format");
expect(validator.includes("`protokoll-bim`"), "validator documents BIM format");
expect(
  validator.includes("Kein D/K, kein B, keine LN, keine Status-Spalte verlangen."),
  "validator explicitly avoids D/K and Status requirements for simple formats",
);
expect(
  validator.includes('format: "gespraechsnotiz" | "protokoll-einfach" | "protokoll-lp1-4" | "protokoll-bim" | "protokoll-lp5" | "unklar"'),
  "validator output includes detected format",
);
expect(
  validator.includes("`000` ist ein") &&
    validator.includes("Metadaten sind **Warnungen**, keine Fehler"),
  "validator accepts metadata fallbacks as warnings, not errors",
);

const autoSkill = read("skills/eba-protokoll/SKILL.md");
expect(
  autoSkill.indexOf("**BIM-Protokoll**") < autoSkill.indexOf("**Bauleitungsprotokoll LP5**"),
  "auto-detection checks BIM before LP5",
);
expect(
  autoSkill.includes("BIM-Signale gewinnen vor LP5-Signalen"),
  "auto-detection documents that BIM signals win over LP5",
);
expect(
  autoSkill.includes("Flexible Metadaten bedeuten **nicht** flexible Formatwahl") &&
    autoSkill.includes("metadaten-konvention.md"),
  "auto-detection keeps format choice strict while using metadata fallbacks",
);

const lp5Skill = read("skills/protokoll-lp5/SKILL.md");
expect(
  lp5Skill.includes("Do not use for pure BIM-Koordination"),
  "LP5 skill description excludes pure BIM coordination",
);
expect(
  autoSkill.includes("EBA-Gesprächsnotiz ohne Projektbezug") &&
    autoSkill.includes("ARD/ZDF/rbb/Deutschlandfunk/Magazin") &&
    autoSkill.includes("Projekt-Nummer = 000"),
  "auto-detection supports EBA media/interview notes without project metadata",
);

const gespraechsnotizSkill = read("skills/gespraechsnotiz/SKILL.md");
expect(
  gespraechsnotizSkill.includes("EBA-Interview / Presse / Medien ohne Projekt") &&
    gespraechsnotizSkill.includes("Nicht abbrechen und nicht nach Projektmetadaten fragen") &&
    gespraechsnotizSkill.includes("Projekt-Nummer**: `000`"),
  "Gesprächsnotiz skill documents non-project EBA interview defaults",
);

const interview = read("references/examples/beispiel-ausgabe-eba-interview.md");
expect(interview.includes("| Projekt-Nummer     | 000"), "EBA interview example uses project number 000");
expect(interview.includes("ARD Morgenmagazin / Studio Berlin"), "EBA interview example derives the source/location");
expect(
  interview.includes("Anmerkung: Klärung durch") && !interview.includes("## Fachliche Einordnung"),
  "EBA interview example keeps fachliche Klärung inside Gesprächsinhalt rows",
);

// ─── Template-faithful output pipeline ───────────────────────────────────
//
// Protocol skills must instruct Claude to produce the original QMG source
// format, not Markdown. A central reference describes the pipeline; every
// format skill must cite it.

expectFile("scripts/render_protokoll.py");
expectFile("references/categories/ausgabe-konvention.md");
expectFile("references/templates/qmg/QMG-024-141_ORG-GESPRAECHSNOTIZ_230202-D.docx");
expectFile("references/templates/qmg/QMG-024-141_ORG-PK-LP1-4-MA_230227-A.docx");
expectFile("references/templates/qmg/QMG-024-141_ORG-PK-LP5-MA_230202-B.docx");
expectFile("references/templates/qmg/QMG-024-141_ORG-PK-LP1-4-EXCEL-MA_240920-A.xlsx");
expectFile("references/templates/qmg/QMG-024-141_ORG-PK-EXCEL-MA_240926-C.xlsx");
const qmgTemplateHashes = {
  "references/templates/qmg/QMG-024-141_ORG-GESPRAECHSNOTIZ_230202-D.docx":
    "d89c4b57fa22810c48ae3cec31bb283d283db32a4701081a4454bab8322a3930",
  "references/templates/qmg/QMG-024-141_ORG-PK-LP1-4-MA_230227-A.docx":
    "fed52b658540355e491600d43f8e75f3254855aed7e665e1e843e2e0cc699019",
  "references/templates/qmg/QMG-024-141_ORG-PK-LP5-MA_230202-B.docx":
    "f61a9e4657a1fac2cb0642d35fa22427087630457ff76f988700f7560ecc1a6c",
  "references/templates/qmg/QMG-024-141_ORG-PK-LP1-4-EXCEL-MA_240920-A.xlsx":
    "0026537daffaf3809c273b71e77264848c3bbd569e31f78ded496eabf0177e70",
  "references/templates/qmg/QMG-024-141_ORG-PK-EXCEL-MA_240926-C.xlsx":
    "9db7d927f5f6909be842ec2bd858df4b0985c97578fa420d04245e62c63e808a",
};
for (const [templatePath, expectedHash] of Object.entries(qmgTemplateHashes)) {
  expect(sha256(templatePath) === expectedHash, `${templatePath} matches the original QMG source file`);
}

const ausgabeKonvention = read("references/categories/ausgabe-konvention.md");
expect(
  ausgabeKonvention.includes("render_protokoll.py"),
  "ausgabe-konvention references the renderer",
);
expect(
  ausgabeKonvention.includes("LibreOffice") && ausgabeKonvention.includes("MS Word"),
  "ausgabe-konvention documents Windows PDF converter options",
);
expect(
  ausgabeKonvention.includes("Selbstheilende Umgebung") &&
    ausgabeKonvention.includes("keinen separaten Setup-Schritt"),
  "ausgabe-konvention documents self-healing setup for nontechnical users",
);

const renderer = read("scripts/render_protokoll.py");
const requirements = read("scripts/requirements.txt");
expect(
  renderer.includes("def _bootstrap_requirements()") &&
    renderer.includes("python-docx, openpyxl, or pywin32") &&
    renderer.includes("_bootstrap_package(\"pywin32>=306\")"),
  "renderer bootstraps python-docx, openpyxl and pywin32 automatically",
);
expect(
  requirements.includes("openpyxl>=3.1.0"),
  "requirements include openpyxl for official QMG XLSX output",
);
expect(
  renderer.includes("pdf_required = sys.platform == \"win32\""),
  "renderer treats PDF as required on Windows",
);
expect(
  renderer.includes("GESPRAECHSNOTIZ_TEMPLATE") &&
    renderer.includes("PROTOKOLL_EINFACH_TEMPLATE") &&
    renderer.includes("TRACKING_WORD_TEMPLATE") &&
    renderer.includes("PROTOKOLL_EINFACH_EXCEL_TEMPLATE") &&
    renderer.includes("TRACKING_EXCEL_TEMPLATE") &&
    renderer.includes("def _render_gespraechsnotiz_template") &&
    renderer.includes("def _render_protokoll_einfach_template") &&
    renderer.includes("def _render_simple_excel_template") &&
    renderer.includes("def _render_tracking_template") &&
    renderer.includes("def _is_xlsx_only_format") &&
    renderer.includes("def render_to_xlsx") &&
    renderer.includes("Refusing to render without a supported QMG template") &&
    renderer.includes("page numbering and EBA-CI are preserved"),
  "renderer fills the official QMG Word and Excel templates, keeps Excel formats XLSX-only, and rejects generic output",
);

for (const skillRel of [
  "skills/gespraechsnotiz/SKILL.md",
  "skills/protokoll-einfach/SKILL.md",
  "skills/protokoll-lp1-4/SKILL.md",
  "skills/protokoll-lp5/SKILL.md",
  "skills/protokoll-fortschreiben/SKILL.md",
]) {
  const skill = read(skillRel);
  expect(
    skill.includes("ausgabe-konvention.md"),
    `${skillRel} cites the ausgabe-konvention reference`,
  );
  expect(
    skill.includes("render_protokoll.py"),
    `${skillRel} invokes the render_protokoll.py renderer`,
  );
  expect(
    skill.includes("DOCX") && skill.includes("PDF"),
    `${skillRel} documents DOCX + PDF as the deliverables`,
  );
  expect(
    skill.includes("metadaten-konvention.md"),
    `${skillRel} cites the metadata fallback reference`,
  );
}

for (const skillRel of [
  "skills/protokoll-lp1-4/SKILL.md",
  "skills/protokoll-fortschreiben/SKILL.md",
]) {
  const skill = read(skillRel);
  expect(skill.includes("XLSX"), `${skillRel} documents tracking XLSX output`);
}

const pluginManifest = JSON.parse(read(".claude-plugin/plugin.json"));
expect(pluginManifest.version === "0.2.7", "plugin.json bumped to 0.2.7");
const market = JSON.parse(read(".claude-plugin/marketplace.json"));
expect(
  market.plugins[0].version === "0.2.7",
  "marketplace.json plugin entry bumped to 0.2.7",
);

// Dispatcher smoke test — verify each example transcript would route to the
// correct format skill via the auto-detection heuristic. Mirrors the rules
// documented in skills/eba-protokoll/SKILL.md (Meeting-Anker prinzip).
function classifyTranscript(text, filename) {
  const head = text.split("\n").slice(0, 30).join("\n");
  const speakers = new Set(
    text
      .split("\n")
      .map((l) => l.match(/^\[\d{2}:\d{2}:\d{2}\]\s+([^:]+):/))
      .filter(Boolean)
      .map((m) => m[1].trim()),
  );
  const wordCount = text.split(/\s+/).filter(Boolean).length;
  const bimAnchor =
    /(BIM-Koordination|BIM-Jour-Fixe|BIM-JF\b|Koordinations-JF|BIM-Termin)/.test(head) ||
    /(BIM-PK-JF|EBA_BIM-PK-JF)/.test(filename);
  const lp5Anchor =
    /(Baubesprechung Nr\.|Bauleitungs-JF|Baustellenbegehung|Mängelbegehung|Bauleitung Jour Fixe|OBÜ-Termin|\bLP5\b|\bLPH\s?5\b)/.test(
      head,
    );
  const lp14Anchor =
    /(Planungsbesprechung Nr\.|Jour Fixe Nr\.|JF-\d+|Werkplanungs-JF|Planungs-JF)/.test(head);
  const einfachAnchor =
    /(Kick-Off|Kickoff|Workshop|Erstgespräch|Auftaktbesprechung|\bAuftakt\b|Erstbesprechung)/i.test(head);
  const priorRefs =
    /(letztes Mal|letzte Woche|aus #\d+|LN\s?\d+E|Besprechung Nr\.|Punkt von letzter Woche)/i.test(text);
  const ebaInterviewAnchor =
    /(ARD|ZDF|rbb|Deutschlandfunk|Morgenmagazin|Interview|Pressegespräch|Redaktion|Moderator|Journalist)/i.test(head) &&
    /(Eike Becker|EBA|Eike Becker_Architekten|Architekt)/i.test(text);
  const rawActionTranscript =
    speakers.size >= 3 &&
    /(bis \d{1,2}\.\d{1,2}\.\d{2,4}|KW\s?\d+|übernimmt|schickt|prüft|klärt|Termin|Frist|Aufgabe)/i.test(text);

  if (bimAnchor) return "protokoll-lp1-4-bim";
  if (lp5Anchor) return "protokoll-lp5";
  if (priorRefs || lp14Anchor) return "protokoll-lp1-4";
  if (einfachAnchor && speakers.size >= 3) return "protokoll-einfach";
  if (ebaInterviewAnchor) return "gespraechsnotiz";
  if (rawActionTranscript) return "protokoll-einfach";
  if (
    wordCount < 1500 &&
    speakers.size <= 3 &&
    !lp5Anchor &&
    !bimAnchor &&
    !lp14Anchor &&
    !einfachAnchor
  ) {
    return "gespraechsnotiz";
  }
  return "unklar";
}

const dispatchCases = [
  { file: "references/examples/beispiel-transkript-gespraechsnotiz.txt", expect: "gespraechsnotiz" },
  { file: "references/examples/beispiel-transkript-eba-interview.txt", expect: "gespraechsnotiz" },
  { file: "references/examples/beispiel-transkript-einfach.txt", expect: "protokoll-einfach" },
  { file: "references/examples/beispiel-transkript-lp1-4.txt", expect: "protokoll-lp1-4" },
  { file: "references/examples/beispiel-transkript-lp5.txt", expect: "protokoll-lp5" },
  { file: "references/examples/beispiel-transkript-bim.txt", expect: "protokoll-lp1-4-bim" },
];

for (const { file, expect: expected } of dispatchCases) {
  const text = read(file);
  const filename = file.split("/").pop();
  const got = classifyTranscript(text, filename);
  expect(got === expected, `dispatch heuristic routes ${filename} to ${expected} (got ${got})`);
}

const rawNoProjectTranscript = `
[00:00:02] Becker: Wir starten mit der Abstimmung zur Fassade.
[00:00:14] Scholz: Ich prüfe die Detailzeichnung bis 02.05.26.
[00:00:31] Hubertz: EBA schickt die Materialfreigabe in KW 19.
[00:00:58] Nassif: Dann ist die Frist klar, danke.
`;
expect(
  classifyTranscript(rawNoProjectTranscript, "roh-ohne-projektnummer.txt") === "protokoll-einfach",
  "raw transcript without project metadata but with tasks/deadlines routes to Protokoll-einfach",
);

if (failures.length > 0) {
  console.error(`Reference validation failed with ${failures.length} issue(s):`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("Reference validation passed.");

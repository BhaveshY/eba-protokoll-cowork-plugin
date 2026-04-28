import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(dirname(fileURLToPath(import.meta.url)));

const failures = [];

function read(relativePath) {
  return readFileSync(join(repoRoot, relativePath), "utf8");
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

const readme = read("README.md");
expect(readme.includes("beispiel-transkript-bim.txt"), "README lists the BIM transcript example");
expect(readme.includes("beispiel-ausgabe-bim.md"), "README lists the BIM output example");

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

const autoSkill = read("skills/eba-protokoll/SKILL.md");
expect(
  autoSkill.indexOf("**BIM-Protokoll**") < autoSkill.indexOf("**Bauleitungsprotokoll LP5**"),
  "auto-detection checks BIM before LP5",
);
expect(
  autoSkill.includes("BIM-Signale gewinnen vor LP5-Signalen"),
  "auto-detection documents that BIM signals win over LP5",
);

const lp5Skill = read("skills/protokoll-lp5/SKILL.md");
expect(
  lp5Skill.includes("Do not use for pure BIM-Koordination"),
  "LP5 skill description excludes pure BIM coordination",
);

if (failures.length > 0) {
  console.error(`Reference validation failed with ${failures.length} issue(s):`);
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("Reference validation passed.");

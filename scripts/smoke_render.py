#!/usr/bin/env python3
"""Smoke-test the DOCX renderer against repository examples.

Developer test dependencies:
    python3 -m pip install -r scripts/requirements.txt

This test intentionally uses --no-pdf so it is independent of Word,
LibreOffice, or Pages. PDF conversion is environment-dependent; DOCX content
preservation is the renderer contract this script locks down. End users do not
run this; render_protokoll.py bootstraps its own dependencies.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from docx import Document
except ImportError:
    sys.stderr.write(
        "smoke_render.py: missing dependency 'python-docx'.\n"
        "Install with: python3 -m pip install -r scripts/requirements.txt\n"
    )
    sys.exit(3)


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDERER = REPO_ROOT / "scripts" / "render_protokoll.py"
W_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
QMG_TEMPLATE_EXAMPLES = {
    "references/examples/beispiel-ausgabe-gespraechsnotiz.md",
    "references/examples/beispiel-ausgabe-eba-interview.md",
    "references/examples/beispiel-ausgabe-einfach.md",
    "references/examples/beispiel-ausgabe-lp1-4.md",
    "references/examples/beispiel-ausgabe-lp5.md",
    "references/examples/beispiel-ausgabe-bim.md",
}


def read_docx_text(path: Path) -> str:
    doc = Document(str(path))
    parts: list[str] = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(parts)


def qmg_template_checks(path: Path, example: str) -> list[str]:
    if example not in QMG_TEMPLATE_EXAMPLES:
        return []
    failures: list[str] = []
    with ZipFile(path) as z:
        names = z.namelist()
        body = ET.fromstring(z.read("word/document.xml")).find("w:body", W_NS)
        if body is None:
            return [f"{example}: DOCX has no body"]
        body_tables = body.findall("w:tbl", W_NS)
        if len(body_tables) != 4:
            failures.append(f"{example}: rendered output should keep exactly 4 QMG body tables")
        xml_blob = "\n".join(
            z.read(name).decode("utf-8", "ignore")
            for name in names
            if name.startswith("word/") and name.endswith(".xml")
        )
        for internal_marker in ["Hilfe und Tipps", "Dokument-Raster", "Diese Zeile bitte nicht löschen"]:
            if internal_marker in xml_blob:
                failures.append(f"{example}: internal QMG helper page leaked into output")
        for placeholder in [
            "_Vorname_",
            "_Name_",
            "_Firma_",
            "_ Dokument/e, Plan/Pläne _",
            "_Thema 01_",
            "_Beschreibung einfügen_",
            "Besprechnungsthema A",
        ]:
            if placeholder in xml_blob:
                failures.append(f"{example}: QMG placeholder leaked into output: {placeholder}")
        headers = [name for name in names if name.startswith("word/header")]
        footers = [name for name in names if name.startswith("word/footer")]
        if not headers:
            failures.append(f"{example}: official header parts are missing")
        if not footers:
            failures.append(f"{example}: official footer parts are missing")
        header_text = "\n".join(z.read(name).decode("utf-8", "ignore") for name in headers)
        footer_text = "\n".join(z.read(name).decode("utf-8", "ignore") for name in footers)
        if "Eike Becker_Architekten" not in header_text and "Eike Becker_Architekten" not in footer_text:
            failures.append(f"{example}: EBA header/footer branding missing")
        if "PAGE" not in footer_text or "SECTIONPAGES" not in footer_text:
            failures.append(f"{example}: page number fields missing from footer")
    return failures


def render_example(example: str, required_text: list[str]) -> list[str]:
    failures: list[str] = []
    src = REPO_ROOT / example
    with tempfile.TemporaryDirectory(prefix="eba-render-smoke-") as tmp:
        tmp_path = Path(tmp)
        md_path = tmp_path / src.name
        out_dir = tmp_path / "out"
        shutil.copy2(src, md_path)
        result = subprocess.run(
            [
                sys.executable,
                str(RENDERER),
                str(md_path),
                "--out-dir",
                str(out_dir),
                "--no-pdf",
            ],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            failures.append(
                f"{example}: renderer exited {result.returncode}: {result.stderr.strip()}"
            )
            return failures
        if md_path.exists():
            failures.append(f"{example}: markdown intermediate was not deleted")
        docx_path = out_dir / f"{md_path.stem}.docx"
        if not docx_path.exists():
            failures.append(f"{example}: DOCX was not written")
            return failures
        rendered = read_docx_text(docx_path)
        for needle in required_text:
            if needle not in rendered:
                failures.append(f"{example}: rendered DOCX missing {needle!r}")
        failures.extend(qmg_template_checks(docx_path, example))
    return failures


def main() -> int:
    checks = {
        "references/examples/beispiel-ausgabe-gespraechsnotiz.md": [
            "Gesprächsnotiz",
            "Bauantragsstand und Rückmeldung der Bauaufsicht",
            "Werden innerhalb von 3 Kalendertagen",
        ],
        "references/examples/beispiel-ausgabe-einfach.md": [
            "Protokoll",
            "Kick-Off Meeting Projekt VTS-549",
            "Zuständig/Frist",
        ],
        "references/examples/beispiel-ausgabe-lp1-4.md": [
            "zur Besprechung Nr. 12",
            "Planungsbesprechung — BIM, Bauantrag, Wohnfassade",
            "LP3-Modell (FusionLive-Upload)",
            "Ort | Online",
            "Datum | 24.03.26",
            "Zeit | 09:00 – 09:07",
            "Werden innerhalb von 5 Kalendertagen",
            "Besprechungsthemen",
        ],
        "references/examples/beispiel-ausgabe-lp5.md": [
            "zur Besprechung Nr. 8",
            "Baubesprechung — Rohbau, Mängel, Brandschutz",
            "Witterung",
            "Schalungsplan UG1, UG2",
            "M-048",
        ],
        "references/examples/beispiel-ausgabe-bim.md": [
            "zur Besprechung Nr. 07",
            "BIM-Koordination JF-07",
            "BIMcollab-Issue-Liste",
            "Ort | Online",
            "D/K | B | LN",
        ],
    }

    failures: list[str] = []
    for example, required_text in checks.items():
        failures.extend(render_example(example, required_text))

    if failures:
        print(f"Render smoke test failed with {len(failures)} issue(s):")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Render smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

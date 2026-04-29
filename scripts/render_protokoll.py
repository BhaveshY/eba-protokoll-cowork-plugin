#!/usr/bin/env python3
"""Render an EBA protokoll Markdown file as DOCX (and optionally PDF).

Used by all five format skills. The Markdown is treated as an in-memory
intermediate and is NOT preserved in the user-facing output. The deliverables
are the .docx (always) and .pdf (when a converter is available).

Usage:
    python3 render_protokoll.py <markdown_path> [--format <fmt>] [--no-pdf]

The script auto-detects the format from the Markdown header if --format is not
given:
    "# Gesprächsnotiz"          -> gespraechsnotiz
    "# Protokoll" + "Gesprächsinhalt" + "Frist" header -> protokoll-einfach
    "# Protokoll" + "Besprechungsthemen" + "D/K"       -> protokoll-lp1-4 / -lp5 / -bim

Output files are written next to <markdown_path>:
    <basename>.docx
    <basename>.pdf  (if Pages or LibreOffice is available)

The Markdown intermediate at <markdown_path> is removed on success unless
--keep-md is passed.

Exit codes:
    0 success (DOCX written; PDF best-effort)
    2 markdown could not be parsed
    3 docx generation failed
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor, Mm
    from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.section import WD_ORIENTATION
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    sys.stderr.write(
        "render_protokoll.py: missing dependency 'python-docx'.\n"
        "Install with:  pip install python-docx\n"
    )
    sys.exit(3)


# EBA brand colors lifted from the QMG-024-141 templates' "intern" page:
EBA_ORANGE = "FA6400"   # 'energy' accent
EBA_ORANGE_SOFT = "FFE0CC"  # 'soft' background tint
EBA_GREY_HEADER = "E1E1E1"  # 'silver' for table headers
EBA_GREY_LIGHT = "F2F2F2"   # very light grey for key cells
EBA_TEXT_GREY = "404040"


# ─── Markdown parsing ──────────────────────────────────────────────────────


@dataclass
class MdSection:
    """One ## section of the protokoll: heading + raw lines (no leading ##)."""

    heading: str
    lines: list[str] = field(default_factory=list)


@dataclass
class ParsedMd:
    """Structured view of an EBA protokoll Markdown file."""

    title: str = ""
    subtitle: str = ""  # the italic line right under the title (if any)
    header_tables: list[list[list[str]]] = field(default_factory=list)
    notice: str = ""  # the > Hinweis / > Vorbemerkung blockquote
    sections: list[MdSection] = field(default_factory=list)
    detected_format: str = "unknown"


def _strip_md_inline(s: str) -> str:
    """Remove a *small* set of inline Markdown tokens (bold, italics) so the
    resulting text reads as plain Word body text. We deliberately keep the
    behaviour conservative — anything we don't recognise stays as-is."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"__(.+?)__", r"\1", s)
    s = re.sub(r"(?<![A-Za-z0-9])\*(.+?)\*(?![A-Za-z0-9])", r"\1", s)
    s = re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"\1", s)
    return s


def _parse_md_table(block: list[str]) -> list[list[str]]:
    """Parse a Markdown pipe-table block into a list of rows of cell strings.
    The separator row (---|---) is skipped."""
    rows: list[list[str]] = []
    for raw in block:
        line = raw.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line[1:-1].split("|")]
        if all(re.fullmatch(r":?-+:?", c or "-") for c in cells):
            continue  # separator row
        rows.append([_strip_md_inline(c) for c in cells])
    return rows


def parse_protokoll_md(md_text: str) -> ParsedMd:
    """Walk the markdown line by line, collecting:
       - title (# H1)
       - subtitle (italic line directly under H1)
       - header tables (the tables before the first ## heading)
       - notice block (>... immediately after header tables)
       - body sections (## Heading + content)
    """
    parsed = ParsedMd()
    lines = md_text.splitlines()
    i = 0

    # --- title ---
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        parsed.title = lines[i][2:].strip()
        i += 1

    # --- subtitle: skip blank lines, then capture an italic line if present ---
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        m = re.match(r"^_(.+)_\s*$", lines[i].strip())
        if m:
            parsed.subtitle = m.group(1).strip()
            i += 1

    # --- collect everything until first ## as header / notice content ---
    pre_section: list[str] = []
    while i < len(lines) and not lines[i].startswith("## "):
        pre_section.append(lines[i])
        i += 1

    # split pre-section into tables / blockquotes / other
    j = 0
    cur_table: list[str] = []
    cur_quote: list[str] = []
    while j < len(pre_section):
        line = pre_section[j]
        if line.lstrip().startswith("|"):
            cur_table.append(line)
        else:
            if cur_table:
                parsed.header_tables.append(_parse_md_table(cur_table))
                cur_table = []
            if line.lstrip().startswith(">"):
                cur_quote.append(re.sub(r"^>\s?", "", line.strip()))
            elif cur_quote and not line.strip():
                pass  # allow inline blank lines inside quote
            elif cur_quote:
                parsed.notice = " ".join(cur_quote).strip()
                cur_quote = []
        j += 1
    if cur_table:
        parsed.header_tables.append(_parse_md_table(cur_table))
    if cur_quote and not parsed.notice:
        parsed.notice = " ".join(cur_quote).strip()

    # --- body sections ---
    cur_section: MdSection | None = None
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            if cur_section:
                parsed.sections.append(cur_section)
            cur_section = MdSection(heading=line[3:].strip())
        else:
            if cur_section is not None:
                cur_section.lines.append(line)
        i += 1
    if cur_section:
        parsed.sections.append(cur_section)

    parsed.detected_format = _detect_format(parsed)
    return parsed


def _detect_format(parsed: ParsedMd) -> str:
    if parsed.title.startswith("Gesprächsnotiz"):
        return "gespraechsnotiz"
    if parsed.title.startswith("Protokoll"):
        all_text = "\n".join(
            line for s in parsed.sections for line in [s.heading] + s.lines
        )
        if "D/K" in all_text and "Besprechungsthemen" in all_text:
            # tracking format - distinguishing lp1-4 / lp5 / bim happens later
            # by inspecting D/K column values; for rendering they're identical
            return "protokoll-tracking"
        if "Gesprächsinhalt" in all_text:
            return "protokoll-einfach"
    return "unknown"


# ─── DOCX rendering ────────────────────────────────────────────────────────


def _set_cell_shading(cell, fill: str) -> None:
    """Apply a hex fill (e.g. 'F0F0F0') to a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def _set_table_borders(tbl) -> None:
    """Add a thin black border to every cell side."""
    tblPr = tbl._tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl._tbl.insert(0, tblPr)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), "808080")
        borders.append(b)
    tblPr.append(borders)


def _add_run(p, text: str, *, bold=False, italic=False, size_pt: int | None = None):
    r = p.add_run(text)
    r.font.name = "Arial"
    if bold:
        r.bold = True
    if italic:
        r.italic = True
    if size_pt:
        r.font.size = Pt(size_pt)
    return r


def _make_table(doc, headers: list[str], rows: list[list[str]], *, header_fill=EBA_GREY_HEADER):
    """Standard EBA-style table: bold grey header row, thin grey borders, alternating row tint."""
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    _set_table_borders(tbl)
    for ci, h in enumerate(headers):
        cell = tbl.rows[0].cells[ci]
        cell.text = ""
        _set_cell_shading(cell, header_fill)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        _add_run(p, h, bold=True, size_pt=10)
    for ri, row in enumerate(rows):
        if ri % 2 == 1:
            for ci in range(len(headers)):
                _set_cell_shading(tbl.rows[ri + 1].cells[ci], "FAFAFA")
        for ci, value in enumerate(row[: len(headers)]):
            cell = tbl.rows[ri + 1].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            _add_run(p, value, size_pt=10)
    return tbl


def _add_heading(doc, text: str, *, level=1):
    p = doc.add_paragraph()
    if level == 1:
        _add_run(p, text, bold=True, size_pt=14)
    elif level == 2:
        _add_run(p, text, bold=True, size_pt=12)
    else:
        _add_run(p, text, bold=True, size_pt=11)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    return p


def _add_para(doc, text: str, *, italic=False, indent_left_cm=0.0):
    p = doc.add_paragraph()
    if indent_left_cm:
        p.paragraph_format.left_indent = Cm(indent_left_cm)
    _add_run(p, text, italic=italic, size_pt=10)
    return p


def _setup_page(doc):
    """A4 portrait, EBA-style margins, default font Arial 10pt."""
    style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.font.size = Pt(10)
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(attr), "Arial")

    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.orientation = WD_ORIENTATION.PORTRAIT
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.0)


def _add_title_block(doc, title: str, subtitle: str | None) -> None:
    """An EBA-style title: orange accent bar + bold title + optional subtitle."""
    # Orange accent bar (a thin shaded paragraph)
    bar = doc.add_paragraph()
    bar.paragraph_format.space_after = Pt(0)
    bar_pPr = bar._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "24")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), EBA_ORANGE)
    pBdr.append(bottom)
    bar_pPr.append(pBdr)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = RGBColor.from_string("000000")

    if subtitle:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(12)
        sr = sp.add_run(subtitle)
        sr.font.name = "Arial"
        sr.font.size = Pt(11)
        sr.font.italic = True
        sr.font.color.rgb = RGBColor.from_string(EBA_TEXT_GREY)


def render_to_docx(parsed: ParsedMd, out_path: Path) -> None:
    """Build an EBA-styled DOCX from the parsed MD.

    This does NOT fill the official QMG-024-141 .docx template — instead it
    produces a fresh, well-formatted document with the same content, tables,
    and hierarchy. The styling matches EBA's brand (Arial, orange accent,
    grey table headers, A4 portrait, professional spacing) so it reads as
    an EBA document in MS Word on Windows."""
    doc = Document()
    _setup_page(doc)

    if parsed.title:
        _add_title_block(doc, parsed.title, parsed.subtitle or None)

    # Header tables
    for tbl in parsed.header_tables:
        if not tbl:
            continue
        headers, rows = tbl[0], tbl[1:]
        if len(headers) == 2 and rows and all(len(r) == 2 for r in rows):
            _make_kv_table(doc, [headers] + rows)
        else:
            _make_table(doc, headers, rows)
        doc.add_paragraph()

    if parsed.notice:
        _add_notice_box(doc, parsed.notice)

    # Body sections
    for s in parsed.sections:
        _add_heading(doc, s.heading, level=2)
        _render_section_lines(doc, s.lines)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))


def _render_section_lines(doc, lines: list[str]) -> None:
    """Render a markdown section in document order.

    Tracking protocols put multiple header tables and the Vorbemerkung inside the
    first ``## zur Besprechung`` section. Rendering only the first table silently
    drops Ort/Datum/Zeit and the standard notice, so this function walks the
    whole section and flushes tables/blockquote groups as they appear.
    """
    table_block: list[str] = []
    quote_block: list[str] = []

    def flush_table() -> None:
        nonlocal table_block
        if not table_block:
            return
        table = _parse_md_table(table_block)
        table_block = []
        if not table:
            return
        _make_table(doc, table[0], table[1:])
        doc.add_paragraph()

    def flush_quote() -> None:
        nonlocal quote_block
        if not quote_block:
            return
        text = " ".join(quote_block).strip()
        quote_block = []
        if not text:
            return
        if "Vorbemerkung" in text or "Hinweis" in text:
            _add_notice_box(doc, _strip_md_inline(text))
        else:
            _add_para(doc, _strip_md_inline(text), italic=True)

    for raw in lines:
        stripped = raw.lstrip()
        if stripped.startswith("|"):
            flush_quote()
            table_block.append(raw)
            continue

        flush_table()

        if not stripped:
            flush_quote()
            continue
        if stripped.startswith(">"):
            quote_block.append(re.sub(r"^>\s?", "", stripped).strip())
            continue

        flush_quote()

        if stripped.startswith("### "):
            _add_heading(doc, _strip_md_inline(stripped[4:].strip()), level=3)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            _add_run(p, _strip_md_inline(stripped[2:]), size_pt=10)
        elif stripped == "---":
            continue
        else:
            _add_para(doc, _strip_md_inline(stripped))

    flush_table()
    flush_quote()


def _add_notice_box(doc, text: str) -> None:
    """A shaded callout box for the Hinweis/Vorbemerkung blockquote."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.autofit = True
    cell = tbl.rows[0].cells[0]
    _set_cell_shading(cell, EBA_ORANGE_SOFT)
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    _add_run(p, text, italic=True, size_pt=9)
    doc.add_paragraph()


def _make_kv_table(doc, rows: list[list[str]]):
    """Two-column key/value table — bold grey label cells, plain value cells."""
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.style = "Table Grid"
    _set_table_borders(tbl)
    # Set column widths: 35% / 65% of usable page width (~16.5 cm)
    for row in tbl.rows:
        if len(row.cells) >= 2:
            row.cells[0].width = Cm(5.5)
            row.cells[1].width = Cm(11.0)
    for ri, row in enumerate(rows):
        if len(row) < 2:
            continue
        kc, vc = tbl.rows[ri].cells
        kc.text = ""
        vc.text = ""
        _set_cell_shading(kc, EBA_GREY_LIGHT)
        for c in (kc, vc):
            c.paragraphs[0].paragraph_format.space_before = Pt(1)
            c.paragraphs[0].paragraph_format.space_after = Pt(1)
        _add_run(kc.paragraphs[0], row[0], bold=True, size_pt=10)
        _add_run(vc.paragraphs[0], row[1], size_pt=10)
    return tbl


# ─── PDF rendering ─────────────────────────────────────────────────────────


def render_to_pdf(docx_path: Path, pdf_path: Path) -> bool:
    """Best-effort DOCX→PDF conversion. Returns True on success.

    Conversion strategies are tried in this order — first one that succeeds
    wins:

      1. **MS Word COM** (Windows, if Word installed) — best fidelity for
         Windows users. Requires `pywin32`.
      2. **LibreOffice headless** (`soffice --headless`) — cross-platform
         (Win/Mac/Linux). The recommended Windows install is the bundled
         LibreOffice from libreoffice.org.
      3. **macOS Pages** via AppleScript — fallback for macOS development.

    All three are graceful: if the converter isn't available, fall through
    to the next. If none are available, the function returns False and the
    caller proceeds with a DOCX-only deliverable.
    """
    # 1. Word COM on Windows
    if sys.platform == "win32":
        try:
            import win32com.client  # type: ignore[import-not-found]

            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            try:
                doc = word.Documents.Open(str(docx_path))
                # 17 == wdFormatPDF
                doc.SaveAs(str(pdf_path), FileFormat=17)
                doc.Close(SaveChanges=False)
            finally:
                word.Quit()
            if pdf_path.exists():
                return True
        except Exception as exc:
            sys.stderr.write(f"Word COM export skipped/failed: {exc}\n")

    # 2. LibreOffice headless (Windows, Linux, macOS)
    soffice_candidates = ["soffice", "libreoffice"]
    if sys.platform == "win32":
        # Most common Windows install paths
        soffice_candidates = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ] + soffice_candidates
    for cand in soffice_candidates:
        try:
            r = subprocess.run(
                [
                    cand,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(pdf_path.parent),
                    str(docx_path),
                ],
                capture_output=True,
                text=True,
                timeout=180,
            )
            if r.returncode == 0:
                produced = pdf_path.parent / (docx_path.stem + ".pdf")
                if produced != pdf_path and produced.exists():
                    produced.replace(pdf_path)
                if pdf_path.exists():
                    return True
        except FileNotFoundError:
            continue
        except Exception as exc:
            sys.stderr.write(f"LibreOffice export failed: {exc}\n")

    # 3. macOS Pages — dev-environment fallback only
    if sys.platform == "darwin" and Path("/Applications/Pages.app").exists():
        try:
            script = (
                'tell application "Pages"\n'
                "  launch\n"
                "  delay 0.5\n"
                f'  set theDoc to open POSIX file "{docx_path}"\n'
                "  delay 1\n"
                f'  export theDoc to POSIX file "{pdf_path}" as PDF\n'
                "  try\n"
                "    close theDoc saving no\n"
                "  end try\n"
                "end tell\n"
            )
            r = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if pdf_path.exists():
                return True
            sys.stderr.write(f"Pages export failed: {r.stderr.strip()}\n")
        except Exception as exc:
            sys.stderr.write(f"Pages export error: {exc}\n")

    return False


# ─── CLI ───────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("md_path", type=Path, help="Markdown file to render")
    ap.add_argument("--format", default=None, help="Force format (overrides auto-detect)")
    ap.add_argument("--no-pdf", action="store_true", help="Skip PDF rendering")
    ap.add_argument("--keep-md", action="store_true", help="Don't delete the MD intermediate")
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: alongside MD)",
    )
    args = ap.parse_args(argv)

    md_path: Path = args.md_path.resolve()
    if not md_path.is_file():
        sys.stderr.write(f"Not a file: {md_path}\n")
        return 2

    parsed = parse_protokoll_md(md_path.read_text(encoding="utf-8"))
    if args.format:
        parsed.detected_format = args.format

    out_dir = (args.out_dir or md_path.parent).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    docx_path = out_dir / (md_path.stem + ".docx")
    pdf_path = out_dir / (md_path.stem + ".pdf")

    try:
        render_to_docx(parsed, docx_path)
    except Exception as exc:
        sys.stderr.write(f"DOCX render failed: {exc}\n")
        return 3

    pdf_ok = False
    if not args.no_pdf:
        pdf_ok = render_to_pdf(docx_path, pdf_path)

    if not args.keep_md:
        try:
            md_path.unlink()
        except OSError:
            pass

    print(f"DOCX: {docx_path}")
    if pdf_ok:
        print(f"PDF:  {pdf_path}")
    elif not args.no_pdf:
        print(
            "PDF:  (skipped — no converter available. On Windows install "
            "LibreOffice from https://www.libreoffice.org/ or have MS Word "
            "+ pywin32 installed.)"
        )
    print(f"Format: {parsed.detected_format}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

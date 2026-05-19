# Ausgabe-Konvention: DOCX/PDF oder QMG-XLSX (kein Markdown)

Alle Protokoll-Skills schreiben das Endformat der jeweiligen Originalvorlage:
Word-Ursprungsvorlagen als **DOCX + PDF**, Excel-Ursprungsvorlagen als
offizielles **QMG-XLSX**. Markdown ist nur ein **flüchtiges Zwischenformat** und
wird nach dem Rendern gelöscht.

Die Produktionsumgebung ist **Windows 11 mit installiertem Microsoft Word**.
Der Nutzer ist nicht technisch. Die Skill darf den Nutzer deshalb **nicht**
nach Python-Paketen, `pip`, `pywin32`, LibreOffice oder Konverterdetails fragen.
Der Renderer kümmert sich selbst darum.

Diese Datei beschreibt die einheitliche Rendering-Pipeline. Die
format-spezifischen Skills (`gespraechsnotiz`, `protokoll-einfach`,
`protokoll-lp1-4`, `protokoll-lp5`, BIM-Sub-Variante,
`protokoll-fortschreiben`) verweisen alle hierher.

## Verzeichnisstruktur

Die Ausgaben landen relativ zum aktuellen Arbeitsverzeichnis:

```
protokolle/
└── <projekt>/                 # z.B. 553-WIL/
    ├── 2026-03-24_planungsbesprechung-12.docx   # Word-Vorlage
    ├── 2026-03-24_planungsbesprechung-12.pdf
    └── 2026-03-31_bim-pk-jf-07.xlsx             # Excel-Vorlage
```

`<projekt>` ist optional. Wenn der Nutzer keinen Projektordner nennt, lege
direkt unter `protokolle/` ab. Wenn `protokolle/` nicht existiert, anlegen.

## Pipeline-Schritte

### 0. Selbstheilende Umgebung

Vor dem ersten DOCX/PDF/XLSX-Rendern prüft `render_protokoll.py` seine
Abhängigkeiten:

- `python-docx` für DOCX-Erzeugung.
- `openpyxl` für die offiziellen QMG-XLSX-Ausgaben.
- `pywin32` auf Windows für den MS-Word-COM-PDF-Export.

Fehlt ein Paket, installiert der Renderer es automatisch mit:

```bash
python -m pip install --user --upgrade -r scripts/requirements.txt
```

In einer virtuellen Umgebung wird `--user` automatisch weggelassen. Die Skill
soll **keinen separaten Setup-Schritt** an den Nutzer delegieren. Einfach den
Renderer ausführen; er bootstrapt beim ersten Lauf und ist danach schnell.

### 1. Inhalt als Markdown im Zwischenpfad erzeugen

Schreibe das Protokoll als Markdown unter einen flüchtigen Pfad:

```
<temp-dir>/eba-<format>-<jjjj-mm-tt>-<projekt-kuerzel>.md
```

`<temp-dir>` ist das temporäre Verzeichnis des Betriebssystems, z.B. über
`tempfile.gettempdir()` (`%TEMP%` auf Windows, `/tmp` auf macOS/Linux).
Den Pfad **nicht fest auf `/tmp`** setzen.

Beispiel: `<temp-dir>/eba-gespraechsnotiz-2026-03-24-WIL.md`

Die Markdown-Struktur folgt **exakt** der jeweiligen Vorlage in
`${CLAUDE_PLUGIN_ROOT}/references/templates/<format>.md`. Standard-Hinweistexte
(„Hinweis", „Vorbemerkung") werden wortgleich übernommen.

### 2. Renderer aufrufen

Führe das folgende Bash-Kommando aus:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
  "<temp-dir>/eba-<format>-<datum>-<kuerzel>.md" \
  --out-dir "protokolle/<projekt>/"
```

Ohne projekt-Unterordner:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
  "<temp-dir>/eba-<format>-<datum>-<kuerzel>.md" \
  --out-dir "protokolle/"
```

Auf Windows kann statt `python3` derselbe Befehl mit `python` oder `py -3`
ausgeführt werden, wenn `python3` nicht registriert ist.

Wichtige Flags:

- `--no-pdf` — DOCX-only, PDF-Schritt überspringen.
- `--no-xlsx` — nur für Debugging. Bei Excel-Ursprungsvorlagen bleibt dann kein
  Enddokument übrig und der Renderer bricht ab.
- `--keep-md` — nur für Debugging: behält das MD-Zwischenformat.
- `--out-dir <pfad>` — Zielverzeichnis (Default: neben dem MD).
- `--format <name>` — überschreibt die Auto-Erkennung
  (`gespraechsnotiz` / `protokoll-einfach` / `protokoll-lp1-4` /
  `protokoll-bim` / `protokoll-lp5`).

### 3. Ausgabe an den Nutzer

Der Renderer gibt die finalen Pfade auf stdout aus, z.B. Word-Ursprung:

```
DOCX: protokolle/553-WIL/2026-03-24_planungsbesprechung-12.docx
XLSX: protokolle/553-WIL/2026-03-24_planungsbesprechung-12.xlsx
PDF:  protokolle/553-WIL/2026-03-24_planungsbesprechung-12.pdf
Format: protokoll-lp1-4
```

Oder Excel-Ursprung:

```
XLSX: protokolle/553-WIL/2026-03-31_bim-pk-jf-07.xlsx
Format: protokoll-bim
```

Falls bei einem Word-Ursprungsformat die PDF-Zeile lautet
`(skipped — no converter found ...)`, hat das System keinen PDF-Konverter. Auf
Windows ist das ein Fehlerzustand, den Claude Code intern beheben soll
(Renderer erneut ausführen, Word/COM-Fehler prüfen), nicht eine Aufgabe für den
Nutzer.

## PDF-Konverter pro Plattform

Der Renderer probiert die folgenden Konverter in dieser Reihenfolge — der
erste funktionierende gewinnt:

| Plattform | Bevorzugt | Setup |
|-----------|-----------|-------|
| **Windows 11** | MS Word COM | automatisch via `pywin32`-Bootstrap |
| **Windows 11** | LibreOffice headless | Fallback, falls bereits vorhanden |
| Linux       | LibreOffice headless | `apt install libreoffice` oder gleichwertig |
| macOS       | LibreOffice headless | `brew install --cask libreoffice` |
| macOS (dev) | Pages via osascript | nur Fallback für Entwicklung |

**Windows-Produktion**: MS Word ist der bevorzugte Pfad. Wenn Word installiert
ist, soll PDF-Erzeugung ohne Nutzerinteraktion funktionieren.

Wenn auf Windows kein PDF entsteht, ist das Ergebnis **nicht fertig**. Claude
Code soll den Fehler aus stderr lesen, denselben Renderbefehl nach
Selbstheilung erneut versuchen und dem Nutzer erst dann antworten, wenn DOCX
und PDF vorhanden sind oder ein echter Blocker vorliegt.

## Qualitätsanspruch

- Inhaltliche Struktur, Standardtexte, Tabellenblöcke und Kennzeichnungen müssen
  den QMG-024-141-Referenzen entsprechen.
- Die offiziellen Dateien in `references/templates/qmg/` sind die fachliche
  Layout- und Wortlaut-Referenz.
- DOCX-Ausgaben werden aus den vorhandenen QMG-Word-Templates erzeugt:
  `QMG-024-141_ORG-GESPRAECHSNOTIZ_230202-D.docx`,
  `QMG-024-141_ORG-PK-LP1-4-MA_230227-A.docx` und dem
  QMG-Tracking-Word-Shell `QMG-024-141_ORG-PK-LP5-MA_230202-B.docx`.
- Explizite einfache Excel-Ausgaben werden direkt aus
  `QMG-024-141_ORG-PK-LP1-4-EXCEL-MA_240920-A.xlsx` erzeugt. Dieses Workbook
  hat die einfache `Gesprächsinhalt` / `zuständig` / `Frist`-Struktur und kein
  D/K|B|LN-Tracking.
- BIM- und explizite Tracking-Excel-Ausgaben werden direkt aus
  `QMG-024-141_ORG-PK-EXCEL-MA_240926-C.xlsx` erzeugt. Die Sheets
  `Deckblatt`, `Protokoll`, `Doku_Info`, `Hilfe und Tipps` und `intern`
  bleiben erhalten; befüllt werden nur die fachlichen Bereiche.
- Markdown-Beispiele in `references/examples/` sind Regressionstests für den
  Renderer. Nach Änderungen an Renderer oder Skills `scripts/smoke_render.py`
  ausführen.
- Keine frei erfundenen Felder, keine ausgelassenen Header- oder Endblöcke, kein
  Markdown im Projektordner.
- Unbekannte Markdown-Formate werden nicht generisch gerendert. Wenn der
  Renderer ein Format ablehnt, muss Claude den passenden EBA-Typ bestimmen
  oder bei echtem Formatkonflikt kurz nachfragen.

## Was beim Fortschreiben anders ist

`protokoll-fortschreiben` schreibt zusätzlich die `protokoll-state.json` neben
die Ausgabedateien. Diese JSON-Datei bleibt erhalten — sie ist KEIN flüchtiges
Zwischenformat, sondern die persistente Projektzustand-Datei für den
nächsten Lauf.

## Anti-Pattern

- ❌ Markdown direkt ins Projekt-Verzeichnis schreiben — kein `.md` im
  `protokolle/`-Ordner.
- ❌ DOCX im aktuellen Verzeichnis oder auf dem Desktop ablegen — immer in
  `protokolle/<projekt>/`.
- ❌ Word-Vorlagen zusätzlich als XLSX ausgeben oder Excel-Vorlagen zusätzlich
  als DOCX/PDF ausgeben — das Originalformat der QMG-Vorlage entscheidet.
- ❌ Den Nutzer bitten, `pip install`, `pywin32`, LibreOffice oder andere
  technische Setup-Schritte auszuführen — der Renderer bootstrapt selbst.
- ❌ Auf Windows mit nur DOCX antworten, wenn PDF fehlt — Word-PDF ist dort
  Pflicht, außer der Nutzer verlangt ausdrücklich DOCX-only.
- ❌ Den Renderer überspringen, wenn nur DOCX gefordert ist — auch dann via
  `--no-pdf` aufrufen, damit die Konvention konsistent bleibt.
- ❌ `--keep-md` standardmäßig setzen — nur bei Debugging.
- ❌ Unbekannte Inhalte mit einem freien DOCX-Layout ausgeben — nur unterstützte
  QMG-Template-Pfade sind zulässig.

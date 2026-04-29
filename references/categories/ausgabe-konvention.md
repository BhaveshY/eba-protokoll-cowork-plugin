# Ausgabe-Konvention: DOCX + PDF (kein Markdown)

Alle Protokoll-Skills schreiben als Endformat **DOCX** (immer) und **PDF**
(soweit ein Konverter — Pages oder LibreOffice — verfügbar ist). Markdown ist
nur ein **flüchtiges Zwischenformat** und wird nach dem Rendern gelöscht.

Diese Datei beschreibt die einheitliche Rendering-Pipeline. Die
format-spezifischen Skills (`gespraechsnotiz`, `protokoll-einfach`,
`protokoll-lp1-4`, `protokoll-lp5`, BIM-Sub-Variante,
`protokoll-fortschreiben`) verweisen alle hierher.

## Verzeichnisstruktur

Die Ausgaben landen relativ zum aktuellen Arbeitsverzeichnis:

```
protokolle/
└── <projekt>/                 # z.B. 553-WIL/
    ├── 2026-03-24_planungsbesprechung-12.docx   # immer
    └── 2026-03-24_planungsbesprechung-12.pdf    # wenn Konverter vorhanden
```

`<projekt>` ist optional. Wenn der Nutzer keinen Projektordner nennt, lege
direkt unter `protokolle/` ab. Wenn `protokolle/` nicht existiert, anlegen.

## Pipeline-Schritte

### 1. Inhalt als Markdown im Zwischenpfad erzeugen

Schreibe das Protokoll als Markdown unter einen flüchtigen Pfad:

```
/tmp/eba-<format>-<jjjj-mm-tt>-<projekt-kuerzel>.md
```

Beispiel: `/tmp/eba-gespraechsnotiz-2026-03-24-WIL.md`

Die Markdown-Struktur folgt **exakt** der jeweiligen Vorlage in
`${CLAUDE_PLUGIN_ROOT}/references/templates/<format>.md`. Standard-Hinweistexte
(„Hinweis", „Vorbemerkung") werden wortgleich übernommen.

### 2. Renderer aufrufen

Führe das folgende Bash-Kommando aus:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
  "/tmp/eba-<format>-<datum>-<kuerzel>.md" \
  --out-dir "protokolle/<projekt>/"
```

Ohne projekt-Unterordner:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
  "/tmp/eba-<format>-<datum>-<kuerzel>.md" \
  --out-dir "protokolle/"
```

Wichtige Flags:

- `--no-pdf` — DOCX-only, PDF-Schritt überspringen.
- `--keep-md` — nur für Debugging: behält das MD-Zwischenformat.
- `--out-dir <pfad>` — Zielverzeichnis (Default: neben dem MD).
- `--format <name>` — überschreibt die Auto-Erkennung
  (`gespraechsnotiz` / `protokoll-einfach` / `protokoll-tracking`).

### 3. Ausgabe an den Nutzer

Der Renderer gibt die finalen Pfade auf stdout aus, z.B.:

```
DOCX: protokolle/553-WIL/2026-03-24_planungsbesprechung-12.docx
PDF:  protokolle/553-WIL/2026-03-24_planungsbesprechung-12.pdf
Format: protokoll-tracking
```

Falls die PDF-Zeile lautet `(skipped — no converter found ...)`, hat das
System weder Pages noch LibreOffice. Das DOCX ist trotzdem geschrieben.

## PDF-Konverter pro Plattform

Der Renderer probiert die folgenden Konverter in dieser Reihenfolge — der
erste funktionierende gewinnt:

| Plattform | Bevorzugt | Setup |
|-----------|-----------|-------|
| **Windows** | MS Word COM | `pip install pywin32` (wenn Word installiert ist) |
| **Windows** | LibreOffice headless | LibreOffice von https://www.libreoffice.org/ installieren |
| Linux       | LibreOffice headless | `apt install libreoffice` oder gleichwertig |
| macOS       | LibreOffice headless | `brew install --cask libreoffice` |
| macOS (dev) | Pages via osascript | nur Fallback für Entwicklung |

**Empfohlener Setup für Windows-Produktion**: LibreOffice installieren. Damit
funktioniert die PDF-Erzeugung sofort und unabhängig davon, ob MS Word
vorhanden ist.

Wenn kein Konverter gefunden wird, gibt der Renderer nur das DOCX aus — das
DOCX lässt sich manuell in MS Word/LibreOffice öffnen und dort als PDF
exportieren.

## Was beim Fortschreiben anders ist

`protokoll-fortschreiben` schreibt zusätzlich die `protokoll-state.json` neben
das DOCX. Diese JSON-Datei bleibt erhalten — sie ist KEIN flüchtiges
Zwischenformat, sondern die persistente Projektzustand-Datei für den
nächsten Lauf.

## Anti-Pattern

- ❌ Markdown direkt ins Projekt-Verzeichnis schreiben — kein `.md` im
  `protokolle/`-Ordner.
- ❌ DOCX im aktuellen Verzeichnis oder auf dem Desktop ablegen — immer in
  `protokolle/<projekt>/`.
- ❌ Den Renderer überspringen, wenn nur DOCX gefordert ist — auch dann via
  `--no-pdf` aufrufen, damit die Konvention konsistent bleibt.
- ❌ `--keep-md` standardmäßig setzen — nur bei Debugging.

# eba-protokoll-cowork

Ein Claude-Code-Plugin, das aus Transkripten der **EBA Protokoll App** strukturierte
Protokolle nach den EBA-Vorlagen `QMG-024-141` erzeugt:

| Format | QMG-Index | Verwendung |
|--------|-----------|------------|
| **Gesprächsnotiz** | `ORG-GESPRAECHSNOTIZ` (Stand D, 02.02.23) | Kurze formlose Notiz, ≤ 3 Sprecher, ohne Tracking. |
| **Protokoll-einfach** | `ORG-PK-LP1-4-MA` (Word, Stand A, 27.02.23) + `ORG-PK-LP1-4-EXCEL-MA` (Excel, Stand A, 20.09.24) | Kick-Off, Workshop, einmalige Abstimmung mit Frist-Spalte aber ohne D/K-Tracking. |
| **Planungsprotokoll LP1-4** | `ORG-PK-EXCEL-MA` (Stand C, 26.09.24) + QMG-Tracking-Word-Shell | LP1-4 Tracking-Protokoll mit D/K\|B\|LN-Schema, Status, Fortschreibung. |
| **Bauleitungsprotokoll LP5** | `ORG-PK-LP5-MA` (Stand B, 02.02.23) | LP5 Bauleitung mit baustellenspezifischen Kategorien, Mängeln, Bemusterungen. |

Das Plugin kennt die **Fortschreibung** über mehrere Besprechungen (offene Punkte werden
übernommen, neue Bemerkungen mit `LN = NNE` und `#NN:`-Versionsmarker als Ergänzung
markiert) und führt einen pro-Projekt-State, der zwischen Sitzungen erhalten bleibt.

## Installation

### Variante A — direkt vom GitHub-Repo (empfohlen für Claude Cowork)

```
/plugin marketplace add BhaveshY/eba-protokoll-cowork-plugin
/plugin install eba-protokoll-cowork
```

### Variante B — als lokaler Marketplace

```bash
git clone https://github.com/BhaveshY/eba-protokoll-cowork-plugin.git
```

In Claude Code:

```
/plugin marketplace add ./eba-protokoll-cowork-plugin
/plugin install eba-protokoll-cowork
```

### Variante C — Schwester-Repo zum EBA Protokoll App

Dieses Plugin ist das Cowork-Gegenstück zur [EBA Protokoll App](https://github.com/BhaveshY/eba-protokoll-app)
(Electron-Desktop-App für Audio-Aufnahme und Transkription via Deepgram).
Workflow: Aufnahme + Transkript mit der App → Transkript mit diesem Plugin in
ein EBA-konformes Protokoll überführen.

## Schnellstart

Nimm ein Meeting mit der EBA Protokoll App auf und transkribiere es. Das Transkript
landet in `transkripte/<datum>_<thema>.txt`. Dann:

```
/protokoll transkripte/2026-04-22_pk-12.txt
```

Das Plugin erkennt automatisch den passenden Format-Typ (Gesprächsnotiz / LP1-4 / LP5),
zeigt die Erkennung transparent an, und schreibt das fertige Protokoll als
**DOCX + PDF** nach
`protokolle/<projekt>/<datum>_protokoll-NN_<thema>.docx` (und `.pdf`).
Bei Protokoll-einfach und LP1-4/BIM-Tracking entsteht zusätzlich die passende
offizielle QMG-Excel-Datei `…<thema>.xlsx`.
Markdown wird **nicht** ins Projekt geschrieben — es ist nur ein flüchtiges
Zwischenformat. Auf **Windows 11 mit MS Word** erzeugt der Renderer die PDF
automatisch über Word und richtet fehlende Python-Pakete selbst ein.
Die DOCX-Ausgabe befüllt die vorhandenen QMG-Word-Templates:
Gesprächsnotiz, Protokoll-einfach und den QMG-Tracking-Word-Shell für LP1-4/BIM
und LP5. Die einfache XLSX-Ausgabe befüllt
`QMG-024-141_ORG-PK-LP1-4-EXCEL-MA_240920-A.xlsx`; die Tracking-XLSX-Ausgabe
für LP1-4/BIM befüllt `QMG-024-141_ORG-PK-EXCEL-MA_240926-C.xlsx` mit den
Sheets `Deckblatt`, `Protokoll` und `Doku_Info`. Dadurch bleiben EBA-CI,
Header, Footer, Seitenzahlen und Excel-Struktur erhalten.

Rohe Transkripte dürfen unvollständig sein. Wenn Projekt-Nr., Projektname, Ort
oder Ersteller fehlen, erzeugt das Plugin trotzdem das passende Protokoll,
füllt die Header mit Fallbacks (`Projekt-Nr. 000`, `Ort nicht angegeben`,
`Ersteller EBA`) und nennt diese Annahmen am Ende. Nur echte Format-Konflikte
wie LP1-4 vs. LP5 werden zurückgefragt.

Wenn du das Format explizit setzen willst:

```
/gespraechsnotiz   transkripte/kurzes-team-meeting.txt
/protokoll-einfach transkripte/kick-off-meeting.txt
/protokoll-lp1-4   transkripte/planungsbespr-12.txt
/protokoll-lp5     transkripte/baustellenbegehung.txt
```

Für Folgeprotokolle (Fortschreibung):

```
/protokoll-fortschreiben transkripte/baubespr-09.txt
```

## Verfügbare Slash-Befehle

| Befehl | Zweck |
|--------|-------|
| `/protokoll <transkript>` | Auto-Erkennung des Formats und Protokoll-Erstellung. |
| `/gespraechsnotiz <transkript>` | Erzwinge Gesprächsnotiz-Format. |
| `/protokoll-einfach <transkript>` | Erzwinge einfaches Protokoll (LP1-4 Word, ohne Tracking). |
| `/protokoll-lp1-4 <transkript>` | Erzwinge Planungsprotokoll LP1-4 (Tracking). |
| `/protokoll-lp5 <transkript>` | Erzwinge Bauleitungsprotokoll LP5. |
| `/protokoll-fortschreiben <transkript>` | Folgeprotokoll mit Übernahme offener Punkte. |
| `/transkript-vorbereiten <transkript>` | Sprecher umbenennen, Turns mergen, Files zusammenführen. |

## Verfügbare Skills (auto-getriggert)

| Skill | Trigger |
|-------|---------|
| `eba-protokoll` | Nutzer sagt „Protokoll erstellen", „make a protocol", übergibt eine Transkript-Datei ohne Format-Hint. |
| `gespraechsnotiz` | „Gesprächsnotiz", „kurze Notiz", „kurzes Protokoll". |
| `protokoll-einfach` | „einfaches Protokoll", „Workshop", „Kick-Off", „Erstgespräch" — mit Frist, ohne D/K-Tracking. |
| `protokoll-lp1-4` | „Planungsprotokoll", „LP1-4", „Jour Fixe Nr.", „BIM-Koordination", „Tracking-Protokoll". |
| `protokoll-lp5` | „LP5-Protokoll", „Baubesprechung", „Bauleitungsprotokoll", „Baustelle", „Mängelprotokoll". |
| `protokoll-fortschreiben` | Folgeprotokoll, Vorprotokoll vorhanden. |
| `transkript-vorbereiten` | „Sprecher umbenennen", „Transkripte zusammenführen", „Transkript bereinigen". |

## Subagents

| Agent | Aufgabe |
|-------|---------|
| `themen-extractor` | Strukturiert Themen aus dem Transkript (Sprecher, Beschlüsse, Aufgaben, D/K-Vorschlag). |
| `teilnehmer-resolver` | Identifiziert Teilnehmer, ordnet Firmen + Kürzel zu. |
| `protokoll-validator` | Prüft fertige Protokolle gegen EBA-Konventionen. |

## Verzeichnisstruktur

```
plugins/eba-protokoll-cowork/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── commands/                      # Slash-Befehle
├── skills/                        # Auto-Skills (model-invoked)
├── agents/                        # Subagents
├── references/
│   ├── templates/                 # Markdown-Vorlagen (Skill-Anleitungen)
│   │   └── qmg/                   # Original-QMG-024-141-Templates (.docx, .xlsx)
│   ├── categories/                # D/K-Schemata, Kürzel, Status, Stil, Ausgabe-/Metadaten-Konvention
│   └── examples/                  # Beispiel-Transkripte und -Protokolle
├── scripts/
│   ├── render_protokoll.py        # MD → DOCX + PDF (+ XLSX für einfach/LP1-4/BIM)
│   ├── protokoll-state.md         # State-File-Schema-Dokumentation
│   └── validate-references.mjs    # Statische Plugin-Validierung
└── README.md
```

## Speicherorte (Konvention)

```
<arbeitsverzeichnis>/
├── transkripte/                   # rohe Transkripte aus der EBA Protokoll App
│   └── 2026-04-22_pk-12.txt
└── protokolle/                    # vom Plugin erzeugte Protokolle
    └── 553-WIL/                   # je Projekt ein Ordner
        ├── 2026-03-24_protokoll-12_planungsbespr.docx   # immer
        ├── 2026-03-24_protokoll-12_planungsbespr.pdf    # wenn Konverter vorhanden
        ├── 2026-03-24_protokoll-12_planungsbespr.xlsx   # Protokoll-einfach/LP1-4/BIM
        ├── 2026-04-22_protokoll-13_planungsbespr.docx
        ├── 2026-04-22_protokoll-13_planungsbespr.pdf
        ├── 2026-04-22_protokoll-13_planungsbespr.xlsx
        └── protokoll-state.json   # Gedächtnis zwischen Sitzungen
```

## Beispiele

Im `references/examples/`-Ordner:

- `beispiel-transkript-gespraechsnotiz.txt` + `beispiel-ausgabe-gespraechsnotiz.md` —
  einfache 90-Sekunden-Abstimmung.
- `beispiel-transkript-eba-interview.txt` + `beispiel-ausgabe-eba-interview.md` —
  EBA-bezogenes Medien-/Interviewbeispiel ohne Projekt-Nr. mit Gesprächsnotiz-Defaults.
- `beispiel-transkript-einfach.txt` + `beispiel-ausgabe-einfach.md` — Kick-Off
  Meeting mit 4 Teilnehmern, 5 Themen + Unterpunkten, kombinierte Frist-Spalte.
- `beispiel-transkript-lp1-4.txt` + `beispiel-ausgabe-lp1-4.md` — Planungsbesprechung
  mit 5 Teilnehmern, 7 Themen.
- `beispiel-transkript-bim.txt` + `beispiel-ausgabe-bim.md` — BIM-Koordination JF-07
  als LP1-4-Subvariante mit eigenem BIM-D/K-Schema (1–8).
- `beispiel-transkript-lp5.txt` + `beispiel-ausgabe-lp5.md` — Baustellenbegehung
  mit Mängelaufnahme und Bemusterung.
- `beispiel-state.json` — vollständiges State-File für ein laufendes Projekt.

## Qualitätschecks

Die Referenzen lassen sich statisch prüfen mit:

```bash
node scripts/validate-references.mjs
```

Der Check stellt sicher, dass die Beispielausgaben die aktuellen Vorlagen-Endblöcke
verwenden, die BIM-Variante als Beispielpaar vorhanden ist, der Validator
formatabhängig zwischen Gesprächsnotiz, Protokoll-einfach und Tracking-Protokollen
unterscheidet und rohe Transkripte ohne Projektmetadaten über Fallbacks weiterlaufen.

## Konfiguration

Das Plugin braucht keine Konfiguration. Optional kannst du am Anfang eines Projekts
ein leeres State-File anlegen:

```bash
mkdir -p protokolle/553-WIL
echo '{"schema_version":1,"projekt":{"nr":"553","name":"WIL"}}' \
  > protokolle/553-WIL/protokoll-state.json
```

Das Plugin füllt das State-File mit dem ersten Protokoll vollständig auf.

## Endformat-Pipeline (DOCX + PDF + QMG-XLSX)

Alle Skills delegieren das Rendering an
`scripts/render_protokoll.py`. Der Renderer:

1. Liest das vom Skill erzeugte Markdown-Zwischenformat aus `/tmp/`.
2. Schreibt ein EBA-konformes DOCX aus den QMG-Word-Templates nach
   `protokolle/<projekt>/`.
3. Schreibt bei `protokoll-einfach`, `protokoll-lp1-4` und `protokoll-bim`
   zusätzlich ein XLSX aus der passenden offiziellen QMG-Excel-Vorlage.
4. Konvertiert die DOCX zu PDF — Reihenfolge der versuchten Konverter:
   1. **MS Word COM** (Windows 11, `pywin32` wird automatisch installiert)
   2. **LibreOffice headless** (Win/Mac/Linux)
   3. **macOS Pages** (nur als macOS-Dev-Fallback)
5. Löscht das MD-Zwischenformat.

Die volle Konvention steht in
`references/categories/ausgabe-konvention.md`.

**Windows-11-Nutzer müssen nichts vorbereiten.** Der Renderer prüft beim ersten
Lauf selbst, ob `python-docx`, `openpyxl` und `pywin32` verfügbar sind, installiert fehlende
Pakete im Benutzerkontext und nutzt danach MS Word für die PDF-Erzeugung.
Claude Code soll technische Setup-Details intern lösen und den Nutzer erst mit
den fertigen `.docx`-, `.pdf`- und ggf. `.xlsx`-Pfaden konfrontieren.

Wenn auf Windows keine PDF entsteht, gilt das Protokoll als nicht fertig. Der
Renderer gibt einen Fehler zurück, damit Claude Code nachbessert statt nur ein
DOCX abzuliefern.

## Entwicklungsstand

Version 0.2.6 — DOCX + PDF Output, QMG-XLSX für Protokoll-einfach und
Tracking-XLSX für LP1-4/BIM,
Windows-11-First mit automatischem
Dependency-Bootstrap, Metadaten-Fallbacks für rohe Transkripte und
QMG-Template-Füllung. Deckt die Standardvorlagen QMG-024-141 ab
(Gesprächsnotiz, Protokoll-einfach Word + Excel LP1-4 Stand A,
Planungsprotokoll LP1-4/BIM mit D/K|B|LN-Tracking, Bauleitungsprotokoll LP5
Stand B). Geplant:

- Sondervorlage für DGNB-Workshops.
- Visualisierung des State-Files (offene Punkte, Termine, Mängelliste) als
  HTML-Dashboard.

## Lizenz

MIT — siehe Hauptrepo.

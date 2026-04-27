# eba-protokoll-cowork

Ein Claude-Code-Plugin, das aus Transkripten der **EBA Protokoll App** strukturierte
Protokolle nach den EBA-Vorlagen `QMG-024-141` erzeugt:

- **Gesprächsnotiz** (`ORG-GESPRAECHSNOTIZ`, Stand D)
- **Planungsprotokoll LP1-4** (`ORG-PK-LP1-4`, mit D/K|B|LN-Tracking)
- **Bauleitungsprotokoll LP5** (`ORG-PK-LP5`, mit baustellenspezifischen Kategorien)

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
zeigt die Erkennung transparent an, und schreibt das fertige Protokoll als Markdown
nach `protokolle/<projekt>/<datum>_protokoll-NN_<thema>.md`.

Wenn du das Format explizit setzen willst:

```
/gespraechsnotiz transkripte/kurzes-team-meeting.txt
/protokoll-lp1-4  transkripte/planungsbespr-12.txt
/protokoll-lp5    transkripte/baustellenbegehung.txt
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
| `/protokoll-lp1-4 <transkript>` | Erzwinge Planungsprotokoll LP1-4. |
| `/protokoll-lp5 <transkript>` | Erzwinge Bauleitungsprotokoll LP5. |
| `/protokoll-fortschreiben <transkript>` | Folgeprotokoll mit Übernahme offener Punkte. |
| `/transkript-vorbereiten <transkript>` | Sprecher umbenennen, Turns mergen, Files zusammenführen. |

## Verfügbare Skills (auto-getriggert)

| Skill | Trigger |
|-------|---------|
| `eba-protokoll` | Nutzer sagt „Protokoll erstellen", „make a protocol", übergibt eine Transkript-Datei ohne Format-Hint. |
| `gespraechsnotiz` | „Gesprächsnotiz", „kurze Notiz", „kurzes Protokoll". |
| `protokoll-lp1-4` | „Planungsprotokoll", „LP1-4", „Jour Fixe", „Kick-Off", „BIM-Koordination", „Workshop-Protokoll". |
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
│   ├── templates/                 # Markdown-Vorlagen
│   ├── categories/                # D/K-Schemata, Kürzel, Status, Stil
│   └── examples/                  # Beispiel-Transkripte und -Protokolle
├── scripts/
│   └── protokoll-state.md         # State-File-Schema-Dokumentation
└── README.md
```

## Speicherorte (Konvention)

```
<arbeitsverzeichnis>/
├── transkripte/                   # rohe Transkripte aus der EBA Protokoll App
│   └── 2026-04-22_pk-12.txt
└── protokolle/                    # vom Plugin erzeugte Protokolle
    └── 553-WIL/                   # je Projekt ein Ordner
        ├── 2026-03-24_protokoll-12_planungsbespr.md
        ├── 2026-04-22_protokoll-13_planungsbespr.md
        └── protokoll-state.json   # Gedächtnis zwischen Sitzungen
```

## Beispiele

Im `references/examples/`-Ordner:

- `beispiel-transkript-gespraechsnotiz.txt` + `beispiel-ausgabe-gespraechsnotiz.md` —
  einfache 90-Sekunden-Abstimmung.
- `beispiel-transkript-lp1-4.txt` + `beispiel-ausgabe-lp1-4.md` — Planungsbesprechung
  mit 5 Teilnehmern, 7 Themen.
- `beispiel-transkript-lp5.txt` + `beispiel-ausgabe-lp5.md` — Baustellenbegehung
  mit Mängelaufnahme und Bemusterung.
- `beispiel-state.json` — vollständiges State-File für ein laufendes Projekt.

## Konfiguration

Das Plugin braucht keine Konfiguration. Optional kannst du am Anfang eines Projekts
ein leeres State-File anlegen:

```bash
mkdir -p protokolle/553-WIL
echo '{"schema_version":1,"projekt":{"nr":"553","name":"WIL"}}' \
  > protokolle/553-WIL/protokoll-state.json
```

Das Plugin füllt das State-File mit dem ersten Protokoll vollständig auf.

## Entwicklungsstand

Version 0.1.0 — Initiale Veröffentlichung, deckt die drei Standardvorlagen
QMG-024-141 ab. Geplant:

- Export nach `.docx` direkt aus dem Plugin (Pandoc-Wrapper).
- Sondervorlage für DGNB-Workshops.
- Visualisierung des State-Files (offene Punkte, Termine, Mängelliste) als HTML-Dashboard.

## Lizenz

MIT — siehe Hauptrepo.

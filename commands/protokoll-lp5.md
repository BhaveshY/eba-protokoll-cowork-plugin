---
description: Erstellt ein Bauleitungsprotokoll LP5 (Tracking mit baustellenspezifischen Kategorien) aus einem Transkript.
argument-hint: <pfad/zur/transkript.txt> [--neu | --fortschreiben]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du erstellst ein Bauleitungsprotokoll im EBA-Format `QMG-024-141 ORG-PK-LP5`.

## Eingabe

Argument: $ARGUMENTS — Pfad zur Transkript-Datei, optional gefolgt von:
- `--neu`: erzwinge erste Besprechung im Projekt.
- `--fortschreiben`: erzwinge Fortschreibungs-Modus.

Default: automatisch erkennen.

## Vorgehen

1. **Skill `protokoll-lp5`** invocieren.
2. Bei Fortschreibung → an `protokoll-fortschreiben` weitergeben.
3. Referenzen aus `${CLAUDE_PLUGIN_ROOT}/references/`:
   - `templates/protokoll-lp5.md`
   - `categories/disziplin-kategorien.md` (LP5-Sektion)
   - `categories/firma-kuerzel.md`
   - `categories/status-codes.md`
   - `categories/sprache-und-stil.md`
   - `categories/transkript-format.md`
4. Spezifika für LP5 berücksichtigen:
   - Witterung im Header (falls aus Transkript erkennbar).
   - Mängelnummer-Nummerierung (über `letzte_mangelnummer` im State).
   - Bemusterungen als eigene Themen-Zeilen unter D/K = 04.
5. Ausgabe als **DOCX + PDF** (kein Markdown im Projekt):
   `protokolle/<projekt>/<jjjj-mm-tt>_protokoll-lp5-<NN>_<thema>.docx` und `…<thema>.pdf`.
   Pipeline: `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.
6. State-Datei aktualisieren.

## Verwendung

```
/protokoll-lp5 transkripte/2026-04-22_baustellenbegehung-w1.txt
/protokoll-lp5 transkripte/maengelbegehung.txt --fortschreiben
```

## Wann das richtige Format

- Bauphasen LP5 (Ausführungsplanung) und LP8 (Objektüberwachung).
- Baubesprechungen, Baustellenbegehungen, Mängelbegehungen, Bemusterungen, Abnahmen.
- Witterungsabhängige Termine, Gewerk-Logistik, Lieferungen.

Bei Planungsphasen LP1-4: `/protokoll-lp1-4`.

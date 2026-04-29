---
description: Erstellt ein Planungsprotokoll LP1-4 (Tracking-Format mit D/K|B|LN-Schema) aus einem Transkript.
argument-hint: <pfad/zur/transkript.txt> [--neu | --fortschreiben]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du erstellst ein Planungsprotokoll im EBA-Format `QMG-024-141 ORG-PK-(LP1-4)`.

## Eingabe

Argument: $ARGUMENTS — Pfad zur Transkript-Datei, optional gefolgt von:
- `--neu`: erzwinge erste Besprechung im Projekt (`B = 01`), auch wenn Vorprotokoll existiert.
- `--fortschreiben`: erzwinge Fortschreibungs-Modus (Vorprotokoll lesen).

Default: automatisch erkennen — wenn `protokolle/<projekt>/protokoll-state.json`
existiert, fortschreiben; sonst neu.

## Vorgehen

1. **Skill `protokoll-lp1-4`** invocieren.
2. Wenn Fortschreibungs-Modus erkannt → die Skill ruft `protokoll-fortschreiben` auf.
3. Referenzen aus `${CLAUDE_PLUGIN_ROOT}/references/` laden:
   - `templates/protokoll-lp1-4.md`
   - `categories/disziplin-kategorien.md`
   - `categories/firma-kuerzel.md`
   - `categories/status-codes.md`
   - `categories/sprache-und-stil.md`
   - `categories/transkript-format.md`
   - `categories/metadaten-konvention.md`
4. Header, Teilnehmer, Unterlagen, Themen-Tabelle (D/K|B|LN), Termine, Anlagen,
   Aufstellvermerk.
5. Ausgabe als **DOCX + PDF** (kein Markdown im Projekt):
   `protokolle/<projekt>/<jjjj-mm-tt>_protokoll-<NN>_<thema>.docx` und `…<thema>.pdf`.
   Pipeline: `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.
6. State-Datei aktualisieren / anlegen: `protokolle/<projekt>/protokoll-state.json`.

## Verwendung

```
/protokoll-lp1-4 transkripte/2026-04-15_planungsbesprechung-12.txt
/protokoll-lp1-4 transkripte/kickoff.txt --neu
```

## Wann das richtige Format

- Planungsphase (LP1 Grundlagenermittlung … LP4 Genehmigungsplanung).
- Kick-Off, Workshops, Jour Fixe, BIM-Koordination, DGNB-Abstimmungen.
- Mehrere Teilnehmer, oft externe Fachplaner.
- Tracking über mehrere Termine erwünscht.
- Fehlende Projekt-Nr., Projektname, Ort oder Ersteller ändern diese Formatwahl
  nicht; automatisch Fallbacks verwenden und als Annahmen nennen.

Bei Bauphasen ab LP5 (Ausführung): `/protokoll-lp5`.
Bei kurzen formlosen Gesprächen: `/gespraechsnotiz`.

---
description: Erstellt eine kurze EBA-Gesprächsnotiz aus einem Transkript (formloses Format, kein Tracking).
argument-hint: <pfad/zur/transkript.txt>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du erstellst eine Gesprächsnotiz im EBA-Format `QMG-024-141 ORG-GESPRAECHSNOTIZ`.

## Eingabe

Argument: $ARGUMENTS — Pfad zur Transkript-Datei.

Wenn leer, frage den Nutzer nach der Datei oder liste verfügbare Transkripte aus
`transkripte/` und `./*.txt`.

## Vorgehen

1. **Skill `gespraechsnotiz`** invocieren (über das Skill-Tool).
2. Den Anweisungen folgen:
   - Referenzen aus `${CLAUDE_PLUGIN_ROOT}/references/templates/gespraechsnotiz.md`,
     `sprache-und-stil.md` und `transkript-format.md` lesen.
   - Header (Projekt, Ort, Datum, Ersteller).
   - Teilnehmer- und Verteilertabelle.
   - Gesprächsinhalt mit hierarchischer Themenstruktur.
3. Ausgabe als **DOCX + PDF** (kein Markdown im Projekt) unter
   `protokolle/<jjjj-mm-tt>_<projekt>_gespraechsnotiz.docx` und
   `…_gespraechsnotiz.pdf`. Pipeline:
   `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

## Verwendung

```
/gespraechsnotiz transkripte/2026-04-15_kurzes-team-meeting.txt
```

## Wann das richtige Format

- Kurze, formlose Gespräche.
- ≤ 3 Teilnehmer.
- < ~10 Min Gesprächsdauer.
- Keine Notwendigkeit für Tracking über mehrere Termine.

Andernfalls: `/protokoll-lp1-4` oder `/protokoll-lp5`.

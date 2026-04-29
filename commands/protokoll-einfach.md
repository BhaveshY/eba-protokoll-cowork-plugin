---
description: Erstellt ein einfaches EBA-Protokoll (LP1-4 Word + Excel Stand A) aus einem Transkript — hierarchische Themen, Frist-Spalte, kein D/K-Tracking.
argument-hint: <pfad/zur/transkript.txt>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du erstellst ein einfaches Protokoll im EBA-Format
`QMG-024-141 ORG-PK-LP1-4-MA` (Stand A, Word-Variante) plus
`QMG-024-141 ORG-PK-LP1-4-EXCEL-MA` (Stand A, Excel-Variante).

## Eingabe

Argument: $ARGUMENTS — Pfad zur Transkript-Datei.

Wenn leer, frage den Nutzer nach der Datei oder liste verfügbare Transkripte aus
`transkripte/` und `./*.txt`.

## Vorgehen

1. **Skill `protokoll-einfach`** invocieren (über das Skill-Tool).
2. Den Anweisungen folgen:
   - Referenzen aus `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-einfach.md`,
     `sprache-und-stil.md`, `transkript-format.md`, `firma-kuerzel.md` und
     `metadaten-konvention.md` lesen.
   - Header (Projekt, Ort, Datum, Ersteller) automatisch füllen; fehlende
     Projektmetadaten mit `Projekt-Nummer = 000` und passenden Fallbacks ersetzen.
   - Teilnehmer (4 Spalten: Vorname, Name, Kürzel, Firma).
   - Verteiler (3 Spalten: Vorname, Name, Firma).
   - Gesprächsinhalt mit hierarchischer Themenstruktur und kombinierter
     Spalte „Zuständig / Frist".
3. Ausgabe als **DOCX + PDF + XLSX** (kein Markdown im Projekt) unter
   `protokolle/<jjjj-mm-tt>_<projekt-kurzname>_protokoll.docx` und
   `…_protokoll.pdf` sowie `…_protokoll.xlsx`. Pipeline:
   `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

## Verwendung

```
/protokoll-einfach transkripte/2026-04-15_kick-off.txt
```

## Wann das richtige Format

- Workshops, Kick-Offs **ohne** Folgetermin.
- Mehrere Teilnehmer, konkrete Aufgaben mit Datum, **aber kein** Tracking.
- Hinweis-Frist: 3 Kalendertage (nicht 5 wie bei LP1-4-Tracking).

Andernfalls:
- `gespraechsnotiz` — kürzer, ≤ 3 Teilnehmer, ohne Frist.
- `protokoll-lp1-4` — mit D/K|B|LN-Tracking, Status, Fortschreibung.
- `protokoll-lp5` — Bauleitung, Mängel, Bemusterungen.

## Wichtig

- Niemals den ursprünglichen Transkript verändern.
- Nicht wegen fehlender Projektmetadaten nachfragen; Fallbacks nutzen und am Ende
  transparent nennen.
- Hinweis-Text bleibt **wortgleich** mit „3 Kalendertagen".
- Spalte „Zuständig / Frist" ist **eine** kombinierte Spalte, kein Split.

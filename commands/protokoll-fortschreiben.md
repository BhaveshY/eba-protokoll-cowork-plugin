---
description: Schreibt ein bestehendes LP1-4- oder LP5-Protokoll fort — übernimmt offene Punkte, ergänzt neue Bemerkungen mit #NN-Versionsmarkern.
argument-hint: <pfad/zur/transkript.txt> [--projekt <projektordner>]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du schreibst ein bestehendes EBA-Protokoll fort.

## Eingabe

Argument: $ARGUMENTS — Pfad zur neuen Transkript-Datei. Optional `--projekt <pfad>`,
um das Projektverzeichnis explizit zu setzen.

Wenn `--projekt` fehlt: Projektverzeichnis aus dem Transkript-Pfad heuristisch
ableiten (`protokolle/<projekt>/` nahe der Transkript-Datei oder im aktuellen
Arbeitsverzeichnis).
Wenn nur Rohmetadaten fehlen, nicht abbrechen: Fallbacks aus
`${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md` verwenden.

## Vorgehen

1. **Skill `protokoll-fortschreiben`** invocieren.
2. Vorprotokoll und State laden:
   - `protokolle/<projekt>/protokoll-state.json`
   - Neuestes vorhandenes Protokoll im Projektordner.
3. Wenn keine State-Datei vorhanden: aus dem Vorprotokoll heuristisch ableiten und
   die State-Datei generieren.
4. Wenn weder State noch Vorprotokoll: dem Nutzer mitteilen, dass es keine
   Fortschreibung gibt — empfehlen, `/protokoll-lp1-4` oder `/protokoll-lp5` mit
   `--neu` zu verwenden.
5. Themen zusammenführen (Übernahme + Ergänzung + neu).
6. Ausgabe als **DOCX + PDF** schreiben (kein Markdown im Projekt), State aktualisieren.
   Auf Windows 11 mit MS Word richtet der Renderer fehlende Python-Pakete selbst
   ein und PDF ist Pflicht, sofern der Nutzer nicht ausdrücklich DOCX-only verlangt.
   Pipeline: `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

## Verwendung

```
/protokoll-fortschreiben transkripte/2026-04-22_pk-12.txt
/protokoll-fortschreiben transkripte/baubespr-08.txt --projekt protokolle/553-WIL/
```

## Output

- Pfade zu DOCX und PDF.
- Aktualisierter State (`protokoll-state.json`).
- Übersicht: übernommen / ergänzt / neu / erledigt / überfällig.

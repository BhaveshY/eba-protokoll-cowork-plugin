---
description: Bereinigt ein rohes EBA-App-Transkript vor der Protokollerstellung (Sprecher umbenennen, Turns mergen, Files zusammenführen).
argument-hint: <pfad/zur/transkript.txt> [...weitere transkripte]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du bereitest ein Transkript für die Protokollerstellung vor.

## Eingabe

Argument: $ARGUMENTS — eine oder mehrere Transkript-Dateien. Bei mehreren Dateien:
sie werden zusammengeführt (in zeitlicher Reihenfolge, Zeitstempel verschoben).

## Vorgehen

1. **Skill `transkript-vorbereiten`** invocieren.
2. Bei einer einzelnen Datei: dem Nutzer die Optionen anbieten:
   - Sprecher-Labels umbenennen (mit heuristischer Vorschlagsliste).
   - Aneinander gereihte Same-Speaker-Turns mergen.
   - Füllwörter entfernen (optional, default aus).
   - Zeitstempel-Reihenfolge reparieren (selten nötig).
3. Bei mehreren Dateien: zusammenführen.
4. Ausgabe in eine **neue Datei** schreiben — Original bleibt unangetastet:
   - Suffix `.bereinigt.txt` für eine bereinigte Version.
   - Suffix `.zusammengefuehrt.txt` für mehrere zusammengeführte.
5. Zusammenfassung: Original-Zeilen → neue Zeilen, Liste der Änderungen.

## Verwendung

```
/transkript-vorbereiten transkripte/rohaufnahme.txt
/transkript-vorbereiten transkripte/teil1.txt transkripte/teil2.txt
```

---
name: transkript-vorbereiten
description: >-
  Use when the user wants to clean up a transcript before generating a protocol
  — fixing speaker labels (renaming "Sprecher 1" to real names), merging
  adjacent same-speaker turns, removing filler words, splitting overly long
  transcripts by date, or stitching multiple transcripts of one continuous
  meeting together.
---

# Transkript vorbereiten (Pre-Processing)

Bereitet ein rohes EBA-App-Transkript so auf, dass die Protokoll-Skills die bestmögliche
Eingabe haben. Wird normalerweise **vor** den Protokoll-Skills aufgerufen, wenn der
Nutzer Qualitätsprobleme im Transkript bemängelt.

## Typische Aufgaben

### 1. Sprecher-Labels vereinheitlichen

Die EBA Protokoll App vergibt initial Labels wie `Ich`, `Sprecher 1`, `Sprecher 2`, …
Wenn der Nutzer die Sprecher in der App nicht umbenannt hat, kann diese Skill eine
**heuristische Zuordnung** anbieten:

1. Liste alle eindeutigen Labels im Transkript.
2. Suche im Transkript-Text nach Selbstvorstellungen („Mein Name ist …", „Ich bin von …"),
   nach Anreden („Herr X, …", „Frau Y, können Sie …") und nach Firma-Erwähnungen.
3. Schlage eine Zuordnung vor (z.B. `Sprecher 1 → Helge Schmidt (EBA)`), und lass den
   Nutzer bestätigen.
4. Schreibe das Transkript mit den neuen Labels in eine Kopie:
   `<original>.bereinigt.txt`. Original bleibt unangetastet.

### 2. Aneinander gereihte Same-Speaker-Turns zusammenführen

Wenn zwei aufeinanderfolgende Zeilen denselben Sprecher haben (passiert bei längeren
Pausen in der Diarisierung), zu einem Turn zusammenfassen — Zeitstempel des ersten Turns
behalten.

```
[00:01:05] Herr Müller: Ich habe die Unterlagen geprüft.
[00:01:18] Herr Müller: Es sind noch zwei Punkte offen.
```

→

```
[00:01:05] Herr Müller: Ich habe die Unterlagen geprüft. Es sind noch zwei Punkte offen.
```

### 3. Füllwörter entfernen (optional)

Auf Wunsch des Nutzers: typische Füllwörter wie „äh", „ähm", „also", „halt", „ne?" am
Satzanfang/-ende entfernen, **aber nur wenn der Nutzer das explizit möchte**. Im Default
beibehalten — die Protokoll-Skills überspringen sie ohnehin beim Zusammenfassen.

### 4. Zeitlich sortierte Sprecherwechsel reparieren

Wenn das Transkript Zeilen mit zurückspringenden Zeitstempeln enthält (Bug in der
Diarisierung), nach Zeitstempel umsortieren. Dies sollte **nur** auf expliziten Wunsch
geschehen, da es die ursprüngliche Sequenz ändert.

### 5. Mehrere Transkripte einer Besprechung zusammenführen

Wenn eine Besprechung in mehreren Dateien aufgenommen wurde (z.B. wegen App-Neustart):

1. Sortiere Dateien nach Zeitstempel.
2. Verschiebe die Zeitstempel der zweiten/dritten Datei so, dass sie an das Ende der
   vorigen anschließen (z.B. wenn Datei 1 bei `[00:45:12]` endet, Datei 2 von
   `[00:00:00]` startet, dann beginnt Datei 2 in der zusammengeführten Datei bei
   `[00:45:12]`).
3. Konkateniere zu einer Datei `<projekt>_<datum>_zusammengefuehrt.txt`.
4. Falls die Sprecher in den Dateien unterschiedlich gelabelt sind: Mapping erfragen
   und vereinheitlichen.

### 6. Ein zu langes Transkript splitten

Wenn ein Transkript mehrere getrennte Besprechungen enthält (z.B. Vormittagstermin +
Nachmittagstermin am selben Tag), nach längeren Pausen (> 15 Minuten ohne Sprache)
splitten und je Block eine separate Datei erzeugen.

## Vorgehen (allgemein)

1. **Frage den Nutzer**, was bereinigt werden soll, wenn es nicht aus dem Kontext klar ist.
2. **Lies das Originaltranskript** mit Read-Tool.
3. **Wende die gewünschten Schritte an**.
4. **Schreibe die Ausgabe** in eine neue Datei mit Suffix `.bereinigt.txt` (oder
   `.zusammengefuehrt.txt`).
5. **Berichte** dem Nutzer:
   - Originale Zeilenzahl vs. neue Zeilenzahl.
   - Liste der Änderungen (z.B. „3 Sprecher umbenannt", „17 Zeilen zusammengeführt").
   - Pfad zur neuen Datei.

## Anti-Pattern

- ❌ Original überschreiben — immer in eine neue Datei schreiben.
- ❌ Inhalt umformulieren oder „korrigieren" — nur strukturelle Bereinigung, keine
  inhaltliche Veränderung.
- ❌ Zeitstempel ohne Notwendigkeit verändern.
- ❌ Sprecher-Mapping ohne Bestätigung des Nutzers anwenden — solche Änderungen sind
  inhaltlich relevant.

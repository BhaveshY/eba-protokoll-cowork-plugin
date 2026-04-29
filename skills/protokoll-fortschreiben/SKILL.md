---
name: protokoll-fortschreiben
description: >-
  Use when generating an LP1-4, LP1-4-BIM or LP5 tracking protocol that follows
  a previous one in the same project — i.e. when a protokoll-state.json or
  earlier protocol exists in the project's protokolle/ directory. Carries open
  items forward, marks new comments as Ergänzung (LN-suffix E, prefix #NN:),
  increments the meeting number B, and preserves the project-specific D/K
  schema (LP1-4 and LP5 use 2-digit D/K, BIM uses 1-digit D/K 1–8), distribution
  list, and Firma-/Personen-Kürzel. Does not apply to Gesprächsnotiz or
  Protokoll-einfach (these formats have no tracking).
---

# Protokoll fortschreiben (Folgeprotokoll erstellen)

Übernimmt offene Punkte aus dem vorherigen Protokoll, ergänzt sie um die in der
aktuellen Besprechung neu hinzugekommenen Bemerkungen und Beschlüsse, und schreibt
ein **konsistentes Folgeprotokoll**, das sich nahtlos in die Projekt-Historie einreiht.

## Wann zu verwenden

- Ein Vorprotokoll existiert in `protokolle/<projekt>/`.
- Eine `protokoll-state.json` ist im Projektordner vorhanden.
- Der Nutzer sagt explizit „fortschreiben", „Folgeprotokoll", „weiter mit Protokoll #NN".

Diese Skill wird **aus** den Skills `protokoll-lp1-4` oder `protokoll-lp5` aufgerufen,
nachdem dort die Vorprotokoll-Erkennung getriggert hat. Sie kann auch direkt invoziert
werden, wenn der Nutzer explizit eine Fortschreibung fordert.

## Vorgehen

Bei fehlender Projekt-Nr. oder fehlendem Projekt-Namen gelten die Fallbacks aus
`${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md`. Für neue
oder nicht eindeutig zuordenbare Rohtranskripte `protokolle/000-RAW/` verwenden.
Nur wenn der Nutzer ausdrücklich eine Fortschreibung verlangt und weder State noch
Vorprotokoll auffindbar sind, ist das ein echter Blocker.

### 1. Vorprotokoll und State laden

```
protokolle/<projekt>/protokoll-state.json
protokolle/<projekt>/<jjjj-mm-tt>_protokoll-NN_<thema>.md   # neuestes vorheriges
```

Lies die State-Datei (siehe `${CLAUDE_PLUGIN_ROOT}/scripts/protokoll-state.md` für das Schema). Sie enthält:

- `projekt`: Name + Nummer.
- `dk_schema`: aktuelle Liste der genutzten D/K-Kategorien.
- `letzte_besprechung_nr`: höchstes bisher vergebenes B.
- `offene_punkte`: alle Themen mit Status `O` aus dem Vorprotokoll, samt D/K, B, LN, Beschreibung.
- `verteiler`: Master-Verteiler.
- `firma_kuerzel`: projektspezifische Kürzel-Zuordnungen.
- `letzte_mangelnummer`: nur bei LP5, die letzte vergebene Mangelnummer.

Wenn keine State-Datei vorhanden, aber ein Vorprotokoll existiert: aus dem Vorprotokoll
heuristisch ableiten und neue State-Datei erzeugen.

### 2. Aktuelles Transkript analysieren

Wie in den Skills `protokoll-lp1-4` / `protokoll-lp5` beschrieben: Themenblöcke,
Sprecher, Verantwortlichkeiten ableiten.

### 3. Neue Besprechungsnummer setzen

`B_neu = State.letzte_besprechung_nr + 1`.

### 4. Themen zusammenführen

Hier liegt der Kernlogik dieser Skill. Es entstehen drei Arten von Einträgen:

#### a) Übernahme offener Punkte ohne Änderung

Für jeden Eintrag in `state.offene_punkte`, der im aktuellen Transkript **nicht**
erwähnt wurde:

- Eintrag wird 1:1 übernommen, **mit der ursprünglichen B/LN**.
- Status bleibt `O`.
- Beschreibung bleibt unverändert.

#### b) Ergänzungen zu offenen Punkten

Für jeden Eintrag in `state.offene_punkte`, der im aktuellen Transkript **erwähnt** wurde
(neue Information, Status-Update, Konkretisierung, Erledigung):

- Original-Eintrag bleibt mit ursprünglicher B/LN, Status bleibt was er war.
- **Zusätzlich** eine neue Zeile in derselben D/K-Kategorie:
  - `B = B_neu`, `LN = <Original-LN>E` (z.B. `02E`).
  - Beschreibung beginnt mit `#<B_neu>:` als Versionsmarker (z.B. `#08:`).
  - Beschreibung enthält die neue Information aus der aktuellen Besprechung.
  - `zuständig`, `Termin`, `Status` aktualisiert auf den neuen Stand.

  Beispiel:
  > Original (B=07): `D/K=03, LN=02 — EBA bittet ZÜB um Klärung der Verkehrsplanung. zuständig: ZÜB, Termin: 16.01.26, Status: O`
  >
  > Ergänzung (B=08): `D/K=03, LN=02E — #08: Am 29.01.26 wird ein Termin bezüglich der Verkehrsplanung stattfinden. Das Büro Richter wurde beauftragt. zuständig: ZÜB, Termin: KW 6, Status: E`

- Wenn der Original-Punkt mit der Ergänzung **erledigt** ist: Status der Ergänzung auf
  `E` setzen. Der Original-Eintrag bleibt unverändert mit `O` — die Erledigung ergibt
  sich aus dem `E`-Status der jüngsten Ergänzung.

#### c) Neue Punkte aus aktueller Besprechung

Themen, die im Transkript neu sind und keinem Vorpunkt zugeordnet werden können:

- D/K aus dem Schema wählen (oder Schema erweitern, wenn neue Kategorie nötig ist).
- `B = B_neu`, `LN = <nächste freie LN in der D/K-Kategorie>`.
- Default-Status `O` für Aufgaben, `Info` für Informationspunkte, `E` für sofort
  erledigte Beschlüsse.

### 5. Sortierung der Themen-Tabelle

Innerhalb jeder D/K-Kategorie:

1. Nach `LN` aufsteigend.
2. Originaleinträge **vor** ihren Ergänzungen (also `01, 01E, 01EE, 02, 02E, …`).

So bleibt die Geschichte jedes Punktes lesbar nachvollziehbar.

### 6. Header und Teilnehmer

- Übernimm den **Verteiler** aus der State-Datei. Aktualisiere die `Teilnahme`-Spalte
  basierend auf den Sprechern im aktuellen Transkript:
  - Sprecher anwesend → `X` (oder `O` falls online erkennbar).
  - Im Verteiler aber nicht Sprecher → `N` (oder `E` falls als entschuldigt erwähnt).
- Falls in der aktuellen Besprechung neue Personen dazugekommen sind: zur
  Teilnehmer-/Verteilertabelle hinzufügen und ihre Kürzel der State-Datei hinzufügen.

### 7. State-Datei aktualisieren

Schreibe die State-Datei neu mit:

- `letzte_besprechung_nr = B_neu`.
- `offene_punkte`: alle Punkte aus dem neuen Protokoll mit Status `O` (Originaleinträge
  und Ergänzungen, deren letzter Status `O` ist).
- `verteiler`: aktualisierte Liste.
- `firma_kuerzel`: aktualisiert mit ggf. neu hinzugekommenen.
- `dk_schema`: aktualisiert mit ggf. neu hinzugekommenen Kategorien.
- `letzte_mangelnummer` (nur LP5): aktualisiert.

### 8. Ausgabe formatgetreu schreiben & Zusammenfassung

**Endformat**: Word-Ursprungsformate als DOCX + PDF; BIM/Excel-Ursprungsformate
als offizielles QMG-XLSX. **Kein Markdown** im Projekt-Ordner. Die
`protokoll-state.json` bleibt erhalten (persistente Projektzustand-Datei). Auf
Windows 11 mit MS Word bootstrapt der Renderer fehlende Python-Pakete selbst
und exportiert Word-Ursprungs-DOCX via Word zu PDF. Keine technischen
Setup-Fragen an den Nutzer.

Schritte:

1. Erzeuge das Folgeprotokoll als Markdown unter einem flüchtigen Pfad:
   `/tmp/eba-protokoll-fortschreibung-<jjjj-mm-tt>-<projekt>.md`.

2. Rufe den Renderer auf:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
     "/tmp/eba-protokoll-fortschreibung-<datum>-<projekt>.md" \
     --format <protokoll-lp1-4|protokoll-bim|protokoll-lp5> \
     --out-dir "protokolle/<projekt>/"
   ```

3. Wähle den `--format`-Wert aus dem bestehenden Projekt-State bzw. dem
   erkannten Protokolltyp, damit die passende QMG-Tracking-Vorlage genutzt wird.
4. Schreibe die aktualisierte `protokolle/<projekt>/protokoll-state.json`.
   Wenn der Renderer bei einem Word-Ursprungsformat einen Windows-PDF-Fehler
   meldet, stderr lesen, denselben Befehl nach der automatischen Selbstheilung
   erneut versuchen und erst danach echte Blocker melden.

Berichte dem Nutzer:

- Pfade der erzeugten DOCX/PDF- oder XLSX-Datei.
- Anzahl übernommener offener Punkte ohne Änderung.
- Anzahl Ergänzungen zu Vorpunkten (mit kurzer Auflistung der LN-Referenzen).
- Anzahl neu eröffneter Punkte.
- Anzahl in dieser Besprechung erledigter Punkte (Status-Wechsel von `O` auf `E`).
- Anzahl überfälliger Punkte (Termin liegt vor dem aktuellen Datum, Status weiterhin `O`).

Volle Pipeline-Beschreibung:
`${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

### 9. Optionale „Ausblenden"-Logik

Erledigte Punkte aus früheren Besprechungen können in der Markdown-Ausgabe
optional **ausgeblendet** werden, um das Protokoll lesbarer zu machen. Standard:
ab Protokoll Nr. 2 alle erledigten Punkte aus Besprechungen `B < B_neu - 1`
ausblenden, in einem zusätzlichen „Archiv"-Abschnitt am Ende des Protokolls auflisten.

Diese Logik ist konfigurierbar — der Nutzer kann „nichts ausblenden" oder „alle
erledigten ausblenden" wählen.

## Anti-Pattern

- ❌ Offene Punkte aus dem Vorprotokoll silently weglassen — sie müssen mindestens
  unverändert übernommen werden.
- ❌ B-Nummer nicht hochzählen — jedes neue Protokoll braucht eine neue B-Nummer.
- ❌ Ergänzungen ohne `#NN:`-Prefix schreiben — der Versionsmarker macht die Historie
  lesbar.
- ❌ Original-Eintrag verändern, wenn eine Ergänzung dazukommt — Original bleibt
  unverändert, Ergänzung kommt als neue Zeile dazu.
- ❌ Verteiler bei jedem Protokoll neu „raten" — er kommt aus der State-Datei.

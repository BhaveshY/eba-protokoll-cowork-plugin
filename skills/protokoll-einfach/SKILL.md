---
name: protokoll-einfach
description: >-
  Use when the user asks for a "Protokoll einfach", "einfaches Protokoll",
  "Protokoll ohne Tracking", "Workshop-Protokoll ohne D/K", "Kick-Off Notiz",
  or "simple meeting protocol with deadlines but no tracking". Produces the EBA
  QMG-024-141 ORG-PK-LP1-4-MA Word format (Stand A): hierarchical theme
  numbering (Thema 01.1), combined "Zuständig / Frist" column, 3-day notice
  period, no status column, no D/K|B|LN scheme.
---

# Einfaches Protokoll erstellen

Erstellt ein Protokoll im EBA-Format `QMG-024-141 ORG-PK-LP1-4-MA` (Stand A,
Word-Variante). Dieses Format liegt **zwischen** Gesprächsnotiz und voller
LP1-4-Tracking: hierarchische Themen mit Frist-Spalte, aber **ohne** D/K|B|LN-Schema
und **ohne** Status.

## Wann dieses Format

- Workshop oder Kick-Off **ohne** Folgetermin (kein Tracking nötig).
- Kurze Planungsbesprechung mit konkreten Fristen, aber wenigen offenen
  Trackingpunkten.
- Mehr als 3 Sprecher und Aufgaben mit Datum, aber **noch kein** D/K-Schema
  im Projekt etabliert.

Wenn Tracking, Status-Spalte oder Fortschreibung gebraucht wird → `protokoll-lp1-4`.
Wenn weniger als 3 Sprecher und kein Datum → `gespraechsnotiz`.

## Vorgehen

### 1. Referenzen laden

Lies in dieser Reihenfolge (mit Read-Tool):

1. `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-einfach.md` — die Markdown-Vorlage.
2. `${CLAUDE_PLUGIN_ROOT}/references/categories/sprache-und-stil.md` — Stilregeln.
3. `${CLAUDE_PLUGIN_ROOT}/references/categories/transkript-format.md` — Eingabeformat.
4. `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md` — Kürzel-Verzeichnis.

### 2. Transkript einlesen und analysieren

Mit Read-Tool die ganze Datei einlesen.

**Sprecher identifizieren**: Alle eindeutigen Namen vor dem ersten Doppelpunkt jeder
Zeile sammeln. Den Sprecher `Ich` als Protokollersteller behandeln.

**Themen erkennen**: Das Transkript in inhaltliche Blöcke (Themen) aufteilen.
Übergangsphrasen wie „Nächster Punkt", „Kommen wir zu …", „Kurz zu …" markieren
typischerweise einen Themenwechsel.

**Verantwortlichkeiten und Fristen ableiten**: Pro Thema den oder die Verantwortlichen
und — wenn genannt — den konkreten Liefertermin.

### 3. Header befüllen

- **Projektname** / **Projekt-Nummer** / **Projekt-Beschreibung**: aus dem Transkript
  oder vom Nutzer abfragen, wenn nichts erkennbar ist.
- **Ort**: erstes erwähntes Ort-Wort, sonst „nicht angegeben".
- **Gesprächsdatum**: aus Dateiname (`YYMMDD_…`) oder dem ersten Zeitstempel.
- **Erstelldatum**: heutiges Datum.
- **Ersteller**: Kürzel des Protokollerstellers.

Die Hinweis-Box bleibt **wortgleich** — sie erwähnt **3 Kalendertage**, nicht 5.

### 4. Teilnehmer- und Verteilertabelle erstellen

**Teilnehmer**-Tabelle (4 Spalten): `Vorname | Name | Kürzel | Firma`. Eine Zeile
pro identifiziertem Sprecher.

**Verteiler**-Tabelle (3 Spalten): `Vorname | Name | Firma`. Default: kopiert die
Teilnehmertabelle ohne Kürzel-Spalte. Wenn im Transkript explizit zusätzliche
Verteilerempfänger genannt werden, ergänzen.

### 5. Gesprächsinhalt befüllen

Pro erkanntem Themenblock eine Zeile (oder Hauptzeile + Unterzeilen mit Hierarchie):

- **Thema NN** / **NN.M**: kurze Bezeichnung (3–6 Wörter).
- **Beschreibung**: 2–6 Sätze prägnant zusammengefasst, **nie wörtlich zitieren**.
  Aktive Stimme, sachlicher Ton. Implizite Aufgaben mit aufnehmen.
- **Zuständig / Frist**: kombinierte Spalte. Format:
  - Mit Datum: `EBA / 27.03.26`
  - Mit KW: `WB / KW 13`
  - Ohne konkreten Termin: `EBA / –`
  - Reiner Info-Punkt: `– / –` oder `Info / –`

Bei Unterthemen: `Thema 01`, `Thema 01.1`, `Thema 01.2`, `Thema 02`, …

### 6. Ausgabe als DOCX + PDF schreiben

**Endformat**: DOCX + PDF. **Kein Markdown** im Projekt-Ordner.
Auf Windows 11 mit MS Word bootstrapt der Renderer fehlende Python-Pakete
selbst und exportiert die PDF via Word. Keine technischen Setup-Fragen an den
Nutzer.

Schritte:

1. Erzeuge das Protokoll als Markdown unter einem flüchtigen Pfad:
   `/tmp/eba-protokoll-einfach-<jjjj-mm-tt>-<projekt-kuerzel>.md`.
   Verwende **exakt** die Markdown-Struktur aus
   `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-einfach.md`. Die
   „Hinweis"-Box bleibt wortgleich (mit **3 Kalendertagen**, nicht 5).

2. Rufe den Renderer auf:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
     "/tmp/eba-protokoll-einfach-<datum>-<kuerzel>.md" \
     --out-dir "protokolle/"
   ```

3. Der Renderer schreibt
   `protokolle/eba-protokoll-einfach-<datum>-<kuerzel>.docx` und
   `protokolle/eba-protokoll-einfach-<datum>-<kuerzel>.pdf`,
   und löscht das MD-Zwischenformat. Wenn der Renderer einen Windows-PDF-Fehler
   meldet, stderr lesen, denselben Befehl nach der automatischen Selbstheilung
   erneut versuchen und erst danach echte Blocker melden.

**EBA-Dateinamen-Konvention** (wenn vom Nutzer gewünscht): siehe
`${CLAUDE_PLUGIN_ROOT}/references/categories/dateinamen-konvention.md`. Schema:
`<PrjNr>-<PrjKZ>-EBA-WS-PK-<JJMMTT>` (ohne Endung; Renderer hängt `.docx`/`.pdf` an).

Volle Pipeline-Beschreibung:
`${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

### 7. Zusammenfassung an den Nutzer

Nach dem Schreiben kurz mitteilen:

- Pfad zur erzeugten Datei.
- Anzahl der erkannten Teilnehmer.
- Anzahl der Themen (mit Aufschlüsselung Hauptthemen / Unterpunkte).
- Anzahl von Aufgaben mit konkreter Frist.
- Punkte, die als unklar markiert wurden und Klärung brauchen.

## Anti-Pattern

- ❌ Status-Spalte (O / E / Info) einfügen — dafür ist `protokoll-lp1-4` zuständig.
- ❌ D/K-Kategorienheader einfügen — dieses Format hat **keine** D/K-Spalte.
- ❌ Frist und Zuständig in zwei separate Spalten splitten — das Format hat
  eine **kombinierte** Spalte „Zuständig / Frist".
- ❌ Hinweis-Text mit „5 Kalendertagen" übernehmen — dieses Format hat
  **3 Kalendertage**.

---
name: gespraechsnotiz
description: >-
  Use when the user asks for a "Gesprächsnotiz", "kurze Notiz",
  "conversation note", "kurzes Protokoll", "informelle Notiz", or has a short
  transcript (under ~1500 words, ≤3 speakers, no LP-specific vocabulary) that
  should be turned into the simple EBA Gesprächsnotiz format (no D/K|B|LN
  tracking, no status column).
---

# Gesprächsnotiz erstellen

Erstellt eine **formlose, einmalige Gesprächsnotiz** im EBA-Format
`QMG-024-141 ORG-GESPRAECHSNOTIZ` (Stand D).

## Vorgehen

### 1. Referenzen laden

Lies in dieser Reihenfolge (mit Read-Tool):

1. `${CLAUDE_PLUGIN_ROOT}/references/templates/gespraechsnotiz.md` — die Markdown-Vorlage.
2. `${CLAUDE_PLUGIN_ROOT}/references/categories/sprache-und-stil.md` — Stilregeln.
3. `${CLAUDE_PLUGIN_ROOT}/references/categories/transkript-format.md` — Eingabeformat.

### 2. Transkript einlesen und analysieren

Mit Read-Tool die ganze Datei einlesen.

**Sprecher identifizieren**: Alle eindeutigen Namen vor dem ersten Doppelpunkt jeder
Zeile sammeln. Den Sprecher `Ich` als Protokollersteller behandeln.

**Themen erkennen**: Das Transkript in inhaltliche Blöcke (Themen) aufteilen. Die
Zeitstempel helfen — typischerweise gibt es alle 1–5 Minuten einen Themenwechsel,
markiert durch Übergangsphrasen wie „Nächster Punkt", „Kommen wir zu …", „Kurz zu …".

**Verantwortlichkeiten ableiten**: Für jedes Thema, wer hat was gesagt, wer übernimmt
welche Aufgabe. „Ich kümmere mich darum" → der Sprecher ist verantwortlich.
„Können Sie das machen?" + Bestätigung → der Angesprochene.

### 3. Header befüllen

Aus den Metadaten:

- **Projektname** / **Projekt-Nummer** / **Projekt-Beschreibung**: aus dem Transkript
  oder vom Nutzer abfragen, wenn nichts erkennbar ist.
- **Ort**: erstes erwähntes Ort-Wort (Stadt, Büro), sonst „nicht angegeben".
- **Gesprächsdatum**: aus Dateiname (`YYMMDD_…`) oder dem ersten Zeitstempel des Tages.
- **Erstelldatum**: heutiges Datum (`<currentDate>`).
- **Ersteller**: Kürzel des Protokollerstellers — entweder aus dem App-Sprechernamen
  ableiten (wenn `Ich` umbenannt wurde) oder beim Nutzer rückfragen.

### 4. Teilnehmer- und Verteilertabelle erstellen

Eine Zeile pro identifiziertem Sprecher. Für jeden:

- **Vorname**, **Name**: aus dem Transkript-Sprecherlabel. Wenn nur ein Nachname
  erkennbar ist, Vorname leer lassen oder mit `–` füllen.
- **Kürzel**: aus dem Verzeichnis `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md` oder neu
  ableiten (Vorname-Initiale + Nachname-Initiale).
- **Firma**: aus Kontext im Transkript (z.B. „Wir bei Züblin …"). Wenn nichts erwähnt:
  leer lassen.

Verteiler: kopiert die Teilnehmertabelle. Falls im Transkript explizit zusätzliche
Personen genannt werden, die das Protokoll bekommen sollen, ergänzen.

### 5. Themenbereich befüllen

Pro erkanntem Themenblock eine Zeile (oder Hauptzeile + Unterzeilen mit Hierarchie):

- **Thema NN**: kurze Bezeichnung (3–6 Wörter, z.B. „Brandschutzkonzept Zwischenstand").
- **Beschreibung**: 2–6 Sätze prägnant zusammengefasst, **nie wörtlich zitieren**. Aktive
  Stimme, sachlicher Ton. Implizite Aufgaben mit aufnehmen.
- **Zuständig**: Kürzel des Verantwortlichen (oder `–` bei reinen Informationspunkten).

Bei Unterthemen: `Thema 01`, `Thema 01.1`, `Thema 01.2`, `Thema 02`, …

### 6. Ausgabe als DOCX + PDF schreiben

**Endformat**: DOCX + PDF. **Kein Markdown** im Projekt-Ordner.
Auf Windows 11 mit MS Word bootstrapt der Renderer fehlende Python-Pakete
selbst und exportiert die PDF via Word. Keine technischen Setup-Fragen an den
Nutzer.

Schritte:

1. Erzeuge die Notiz als Markdown unter einem flüchtigen Pfad:
   `/tmp/eba-gespraechsnotiz-<jjjj-mm-tt>-<projekt-kuerzel>.md`.
   Verwende **exakt** die Markdown-Struktur aus
   `${CLAUDE_PLUGIN_ROOT}/references/templates/gespraechsnotiz.md`. Die
   „Hinweis"-Box bleibt wortgleich.

2. Rufe den Renderer auf:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
     "/tmp/eba-gespraechsnotiz-<datum>-<kuerzel>.md" \
     --out-dir "protokolle/"
   ```

3. Der Renderer schreibt
   `protokolle/eba-gespraechsnotiz-<datum>-<kuerzel>.docx` und
   `protokolle/eba-gespraechsnotiz-<datum>-<kuerzel>.pdf`,
   und löscht das MD-Zwischenformat. Wenn der Renderer einen Windows-PDF-Fehler
   meldet, stderr lesen, denselben Befehl nach der automatischen Selbstheilung
   erneut versuchen und erst danach echte Blocker melden.

**EBA-Dateinamen-Konvention** (wenn vom Nutzer gewünscht): siehe
`${CLAUDE_PLUGIN_ROOT}/references/categories/dateinamen-konvention.md`. Schema:
`<PrjNr>-<PrjKZ>-EBA-GN-<JJMMTT>` (ohne Endung; Renderer hängt `.docx`/`.pdf` an).

Volle Pipeline-Beschreibung:
`${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

### 7. Zusammenfassung an den Nutzer

Nach dem Schreiben kurz mitteilen:

- Pfad zur erzeugten Datei.
- Anzahl der erkannten Teilnehmer.
- Anzahl der Themen.
- Anzahl impliziter Aufgaben mit Verantwortlichkeit.
- Punkte, die als unklar markiert wurden und Klärung brauchen.

## Anti-Pattern

- ❌ Status-Spalte einfügen — Gesprächsnotizen haben keine Status. Wenn Tracking
  nötig ist: Skill `protokoll-lp1-4` oder `protokoll-lp5` verwenden.
- ❌ Aus Gesprächsnotiz nachträglich ein Tracking-Protokoll ableiten — das ist eine
  Format-Änderung, die mit dem Nutzer abgestimmt werden muss.
- ❌ Mehr als 3 Sprecher zwingen — bei großen Runden ist eher LP1-4 angebracht.

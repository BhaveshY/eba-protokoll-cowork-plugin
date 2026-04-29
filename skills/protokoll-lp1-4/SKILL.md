---
name: protokoll-lp1-4
description: >-
  Use when the user asks for a "Protokoll LP1-4", "Planungsprotokoll",
  "Planungsbesprechung", "Jour Fixe", "Kick-Off", "BIM-Koordination",
  "Workshop-Protokoll", or has a transcript from a planning-phase meeting
  (LP1-Grundlagenermittlung, LP2-Vorplanung, LP3-Entwurfsplanung,
  LP4-Genehmigungsplanung). Produces the EBA QMG-024-141 ORG-PK-(LP1-4)
  tracking protocol with D/K|B|LN topic numbering, status column, and continuous
  tracking across meetings.
---

# Planungsprotokoll LP1-4 erstellen

Erstellt ein **fortschreibungsfähiges Protokoll** im EBA-Format
`QMG-024-141 ORG-PK-LP1-4-EXCEL-MA` (Stand A) bzw. dessen Word-Pendant. Das Protokoll
verwendet die D/K|B|LN-Nummerierung und ist für **kontinuierliches Tracking** über
mehrere Besprechungen hinweg ausgelegt.

## Vorgehen

### 1. Referenzen laden

Lies in dieser Reihenfolge:

1. `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp1-4.md` — die Markdown-Vorlage.
2. `${CLAUDE_PLUGIN_ROOT}/references/categories/disziplin-kategorien.md` — D/K-Schema.
3. `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md` — Firma- und Personen-Kürzel.
4. `${CLAUDE_PLUGIN_ROOT}/references/categories/status-codes.md` — Status- und Teilnahme-Codes.
5. `${CLAUDE_PLUGIN_ROOT}/references/categories/sprache-und-stil.md` — Stilregeln.
6. `${CLAUDE_PLUGIN_ROOT}/references/categories/transkript-format.md` — Eingabeformat.
7. `${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md` — Fallbacks für rohe Transkripte.

### 2. Vorprotokoll prüfen (wenn vorhanden)

Wenn ein vorheriges Protokoll im selben Projektordner existiert:
`protokolle/<projekt>/protokoll-NN-…md` oder `protokolle/<projekt>/protokoll-state.json`.

→ Lies das vorherige Protokoll und/oder den State.
→ **Folge dann der Skill `protokoll-fortschreiben`**, statt von Grund auf neu zu
  erzeugen. Diese Skill übernimmt:
  - Übernahme aller offenen Punkte (`Status = O`).
  - Markierung neuer Bemerkungen als Ergänzung (`LN = NNE`, Beschreibung mit `#NN:`-Prefix).
  - Hochzählen der Besprechungs-Nummer `B`.
  - Fortführung des projektspezifischen D/K-Schemas.

Wenn kein Vorprotokoll existiert: `B = 01` (erste Besprechung) und mit Schritt 3 fortfahren.

### 3. Header befüllen

- **Besprechung Nr.**: `01` für die erste Besprechung im Projekt, sonst aus Vorprotokoll
  hochgezählt. Wird vom Nutzer bestätigt oder überschrieben.
- **Besprechungsthema**: aus Transkript ableiten (z.B. „Kick-Off Meeting",
  „Planungsbesprechung #11", „BIM-Koordination JF-07").
- **Projekt-Nr.** und **Projekt-Name**: aus Transkript ableiten. Wenn nichts
  erkennbar ist, **nicht abbrechen**: Fallbacks aus `metadaten-konvention.md`
  verwenden (`Projekt-Nr. = 000`, Projektname aus Datei/Thema oder `EBA / Allgemein`).
- **Ort**: aus Transkript (z.B. „Berlin", „Online", „Präsenz / Online"), sonst
  `nicht angegeben`.
- **Datum**: aus Dateinamen oder Transkript, sonst heutiges Datum.
- **Zeit**: erster und letzter Zeitstempel im Transkript ergeben Anfang und Ende;
  ohne Zeitstempel `nicht angegeben`.

Fehlende Projektmetadaten ändern den Protokolltyp nicht: ein klarer Planungs-JF
oder BIM-JF bleibt LP1-4/BIM, nur die Headerfelder bekommen Fallbacks.

Die Vorbemerkungs-Box („5 Kalendertage …") bleibt **wortgleich** wie im Template.

### 4. Teilnehmertabelle befüllen

Eine Zeile pro Sprecher. Spalten:

- `Vorname` / `Name` / `KZ` — aus Transkript bzw. Kürzel-Verzeichnis.
- `Firma` — aus Kontext (z.B. „Bei uns bei DES …").
- `Firma-KZ` — aus `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md`.
- `Teilnahme` — Default: `X` (anwesend) für aktive Sprecher. Wenn aus dem Transkript
  hervorgeht, dass jemand nur online war (z.B. Nennung von „in der Videokonferenz"),
  dann `O`.
- `Verteiler` — Default: `X` (jeder Teilnehmer steht auch im Verteiler).

Falls aus dem Vorprotokoll ein Verteiler bekannt ist und Personen darin nicht in der
aktuellen Besprechung waren, übernimm sie mit `Teilnahme = N` (oder `E`, falls als
entschuldigt erwähnt) und `Verteiler = X`.

### 5. Besprochene Unterlagen

Aus dem Transkript: was wurde übergeben/gezeigt? Beispiele aus echten Protokollen:
„Planstand", „IFC-Modell vom 24.03.26", „Brandschutzkonzept v2", „TGA-Schemata".

Wenn nichts explizit übergeben wurde, die Tabelle mit einer einzigen Zeile
„Planstand | – | – | – | –" füllen oder ganz weglassen, wenn nicht relevant.

### 6. Themen-Tabelle (D/K|B|LN-Schema) befüllen

Das ist der **wichtigste Schritt**. Für jeden inhaltlichen Block im Transkript:

#### a) D/K (Disziplin/Kategorie) zuordnen

Anhand des Themas die passende Kategorie aus dem Schema in
`${CLAUDE_PLUGIN_ROOT}/references/categories/disziplin-kategorien.md` wählen. Default-Schema:

- 01 Organisation, 02 Termine, 03 Planungsvorgaben/Entscheidungen, 04 Kosten,
  05 Flächen, 06 Objektplanung, 07 Tragwerksplanung, 08 TGA, 09 Brandschutz,
  10 Freianlagen.

Bei BIM-Koordinationsterminen das BIM-Schema verwenden.
Ein `BIM-PK-JF`, `BIM-Jour-Fixe` oder `EBA_BIM-PK-JF` bleibt die LP1-4-BIM-Variante,
auch wenn Generalunternehmer, ausführende Firmen oder Züblin BIM-Management teilnehmen.
Nur bei ausdrücklichem LP5-/Baustellen-Hinweis auf `/protokoll-lp5` wechseln.

Pro D/K-Kategorie eine Header-Zeile (`D/K = 03`, restliche Spalten leer, Beschreibung
wie „**Planungsvorgaben / Entscheidungen**"), dann die Themen darunter.

#### b) B (Besprechungsnummer)

Bei der ersten Besprechung im Projekt: `B = 01`. Bei späteren: aus Vorprotokoll-State.

#### c) LN (Laufende Nummer)

Pro D/K-Kategorie hochzählend (`01`, `02`, `03`, …). Innerhalb einer D/K-Kategorie sind
alle LNs eindeutig.

#### d) Beschreibung

Prägnante Zusammenfassung in 1–6 Sätzen. Aktive Stimme. Firmenkürzel als Subjekt:
„EBA weist darauf hin, dass …", „ZÜB übernimmt die Abstimmung mit …".

Bei Aufzählungen: Bullet-Points mit `•` oder `-`.

#### e) zuständig

Firma-KZ (oder mehrere durch Leerzeichen getrennt). Bei reiner Information: `Info`.
Bei „alle Teilnehmer betroffen": `Alle`.

#### f) Termin

Konkretes Datum (`TT.MM.JJ`) oder `KW NN`. Niemals „nächste Woche" oder „bald".

#### g) Status

- `O` (offen): Aufgabe noch nicht erledigt — Default für neue Aktionspunkte.
- `E` (erledigt): wurde abschließend erledigt oder im Gespräch beschlossen.
- `Info`: reine Information ohne Handlungsbedarf.

### 7. Termine-Tabelle (Folgetermine)

Aus dem Transkript: welche zukünftigen Besprechungen wurden vereinbart? Eine Zeile
pro Termin mit Thema, Teilnehmer-Kürzeln, Ort, Datum, Zeit.

### 8. Anlagen

Wenn im Transkript explizit Anlagen erwähnt werden („siehe Anlage", „im Anhang"), dort
auflisten. Sonst weglassen oder als „keine" vermerken.

### 9. Aufstellvermerk

- **Erstellt durch**: Kürzel des Protokollerstellers.
- **Erstelldatum**: heute (`<currentDate>`).
- **Geprüft durch / Prüfdatum**: leer lassen — wird später von der prüfenden Person
  ausgefüllt.

### 10. Ausgabe als DOCX + PDF + XLSX schreiben & State aktualisieren

**Endformat**: DOCX + PDF + offizielles QMG-XLSX. **Kein Markdown** im
Projekt-Ordner.
Auf Windows 11 mit MS Word bootstrapt der Renderer fehlende Python-Pakete
selbst und exportiert die PDF via Word. Keine technischen Setup-Fragen an den
Nutzer.

Schritte:

1. Erzeuge das Protokoll als Markdown unter einem flüchtigen Pfad:
   `/tmp/eba-protokoll-lp1-4-<jjjj-mm-tt>-<projekt>.md` (bzw.
   `/tmp/eba-protokoll-bim-...md` für BIM-Koordinationen).
   Die Vorbemerkungs-Box bleibt wortgleich (mit **5 Kalendertagen**).

2. Rufe den Renderer auf:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
     "/tmp/eba-protokoll-lp1-4-<datum>-<projekt>.md" \
     --format protokoll-lp1-4 \
     --out-dir "protokolle/<projekt>/"
   ```

   Für BIM-Koordinationen `--format protokoll-bim` verwenden.

3. Der Renderer schreibt
   `protokolle/<projekt>/eba-protokoll-lp1-4-<datum>-<projekt>.docx`,
   die zugehörige `.pdf` und das offizielle `.xlsx`, und löscht das
   MD-Zwischenformat. Das Format wird vom
   Renderer als `protokoll-lp1-4` bzw. bei BIM-Ankern als `protokoll-bim`
   erkannt. Wenn der Renderer einen
   Windows-PDF-Fehler meldet, stderr lesen, denselben Befehl nach der
   automatischen Selbstheilung erneut versuchen und erst danach echte Blocker
   melden.

Wenn kein Projektordner ableitbar ist, `protokolle/000-RAW/` verwenden.

**EBA-Dateinamen-Konvention** (wenn der Nutzer das wünscht oder im
Projekt etabliert ist): siehe
`${CLAUDE_PLUGIN_ROOT}/references/categories/dateinamen-konvention.md`. Schema:
`<PrjNr>-<PrjKZ>-EBA-PLB-PK-<JJMMTT>` (ohne Endung; Renderer hängt
`.docx`/`.pdf` an), z.B. `553-WIL-EBA-PLB-PK-260324.docx`. Für die
BIM-Variante: `<PrjNr>-<PrjKZ>-EBA_BIM-PK-JF-<NN>_<JJMMTT>`.

Volle Pipeline-Beschreibung:
`${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

Aktualisiere die State-Datei `protokolle/<projekt>/protokoll-state.json` (siehe
`${CLAUDE_PLUGIN_ROOT}/scripts/protokoll-state.md` für das Format) — sie enthält:

- `projekt`: Projektname und -nummer.
- `dk_schema`: Liste der projektspezifisch genutzten D/K-Kategorien.
- `letzte_besprechung_nr`: aktuelles `B`.
- `offene_punkte`: alle Themen mit `Status = O` zur Übernahme in das nächste Protokoll.
- `verteiler`: Master-Verteilerliste.
- `firma_kuerzel`: projektspezifische Firma- und Personen-KZ-Zuordnungen.

### 11. Zusammenfassung an den Nutzer

- Pfad zur erzeugten Datei.
- Pfad zur State-Datei (für Folgeprotokolle).
- Anzahl Teilnehmer / D/K-Kategorien / Themen / offene vs. erledigte Punkte.
- Annahmen/Fallbacks knapp nennen, z.B. `Projekt-Nr. 000, Ort nicht angegeben`.
- Punkte, die fachlich unklar sind und später geprüft werden sollten.

## BIM-Koordinations-Sondervariante

Wenn das Transkript ein BIM-Koordinations-JF ist (siehe Auto-Erkennung in der
`eba-protokoll`-Skill), verwende:

- **Besprechungsthema**: „BIM-Koordination" mit JF-Nummer.
- **D/K-Schema**: BIM-Variante aus `disziplin-kategorien.md` (1 Organisation,
  2 Termine, 3 Modellierungsvorgaben, 4 Modell Allgemein, 5 ARC, 6 TWP, 7 TGA,
  8 Sonstiges).
- Spalte `ausblenden = x` für erledigte Themen (wird in Markdown nicht dargestellt,
  aber im State-File getrackt).
- Beispielpaar: `references/examples/beispiel-transkript-bim.txt` und
  `references/examples/beispiel-ausgabe-bim.md`.

## Anti-Pattern

- ❌ Eine D/K-Kategorie auslassen, weil sie in der aktuellen Besprechung leer wäre —
  wenn sie im Projekt-D/K-Schema definiert ist, sollte sie zumindest mit dem Header
  erscheinen (auch wenn ohne Themenzeilen).
- ❌ LN-Nummerierung kategorienübergreifend zählen — LNs sind **pro D/K-Kategorie**.
- ❌ Vorbemerkungs-Text umschreiben — er ist Standardtext.
- ❌ Den State der vorherigen Besprechungen vergessen — bei Fortschreibung **immer**
  Vorprotokoll lesen.
- ❌ Erledigte Punkte aus dem Vorprotokoll silently löschen — sie bleiben mit
  `Status = E` im Protokoll und werden ggf. mit `ausblenden = x` versteckt.

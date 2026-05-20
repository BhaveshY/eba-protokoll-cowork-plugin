---
name: protokoll-lp5
description: >-
  Use when the user asks for a "Protokoll LP5", "Bauleitungsprotokoll",
  "Baubesprechung", "Baustelle", "Mängelprotokoll", "Bemusterungsprotokoll", or
  has a transcript from a construction-phase meeting (LP5 Ausführungsplanung /
  LP8 Objektüberwachung). Produces the EBA QMG-024-141 ORG-PK-LP5 tracking
  protocol with construction-specific D/K categories (Mängel, Bemusterung,
  Bauablauf, …). Do not use for pure BIM-Koordination, BIM-Jour-Fixe,
  BIM-PK-JF, IFC, BCF, BIMcollab, CDE, BAP, LOIN, or Datendrop transcripts
  unless the user explicitly asks for LP5.
---

# Bauleitungsprotokoll LP5 erstellen

Erstellt ein **fortschreibungsfähiges Protokoll** im EBA-Format
`QMG-024-141 ORG-PK-LP5-MA` (Stand B). Strukturell identisch zum LP1-4-Tracking-Protokoll,
aber mit **baustellenspezifischen D/K-Kategorien** und zusätzlichen Konventionen für
Mängel, Bemusterungen und Witterung.

## Vorgehen

### 1. Referenzen laden

Lies in dieser Reihenfolge:

1. `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp5.md` — die Markdown-Vorlage für LP5.
2. `${CLAUDE_PLUGIN_ROOT}/references/categories/disziplin-kategorien.md` — D/K-Schema (LP5-Sektion).
3. `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md`
4. `${CLAUDE_PLUGIN_ROOT}/references/categories/status-codes.md`
5. `${CLAUDE_PLUGIN_ROOT}/references/categories/sprache-und-stil.md`
6. `${CLAUDE_PLUGIN_ROOT}/references/categories/transkript-format.md`
7. `${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md`

### 2. Vorprotokoll prüfen

Wie bei LP1-4: wenn ein Vorprotokoll existiert, an `protokoll-fortschreiben` übergeben.
Sonst `B = 01` setzen und mit Schritt 3 fortfahren.

### 3. Header befüllen

Spezifisch für LP5:

- **Besprechungsthema**: typischerweise „Baubesprechung Nr. NN", „Jour Fixe Bauleitung",
  „Baustellenbegehung", „Mängelbegehung".
- **Witterung**: wenn aus dem Transkript erkennbar (z.B. „heute morgen war es regnerisch"),
  in der Vorbemerkung erwähnen: „Witterung: regnerisch, ca. 8 °C".
- **Ort**: Adresse der Baustelle, falls aus dem Transkript erkennbar.
- **Projekt-Nr. / Projekt-Name**: aus Transkript ableiten. Wenn nichts erkennbar
  ist, **nicht abbrechen**: Fallbacks aus `metadaten-konvention.md` verwenden
  (`Projekt-Nr. = 000`, Projektname aus Datei/Thema oder `EBA / Allgemein`).
- **Datum / Zeit / Ersteller**: wie LP1-4; fehlende Werte mit
  `metadaten-konvention.md` füllen.

Fehlende Projektmetadaten ändern den Protokolltyp nicht: eine klare Baubesprechung,
Baustellenbegehung oder Mängelbegehung bleibt LP5, nur die Headerfelder bekommen
Fallbacks.

### 4. Teilnehmer

Wie LP1-4. Achte auf zusätzliche typische Teilnehmer in LP5:

- Polier / Bauleiter der ausführenden Firma.
- Vertreter der einzelnen Gewerke (Rohbau, TGA, Dach, Fassade, …).
- Bauherr / Bauherrenvertreter.
- Sachverständige (z.B. Brandschutz-Prüfsachverständiger).

### 5. Besprochene Unterlagen

Im Bauleitungs-Kontext häufig:

- Bauzeitenplan, aktuelle Version.
- Mängellisten.
- Werkpläne.
- Lieferscheine / Nachträge.
- Abnahmeprotokolle.

### 6. Themen-Tabelle (LP5-D/K-Schema)

Default-Schema:

| D/K | Kategorie |
|-----|-----------|
| 01  | Organisation / Baustelle |
| 02  | Termine / Bauzeitenplan |
| 03  | Bauablauf / Logistik / Andienung |
| 04  | Kosten / Nachträge / Bemusterung |
| 05  | Mängel / Abnahmen |
| 06  | Rohbau |
| 07  | Tragwerk / Statik |
| 08  | TGA |
| 09  | Brandschutz |
| 10  | Fassade / Dach |
| 11  | Innenausbau |
| 12  | Freianlagen |

Innerhalb der Kategorie 04 oder 05 können einzelne **Mängelpunkte** als eigene Zeilen
geführt werden mit dem Format:

> M-NNN: <Kurzbeschreibung>. <Detail>. <Behebungsfrist>.

Wobei `M-NNN` die durchlaufende Mangelnummer im Projekt ist (über alle Protokolle hinweg
hochgezählt — im State-File getrackt).

### 7. Bemusterungen

Wenn im Transkript eine Bemusterung dokumentiert wird:

- Eigene Themenzeile in D/K = 04 (Kosten / Nachträge / Bemusterung).
- Beschreibung: Produkt, Hersteller, Variante, Entscheidung des Bauherrn.
- Verweis auf Foto-/Anlage-Nummer, falls vorhanden.

### 8. Termine, Anlagen, Aufstellvermerk

Wie LP1-4. Bei LP5 oft besonders wichtig:

- **Nächster Baustellentermin** als prominenter Folgetermin.
- **Gewerk-Liefertermine** in der Termine-Tabelle, falls relevant.

### 9. Ausgabe als DOCX + PDF schreiben & State aktualisieren

**Endformat**: DOCX + PDF. **Kein Markdown** im Projekt-Ordner.
Auf Windows 11 mit MS Word bootstrapt der Renderer fehlende Python-Pakete
selbst und exportiert die PDF via Word. Keine technischen Setup-Fragen an den
Nutzer.

Schritte:

1. Erzeuge das Protokoll als Markdown unter einem flüchtigen Pfad:
   `<temp-dir>/eba-protokoll-lp5-<jjjj-mm-tt>-<projekt>.md`. `<temp-dir>` ist
   das OS-Temp-Verzeichnis (`tempfile.gettempdir()`; `%TEMP%` auf Windows,
   `/tmp` auf Unix), nicht fest `/tmp`. Die Vorbemerkungs-Box bleibt wortgleich
   (mit **5 Kalendertagen**).

2. Rufe den Renderer auf:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
     "<temp-dir>/eba-protokoll-lp5-<datum>-<projekt>.md" \
     --format protokoll-lp5 \
     --out-dir "protokolle/<projekt>/"
   ```

3. Der Renderer schreibt
   `protokolle/<projekt>/eba-protokoll-lp5-<datum>-<projekt>.docx` plus
   die zugehörige PDF und löscht das MD-Zwischenformat. Wenn der Renderer einen
   Windows-PDF-Fehler meldet, stderr lesen, denselben Befehl nach der
   automatischen Selbstheilung erneut versuchen und erst danach echte Blocker
   melden.

Wenn kein Projektordner ableitbar ist, `protokolle/000-RAW/` verwenden.

**EBA-Dateinamen-Konvention**: siehe
`${CLAUDE_PLUGIN_ROOT}/references/categories/dateinamen-konvention.md`. Schema:
`<PrjNr>-<PrjKZ>-EBA-BL-PK-<JJMMTT>` (ohne Endung; Renderer hängt
`.docx`/`.pdf` an), z.B. `541-MAR-EBA-BL-PK-260415.docx`.

Volle Pipeline-Beschreibung:
`${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

State-File: `protokolle/<projekt>/protokoll-state.json` mit zusätzlichen LP5-Feldern:

- `letzte_mangelnummer`: für die fortlaufende Mangelnummerierung.
- `bemusterungen`: Liste der bisherigen Bemusterungspunkte.

### 10. Zusammenfassung an den Nutzer

Wie LP1-4. Zusätzlich:

- Anzahl neu eröffneter Mängel.
- Anzahl als erledigt markierter Mängel.
- Nächster Baustellentermin.

## Anti-Pattern

- ❌ Reine BIM-Koordination (`BIM-PK-JF`, `BIM-Jour-Fixe`, IFC/BCF/BIMcollab/CDE,
  Datendrop, BAP, LOIN) als LP5 behandeln — dafür die LP1-4-BIM-Variante verwenden,
  außer der Nutzer verlangt ausdrücklich LP5.
- ❌ Mängelpunkte ohne Mangelnummer notieren — sie müssen über die Projektdauer
  eindeutig referenzierbar sein.
- ❌ Witterung weglassen, wenn sie auf der Baustelle relevant war (z.B. wegen
  unterbrochener Außenarbeiten).
- ❌ LP1-4-Kategorienschema verwenden — LP5 hat sein eigenes Schema mit
  baustellenspezifischen Kategorien.
- ❌ Bemusterung in „Information" stecken — sie sind Entscheidungsdokumente und
  müssen mit Status `E` (erledigt = Bemusterung erfolgt) erfasst werden.

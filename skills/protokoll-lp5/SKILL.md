---
name: protokoll-lp5
description: Use when the user asks for a "Protokoll LP5", "Bauleitungsprotokoll", "Baubesprechung", "Baustelle", "Mängelprotokoll", "Bemusterungsprotokoll", or has a transcript from a construction-phase meeting (LP5 Ausführungsplanung / LP8 Objektüberwachung). Produces the EBA QMG-024-141 ORG-PK-LP5 tracking protocol with construction-specific D/K categories (Mängel, Bemusterung, Bauablauf, …).
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
- Restliche Header-Felder: wie LP1-4.

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

### 9. Ausgabe & State

Speicherort:
`protokolle/<projekt>/<jjjj-mm-tt>_protokoll-lp5-<NN>_<thema>.md`.

State-File: `protokolle/<projekt>/protokoll-state.json` mit zusätzlichen LP5-Feldern:

- `letzte_mangelnummer`: für die fortlaufende Mangelnummerierung.
- `bemusterungen`: Liste der bisherigen Bemusterungspunkte.

### 10. Zusammenfassung an den Nutzer

Wie LP1-4. Zusätzlich:

- Anzahl neu eröffneter Mängel.
- Anzahl als erledigt markierter Mängel.
- Nächster Baustellentermin.

## Anti-Pattern

- ❌ Mängelpunkte ohne Mangelnummer notieren — sie müssen über die Projektdauer
  eindeutig referenzierbar sein.
- ❌ Witterung weglassen, wenn sie auf der Baustelle relevant war (z.B. wegen
  unterbrochener Außenarbeiten).
- ❌ LP1-4-Kategorienschema verwenden — LP5 hat sein eigenes Schema mit
  baustellenspezifischen Kategorien.
- ❌ Bemusterung in „Information" stecken — sie sind Entscheidungsdokumente und
  müssen mit Status `E` (erledigt = Bemusterung erfolgt) erfasst werden.

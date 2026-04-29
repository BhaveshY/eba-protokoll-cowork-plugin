# Disziplin-/Kategorie-Schema (D/K)

Quelle: real verwendete Protokolle der Eike Becker_Architekten (Projekt 553-WIL,
Projekt 549-VTS), abgeglichen mit der EBA-Excel-Vorlage `QMG-024-141 ORG-PK-EXCEL-MA`.

Die D/K-Spalte ist projektspezifisch — sie wird zu Projektbeginn festgelegt und dann
über alle Besprechungen hinweg beibehalten. Wenn eine zuvor unbekannte Kategorie
auftritt, muss sie projektweit ergänzt werden, **nicht** nur in einem einzelnen Protokoll.

## Standard-Schema (Planungsbesprechung LP1-4 / Hochbau)

| D/K | Kategorie |
|-----|-----------|
| 01  | Organisation |
| 02  | Termine |
| 03  | Planungsvorgaben / Entscheidungen |
| 04  | Kosten |
| 05  | Flächen |
| 06  | Objektplanung |
| 07  | Tragwerksplanung |
| 08  | TGA |
| 09  | Brandschutz |
| 10  | Freianlagen |

## BIM-Koordinations-Schema

| D/K | Kategorie |
|-----|-----------|
| 1   | Organisation |
| 2   | Termine |
| 3   | Modellierungsvorgaben / Entscheidungen |
| 4   | Modell Allgemein |
| 5   | Objektplanung (ARC) |
| 6   | Tragwerksplanung (TWP) |
| 7   | TGA |
| 8   | Sonstiges |

## Bauleitungs-Schema (LP5 / Ausführung)

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

## Schema-Erkennung aus dem Transkript

Anhand des Transkriptinhalts lässt sich abschätzen, welches Schema passt:

- Fallen Begriffe wie „IFC", „BCF", „ViCADo", „BIMcollab", „LP3", „Modell" → BIM-Schema.
- Fallen Begriffe wie „Bauantrag", „LPH 4", „Genehmigungsplanung", „Vorentwurf" → LP1-4-Schema.
- Fallen Begriffe wie „Baustelle", „Mangel", „Bemusterung", „Abnahme", „Rohbau-Fortschritt",
  „Baufortschritt", „Witterung" → LP5-Schema.

Bei Unsicherheit → nur nachfragen, wenn LP1-4 vs. LP5 strukturell wirklich
unentscheidbar ist. Fehlende Projektmetadaten sind kein Grund zur Rückfrage;
dann die Fallbacks aus `metadaten-konvention.md` verwenden. Wenn kein
Baustellen-/LP5-Anker vorliegt, das LP1-4-Schema (Standard) verwenden.

## Erweiterung um projektspezifische Kategorien

Manche Projekte haben Sonder-Kategorien (z.B. „13 Nachhaltigkeit / DGNB", „14 Akustik",
„15 Sicherheit & Gesundheit"). Wenn das Transkript klar auf eine solche Sonder-Kategorie
zeigt und sie noch nicht im Schema ist, **die Kategorie als nächste freie Nummer aufnehmen**
und in der Datei `protokoll-state.json` (siehe `scripts/protokoll-state.md`) ergänzen,
damit sie in allen Folgeprotokollen erhalten bleibt.

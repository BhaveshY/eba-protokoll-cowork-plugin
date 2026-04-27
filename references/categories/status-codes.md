# Status- und Teilnahme-Codes

## Themen-Status (Spalte „Status")

| Code  | Bedeutung   | Wann verwenden |
|-------|-------------|----------------|
| `O`   | offen       | Aufgabe steht aus, niemand hat sie abschließend bearbeitet. Default für neue Themen, die eine Aktion erfordern. |
| `E`   | erledigt    | Aufgabe abgeschlossen oder Beschluss gefasst. |
| `Info`| Information | Reiner Informationspunkt — keine Aktion nötig. Wird auch genutzt für Termin-Ankündigungen, Hinweise, Kommunikationsstand. |

Optional in der Excel-Variante:
- Spalte `ausblenden = x`: Erledigte Punkte werden in Folgeversendungen ausgeblendet, bleiben aber im Master enthalten.

## Teilnahme (Spalte „Teilnahme" in Teilnehmertabelle)

| Code  | Bedeutung |
|-------|-----------|
| `X`   | teilgenommen (vor Ort) |
| `(X)` | zeitweise teilgenommen |
| `O`   | online teilgenommen |
| `N`   | nicht teilgenommen |
| `E`   | entschuldigt |

## Verteiler (Spalte „Verteiler")

| Code  | Bedeutung |
|-------|-----------|
| `X`   | im Verteiler |
| (leer) / `–` | nicht im Verteiler |

Üblicherweise stehen alle Teilnehmer **plus** zusätzlich projektrelevante Personen im
Verteiler. Im Header der Verteiler-Tabelle steht oft „Wie Teilnehmer und zusätzlich".

## Termin-Notation (Spalte „Termin")

| Notation     | Bedeutung |
|--------------|-----------|
| `TT.MM.JJ`   | Konkretes Datum (z.B. `27.03.26`) |
| `KW NN`      | Kalenderwoche (z.B. `KW 13`) |
| `–` oder `-` | Kein Termin / nicht relevant |
| (leer)       | wie `–` |

**Wichtig**: Termine niemals als „nächste Woche" / „bald" / „demnächst" — immer in
absolute Daten umrechnen anhand des Besprechungsdatums. Zum Beispiel:

- Besprechung am 24.03.2026, Aussage „bis nächsten Freitag" → Termin = `27.03.26`.
- Besprechung am 24.03.2026, Aussage „bis Ende des Monats" → Termin = `31.03.26`.
- Besprechung am 24.03.2026, Aussage „in zwei Wochen" → Termin = `07.04.26` oder
  `KW 15` (je nach Genauigkeit der Aussage).

## Ergänzungen (LN-Suffix `E`)

Wenn ein Punkt aus einer früheren Besprechung in einer Folgebesprechung wieder
aufgegriffen wird:

| Original (Besprechung 7) | Ergänzung (Besprechung 8) |
|---------------------------|----------------------------|
| `D/K=03, B=07, LN=02` … Status `O` | `D/K=03, B=08, LN=02E`, Beschreibung beginnt mit `#08:` … Status `O` oder `E` |

Die LN bleibt mit `E`-Suffix erhalten — so lassen sich Original und Ergänzungen
beim Sortieren zusammenhalten. In der Ausgabe erscheinen alle Ergänzungen direkt
unterhalb des Original-Eintrags.

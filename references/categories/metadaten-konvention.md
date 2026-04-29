# Metadaten-Konvention für rohe Transkripte

Die EBA Protokoll App liefert in der Praxis oft **rohe Transkripte** ohne
vollständigen Header. Das Plugin darf die Protokollerstellung deshalb nicht
blockieren, nur weil Projekt-Nr., Projektname, Ort, Ersteller oder Datum fehlen.

Grundsatz: **erst erzeugen, dann transparent Annahmen nennen**. Fehlende
Metadaten sind Warnungen für die Zusammenfassung, keine Abbruchgründe.

## Fallback-Werte

| Feld | Fallback |
|------|----------|
| Projekt-Nr. / Projekt-Nummer | `000` |
| Projekt-Name / Projektname | Aus Dateiname, Transkript-Titel oder erstem Thema ableiten; sonst `EBA / Allgemein` |
| Projekt-Beschreibung | Kurze Ableitung aus Thema; sonst `Aus rohem Transkript abgeleitet` |
| Projektordner | `protokolle/000-RAW/` oder, wenn ein Name ableitbar ist, `protokolle/000-<kuerzel>/` |
| Ort | Aus Transkript ableiten; sonst `nicht angegeben` |
| Gesprächsdatum / Datum | Aus Dateiname oder Transkript ableiten; sonst heutiges Datum |
| Ersteller | Aus Sprecher ableiten; sonst `EBA` |
| Ersteller-Datum | heutiges Datum |
| Teilnehmername | Sprecherlabel verwenden, wenn Name nicht auflösbar ist |
| Firmen-Kürzel | aus Kontext ableiten; sonst leer lassen oder `EBA` bei EBA-Sprecher |

`000` bedeutet: **kein Projekt im Transkript eindeutig erkennbar**. Es ist ein
bewusster Platzhalter und darf vom Validator nicht als Fehler behandelt werden.

## Wann nachfragen?

Nur nachfragen, wenn die Antwort die Struktur wesentlich ändert:

- LP1-4 vs. LP5 ist wirklich unklar und beide wären plausibel.
- Der Nutzer verlangt ausdrücklich eine fortgeschriebene Besprechung, aber es
  gibt weder State-Datei noch Vorprotokoll.
- Ein rechtlich/vertraglich relevanter Beschluss ist ohne Zuständigkeit nicht
  sicher zuordenbar.

Nicht nachfragen bei:

- fehlender Projekt-Nr.,
- fehlendem Projekt-Namen,
- fehlendem Ort,
- unbekanntem Ersteller-Kürzel,
- generischen Sprecherlabels.

Diese Punkte mit Fallbacks füllen und am Ende als Annahmen nennen.

## Formatwahl bei rohen Transkripten

- Kein Meeting-Anker, kurzer Austausch, wenig Struktur → `gespraechsnotiz`.
- Kein Meeting-Anker, aber mehrere Sprecher und Aufgaben/Fristen → `protokoll-einfach`.
- Klarer Planungs-/Jour-Fixe-/BIM-/Baustellen-Anker → entsprechendes Trackingformat.
- EBA-Interview/Presse/Medien ohne Projekt → `gespraechsnotiz` mit `Projekt-Nummer = 000`.

## Zusammenfassung an den Nutzer

Die finale Antwort soll keine technischen oder blockierenden Fragen enthalten.
Stattdessen:

- Pfade zu DOCX und PDF nennen.
- Format nennen.
- Annahmen knapp auflisten, z.B.:
  `Annahmen: Projekt-Nr. 000, Ort nicht angegeben, Ersteller EBA.`
- Optional sagen, dass diese Felder später in Word angepasst werden können.

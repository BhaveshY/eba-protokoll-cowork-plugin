# Vorlage: Protokoll LP1-4 (Planungsphase)

QM-Index: `QMG-024-141 ORG-PK-LP1-4-MA` (Stand A, 27.02.23) sowie
`QMG-024-141 ORG-PK-LP1-4-EXCEL-MA` (Stand A, 20.09.24).

Verwendung: Planungsbesprechungen in den Leistungsphasen 1–4 (Grundlagenermittlung,
Vorplanung, Entwurfsplanung, Genehmigungsplanung). Inkl. Kick-Off, Workshops,
Jour-Fixe, BIM-Koordination, DGNB-Abstimmungen.

Wichtigstes Merkmal: **Fortgeschriebenes Tracking** — offene Themen aus früheren
Besprechungen werden in jedem neuen Protokoll mit ihrer Historie weitergeführt
(Ergänzungen werden mit `E` am Suffix der LN markiert).

---

```markdown
# Protokoll
## zur Besprechung Nr. <NN>
### <Besprechungsthema>

| Projekt-Nr.  | <Prj.-Nr.>   |
|--------------|--------------|
| Projekt-Name | <Prj.-Name>  |

| Ort  | <Ort / Online / Präsenz> |
|------|--------------------------|
| Datum | <TT.MM.JJJJ>            |
| Zeit | <0.00 – 0.00 Uhr>        |

> **Vorbemerkung** Wir bitten alle im Verteiler Benannten, den Inhalt dieses Protokolls
> zu prüfen und dem Ersteller mögliche Änderungen und/oder Ergänzungen mitzuteilen.
> Werden innerhalb von 5 Kalendertagen keine Änderungen und/oder Ergänzungen angezeigt,
> gilt der Protokollinhalt als anerkannt und zur weiteren Planung und Umsetzung freigegeben.

## Teilnehmer

| Vorname | Name | KZ | Firma | KZ | Teilnahme | Verteiler |
|---------|------|----|-------|----|-----------|-----------|
| <Vorname> | <Name> | <KZ> | <Firma> | <Firma-KZ> | X | X |

> X = teilgenommen, (X) = zeitweise teilgenommen, O = online teilgenommen,
> N = nicht teilgenommen, E = entschuldigt

## Besprochene Unterlagen

| Dokument/e, Plan/Pläne | Datum | V/I | von | an |
|------------------------|-------|-----|-----|-----|
| <Doc>                  | <TT.MM.JJJJ> | <V/I> | <von> | <an> |

> V = Version, I = Index

## Besprechungsthemen

> D/K = Disziplin oder Kategorie · B = Nr. der Besprechung ·
> LN = Laufende Nummer bezogen auf die Besprechung · E = Ergänzung zum Vorpunkt
> Status: O = offen · E = erledigt · Info = Information

| D/K | B | LN | Besprechungsthemen | zuständig | Termin | Status |
|-----|---|-----|--------------------|-----------|--------|--------|
| 01  | – | –   | **Organisation**   |           |        |        |
| 01  | <NN> | <LN> | <Beschreibung des Themas / Beschluss / Aufgabe> | <KZ / Firma-KZ> | <TT.MM.JJ oder KW NN oder ->| O / E / Info |
| 01  | <NN> | <LN>E | <Ergänzung aus späterer Besprechung — beginnend mit `#NN:` als Verweis> | <KZ> | <Termin> | <Status> |
| 02  | – | –   | **Termine**        |           |        |        |
| …   | … | …   | …                  | …         | …      | …      |

## Termine (Folgetermine)

| Thema der Besprechung | Teilnehmer | Ort | Datum | Zeit |
|-----------------------|------------|-----|-------|------|
| <Thema>               | <Namen>    | <Ort> | <TT.MM.JJ> | <0.00–0.00> |

## Aufstellvermerk zum Dokument

| Rolle    | Name / Kürzel        | Datum       |
|----------|----------------------|-------------|
| Ersteller | <Name oder Kürzel> | <TT.MM.JJ>  |
| Geprüft   | <Name oder Kürzel> | <TT.MM.JJ>  |

## Nachträgliche Anmerkungen zum Dokument

| Ersteller | Erstell-/Änderungsdatum | Anmerkung                          |
|-----------|-------------------------|------------------------------------|
| ---       | ---                     | ---                                |

## Anlagen

| Dokument/e, Plan/Pläne | V/I | Datum | Format |
|------------------------|-----|-------|--------|
| <Anlage>               | <V> | <TT.MM.JJ> | <PDF / DWG / IFC / …> |

## Kennzeichnungen im Dokument

> Die Themen/Inhalte erhalten zur besseren Nachvollziehbarkeit je Status eine
> entsprechende Kennzeichnung.

| Termin Status            | Farbe              | Bemerkung                                        |
|--------------------------|--------------------|--------------------------------------------------|
| aktuell/fortgeschrieben  | _Kennzeichnung_    | ab Protokoll 2, ausgenommen Versendung Nr. 1     |
| aktuell/angemerkt        | _Kennzeichnung_    | Anmerkungen nach erster Versendung/Wiederversendung |
| überschritten            | _Kennzeichnung_    | offene überfällige Termine                       |
| erledigt                 | _Kennzeichnung_    | erledigte Themen (einmalig)                      |
```

Wenn Projekt-Nr., Projekt-Name, Ort, Datum oder Ersteller im Rohtranskript fehlen,
die Fallbacks aus `references/categories/metadaten-konvention.md` verwenden.
`Projekt-Nr. = 000` ist dabei ein bewusster Platzhalter und kein Validator-Fehler.

## Disziplin-/Kategorie-Konvention (D/K)

Standard-Kategorien (projektabhängig erweiterbar — siehe `references/categories/`):

| D/K | Bedeutung |
|-----|-----------|
| 01  | Organisation |
| 02  | Termine |
| 03  | Planungsvorgaben / Entscheidungen / Modellierungsvorgaben |
| 04  | Kosten / Modell Allgemein |
| 05  | Flächen / Objektplanung (ARC) |
| 06  | Objektplanung / Tragwerksplanung (TWP) |
| 07  | Tragwerksplanung |
| 08  | TGA |
| 09  | Brandschutz |
| 10  | Freianlagen |

Wenn ein BIM-Koordinations-JF protokolliert wird, gilt die BIM-Variante:

| D/K | Bedeutung |
|-----|-----------|
| 1   | Organisation |
| 2   | Termine |
| 3   | Modellierungsvorgaben / Entscheidungen |
| 4   | Modell Allgemein |
| 5   | Objektplanung (ARC) |
| 6   | Tragwerksplanung (TWP) |
| 7   | TGA |
| 8   | Fassade / Sonstiges |

## LN-Konvention (Laufende Nummer)

- **Erstmaliger Eintrag** in Besprechung B=07: `LN = 01` (oder die nächste freie Nummer
  innerhalb der D/K-Kategorie für diese Besprechung).
- **Ergänzung in Folgebesprechung** B=08 zum Vorpunkt `LN=01` aus B=07: Eintrag mit
  `LN = 01E` und Beschreibung beginnend mit `#08:` als Versionsmarker.
- Je weitere Ergänzung: weiter in der Besprechungsspalte hochzählen, LN behält das `E`-Suffix.
- **Erledigt = E im Status** entfernt den Punkt nicht — er bleibt im Protokoll mit Status `E`.
  Bei der nächsten Versendung kann er optional ausgeblendet werden (in Excel via Spalte
  `ausblenden = x`).

## Termin-Format

- Konkretes Datum: `TT.MM.JJ` (z.B. `27.03.26`).
- Kalenderwoche: `KW NN` (z.B. `KW 13`).
- Information ohne Termin: `-` oder `Info`.

## Zuständigkeit

Eine oder mehrere **Firmen-Kürzel** (z.B. `EBA`, `WB`, `ZÜB`, `LHT`, `DES`, `AMA`, `A8`),
optional gefolgt von Personen-Kürzeln (z.B. `EBA RvG`). Bei mehreren Verantwortlichen
durch Leerzeichen getrennt: `EBA WB ZÜB`.

Sonderwerte:
- `Alle` — alle Teilnehmer sind zuständig.
- `Info` — reiner Informationspunkt, niemand muss handeln.

## Sprache & Stil

- Vollständig auf Deutsch.
- Sachlich, professionell, in der dritten Person passiv oder mit Firmenkürzel als Subjekt
  (z.B. „EBA weist darauf hin, dass …", „ZÜB übernimmt die Abstimmung mit …").
- **Keine wörtlichen Zitate** aus dem Transkript — immer prägnant zusammenfassen.
- Implizite Aufgaben erkennen: „Ich schicke das morgen" → Aufgabe für den Sprecher mit
  Termin „morgen" (in absolutes Datum umrechnen anhand des Besprechungsdatums).

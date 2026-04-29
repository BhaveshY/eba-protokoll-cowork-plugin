# Vorlage: Protokoll LP5 (Bauleitung)

QM-Index: `QMG-024-141 ORG-PK-LP5-MA` (Stand B, 02.02.23).

Verwendung: Baubesprechungen in Leistungsphase 5 (Ausführungsplanung) und der
Objektüberwachung. Inhaltlich identisch strukturiert zum LP1-4-Tracking-Protokoll,
aber mit baustellenspezifischen Kategorien und einem zusätzlichen Block für
übergebene Pläne / Anlagen.

Wichtigstes Merkmal: **Fortgeschriebenes Tracking** — siehe
[`protokoll-lp1-4.md`](protokoll-lp1-4.md) für die LN/Ergänzungs-Konvention.

---

```markdown
# Protokoll
## zur Besprechung Nr. <NN>
### <Besprechungsthema>

| Projekt-Nr.  | <Prj.-Nr.>  |
|--------------|-------------|
| Projekt-Name | <Prj.-Name> |

| Ort  | <Ort> |
|------|-------|
| Datum | <TT.MM.JJ> |
| Zeit | <0.00 – 0.00 Uhr> |

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
| <Doc>                  | <TT.MM.JJ> | <V/I> | <von> | <an> |

> V = Version, I = Index

## Besprechungsthemen

> D/K = Disziplin oder Kategorie · B = Nr. der Besprechung ·
> LN = Laufende Nummer bezogen auf die Besprechung · E = Ergänzung zum Vorpunkt
> Status: O = offen · E = erledigt

| D/K | B | LN | Besprechungsthemen | zuständig | Termin | Status |
|-----|---|-----|--------------------|-----------|--------|--------|
| 01  | – | –   | **Organisation / Baustelle** |         |        |       |
| 01  | <NN> | <LN> | <Beschreibung> | <KZ> | <TT.MM.JJ> | O / E |
| 02  | – | –   | **Termine**     |        |        |       |
| 03  | – | –   | **Bauablauf / Logistik** | | | |
| 04  | – | –   | **Kosten / Nachträge** | | | |
| 05  | – | –   | **Mängel / Abnahmen** | | | |

## Termine

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
| <Anlage>               | <V> | <TT.MM.JJ> | <PDF / DWG / IFC> |

## Kennzeichnungen im Dokument

> Die Themen/Inhalte erhalten zur besseren Nachvollziehbarkeit je Status eine
> entsprechende Kennzeichnung.

| Termin Status              | Farbe              | Bemerkung                                        |
|----------------------------|--------------------|--------------------------------------------------|
| aktuell/fortgeschrieben    | _Kennzeichnung_    | ab Protokoll 2, ausgenommen Versendung Nr. 1     |
| aktuell/angemerkt          | _Kennzeichnung_    | Anmerkungen nach erster Versendung/Wiederversendung |
| überschritten              | _Kennzeichnung_    | offene überfällige Termine                       |
| erledigt                   | _Kennzeichnung_    | erledigte Themen (einmalig)                      |
```

Wenn Projekt-Nr., Projekt-Name, Ort, Datum oder Ersteller im Rohtranskript fehlen,
die Fallbacks aus `references/categories/metadaten-konvention.md` verwenden.
`Projekt-Nr. = 000` ist dabei ein bewusster Platzhalter und kein Validator-Fehler.

## LP5-spezifische Kategorien

Vorschlag für die D/K-Kategorien in LP5 (projektabhängig anpassbar):

| D/K | Bedeutung |
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

Diese Kategorien gelten zusätzlich zu den LP1-4-Kategorien. In Ausführungsphase werden
oft auch noch **Mängelpunkte** und **Bemusterungspunkte** als eigene Kategorien geführt.

## Zusätzliche LP5-Konventionen

- **Überschrittene Termine** werden mit Status `O` (offen) und in der Excel-Variante
  mit Schattierung markiert (Farbe `soft = FFE0CC`).
- **Mängel** erhalten oft eine zusätzliche Spalte „Mangelnummer" und einen separaten
  Mängelblock am Ende des Protokolls.
- **Bemusterungen** werden mit Foto-/Anlagen-Verweis dokumentiert.
- Bei Baustellenbegehungen wird die **Witterung** im Header oder in der Vorbemerkung
  erwähnt (z.B. „Witterung: trocken, 8 °C").

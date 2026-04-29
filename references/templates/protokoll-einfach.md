# Vorlage: Protokoll (einfach, Word LP1-4 Stand A)

QM-Index: `QMG-024-141 ORG-PK-LP1-4-MA` (Stand A, 27.02.23) — Word-Variante.
Die separate Excel-Variante `QMG-024-141 ORG-PK-LP1-4-EXCEL-MA` (Stand A,
20.09.24) wird nur bei ausdrücklichem Excel-Wunsch verwendet.

Verwendung: Einfache Planungsbesprechung **ohne** D/K|B|LN-Tracking.
Zwischen-Format zwischen Gesprächsnotiz (formlos, ohne Frist) und LP1-4-Tracking
(D/K|B|LN, Status, Fortschreibung). Dieses Format hat:

- Hierarchisch nummerierte Themen (`Thema 01`, `01.1`, `01.2`, `02`, …).
- Eine Spalte „Zuständig / Frist" — also eine kombinierte Verantwortlichkeits-/
  Termin-Spalte, kein Status, kein D/K, kein B, keine LN.
- Frist von 3 Kalendertagen für Rückmeldung der Verteilerempfänger
  (NICHT 5 Tage wie beim Tracking-Protokoll).

Wird typischerweise verwendet für:

- Kick-Off-Meetings, in denen noch keine Aufgaben in das D/K-Schema gehören.
- Workshops mit definiertem Endpunkt (kein Folgetermin).
- Mittlere Besprechungen (mehr als Gesprächsnotiz, weniger als JF mit Tracking).

---

```markdown
# Protokoll

_<kurze Beschreibung zum Dokument / Übergeordnetes Thema>_

| Projektname        | <Projektname>                                                |
|--------------------|--------------------------------------------------------------|
| Projekt-Nummer     | <Projektnummer>                                              |
| Projekt-Beschreibung | <Projektbeschreibung>                                      |

| Ort   | Gesprächsdatum | Erstelldatum | Ersteller |
|-------|----------------|--------------|-----------|
| <Ort> | <TT.MM.JJ>     | <TT.MM.JJ>   | <Kürzel>  |

> **Hinweis** Wir bitten alle im Verteiler Benannten, den Inhalt dieses Protokolls zu prüfen
> und dem Ersteller mögliche Änderungen und/oder Ergänzungen mitzuteilen. Werden
> innerhalb von 3 Kalendertagen keine Änderungen und/oder Ergänzungen angezeigt, gilt
> der Protokollinhalt als anerkannt und zur weiteren Planung und Umsetzung freigegeben.

## Teilnehmer

| Vorname | Name | Kürzel | Firma |
|---------|------|--------|-------|
| <Vorname> | <Name> | <KZ> | <Firma> |

## Verteiler

> Wie Teilnehmer und zusätzlich

| Vorname | Name | Firma |
|---------|------|-------|
| <Vorname> | <Name> | <Firma> |

## Gesprächsinhalt

| Thema | Beschreibung | Zuständig / Frist |
|-------|--------------|-------------------|
| Thema 01 | <Beschreibung> | <KZ> / <TT.MM.JJ> |
| Thema 01.1 | <Detail / Unterpunkt> | <KZ> / <TT.MM.JJ> |
| Thema 02 | <Beschreibung> | <KZ> / – |

---

_Diese Notiz wurde mit der EBA Protokoll App + eba-protokoll-cowork erstellt._
```

## Regeln

1. Die Hinweis-Box bleibt **wortgleich** — und enthält **3 Kalendertage**, nicht 5.
2. `Projekt-Nummer` ist die EBA-interne Projektnummer (z.B. `549`, `553`).
   Bei rohen Transkripten ohne erkennbare Projektnummer ist `000` der zulässige
   Fallback.
3. `Ersteller` ist das **Kürzel** des Protokollerstellers, nicht der volle Name.
4. `Kürzel` für Teilnehmer sind 2–3-stellige Initialen (z.B. `EB`, `RvG`, `SK`).
5. Themen sind hierarchisch nummeriert: `Thema 01`, `Thema 01.1`, `Thema 01.2`, `Thema 02`, …
6. Spalte **Zuständig / Frist** ist kombiniert: `<Kürzel> / <TT.MM.JJ>` oder
   `<Kürzel> / KW NN` oder `<Kürzel> / –` bei reinen Informationspunkten.
7. **Keine Status-Spalte**, **kein D/K-Schema**, **keine LN** — wenn diese
   benötigt werden, ist das Format `protokoll-lp1-4` richtig.

## Abgrenzung zu anderen Formaten

| Format | Hinweis-Frist | Themen-Nummerierung | Frist-Spalte | Status | Fortschreibung |
|--------|---------------|---------------------|--------------|--------|----------------|
| `gespraechsnotiz` | 3 Tage | `Thema 01.1` | nein | nein | nein |
| `protokoll-einfach` | 3 Tage | `Thema 01.1` | ja (kombiniert) | nein | nein |
| `protokoll-lp1-4`  | 5 Tage | `D/K|B|LN` | ja (Termin) | ja (O/E/Info) | ja |
| `protokoll-lp5`    | 5 Tage | `D/K|B|LN` | ja (Termin) | ja (O/E) | ja + Mängel |

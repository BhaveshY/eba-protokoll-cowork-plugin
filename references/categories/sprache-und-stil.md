# Sprache und Stil von EBA-Protokollen

## Grundregeln

1. **Vollständig auf Deutsch** — auch bei englischen Passagen im Transkript wird das
   fertige Protokoll auf Deutsch geschrieben (Eigennamen und Produktnamen ausgenommen).
2. **Sachliche, professionelle Sprache** — keine umgangssprachlichen Formulierungen,
   keine Füllwörter wie „eigentlich", „halt", „so".
3. **Keine wörtlichen Zitate** — Beiträge werden zusammengefasst, nicht abgeschrieben.
4. **Sie-Form** in Anreden, falls überhaupt nötig (selten — Protokolle sind in dritter Person).
5. **Aktive Stimme mit Firmenkürzel als Subjekt** ist üblich:
   - „EBA weist darauf hin, dass …"
   - „ZÜB übernimmt die Abstimmung mit …"
   - „LHT lädt die Unterlagen bis 25.03.26 hoch."
6. Alternativ Passiv-Konstruktion mit Verantwortlichkeit hinten:
   - „Der Bauantrag wird auf Grundlage der aktuellen Planung eingereicht. (EBA)"

## Stilbeispiele aus echten EBA-Protokollen

### Schlechter Stil (nicht so)

> „Also, Herr Regener hat halt gesagt, dass er das vielleicht bis Freitag machen wird,
> aber er ist sich nicht ganz sicher."

### Guter Stil

> „WB beauftragt die Vermessung und stellt den aktuellen Lageplan zur Verfügung. Die
> Angaben sollen zum nächsten Jour Fixe vorliegen."
> _zuständig: WB_, _Termin: KW 44_, _Status: E_

### Schlechter Stil

> „Die Lüftung im Innenhof ist noch nicht ganz klar. Wir müssen da nochmal drüber reden."

### Guter Stil

> „Am 26.03.2026 wird eine Besprechung bezüglich der Lüftung im Innenhof stattfinden."
> _zuständig: WB LHT A8 DES EBA_, _Termin: 26.03.26_, _Status: E_

## Erkennen impliziter Aufgaben

„Ich schicke Ihnen das morgen" → Aufgabe für den Sprecher mit Termin „morgen" (umrechnen
in absolutes Datum).

„Wir sollten mal …" → bei Konsens im Transkript: konkrete Aufgabe ableiten und einem
Verantwortlichen zuordnen. Bei unklarer Verantwortlichkeit: Protokollersteller mit
„(klären)" markieren oder im Status `O` bleiben mit Beschreibung „… ist zu klären".

„Können Sie das bitte machen?" + bestätigende Antwort → Aufgabe an die angesprochene
Person mit dem im Gespräch genannten Termin.

## Termine in absolute Daten umrechnen

Anhand des Besprechungsdatums (steht im Transkript-Header oder im Dateinamen):

| Im Transkript        | Im Protokoll (Besprechung am 24.03.2026) |
|----------------------|------------------------------------------|
| „nächste Woche"      | `KW 14` oder `31.03.26`                  |
| „Ende der Woche"     | `28.03.26` (Freitag)                     |
| „in 14 Tagen"        | `07.04.26` oder `KW 15`                  |
| „Anfang Mai"         | `KW 18` oder `04.05.26`                  |
| „Mitte April"        | `KW 16` oder `15.04.26`                  |
| „nach Ostern"        | konkretes Datum aus Kalender (2026: `07.04.26`) |
| „heute"              | `24.03.26`                               |
| „morgen"             | `25.03.26`                               |
| „bis nächsten Freitag" | `27.03.26`                              |

Wenn der Sprecher einen ungenauen Zeitraum nennt („in den nächsten Wochen", „bald",
„demnächst"), Termin als `–` markieren und im Status `O` lassen — das Protokoll fordert
in der nächsten Besprechung eine Konkretisierung.

## Strukturierung der Themen-Beschreibung

Eine gute Beschreibungszeile in der Themen-Tabelle ist:

- **Selbsterklärend**: aus der Zeile allein lässt sich verstehen, worum es geht — auch
  ohne Kontext der Besprechung.
- **Faktisch**: was wurde besprochen, beschlossen, entschieden — keine Absichtserklärungen
  ohne Aktion.
- **Kompakt**: 1–4 Sätze, manchmal mit Aufzählungspunkten für mehrere Aspekte.
- **Mit Verantwortlichkeitsklarheit**: wer macht was bis wann.

### Beispiel einer guten Themen-Beschreibung

> EBA weist darauf hin, dass die Höhe OKFF EG auf +34,98 m üNHN festgelegt wurde.
> Benötigt wird ein DWG-Lageplan des Vermessers inklusive Georeferenzierung und Nullpunkt.
> Herr Regener beauftragt den aktuellen Vermesserlageplan und stellt diesen zur
> Verfügung. Die Angaben sollen zum nächsten Jour Fixe vorliegen.

`zuständig: WB`, `Termin: KW 44`, `Status: E`.

## Umgang mit unklaren Aussagen

Wenn das Transkript an einer Stelle unverständlich ist:

- Bei kurzen unverständlichen Abschnitten: weglassen.
- Bei wesentlichen unklaren Aussagen: Eintrag mit `[unklar – im Transkript bei
  HH:MM:SS]` versehen und Status `O` (zu klären).
- Bei widersprüchlichen Aussagen: beide Versionen in der Beschreibung erwähnen
  und Status `O` mit zuständig-Eintrag „(klären)".

# Format der `protokoll-state.json`

Pro Projekt eine Datei in `protokolle/<projekt>/protokoll-state.json`. Sie ist das
Gedächtnis zwischen Besprechungen und ermöglicht das Fortschreiben, ohne dass das
gesamte Vorprotokoll geparst werden muss.

## Schema

```jsonc
{
  // Schema-Version – falls sich das Format ändert
  "schema_version": 1,

  // Projekt-Identität
  "projekt": {
    "nr":   "553",
    "name": "WIL",
    "beschreibung": "Wilmersdorfer Straße — gemischtes Wohn- und Bürogebäude"
  },

  // Welche Vorlage wird benutzt? Beeinflusst das D/K-Schema.
  "typ": "lp1-4" | "lp5" | "bim",

  // Höchste bisher vergebene Besprechungsnummer (B).
  "letzte_besprechung_nr": 11,

  // Projekt-spezifisches D/K-Schema (kann vom Default abweichen).
  "dk_schema": [
    { "dk": "01", "name": "Organisation" },
    { "dk": "02", "name": "Termine" },
    { "dk": "03", "name": "Planungsvorgaben/Entscheidungen" },
    { "dk": "06", "name": "Objektplanung" },
    { "dk": "07", "name": "Tragwerksplanung" },
    { "dk": "08", "name": "TGA" },
    { "dk": "09", "name": "Brandschutz" },
    { "dk": "10", "name": "Freianlagen" }
  ],

  // Master-Verteiler — alle Personen, die alle Protokolle bekommen.
  "verteiler": [
    {
      "vorname": "Helge", "name": "Schmidt",
      "kz": "HS",
      "firma": "Eike Becker_Architekten", "firma_kz": "EBA"
    },
    {
      "vorname": "Robert", "name": "von Gruenewaldt",
      "kz": "RvG",
      "firma": "Eike Becker_Architekten", "firma_kz": "EBA"
    }
  ],

  // Projekt-spezifische Firma-Kürzel-Map (Erweitert globale Map).
  "firma_kuerzel": {
    "EBA": "Eike Becker_Architekten",
    "WB":  "Wiwela Bau Projekt GmbH",
    "ZÜB": "Ed. Züblin AG",
    "LHT": "LHT Bauingenieure GmbH",
    "DES": "DES GmbH",
    "AMA": "AMA Brandschutz",
    "G4W": "G4W GmbH",
    "A8":  "Atelier 8"
  },

  // Offene Punkte zur Übernahme ins nächste Protokoll.
  "offene_punkte": [
    {
      "dk": "06",
      "b":  "10",
      "ln": "01",
      "beschreibung": "EBA weist darauf hin, dass der aktuelle Stand zur Prüfung durch den BH hochgeladen wurde und die Unterlagen für den Bauantrag derzeit finalisiert werden.",
      "zustaendig": "EBA",
      "termin": "KW 13",
      "status": "O",
      "historie": [
        { "b": "10", "kommentar": "ursprünglich eröffnet" }
      ]
    }
  ],

  // Nur bei LP5: für die durchlaufende Mangelnummerierung.
  "letzte_mangelnummer": 47,

  // Nur bei LP5: bisherige Bemusterungspunkte zur Referenz.
  "bemusterungen": [
    {
      "datum": "12.03.26",
      "thema": "Bodenbelag Treppenhäuser",
      "entscheidung": "Granitstein, Hersteller XY, Variante grau."
    }
  ],

  // Letztes erstelltes Protokoll (zum Cross-Check).
  "letztes_protokoll": "2026-03-24_protokoll-11_planungsbespr.md",

  // Wann zuletzt aktualisiert.
  "aktualisiert_am": "2026-03-24T15:32:18+01:00"
}
```

## Lesen / Schreiben

Skills und Subagents schreiben das State-File mit dem Write-Tool. Das ist `JSON`,
mit `indent=2` und Stable-Key-Order.

Bei Konflikten (z.B. wenn der Nutzer das State-File manuell editiert hat) gilt:

- **Manuelle Änderungen am State-File haben Vorrang** — nicht überschreiben, nur
  ergänzen.
- Wenn die Skill einen Eintrag ändert, den der Nutzer in der Zwischenzeit angepasst hat,
  einen Hinweis in den Output für den Nutzer aufnehmen: „Achtung: `offene_punkte[3]`
  wurde gegenüber dem letzten State manuell verändert."

## Lokation

Default: `protokolle/<projekt>/protokoll-state.json` relativ zum aktuellen Arbeits-
verzeichnis. Der `<projekt>`-Ordnername entspricht der Projekt-Kurzbezeichnung
(z.B. `553-WIL`, `549-VTS`).

## Versionierung

Das State-File sollte unter Git stehen (oder im Cloud-Sync), damit zwischen
Sessions nichts verloren geht. Empfehlung: das `protokolle/`-Verzeichnis ist Teil
des Projekt-Repos.

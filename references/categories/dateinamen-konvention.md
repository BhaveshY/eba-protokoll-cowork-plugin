# EBA-Dateinamen-Konvention für Protokolle

EBA-Protokolle folgen einer projektübergreifenden Dateinamenskonvention. Sie ist
in Echt-Projekten konsistent verwendet (siehe `references/examples/`-Dateien).

## Grundschema

```
<PrjNr>-<PrjKZ>-<FirmaKZ>[-<Bereich>]-<Typ>-<JJMMTT>[-<Suffix>].md
```

| Feld | Beschreibung | Beispiele |
|------|--------------|-----------|
| `<PrjNr>` | EBA-Projektnummer (3-stellig) | `553`, `549`, `541` |
| `<PrjKZ>` | Projekt-Kurzname (Großbuchstaben) | `WIL`, `VTS`, `MAR` |
| `<FirmaKZ>` | Firma-Kürzel des Erstellers (in der Regel `EBA`) | `EBA` |
| `<Bereich>` | _optional_, z.B. fachlicher Schwerpunkt | `BIM`, `TWP`, `BL` |
| `<Typ>` | Typ-Kürzel des Protokolls — siehe unten | `PK`, `PLB-PK`, `JF` |
| `<JJMMTT>` | Datum 2-stellig: Jahr, Monat, Tag | `260324` für 24.03.2026 |
| `<Suffix>` | _optional_, z.B. `g-KI` (geprüft / KI-erstellt), `v2`, `Entwurf` | `g-KI` |

## Typ-Kürzel

| Kürzel | Format | Beschreibung |
|--------|--------|--------------|
| `GN`   | Gesprächsnotiz | Kurze formlose Notiz (`gespraechsnotiz`) |
| `PK`   | Protokoll | Generelles Protokoll |
| `PLB-PK` | Planungsbesprechungs-Protokoll | LP1-4-Tracking-Protokoll (`protokoll-lp1-4`) |
| `BIM-PK-JF-NN` | BIM-Koordinations-Jour-Fixe Nr. NN | LP1-4-Tracking, BIM-Variante |
| `BL-PK` | Bauleitungs-Protokoll | LP5-Tracking-Protokoll (`protokoll-lp5`) |
| `WS-PK` | Workshop-Protokoll | Einfaches Protokoll (`protokoll-einfach`) |

## Beispiele aus echten EBA-Projekten

```
553-WIL-EBA-PLB-PK-260324.md           — Planungsbesprechung 24.03.26 (LP1-4)
553-WIL-EBA_BIM-PK-JF-07_260331-g-KI.md — BIM-Jour-Fixe 07, 31.03.26 (geprüft, KI)
549-VTS-EBA-PK-240112.md                — Generisches Protokoll 12.01.24
541-MAR-EBA-BL-PK-260415.md             — Bauleitungs-Protokoll 15.04.26 (LP5)
```

## Mapping zur Plugin-Skill

| Plugin-Skill | Default-Typ-Kürzel im Dateinamen |
|--------------|----------------------------------|
| `gespraechsnotiz`   | `GN` |
| `protokoll-einfach` | `WS-PK` (Workshop / einfach) |
| `protokoll-lp1-4`   | `PLB-PK` (Planungsbesprechung) |
| `protokoll-lp1-4` (BIM-Variante) | `BIM-PK-JF-NN` |
| `protokoll-lp5`     | `BL-PK` |

## Vereinfachte Variante (Default des Plugins)

Wenn der Nutzer keine EBA-Dateinamen-Konvention erzwingt, verwendet das Plugin
den lesbareren Markdown-Namen:

```
<JJJJ-MM-TT>_<projekt-kurzname>_<typ>.md
```

z.B.:
```
2026-03-24_WIL_planungsbesprechung-11.md
2026-03-31_WIL_bim-jf-07.md
```

Beide Namensschemata sind gültig. Das EBA-Schema ist die offizielle Konvention für
abgelegte Dokumente; das vereinfachte Schema ist für die schnelle Benutzung im
Plugin-Workflow gedacht.

## Verzeichnisstruktur

Innerhalb von `protokolle/<projekt>/` werden alle Protokolle eines Projekts
abgelegt:

```
protokolle/
└── 553-WIL/
    ├── 553-WIL-EBA-PLB-PK-260224.md       — Besprechung 10
    ├── 553-WIL-EBA-PLB-PK-260324.md       — Besprechung 11
    ├── 553-WIL-EBA_BIM-PK-JF-07_260331.md — BIM-JF 07
    └── protokoll-state.json               — Zustand zwischen Besprechungen
```

## Nutzung im Plugin

Wenn der Nutzer EBA-Dateinamen wünscht, kann er das beim Aufruf so ausdrücken:

> „Speichere als EBA-Dateiname" / „use EBA filename"

Das Plugin erzeugt dann den Namen nach diesem Schema. Default bleibt das
einfachere `<JJJJ-MM-TT>_…`.

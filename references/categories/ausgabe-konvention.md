# Ausgabe-Konvention: Stand-D-QMG-XLSX

Der automatische Workflow für Transkripte aus der EBA Protokoll App erzeugt
genau eine XLSX-Datei aus der gebündelten Originalvorlage:

`references/templates/qmg/QMG-024-141_ORG-PK-EXCEL-MA_260828-D.xlsx`

Es gibt im automatischen Workflow keine Vorlagenauswahl. Besprechungsart und
Inhalt beeinflussen die D/K-Kategorien und Protokollpunkte, nicht die Datei-
Vorlage. Legacy-Word- oder andere Excel-Formate sind nur zulässig, wenn der
Nutzer sie ausdrücklich anfordert.

## Verzeichnisstruktur

```text
protokolle/
└── <projekt>/
    ├── <datum>_<projekt>_protokoll.xlsx
    └── protokoll-state.json        # nur bei Fortschreibung
```

Ohne ableitbaren Projektordner unter `protokolle/000-RAW/` ablegen.

## Pipeline

### 1. Flüchtiges Inhaltsformat

Das Protokoll zunächst gemäß
`${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp1-4.md` als Markdown in
einem OS-Temporärordner erzeugen (`tempfile.gettempdir()`, unter Windows
typischerweise `%TEMP%`). Markdown ist nur ein internes Zwischenformat und darf
nicht im Projektordner verbleiben.

### 2. Originalvorlage befüllen

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py" \
  "<temp-dir>/eba-protokoll-<datum>-<projekt>.md" \
  --format protokoll \
  --out-dir "protokolle/<projekt>/"
```

Auf Windows kann derselbe Befehl mit `python` oder `py -3` ausgeführt werden.
Der Renderer bootstrapt fehlende Python-Pakete selbst. Nutzer werden nicht nach
`pip`, `openpyxl` oder technischer Einrichtung gefragt.

### 3. Was geändert werden darf

Der Renderer öffnet die Originaldatei und befüllt nur die vorgesehenen
Inhaltsbereiche:

- `Deckblatt`: Besprechungsdaten, Projekt, Teilnehmende und Unterlagen.
- `Protokoll`: D/K, B, LN, Thema, Zuständigkeit, Termin und Status.
- `Doku_Info`: Termine, Aufstellvermerk, Anmerkungen und Anlagen.

`Hilfe und Tipps`, `intern`, Workbook-Design, Blattreihenfolge, Druckbereiche,
Header/Footer, Tabellenstruktur, Formate und die native Spalte `ausblenden`
bleiben aus der Quelle erhalten. Die Arbeitsmappe nicht neu aufbauen oder aus
einer visuellen Nachbildung erzeugen.

### 4. Quellenbindung

- Aussagen nur aus Transkript oder ausdrücklich bereitgestelltem Vorprotokoll.
- Keine erfundenen Entscheidungen, Zuständigkeiten, Fristen oder Teilnehmer.
- Unbekannte Sachangaben als `–`, `nicht angegeben` oder `zu klären` ausgeben.
- Dokumentierte Header-Fallbacks sind zulässig und werden in der
  Ergebniszusammenfassung genannt.
- Das Originaltranskript bleibt unverändert.

### 5. Prüfung

Vor Abschluss prüfen:

- XLSX lässt sich öffnen und enthält alle fünf Original-Sheets.
- Die Tabelle `Protokoll` reicht von Spalte A bis H.
- Spalte H heißt `ausblenden` und enthält die Stand-D-`IFERROR`-Formeln.
- `Hilfe und Tipps` und `intern` sind inhaltlich unverändert.
- Keine Mustertexte wie `_Vorname_`, `_Firma_` oder Lorem ipsum verbleiben in
  den befüllten Bereichen.
- Keine zweite XLSX-, DOCX-, PDF- oder Markdown-Ausgabe wurde erzeugt.

## Fortschreibung

Bei einem Vorprotokoll offene Punkte und Projektzustand über
`protokoll-fortschreiben` übernehmen. `protokoll-state.json` bleibt als
persistente Zustandsdatei bestehen; die sichtbare Ausgabe verwendet weiterhin
dieselbe Stand-D-XLSX-Vorlage.

## Explizite Legacy-Ausnahmen

Die übrigen gebündelten QMG-Vorlagen bleiben für ausdrücklich benannte
Sonderausgaben verfügbar. Sie dürfen nicht anhand von Schlüsselwörtern im
Transkript automatisch gewählt werden.

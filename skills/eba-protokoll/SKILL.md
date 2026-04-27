---
name: eba-protokoll
description: Use when the user asks to "make a protocol", "create a protocol", "Protokoll erstellen", "Protokoll generieren", "process this transcript", or hands over a transcript file (.txt or .srt produced by the EBA Protokoll App) without specifying which template. Auto-detects the right EBA protocol format (Gesprächsnotiz, Planungsprotokoll LP1-4, Bauleitungsprotokoll LP5) from the transcript content and project metadata, then delegates to the matching format skill.
---

# EBA-Protokoll: Auto-Erkennung & Dispatch

Diese Skill ist der **Haupteinstieg**, wenn der Nutzer einen Transkript zur Protokollierung
übergibt, ohne explizit eine Vorlage zu benennen. Sie erkennt das passende Format und
delegiert an die spezifische Format-Skill.

## Vorgehen

### 1. Eingabe prüfen

Erwartet wird ein Pfad zu einer Transkript-Datei (`.txt`, `.srt` oder Markdown). Die
EBA Protokoll App legt Transkripte standardmäßig unter `transkripte/` im Ausgabe-Verzeichnis
ab. Falls der Nutzer keinen Pfad nennt:

- Frage nach: „Welche Transkript-Datei soll ich verarbeiten?"
- Oder, wenn ein Ordner bekannt ist: liste alle `.txt`-Dateien im aktuellen Verzeichnis
  und im `transkripte/`-Unterordner.

### 2. Transkript einlesen und Metadaten extrahieren

Mit dem Read-Tool die ganze Datei einlesen. Folgende Metadaten heuristisch ableiten:

- **Besprechungsdatum**: aus dem Dateinamen (`YYMMDD_…` oder `YYYY-MM-DD_…`) oder, falls
  nicht erkennbar, aus erstgenannten Zeitstempeln im Transkript-Header. Wenn nichts
  erkennbar ist: heutiges Datum verwenden und im Protokoll mit `(angenommen)` markieren.
- **Sprecher**: alle eindeutigen Namen vor dem ersten Doppelpunkt jeder Zeile
  (`[HH:MM:SS] <Name>: <Text>`).
- **Projektname und -nummer**: aus dem ersten Vorkommen im Text (Sprecher nennen es
  oft am Anfang). Wenn nichts genannt ist: später beim Nutzer rückfragen.

### 3. Protokoll-Typ erkennen

Wende folgende Heuristik an (in dieser Reihenfolge, der erste Treffer gewinnt):

1. **Gesprächsnotiz** wenn alle gelten:
   - Transkript ist kürzer als ~1500 Wörter (≈ 10 Min Gespräch).
   - Es kommt **kein** Begriff aus dem LP-Vokabular vor (siehe unten).
   - Höchstens 3 Sprecher.
   - Kein „Besprechung Nr. …", „Jour Fixe", „LPH", „Werkplanung" im Text.

2. **Bauleitungsprotokoll LP5** wenn einer dieser Begriffe vorkommt:
   `Baustelle`, `Mangel`, `Bemusterung`, `Abnahme`, `Rohbau`, `Witterung`,
   `Gewerk`, `Kran`, `Liefertermin`, `LPH 5`, `LP5`, `LP 5`, `Bauleitung`,
   `OBÜ` (Objektüberwachung), `Polier`, `Bauleiter`, `Baustellenbegehung`.

3. **BIM-Protokoll** (Sub-Variante von LP1-4) wenn einer dieser Begriffe vorkommt:
   `BIM`, `IFC`, `BCF`, `BIMcollab`, `Revit`, `ViCADo`, `CDE`, `Fachmodell`,
   `Modellaustausch`, `LOIN`, `LOG`, `LOI`, `BAP`, `AIA`, `Datendrop`.
   → Verwendet das LP1-4-Skelett mit BIM-Kategorienschema.

4. **Planungsprotokoll LP1-4** (Default für längere Besprechungen):
   - Begriffe: `Bauantrag`, `Genehmigungsplanung`, `Vorentwurf`, `Entwurf`,
     `LPH 1`–`LPH 4`, `Planungsbesprechung`, `Jour Fixe`, `Kick-Off`,
     `Vorplanung`, `Workshop`, `DGNB`, `Brandschutzkonzept`,
     `Statik` (Kontext Planung), `TGA`-Konzept, `Fassadenplanung`.
   - Oder: > 3 Sprecher und > 1500 Wörter.

5. Wenn nichts klar passt: **frage den Nutzer**.

Stelle die erkannte Klassifikation **transparent** an den Nutzer und biete an, sie zu
ändern, bevor das Protokoll erzeugt wird:

> „Ich erkenne dies als **Planungsprotokoll LP1-4** (Begriffe: Bauantrag, DGNB, LP3).
> Soll ich so fortfahren oder eine andere Vorlage wählen
> (Gesprächsnotiz / LP1-4 / LP5)?"

In **Auto-Mode** (kontinuierlicher Modus, keine Rückfragen erwünscht): Klassifikation
ohne Rückfrage anwenden, aber im Protokoll-Header als `_(automatisch erkannt)_` vermerken.

### 4. An die Format-Skill delegieren

- **Gesprächsnotiz** → Skill `gespraechsnotiz` in `skills/gespraechsnotiz/SKILL.md`.
- **LP1-4** (inkl. BIM) → Skill `protokoll-lp1-4` in `skills/protokoll-lp1-4/SKILL.md`.
- **LP5** → Skill `protokoll-lp5` in `skills/protokoll-lp5/SKILL.md`.

Lies die jeweilige Skill-Datei und folge ihren Anweisungen.

### 5. Optional: Fortschreibung erkennen

Wenn ein vorheriges Protokoll im selben Projektordner existiert (Konvention:
`protokolle/<projekt>/protokoll-<NN>-…md` oder eine `protokoll-state.json`), gilt die
Folgebesprechung als **Fortschreibung**. Verwende dann zusätzlich die Skill
`protokoll-fortschreiben`, die offene Punkte aus dem Vorprotokoll übernimmt und mit
dem `E`-Suffix als Ergänzung markiert.

### 6. Ausgabe ablegen

Default-Speicherort: `protokolle/<jjjj-mm-tt>_<projekt>_<typ>.md` relativ zum aktuellen
Arbeitsverzeichnis. Wenn der Nutzer einen anderen Pfad wünscht, dort.

Wenn `protokolle/` nicht existiert: anlegen.

## Verfügbare Referenz-Dateien

- `${CLAUDE_PLUGIN_ROOT}/references/templates/gespraechsnotiz.md`
- `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp1-4.md`
- `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp5.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/disziplin-kategorien.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/status-codes.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/sprache-und-stil.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/transkript-format.md`

Lies die jeweils relevanten Referenzen vor dem Schreiben des Protokolls — sie enthalten
die EBA-spezifischen Konventionen.

## Anti-Pattern (was NICHT tun)

- ❌ Wörtliche Zitate aus dem Transkript ins Protokoll übernehmen.
- ❌ Den Sprecher „Ich" im Protokoll behalten — immer durch Kürzel oder
  „Protokollersteller" ersetzen.
- ❌ Englische Passagen unübersetzt lassen, wenn sie inhaltliche Aussagen sind.
- ❌ Termine als „nächste Woche" oder „bald" — immer in absolutes Datum oder Kalenderwoche
  umrechnen.
- ❌ Eine Themenzeile ohne Verantwortlichkeit erstellen — bei unklarer Zuordnung den
  Protokollersteller mit `(klären)` eintragen oder die Zeile mit Status `O` und einem
  Verantwortlichkeits-Hinweis versehen.
- ❌ Den Standard-Hinweistext („Vorbemerkung … 5 Kalendertage …") umschreiben — wortgleich
  aus der Vorlage übernehmen.

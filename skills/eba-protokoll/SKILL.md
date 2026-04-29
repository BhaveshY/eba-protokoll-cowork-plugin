---
name: eba-protokoll
description: >-
  Use when the user asks to "make a protocol", "create a protocol",
  "Protokoll erstellen", "Protokoll generieren", "process this transcript", or
  hands over a transcript file (.txt or .srt produced by the EBA Protokoll App)
  without specifying which template. Auto-detects the right EBA protocol format
  (Gesprächsnotiz, Protokoll-einfach, Planungsprotokoll LP1-4,
  Bauleitungsprotokoll LP5) from the transcript content and project metadata,
  then delegates to the matching format skill.
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
  oft am Anfang). Wenn nichts genannt ist: **nicht abbrechen** und nicht sofort
  rückfragen. Fallbacks aus
  `${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md` verwenden
  (`Projekt-Nummer = 000`, Projektname aus Datei/Thema oder `EBA / Allgemein`).

### 3. Protokoll-Typ erkennen

**Anker-Prinzip**: Echte EBA-Besprechungen benennen ihren Typ in den ersten
1–3 Sätzen ("Guten Morgen zur **Planungsbesprechung Nr. 12** …",
"Willkommen zur **BIM-Koordination Jour Fixe 07** …", "Wir starten die
**Baubesprechung Nr. 9** …"). Erkenne das Format vorrangig aus diesem
**Meeting-Anker** in den ersten ~30 Zeilen — nicht aus zufälligen
Stichwortvorkommen im Themenkörper.

Eine **LP1-4-Planungsbesprechung darf BIM-Themen enthalten**; das macht sie
nicht zu einer BIM-Koordination. Nur wenn das Meeting *selbst* eine
BIM-Koordination ist, gilt die BIM-Variante.

Wichtig: Flexible Metadaten bedeuten **nicht** flexible Formatwahl. Fehlende
Projekt-Nr. oder fehlender Projektname ändern nicht den Protokolltyp. Wenn ein
rohes Transkript klar eine Baubesprechung ist, bleibt es LP5; wenn es klar ein
Planungs-JF ist, bleibt es LP1-4. Nur die Headerfelder bekommen Fallbacks.

Wende folgende Heuristik an (in dieser Reihenfolge, der erste Treffer gewinnt):

1. **BIM-Protokoll** (Sub-Variante von LP1-4) wenn der **Meeting-Anker** in den
   ersten ~30 Zeilen oder im Dateinamen explizit eine BIM-Koordination benennt:
   - Phrasen: `BIM-Koordination`, `BIM-Jour-Fixe`, `BIM-JF`, `BIM-Koordination
     Jour Fixe`, `Koordinations-JF`, `BIM-Termin`.
   - Dateiname-Marker: `BIM-PK-JF`, `EBA_BIM-PK-JF`.

   → Verwendet das LP1-4-Skelett mit BIM-Kategorienschema (D/K = `1`–`8`).

   BIM-Signale gewinnen vor LP5-Signalen, wenn ein Meeting **explizit** als
   BIM-Koordination eröffnet wird — auch wenn Bauleitungs-Personal teilnimmt.

   **NICHT** als BIM klassifizieren, nur weil im Themenkörper Begriffe wie `BIM`,
   `IFC`, `BCF`, `BIMcollab`, `Revit`, `Fachmodell`, `Modellaustausch`, `LOIN`,
   `BAP`, `AIA`, `Datendrop` vorkommen. Diese können auch in einer
   Planungsbesprechung als ein Thema unter mehreren auftreten.

2. **Bauleitungsprotokoll LP5** wenn der **Meeting-Anker** eine Baustellen-
   oder Bauleitungsbesprechung benennt:
   - Phrasen: `Baubesprechung Nr.`, `Bauleitungs-JF`, `Baustellenbegehung`,
     `Mängelbegehung`, `Bauleitung Jour Fixe`, `OBÜ-Termin`, `LP5`, `LPH 5`.
   - Oder: Mehrere Themen rund um `Mangel`, `Bemusterung`, `Abnahme`, `Rohbau`,
     `Gewerk`, `Polier`, `Kran`, `Liefertermin`, `Witterung` werden im Transkript
     systematisch durchgesprochen (nicht nur einmal erwähnt).

3. **Planungsprotokoll LP1-4** (Tracking, mit D/K|B|LN) wenn einer gilt:
   - Es existiert ein Vorprotokoll im Projektordner
     (`protokolle/<projekt>/protokoll-state.json` oder ältere `protokoll-NN-…md`).
   - Im Transkript fallen **Verweise auf vorherige Besprechungen** (z.B.
     „letzte Woche", „letztes Mal", „aus #08", „LN 02E", „Punkt von letzter
     Woche damit erledigt").
   - **Meeting-Anker** in den ersten ~30 Zeilen: `Planungsbesprechung Nr.`,
     `Jour Fixe Nr.`, `JF-NN`, `Werkplanungs-JF`, `Planungs-JF`.
   - Oder: Im Transkript wird ein **fortgeschrittener LP-Kontext** beschrieben
     (Bauantrag-Einreichung, DGNB-Workshop mit Nummer, LP3-Abschluss,
     Fassadenstand mit Vorlagen) UND das Meeting hat eine erkennbare
     Tracking-Konvention (Themen mit konkretem Datum + Verantwortlichem
     im EBA-Kürzel-Stil).

4. **Protokoll-einfach** (Word LP1-4 Stand A, ohne Tracking) wenn der
   **Meeting-Anker** ein Kick-Off, Workshop, Erstgespräch ist:
   - Phrasen: `Kick-Off`, `Kickoff`, `Workshop`, `Erstgespräch`,
     `Auftaktbesprechung`, `Auftakt`, `Erstbesprechung`.
   - 3+ Sprecher, konkrete Liefertermine im Gespräch.
   - **Aber** kein Vorprotokoll, keine Verweise auf vorherige Besprechungen,
     kein D/K-Schema im Projekt etabliert.
   - Auch ohne Meeting-Anker verwenden, wenn ein rohes Transkript mehrere
     Sprecher, konkrete Aufgaben/Fristen und keinen Tracking-Hinweis enthält.

5. **EBA-Gesprächsnotiz ohne Projektbezug** wenn es EBA-bezogen ist, aber keine
   Projektbesprechung:
   - Beispiele: Interview, Pressegespräch, Redaktionstermin, Podcast, Radio- oder
     TV-Beitrag, ARD/ZDF/rbb/Deutschlandfunk/Magazin.
   - Sprecherrollen wie `Moderator`, `Redaktion`, `Journalist`, `Interviewer`,
     `Eike Becker`, `EBA`, `Architekt`.
   - Kein Projekt-Meeting-Anker für BIM, LP5, LP1-4 oder Kick-Off.

   → Verwende **Gesprächsnotiz**, nicht abbrechen. Fehlende Projektfelder werden
   mit EBA-Defaults befüllt:
   `Projektname = EBA`, `Projekt-Nummer = 000`,
   `Projekt-Beschreibung = EBA allgemein / Medien- und Interviewnotiz`.
   Ort/Quelle aus dem Text ableiten (z.B. `ARD Morgenmagazin / Studio Berlin`),
   sonst `nicht angegeben`. Ersteller default `EBA`, wenn kein Kürzel erkennbar ist.

6. **Gesprächsnotiz** wenn alle gelten:
   - Transkript ist kürzer als ~1500 Wörter (≈ 10 Min Gespräch).
   - Höchstens 3 Sprecher.
   - **Kein** Meeting-Anker für BIM, LP5, LP1-4 oder Kick-Off.
   - Keine fortgeschrittene Tracking-Sprache („aus #08", „LN 02E",
     „Besprechung Nr."). Casual Datums- und Wochentagsverweise
     („Donnerstag", „morgen", „bis 18.03.") sind in einer Gesprächsnotiz
     **erlaubt**.

7. Wenn nichts klar passt: nicht wegen fehlender Metadaten blockieren. Wähle
   das kleinste plausible Format: `gespraechsnotiz` für kurze/inhaltliche
   Mitschnitte, `protokoll-einfach` für mehrere Sprecher mit Aufgaben/Fristen.
   Frage nur nach, wenn LP1-4 vs. LP5 strukturell wirklich unentscheidbar ist.

Stelle die erkannte Klassifikation **transparent** dar, aber blockiere die
Erzeugung nicht wegen fehlender Projektmetadaten und warte im Normalfall nicht
auf Bestätigung:

> „Ich erkenne dies als **Planungsprotokoll LP1-4** (Begriffe: Bauantrag, DGNB, LP3).
> Ich fahre damit fort; falls das Format anders gemeint war, kann es danach mit
> einem Format-Hint neu erzeugt werden."

In **Auto-Mode** oder bei rohen Transkripten: Klassifikation ohne Rückfrage
anwenden, Fallback-Metadaten verwenden und Annahmen in der finalen
Zusammenfassung nennen.

### 4. An die Format-Skill delegieren

- **Gesprächsnotiz** → Skill `gespraechsnotiz` in `skills/gespraechsnotiz/SKILL.md`.
- **Protokoll-einfach** → Skill `protokoll-einfach` in `skills/protokoll-einfach/SKILL.md`.
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

**Endformat: Word-Vorlagen als DOCX + PDF; Excel-Vorlagen als XLSX. Kein
Markdown im Projekt-Ordner.**

Produktionsannahme: Windows 11 mit installiertem MS Word. Der Renderer
installiert fehlende Python-Pakete (`python-docx`, auf Windows `pywin32`)
automatisch im Benutzerkontext und nutzt Word für den PDF-Export. Stelle dem
Nutzer keine technischen Setup-Fragen.

Default-Speicherort:
`protokolle/<jjjj-mm-tt>_<projekt>_<typ>.<endung>` relativ zum aktuellen
Arbeitsverzeichnis. Wenn der Nutzer einen anderen Pfad wünscht, dort.

Wenn `protokolle/` nicht existiert: anlegen.

Die Format-Skills delegieren das Rendering an
`${CLAUDE_PLUGIN_ROOT}/scripts/render_protokoll.py`. Die vollständige Pipeline
ist beschrieben in
`${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.

## Verfügbare Referenz-Dateien

- `${CLAUDE_PLUGIN_ROOT}/references/templates/gespraechsnotiz.md`
- `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-einfach.md`
- `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp1-4.md`
- `${CLAUDE_PLUGIN_ROOT}/references/templates/protokoll-lp5.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/disziplin-kategorien.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/firma-kuerzel.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/status-codes.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/sprache-und-stil.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/transkript-format.md`
- `${CLAUDE_PLUGIN_ROOT}/references/categories/dateinamen-konvention.md`

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

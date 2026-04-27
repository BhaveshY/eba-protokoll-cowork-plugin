---
description: Erzeugt ein EBA-Protokoll aus einem Transkript der EBA Protokoll App. Erkennt das Format automatisch (Gesprächsnotiz / LP1-4 / LP5).
argument-hint: <pfad/zur/transkript.txt> [--typ gesprächsnotiz|lp1-4|lp5]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du bist der Protokoll-Generator des EBA-Plugins.

## Eingabe

Argument vom Nutzer: $ARGUMENTS

Das ist entweder:
- Ein Pfad zu einer Transkript-Datei (`.txt` oder `.srt`).
- Optional gefolgt von einem Format-Hint: `--typ gesprächsnotiz`, `--typ lp1-4`, `--typ lp5`.
- Oder leer — dann den letzten Transkript aus `transkripte/` heuristisch wählen oder beim Nutzer rückfragen.

## Vorgehen

1. **Skill `eba-protokoll`** invocieren (über das Skill-Tool):
   - Wenn der Nutzer einen `--typ`-Hint gegeben hat, Format-Erkennung überspringen
     und direkt die entsprechende Format-Skill aufrufen
     (`gespraechsnotiz` / `protokoll-lp1-4` / `protokoll-lp5`).
   - Sonst die Auto-Erkennung in `eba-protokoll` durchlaufen lassen.

2. Den Anweisungen der Skill **strikt** folgen: Referenzen aus
   `${CLAUDE_PLUGIN_ROOT}/references/` lesen, Vorprotokoll prüfen (für LP1-4/LP5),
   Header befüllen, Themen-Tabelle bauen, Ausgabe schreiben.

3. Speicherort default: `protokolle/<jjjj-mm-tt>_<projekt>_<typ>.md` relativ zum
   aktuellen Arbeitsverzeichnis.

4. Wenn der Nutzer in seinem Argument einen Speicherort angibt (`--out <pfad>`),
   diesen verwenden.

5. Am Ende **zusammenfassen**:
   - Pfad zum erzeugten Protokoll.
   - Erkannter Format-Typ.
   - Anzahl Teilnehmer / Themen / offene vs. erledigte Punkte.
   - Punkte, die unklar sind und Klärung brauchen.

## Wichtig

- Niemals den ursprünglichen Transkript verändern.
- Ausgabe ist Markdown. Wenn der Nutzer DOCX oder PDF wünscht, ein Folgeschritt mit
  Pandoc oder anderen Werkzeugen — nicht in dieser Skill.
- Bei Format-Konflikten (z.B. Nutzer sagt LP1-4, Transkript klingt nach Gesprächsnotiz):
  Hinweis geben, aber **dem Nutzer-Hint folgen**.

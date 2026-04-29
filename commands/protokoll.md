---
description: Erzeugt ein EBA-Protokoll aus einem Transkript der EBA Protokoll App. Erkennt das Format automatisch (Gesprächsnotiz / Protokoll-einfach / LP1-4 / LP5).
argument-hint: <pfad/zur/transkript.txt> [--typ gesprächsnotiz|einfach|lp1-4|lp5]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

Du bist der Protokoll-Generator des EBA-Plugins.

## Eingabe

Argument vom Nutzer: $ARGUMENTS

Das ist entweder:
- Ein Pfad zu einer Transkript-Datei (`.txt` oder `.srt`).
- Optional gefolgt von einem Format-Hint: `--typ gesprächsnotiz`,
  `--typ einfach`, `--typ lp1-4`, `--typ lp5`.
- Oder leer — dann den letzten Transkript aus `transkripte/` heuristisch wählen oder beim Nutzer rückfragen.

## Vorgehen

1. **Skill `eba-protokoll`** invocieren (über das Skill-Tool):
   - Wenn der Nutzer einen `--typ`-Hint gegeben hat, Format-Erkennung überspringen
     und direkt die entsprechende Format-Skill aufrufen
     (`gespraechsnotiz` / `protokoll-einfach` / `protokoll-lp1-4` / `protokoll-lp5`).
   - Sonst die Auto-Erkennung in `eba-protokoll` durchlaufen lassen.

2. Den Anweisungen der Skill **strikt** folgen: Referenzen aus
   `${CLAUDE_PLUGIN_ROOT}/references/` lesen, Vorprotokoll prüfen (für LP1-4/LP5),
   Header mit Fallbacks aus
   `${CLAUDE_PLUGIN_ROOT}/references/categories/metadaten-konvention.md`
   befüllen, Themen-Tabelle bauen, Ausgabe schreiben.

3. Speicherort default:
   `protokolle/<jjjj-mm-tt>_<projekt>_<typ>.docx` (+ `.pdf`, bei LP1-4/BIM
   auch `.xlsx`) relativ zum aktuellen Arbeitsverzeichnis. **DOCX und PDF sind
   die Endausgabe; LP1-4/BIM liefert zusätzlich XLSX**.
   Auf Windows 11 mit MS Word erzeugt der Renderer die PDF automatisch und
   bootstrapt fehlende Python-Pakete selbst. **Kein Markdown** im Projekt.

4. Wenn der Nutzer in seinem Argument einen Speicherort angibt (`--out <pfad>`),
   diesen verwenden.

5. Am Ende **zusammenfassen**:
   - Pfade zu DOCX und PDF; bei LP1-4/BIM auch zu XLSX.
   - Erkannter Format-Typ.
   - Anzahl Teilnehmer / Themen / offene vs. erledigte Punkte.
   - Annahmen/Fallbacks, z.B. `Projekt-Nr. 000`, `Ort nicht angegeben`.
   - Punkte, die fachlich unklar sind und später geprüft werden sollten.

## Wichtig

- Niemals den ursprünglichen Transkript verändern.
- Ausgabe ist **DOCX + PDF**, bei LP1-4/BIM zusätzlich **XLSX** — nicht
  Markdown. Keine technischen Setup-Fragen an den Nutzer; der Renderer heilt
  Abhängigkeiten selbst. Pipeline:
  `${CLAUDE_PLUGIN_ROOT}/references/categories/ausgabe-konvention.md`.
- Nicht wegen fehlender Projekt-Nr., Projektname, Ort oder Ersteller fragen.
  Diese Felder automatisch aus dem Transkript ableiten oder per
  `metadaten-konvention.md` füllen. Nur echte Format-Konflikte klären.
- Bei Format-Konflikten (z.B. Nutzer sagt LP1-4, Transkript klingt nach Gesprächsnotiz):
  Hinweis geben, aber **dem Nutzer-Hint folgen**.

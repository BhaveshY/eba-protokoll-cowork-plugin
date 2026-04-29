# Eingabeformat: EBA-Protokoll-App-Transkripte

Die EBA Protokoll App schreibt Transkripte in folgendem Format:

```
[HH:MM:SS] <Sprechername>: <gesprochener Text...>
```

## Sprecher-Konventionen

- **`Ich`** — der Protokollersteller (die Person, die die App bedient hat). Im Protokoll
  wird daraus entweder der echte Name (falls vom Nutzer eingetragen) oder
  „Protokollersteller". Die App-Kennung „Ich" darf **nicht** im fertigen Protokoll
  auftauchen.
- **`Sprecher 1`, `Sprecher 2`, …** — automatisch erkannte weitere Teilnehmer ohne
  manuelle Namenszuweisung. Im Protokoll bleibt diese Kennung nur dann, wenn keine
  bessere Information vorliegt; ansonsten den realen Namen aus dem Kontext erschließen.
  Nicht blockieren, wenn der Name fehlt: Sprecherlabel als Platzhalter verwenden und
  in der Zusammenfassung als Annahme nennen.
- **`Herr Müller`, `Frau Schmidt`, …** — wenn der Nutzer die Sprecher in der App
  umbenannt hat. Diese Namen sind autoritativ und werden 1:1 ins Protokoll übernommen.

## Zeitstempel

`[HH:MM:SS]` markiert den Beginn jedes Redebeitrags. Die letzte Zeit im Transkript
ist die effektive Endzeit der Besprechung — sie wird als „Zeit Ende" verwendet, wenn
nichts anderes bekannt ist.

## Mehrsprachigkeit

Deepgram Nova-3 transkribiert mehrsprachig. Wenn ein Transkript überwiegend deutsch
ist und einzelne englische Passagen enthält, bleiben diese im Protokoll auf Englisch
nur, wenn es sich um Eigennamen oder Fachbegriffe handelt. Inhaltliche Aussagen werden
ins Deutsche übersetzt und zusammengefasst.

## Untertitel-Variante

Liegt eine `.srt`-Datei statt einer `.txt`-Datei vor, hat sie das Format:

```
1
00:00:05,123 --> 00:00:11,456
[<Sprechername>] <Text>

2
00:00:12,000 --> 00:00:18,789
…
```

Die Sprecherkennzeichnung steht hier in eckigen Klammern am Anfang des Textes.

## Beispiel-Transkript

```
[00:00:05] Ich: Guten Morgen, fangen wir mit dem Bauantragsstand an.
[00:00:18] Herr Regener: Die Unterlagen sind vollständig, wir liegen im Plan.
[00:00:35] Frau Schmidt: Die Brandschutzauflagen sind noch offen.
           Ich kümmere mich darum bis Freitag.
[00:00:52] Ich: Danke. Nächster Punkt: BIM-Modell-Stand.
[00:01:05] Sprecher 3: Das LP3-Modell ist hochgeladen, Prüfung läuft.
```

In diesem Transkript:
- Protokollersteller = „Ich" (im Protokoll → realer Name oder Kürzel)
- Herr Regener, Frau Schmidt → reale Namen, 1:1 übernehmen
- „Sprecher 3" → bleibt als Platzhalter, wenn nicht aus Kontext aufgelöst werden kann

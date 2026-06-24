# Part B – Fachlogik & Regelwerk

Part A ist der Anfang des gesamten Dienstes. Es greift auf die UserStories in verschiedenen Formaten zu, liest diese ein, erstellt daraus das hauseigene Format **UniStori** und stellt dieses Format dann dem **Part_B** über die Function **get_all_uni_stories** .

## Einordnung im Projekt (Data → A → B)

Die drei Teile sind **keine getrennten Dienste**, die sich über das Netz
aufrufen. Es sind Python-Module, die sich direkt importieren:

Data: Die Daten liegen in dem entsprechenden Ordner bereit. Diese Vorraussetzung ist dabei auch die größte Einschränkung des ganzen Prozesses. Keine Oberfläche mit Uploadmöglichkeit oder ähnliches.

A: Part_A liest diesen Daten ein, stellt ein eigenes Datenmodell "UniStori" zur Verfügung und wandelt die eingelesen Daten in das UniStori Format um.

B: Part_B kann die umgewandelt Stories von Part_A über die Function "get_all_uni_stories" anfragen.

## Die Struktur von Part_A

Die Struktur ist von der Ki vorgegeben und bewusst zukunftsfähig (wartbar) aufgebaut

Ordner Loader: Hier werden die Daten aus dem Data Ordner je nach Format entsprechend importiert
Ordner Mapper: Hier wird das jeweilige Struktur in das UniStori Format umgewandelt
Ordner Models: Hier wird das UniStori Model definiert. Weitere Modelle könnten hier ganz einfach ergänzt werden
Ordner Utils: Hilfsfunktionen, die evtl. später nochmals verwenden werden könnten und deshalb seperat gehalten werden
main_a: Die Hauptdatei, die den ganzen Part_A strukturiert, alles korrekt aufruft und abschließend die Daten im UniStori Format zurückgibt

## Aufbau der UniStori

Die drei Kernfelder des UniStori-Schemas sind:

- id: string
- titlnamee: string
- beschreibung: string

Vorteilhaft ist, das die UniStori ganz einfach um weitere Felder ergänzt werden kann. Alternative kann man auch weitere eigene Modelle ergänzen und zwischen den Modellen wechseln

## Welche Hilfsfunktionen gibt es?

Wichtige Utils (Beispiele):

- normalize(text) → entfernt vorangehende bzw. abschließende Leerzeichen aus String. Außerdem werden mehrere Leerzeichen hintereinander entfernt und durch ein eizelnes ersetzt

## Ausgabe-Format (für Part_B)

Erreichbar über die Funktion: get_all_uni_stories(path: str = DATA_PATH)
Gibt einfach alle Stories Zeilenweise hintereinander aus.

Beispiel:

## Starten / Testen

- Um einfach nur den part_a laufen zu lassen kann man einfach die main_a.py datei ausführen (Über die GUI oder übers Terminal). Dabei muss beachtet werden, dass man in der main_a auch immer das Format und damit dann auch die entsprechenden stories auswählt. Das kann man an der hart codierten Stelle (wahl = "csv")

## Erweiterbarkeit & Entwicklungshinweise

- Untersützung von weiteren Foramten
  - Neuen Loader & Mapper ergänzen (Beispiel: XML)
- Models:
  - Ganz neue Modelle erstellen
  - Erweitern von bestehendem UniStori Model
- Anpassen der Function: get_all_uni_stories
  - Parameter: Filterkriterien mitgeben
  - Parameter: Pfad einer neuen Datei, Format würde dann automatisch erkannt
- Hinzufügen einer richtigen GUI für den Upload
- Ergänzung von richtigem Logging

<!-- Ende Part A Dokumentation -->

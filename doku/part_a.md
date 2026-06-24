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

## Wie die Zuordnung funktioniert

- Loader erkennt Quelldatei (Dateiendung / Header / Muster) und liefert Rohdatensätze (dict / lines / tabular).
- Mapper nimmt Rohdatensätze und wandelt sie in ein UniStori-Objekt (Instanz des Models) um.
- Models definieren das Schema, Validierung und serielle Schnittstelle (to_dict / from_dict).
- Utils bieten Hilfsfunktionen (Normalisierung, Datumsparsing, Tokenisierung).
- Reihenfolge (high-level):
  1. Loader.scan(data_path) → list[raw_records]
  2. for record in raw_records: mapper.map(record) → UniStori
  3. model.validate(uni_stori) → falls ok, sammeln
  4. main_a. get_all_uni_stories() gibt die Liste zurück

## Wie funktioniert der Import?

- Unterstützte Formate (aktuell): Markdown (.md), JSON (.json), CSV (.csv), Excel (.xlsx). Erweiterbar durch neuen Loader.
- Ablauf Loader:
  - Dateityp erkennen
  - Datei zeilenweise/als JSON/tabellarisch einlesen
  - Basis-Metadaten extrahieren (Dateiname, Pfad, Erstell-/Änderungsdatum)
  - Rohstruktur an Mapper weitergeben
- Fehlerbehandlung:
  - Parser-Fehler protokollieren und betreffenden Datensatz überspringen
  - Encoding-Probleme: UTF-8 fallback, Fehlerfallen dokumentieren
- Beispiel-Pseudocode:
  ```
  raw = loader.load_file(path)
  try:
      uni = mapper.map(raw)
  except MappingError as e:
      logger.warn(...)
      continue
  ```

## Aufbau der UniStori

Kernfelder des UniStori-Schemas (konservativ, erweiterbar):

- id: string (eindeutige ID, z.B. hash von Quelle+Titel)
- title: string
- description: string (Kurzbeschreibung)
- actors: list[string]
- preconditions: list[string]
- steps: list[ { step_id, text, outcome, type } ]
- acceptance_criteria: list[string]
- metadata: { source_file, source_type, created_at, tags, raw_source_excerpt }
- raw: optional original payload (zur Nachverfolgbarkeit)

Beispiel (schematisch):
{
"id": "md-abc123",
"title": "Als Nutzer möchte ich ...",
"description": "Kurzbeschreibung",
"actors": ["Nutzer", "System"],
"preconditions": [],
"steps": [{"step_id":1,"text":"Schritt 1","outcome":"..."}],
"acceptance_criteria": ["Kriterium 1"],
"metadata": {"source_file":"stories/foo.md","source_type":"markdown","created_at":"2024-01-01"},
"raw": {...}
}

## Welche Hilfsfunktionen gibt es?

Wichtige Utils (Beispiele):

- normalize_text(text) → konsistente Whitespace/Unicode-Normalisierung
- parse_steps(text) → list[steps] (erkennt nummerierte und freitext-Schritte)
- extract_metadata_from_filename(filename) → dict
- validate_uni_stori(uni_stori) → raises oder returns bool + errors
- deduplicate(stories) → entfernt doppelte Stories nach ID/Hash

## Ausgabe-Format (für Part_B)

- API-Funktion: get_all_uni_stories(path: str = DATA_PATH, filters: dict = None) → list[dict]
  - Gibt eine Liste der UniStori-Objekte (serialisiert als dict) zurück.
  - Optional: filterbar nach tags, source_type, date-range.
  - Fehler: Liefert leere Liste bei fehlenden Daten, protokolliert Probleme.

Beispiel Signatur in main_a:
def get_all_uni_stories(data_path: str = DEFAULT_PATH, filters: Optional[dict] = None) -> List[Dict]: # ...existing code...
return stories

## Starten / Testen

- lokal starten (Beispiel):
  - python -m part_a.main_a --data /path/to/data
- Tests:
  - pytest tests/ für Unit-Tests von Loader/Mapper/Models
  - Beispiel: teste mappe einer sample.md → erwartete UniStori-Felder
- Tip: Nutz end-to-end Fixtures im tests/data/ mit je einem Beispiel für jedes Format

## Logging & Fehlerbehandlung

- Verwende standardisiertes Logging (logging.getLogger("part_a")).
- Fehlerkategorien:
  - Recoverable (ein Datensatz fehlerhaft) → warn, skip
  - Fatal (Konfigurationsfehler) → raise/exit
- Fehlerstruktur: { type, message, source, record_id }

## Erweiterbarkeit & Entwicklungshinweise

- Neuen Loader hinzufügen:
  - Ordner: part_a/loader/new_loader.py
  - API: load_file(path) -> raw_record(s)
- Neuen Mapper hinzufügen:
  - Ordner: part_a/mapper/new_mapper.py
  - API: map(raw_record) -> UniStori
- Models:
  - Felder versionieren (UniStori v1, v2), Migrationspfad dokumentieren
- Tests & CI:
  - Jede neue Quelle benötigt mindestens einen Fixture-Test

## FAQ / Beispiele

- Wie erkenne ich Duplikate?
  - Hash aus (source_file + title + normalized_text)
- Wie erweitere ich das Schema?
  - Backwards-kompatible Felder optional hinzufügen, Versionsfeld einführen

<!-- Ende Part A Dokumentation -->

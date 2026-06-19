# Part B – Fachlogik & Regelwerk

Part B ist das **Gehirn in der Mitte** der Anwendung. Es bekommt die fertig
eingelesenen User-Stories von Part A und entscheidet **regelbasiert** (ohne KI),
zu welchem Bündelungsfach jede Story gehört: **SDM**, **EvP** oder **GiD**.

---

## Einordnung im Projekt (A → B → C)

Die drei Teile sind **keine getrennten Dienste**, die sich über das Netz
aufrufen. Es sind Python-Module, die sich direkt importieren:

```
data/stories.csv + stories.json
        │
   [Part A]  einlesen + mappen   →  list[UniStori]   (id, name, beschreibung)
        │   (direkter Import, kein HTTP)
   [Part B]  normalisieren + klassifizieren  →  list[Recommendation]
        │   (direkter Import, kein HTTP)
   [Part C]  stellt das Ergebnis per API bereit  →  GET /recommendations, …
```

Part B holt sich die Daten also **direkt von Part A** (Funktionsaufruf) und gibt
`Recommendation`-Objekte zurück. Nur **Part C** spricht HTTP.

---

## Die drei Bündelungsfächer

| Fach    | Bedeutung (Team-Definition)        | Typische Keywords                          |
|---------|------------------------------------|--------------------------------------------|
| **SDM** | Coding / Softwareentwicklung       | code, funktion, klasse, algorithmus, datenmodell, sql, mapping |
| **EvP** | Systemintegration & Administration | api, rest, endpunkt, server, **switch, router, firewall**, docker, deployment |
| **GiD** | Gestaltung von IT-Dienstleistungen | kunde, nutzer, anforderung, dokumentation, oberflaeche, prozess |

Die vollständigen Listen stehen in [`part_b/rules.py`](../part_b/rules.py) und
lassen sich dort leicht erweitern, ohne den Code anzufassen.

---

## Wie die Zuordnung funktioniert

Das Verfahren ist bewusst **transparent und nachvollziehbar** (Keyword-Scoring):

1. **Titel + Beschreibung** der Story werden in Kleinbuchstaben zusammengefügt.
2. Für **jedes Fach** wird gezählt, wie viele seiner Keywords vorkommen → `score`.
3. Das Fach mit dem **höchsten Score gewinnt**.
4. **Gleichstand?** Es entscheidet die feste Reihenfolge `SDM > EvP > GiD`.
5. **Kein Treffer?** Fallback auf `GiD`.

Jede Empfehlung liefert die **getroffenen Keywords als Begründung** mit – so ist
für die Bewertung sichtbar, *warum* eine Story einem Fach zugeordnet wurde.

> Hinweis: Es wird per Teilstring gesucht. `implementier` trifft also
> `implementieren`/`implementierung`. Sehr kurze Begriffe (`ip`, `lan`, `port`)
> wurden bewusst weggelassen, weil sie in anderen Wörtern stecken.

---

## Grenzfälle der Logik

Zwei Sonderfälle sind fest definiert und immer **deterministisch** – das gleiche
Ergebnis bei gleicher Eingabe.

### 1. Kein Keyword trifft (score 0)

Trifft kein einziges Keyword, fällt die Story auf **GiD** zurück
(`DEFAULT_SUBJECT`). Der Score ist dann `0` und die Treffer-Liste leer. Part C
erhält:

```json
{
  "empfehlung": {
    "fach": "GiD",
    "score": 0,
    "treffer": [],
    "alle_scores": { "SDM": 0, "EvP": 0, "GiD": 0 }
  }
}
```

**Erkennbar** ist so ein Fall an `score: 0` und `treffer: []` – eine *echte*
GiD-Story hat mindestens einen Treffer. Achtung: solche Stories erhöhen die
GiD-Zahl in `/summary`, ohne wirklich GiD zu sein.

### 2. Gleichstand / Mischfall (Tie)

Haben zwei (oder drei) Fächer den gleichen höchsten Score, gewinnt das Fach in
der festen Reihenfolge **`SDM > EvP > GiD`**. Beispiel mit `SDM = 2`, `EvP = 2`:

```json
{
  "empfehlung": {
    "fach": "SDM",
    "score": 2,
    "treffer": ["funktion", "logik"],
    "alle_scores": { "SDM": 2, "EvP": 2, "GiD": 0 }
  }
}
```

Das gewählte Fach steht in `fach`, aber `alle_scores` macht den Gleichstand
**transparent** sichtbar – man sieht, dass es knapp war.

---

## Beispiel-Ausgabe

| Story                                  | Fach    | Begründung (Treffer)                         |
|----------------------------------------|---------|----------------------------------------------|
| Datenbank-Schema anlegen               | **SDM** | modell, schema, sql, datenbank               |
| REST-Endpunkt implementieren           | **EvP** | api, rest, endpunkt, routing                 |
| Defekten Switch im Serverraum tauschen | **EvP** | switch, kabel, rechenzentrum, serverraum     |
| Anforderungen mit Kunde abstimmen      | **GiD** | kunde, anforderung, workshop                 |

---

## Dateien

| Datei                                              | Zweck                                              |
|----------------------------------------------------|----------------------------------------------------|
| [`part_b/rules.py`](../part_b/rules.py)            | Nur die Keyword-Listen je Fach (leicht editierbar) |
| [`part_b/classifier.py`](../part_b/classifier.py)  | Die Logik: `classify()` und `classify_all()`       |
| [`part_b/main_b.py`](../part_b/main_b.py)          | Demo/Schnelltest zum Ausprobieren                  |

---

## Starten / Testen

Aus dem Projekt-Root ausführen:

```bash
python part_b/main_b.py
```

Lädt die Stories über Part A, klassifiziert sie und gibt pro Story Fach, Score
und Treffer aus.

---

## Ausgabe-Format (für Part C)

Part C ruft `classify_all(stories)` auf und gibt jede `Recommendation` per
`to_dict()` aus. Eine Story sieht dann so aus:

```json
{
  "id": 102,
  "name": "Datenmodell fuer Mapping speichern",
  "beschreibung": "Die normalisierten Daten muessen in der Datenbank ...",
  "empfehlung": {
    "fach": "SDM",
    "score": 7,
    "treffer": ["datenmodell", "modell", "mapping", "datenbank", "repository"],
    "alle_scores": { "SDM": 7, "EvP": 1, "GiD": 0 }
  }
}
```

`alle_scores` zeigt immer **alle** Fach-Punkte mit – auch das macht die
Entscheidung nachvollziehbar.

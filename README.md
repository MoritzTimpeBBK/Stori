# Stori – User-Story Mapping Service

Abschlussprojekt LF8 (Fachinformatiker Anwendungsentwicklung, 2025/2026).

Stori liest User Stories aus heterogenen Quellen (CSV, JSON, später XML), überführt
sie in ein einheitliches Datenmodell und gibt eine **regelbasierte Empfehlung**,
zu welchem Bündelungsfach eine Story gehört: **SDM**, **EvP** oder **GiD**.
Die normalisierten Daten und die Zuordnung werden (geplant) über eine REST-API
bereitgestellt.

## Team & Rollen (Team 3)

| Rolle | Schwerpunkt                     | Person     |
|-------|---------------------------------|------------|
| A     | Datenimport & Mapping           | Marc P.    |
| B     | Fachlogik & Regelwerk           | Moritz T.  |
| C     | API, Tests & Dokumentation      | Jeremy P.  |

## Projektstruktur

```
Stori/
├── part_a/            Rolle A – Quellen einlesen + ins Modell mappen
│   ├── main_a.py        get_all_uni_stories("csv" | "json")
│   ├── loader/          CSV-/JSON-Leser
│   ├── mapper/          Quelle -> UniStori
│   ├── models/          UniStori (gemeinsames Datenmodell)
│   └── utils/           Text-Normalisierung
├── part_b/            Rolle B – regelbasierte Fachzuordnung
│   ├── classifier.py    classify() / classify_all()
│   ├── rules.py         Keyword-Listen je Fach
│   └── main_b.py        Demo/Schnelltest
├── part_c/            Rolle C – REST-API
├── data/              Beispiel-Quelldateien (stories.csv/json/xml)
├── doku/              Dokumentation
├── requirements.txt
└── README.md
```

## Voraussetzungen

- **Python 3.9 oder neuer**
- Keine externen Abhängigkeiten – nur die Python-Standardbibliothek.

## Was aktuell läuft

Beide Demos **aus dem Projekt-Root** ausführen (Part A nutzt relative Pfade wie
`data/stories.csv`):

```bash
# Rolle A – Einlesen + Mapping zeigen
python part_a/main_a.py

# Rolle B – Fachzuordnung zeigen (nutzt Part A)
python part_b/main_b.py
```

## API (Rolle C)

Endpunkte der REST-API:

| Methode | Pfad                          | Zweck                                            |
|---------|-------------------------------|--------------------------------------------------|
| GET     | `/userstories`                | alle Stories (mit optionalen Filtern)            |
| GET     | `/userstories/{id}`           | einzelne Story                                   |
| POST    | `/userstories`                | neue Story anlegen                               |
| PUT     | `/userstories/{id}`           | Story aktualisieren                              |
| DELETE  | `/userstories/{id}`           | Story löschen                                     |
| GET     | `/userstories/{id}/zuordnung` | Fach-Zuordnung (SDM/EvP/GiD) für eine Story      |

## Wie die Fachzuordnung funktioniert

Pro Bündelungsfach gibt es eine Liste typischer Schlüsselbegriffe
([`part_b/rules.py`](part_b/rules.py)). Titel + Beschreibung einer Story werden
durchsucht, das Fach mit den meisten Treffern gewinnt – die getroffenen Keywords
werden als Begründung mitgeliefert, damit die Entscheidung nachvollziehbar ist.

Details (Logik, Grenzfälle, Schnittstelle für Part C): **[doku/part_b.md](doku/part_b.md)**.

## Bekannter Stand

**Funktioniert:**
- Import aus CSV und JSON (Rolle A)
- gemeinsames Datenmodell `UniStori`
- regelbasierte Zuordnung zu SDM / EvP / GiD inkl. Begründung (Rolle B)
- Demo-Skripte für Part A und Part B

**Offene Punkte:**
- XML-Quelle (Datei vorhanden, noch nicht eingebunden)
- Tests und die Team-Dokus `doku/api.md`, `doku/teamdoku.md`, `doku/tests.md`

## Dokumentation

- [`doku/part_b.md`](doku/part_b.md) – Fachlogik & Regelwerk (Rolle B)
- [`doku/UniStori_Format_Spezifikation.md`](doku/UniStori_Format_Spezifikation.md) – Datenmodell
- [`doku/teamlog.md`](doku/teamlog.md) – Arbeitsprotokoll

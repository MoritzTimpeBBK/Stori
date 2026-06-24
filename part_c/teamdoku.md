# Team-Dokumentation (Team 3)

Übergreifende Doku zum Projekt **Stori – User-Story Mapping Service**
(LF8, 2025/2026). Ergänzt die rollenspezifischen Dokus.

## Team & Rollen

| Rolle | Schwerpunkt                | Person    | Hauptartefakte                              |
|-------|----------------------------|-----------|---------------------------------------------|
| A     | Datenimport & Mapping      | Marc P.   | `part_a/` (loader, mapper, models, utils)   |
| B     | Fachlogik & Regelwerk      | Moritz T. | `part_b/classifier.py`, `part_b/rules.py`   |
| C     | API, Tests & Dokumentation | Jeremy P. | `part_c/api.py`, `part_c/test_api.py`, `doku/` |

## Architektur / Datenfluss

```
Quelle (CSV/JSON/XML)
        │  Part A: loader -> mapper
        ▼
   UniStori (id, name, beschreibung)      <- gemeinsames Datenmodell
        │  Part B: classify() (Keyword-Scoring)
        ▼
   Recommendation (fach, score, treffer, alle_scores)
        │  Part C: FastAPI
        ▼
   REST-API (CRUD + /zuordnung)  ->  Client / Swagger UI
```

- **Part A** liest heterogene Quellen ein und überführt sie ins einheitliche
  Modell `UniStori`.
- **Part B** klassifiziert eine Story regelbasiert und transparent (Keyword-
  Treffer als Begründung) zu **SDM / EvP / GiD**.
- **Part C** stellt alles über eine REST-API bereit und liefert die Zuordnung
  on demand.

## Schnittstellen zwischen den Rollen

- A → B: `UniStori` (`id: int`, `name: str`, `beschreibung: str`)
- A → C: `get_all_uni_stories("csv" | "json")` zum Befüllen des Stores
- B → C: `classify(story) -> Recommendation`; `Recommendation.to_dict()` liefert
  exakt das JSON für den `/zuordnung`-Endpunkt
- B → C: `TIEBREAK_ORDER` als Quelle der gültigen Fächer (`SDM`, `EvP`, `GiD`)

## Setup

```bash
pip install -r requirements.txt   # FastAPI, uvicorn, pytest, httpx

# Demos (aus dem Projekt-Root)
python part_a/main_a.py           # Rolle A: Einlesen + Mapping
python part_b/main_b.py           # Rolle B: Fachzuordnung

# API
uvicorn part_c.api:app --reload   # Swagger UI unter /docs

# Tests
pytest part_c/test_api.py -v
```

## Stand & offene Punkte

**Funktioniert:**
- Import aus CSV und JSON (Rolle A)
- gemeinsames Datenmodell `UniStori`
- regelbasierte Zuordnung inkl. Begründung (Rolle B)
- vollständige REST-API mit allen sechs Endpunkten (Rolle C)
- automatisierte Tests (21 Tests, alle grün) (Rolle C)
- Doku: `doku/api.md`, `doku/tests.md`, `doku/teamdoku.md`

**Offen:**
- XML-Quelle (Datei vorhanden, Loader/Mapper noch nicht eingebunden)
- ggf. echte Persistenz statt In-Memory-Store (Part C ist dafür vorbereitet:
  der `StoryStore` ist gekapselt und kann ohne Endpunkt-Änderung ersetzt werden)

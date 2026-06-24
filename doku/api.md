# API-Dokumentation (Rolle C)

REST-API für den **Stori – User-Story Mapping Service**. Stellt CRUD-Operationen
für User Stories bereit und berechnet die regelbasierte Fach-Zuordnung
(**SDM / EvP / GiD**) über den Klassifizierer aus Part B.

- **Framework:** FastAPI
- **Basis-URL (lokal):** `http://127.0.0.1:8000`
- **Interaktive Doku:** `http://127.0.0.1:8000/docs` (Swagger UI) bzw. `/redoc`

## Starten

```bash
# aus dem Projekt-Root
pip install -r requirements.txt
uvicorn part_c.api:app --reload
```

Beim Start lädt die API die vorhandenen Stories aus Part A (CSV + JSON) in einen
In-Memory-Store. Fehlt eine Quelldatei, wird sie übersprungen (kein Abbruch).

## Datenmodell

Eine Story (`StoryOut`):

| Feld          | Typ    | Beschreibung                |
|---------------|--------|-----------------------------|
| `id`          | int    | eindeutige ID               |
| `name`        | string | Titel der Story             |
| `beschreibung`| string | Beschreibungstext           |

## Endpunkte im Überblick

| Methode | Pfad                          | Erfolg | Fehler            |
|---------|-------------------------------|--------|-------------------|
| GET     | `/userstories`                | 200    | 400 (Fach)        |
| GET     | `/userstories/{id}`           | 200    | 404               |
| POST    | `/userstories`                | 201    | 409, 422          |
| PUT     | `/userstories/{id}`           | 200    | 404, 422          |
| DELETE  | `/userstories/{id}`           | 204    | 404               |
| GET     | `/userstories/{id}/zuordnung` | 200    | 404               |

---

## GET /userstories

Liefert alle Stories. Optionale Query-Parameter:

| Parameter | Typ    | Beschreibung                                                        |
|-----------|--------|--------------------------------------------------------------------|
| `q`       | string | Volltextfilter (Teilstring in Name **oder** Beschreibung, case-insensitive) |
| `fach`    | string | Filter nach berechnetem Fach: `SDM`, `EvP` oder `GiD`              |

Der `fach`-Filter berechnet die Zuordnung **on-the-fly** über Part B – es wird
nichts persistent gespeichert. Ein ungültiger Wert führt zu **400**.

**Beispiel**

```bash
curl "http://127.0.0.1:8000/userstories?q=login&fach=GiD"
```

```json
[
  { "id": 1, "name": "Login-Maske bauen", "beschreibung": "Benutzer-Oberflaeche fuer den Login." }
]
```

---

## GET /userstories/{id}

Liefert eine einzelne Story. Existiert die ID nicht → **404**.

```bash
curl "http://127.0.0.1:8000/userstories/1"
```

```json
{ "id": 1, "name": "Login-Maske bauen", "beschreibung": "..." }
```

---

## POST /userstories

Legt eine neue Story an. **Body:**

| Feld          | Typ    | Pflicht | Beschreibung                                  |
|---------------|--------|---------|-----------------------------------------------|
| `id`          | int    | nein    | optional; wird sonst automatisch vergeben     |
| `name`        | string | ja      | mind. 1 Zeichen                               |
| `beschreibung`| string | nein    | Standard: leerer String                       |

- Erfolg → **201** mit der angelegten Story.
- ID bereits vorhanden → **409**.
- `name` fehlt/leer → **422** (Pydantic-Validierung).

```bash
curl -X POST "http://127.0.0.1:8000/userstories" \
  -H "Content-Type: application/json" \
  -d '{"name":"Docker-Deployment","beschreibung":"CI/CD container deploy server"}'
```

```json
{ "id": 4, "name": "Docker-Deployment", "beschreibung": "CI/CD container deploy server" }
```

---

## PUT /userstories/{id}

Aktualisiert eine Story (**Teil-Update** – nur übergebene Felder werden geändert).

| Feld          | Typ    | Pflicht | Beschreibung               |
|---------------|--------|---------|----------------------------|
| `name`        | string | nein    | neuer Titel (mind. 1 Zeichen) |
| `beschreibung`| string | nein    | neue Beschreibung          |

- Erfolg → **200** mit der aktualisierten Story.
- ID nicht vorhanden → **404**.

```bash
curl -X PUT "http://127.0.0.1:8000/userstories/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Geaenderter Titel"}'
```

---

## DELETE /userstories/{id}

Löscht eine Story.

- Erfolg → **204** (kein Body).
- ID nicht vorhanden → **404**.

```bash
curl -X DELETE "http://127.0.0.1:8000/userstories/1"
```

---

## GET /userstories/{id}/zuordnung

Berechnet die Fach-Zuordnung für eine Story über den transparenten
Keyword-Klassifizierer aus Part B. Die Antwort liefert das gewählte Fach, den
Score, die getroffenen Keywords (**Begründung**) sowie **alle** Fach-Scores zur
vollen Nachvollziehbarkeit. ID nicht vorhanden → **404**.

```bash
curl "http://127.0.0.1:8000/userstories/2/zuordnung"
```

```json
{
  "id": 2,
  "name": "SQL-Query optimieren",
  "beschreibung": "Datenbank Query refactoren, Schema anpassen.",
  "empfehlung": {
    "fach": "SDM",
    "score": 5,
    "treffer": ["refactor", "schema", "query", "sql", "datenbank"],
    "alle_scores": { "SDM": 5, "EvP": 0, "GiD": 0 }
  }
}
```

## Fehlerformat

Fehler folgen dem FastAPI-Standard:

```json
{ "detail": "Story mit id 999 nicht gefunden" }
```

| Status | Bedeutung                                             |
|--------|------------------------------------------------------|
| 400    | ungültiger `fach`-Filter                             |
| 404    | Story nicht gefunden                                 |
| 409    | POST mit bereits vergebener ID                       |
| 422    | Validierungsfehler im Request-Body                  |

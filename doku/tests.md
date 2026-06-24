# Test-Dokumentation (Rolle C)

Automatisierte Tests für die REST-API. Sie decken **alle sechs Endpunkte** ab –
sowohl den Happy Path als auch die Fehlerfälle (400 / 404 / 409 / 422).

- **Framework:** pytest
- **Test-Client:** `fastapi.testclient.TestClient` (basiert auf `httpx`)
- **Datei:** `part_c/test_api.py`

## Ausführen

```bash
# aus dem Projekt-Root
pip install -r requirements.txt
pytest part_c/test_api.py -v
```

Erwartetes Ergebnis: **21 passed**.

## Isolation der Tests

Die Tests sind **unabhängig von den Dateien unter `data/`**. Eine autouse-Fixture
(`fresh_store`) leert vor jedem Test den In-Memory-Store und befüllt ihn mit drei
festen Beispiel-Stories:

| id | name                  | erwartetes Fach |
|----|-----------------------|-----------------|
| 1  | Login-Maske bauen     | GiD             |
| 2  | SQL-Query optimieren  | SDM             |
| 3  | Server deployen       | EvP             |

Der `client`-Fixture nutzt den `TestClient` **bewusst ohne** Context-Manager,
damit der Startup-Bootstrap (Laden aus Part A) übersprungen wird und den Seed
nicht überschreibt.

## Abgedeckte Fälle

### GET /userstories
- `test_list_all` – alle Stories werden geliefert
- `test_list_filter_q` – Volltextfilter trifft die richtige Story
- `test_list_filter_q_case_insensitive` – Filter ist case-insensitive
- `test_list_filter_fach` – Filter nach Fach `SDM`
- `test_list_filter_fach_evp` – Filter nach Fach `EvP`
- `test_list_filter_fach_invalid` – ungültiges Fach → **400**

### GET /userstories/{id}
- `test_get_one` – vorhandene Story → **200**
- `test_get_one_missing` – unbekannte ID → **404**

### POST /userstories
- `test_create_autoid` – ohne ID → automatische Vergabe, **201**
- `test_create_with_id` – mit ID → **201**
- `test_create_duplicate_id` – vergebene ID → **409**
- `test_create_missing_name` – ohne `name` → **422**

### PUT /userstories/{id}
- `test_update` – Teil-Update (nur `name`), Beschreibung bleibt erhalten
- `test_update_both_fields` – beide Felder aktualisiert
- `test_update_missing` – unbekannte ID → **404**

### DELETE /userstories/{id}
- `test_delete` – löschen → **204**, danach **404**
- `test_delete_missing` – unbekannte ID → **404**

### GET /userstories/{id}/zuordnung
- `test_zuordnung_sdm` – korrektes Fach + Score + Begründung + alle Scores
- `test_zuordnung_evp` – Fach `EvP`
- `test_zuordnung_gid` – Fach `GiD`
- `test_zuordnung_missing` – unbekannte ID → **404**

## Hinweise

- Es werden keine echten Netzwerk-Ports geöffnet; der `TestClient` ruft die App
  in-process auf.
- Die Tests prüfen die Integration mit Part B (Klassifizierer) anhand der
  erwarteten Fächer – ändern sich die Keyword-Listen in `part_b/rules.py`,
  können die Zuordnungs-Tests angepasst werden müssen.

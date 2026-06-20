# Part B – Kurzüberblick (fürs Team)

**Was macht Part B?**
Ordnet jede User-Story **regelbasiert** einem Bündelungsfach zu: **SDM**, **EvP**
oder **GiD**. Keine KI – nur Keyword-Treffer, also voll nachvollziehbar.

**Wo sitzt es?**
```
A (liest ein)  →  B (ordnet zu)  →  C (stellt per API bereit)
 UniStori          Recommendation     JSON
```
Alles über **direkte Imports** – kein HTTP zwischen den Teilen.

---

## Die 3 Fächer

| Fach    | Bedeutung                          | Beispiel-Keywords                         |
|---------|------------------------------------|-------------------------------------------|
| **SDM** | Coding / Softwareentwicklung       | code, funktion, sql, datenmodell, mapping |
| **EvP** | Systemintegration & Administration | api, server, switch, router, firewall     |
| **GiD** | Gestaltung von IT-Dienstleistungen | kunde, doku, anforderung, oberflaeche     |

Keywords ändern? **Nur `part_b/rules.py`** anfassen – kein Code nötig.

---

## Für Part C – einfach das hier aufrufen

```python
from part_b.classifier import classify, classify_all

classify(story)            # eine UniStori  -> Recommendation
classify_all(stories)      # Liste          -> Liste von Recommendations
classify(story).to_dict()  # fertiges JSON-dict (Story + Empfehlung)
```

Für den Endpunkt `GET /userstories/{id}/zuordnung`:
```python
return classify(story).to_dict()["empfehlung"]
```

**Output (Empfehlung):**
```json
{ "fach": "SDM", "score": 7,
  "treffer": ["datenmodell", "sql", "mapping"],
  "alle_scores": { "SDM": 7, "EvP": 1, "GiD": 0 } }
```

---

## Gut zu wissen

- **Live berechnet** – Zuordnung wird bei jedem Aufruf neu ermittelt → nach einem
  `PUT` immer aktuell, nie veraltet.
- **Kein Treffer** → Fallback auf **GiD** (`score: 0`, `treffer: []`).
- **Gleichstand** → feste Reihenfolge **SDM > EvP > GiD** (`alle_scores` zeigt's offen).
- **Part B ist zustandslos** (reine Funktionen). Den Story-Speicher für CRUD
  (POST/PUT/DELETE) hält **Part C**.

Mehr Details: **[doku/part_b.md](part_b.md)**

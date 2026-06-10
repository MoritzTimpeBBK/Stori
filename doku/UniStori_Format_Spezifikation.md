# UniStori-Format — Spezifikation

> **Uni**fied **Stori**es · Entwickelt von Jeremy, Marc & Moritz · Team 3

---

## Was ist das UniStori-Format?

Das **UniStori-Format** ist das einheitliche, interne Datenformat des Teams. Es definiert,
wie alle externen Datenquellen — unabhängig von ihrer Herkunft — in eine einzige,
konsistente Struktur überführt werden, bevor sie weiterverarbeitet, gespeichert oder
über die API ausgegeben werden.

Der Name verbindet zwei Ideen: **Uni**fied steht für das gemeinsame Format, das alle
Quellen zusammenführt — und **Stori** ist der Projektname des Teams (GitHub-Repo:
[MoritzTimpeBBK/Stori](https://github.com/MoritzTimpeBBK/Stori)).

---

## Das Kern-Prinzip

```
Externe Quelle   →   Mapping   →   UniStori-Format   →   Fachlogik   →   API
  (CSV / JSON)       (Marc)           (intern)            (Moritz)      (Jeremy)
```

Jede Datenquelle wird **einmal** gemappt. Danach spricht das gesamte System
nur noch UniStori.

---

## Feldstruktur

Jeder UniStori-Datensatz enthält folgende Pflichtfelder:

| UniStori-Feld  | Typ       | Beschreibung                              |
|----------------|-----------|-------------------------------------------|
| `id`           | `integer` | Eindeutiger Bezeichner des Datensatzes    |
| `name`         | `string`  | Titel oder Kurzbezeichnung               |
| `beschreibung` | `string`  | Ausführlicher Beschreibungstext           |

> **Hinweis:** Weitere optionale Felder können bei Bedarf ergänzt werden, ohne die Pflichtstruktur zu brechen.

---

## Mapping-Tabelle: Bekannte Quellen

### Quelle 1 — JSON (GitHub Issues)

| Quellfeld | UniStori-Feld  | Typ       | Konvertierung     |
|-----------|----------------|-----------|-------------------|
| `number`  | `id`           | `integer` | Direkt (JSON)     |
| `title`   | `name`         | `string`  | Direkt (JSON)     |
| `body`    | `beschreibung` | `string`  | Direkt (JSON)     |

Alle weiteren Felder (`state`, `assignees`, `createdAt`, `closedAt`, `milestone`, …)
werden beim Import **nicht übernommen**.

### Quelle 2 — CSV

| Quellfeld *(variiert)* | UniStori-Feld  | Typ       | Konvertierung       |
|------------------------|----------------|-----------|---------------------|
| Spalte 1               | `id`           | `integer` | Parse & cast        |
| Spalte 2               | `name`         | `string`  | Trim & normalize    |
| Spalte 3               | `beschreibung` | `string`  | Trim & normalize    |

---

## Beispiel-Datensatz (UniStori)

Eingabe (GitHub Issue):

```json
{
  "number": 6,
  "title": "CSV-Import für die Lieferanten-Datenbank bereitstellen",
  "state": "open",
  "body": "## User Story\nAls Einkäufer möchte ich eine Schnittstelle nutzen, um Lieferanten-Stammdaten direkt in die relationale Datenbank einzuspielen und manuelle Aufwände zu minimieren.\n\n## Akzeptanzkriterien\n- [ ] Eine Upload-Maske nimmt CSV-Dateien im Backend entgegen.\n- [ ] Die Logik validiert alle erforderlichen Pflichtfelder vor dem Schreibvorgang.\n- [ ] Bei Fehlern wird ein Protokoll generiert und an den Client zurückgegeben.",
  "assignees": [{ "login": "thomas-braun" }],
  "createdAt": "2025-05-01T07:45:00Z",
  "closedAt": null,
  "milestone": { "title": "Sprint 3" }
}
```

Ausgabe (UniStori):

```json
{
  "id": 6,
  "name": "CSV-Import für die Lieferanten-Datenbank bereitstellen",
  "beschreibung": "## User Story\nAls Einkäufer möchte ich eine Schnittstelle nutzen, um Lieferanten-Stammdaten direkt in die relationale Datenbank einzuspielen und manuelle Aufwände zu minimieren.\n\n## Akzeptanzkriterien\n- [ ] Eine Upload-Maske nimmt CSV-Dateien im Backend entgegen.\n- [ ] Die Logik validiert alle erforderlichen Pflichtfelder vor dem Schreibvorgang.\n- [ ] Bei Fehlern wird ein Protokoll generiert und an den Client zurückgegeben."
}
```

---

## Datenfluss-Diagramm

```
┌─────────────────────────────────────────────────────────────────┐
│                         Externe Quellen                         │
│                                                                 │
│    ┌──────────────┐              ┌──────────────┐               │
│    │     CSV      │              │     JSON     │               │
│    │  (Quelle 1)  │              │  (Quelle 2)  │               │
│    └──────┬───────┘              └──────┬───────┘               │
└───────────┼─────────────────────────────┼───────────────────────┘
            │                             │
            ▼                             ▼
┌───────────────────────────────────────────────────────────────────┐
│                    MAPPING-SCHICHT  (Marc)                        │
│                                                                   │
│   Quellfeld → UniStori-Feld · Typprüfung · Normalisierung        │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ UniStori-Format  │  ← Alles spricht ab hier UniStori
                    │  { id, name,     │
                    │    beschreibung }│
                    └────────┬─────────┘
                             │
            ┌────────────────┴───────────────┐
            ▼                                ▼
┌─────────────────────┐          ┌────────────────────────┐
│  FACHLOGIK (Moritz) │          │    API / Tests          │
│                     │          │      (Jeremy)           │
│  Regelwerk, Validie-│          │                         │
│  rung, Geschäftslog.│          │  GET  /userstories      │
│                     │          │  POST /userstories      │
└─────────────────────┘          └────────────────────────┘
```

---

## Rollenverteilung & Verantwortlichkeiten

### 🗂️ Marc Price — Rolle A: Datenimport und Mapping
Marc ist verantwortlich für alles, was **vor** dem UniStori-Format passiert.

- Anbindung externer Quellen (CSV, JSON, …)
- Implementierung der Mapping-Logik
- Sicherstellung von Typen und Datenqualität beim Import

### ⚙️ Moritz Timpe — Rolle B: Fachlogik und Regelwerk
Moritz arbeitet **auf** dem UniStori-Format.

- Definition und Umsetzung der Geschäftsregeln
- Validierung eingehender UniStori-Datensätze
- Steuerung der internen Verarbeitungspipeline

### 🔌 Jeremy Alejo Plato — Rolle C: API, Validierung, Tests und Doku
Jeremy stellt das UniStori-Format nach **außen** zur Verfügung.

- Entwicklung der REST-API (FastAPI / Python)
- Schreiben und Pflegen der Tests
- Dokumentation der Schnittstellen

---

## Technologie-Stack

| Komponente     | Technologie              |
|----------------|--------------------------|
| Backend        | Python · FastAPI         |
| Architektur    | REST API · Frontend/Backend-Trennung |
| Quellcode      | [github.com/MoritzTimpeBBK/Stori](https://github.com/MoritzTimpeBBK/Stori) |
| Datenformate   | JSON · CSV               |

---

## Validierungsregeln

Ein gültiger UniStori-Datensatz muss folgende Bedingungen erfüllen:

1. `id` — muss vorhanden, eindeutig und eine ganze Zahl (`integer`) sein
2. `name` — darf nicht leer oder `null` sein
3. `beschreibung` — darf nicht leer oder `null` sein

Datensätze, die diese Regeln verletzen, werden beim Import **abgewiesen** und geloggt.

---

## Namens-Konventionen

- Feldnamen: `snake_case`, deutsch
- Werte: UTF-8, keine führenden/nachgestellten Leerzeichen
- IDs: immer numerisch, nie als String

---

## Versionierung

| Version | Datum      | Änderung                        | Autor                |
|---------|------------|---------------------------------|----------------------|
| 1.0     | 2026-06-10 | Initiale Definition             | Marc, Jeremy, Moritz |

---

> *„Ein Format für alle. Einmal gemappt, überall verstanden."*
> — Team 3, LF 8

---

*UniStori-Format · Team 3 · Abschlussprojekt LF 8*
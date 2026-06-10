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

Jeder UniStori-Datensatz enthält folgende Felder:

| UniStori-Feld  | Typ              | Pflicht | Beschreibung                                        |
|----------------|------------------|:-------:|-----------------------------------------------------|
| `id`           | `integer`        | ✅      | Eindeutiger Bezeichner des Datensatzes              |
| `name`         | `string`         | ✅      | Titel oder Kurzbezeichnung                          |
| `beschreibung` | `string`         | ✅      | Ausführlicher Beschreibungstext (User Story + AKs)  |
| `status`       | `string`         | ✅      | Bearbeitungsstatus: `"open"` oder `"closed"`        |
| `verantwortliche` | `string[]`    | ❌      | Liste der zugewiesenen Personen (kann leer sein)    |
| `erstellt_am`  | `string` (ISO 8601) | ✅   | Erstellungszeitpunkt im Format `YYYY-MM-DDTHH:mm:ssZ` |
| `geschlossen_am` | `string\|null` (ISO 8601) | ❌ | Abschlusszeitpunkt, `null` wenn noch offen      |
| `sprint`       | `string\|null`   | ❌      | Zugehöriger Sprint oder Backlog, `null` wenn keiner |

> **Hinweis:** Felder mit ❌ sind optional. Pflichtfelder mit ✅ müssen immer vorhanden
> und gültig sein — andernfalls wird der Datensatz beim Import **abgewiesen**.

---

## Mapping-Tabelle: GitHub Issues (JSON)

Die primäre Datenquelle sind GitHub Issues im JSON-Format.

| GitHub-Quellfeld       | UniStori-Feld      | Typ                  | Konvertierung / Hinweis                          |
|------------------------|--------------------|----------------------|--------------------------------------------------|
| `number`               | `id`               | `integer`            | Direkt übernehmen                                |
| `title`                | `name`             | `string`             | Direkt übernehmen, führende Leerzeichen trimmen  |
| `body`                 | `beschreibung`     | `string`             | Direkt übernehmen                                |
| `state`                | `status`           | `string`             | Direkt übernehmen (`"open"` / `"closed"`)        |
| `assignees[].login`    | `verantwortliche`  | `string[]`           | Alle `login`-Werte in ein Array extrahieren      |
| `createdAt`            | `erstellt_am`      | `string` (ISO 8601)  | Direkt übernehmen                                |
| `closedAt`             | `geschlossen_am`   | `string\|null`       | Direkt übernehmen, `null` wenn nicht gesetzt     |
| `milestone.title`      | `sprint`           | `string\|null`       | Nur `.title` extrahieren, `null` wenn kein Milestone |

### Nicht übernommene GitHub-Felder

Folgende Felder aus den GitHub Issues werden im UniStori-Format **nicht** abgebildet,
da sie für die interne Verarbeitung nicht benötigt werden:

- `labels`, `comments`, `url`, `html_url`, `user`, `reactions`, u. a.

---

## Mapping-Tabelle: CSV

Bei CSV-Quellen orientiert sich das Mapping an der Spaltenreihenfolge oder den
Spaltenköpfen. Fehlende Felder werden mit Standardwerten befüllt.

| CSV-Spalte / Header    | UniStori-Feld      | Typ       | Konvertierung / Standardwert              |
|------------------------|--------------------|-----------|-------------------------------------------|
| `number` / Spalte 1    | `id`               | `integer` | Parse & cast zu Integer                   |
| `title` / Spalte 2     | `name`             | `string`  | Trim & normalize                          |
| `body` / Spalte 3      | `beschreibung`     | `string`  | Trim & normalize                          |
| `state` / Spalte 4     | `status`           | `string`  | Lowercase, Standardwert: `"open"`         |
| `assignees` / Spalte 5 | `verantwortliche`  | `string[]`| Semikolon-getrennte Liste → Array, Standard: `[]` |
| `createdAt` / Spalte 6 | `erstellt_am`      | `string`  | ISO-8601-Parsing, Pflichtfeld             |
| `closedAt` / Spalte 7  | `geschlossen_am`   | `string\|null` | ISO-8601-Parsing, Standard: `null`   |
| `milestone` / Spalte 8 | `sprint`           | `string\|null` | Trim, Standard: `null`               |

---

## Beispiel-Datensätze (UniStori)

### Offenes Issue mit Assignee und Sprint

Basierend auf GitHub Issue #1 aus den realen Projektdaten:

```json
{
  "id": 1,
  "name": "Automatisierte Einarbeitung über den internen Server",
  "beschreibung": "## User Story\nAls HR-Manager möchte ich ein digitales System auf unserem Server bereitstellen, damit das Onboarding neuer Mitarbeiter papierlos und zentral gesteuert wird.\n\n## Akzeptanzkriterien\n- [ ] Das Netzwerk muss die sichere Übertragung des Personaldaten-Formulars garantieren.\n- [ ] Automatischer Versand von System-Zugangsdaten nach erfolgreicher Registrierung.\n- [ ] Eine interaktive Checkliste für die Einarbeitung wird im Intranet bereitgestellt.",
  "status": "open",
  "verantwortliche": ["anna-mueller"],
  "erstellt_am": "2025-05-01T08:23:00Z",
  "geschlossen_am": null,
  "sprint": "Sprint 3"
}
```

### Geschlossenes Issue ohne Assignee

Basierend auf GitHub Issue #10:

```json
{
  "id": 10,
  "name": "Automatisierte Backend-Meldung bei ablaufenden Verträgen",
  "beschreibung": "## User Story\nAls Einkäufer möchte ich bei bevorstehendem Vertragsende benachrichtigt werden, basierend auf den in der Datenbank hinterlegten Fristen.\n\n## Akzeptanzkriterien\n- [ ] Das Backend stößt 30 Tage vor Ablauf eine E-Mail-Generierung an.\n- [ ] Eine finale Warnung erfolgt 7 Tage vor dem Stichtag.\n- [ ] Die Nachricht enthält eine URL, die direkt auf den Datensatz in der App verweist.",
  "status": "closed",
  "verantwortliche": ["thomas-braun"],
  "erstellt_am": "2025-03-01T08:00:00Z",
  "geschlossen_am": "2025-04-01T12:00:00Z",
  "sprint": "Sprint 1"
}
```

### Issue ohne Assignee und ohne Sprint (Backlog)

Basierend auf GitHub Issue #3:

```json
{
  "id": 3,
  "name": "Karrierepfade im mobilen WAN-Netzwerk bereitstellen",
  "beschreibung": "## User Story\nAls Mitarbeiter möchte ich meine Entwicklungswege auch von unterwegs über das Firmen-WAN einsehen können, um meine Weiterbildung flexibel zu planen.\n\n## Akzeptanzkriterien\n- [ ] Die Server-Infrastruktur stellt mindestens zwei visuelle Karrierepfade stabil dar.\n- [ ] Direkte Verlinkung zu passenden Bildungsangeboten im Intranet.\n- [ ] Optimierte mobile Ansicht für den Abruf außerhalb des lokalen Büros.",
  "status": "open",
  "verantwortliche": [],
  "erstellt_am": "2025-05-12T11:30:00Z",
  "geschlossen_am": null,
  "sprint": "Backlog"
}
```

---

## Datenfluss-Diagramm

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Externe Quellen                             │
│                                                                      │
│   ┌─────────────────────────┐    ┌─────────────────────────┐        │
│   │       JSON              │    │         CSV             │        │
│   │  (GitHub Issues API)    │    │    (Manueller Import)   │        │
│   │                         │    │                         │        │
│   │  number, title, body,   │    │  Spalten: id, title,    │        │
│   │  state, assignees,      │    │  body, state, assignees,│        │
│   │  createdAt, closedAt,   │    │  createdAt, closedAt,   │        │
│   │  milestone              │    │  milestone              │        │
│   └────────────┬────────────┘    └────────────┬────────────┘        │
└────────────────┼─────────────────────────────────┼───────────────────┘
                 │                                 │
                 ▼                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      MAPPING-SCHICHT  (Marc)                           │
│                                                                        │
│   Quellfeld → UniStori-Feld · Typprüfung · Normalisierung             │
│   assignees[].login → string[]  ·  milestone.title → string|null      │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
                   ┌─────────────────────────────────┐
                   │        UniStori-Format           │  ← Einheitliche Sprache
                   │                                  │
                   │  { id, name, beschreibung,       │
                   │    status, verantwortliche,      │
                   │    erstellt_am, geschlossen_am,  │
                   │    sprint }                      │
                   └────────────────┬─────────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
  ┌──────────────────────────┐             ┌──────────────────────────┐
  │    FACHLOGIK (Moritz)    │             │    API / Tests (Jeremy)  │
  │                          │             │                          │
  │  Regelwerk, Validierung, │             │  GET  /userstories       │
  │  Geschäftslogik,         │             │  POST /userstories       │
  │  Duplikatsprüfung        │             │  PUT  /userstories/{id}  │
  │                          │             │  DELETE /userstories/{id}│
  └──────────────────────────┘             └──────────────────────────┘
```

---

## Validierungsregeln

Ein gültiger UniStori-Datensatz muss folgende Bedingungen erfüllen:

| # | Feld              | Regel                                                                 |
|---|-------------------|-----------------------------------------------------------------------|
| 1 | `id`              | Vorhanden, eindeutig, ganzzahlig (`integer`), größer als `0`         |
| 2 | `name`            | Vorhanden, nicht leer, nicht `null`                                  |
| 3 | `beschreibung`    | Vorhanden, nicht leer, nicht `null`                                  |
| 4 | `status`          | Genau `"open"` oder `"closed"`, kein anderer Wert erlaubt            |
| 5 | `verantwortliche` | Muss ein Array sein — auch leeres Array `[]` ist gültig              |
| 6 | `erstellt_am`     | Vorhanden, gültiges ISO-8601-Datum                                   |
| 7 | `geschlossen_am`  | Gültiges ISO-8601-Datum **oder** explizit `null`                     |
| 8 | `sprint`          | Beliebiger String **oder** `null` — kein Leerstring `""` erlaubt    |

Datensätze, die diese Regeln verletzen, werden beim Import **abgewiesen** und in einem
Fehlerprotokoll erfasst.

---

## Rollenverteilung & Verantwortlichkeiten

### 🗂️ Marc Price — Rolle A: Datenimport und Mapping
Marc ist verantwortlich für alles, was **vor** dem UniStori-Format passiert.

- Anbindung externer Quellen (JSON via GitHub API, CSV)
- Implementierung der Mapping-Logik (inkl. `assignees[].login`-Extraktion)
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

| Komponente   | Technologie                                                                         |
|--------------|-------------------------------------------------------------------------------------|
| Backend      | Python · FastAPI                                                                    |
| Architektur  | REST API · Frontend/Backend-Trennung                                                |
| Quellcode    | [github.com/MoritzTimpeBBK/Stori](https://github.com/MoritzTimpeBBK/Stori)        |
| Datenformate | JSON (GitHub Issues API) · CSV                                                      |

---

## Namens-Konventionen

- Feldnamen: `snake_case`, Deutsch
- String-Werte: UTF-8, keine führenden/nachgestellten Leerzeichen
- IDs: immer numerisch (`integer`), nie als String
- Datumsfelder: immer ISO 8601 mit Zeitzone (`Z` = UTC)
- Leere Listen: `[]` statt `null`
- Fehlende optionale Strings: `null` statt `""`

---

## Versionierung

| Version | Datum      | Änderung                                          | Autor                |
|---------|------------|---------------------------------------------------|----------------------|
| 1.0     | 2026-06-10 | Initiale Definition (3 Felder: id, name, beschreibung) | Marc, Jeremy, Moritz |
| 1.1     | 2026-06-10 | Erweiterung auf 8 Felder anhand realer GitHub-Issues-Daten | Marc, Jeremy, Moritz |

---

> *„Ein Format für alle. Einmal gemappt, überall verstanden."*
> — Team 3, LF 8

---

*UniStori-Format · Team 3 · Abschlussprojekt LF 8*

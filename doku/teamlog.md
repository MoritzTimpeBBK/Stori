# Teamlog

> **Datei:** `doku/teamlog.md`  
> **Format:** Nach jedem Termin ergänzen – wer hat was gemacht, was ist offen, was ist der nächste Schritt.

---

## 27.05. – Projektstart

| Person  | Was wurde bearbeitet     |
| ------- | ------------------------ |
| Moritz  | Git Repo erstllt         |
| Marc    | Projekt Namen ausgewählt |
| Jerremy | Nicht Anwesend           |

**Offene Punkte:**

- Rollen Einteilung
- Einheitliches Format

**Nächster Schritt:**

- Jerremy über Projekt informieren
- Alle Mittglieder müssen sich Git Accounts erstellen

---

## 03.06. – Konzept steht

| Person                | Was wurde bearbeitet                |
| --------------------- | ----------------------------------- |
| Marc, Jerremy, Moritz | Rolleneinteilung                    |
| Marc, Jerremy, Moritz | Einheitliches Format ausgewählt     |
| Moritz                | Alle Mitglieder im Repo hinzugefügt |

**Offene Punkte:**

- Git Repo Minimal Struktur
- Einheitliches Format Dokumentieren

**Nächster Schritt:**

- Git Repo clonen auf jeden Gerät

---

## 10.06. – Vertretungssprint

| Person  | Was wurde bearbeitet                                                                                                                          |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Moritz  | UniStori-Format-Spezifikation (v1.1) inkl. GitHub-Issues-Mapping-Beispiel erstellt; Projekt- und Abgabe-HTML in `doku` abgelegt (10:06–11:10) |
| Marc    | Minimale Ordnerstruktur aufgebaut (`requirements.txt`, `doku/` mit api.md, teamdoku.md, teamlog.md, tests.md) (11:04)                         |
| Jerremy | Nicht anwesend                                                                                                                                |

**Offene Punkte:**

- Mapping-Tabelle Quelle → UniStori vervollständigen
- Regelwerk (SDM/EvP/GiD) und API-Skizze ausarbeiten

**Nächster Schritt:**

- erste Implementierung von Import und Zuordnung bis zum Technikreview (17.06.)

---

## 17.06. – Technikreview

| Person | Was wurde bearbeitet                                                                                                                                             |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Moritz | Erster lauffähiger Prototyp aller drei Rollen als Einzelskripte (`role_a_ingest.py`, `role_b_logic.py`, `role_c_api.py`); Merge-Konflikt aufgelöst (11:35–11:57) |
| Marc   | Erstes Datenmodell ergänzt (`PartA/Data_model`) (11:36)                                                                                                          |
| Jeremy | kein Commit im Repo (Git-Probleme, siehe 24.06.)                                                                                                                 |

**Offene Punkte:**

- Prototyp in saubere Modulstruktur (part_a / part_b / part_c) überführen
- einheitliche Lade-Methode für die Quellen fehlt noch

**Nächster Schritt:**

- Marc: part_a als Module umsetzen (Loader, Mapper, UniStori-Modell)
- Moritz: part_b mit Keyword-Regeln und Zuordnung (SDM/EvP/GiD)
- Team: Treffen in der Stadt um zusammen weiter zu entwicklen

---

## 19.06. – Präsenzmeeting

Gemeinsames Präsenztreffen in der Stadt am Abend des 19.06. – hier entstand der Großteil der Implementierung zusammen (belegt durch den dichten Commit-Block am Abend).

| Person | Was wurde bearbeitet                                                                                                                                                                                                                           |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Marc   | part_a als saubere Modulstruktur umgesetzt (loader, mapper, models/UniStori, utils, 21:48); Pfad-Problem Windows/macOS behoben (22:28); zentrale Lade-Methode `get_all_uni_stories(source_type)` ergänzt (kurz nach Mitternacht, 20.06. 00:21) |
| Moritz | Bugfix in den part_a-Loadern (fehlerhafter `typing`-Import, 22:12); part_b umgesetzt (classifier, rules, main_b) inkl. part_b-Doku (23:53)                                                                                                     |
| Jeremy | kein Commit im Repo (Git-Probleme); arbeitet an den Part-C-Endpunkten                                                                                                                                                                          |

**Offene Punkte:**

- part_b an die finale Part-A-Methode `get_all_uni_stories` anbinden
- Part C (Endpunkte) implementieren und ins Repo pushen

**Nächster Schritt:**

- Moritz: Integration der Part-A-Methode in part_b (folgte am 20.06.)
- Repo aufräumen und Doku vervollständigen

---

## 24.06. – Kernabnahme

| Person | Was wurde bearbeitet                                                                                                                                                  |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Marc   | Kern von part_a beim Treffen am 19.06. gebaut (siehe oben); part_a zum Stichtag stabil lauffähig; part_a-Doku wird nachgereicht                                       |
| Moritz | part_b am 20.06. an `get_all_uni_stories` angebunden (16:17); Doku part_b zusammengeführt; Repo aufgeräumt (tote Dateien entfernt, 24.06. 09:43); README aktualisiert |
| Jeremy | API-Endpunkte definiert und im Team (Teams) geteilt; part_c-Code wegen Git-Problemen noch nicht im Repository                                                         |

**Entscheidung:**

- Die Fachzuordnung ("Recommendation") wird **nicht** in `UniStori` gespeichert, sondern bleibt ein eigenes Objekt. Part C holt sie per `GET /userstories/{id}/zuordnung` über die ID ab. Begründung: klare Trennung der Verantwortlichkeiten (Part A = Daten, Part B = Zuordnung).

**Offene Punkte:**

- Part C (REST-API) noch nicht im Repository (Git-Probleme bei Jeremy)
- Doku (`api.md` / `teamdoku.md` / `part_a.md` ) wird nachgereicht
- Abgabe-Formular (HTML) wird gemeinsam im Unterricht ausgefüllt (persönliche Statements)
- XML-Quelle vorbereitet, aber noch nicht eingebunden

**Nächster Schritt:**

- Jeremy: part_c pushen
- Abgabe und restliche Doku gemeinsam im Unterricht fertigstellen

---

## 08.07. – Politur

| Person | Was wurde bearbeitet |
| ------ | -------------------- |
|        |                      |
|        |                      |
|        |                      |

**Offene Punkte:**

-

**Nächster Schritt:**

-

---

## 15.07. – Abschluss

| Person | Was wurde bearbeitet |
| ------ | -------------------- |
|        |                      |
|        |                      |
|        |                      |

**Offene Punkte:**

-

**Nächster Schritt:**

-

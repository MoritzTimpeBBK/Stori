# Abschlussprojekt LF8 - User-Story Mapping Service

Liest User Stories aus heterogenen Quellen (CSV, JSON, XML), ueberfuehrt sie in
ein einheitliches Modell, stellt sie per REST-API bereit und gibt eine
regelbasierte Empfehlung fuer das Buendelungsfach (SDM / EvP / GiD).

## Sofort starten (ein Befehl, keine Installation noetig)

```bash
python3 main.py
```

Dann im Browser oder per curl aufrufen:

- http://127.0.0.1:8000/recommendations  <- das Kernergebnis
- http://127.0.0.1:8000/summary          <- Zaehlung pro Fach
- http://127.0.0.1:8000/stories
- http://127.0.0.1:8000/stories/GH-102
- http://127.0.0.1:8000/health

## Dateien = Rollen (jede Rolle eine Datei)

| Datei              | Rolle | Aufgabe                                              |
|--------------------|-------|------------------------------------------------------|
| `role_a_ingest.py` | A     | CSV/JSON/XML einlesen -> einheitliches Modell        |
| `role_b_logic.py`  | B     | Normalisieren + regelbasierte Zuordnung SDM/EvP/GiD  |
| `role_c_api.py`    | C     | REST-API, stellt Daten + Empfehlungen bereit         |
| `main.py`          | -     | Verkettet alles, startet die API                     |
| `data/`            | -     | Beispiel-Quelldateien (3 Formate)                    |

Jede Rolle kann auch einzeln getestet werden:

```bash
python3 role_a_ingest.py   # zeigt nur das Einlesen
python3 role_b_logic.py    # zeigt nur die Zuordnung
```

## Wie die Zuordnung funktioniert (Rolle B)

Pro Buendelungsfach gibt es eine Liste typischer Schluesselbegriffe (in
`role_b_logic.py`, Konstante `RULES`). Titel + Beschreibung + Labels werden
durchsucht, das Fach mit den meisten Treffern gewinnt. Die getroffenen
Keywords werden als Begruendung mitgeliefert - damit ist die Entscheidung
nachvollziehbar. Die Keyword-Listen sind bewusst leicht anpassbar.

Hinweis: Die genauen Voll-Namen der Faecher SDM/EvP/GiD bitte mit der
Lehrkraft abgleichen und die Keyword-Regeln ggf. ergaenzen.

## 1-Minuten-Demo fuer die Praesentation

1. `python3 main.py` starten.
2. `/summary` zeigen -> "9 Stories aus 3 Formaten, automatisch auf 3 Faecher verteilt".
3. `/recommendations` zeigen -> pro Story das Fach + die getroffenen Keywords.
4. Eine neue Zeile in `data/stories.csv` ergaenzen, Server neu starten -> sie
   taucht klassifiziert auf. Zeigt: das System ist erweiterbar.

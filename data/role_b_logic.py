"""
Rolle B - Logik & Mapping  (DEINE Rolle)
========================================

Aufgabe:
1. Die eingelesenen Stories normalisieren (saubere, einheitliche Daten).
2. Jede Story regelbasiert einem Buendelungsfach zuordnen: SDM, EvP oder GiD.

Das Mapping ist TRANSPARENT und regelbasiert (Keyword-Scoring):
- Pro Fach gibt es eine Liste typischer Schluesselbegriffe.
- Title + Description + Labels werden durchsucht.
- Das Fach mit dem hoechsten Score gewinnt; die Treffer werden als
  Begruendung mitgeliefert (nachvollziehbar fuer die Bewertung).

Hinweis: Die genauen Voll-Namen der Buendelungsfaecher (SDM/EvP/GiD) bitte
mit der Lehrkraft abgleichen - die Keyword-Regeln unten sind bewusst
leicht anpassbar gehalten.

Standardbibliothek only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

from role_a_ingest import UnifiedStory


# ---------------------------------------------------------------------------
# Regelwerk: Buendelungsfach -> typische Schluesselbegriffe
# ---------------------------------------------------------------------------
RULES: Dict[str, List[str]] = {
    # SDM - Schwerpunkt Daten / Datenmanagement / Persistenz
    "SDM": [
        "datenbank", "sql", "schema", "daten", "persistenz", "repository",
        "query", "migration", "modell", "tabelle", "speichern",
    ],
    # EvP - Schwerpunkt Programmierung / Logik / Backend
    "EvP": [
        "api", "endpunkt", "logik", "algorithmus", "funktion", "backend",
        "service", "berechnung", "klasse", "implementieren", "routing", "token",
    ],
    # GiD - Schwerpunkt Geschaeftsprozesse / Anforderungen / UI
    "GiD": [
        "prozess", "workflow", "anforderung", "ui", "oberflaeche", "dashboard",
        "kunde", "formular", "benutzer", "login", "reporting", "geschaeftsprozess",
    ],
}


@dataclass
class Recommendation:
    story: UnifiedStory
    subject: str               # SDM | EvP | GiD
    score: int                 # Anzahl Treffer fuer das gewaehlte Fach
    matched: List[str]         # welche Keywords getroffen haben
    scores: Dict[str, int]     # alle Fach-Scores (Transparenz)

    def to_dict(self) -> dict:
        return {
            **self.story.to_dict(),
            "recommendation": {
                "subject": self.subject,
                "score": self.score,
                "matched_keywords": self.matched,
                "all_scores": self.scores,
            },
        }


# ---------------------------------------------------------------------------
# Normalisierung
# ---------------------------------------------------------------------------
def normalize(story: UnifiedStory) -> UnifiedStory:
    """Vereinheitlicht Whitespace, Kleinschreibung der Labels, etc."""
    story.title = re.sub(r"\s+", " ", story.title).strip()
    story.description = re.sub(r"\s+", " ", story.description).strip()
    story.labels = sorted({lbl.strip().lower() for lbl in story.labels if lbl.strip()})
    if story.estimate < 0:
        story.estimate = 0
    return story


# ---------------------------------------------------------------------------
# Regelbasierte Klassifikation
# ---------------------------------------------------------------------------
def classify(story: UnifiedStory) -> Recommendation:
    haystack = " ".join([story.title, story.description, " ".join(story.labels)]).lower()

    scores: Dict[str, int] = {}
    matched_per_subject: Dict[str, List[str]] = {}
    for subject, keywords in RULES.items():
        hits = [kw for kw in keywords if kw in haystack]
        scores[subject] = len(hits)
        matched_per_subject[subject] = hits

    # Gewinner bestimmen (bei Gleichstand: feste Reihenfolge SDM > EvP > GiD)
    best_subject = max(scores, key=lambda s: (scores[s], -list(RULES).index(s)))

    # Fallback, wenn gar nichts trifft
    if scores[best_subject] == 0:
        best_subject = "GiD"  # Default: Anforderungen/Prozess

    return Recommendation(
        story=story,
        subject=best_subject,
        score=scores[best_subject],
        matched=matched_per_subject[best_subject],
        scores=scores,
    )


def process(stories: List[UnifiedStory]) -> List[Recommendation]:
    """Komplette Pipeline der Rolle B: normalisieren + klassifizieren."""
    return [classify(normalize(s)) for s in stories]


# Schnelltest: python3 role_b_logic.py
if __name__ == "__main__":
    import os
    from role_a_ingest import load_all

    here = os.path.join(os.path.dirname(__file__), "data")
    for rec in process(load_all(here)):
        print(f"{rec.story.id:8} -> {rec.subject}  (Treffer: {rec.matched})")

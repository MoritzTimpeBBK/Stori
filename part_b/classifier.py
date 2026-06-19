"""
Rolle B - Logik: normalisieren + regelbasiert klassifizieren
============================================================
Verbraucht UniStori-Objekte aus Part A und liefert Recommendation-Objekte,
die Part C dann per API ausgibt.

Das Verfahren ist bewusst TRANSPARENT (Keyword-Scoring, keine KI):
- Titel + Beschreibung werden in Kleinbuchstaben durchsucht.
- Pro Fach wird gezaehlt, wie viele Keywords vorkommen (= score).
- Das Fach mit dem hoechsten Score gewinnt. Die Treffer werden als
  Begruendung mitgeliefert - nachvollziehbar fuer die Bewertung.
"""

from dataclasses import dataclass

from part_a.models.unistori import UniStori
from part_b.rules import RULES, TIEBREAK_ORDER, DEFAULT_SUBJECT


@dataclass
class Recommendation:
    story: UniStori
    subject: str            # SDM | EvP | GiD
    score: int              # Anzahl Treffer fuer das gewaehlte Fach
    matched: list[str]      # welche Keywords getroffen haben (Begruendung)
    scores: dict[str, int]  # alle Fach-Scores (volle Transparenz)

    def to_dict(self) -> dict:
        return {
            "id": self.story.id,
            "name": self.story.name,
            "beschreibung": self.story.beschreibung,
            "empfehlung": {
                "fach": self.subject,
                "score": self.score,
                "treffer": self.matched,
                "alle_scores": self.scores,
            },
        }


def classify(story: UniStori) -> Recommendation:
    """Ordnet eine einzelne Story einem Buendelungsfach zu."""
    haystack = f"{story.name} {story.beschreibung}".lower()

    scores: dict[str, int] = {}
    matched_per_subject: dict[str, list[str]] = {}
    for subject, keywords in RULES.items():
        hits = [kw for kw in keywords if kw in haystack]
        scores[subject] = len(hits)
        matched_per_subject[subject] = hits

    # Gewinner: hoechster Score; bei Gleichstand entscheidet TIEBREAK_ORDER.
    best = max(TIEBREAK_ORDER, key=lambda s: (scores[s], -TIEBREAK_ORDER.index(s)))

    # Fallback, wenn gar nichts getroffen hat.
    if scores[best] == 0:
        best = DEFAULT_SUBJECT

    return Recommendation(
        story=story,
        subject=best,
        score=scores[best],
        matched=matched_per_subject[best],
        scores=scores,
    )


def classify_all(stories: list[UniStori]) -> list[Recommendation]:
    """Komplette Pipeline der Rolle B fuer eine Liste von Stories."""
    return [classify(s) for s in stories]

"""
Rolle A - Datenquellen & Ingest
================================

Aufgabe: User Stories aus heterogenen Quellen (CSV, JSON, optional XML)
einlesen und in ein EINHEITLICHES Modell (UnifiedStory) ueberfuehren.

Die Quelldateien benutzen absichtlich unterschiedliche Feldnamen
(z. B. "Aufgabe" vs. "title" vs. "name") - genau das ist die
"Heterogenitaet", die hier aufgeloest wird.

Standardbibliothek only - kein pip install noetig.
"""

from __future__ import annotations

import csv
import json
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from typing import List


# ---------------------------------------------------------------------------
# Einheitliches Modell - darauf einigen sich alle drei Rollen
# ---------------------------------------------------------------------------
@dataclass
class UnifiedStory:
    id: str
    title: str
    description: str
    labels: List[str] = field(default_factory=list)
    estimate: int = 0
    status: str = "unknown"
    source: str = "unknown"

    def to_dict(self) -> dict:
        return asdict(self)


def _split_labels(raw: str) -> List[str]:
    """Hilfsfunktion: 'ui,login' -> ['ui', 'login']."""
    if not raw:
        return []
    return [token.strip().lower() for token in raw.split(",") if token.strip()]


# ---------------------------------------------------------------------------
# CSV  (simulierter Microsoft-Planner-Export, Semikolon-getrennt)
# ---------------------------------------------------------------------------
def load_csv(path: str) -> List[UnifiedStory]:
    stories: List[UnifiedStory] = []
    with open(path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for index, row in enumerate(reader, start=1):
            stories.append(
                UnifiedStory(
                    id=f"CSV-{index}",
                    title=row.get("Aufgabe", "").strip(),
                    description=row.get("Beschreibung", "").strip(),
                    labels=_split_labels(row.get("Labels", "")),
                    estimate=int(row.get("Aufwand") or 0),
                    status=row.get("Prioritaet", "").strip().lower() or "unknown",
                    source="csv",
                )
            )
    return stories


# ---------------------------------------------------------------------------
# JSON  (simulierter GitHub-Issues-Export)
# ---------------------------------------------------------------------------
def load_json(path: str) -> List[UnifiedStory]:
    stories: List[UnifiedStory] = []
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    for item in data:
        labels = [lbl.get("name", "").lower() for lbl in item.get("labels", [])]
        stories.append(
            UnifiedStory(
                id=f"GH-{item.get('number')}",
                title=item.get("title", "").strip(),
                description=item.get("body", "").strip(),
                labels=labels,
                estimate=int(item.get("estimate") or 0),
                status=item.get("state", "unknown"),
                source="json",
            )
        )
    return stories


# ---------------------------------------------------------------------------
# XML  (simulierter Export aus aelterem Projekttool) - optional
# ---------------------------------------------------------------------------
def load_xml(path: str) -> List[UnifiedStory]:
    stories: List[UnifiedStory] = []
    tree = ET.parse(path)
    for node in tree.getroot().findall("story"):
        stories.append(
            UnifiedStory(
                id=node.get("id", "XML-?"),
                title=(node.findtext("name") or "").strip(),
                description=(node.findtext("text") or "").strip(),
                labels=_split_labels(node.findtext("tags") or ""),
                estimate=int(node.findtext("points") or 0),
                status=(node.findtext("state") or "unknown").strip(),
                source="xml",
            )
        )
    return stories


# ---------------------------------------------------------------------------
# Sammelt alle Quellen aus dem data/-Ordner ein
# ---------------------------------------------------------------------------
def load_all(data_dir: str) -> List[UnifiedStory]:
    stories: List[UnifiedStory] = []
    csv_path = os.path.join(data_dir, "stories.csv")
    json_path = os.path.join(data_dir, "stories.json")
    xml_path = os.path.join(data_dir, "stories.xml")

    if os.path.exists(csv_path):
        stories += load_csv(csv_path)
    if os.path.exists(json_path):
        stories += load_json(json_path)
    if os.path.exists(xml_path):
        stories += load_xml(xml_path)
    return stories


# Schnelltest: python3 role_a_ingest.py
if __name__ == "__main__":
    here = os.path.join(os.path.dirname(__file__), "data")
    for s in load_all(here):
        print(f"[{s.source:4}] {s.id:8} | {s.title}  (labels={s.labels})")

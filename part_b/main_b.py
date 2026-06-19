"""
Rolle B - Demo / Schnelltest
============================
Laedt die Stories ueber Part A, klassifiziert sie und gibt das Ergebnis aus.

Start (aus dem Projekt-Root):
    python part_b/main_b.py
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from part_a.models.unistori import UniStori
from part_a.main_a import load_unistories_from_csv, load_unistories_from_json
from part_b.classifier import classify_all


# Beispiel-Stories fuer Hardware / Netzwerk (Systemintegration -> EvP).
# Nur fuer die Demo, damit die neuen Hardware-Keywords sichtbar greifen.
HARDWARE_BEISPIELE = [
    UniStori(
        id=901,
        name="Defekten Switch im Serverraum tauschen",
        beschreibung="Netzwerk-Switch im Rechenzentrum ausbauen, neuen Switch "
                     "einbauen und Ports neu verkabeln.",
    ),
    UniStori(
        id=902,
        name="Firewall-Regeln am Gateway konfigurieren",
        beschreibung="Firewall am Gateway einrichten und das Netzwerk gegen "
                     "Zugriffe von aussen absichern.",
    ),
    UniStori(
        id=903,
        name="Router und Access-Point einrichten",
        beschreibung="Neuen Router konfigurieren, WLAN Access-Point anbinden "
                     "sowie DHCP und DNS einstellen.",
    ),
]


if __name__ == "__main__":
    data_dir = PROJECT_ROOT / "data"

    stories = load_unistories_from_csv(str(data_dir / "stories.csv"))
    stories += load_unistories_from_json(str(data_dir / "stories.json"))
    stories += HARDWARE_BEISPIELE

    for rec in classify_all(stories):
        print(f"[{rec.subject}] {rec.story.name}")
        print(f"    score {rec.score}, treffer: {rec.matched}")

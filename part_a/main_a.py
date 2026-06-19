from pathlib import Path
import sys
 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
 
from part_a.loader.json_loader import load_json
from part_a.mapper.json_mapper import map_github_issues
from part_a.loader.csv_loader import load_csv
from part_a.mapper.csv_mapper import map_csv
 
 
def load_unistories_from_json(path: str):
    raw = load_json(path)
    return map_github_issues(raw)
 
 
def load_unistories_from_csv(path: str):
    raw = load_csv(path)
    return map_csv(raw)
 
 
if __name__ == "__main__":
    # 🔹 Format auswählen
    source_type = "csv"  # "json" oder "csv"
 
    if source_type == "json":
        stories = load_unistories_from_json("data/stories.json")
 
    elif source_type == "csv":
        stories = load_unistories_from_csv("data\stories.csv")
 
    else:
        raise ValueError("Unbekannter Datentyp")
 
    for s in stories:
        print(s)
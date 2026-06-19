from pathlib import Path
import sys
 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
 
from part_a.loader.json_loader import load_json
from part_a.mapper.json_mapper import map_github_issues
from part_a.loader.csv_loader import load_csv
from part_a.mapper.csv_mapper import map_csv
# evtl. später noch für XML liefern
 
 
def load_unistories_from_json(path: str):
    raw = load_json(path)
    return map_github_issues(raw)
 
 
def load_unistories_from_csv(path: str):
    raw = load_csv(path)
    return map_csv(raw)


def get_all_uni_stories(source_type: str):
    if source_type == "json":
        return load_unistories_from_json("data/stories.json")
 
    if source_type == "csv":
        return load_unistories_from_csv("data/stories.csv")
        
    if source_type == "xml":
        # return load_unistories_from_xml("data/stories.xml") #noch nicht vorhanden
        pass
 
    raise ValueError(f"Unbekannter Datentyp: {source_type}")
 
 
if __name__ == "__main__":
    # 🔹 Hier kannst du jetzt flexibel "json", "csv" (oder später "xml") eintragen:
    wahl = "csv" 
 
    try:
        stories = get_all_uni_stories(wahl)
        for s in stories:
            print(s)
    except ValueError as e:
        print(e)
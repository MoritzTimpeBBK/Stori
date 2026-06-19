# mapper/csv_mapper.py
from part_a.models.unistori import UniStori
from part_a.utils.text_utils import normalize
 
def map_csv(rows: list[list[str]]) -> list[UniStori]:
    result: list[UniStori] = []
 
    for row in rows:
        if len(row) < 3:
            continue  # ungültiger Datensatz
 
        unistori = UniStori(
            id=int(row[0]),
            name=normalize(row[1]),
            beschreibung=normalize(row[2])
        )
        result.append(unistori)
 
    return result
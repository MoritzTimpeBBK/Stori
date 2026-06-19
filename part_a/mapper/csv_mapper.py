# mapper/csv_mapper.py
from part_a.models.unistori import UniStori
from part_a.utils.text_utils import normalize
 
def map_csv(rows: list[list[str]]) -> list[UniStori]:
    result: list[UniStori] = []

    for i, row in enumerate(rows[1:], start=1):  # skip header row
        if len(row) < 3:
            continue

        unistori = UniStori(
            id=i,
            name=normalize(row[0]),
            beschreibung=normalize(row[1])
        )
        result.append(unistori)

    return result
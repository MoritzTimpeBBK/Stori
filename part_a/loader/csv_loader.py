import csv
from typing import list

def load_csv(path: str) -> list[list[str]]:
    import csv
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
    return list(reader)
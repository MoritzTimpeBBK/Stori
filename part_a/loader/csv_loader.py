import csv

def load_csv(path: str) -> list[list[str]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        return list(reader)

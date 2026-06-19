# mapper/json_mapper.py
from part_a.models.unistori import UniStori
 
def map_github_issues(data: list[dict]) -> list[UniStori]:
    result: list[UniStori] = []
 
    for issue in data:
        unistori = UniStori(
            id=int(issue["number"]),
            name=issue["title"].strip(),
            beschreibung=issue["body"].strip() if issue.get("body") else ""
        )
        result.append(unistori)
 
    return result
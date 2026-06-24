"""
Rolle C - REST-API (FastAPI) fuer User Stories
==============================================
Stellt CRUD-Endpunkte fuer User Stories bereit und nutzt die regelbasierte
Klassifizierung aus Part B (classifier.classify) fuer die Fach-Zuordnung
(SDM / EvP / GiD) gemaess der Regelidee aus dem Buendelungsfaecher-Dokument.

Endpunkte:
    GET    /userstories                  - alle Stories (mit optionalen Filtern)
    GET    /userstories/{id}             - einzelne Story
    POST   /userstories                  - neue Story anlegen
    PUT    /userstories/{id}             - Story aktualisieren
    DELETE /userstories/{id}             - Story loeschen
    GET    /userstories/{id}/zuordnung   - Fach-Zuordnung berechnen

Start (aus dem Projekt-Root):
    uvicorn part_c.api:app --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from part_a.models.unistori import UniStori
from part_a.main_a import get_all_uni_stories
from part_b.classifier import classify
from part_b.rules import TIEBREAK_ORDER


# ---------------------------------------------------------------------------
# Pydantic-Schemas (Request/Response)
# ---------------------------------------------------------------------------
GUELTIGE_FAECHER = set(TIEBREAK_ORDER)  # {"SDM", "EvP", "GiD"}


class StoryOut(BaseModel):
    """Repraesentation einer User Story nach aussen."""
    id: int
    name: str
    beschreibung: str


class StoryCreate(BaseModel):
    """Body zum Anlegen einer Story. id ist optional (wird sonst vergeben)."""
    id: Optional[int] = Field(default=None, description="Optional; wird sonst automatisch vergeben")
    name: str = Field(..., min_length=1)
    beschreibung: str = Field(default="")


class StoryUpdate(BaseModel):
    """Body zum Aktualisieren. Alle Felder optional (Teil-Update)."""
    name: Optional[str] = Field(default=None, min_length=1)
    beschreibung: Optional[str] = None


class EmpfehlungOut(BaseModel):
    fach: str
    score: int
    treffer: list[str]
    alle_scores: dict[str, int]


class ZuordnungOut(BaseModel):
    id: int
    name: str
    beschreibung: str
    empfehlung: EmpfehlungOut


# ---------------------------------------------------------------------------
# In-Memory-Store
# ---------------------------------------------------------------------------
# Bewusst einfach gehalten: ein dict id -> UniStori. Beim Start werden die
# vorhandenen Stories aus Part A (CSV + JSON) geladen. Spaeter laesst sich das
# durch eine echte Persistenz (Repository) ersetzen, ohne die Endpunkte zu
# aendern.
class StoryStore:
    def __init__(self) -> None:
        self._items: dict[int, UniStori] = {}
        self._next_id: int = 1

    def bootstrap(self) -> None:
        """Laedt die vorhandenen Stories aus Part A (best effort)."""
        geladen: list[UniStori] = []
        for quelle in ("csv", "json"):
            try:
                geladen.extend(get_all_uni_stories(quelle))
            except Exception:
                # Quelle (Datei) evtl. nicht vorhanden - kein Abbruch.
                pass
        for s in geladen:
            self._items[s.id] = s
        if self._items:
            self._next_id = max(self._items) + 1

    def clear(self) -> None:
        """Leert den Store (v.a. fuer Tests)."""
        self._items.clear()
        self._next_id = 1

    def list(self) -> list[UniStori]:
        return list(self._items.values())

    def get(self, story_id: int) -> Optional[UniStori]:
        return self._items.get(story_id)

    def exists(self, story_id: int) -> bool:
        return story_id in self._items

    def add(self, name: str, beschreibung: str, story_id: Optional[int] = None) -> UniStori:
        if story_id is None:
            story_id = self._next_id
        if story_id in self._items:
            raise ValueError(f"Story mit id {story_id} existiert bereits")
        story = UniStori(id=story_id, name=name, beschreibung=beschreibung)
        self._items[story_id] = story
        self._next_id = max(self._next_id, story_id + 1)
        return story

    def update(self, story_id: int, name: Optional[str], beschreibung: Optional[str]) -> UniStori:
        story = self._items[story_id]
        if name is not None:
            story.name = name
        if beschreibung is not None:
            story.beschreibung = beschreibung
        return story

    def delete(self, story_id: int) -> None:
        del self._items[story_id]


store = StoryStore()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Stories aus Part A (CSV + JSON) in den Store laden.
    store.bootstrap()
    yield
    # Shutdown: nichts aufzuraeumen (In-Memory-Store).


app = FastAPI(
    title="User Story API (Buendelungsfaecher)",
    version="1.0.0",
    description="CRUD fuer User Stories + regelbasierte Fach-Zuordnung (SDM/EvP/GiD).",
    lifespan=lifespan,
)


def _to_out(story: UniStori) -> StoryOut:
    return StoryOut(id=story.id, name=story.name, beschreibung=story.beschreibung)


# ---------------------------------------------------------------------------
# GET /userstories - alle Stories, mit optionalen Filtern
# ---------------------------------------------------------------------------
@app.get("/userstories", response_model=list[StoryOut], tags=["userstories"])
def list_stories(
    q: Optional[str] = Query(
        default=None,
        description="Volltextfilter (Teilstring in Name oder Beschreibung, case-insensitive)",
    ),
    fach: Optional[str] = Query(
        default=None,
        description="Filter nach berechnetem Buendelungsfach: SDM | EvP | GiD",
    ),
):
    """Liefert alle Stories. Optional gefiltert nach Freitext und/oder Fach.

    Hinweis: Der Fach-Filter berechnet die Zuordnung on-the-fly ueber den
    Klassifizierer aus Part B - es wird nichts persistent gespeichert.
    """
    if fach is not None and fach not in GUELTIGE_FAECHER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ungueltiges Fach '{fach}'. Erlaubt: {sorted(GUELTIGE_FAECHER)}",
        )

    ergebnis = store.list()

    if q:
        nadel = q.lower()
        ergebnis = [
            s for s in ergebnis
            if nadel in s.name.lower() or nadel in s.beschreibung.lower()
        ]

    if fach:
        ergebnis = [s for s in ergebnis if classify(s).subject == fach]

    return [_to_out(s) for s in ergebnis]


# ---------------------------------------------------------------------------
# GET /userstories/{id} - einzelne Story
# ---------------------------------------------------------------------------
@app.get("/userstories/{story_id}", response_model=StoryOut, tags=["userstories"])
def get_story(story_id: int):
    story = store.get(story_id)
    if story is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story mit id {story_id} nicht gefunden",
        )
    return _to_out(story)


# ---------------------------------------------------------------------------
# POST /userstories - neue Story anlegen
# ---------------------------------------------------------------------------
@app.post(
    "/userstories",
    response_model=StoryOut,
    status_code=status.HTTP_201_CREATED,
    tags=["userstories"],
)
def create_story(payload: StoryCreate):
    try:
        story = store.add(
            name=payload.name,
            beschreibung=payload.beschreibung,
            story_id=payload.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return _to_out(story)


# ---------------------------------------------------------------------------
# PUT /userstories/{id} - Story aktualisieren
# ---------------------------------------------------------------------------
@app.put("/userstories/{story_id}", response_model=StoryOut, tags=["userstories"])
def update_story(story_id: int, payload: StoryUpdate):
    if not store.exists(story_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story mit id {story_id} nicht gefunden",
        )
    story = store.update(story_id, payload.name, payload.beschreibung)
    return _to_out(story)


# ---------------------------------------------------------------------------
# DELETE /userstories/{id} - Story loeschen
# ---------------------------------------------------------------------------
@app.delete(
    "/userstories/{story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["userstories"],
)
def delete_story(story_id: int):
    if not store.exists(story_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story mit id {story_id} nicht gefunden",
        )
    store.delete(story_id)
    return None


# ---------------------------------------------------------------------------
# GET /userstories/{id}/zuordnung - Fach-Zuordnung berechnen
# ---------------------------------------------------------------------------
@app.get(
    "/userstories/{story_id}/zuordnung",
    response_model=ZuordnungOut,
    tags=["zuordnung"],
)
def get_zuordnung(story_id: int):
    """Berechnet die Fach-Zuordnung (SDM/EvP/GiD) fuer eine Story.

    Nutzt den transparenten Keyword-Klassifizierer aus Part B. Die Antwort
    enthaelt das gewaehlte Fach, den Score, die getroffenen Keywords
    (Begruendung) und alle Fach-Scores zur vollen Nachvollziehbarkeit.
    """
    story = store.get(story_id)
    if story is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story mit id {story_id} nicht gefunden",
        )
    rec = classify(story)
    # classifier.Recommendation.to_dict() liefert bereits exakt diese Struktur.
    return rec.to_dict()

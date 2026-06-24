"""
Rolle C - Tests fuer die REST-API
=================================
Deckt alle sechs Endpunkte ab: Happy Path + Fehlerfaelle (400/404/409).

Start (aus dem Projekt-Root):
    pytest part_c/test_api.py -v

Die Tests sind isoliert: Vor jedem Test wird der In-Memory-Store geleert und
mit drei festen Beispiel-Stories befuellt. Dadurch sind die Tests unabhaengig
von den Dateien unter data/.
"""

from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from part_a.models.unistori import UniStori
from part_c import api as api_module
from part_c.api import app, store


# --- Test-Fixtures ---------------------------------------------------------

SEED = [
    UniStori(id=1, name="Login-Maske bauen",
             beschreibung="Benutzer-Oberflaeche fuer den Login, Doku fuer Anwender."),
    UniStori(id=2, name="SQL-Query optimieren",
             beschreibung="Datenbank Query refactoren, Schema anpassen."),
    UniStori(id=3, name="Server deployen",
             beschreibung="Deployment ueber Docker-Container auf den Server."),
]


@pytest.fixture(autouse=True)
def fresh_store():
    """Setzt den Store vor jedem Test auf einen bekannten Stand."""
    store.clear()
    for s in SEED:
        store.add(name=s.name, beschreibung=s.beschreibung, story_id=s.id)
    yield
    store.clear()


@pytest.fixture
def client():
    # KEIN Context-Manager -> startup-Bootstrap wird uebersprungen,
    # damit unser fresh_store-Seed nicht ueberschrieben wird.
    return TestClient(app)


# --- GET /userstories ------------------------------------------------------

def test_list_all(client):
    r = client.get("/userstories")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_list_filter_q(client):
    r = client.get("/userstories", params={"q": "query"})
    assert r.status_code == 200
    ids = [s["id"] for s in r.json()]
    assert ids == [2]


def test_list_filter_q_case_insensitive(client):
    r = client.get("/userstories", params={"q": "LOGIN"})
    assert r.status_code == 200
    assert [s["id"] for s in r.json()] == [1]


def test_list_filter_fach(client):
    r = client.get("/userstories", params={"fach": "SDM"})
    assert r.status_code == 200
    assert [s["id"] for s in r.json()] == [2]


def test_list_filter_fach_evp(client):
    r = client.get("/userstories", params={"fach": "EvP"})
    assert r.status_code == 200
    assert [s["id"] for s in r.json()] == [3]


def test_list_filter_fach_invalid(client):
    r = client.get("/userstories", params={"fach": "XXX"})
    assert r.status_code == 400


# --- GET /userstories/{id} -------------------------------------------------

def test_get_one(client):
    r = client.get("/userstories/1")
    assert r.status_code == 200
    assert r.json()["name"] == "Login-Maske bauen"


def test_get_one_missing(client):
    r = client.get("/userstories/999")
    assert r.status_code == 404


# --- POST /userstories -----------------------------------------------------

def test_create_autoid(client):
    payload = {"name": "Neue Story", "beschreibung": "Irgendwas mit code."}
    r = client.post("/userstories", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Neue Story"
    assert body["id"] == 4  # naechste freie ID nach 1,2,3


def test_create_with_id(client):
    payload = {"id": 42, "name": "Mit ID", "beschreibung": "Test."}
    r = client.post("/userstories", json=payload)
    assert r.status_code == 201
    assert r.json()["id"] == 42


def test_create_duplicate_id(client):
    payload = {"id": 1, "name": "Doppelt", "beschreibung": "Test."}
    r = client.post("/userstories", json=payload)
    assert r.status_code == 409


def test_create_missing_name(client):
    # name fehlt -> Pydantic-Validierung 422
    r = client.post("/userstories", json={"beschreibung": "ohne name"})
    assert r.status_code == 422


# --- PUT /userstories/{id} -------------------------------------------------

def test_update(client):
    r = client.put("/userstories/1", json={"name": "Geaenderter Titel"})
    assert r.status_code == 200
    assert r.json()["name"] == "Geaenderter Titel"
    # Beschreibung bleibt erhalten (Teil-Update)
    assert "Login" in r.json()["beschreibung"]


def test_update_both_fields(client):
    r = client.put("/userstories/2",
                   json={"name": "Neu", "beschreibung": "Neue Beschreibung."})
    assert r.status_code == 200
    assert r.json()["name"] == "Neu"
    assert r.json()["beschreibung"] == "Neue Beschreibung."


def test_update_missing(client):
    r = client.put("/userstories/999", json={"name": "x"})
    assert r.status_code == 404


# --- DELETE /userstories/{id} ----------------------------------------------

def test_delete(client):
    r = client.delete("/userstories/1")
    assert r.status_code == 204
    # danach nicht mehr auffindbar
    assert client.get("/userstories/1").status_code == 404


def test_delete_missing(client):
    r = client.delete("/userstories/999")
    assert r.status_code == 404


# --- GET /userstories/{id}/zuordnung ---------------------------------------

def test_zuordnung_sdm(client):
    r = client.get("/userstories/2/zuordnung")
    assert r.status_code == 200
    body = r.json()
    assert body["empfehlung"]["fach"] == "SDM"
    assert body["empfehlung"]["score"] > 0
    assert isinstance(body["empfehlung"]["treffer"], list)
    assert set(body["empfehlung"]["alle_scores"]) == {"SDM", "EvP", "GiD"}


def test_zuordnung_evp(client):
    r = client.get("/userstories/3/zuordnung")
    assert r.status_code == 200
    assert r.json()["empfehlung"]["fach"] == "EvP"


def test_zuordnung_gid(client):
    r = client.get("/userstories/1/zuordnung")
    assert r.status_code == 200
    assert r.json()["empfehlung"]["fach"] == "GiD"


def test_zuordnung_missing(client):
    r = client.get("/userstories/999/zuordnung")
    assert r.status_code == 404

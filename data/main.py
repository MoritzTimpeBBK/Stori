"""
main.py - Einstiegspunkt fuer das gesamte Team
==============================================

Verkettet die drei Rollen:
  Rolle A (role_a_ingest)  -> liest CSV/JSON/XML
  Rolle B (role_b_logic)   -> normalisiert + ordnet SDM/EvP/GiD zu
  Rolle C (role_c_api)     -> stellt alles per REST-API bereit

Starten:   python3 main.py
Dann im Browser oder per curl:  http://127.0.0.1:8000/recommendations
"""

from role_c_api import run

if __name__ == "__main__":
    run()

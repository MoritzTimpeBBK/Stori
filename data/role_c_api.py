"""
Rolle C - API
=============

Aufgabe: Die normalisierten Daten + Empfehlungen per REST-API bereitstellen.

Bewusst OHNE Framework gebaut (nur http.server aus der Standardbibliothek),
damit das Projekt ueberall sofort startet - kein pip install noetig.

Endpunkte:
  GET /                  -> Uebersicht / Hilfe
  GET /health            -> Healthcheck
  GET /stories           -> alle normalisierten Stories
  GET /stories/<id>      -> eine Story per ID
  GET /recommendations   -> alle Stories inkl. Fach-Empfehlung (SDM/EvP/GiD)
  GET /summary           -> Zaehlung pro Buendelungsfach
"""

from __future__ import annotations

import json
import os
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from role_a_ingest import load_all
from role_b_logic import process


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def build_payload():
    """Fuehrt Rolle A (Ingest) + Rolle B (Logik) zusammen und cached das Ergebnis."""
    stories = load_all(DATA_DIR)
    recommendations = process(stories)
    return recommendations


class Handler(BaseHTTPRequestHandler):
    # Daten einmal beim Start aufbauen (Klassen-Attribut)
    recommendations = build_payload()

    def _send(self, obj, status: int = 200):
        body = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        # Schlanke Konsolen-Ausgabe
        print(f"  > {self.command} {self.path}")

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/") or "/"

        if path == "/":
            self._send({
                "service": "User-Story Mapping Service (Abschlussprojekt LF8)",
                "endpoints": [
                    "/health", "/stories", "/stories/<id>",
                    "/recommendations", "/summary",
                ],
            })

        elif path == "/health":
            self._send({"status": "ok", "stories_loaded": len(self.recommendations)})

        elif path == "/stories":
            self._send([rec.story.to_dict() for rec in self.recommendations])

        elif path.startswith("/stories/"):
            story_id = path.split("/stories/", 1)[1]
            for rec in self.recommendations:
                if rec.story.id.lower() == story_id.lower():
                    self._send(rec.story.to_dict())
                    return
            self._send({"error": f"Story '{story_id}' nicht gefunden"}, status=404)

        elif path == "/recommendations":
            self._send([rec.to_dict() for rec in self.recommendations])

        elif path == "/summary":
            counter = Counter(rec.subject for rec in self.recommendations)
            self._send({
                "total": len(self.recommendations),
                "per_subject": dict(counter),
            })

        else:
            self._send({"error": f"Unbekannter Pfad: {path}"}, status=404)


def run(host: str = "127.0.0.1", port: int = 8000):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"API laeuft auf http://{host}:{port}  (Strg+C zum Beenden)")
    print(f"Geladene Stories: {len(Handler.recommendations)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestoppt.")
        server.shutdown()


if __name__ == "__main__":
    run()

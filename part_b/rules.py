"""
Rolle B - Regelwerk (nur die Keyword-Listen)
=============================================
Hier stehen NUR die Schluesselbegriffe je Buendelungsfach. Die Logik liegt in
classifier.py. So koennt ihr Keywords ergaenzen/streichen, ohne Code anzufassen.

Buendelungsfaecher (Team-Definition):
  SDM - Coding / Softwareentwicklung
  EvP - Systemintegration & Administration
  GiD - Gestaltung von IT-Dienstleistungen (Kunde, Doku, Bedienung)

Hinweis zur Suche: Es wird per Teilstring (substring) gesucht und alles in
Kleinbuchstaben. "implementier" trifft also implementieren/implementierung/
implementiert. Kurze Begriffe wie "ui" oder "api" koennen unbeabsichtigt in
anderen Woertern stecken - beim Review ruhig kritisch pruefen.
"""

RULES: dict[str, list[str]] = {
    # SDM - Coding / Softwareentwicklung
    "SDM": [
        "code", "quellcode", "programm", "funktion", "methode", "klasse",
        "objekt", "algorithmus", "logik", "implementier", "refactor",
        "refaktor", "debug", "schleife", "variable", "datenstruktur",
        "datenmodell", "modell", "schema", "query", "sql", "parsing",
        "parsen", "mapping", "datenbank", "persistenz", "repository",
        "migration", "unit-test", "exception", "bibliothek", "modul",
        "speichern",
    ],
    # EvP - Systemintegration & Administration
    "EvP": [
        "api", "rest", "endpunkt", "schnittstelle", "integration", "webhook",
        "deploy", "deployment", "server", "netzwerk", "konfiguration",
        "config", "infrastruktur", "pipeline", "ci/cd", "docker", "container",
        "automatisier", "hosting", "installation", "installier",
        "administration", "admin", "backup", "monitoring", "betrieb",
        "anbindung", "datenaustausch", "http", "microservice", "routing",
        "service", "backend", "workflow",
        # Hardware / Netzwerk (Systemintegration)
        "switch", "router", "firewall", "gateway", "proxy", "loadbalancer",
        "hardware", "kabel", "verkabelung", "patchpanel", "rechenzentrum",
        "serverraum", "wlan", "vlan", "dns", "dhcp", "accesspoint",
        "access-point", "usv", "nas", "san", "rack",
    ],
    # GiD - Gestaltung von IT-Dienstleistungen (Kunde, Doku, Bedienung)
    "GiD": [
        "kunde", "kunden", "nutzer", "benutzer", "anwender", "anforderung",
        "dokumentation", "doku", "anleitung", "handbuch", "readme",
        "oberflaeche", "ui", "maske", "usability", "bedienung", "uebergabe",
        "schulung", "support", "beratung", "dashboard", "darstellung",
        "reporting", "formular", "praesentation", "abnahme",
        "geschaeftsprozess", "prozess", "workshop", "stakeholder", "login",
    ],
}

# Fach mit dem hoechsten Score gewinnt. Bei Gleichstand entscheidet diese
# Reihenfolge (oben = bevorzugt).
TIEBREAK_ORDER = ["SDM", "EvP", "GiD"]

# Wenn KEIN einziges Keyword trifft, faellt die Story hierauf zurueck.
DEFAULT_SUBJECT = "GiD"

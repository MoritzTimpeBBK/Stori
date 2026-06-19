# "Normalisiert" unsauberen Text mit unnötigen Leerzeichen. BEISPIEL:  " Hallo " -> "Hallo"
    # Wird bei der CSV wichtig

def normalize(text: str) -> str:
    return " ".join(text.strip().split())
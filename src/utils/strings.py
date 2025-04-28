import re

def normalize_key(title: str) -> str:
    """Convert a human title into snake_case without accents."""
    s = (title.lower()
         .replace("á","a").replace("é","e")
         .replace("í","i").replace("ó","o")
         .replace("ú","u").replace("ñ","n"))
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")

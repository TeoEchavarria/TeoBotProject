# diagram_fetcher_v3.py
import base64, requests, re
from typing import List

UA = {"User-Agent": "DiagramFetcher/0.5 (tu-mail@ejemplo.com)"}

def _api_url(lang: str) -> str:
    return (
        "https://commons.wikimedia.org/w/api.php"
        if lang == "commons"
        else f"https://{lang}.wikipedia.org/w/api.php"
    )

# ----------------------------------------------------------------------
# 1. --- BÚSQUEDA -------------------------------------------------------
# ----------------------------------------------------------------------

def _search_files(query: str, limit: int, wiki: str) -> List[str]:
    """Devuelve hasta `limit` títulos de archivo (namespace 6)."""
    params = dict(
        action="query", format="json", list="search",
        srnamespace=6, srlimit=limit, srsearch=query
    )
    r = requests.get(_api_url(wiki), params=params, headers=UA, timeout=15)
    r.raise_for_status()
    return [hit["title"] for hit in r.json()["query"]["search"]]

def _first_good_title(keywords: str, wiki: str) -> str:
    """
    Estrategia: comenzar pidiendo palabras ≥4 caracteres; si no hay
    resultados, subir el umbral (≤8). Máx. 4 tokens por búsqueda.
    """
    min_len = 4
    max_tokens = 4
    while max_tokens > 0:
        min_len = 4  # Reset min_len for each max_tokens value
        while min_len <= 8:
            tokens = [w for w in re.split(r"\W+", keywords) if len(w) >= min_len][:max_tokens]
            if not tokens:                 # sin tokens útiles; relajar filtro
                min_len += 1
                continue
            query = " ".join(tokens)
            titles = _search_files(query, 10, wiki)
            if titles:                     # éxito
                return titles[0]
            min_len += 1
        max_tokens -= 1  # Reduce number of tokens when min_len exceeds 8
    return None

# ----------------------------------------------------------------------
# 2. --- METADATOS Y DESCARGA ------------------------------------------
# ----------------------------------------------------------------------

def _image_url(title: str, wiki: str, thumb: int) -> str:
    ii_params = {
        "action": "query", "format": "json", "prop": "imageinfo",
        "titles": title, "iiprop": "url",
    }
    if thumb:
        ii_params["iiurlwidth"] = thumb   # miniatura optimizada
    r = requests.get(_api_url(wiki), params=ii_params, headers=UA, timeout=10)
    r.raise_for_status()
    info = next(iter(r.json()["query"]["pages"].values()))["imageinfo"][0]
    return info["thumburl"] if thumb else info["url"]

# ----------------------------------------------------------------------
# 3. --- FUNCIÓN PÚBLICA -----------------------------------------------
# ----------------------------------------------------------------------

def search_diagram(
    keywords: str,
    *,
    wiki: str = "commons",
    thumb_width: int = 1024
) -> str:
    """
    Devuelve la primera imagen relevante —codificada en Base-64— para
    `keywords`, obtenida de la wiki indicada.
    """
    title = _first_good_title(keywords, wiki)
    if not title:
        return None
    url = _image_url(title, wiki, thumb_width)
    content =  requests.get(url, timeout=10).content
    if "DOCTYPE" in content.decode("utf-8"):
        return None
    return base64.b64encode(content).decode("utf-8")

if __name__ == "__main__":
    # Test the function
    keywords = "lagrange"
    img_path = search_diagram(keywords)
    print(f"Image path: {img_path}")
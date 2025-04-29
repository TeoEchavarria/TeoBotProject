import os 
from typing import Any, Dict, List
from googleapiclient.discovery import build  # type: ignore

def youtube_search(
    query: str,
    *,
    max_results: int = 1,
    safe_search: str = None,
    published_after: str = None,
    language: str = None,
) -> List[Dict[str, Any]]:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Define YOUTUBE_API_KEY env var before calling youtube_search()")

    youtube = build("youtube", "v3", developerKey=api_key)

    # Filter the query: split by spaces, remove words with <4 letters, limit to 7 words
    words = query.split()
    filtered_words = [word for word in words if len(word) >= 4]
    filtered_words = filtered_words[:4]  # Limit to 7 words
    filtered_query = " ".join(filtered_words)
    
    query = filtered_query  # Replace original query with filtered version
    # Build API request parameters
    request_kwargs: Dict[str, Any] = {
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results,
    }
    if safe_search:
        request_kwargs["safeSearch"] = safe_search
    if published_after:
        request_kwargs["publishedAfter"] = published_after
    if language:
        request_kwargs["relevanceLanguage"] = language

    response = youtube.search().list(**request_kwargs).execute()

    results: List[Dict[str, Any]] = []
    for item in response.get("items", []):
        vid_id = item["id"].get("videoId")
        snippet = item["snippet"]
        results.append(
            {
                "title": snippet.get("title"),
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "description": snippet.get("description"),
                "channel": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt"),
            }
        )
    return results
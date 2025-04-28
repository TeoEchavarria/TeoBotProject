import os 
from typing import Any, Dict, List
from googleapiclient.discovery import build  # type: ignore

def youtube_search(
    query: str,
    *,
    max_results: int = 1,
    safe_search: str | None = None,
    published_after: str | None = None,
    language: str | None = None,
) -> List[Dict[str, Any]]:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Define YOUTUBE_API_KEY env var before calling youtube_search()")

    youtube = build("youtube", "v3", developerKey=api_key)

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

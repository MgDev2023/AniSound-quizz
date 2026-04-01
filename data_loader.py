"""
data_loader.py — AnimeThemes + Jikan API fetching (genre & era based)
"""

import time
import random
from typing import Optional, List, Dict, Tuple

import requests

ANIMETHEMES_BASE = "https://api.animethemes.moe"
JIKAN_BASE       = "https://api.jikan.moe/v4"
AUDIO_BASE       = "https://v.animethemes.moe"

# Jikan genre ID map
GENRE_MAP: Dict[str, int] = {
    "Action":        1,
    "Adventure":     2,
    "Comedy":        4,
    "Drama":         8,
    "Fantasy":       10,
    "Horror":        14,
    "Mystery":       17,
    "Romance":       22,
    "Sci-Fi":        24,
    "Slice of Life": 36,
    "Sports":        30,
    "Supernatural":  37,
}

GENRES = list(GENRE_MAP.keys())

# Era name → (start_date, end_date) for Jikan
TIMELINE_MAP: Dict[str, Tuple[str, str]] = {
    "70s & Earlier": ("1960-01-01", "1979-12-31"),
    "80s Classics":  ("1980-01-01", "1989-12-31"),
    "90s Classics":  ("1990-01-01", "1999-12-31"),
    "2000s Era":     ("2000-01-01", "2009-12-31"),
    "2010s Era":     ("2010-01-01", "2019-12-31"),
    "2020s Era":     ("2020-01-01", "2029-12-31"),
}

ERAS = ["All Eras"] + list(TIMELINE_MAP.keys())

# Anime format/system map  →  Jikan 'type' param value
SYSTEM_MAP: Dict[str, Optional[str]] = {
    "All Types":  None,
    "TV Series":  "tv",
    "Movies":     "movie",
    "OVA":        "ova",
    "ONA":        "ona",
    "Specials":   "special",
}

SYSTEMS = list(SYSTEM_MAP.keys())


# ─── Low-level HTTP ──────────────────────────────────────────────────────────────

def _get(url: str, params: dict = None, retries: int = 3) -> Optional[dict]:
    """GET with retry and backoff. Returns parsed JSON or None on failure."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=12)
            if resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
                continue
            resp.raise_for_status()
            return resp.json()
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.5)
    return None


# ─── Jikan fetchers ───────────────────────────────────────────────────────────────

def fetch_anime_by_genre(genre_id: int, page: int = 1, anime_type: str = None) -> List[Dict]:
    """Return up to 25 top-scored anime dicts from Jikan for the given genre."""
    time.sleep(0.4)
    params = {
        "genres":   str(genre_id),
        "order_by": "score",
        "sort":     "desc",
        "limit":    25,
        "page":     page,
    }
    if anime_type:
        params["type"] = anime_type
    data = _get(f"{JIKAN_BASE}/anime", params)
    if not data or not data.get("data"):
        return []
    return data["data"]


def fetch_anime_by_genre_and_era(genre_id: int, start_date: str, end_date: str,
                                  page: int = 1, anime_type: str = None) -> List[Dict]:
    """Return up to 25 top-scored anime dicts from Jikan filtered by genre AND date range."""
    time.sleep(0.4)
    params = {
        "genres":     str(genre_id),
        "start_date": start_date,
        "end_date":   end_date,
        "order_by":   "score",
        "sort":       "desc",
        "limit":      25,
        "page":       page,
    }
    if anime_type:
        params["type"] = anime_type
    data = _get(f"{JIKAN_BASE}/anime", params)
    if not data or not data.get("data"):
        return []
    return data["data"]


# ─── AnimeThemes ─────────────────────────────────────────────────────────────────

def search_theme_for_anime(anime_title: str) -> Optional[Dict]:
    """
    Search AnimeThemes for a theme entry matching the anime title.
    Returns one theme dict (chosen randomly from the top results) or None.
    """
    data = _get(f"{ANIMETHEMES_BASE}/search", {
        "q":                   anime_title,
        "fields[search]":      "animethemes",
        "include[animetheme]": "anime.images,animethemeentries.videos,song",
    })
    if not data:
        return None
    themes = (data.get("search") or {}).get("animethemes", [])
    if not themes:
        return None
    return random.choice(themes[:3])


# ─── Shared round builder ────────────────────────────────────────────────────────

def _build_rounds_from_pool(anime_pool: List[Dict], n: int) -> List[Dict]:
    """Given a shuffled pool of Jikan anime dicts, build up to n quiz rounds."""
    rounds: List[Dict] = []
    seen: set = set()

    for anime_data in anime_pool:
        if len(rounds) >= n:
            break

        try:
            anime_name = (anime_data.get("title") or "").strip()
            if not anime_name or anime_name in seen:
                continue

            theme = search_theme_for_anime(anime_name)
            if not theme:
                continue

            # ── Resolve audio URL ────────────────────────────────────────────
            basename = ""
            for entry in (theme.get("animethemeentries") or []):
                for video in (entry.get("videos") or []):
                    bn = (video.get("basename") or "").strip()
                    if bn:
                        basename = bn
                        break
                if basename:
                    break
            if not basename:
                continue

            audio_url = f"{AUDIO_BASE}/{basename}"

            # ── Poster from Jikan ────────────────────────────────────────────
            imgs = anime_data.get("images", {})
            poster_url = (
                imgs.get("jpg", {}).get("large_image_url")
                or imgs.get("jpg", {}).get("image_url")
                or imgs.get("webp", {}).get("large_image_url")
                or ""
            )
            if not poster_url:
                at_anime = theme.get("anime") or {}
                for img in (at_anime.get("images") or []):
                    link = img.get("link", "")
                    if link:
                        poster_url = link
                        break

            # ── Alternate titles ─────────────────────────────────────────────
            seen_titles = {anime_name.lower()}
            alt_titles: List[str] = []
            for t_obj in anime_data.get("titles", []):
                t = (t_obj.get("title") or "").strip()
                if t and t.lower() not in seen_titles:
                    seen_titles.add(t.lower())
                    alt_titles.append(t)
            for key in ("title_english", "title_japanese"):
                t = (anime_data.get(key) or "").strip()
                if t and t.lower() not in seen_titles:
                    seen_titles.add(t.lower())
                    alt_titles.append(t)

            genres = [g["name"] for g in anime_data.get("genres", []) if g.get("name")]
            score  = anime_data.get("score") or 0
            year   = anime_data.get("year") or ""

            seen.add(anime_name)
            rounds.append({
                "anime_name": anime_name,
                "audio_url":  audio_url,
                "song_name":  (theme.get("song") or {}).get("title") or "Unknown",
                "theme_type": theme.get("type") or "OP",
                "poster_url": poster_url,
                "alt_titles": alt_titles,
                "genres":     genres,
                "score":      score,
                "year":       year,
            })

        except Exception:
            continue

    return rounds


# ─── Public builders ─────────────────────────────────────────────────────────────

def build_quiz_rounds(genre: str = "Action", era: str = "All Eras",
                      system: str = "All Types", n: int = 10) -> List[Dict]:
    """
    Build n quiz rounds filtered by genre, era, and anime format (system).
    'All Eras' skips the date filter. 'All Types' skips the format filter.
    """
    genre_id   = GENRE_MAP.get(genre, 1)
    anime_type = SYSTEM_MAP.get(system)   # None means no type filter

    anime_pool: List[Dict] = []

    if era == "All Eras":
        for page in (1, 2):
            anime_pool.extend(fetch_anime_by_genre(genre_id, page=page, anime_type=anime_type))
            if len(anime_pool) >= n * 2:
                break
    else:
        start_date, end_date = TIMELINE_MAP.get(era, ("2010-01-01", "2019-12-31"))
        for page in (1, 2, 3):
            anime_pool.extend(fetch_anime_by_genre_and_era(
                genre_id, start_date, end_date, page=page, anime_type=anime_type
            ))
            if len(anime_pool) >= n * 2:
                break

    if not anime_pool:
        return []
    random.shuffle(anime_pool)
    return _build_rounds_from_pool(anime_pool, n)

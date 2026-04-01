"""
game_logic.py — Guess checking and scoring logic
"""

import difflib
import re
from typing import List, Tuple


# ─── Rank table (threshold = score out of 10) ────────────────────────────────────

RANKS: List[Tuple[int, str, str]] = [
    (10, "Anime Sage 🧙",         "A perfect score — every OP and ED lives rent-free in your head."),
    (9,  "Grand Otaku Master 👑",  "Nearly flawless. Have you watched 1000+ anime?"),
    (8,  "Seasoned Weeb 🌸",      "You clearly spend your evenings wisely. Impressive!"),
    (7,  "Anime Enthusiast ⭐",    "Solid score — you know your classics."),
    (6,  "Casual Fan 🎌",         "Not bad at all! A few more late nights and you'll level up."),
    (5,  "Halfway There 🎵",      "You know the bangers, but there's more to discover."),
    (4,  "Weekend Watcher 📺",    "You've dipped your toes in. Keep exploring!"),
    (3,  "Anime Newbie 🌱",       "Just getting started on the journey. Welcome!"),
    (2,  "Manga Reader 📚",       "Maybe try watching instead of just reading?"),
    (1,  "Curious Soul 👀",       "One point! At least you stayed for all 10 rounds."),
    (0,  "Future Anime Fan 🚀",   "Everyone starts somewhere. The adventure awaits!"),
]


# ─── String normalisation ────────────────────────────────────────────────────────

def _normalize(s: str) -> str:
    """Lowercase, strip punctuation, and collapse whitespace."""
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", "", s)   # remove punctuation
    s = re.sub(r"\s+", " ", s)      # collapse whitespace
    return s


# ─── Fuzzy match ─────────────────────────────────────────────────────────────────

def fuzzy_match(guess: str, target: str, threshold: float = 0.6) -> bool:
    """
    Return True if guess is sufficiently similar to target.
    Uses difflib.SequenceMatcher — threshold 0.6 forgives most typos.
    """
    g, t = _normalize(guess), _normalize(target)
    if not g or not t:
        return False
    ratio = difflib.SequenceMatcher(None, g, t).ratio()
    return ratio >= threshold


# ─── Public API ──────────────────────────────────────────────────────────────────

def check_guess(
    guess: str,
    correct_title: str,
    alt_titles: List[str] = None,
    threshold: float = 0.6,
) -> bool:
    """
    Return True if `guess` matches `correct_title` or any of `alt_titles`.
    Accepts slight typos via fuzzy matching (SequenceMatcher ≥ threshold).
    Also accepts partial matches: e.g. typing "Naruto" when the title
    is "Naruto: Shippuden" will pass if similarity ≥ threshold.
    """
    if not guess.strip():
        return False

    all_titles = [correct_title] + (alt_titles or [])
    return any(fuzzy_match(guess, t, threshold) for t in all_titles)


def get_rank(score: int, total: int = 10) -> Tuple[str, str]:
    """
    Return (rank_title, rank_description) based on score / total.
    Normalises to a 0-10 scale before looking up the rank.
    """
    normalised = round((score / total) * 10) if total > 0 else 0
    for threshold, title, desc in RANKS:
        if normalised >= threshold:
            return title, desc
    return RANKS[-1][1], RANKS[-1][2]

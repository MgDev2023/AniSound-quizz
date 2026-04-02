# 🎵 AniSound Quiz

Guess the anime from its OP/ED audio clip!

> Deployed on [Streamlit Cloud](https://streamlit.io/cloud)

## Features
- 12 genres (Action, Romance, Comedy, Drama, and more)
- 6 era filters (70s all the way to 2020s)
- 5 format types (TV Series, Movies, OVA, ONA, Specials)
- Fuzzy answer matching — typos are forgiven
- Skip button, Try Again, and View Answer options
- Per-round result summary with ranks

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io) |
| Audio & themes | [AnimeThemes API](https://animethemes.moe) |
| Anime metadata | [Jikan API](https://jikan.moe) |
| Fuzzy matching | Python `difflib.SequenceMatcher` |
| HTTP | `requests` |
| Deployment | [Streamlit Cloud](https://streamlit.io/cloud) |

## Project Structure

```
AniSound/
├── app.py            # Streamlit UI and game flow
├── data_loader.py    # API calls to AnimeThemes & Jikan
├── game_logic.py     # Fuzzy guess checking and rank logic
├── requirements.txt
└── README.md
```

## APIs & Credits

- **[AnimeThemes.moe](https://animethemes.moe)** — community-sourced anime OP/ED audio
- **[Jikan.moe](https://jikan.moe)** — unofficial MyAnimeList REST API (no key required)

Both APIs are free and require no authentication.

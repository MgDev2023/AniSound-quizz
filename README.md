# AniSound Quiz

A web-based quiz game where you listen to anime opening/ending theme songs and try to guess the anime title.

---

## What does it do?

The app plays a short audio clip from an anime theme. You type your guess and it tells you if you're right. It forgives typos too.

You can filter by:
- Genre (Action, Romance, Comedy, Drama, and more)
- Era (1970s to 2020s)
- Format (TV series, movies, OVA, etc.)

At the end of each round you get a score and rank.

---

## How it works

- Audio clips come from the **AnimeThemes API** (free, no key needed)
- Anime info (title, genre, year) comes from the **Jikan API** (unofficial MyAnimeList API, also free)
- Answer checking uses fuzzy matching so small typos don't count as wrong

---

## Tech used

- Python
- Streamlit (web app)
- AnimeThemes API (audio)
- Jikan API (anime data)
- difflib (fuzzy answer matching)

---

## How to run it locally

```bash
git clone https://github.com/MgDev2023/AniSound-quizz.git
cd AniSound-quizz
pip install -r requirements.txt
streamlit run app.py
```

---

## Project structure

```
AniSound-quizz/
├── app.py          ← main game UI
├── data_loader.py  ← fetches data from APIs
├── game_logic.py   ← handles scoring and answer checking
└── requirements.txt
```

---

## Made by

Megan — a fun side project combining my interest in anime with Python and API integration.

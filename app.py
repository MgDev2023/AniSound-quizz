"""
app.py — AniSound Quiz  |  Streamlit entry point
"""

import streamlit as st

from data_loader import build_quiz_rounds, GENRES, ERAS, SYSTEMS
from game_logic import check_guess, get_rank


@st.cache_data(show_spinner=False)
def _load_rounds(genre: str, era: str, system: str) -> list:
    return build_quiz_rounds(genre=genre, era=era, system=system, n=10)

# ─── Page config (must be first Streamlit call) ──────────────────────────────────
st.set_page_config(
    page_title="AniSound Quiz",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Background & layout ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #130a27 0%, #0d1b4b 55%, #130a27 100%);
    min-height: 100vh;
}
[data-testid="stHeader"]  { background: transparent; }
[data-testid="stSidebar"] {
    background: rgba(10, 4, 26, 0.97) !important;
    border-right: 1px solid rgba(180, 79, 255, 0.2);
}

/* ── Title ── */
.big-title {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #b44fff 0%, #ff5fcb 50%, #ffb347 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    letter-spacing: -1px;
    margin-bottom: 4px;
}
.tagline {
    text-align: center;
    color: #7a8fb5;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* ── Cards ── */
.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(180, 79, 255, 0.25);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.8rem 0;
    color: #e2e8f0;
}
.reveal-card {
    background: rgba(180, 79, 255, 0.07);
    border: 1px solid rgba(180, 79, 255, 0.45);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.8rem 0;
}

/* ── Feedback badges ── */
.correct-badge {
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid #22c55e;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    color: #4ade80;
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 0.8rem;
}
.wrong-badge {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid #ef4444;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    color: #f87171;
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 0.8rem;
}

/* ── Genre chips ── */
.chip {
    display: inline-block;
    background: rgba(180, 79, 255, 0.18);
    border: 1px solid rgba(180, 79, 255, 0.35);
    border-radius: 20px;
    padding: 2px 11px;
    font-size: 0.76rem;
    color: #cc88ff;
    margin: 2px 2px;
}

/* ── Results screen ── */
.score-giant {
    font-size: 5.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #b44fff, #ff5fcb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0.5rem 0;
}
.rank-name {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffb347;
    margin-top: 0.4rem;
}
.rank-desc {
    text-align: center;
    color: #7a8fb5;
    font-size: 0.95rem;
    margin-top: 4px;
    margin-bottom: 1.5rem;
}

/* ── In-game labels ── */
.round-label {
    font-size: 0.82rem;
    color: #7a8fb5;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.question-text {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0.4rem 0 1rem;
}
.anime-reveal-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #e2e8f0;
    margin-bottom: 2px;
}
.song-label {
    color: #b44fff;
    font-size: 0.9rem;
    margin-bottom: 4px;
}
.meta-label {
    color: #7a8fb5;
    font-size: 0.82rem;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Session state ───────────────────────────────────────────────────────────────

_DEFAULTS = {
    "phase": "welcome",         # welcome | loading | playing | finished
    "questions": [],
    "round": 0,
    "score": 0,
    "genre": "Action",
    "era": "All Eras",
    "system": "All Types",
    "round_phase": "guessing",  # guessing | wrong | correct | revealed
    "last_guess": "",
    "round_results": [],        # True/False per completed round
}

# Keys preserved across _reset() so the user's genre/era selection sticks
_PRESERVE = {"genre", "era", "system"}


def _init():
    for k, v in _DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset():
    for k in _DEFAULTS:
        if k not in _PRESERVE:
            st.session_state[k] = _DEFAULTS[k]


_init()
ss = st.session_state  # shorthand alias


# ─── Helpers ─────────────────────────────────────────────────────────────────────

def current_q():
    """Return the current round dict or None if out of bounds."""
    if ss.questions and ss.round < len(ss.questions):
        return ss.questions[ss.round]
    return None


def advance_round(correct: bool = False):
    ss.round_results.append(correct)
    ss.round += 1
    ss.round_phase = "guessing"
    ss.last_guess = ""
    if ss.round >= 10 or ss.round >= len(ss.questions):
        ss.phase = "finished"


def _chips(genres):
    if not genres:
        return ""
    return " ".join(f'<span class="chip">{g}</span>' for g in genres[:6])


def show_reveal(q: dict):
    """Render the answer card: poster + metadata."""
    col_img, col_info = st.columns([1, 2], gap="medium")

    with col_img:
        if q.get("poster_url"):
            st.image(q["poster_url"], use_container_width=True)
        else:
            st.markdown(
                '<div style="height:180px;background:rgba(180,79,255,0.1);'
                'border-radius:12px;display:flex;align-items:center;'
                'justify-content:center;color:#7a8fb5;">No Image</div>',
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            f'<div class="anime-reveal-title">{q["anime_name"]}</div>',
            unsafe_allow_html=True,
        )
        theme_label = q.get("theme_type", "OP")
        song = q.get("song_name", "Unknown")
        st.markdown(
            f'<div class="song-label">🎵 {theme_label} — {song}</div>',
            unsafe_allow_html=True,
        )

        meta_parts = []
        if q.get("year"):
            meta_parts.append(f"📅 {q['year']}")
        if q.get("score"):
            meta_parts.append(f"⭐ {q['score']:.1f} / 10")
        if meta_parts:
            st.markdown(
                f'<div class="meta-label">{" &nbsp;·&nbsp; ".join(meta_parts)}</div>',
                unsafe_allow_html=True,
            )

        if q.get("genres"):
            st.markdown(
                f'<div style="margin-top:8px">{_chips(q["genres"])}</div>',
                unsafe_allow_html=True,
            )


# ─── Sidebar ─────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎵 AniSound Quiz")
    st.markdown("---")

    if ss.phase == "welcome":
        genre = st.selectbox("Genre", GENRES,
                             index=GENRES.index(ss.genre) if ss.genre in GENRES else 0)
        ss.genre = genre

        era = st.selectbox("Era", ERAS,
                           index=ERAS.index(ss.era) if ss.era in ERAS else 0)
        ss.era = era

        system = st.selectbox("Format", SYSTEMS,
                              index=SYSTEMS.index(ss.system) if ss.system in SYSTEMS else 0)
        ss.system = system
    else:
        st.markdown(f"**Genre:** {ss.genre}")
        if ss.era != "All Eras":
            st.markdown(f"**Era:** {ss.era}")
        if ss.system != "All Types":
            st.markdown(f"**Format:** {ss.system}")

    if ss.phase in ("playing", "finished"):
        st.markdown("---")
        rounds_done = min(ss.round, 10)
        st.markdown(f"**Score:** {ss.score} / {rounds_done}")
        if ss.phase == "playing":
            st.markdown(f"**Round:** {ss.round + 1} / 10")

    st.markdown("---")
    if ss.phase != "welcome":
        if st.button("🏠 Quit to Menu", use_container_width=True):
            _reset()
            st.rerun()

    st.markdown(
        """
<div style="margin-top:2rem">
<small style="color:#444">
Powered by<br>
<a href="https://animethemes.moe" style="color:#b44fff">AnimeThemes.moe</a>
&nbsp;&&nbsp;
<a href="https://jikan.moe" style="color:#b44fff">Jikan API</a>
</small>
</div>
""",
        unsafe_allow_html=True,
    )


# ─── Welcome screen ───────────────────────────────────────────────────────────────

if ss.phase == "welcome":
    st.markdown('<div class="big-title">🎵 AniSound Quiz</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline">Listen to anime OPs & EDs — can you name the show?</div>',
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 2.2, 1])
    with mid:
        st.markdown(
            """
<div class="card">

**How to play:**

🎵 &nbsp;Listen to the audio clip

✍️ &nbsp;Type the anime name

✅ &nbsp;Score points for correct answers

🏆 &nbsp;See your rank after 10 rounds

&nbsp;

*Typos are forgiven — close enough counts!*
</div>
""",
            unsafe_allow_html=True,
        )
        if st.button("▶ &nbsp;Start Quiz", use_container_width=True, type="primary"):
            ss.phase = "loading"
            st.rerun()


# ─── Loading screen ───────────────────────────────────────────────────────────────

elif ss.phase == "loading":
    st.markdown('<div class="big-title">🎵 AniSound Quiz</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline">Fetching anime OSTs... hang tight! 🎶</div>',
        unsafe_allow_html=True,
    )

    era_label    = ss.era    if ss.era    != "All Eras"   else "all eras"
    system_label = ss.system if ss.system != "All Types"  else ""
    combo = f"{ss.genre} {system_label} anime from {era_label}".replace("  ", " ").strip()
    with st.spinner(f"Loading {combo}..."):
        questions = _load_rounds(ss.genre, ss.era, ss.system)

    if not questions:
        if ss.era != "All Eras" or ss.system != "All Types":
            st.error(
                f"No anime found for **{ss.genre}** / **{ss.era}** / **{ss.system}**. "
                "Try a different combination."
            )
        else:
            st.error(
                "Could not load anime data. Check your internet connection and try again."
            )
        if st.button("← Back to Menu"):
            _reset()
            st.rerun()
    else:
        ss.questions = questions
        ss.phase = "playing"
        st.rerun()


# ─── Playing screen ───────────────────────────────────────────────────────────────

elif ss.phase == "playing":
    q = current_q()
    if q is None:
        ss.phase = "finished"
        st.rerun()

    # Progress bar
    st.progress(ss.round / 10, text=f"Round {ss.round + 1} of 10")

    st.markdown(
        f'<div class="round-label">Round {ss.round + 1} &nbsp;/&nbsp; 10</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="question-text">🎵 &nbsp;What anime is this from?</div>',
        unsafe_allow_html=True,
    )

    # Audio player — always visible during the round
    st.audio(q["audio_url"])

    st.markdown("")

    # ── Guessing ─────────────────────────────────────────────────────────────────
    if ss.round_phase == "guessing":
        with st.form(key=f"guess_{ss.round}", clear_on_submit=True):
            guess = st.text_input(
                "Anime name",
                placeholder="Type the anime name and press Enter...",
                label_visibility="collapsed",
            )
            col_sub, col_skip = st.columns([3, 1])
            with col_sub:
                submitted = st.form_submit_button(
                    "Submit Guess", use_container_width=True, type="primary"
                )
            with col_skip:
                skipped = st.form_submit_button(
                    "⏭ Skip", use_container_width=True
                )

        if skipped:
            ss.round_phase = "revealed"
            st.rerun()
        elif submitted:
            if not guess.strip():
                st.warning("Please type a guess before submitting.")
            else:
                ss.last_guess = guess.strip()
                if check_guess(guess, q["anime_name"], q.get("alt_titles", [])):
                    ss.score += 1
                    ss.round_phase = "correct"
                else:
                    ss.round_phase = "wrong"
                st.rerun()

    # ── Wrong answer ──────────────────────────────────────────────────────────────
    elif ss.round_phase == "wrong":
        st.markdown(
            f'<div class="wrong-badge">✗ &nbsp;Not quite — you guessed: '
            f'<em>{ss.last_guess}</em></div>',
            unsafe_allow_html=True,
        )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Try Again", use_container_width=True):
                ss.round_phase = "guessing"
                ss.last_guess = ""
                st.rerun()
        with col_b:
            if st.button("👁 View Answer", use_container_width=True):
                ss.round_phase = "revealed"
                st.rerun()

    # ── Correct ───────────────────────────────────────────────────────────────────
    if ss.round_phase == "correct":
        st.markdown(
            '<div class="correct-badge">✓ &nbsp;Correct! Well done! +1 point</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="reveal-card">', unsafe_allow_html=True)
        show_reveal(q)
        st.markdown("</div>", unsafe_allow_html=True)

        label = "Next Round →" if ss.round < 9 else "See Results 🏆"
        if st.button(label, use_container_width=True, type="primary"):
            advance_round(correct=True)
            st.rerun()

    # ── Revealed (gave up / skipped) ──────────────────────────────────────────────
    elif ss.round_phase == "revealed":
        st.markdown('<div class="reveal-card">', unsafe_allow_html=True)
        show_reveal(q)
        st.markdown("</div>", unsafe_allow_html=True)

        label = "Next Round →" if ss.round < 9 else "See Results 🏆"
        if st.button(label, use_container_width=True):
            advance_round(correct=False)
            st.rerun()


# ─── Results screen ───────────────────────────────────────────────────────────────

elif ss.phase == "finished":
    st.markdown('<div class="big-title">🏆 Quiz Complete!</div>', unsafe_allow_html=True)

    total = min(len(ss.questions), 10)
    rank_title, rank_desc = get_rank(ss.score, total)

    st.markdown(
        f'<div class="score-giant">{ss.score}/{total}</div>', unsafe_allow_html=True
    )
    st.markdown(f'<div class="rank-name">{rank_title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rank-desc">{rank_desc}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Round Summary")

    for i, q in enumerate(ss.questions[:10]):
        got_it = ss.round_results[i] if i < len(ss.round_results) else False
        badge_color = "#4ade80" if got_it else "#f87171"
        badge_symbol = "✓" if got_it else "✗"
        st.markdown(
            f"<span style='color:{badge_color};font-weight:700'>{badge_symbol}</span> "
            f"**{i + 1}.** {q['anime_name']} "
            f"<small style='color:#7a8fb5'>— {q['theme_type']}: {q['song_name']}</small>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            _reset()
            st.rerun()

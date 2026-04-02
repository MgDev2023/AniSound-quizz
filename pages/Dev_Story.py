"""
pages/Dev_Story.py — AniSound Quiz | Behind the Build
Recruiter-facing page: skills, architecture, and development story.
"""

import streamlit as st

st.set_page_config(
    page_title="Behind the Build — AniSound",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #130a27 0%, #0d1b4b 55%, #130a27 100%);
    min-height: 100vh;
}
[data-testid="stHeader"]  { background: transparent; }
[data-testid="stSidebar"] {
    background: rgba(10, 4, 26, 0.97) !important;
    border-right: 1px solid rgba(180, 79, 255, 0.2);
}
.big-title {
    font-size: 2.8rem;
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
.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #cc88ff;
    margin-top: 2.4rem;
    margin-bottom: 0.7rem;
    border-left: 4px solid #b44fff;
    padding-left: 0.75rem;
}
.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(180, 79, 255, 0.25);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.7rem 0;
    color: #e2e8f0;
    line-height: 1.75;
}
.highlight-card {
    background: rgba(180, 79, 255, 0.07);
    border: 1px solid rgba(180, 79, 255, 0.45);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.7rem 0;
    color: #e2e8f0;
    line-height: 1.75;
}
.skill-group-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: #7a8fb5;
    font-weight: 700;
    margin-bottom: 6px;
}
.skill-pill {
    display: inline-block;
    background: rgba(180, 79, 255, 0.15);
    border: 1px solid rgba(180, 79, 255, 0.40);
    border-radius: 20px;
    padding: 4px 13px;
    font-size: 0.82rem;
    color: #cc88ff;
    margin: 3px 3px;
    font-weight: 600;
}
.skill-pill-green {
    display: inline-block;
    background: rgba(34, 197, 94, 0.10);
    border: 1px solid rgba(34, 197, 94, 0.35);
    border-radius: 20px;
    padding: 4px 13px;
    font-size: 0.82rem;
    color: #4ade80;
    margin: 3px 3px;
    font-weight: 600;
}
.skill-pill-orange {
    display: inline-block;
    background: rgba(255, 179, 71, 0.10);
    border: 1px solid rgba(255, 179, 71, 0.35);
    border-radius: 20px;
    padding: 4px 13px;
    font-size: 0.82rem;
    color: #ffb347;
    margin: 3px 3px;
    font-weight: 600;
}
.stat-box {
    background: rgba(180, 79, 255, 0.10);
    border: 1px solid rgba(180, 79, 255, 0.30);
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
}
.stat-num {
    font-size: 1.9rem;
    font-weight: 900;
    background: linear-gradient(90deg, #b44fff, #ff5fcb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.stat-label {
    color: #7a8fb5;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}
.decision-badge {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-bottom: 6px;
    margin-top: 10px;
}
.yes { color: #4ade80; }
.no  { color: #f87171; }
.dev-card {
    background: linear-gradient(135deg, rgba(180,79,255,0.10) 0%, rgba(255,95,203,0.06) 100%);
    border: 1px solid rgba(180, 79, 255, 0.40);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin: 0.8rem 0 1.6rem;
    color: #e2e8f0;
    line-height: 1.75;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎵 AniSound Quiz")
    st.markdown("---")
    st.markdown("""
<small style="color:#7a8fb5">
📄 You're reading the<br>
<strong style="color:#cc88ff">Behind the Build</strong> page.<br><br>
Use the navigation above<br>to switch pages.
</small>
""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
<div style="margin-top:1rem">
<small style="color:#444">
Powered by<br>
<a href="https://animethemes.moe" style="color:#b44fff">AnimeThemes.moe</a>
&nbsp;&&nbsp;
<a href="https://jikan.moe" style="color:#b44fff">Jikan API</a>
</small>
</div>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="big-title">🔬 Behind the Build</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">API integration · State machine design · Fuzzy matching · Live deployment</div>',
    unsafe_allow_html=True,
)

# ─── Developer Intro ─────────────────────────────────────────────────────────
st.markdown("""
<div class="dev-card">
  <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap; margin-bottom:1rem;">
    <span style="font-size:1.15rem; font-weight:800; color:#cc88ff;">👩‍💻 Megana</span>
    <span style="
      background: linear-gradient(90deg, #b44fff, #ff5fcb);
      color: #fff;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 4px 14px;
      border-radius: 20px;
      letter-spacing: 0.5px;
    ">🎯 Seeking: Junior ML Engineer</span>
  </div>
  <div style="color:#e2e8f0; line-height:1.75;">
    I built AniSound Quiz at the intersection of two things I care deeply about:
    writing clean Python and anime culture. This page walks through every technical
    decision behind the app — the architecture, the problems I hit, how I solved them,
    and what I learned along the way.
  </div>
  <div style="margin-top:1rem; padding:0.9rem 1.1rem; background:rgba(180,79,255,0.10); border-radius:10px; border-left: 3px solid #b44fff;">
    <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1.5px; color:#7a8fb5; font-weight:700; margin-bottom:4px;">What I'm looking for</div>
    <div style="color:#e2e8f0; line-height:1.65; font-size:0.95rem;">
      A <strong style="color:#cc88ff;">Junior Machine Learning Engineer</strong> role where I can apply
      Python, data pipelines, and algorithmic thinking to real ML problems —
      building on what this project taught me about API-driven data collection,
      similarity algorithms, and shipping end-to-end systems from scratch.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Skills at a Glance ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Skills Demonstrated in This Project</div>', unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown("""
<div class="card" style="min-height:130px;">
<div class="skill-group-title">Languages & Frameworks</div>
<span class="skill-pill">Python</span>
<span class="skill-pill">Streamlit</span>
<span class="skill-pill">HTML/CSS</span>
</div>
""", unsafe_allow_html=True)

with sc2:
    st.markdown("""
<div class="card" style="min-height:130px;">
<div class="skill-group-title">Backend & Data</div>
<span class="skill-pill-green">REST API Integration</span>
<span class="skill-pill-green">Caching</span>
<span class="skill-pill-green">Retry Logic</span>
<span class="skill-pill-green">Fuzzy Matching</span>
</div>
""", unsafe_allow_html=True)

with sc3:
    st.markdown("""
<div class="card" style="min-height:130px;">
<div class="skill-group-title">Engineering Practices</div>
<span class="skill-pill-orange">State Machine Design</span>
<span class="skill-pill-orange">Modular Architecture</span>
<span class="skill-pill-orange">Error Handling</span>
<span class="skill-pill-orange">Live Deployment</span>
</div>
""", unsafe_allow_html=True)

# ─── Project Stats ────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-box"><div class="stat-num">2</div><div class="stat-label">REST APIs Integrated</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-box"><div class="stat-num">3</div><div class="stat-label">Separated Modules</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-box"><div class="stat-num">0</div><div class="stat-label">API Keys Needed</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-box"><div class="stat-num">Live</div><div class="stat-label">Deployed on Streamlit Cloud</div></div>', unsafe_allow_html=True)

# ─── What Is AniSound ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">What Is AniSound?</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
<strong style="color:#cc88ff">AniSound Quiz</strong> is an audio-based anime guessing game.
Users listen to an anime opening or ending theme and type their best guess at the show's name.
Ten rounds, a forgiving fuzzy-match engine, genre/era/format filters, and an 11-tier rank system at the end.<br><br>
The idea came from a gap in the market: most anime quiz tools are outdated, ad-heavy, or need an account.
AniSound is intentionally frictionless — no login, no install, pick your genre and play in seconds.
</div>
""", unsafe_allow_html=True)

# ─── Architecture ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Architecture</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-card">
<strong style="color:#ffb347">Phase-based finite state machine</strong><br><br>
Because Streamlit re-executes the entire script on every user interaction,
traditional URL routing doesn't apply. The navigation is implemented as a state machine
via <code>st.session_state["phase"]</code>:<br><br>
<code style="color:#cc88ff;">welcome</code>
&nbsp;→&nbsp;
<code style="color:#ffb347;">loading</code>
&nbsp;→&nbsp;
<code style="color:#4ade80;">playing</code>
&nbsp;→&nbsp;
<code style="color:#ff5fcb;">finished</code>
<br><br>
Inside <code>playing</code>, a nested <code>round_phase</code> tracks each individual round:
<code>guessing</code> → <code>wrong / correct</code> → <code>revealed</code>.
Every button click updates a state key and calls <code>st.rerun()</code>.
The full app state is always visible in one dictionary — simple to debug, impossible to get into an invalid state.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<strong style="color:#ffb347">Modular code separation</strong><br><br>
The codebase is split into three focused modules so each concern can change independently:<br><br>
&nbsp;&nbsp;• &nbsp;<code>app.py</code> — UI rendering and state transitions <em>only</em><br>
&nbsp;&nbsp;• &nbsp;<code>data_loader.py</code> — all API calls, pagination, retries, and data assembly<br>
&nbsp;&nbsp;• &nbsp;<code>game_logic.py</code> — answer validation and rank calculation<br><br>
Changing the fuzzy match threshold doesn't touch the UI. Changing an API endpoint doesn't touch the scoring.
This separation also makes each module independently testable.
</div>
""", unsafe_allow_html=True)

# ─── Engineering Decisions ────────────────────────────────────────────────────
st.markdown('<div class="section-title">Engineering Decisions — What Changed and Why</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<strong style="color:#cc88ff">Answer validation: exact match → fuzzy matching</strong><br>
<div class="decision-badge no">❌ Problem</div>
The first implementation required the user's input to exactly match the stored title (case-insensitive).
Anime titles like <em>"Fullmetal Alchemist: Brotherhood"</em> or <em>"My Hero Academia"</em>
have many valid alternate forms, and even one typo marked correct answers as wrong.<br>
<div class="decision-badge yes">✓ Solution</div>
Replaced with Python's <code>difflib.SequenceMatcher</code> at a 0.6 similarity threshold.
The check runs against every known title for an anime — English, Japanese, romanized, and abbreviations
collected from both APIs — so "FMA", "Fullmetal Alchemist Brotherhood", or "鋼の錬金術師" all score as correct.
Input is normalized first: lowercased, punctuation stripped, whitespace collapsed.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<strong style="color:#cc88ff">Data loading: real-time fetch → cached pipeline</strong><br>
<div class="decision-badge no">❌ Problem</div>
Early versions fetched fresh data on every quiz start.
The two-API pipeline (search Jikan → cross-reference AnimeThemes) took 8–15 seconds per game.<br>
<div class="decision-badge yes">✓ Solution</div>
Wrapping <code>build_quiz_rounds()</code> with <code>@st.cache_data</code> caches results per filter combination.
Replaying with the same genre/era/format is instant. Different combinations each get their own cache entry
so variety is preserved without paying the fetch cost twice.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<strong style="color:#cc88ff">API reliability: crashes → graceful degradation</strong><br>
<div class="decision-badge no">❌ Problem</div>
Both APIs are public and sometimes slow or rate-limited. Early versions showed a raw Python
stack trace when any call failed — a broken experience that exposed implementation details.<br>
<div class="decision-badge yes">✓ Solution</div>
<code>data_loader.py</code> wraps every request in a retry loop with up to 3 attempts.
Rate-limit responses (HTTP 429) trigger exponential backoff — 2s, 4s, 8s — while other
failures wait a flat 1.5s before retrying. Each request also carries a 12-second timeout.
If an anime has no audio on AnimeThemes it is silently skipped and the next candidate is tried.
If no valid questions can be assembled, the user sees a clear error message with a filter
suggestion — never a raw exception.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<strong style="color:#cc88ff">Navigation: tab layout → multi-page architecture</strong><br>
<div class="decision-badge no">❌ Problem</div>
The first prototype used <code>st.tabs()</code> to separate the game view from an info panel.
The tab bar looked cluttered and the tabs rendered content lazily in ways that
broke the audio player's state between switches.<br>
<div class="decision-badge yes">✓ Solution</div>
Moved to Streamlit's native multi-page app model: a <code>pages/</code> folder where
each file is its own page with its own config. The game stays isolated in <code>app.py</code>.
Streamlit auto-generates the sidebar navigation with zero manual routing code.
</div>
""", unsafe_allow_html=True)

# ─── Engineering Challenges ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Engineering Challenges</div>', unsafe_allow_html=True)

ch1, ch2 = st.columns(2)
with ch1:
    st.markdown("""
<div class="card">
<strong style="color:#ffb347">🔗 Joining two independent APIs</strong><br><br>
AnimeThemes and Jikan share no common ID system.
The pipeline runs Jikan first to get a ranked pool of anime candidates,
then searches AnimeThemes by title for each one to find audio.
Because the title search can return near-matches, the code takes a
random pick from the top 3 AnimeThemes results to add variety
rather than always returning the same theme for popular shows.
</div>
""", unsafe_allow_html=True)

with ch2:
    st.markdown("""
<div class="card">
<strong style="color:#ffb347">🎵 Audio coverage gaps</strong><br><br>
Not every Jikan anime has a theme on AnimeThemes.
The data loader over-fetches — up to 50 Jikan candidates for "All Eras"
and up to 75 for a specific era (25 per page across 2–3 pages) —
then filters down to only those with a valid audio URL.
Titles with no audio are skipped silently so the player never sees a broken round.
</div>
""", unsafe_allow_html=True)

ch3, ch4 = st.columns(2)
with ch3:
    st.markdown("""
<div class="card">
<strong style="color:#ffb347">🖼 Missing poster images</strong><br><br>
Jikan's CDN returns 404s for some older titles.
Four image sources are tried in order: JPEG large, JPEG standard,
WebP large (all from Jikan), then the image embedded in the
AnimeThemes response as a final fallback.
If all four are empty, a styled "No Image" placeholder renders instead —
the reveal card never breaks visually.
</div>
""", unsafe_allow_html=True)

with ch4:
    st.markdown("""
<div class="card">
<strong style="color:#ffb347">🧩 Fuzzy match threshold tuning</strong><br><br>
The 0.6 similarity threshold was the most-iterated parameter in the project.
Below 0.55 and obviously wrong answers scored as correct.
Above 0.65 and correct answers with minor spelling differences were rejected.
0.6 was validated through repeated playtesting until the match felt
fair — not too strict, not too lenient.
</div>
""", unsafe_allow_html=True)

# ─── Why Anime Fans Love It ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Why Anime Fans Love It</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-card">
Anime openings and endings aren't just songs —
they are <strong style="color:#cc88ff">emotional timestamps</strong>.
Ask any fan to hum a theme from a show they watched at 12 and they'll do it note-perfect, years later.
AniSound is built on that phenomenon: the moment you hear two seconds of a familiar theme,
your brain doesn't just recognise the tune — it remembers exactly where you were when you first watched it.
<br><br>
The <strong>era filter</strong> quietly surfaces a generational gap: players who grew up in the 90s breeze
through Classics and struggle with 2020s titles, and vice versa.
<strong>Wrong answers</strong> are wins too — the reveal card turns every missed guess into a
potential next watch. And the <strong>rank system</strong> maps exactly to how the community
already talks about itself: every fan places themselves on the tier list without prompting,
which is what makes results worth sharing.
</div>
""", unsafe_allow_html=True)

# ─── Lessons Learned ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Lessons Learned</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<strong style="color:#cc88ff">1. Read the real API responses before writing any logic.</strong><br>
Every field that can be <code>null</code> will be <code>null</code> for some anime.
Assumptions about response shapes caused more bugs than any logic error.
Inspecting live API output first would have saved several debugging sessions.<br><br>

<strong style="color:#cc88ff">2. The user experience is the product.</strong><br>
The fuzzy threshold (0.6) was the single most-iterated parameter.
No unit test could have surfaced this — only playtesting did.
The "feel" of whether a match is fair requires a human, not a CI pipeline.<br><br>

<strong style="color:#cc88ff">3. Match the framework to the problem's actual shape.</strong><br>
Streamlit was the right call for a solo Python developer targeting a fast deployment.
Its constraints only bite at the edges — animation, audio continuity across rerenders —
well outside the core game loop. Choosing tools for the MVP you're building,
not the hypothetical v2, is nearly always the right move.<br><br>

<strong style="color:#cc88ff">4. Graceful failure is a feature, not an afterthought.</strong><br>
The app touches two public APIs, a CDN, and user-submitted text.
Any of these can fail at any time. Building every data path to degrade gracefully —
retries, fallbacks, friendly error messages — is what separates a prototype from
something you can actually put in front of people.
</div>
""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#555; font-size:0.85rem; padding: 1rem 0 2rem; line-height:2;">
Built by <strong style="color:#cc88ff">Megana</strong>
&nbsp;·&nbsp;
Powered by
<a href="https://animethemes.moe" style="color:#b44fff">AnimeThemes.moe</a>
&amp;
<a href="https://jikan.moe" style="color:#b44fff">Jikan API</a>
&nbsp;·&nbsp;
Deployed on
<a href="https://streamlit.io/cloud" style="color:#b44fff">Streamlit Cloud</a>
</div>
""", unsafe_allow_html=True)

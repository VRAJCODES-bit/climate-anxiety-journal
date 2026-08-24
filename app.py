"""
Climate Anxiety Journal
A private journaling and mood-tracking tool for processing climate anxiety,
paired with guided prompts, coping resources, and small actionable steps.
"""

import streamlit as st
import pandas as pd
import json
import os
import random
import time
from datetime import datetime, date

st.set_page_config(page_title="Climate Anxiety Journal", page_icon="🌍", layout="centered")

JOURNAL_FILE = "journal_data.json"
MOOD_FILE = "mood_data.json"
GRATITUDE_FILE = "gratitude_data.json"
STREAK_FILE = "streak_data.json"


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    return default


def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        st.warning("Could not save to disk — data will only persist for this session.")


if "journal" not in st.session_state:
    st.session_state.journal = load_json(JOURNAL_FILE, [])
if "moods" not in st.session_state:
    st.session_state.moods = load_json(MOOD_FILE, [])
if "gratitude" not in st.session_state:
    st.session_state.gratitude = load_json(GRATITUDE_FILE, [])
if "streak" not in st.session_state:
    st.session_state.streak = load_json(STREAK_FILE, {"count": 0, "last_visit": None})

# ---------------------------
# Streak logic (visit-based, no guilt if broken)
# ---------------------------
today_str = date.today().isoformat()
last_visit = st.session_state.streak.get("last_visit")

if last_visit != today_str:
    if last_visit is not None:
        last_date = datetime.fromisoformat(last_visit).date()
        gap = (date.today() - last_date).days
        if gap == 1:
            st.session_state.streak["count"] += 1
        elif gap > 1:
            st.session_state.streak["count"] = 1
    else:
        st.session_state.streak["count"] = 1
    st.session_state.streak["last_visit"] = today_str
    save_json(STREAK_FILE, st.session_state.streak)

streak_count = st.session_state.streak["count"]

st.title("🌍 Climate Anxiety Journal")
st.caption("A judgment-free zone to dump your climate feels. No cap, just vibes and healing.")

col_a, col_b = st.columns([3, 1])
with col_b:
    if streak_count > 0:
        st.metric("🔥 Streak", f"{streak_count}d")

st.info(
    "💙 This is a self-reflection tool, not therapy-in-a-box. If you're really struggling, "
    "a real therapist or counselor is worth it. Climate Mental Health Network (climatementalhealth.net) "
    "is a solid place to start."
)

CLIMATE_WINS = [
    "🌞 Solar power is now the cheapest source of electricity in most of the world.",
    "🐋 Humpback whale populations have rebounded significantly since whaling bans.",
    "🌳 The ozone layer is genuinely healing — projected to fully recover by ~2066.",
    "⚡ India's renewable energy capacity has grown massively over the past decade.",
    "🦅 The bald eagle went from endangered to a full comeback story in the US.",
    "🚲 More cities are adding bike lanes and car-free zones every year.",
    "🌊 Ocean cleanup projects have removed millions of kg of plastic and counting.",
    "🌱 Reforestation projects worldwide have planted billions of trees this decade.",
]

if "daily_win" not in st.session_state or st.session_state.get("win_date") != today_str:
    st.session_state.daily_win = random.choice(CLIMATE_WINS)
    st.session_state.win_date = today_str

st.success(f"**Climate W of the Day:** {st.session_state.daily_win}")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Journal", "😮‍💨 Vibe Check", "🌬️ Breathe", "🌱 Small Wins", "💛 Real Talk / Resources"
])

# ---------------------------
# TAB 1: Journal
# ---------------------------
with tab1:
    st.subheader("Brain dump zone")

    PROMPTS = [
        "What's one climate-related worry that's been living rent-free in your head?",
        "When did you last feel a lil hopeful about the environment? What sparked it?",
        "What's something small you did today that actually aligned with your values?",
        "If you could send one text to someone in power about climate change, what would it say?",
        "What does 'doing enough' even mean, and is that a fair bar to hold yourself to?",
        "Name one thing outside that gave you a moment of peace recently.",
        "What feels heaviest right now — and what feels lightest?",
        "Who or what makes you feel less alone in all this?",
        "Rant mode: what's something climate-related that's just making you mad rn?",
        "What's one thing you wish more people understood about how you feel?",
    ]

    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = random.choice(PROMPTS)

    st.markdown(f"**Today's prompt:** _{st.session_state.current_prompt}_")
    if st.button("🎲 Nah, gimme a different prompt"):
        st.session_state.current_prompt = random.choice(PROMPTS)
        st.rerun()

    entry_text = st.text_area("Write whatever's real — this stays on your device only.", height=200)

    if st.button("💾 Save this entry"):
        if entry_text.strip():
            st.session_state.journal.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "prompt": st.session_state.current_prompt,
                "entry": entry_text.strip(),
            })
            save_json(JOURNAL_FILE, st.session_state.journal)
            st.success("Saved. Proud of you for showing up. ✨")
        else:
            st.warning("Write something first, or just sit with it for a sec — that counts too.")

    if st.session_state.journal:
        st.markdown("---")
        st.markdown(f"### Your past entries ({len(st.session_state.journal)} total)")
        for entry in reversed(st.session_state.journal[-10:]):
            with st.expander(f"{entry['date']} — {entry['prompt'][:50]}..."):
                st.write(entry["entry"])

        journal_text = "\n\n---\n\n".join(
            f"{e['date']}\nPrompt: {e['prompt']}\n\n{e['entry']}" for e in st.session_state.journal
        )
        st.download_button(
            "⬇️ Export your entries",
            data=journal_text,
            file_name="climate_journal_export.txt",
            mime="text/plain",
        )

# ---------------------------
# TAB 2: Mood / Vibe Check
# ---------------------------
with tab2:
    st.subheader("Vibe check: how ya doin?")

    mood_score = st.slider("Climate vibes today (1 = rough, 10 = at peace)", 1, 10, 5)

    mood_tags = st.multiselect(
        "Pick whatever's hitting right now:",
        [
            "Lowkey spiraling", "Numb tbh", "Kinda mad", "Cautiously optimistic",
            "Anxious", "Actually motivated", "Grieving", "Determined",
            "Just tired", "Curious", "In my feels", "Weirdly okay today",
        ],
    )

    if st.button("💾 Log today's vibe"):
        st.session_state.moods.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": mood_score,
            "tags": mood_tags,
        })
        save_json(MOOD_FILE, st.session_state.moods)
        st.success("Logged. Thanks for checking in with yourself. 🫶")

    if st.session_state.moods:
        st.markdown("---")
        st.markdown("### Your vibe over time")
        mood_df = pd.DataFrame(st.session_state.moods)
        st.line_chart(mood_df.set_index("date")["score"])

        all_tags = [tag for entry in st.session_state.moods for tag in entry.get("tags", [])]
        if all_tags:
            tag_counts = pd.Series(all_tags).value_counts()
            st.markdown("**Your most-logged feelings:**")
            st.bar_chart(tag_counts)

        avg_score = mood_df["score"].mean()
        st.markdown("---")
        st.markdown("### 📋 Your Mood Card")
        st.markdown(f"""
        > **{len(st.session_state.moods)} check-ins** · **{avg_score:.1f}/10 avg vibe** · **{streak_count} day streak** 🔥
        """)
    else:
        st.caption("No vibes logged yet — check in above whenever you're ready.")

# ---------------------------
# TAB 3: Breathing Exercise
# ---------------------------
with tab3:
    st.subheader("Okay, let's just breathe for a sec")
    st.write("Box breathing: in for 4, hold for 4, out for 4, hold for 4. Repeat as needed.")

    if st.button("▶️ Start (30ish seconds)"):
        placeholder = st.empty()
        phases = [("Breathe in...", 4), ("Hold...", 4), ("Breathe out...", 4), ("Hold...", 4)]
        for _ in range(2):
            for label, duration in phases:
                for remaining in range(duration, 0, -1):
                    placeholder.markdown(f"## {label} {remaining}")
                    time.sleep(1)
        placeholder.markdown("## 🌿 Nice. You did that.")

    st.caption("Run it back as many times as you need.")

# ---------------------------
# TAB 4: Small Actions
# ---------------------------
with tab4:
    st.subheader("Small stuff that actually helps")
    st.write(
        "Taking small, real actions can genuinely ease climate anxiety — it's about feeling less stuck, "
        "not solving everything single-handedly (that was never your job anyway)."
    )

    actions = [
        "Fire off a message to a local rep about something you care about",
        "Spend 10 minutes outside noticing what's still thriving nearby",
        "Send a friend one accurate, non-doom climate fact",
        "Throw a few bucks or an hour at a local environmental org",
        "Cut one single-use thing out of your week",
        "Actually tell someone how you're feeling about this stuff",
        "Look up a conservation project happening near you",
    ]

    if "today_action" not in st.session_state:
        st.session_state.today_action = random.choice(actions)

    st.markdown(f"### Today's mini-quest: {st.session_state.today_action}")
    if st.button("🎲 Different quest please"):
        st.session_state.today_action = random.choice(actions)
        st.rerun()

    st.markdown("---")
    st.markdown("### 💛 Hope Log")
    st.write("One thing — big or tiny — that gave you hope today.")

    gratitude_text = st.text_input("Today I felt hopeful about...")
    if st.button("💾 Save to hope log"):
        if gratitude_text.strip():
            st.session_state.gratitude.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "entry": gratitude_text.strip(),
            })
            save_json(GRATITUDE_FILE, st.session_state.gratitude)
            st.success("Saved. Hold onto that. ✨")

    if st.session_state.gratitude:
        st.markdown(f"**Recent hopeful moments ({len(st.session_state.gratitude)} logged):**")
        for g in reversed(st.session_state.gratitude[-5:]):
            st.write(f"- {g['date']}: {g['entry']}")

# ---------------------------
# TAB 5: Resources
# ---------------------------
with tab5:
    st.subheader("Real talk & real resources")
    st.write("These are legit, established resources — not a replacement for professional care, but a solid start.")

    st.markdown("""
    - **[Climate Mental Health Network](https://www.climatementalhealth.net/)** — resources specifically for eco-anxiety and climate distress
    - **[Good Grief Network](https://www.goodgriefnetwork.org/)** — peer support for processing climate/environmental grief
    - **[Psychology Today Therapist Finder](https://www.psychologytoday.com/us/therapists)** — find a licensed therapist near you
    - **[Force of Nature](https://forceofnature.xyz/)** — youth-focused climate action and mental health resources
    """)

    st.markdown("---")
    st.warning(
        "If you're having thoughts of self-harm or you're in crisis, please reach out right now: "
        "in the US, call or text **988** (Suicide & Crisis Lifeline). In India, contact **iCall** at "
        "**9152987821** or **AASRA** at **9820466726**. Outside these regions, search for your local "
        "crisis helpline. You deserve support — this isn't a big ask, reach out."
    )
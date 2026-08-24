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
from datetime import datetime

st.set_page_config(page_title="Climate Anxiety Journal", page_icon="🌍", layout="centered")

JOURNAL_FILE = "journal_data.json"
MOOD_FILE = "mood_data.json"
GRATITUDE_FILE = "gratitude_data.json"


def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        st.warning("Could not save to disk — data will only persist for this session.")


if "journal" not in st.session_state:
    st.session_state.journal = load_json(JOURNAL_FILE)
if "moods" not in st.session_state:
    st.session_state.moods = load_json(MOOD_FILE)
if "gratitude" not in st.session_state:
    st.session_state.gratitude = load_json(GRATITUDE_FILE)

st.title("🌍 Climate Anxiety Journal")
st.caption("A quiet space to process how you're feeling about the climate — privately, at your own pace.")

st.info(
    "💙 This is a self-reflection tool, not a substitute for professional support. "
    "If you're struggling, reaching out to a therapist or counselor can help. "
    "The Climate Mental Health Network (climatementalhealth.net) is a good starting point."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Journal", "😔 Mood Tracker", "🌬️ Breathe", "🌱 Small Actions", "💛 Resources"
])

# ---------------------------
# TAB 1: Journal
# ---------------------------
with tab1:
    st.subheader("Guided Journal")

    PROMPTS = [
        "What's one climate-related worry that's been on your mind lately?",
        "When did you last feel a sense of hope about the environment? What sparked it?",
        "What's something small you did today that aligned with your values?",
        "If you could tell someone in power one thing about climate change, what would it be?",
        "What does 'doing enough' mean to you, and is that a fair standard?",
        "Name one thing outside that brought you a moment of peace recently.",
        "What feels heaviest right now — and what feels lightest?",
        "Who or what community makes you feel less alone in this?",
    ]

    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = random.choice(PROMPTS)

    st.markdown(f"**Today's prompt:** _{st.session_state.current_prompt}_")
    if st.button("🔄 Get a different prompt"):
        st.session_state.current_prompt = random.choice(PROMPTS)
        st.rerun()

    entry_text = st.text_area("Write freely — this stays on your device only.", height=200)

    if st.button("💾 Save journal entry"):
        if entry_text.strip():
            st.session_state.journal.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "prompt": st.session_state.current_prompt,
                "entry": entry_text.strip(),
            })
            save_json(JOURNAL_FILE, st.session_state.journal)
            st.success("Entry saved.")
        else:
            st.warning("Write something before saving, or just take the time to reflect — that counts too.")

    if st.session_state.journal:
        st.markdown("---")
        st.markdown("### Past Entries")
        for entry in reversed(st.session_state.journal[-10:]):
            with st.expander(f"{entry['date']} — {entry['prompt'][:50]}..."):
                st.write(entry["entry"])

        journal_text = "\n\n---\n\n".join(
            f"{e['date']}\nPrompt: {e['prompt']}\n\n{e['entry']}" for e in st.session_state.journal
        )
        st.download_button(
            "⬇️ Export all entries as text file",
            data=journal_text,
            file_name="climate_journal_export.txt",
            mime="text/plain",
        )

# ---------------------------
# TAB 2: Mood Tracker
# ---------------------------
with tab2:
    st.subheader("How are you feeling today?")

    mood_score = st.slider("Overall mood about climate issues (1 = very distressed, 10 = at peace)", 1, 10, 5)

    mood_tags = st.multiselect(
        "Any of these resonate right now?",
        ["Overwhelmed", "Numb", "Angry", "Hopeful", "Anxious", "Motivated", "Grieving", "Determined", "Tired", "Curious"],
    )

    if st.button("💾 Log today's mood"):
        st.session_state.moods.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": mood_score,
            "tags": mood_tags,
        })
        save_json(MOOD_FILE, st.session_state.moods)
        st.success("Mood logged.")

    if st.session_state.moods:
        st.markdown("---")
        st.markdown("### Your Mood Over Time")
        mood_df = pd.DataFrame(st.session_state.moods)
        st.line_chart(mood_df.set_index("date")["score"])

        all_tags = [tag for entry in st.session_state.moods for tag in entry.get("tags", [])]
        if all_tags:
            tag_counts = pd.Series(all_tags).value_counts()
            st.markdown("**Most common feelings logged:**")
            st.bar_chart(tag_counts)
    else:
        st.caption("No moods logged yet.")

# ---------------------------
# TAB 3: Breathing Exercise
# ---------------------------
with tab3:
    st.subheader("A moment to ground yourself")
    st.write("Try box breathing: inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat a few times.")

    if st.button("▶️ Start guided breathing (30 seconds)"):
        placeholder = st.empty()
        phases = [("Breathe in...", 4), ("Hold...", 4), ("Breathe out...", 4), ("Hold...", 4)]
        cycles = 2
        for _ in range(cycles):
            for label, duration in phases:
                for remaining in range(duration, 0, -1):
                    placeholder.markdown(f"## {label} {remaining}")
                    time.sleep(1)
        placeholder.markdown("## 🌿 Well done.")

    st.caption("You can repeat this as many times as helps.")

# ---------------------------
# TAB 4: Small Actions
# ---------------------------
with tab4:
    st.subheader("Small, concrete actions")
    st.write(
        "Research suggests that taking small, tangible actions can ease climate anxiety by restoring "
        "a sense of agency. These aren't meant to 'solve' climate change alone — they're meant to help you feel less stuck."
    )

    actions = [
        "Write to one local representative about an environmental issue you care about",
        "Spend 10 minutes outside today, paying attention to what's still thriving nearby",
        "Share one piece of accurate climate information with a friend",
        "Support one local environmental organization, even in a small way",
        "Reduce one single-use item from your week",
        "Talk to someone else about how you're feeling — connection reduces isolation",
        "Learn about one local conservation or restoration project happening near you",
    ]

    if "today_action" not in st.session_state:
        st.session_state.today_action = random.choice(actions)

    st.markdown(f"### Today's suggestion: {st.session_state.today_action}")
    if st.button("🔄 Suggest a different action"):
        st.session_state.today_action = random.choice(actions)
        st.rerun()

    st.markdown("---")
    st.markdown("### 💛 Gratitude / Hope Log")
    st.write("Note one thing — big or small — that gave you hope today.")

    gratitude_text = st.text_input("Today I felt hopeful about...")
    if st.button("💾 Save to hope log"):
        if gratitude_text.strip():
            st.session_state.gratitude.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "entry": gratitude_text.strip(),
            })
            save_json(GRATITUDE_FILE, st.session_state.gratitude)
            st.success("Saved.")

    if st.session_state.gratitude:
        st.markdown("**Recent hopeful moments:**")
        for g in reversed(st.session_state.gratitude[-5:]):
            st.write(f"- {g['date']}: {g['entry']}")

# ---------------------------
# TAB 5: Resources
# ---------------------------
with tab5:
    st.subheader("Support resources")
    st.write("These are real, established resources — not a replacement for professional care, but a good place to start.")

    st.markdown("""
    - **[Climate Mental Health Network](https://www.climatementalhealth.net/)** — resources specifically for eco-anxiety and climate distress
    - **[Good Grief Network](https://www.goodgriefnetwork.org/)** — peer support program for processing climate/environmental grief
    - **[Psychology Today Therapist Finder](https://www.psychologytoday.com/us/therapists)** — find a licensed therapist near you
    - **[Force of Nature](https://forceofnature.xyz/)** — youth-focused climate action and mental health resources
    """)

    st.markdown("---")
    st.warning(
        "If you're experiencing thoughts of self-harm or are in crisis, please reach out immediately: "
        "in the US, call or text **988** (Suicide & Crisis Lifeline). In India, contact **iCall** at "
        "**9152987821** or the **AASRA** helpline at **9820466726**. If you're outside these regions, "
        "search for your local crisis helpline — you deserve support."
    )
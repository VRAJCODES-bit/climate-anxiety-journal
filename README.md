# Climate Anxiety Journal

A private journaling and mood-tracking tool for processing climate anxiety — casual, judgment-free, and built to actually be used, not just opened once and abandoned.

🔗 [Try it live](https://climate-anxiety-journal-uot3rdysdvd3z4bb5rx4dv.streamlit.app)

## Features

- 📝 **Guided journaling** with rotating climate-anxiety-specific prompts
- 😮‍💨 **Vibe check mood tracker** with relatable tags and a trend chart over time
- 🔥 **Daily streak counter** to build a genuine reflection habit
- 🌞 **Climate W of the Day** — a rotating real-world climate good-news fact
- 🌬️ **Guided breathing exercise** for in-the-moment grounding
- 🌱 **Small action suggestions** — concrete, low-effort steps shown to help restore a sense of agency
- 💛 **Hope log** — a lightweight space to track hopeful moments
- ⬇️ **Export your journal** as a plain text file anytime
- 💙 **Real, curated mental health resources** including crisis support contacts

## Why this exists

Climate anxiety is real and well-documented, especially among young people. This tool doesn't try to fix climate change or replace professional support — it's a small, private space to process feelings, notice patterns over time, and remember that hope and grief can coexist.

## Important note

This is a self-reflection tool, not a diagnostic or clinical tool. If you're struggling significantly, please reach out to a licensed therapist or a crisis line — resources are listed directly in the app.

## Setup

```bash
git clone https://github.com/YOUR-USERNAME/climate-anxiety-journal.git
cd climate-anxiety-journal
pip install -r requirements.txt
streamlit run app.py
```

## Data privacy

All journal entries, mood logs, and gratitude notes are stored locally in JSON files on the machine running the app — never sent anywhere else. These files are excluded from version control (`.gitignore`) so personal reflections never get accidentally committed.

## Tech stack

- Streamlit
- Pandas
- Pure Python (JSON-based local storage, no database required)

## Future improvements

- Add a proper database backend for more reliable long-term persistence
- Weekly reflection summary/recap emailed or shown in-app
- Optional reminder notifications (opt-in only, no guilt-based nudging)

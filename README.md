# LeetCode Revision Assistant

Tracks solved LeetCode questions in a local database and resurfaces a randomized set for spaced revision, via a Streamlit dashboard and a scheduled Telegram bot.

## What it does

- Imports and tracks solved questions, with difficulty, into a SQLite database (`import_solved.py`, `models/question.py`).
- Picks a daily revision set weighted toward retention: 4 random Easy questions plus 1 random Medium.
- **Streamlit dashboard** (`app.py`) — browse and pull a revision set on demand.
- **Telegram bot** (`telegram_sheduler.py`) — pushes the same daily revision set to a Telegram chat on a schedule (APScheduler), so revision happens without opening the app.
- Utility scripts to find unsolved questions, verify solved status, fetch difficulty metadata, and keep the local database in sync (`find_unsolved.py`, `verify_solved.py`, `fetch_difficulty.py`, `sync.py`).

## Tech stack

Python, Streamlit, SQLAlchemy (SQLite), python-telegram-bot, APScheduler

## Running locally

```bash
pip install -r requirements.txt
python create_tables.py        # first run only
streamlit run app.py           # dashboard
python telegram_sheduler.py    # scheduled Telegram pushes
```

Required environment variables: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

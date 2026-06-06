import os
import requests
import random

from datetime import date
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from db import SessionLocal
from models.question import Question

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))


def get_revision_questions():
    session = SessionLocal()

    try:
        questions = session.query(Question).all()

        easy = [q for q in questions if q.difficulty == "Easy"]
        medium = [q for q in questions if q.difficulty == "Medium"]

        selected = []

        if len(easy) >= 4:
            selected.extend(random.sample(easy, 4))
        else:
            selected.extend(easy)

        if len(medium) >= 1:
            selected.extend(random.sample(medium, 1))

        if len(selected) < 5:
            remaining = [q for q in questions if q not in selected]
            selected.extend(
                random.sample(remaining, min(5 - len(selected), len(remaining)))
            )

        random.shuffle(selected)
        return selected
    finally:
        session.close()


def send_revision_message():
    questions = get_revision_questions()

    msg = "🚀 Today's LeetCode Revision\n\n"

    for i, q in enumerate(questions, start=1):
        msg += (
            f"{i}. {q.title}\n"
            f"https://leetcode.com/problems/{q.slug}/\n\n"
        )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
    }

    response = requests.post(url, json=payload)
    try:
        print(response.json())
    except Exception:
        print("Sent message, response not JSON or empty")


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(
        send_revision_message,
        trigger="cron",
        hour=9,
        minute=0,
    )

    print("Scheduler started. Daily message at 9:00 AM.")

    # Send one immediately, then start the scheduler to send daily messages
    send_revision_message()

    scheduler.start()

# selector.py

from datetime import date

from db import SessionLocal
from models.question import Question


def get_revision_questions():

    session = SessionLocal()

    questions = session.query(Question).all()

    questions.sort(
        key=lambda q: (
            q.times_revised or 0,
            q.last_revised or date(2000, 1, 1)
        )
    )

    session.close()

    return questions[:5]
# revise.py

from datetime import date

from db import SessionLocal
from models.question import Question

session = SessionLocal()

title = input("Question title: ")

q = (
    session.query(Question)
    .filter_by(title=title)
    .first()
)

if q:
    q.last_revised = date.today()
    q.times_revised += 1

    session.commit()

    print("Updated")
from db import SessionLocal
from models.question import Question

session = SessionLocal()

for q in session.query(Question).filter(
    Question.difficulty == None
):
    print(q.title)

session.close()
import os
import requests
from dotenv import load_dotenv

from db import SessionLocal
from models.question import Question

load_dotenv()

URL = "https://leetcode.com/graphql"

cookies = {
    "LEETCODE_SESSION": os.getenv("LEETCODE_SESSION")
}

query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    difficulty
  }
}
"""

session = SessionLocal()

questions = (
    session.query(Question)
    .filter(
        (Question.difficulty == None) |
        (Question.difficulty == "")
    )
    .all()
)

print(f"Questions to update: {len(questions)}")

updated = 0
failed = 0

for q in questions:

    try:

        response = requests.post(
            URL,
            json={
                "query": query,
                "variables": {
                    "titleSlug": q.slug
                }
            },
            cookies=cookies,
            timeout=10
        )

        data = response.json()

        question_data = data.get("data", {}).get("question")

        if not question_data:
            print(f"Failed: {q.slug}")
            failed += 1
            continue

        difficulty = question_data["difficulty"]

        q.difficulty = difficulty

        session.commit()

        updated += 1

        print(
            f"[{updated}] {q.slug} -> {difficulty}"
        )

    except Exception as e:

        failed += 1

        print(
            f"Error for {q.slug}: {e}"
        )

print("\n======================")
print(f"Updated: {updated}")
print(f"Failed: {failed}")

session.close()
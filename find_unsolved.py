import ast
from urllib.parse import urlparse

from db import SessionLocal
from models.question import Question

with open("solved_urls.txt", "r") as f:
    data = f.read().strip()

if data.startswith("'") and data.endswith("'"):
    data = data[1:-1]

urls = ast.literal_eval(data)

solved_slugs = set()

for url in urls:
    if "status=SOLVED" in url and "envType=" not in url:
        slug = (
            urlparse(url)
            .path
            .split("/problems/")[1]
            .strip("/")
        )
        solved_slugs.add(slug)

session = SessionLocal()

print("\nQuestions in DB but NOT in solved list:\n")

count = 0

for q in session.query(Question).all():

    if q.slug not in solved_slugs:
        print(q.slug)
        count += 1

print("\nExtra Questions:", count)

session.close()

import ast
from urllib.parse import urlparse

from db import SessionLocal
from models.question import Question

session = SessionLocal()

with open("solved_urls.txt", "r") as f:
    urls = ast.literal_eval(f.read())

count = 0

for url in urls:

    slug = (
        urlparse(url)
        .path
        .split("/problems/")[1]
        .strip("/")
    )

    title = slug.replace("-", " ").title()

    q = Question(
        title=title,
        slug=slug,
        difficulty=None,
        times_revised=0
    )

    session.add(q)
    count += 1

session.commit()

print(f"Imported {count} questions")

session.close()
import ast
from urllib.parse import urlparse

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

print("Solved slugs:", len(solved_slugs))
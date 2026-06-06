from db import engine
from models.question import Base

Base.metadata.create_all(bind=engine)

print("Tables Created")
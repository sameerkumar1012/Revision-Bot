from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime



from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Question(Base):

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)

    title = Column(String, unique=True)

    slug = Column(String)

    difficulty = Column(String)

    solved_at = Column(DateTime)

    last_revised = Column(Date)

    times_revised = Column(Integer, default=0)
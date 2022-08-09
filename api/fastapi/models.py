from sqlalchemy import Column, Integer, String
from database import Base


class Article(Base):
    __tablename__ = "scrapped_articles"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    name = Column(String)
    link = Column(String)
    labels = Column(String)
    content = Column(String)

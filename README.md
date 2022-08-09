# WebCrawling
Task: Crawl few links, create database to store the data and give endpoints to see the data.

## Installation
First of all we will make our FASTApi and connect our SQLite database with it. For that perpose you should install fastapi from pip.
```bash
pip install fastapi
```
You should have already installed sqlite3 on your local machine, i am giving you link from where you can download it: https://www.sqlite.org/download.html.

In our project WebCrawling we are creating "api" directory. In that directory we create "fastapi" module where we will implement our connection with database and create our endpoints which are part of out tast.
In "fastapi" module we have database.py file. And now is the time to install sqlalchemy package. You can do that from our terminal and write like this:
```bash
pip install sqlalchemy
```
Our Implementation is looking like this:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./articles.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```
Second file which wre are creating is called models.py. In that file we are creating template of our database, what is the name of our table and what kind of columns it will have. So in our project our database is called Article and our table is "scrapped_articles", here is the code:
```python
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

```
!!! Note that sqlite does not support datetime that's why our date column is type of string!!!

It's time for out schemas.py file where we will create two classes. First class is ArticleBase which inherits from BaseModel class and second class is ArticleOut which inherits from ArticleBase.In that file we have nothing but validation of our columns and what we want to see when we get response from our API.
```python
from pydantic import BaseModel


class ArticleBase(BaseModel):
    class Config:
        orm_mode = True


class ArticleOut(ArticleBase):
    id: int
    date: str
    name: str
    link: str
    labels: str
    content: str

```

## License
[MIT](https://choosealicense.com/licenses/mit/)

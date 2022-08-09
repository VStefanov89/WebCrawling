# WebCrawling
Task: Crawl few links, create database to store the data and give endpoints to see the data.

## First part: Configuration of FASTAPI and UVICORN server
### Installation
Use your terminal
```bash
pip install fastapi
```
after that
```bash
pip install "uvicorn[standard]"
```
You should have already installed sqlite3 on your local machine, i am giving you link from where you can download it: https://www.sqlite.org/download.html.

### Usage
In our project WebCrawling we are creating "api" directory. In that directory we create "fastapi" module where we will implement our connection with database using sqlalchemy package and user all the features from FASTApi framework to be able to create our API for the task.
In "fastapi" module we are creating database.py file. And now is the time to install sqlalchemy package. You can do that from our terminal and write like this:
```bash
pip install sqlalchemy
```
when you do that you can use that script for creating a database with name "articles" where we will populate our scrapped articles.
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
Second file which we are creating is called models.py. In that file we are creating template of our database, what is the name of our table and what kind of columns it will have. So in our project our database is called Article and our table is "scrapped_articles", here is the code:
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
Here we are using features from sqlalchemy like Column, Integer and String, to create our table like we want. What we are doing here is just telling that we will have database with name "Article" and table with name " scrapped_articles", which will have columns id, date, name, link, labels and content with the corresponding types. Nothing more.

It's time for out schemas.py file where we will create two classes. First class is ArticleBase which inherits from BaseModel class which is from pydantic package(this is something that you already have if you have installed fastapi already) and second class is ArticleOut which inherits from ArticleBase.In that file we have nothing but validation of our columns. It is important to note that in these classes we only declare our types of columns, so when we get response from the server to know that we can only have these kind ot types, if we give something different we will get error message.
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
In our project we will have and crud.py file. In that file we will have reusable functions to interact with the data in the database.
```python
from sqlalchemy.orm import Session
import models


def get_item(db: Session, item_id: int):
    return db.query(models.Article).filter(models.Article.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()

def delete_item(db: Session, item_id:int):
    item = db.query(models.Article).filter(models.Article.id == item_id).first()
    db.delete(item)
    db.commit()
    return f"Successfully deleted user with ID{item_id}"
```
Of course we cannot escape from our main.py file where we will integrate and use all the other parts we created before.
```python
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/", response_model=List[schemas.ArticleOut])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/item/{item_id}", response_model=schemas.ArticleOut)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_item


@app.delete("/item/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return  crud.delete_item(db, item_id=item_id)

```


## Second part: Configuration of SCRAPY
### Installation
First of all we should do this:
```bash
pip install scrapy
```
After that you can write in your terminal this:
```bash
scrapy startproject crawling
```
"crawling is something that you can pick. For this task i will use "crawling" as my scrapy project. When you do that few things will happend:
- you create directory in your WebCrawling projet with name crawling;
- in that directory you will make module with the same name "crawling;
- in that module "crawling" you will have "spiders" module, which is generated automaticly and this is the place where you will create your own spiders. We will talk about that later;
- you will also get some others files in crawling module which are generated automaticly from Scrapy. All these files will be used when you want to crawl some site.

## License
[MIT](https://choosealicense.com/licenses/mit/)

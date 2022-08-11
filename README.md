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
In our project WebCrawling we are creating "api" directory. In that directory we create "fastapi" module where we will implement our connection with database using sqlalchemy package and use all the features from FASTApi framework to be able to create our API for the task.
In "fastapi" module we are creating database.py file. And now is the time to install sqlalchemy package. You can do that from our terminal and write like this:
```bash
pip install sqlalchemy
```
when you do that you can use that script for creating a database with name "articles" where we will populate our scraped articles. Note that when we implement our crawling project we will tell Scrapy to connect exactly to this database.

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
- you will also get some others files in crawling module which are generated automaticly from Scrapy. All these files will be used to set up your Scrapy project.

### Usage
First we need to create our spider. Spiders are classes which define how a certain site (or a group of sites) will be scraped, including how to perform the crawl and how to extract structured data from their pages (i.e. scraping items). In other words, Spiders are the place where you define the custom behaviour for crawling and parsing pages for a particular site (or, in some cases, a group of sites). Our Spider should have name and list of urls. The name is very important because after finishing your spider logic in the terminal we will write a command which includes that name to be able to start our crawling. We have class attribute start_urls, which is just list of our urls that we want to scrap. As tha task says we need to scrap the last 20 articles from the given site, so we just placed all these urls in our start_url attribute.

After that in parse method we should write our logic for extracting data from the response we got. When we inspect every single page, we notice some similarities:
-the date when the article is published is under tag "div.nbs-post__date";
-the name(title) of our article is under tag "h1.headline";
-tha link is just response.request.link;
-the labels are under tag "div.label--sm";
-and the content of the page is under tag "p" ( here is very tricky, but we will talk about it later);

So here is the code:
```python
import scrapy
from ..items import CrawlingItem
import w3lib.html


class ArticleSpider(scrapy.Spider):
    name = "article"
    start_urls = [
        'https://nbs.sk/en/news/s-tatement-from-the-27th-meeting-of-the-bank-board-of-the-nbs/',
        'https://nbs.sk/en/news/report-on-economic-development-in-may-2010-summary/',
        'https://nbs.sk/en/news/statement-from-the-24th-meeting-of-the-bank-board-of-nbs/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-april-2010/',
        'https://nbs.sk/en/news/statement-from-the-22nd-meeting-of-the-bank-board-of-nbs/',
        'https://nbs.sk/en/news/statement-from-the-21st-meeting-of-the-bank-board-of-the-nbs-2/',
        'https://nbs.sk/en/news/statement-from-the-20th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/meeting-of-the-nbs-management-representatives-of-banks-and-investment-firms/',
        'https://nbs.sk/en/news/statement-from-the-18th-meeting-of-the-bank-board-of-narodna-banka-slovenska/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-march-2010/',
        'https://nbs.sk/en/news/statement-from-the-17th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/statement-from-the-14th-meeting-of-the-bank-board-of-the-nbs-2/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-february-2010/',
        'https://nbs.sk/en/news/statement-from-the-11th-meeting-of-the-bank-board-of-the-nbs-4/',
        'https://nbs.sk/en/news/statement-from-the-10th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/statement-from-the-9th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/statement-from-the-8th-meeting-of-the-bank-board-of-the-nbs-2/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-january-2010/',
        'https://nbs.sk/en/news/nbs-warning-regarding-unauthorised-activity-of-the-trading-company-plus500-ltd/',
        'https://nbs.sk/en/news/statement-from-the-44th-meeting-of-the-bank-board-of-the-nbs-2/',
    ]

    def parse(self, response, **kwargs):
        item = CrawlingItem()

        date =  response.css("div.nbs-post__date::text").get()
        name = response.css("h1.headline::text").get()
        link = response.request.url
        labels = response.css("div.label--sm::text").get()
        selectors = response.css("p")
        content = ''
        for selector in selectors:
            text = selector.get()
            text = w3lib.html.remove_tags(text)
            if "<p>" in text:
                text = text.replace("<p>", "")
            if "</p>" in text:
                text = text.replace("</p>", "")
            if "<strong>" in text:
                text = text.replace("<strong>", "")
            if "</strong>" in text:
                text = text.replace("</strong>", "")
            if "<br>" in text:
                text = text.replace("<br>", "")
            if "</br>" in text:
                text = text.replace("</br>", "")
            if "Internet:" in text:
                break

            content += text

        item["date"] = date
        item["name"] = name
        item["link"] = link
        item["labels"] = labels
        item["content"] = content

        yield item
```
When we reach the moment to scrap the text of the page we find small problem. In <p> tag some times we have <strong> tag, which is making us to don't be able to take all the text from that tag with one command. For every page in <p> tag we have several selector with different structure. That is why we are forced to check what kind of tags we have in that selector and one by one to remove it from the text. This was the only solution i got, because if we don't do that, all the logic from the text in that page will be misleading (some letters will be missing ). Also here we are removing the html elements from the text, which is part of our task.

Second, we need place to collect all tha data that we are going to scrap so for that reason we need something like container. So scrapy provides us with that container and that is our items.py file. In that file we are just goin to declare out fields of scrapped data.

```python
import scrapy


class CrawlingItem(scrapy.Item):
    date = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    labels = scrapy.Field()
    content = scrapy.Field()
```

Third, we need to store the scrapped data in our sqlite3 database. For that reason we should use piplines.py file to create our database file and score the data. In order to do that we should write few more methods in our CrawlingPipeline class, which is generated automatically for us. In that class we will define our get_db_path method. This method just tells where we want to create our database file. This is important because after we scrapped the data we should know the path to our database to be able to make the connection between database and our api.
We are creating a create_connection method, which is making the connection to our database, pretty straight forward. Creat_table method is creating the table in our database with all the specific columns we want. We also have store_in_table method, which is just committing the data in our database. In the process_item method we just call stroe_in_table method and nothing more. Here is the code:

```python
import sqlite3
import os


class CrawlingPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    @staticmethod
    def get_db_path():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        project_path = os.path.abspath(os.path.join(parent_dir_path, os.pardir))
        fastapi_dir = r"api\fastapi"
        db_name = "articles.db"
        db_path = os.path.join(project_path, fastapi_dir, db_name)
        return db_path


    def create_connection(self):
        self.connection = sqlite3.connect(self.get_db_path())
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS scrapped_articles""")
        self.cursor.execute("""CREATE TABLE scrapped_articles(
                                                  id integer primary key autoincrement,
                                                  date text, 
                                                  name text, 
                                                  link text,
                                                  labels text,
                                                  content text)
                                                  """)

    def process_item(self, item, spider):
        self.store_in_table(item)
        return item

    def store_in_table(self, item):
        date = item["date"]
        name = item["name"]
        link = item["link"]
        labels = item["labels"]
        content = item["content"]
        self.cursor.execute(f"""INSERT INTO scrapped_articles(date, name, link, labels, content)
                                  VALUES("{date}", "{name}", "{link}", "{labels}", "{content}")""")
        self.connection.commit()

```
## Finally
Let's crawl some pages. In order to do that go to your terminal and make sure the path is correct. We should be in crawling module path to run our Spider. Something like this:

```bash
(venv) ...something...\WebCrawling\crawling\crawling>
```
So write to the terminal this command:
```bash
(venv) ...something...\WebCrawling\crawling\crawling>scrapy crawl article
```
!!! Fingers crossed !!!

"article" is the name of our spider.
You should be able to see how Scrapy handles everything by himself and crawl from page to page and store the data in your database.
About the database... If you go to https://sqliteonline.com/ in the upper left corner you should see "File" button. Click on it and find your path to the database from your local machine. When you do that you should be able to see all the 20 articles that are scrapped with all needed information about them.

After that again go to your terminal and make sure that you are on correct path about your API, now we want to run it... So the path to the API in you machine should look something like this:
```bash
(venv) ...something...\WebCrawling\api\fastapi>
```
If you are on the correct path then write in your terminal this command:

```bash
(venv) ...something...\WebCrawling\api\fastapi>uvicorn main:app --reload

```

If you do that and everything is correct you should see someting like this:
```bash
(venv) ...something...\WebCrawling\api\fastapi>uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\usr\\PycharmProjects\\WebCrawling\\api\\fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [10592] using WatchFiles
INFO:     Started server process [3064]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:58513 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:58514 - "GET /items/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:63740 - "GET /item/5 HTTP/1.1" 200 OK


```
If this is the message you see that's mean that your API is running and freely you can check the endpoints we created.


## License
[MIT](https://choosealicense.com/licenses/mit/)

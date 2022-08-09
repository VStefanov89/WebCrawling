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


## License
[MIT](https://choosealicense.com/licenses/mit/)

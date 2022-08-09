import sqlite3
import os


class CrawlingPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    @staticmethod
    def get_db_path():
        working_dir = os.getcwd()
        fastapi_dir = r"api\fastapi"
        db_name = "articles.db"
        db_path = os.path.join(working_dir, fastapi_dir, db_name)
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

    def process_item(self, item):
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

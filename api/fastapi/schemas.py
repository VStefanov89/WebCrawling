from pydantic import BaseModel


class ArticleBase(BaseModel):
    class Config:
        orm_mode = True

class ArticleCreate(ArticleBase):
    date: str
    name: str
    link: str
    labels: str
    content: str

class ArticleOut(ArticleBase):
    id: int
    date: str
    name: str
    link: str
    labels: str
    content: str
from sqlalchemy.orm import Session
import models, schemas


def create_item(db: Session, item: schemas.ArticleCreate):
    db_item = models.Article()
    db_item.date = item.date
    db_item.name = item.name
    db_item.link = item.link
    db_item.labels = item.labels
    db_item.content = item.content
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Article).filter(models.Article.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def delete_item(db: Session, item_id: int):
    item = db.query(models.Article).filter(models.Article.id == item_id).first()
    db.delete(item)
    db.commit()
    return f"Successfully deleted user with ID{item_id}"

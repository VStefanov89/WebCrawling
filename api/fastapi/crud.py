from sqlalchemy.orm import Session
import models


def get_user(db: Session, user_id: int):
    return db.query(models.Article).filter(models.Article.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id:int):
    user = db.query(models.Article).filter(models.Article.id == user_id).first()
    db.delete(user)
    db.commit()
    return f"Successfully deleted user with ID{user_id}"

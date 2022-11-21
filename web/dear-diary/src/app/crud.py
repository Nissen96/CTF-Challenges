from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas, security


def get_user(db: Session, user_id: str) -> schemas.User | None:
    return db.query(models.User).filter_by(id=user_id).first()


def get_user_by_username(db: Session, username: str) -> schemas.User | None:
    return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    hashed_password = security.hash_password(user.password)
    db_user = models.User(username=user.username.lower(), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_entry(db: Session, entry_id: str, user_id: str = None) -> schemas.DiaryEntry | None:
    return db.query(models.DiaryEntry).filter_by(id=entry_id).filter(or_(
        models.DiaryEntry.author_id == user_id,
        models.DiaryEntry.is_public)
    ).first()


def get_entries(db: Session, user_id: str = None) -> list[schemas.DiaryEntry]:
    if user_id is None:
        return db.query(models.DiaryEntry).filter_by(is_public=True).all()
    else:
        return db.query(models.DiaryEntry).filter(or_(
            models.DiaryEntry.author_id == user_id,
            models.DiaryEntry.is_public)
        ).all()


def create_entry(db: Session, entry: schemas.DiaryEntryCreate, author_id: str, author_name) -> schemas.DiaryEntry:
    db_entry = models.DiaryEntry(**entry.dict(), author_id=author_id, author_name=author_name)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

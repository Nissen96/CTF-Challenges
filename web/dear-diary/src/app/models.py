from sqlalchemy import Boolean, Column, ForeignKey, String, CHAR
from sqlalchemy.orm import relationship
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    diary_entries = relationship("DiaryEntry", back_populates="author")


class DiaryEntry(Base):
    __tablename__ = "entries"

    id = Column(CHAR(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    title = Column(String)
    content = Column(String)
    is_public = Column(Boolean)
    author_id = Column(CHAR(32), ForeignKey("users.id"))
    author_name = Column(String)

    author = relationship("User", back_populates="diary_entries")

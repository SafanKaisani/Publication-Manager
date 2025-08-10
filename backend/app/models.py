# backend/app/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    entry_date = Column(Date, nullable=True)
    publication_type = Column(String, nullable=True)
    year = Column(String, nullable=True)
    title = Column(String, nullable=False)
    status = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    theme = Column(String, nullable=True)

    # Relationship to AuthorRole
    authors = relationship("AuthorRole", back_populates="publication", cascade="all, delete-orphan", lazy="joined")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    affiliation = Column(String, nullable=True)

    # Relationship to AuthorRole
    publications = relationship("AuthorRole", back_populates="author", cascade="all, delete-orphan", lazy="joined")


class AuthorRole(Base):
    __tablename__ = "author_roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=True)
    publication_id = Column(Integer, ForeignKey("publications.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))

    # Relationships
    publication = relationship("Publication", back_populates="authors", lazy="joined")
    author = relationship("Author", back_populates="publications", lazy="joined")

# User model for authentication    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
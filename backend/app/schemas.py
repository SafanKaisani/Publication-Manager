from datetime import date
from typing import List, Optional
from pydantic import BaseModel

# ------------------ Author Schemas ------------------
class AuthorBase(BaseModel):
    name: str
    affiliation: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    class Config:
        orm_mode = True

# ------------------ AuthorRole Schemas ------------------
class AuthorRoleBase(BaseModel):
    role: Optional[str] = None

class AuthorRoleCreate(AuthorRoleBase):
    author: AuthorCreate

class AuthorRoleRead(AuthorRoleBase):
    id: int
    author: AuthorRead
    class Config:
        orm_mode = True

# ------------------ Publication Schemas ------------------
class PublicationBase(BaseModel):
    entry_date: Optional[date] = None
    publication_type: Optional[str] = None
    year: Optional[str] = None
    title: str
    status: Optional[str] = None
    reference: Optional[str] = None
    theme: Optional[str] = None

class PublicationCreate(PublicationBase):
    authors: Optional[List[AuthorRoleCreate]] = []

class PublicationRead(PublicationBase):
    id: int
    authors: List[AuthorRoleRead] = []
    class Config:
        orm_mode = True

# ------------------ User Schemas ------------------
class UserBase(BaseModel):
    username: str   

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

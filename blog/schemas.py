from pydantic import BaseModel
from typing import Optional

class BlogBase(BaseModel):  
    title: str
    content: str

class Blog(BlogBase):
    user_id: int

class ShowBlogBase(BlogBase):
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    email: str
    blogs: list[ShowBlogBase] = []
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    user: ShowUser
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
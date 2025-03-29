from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    content: str
    user_id: int
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    password: str

class ShowUser(BaseModel):
    username: str
    email: str
    blogs: list[Blog] = []
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    content: str
    user: ShowUser
    class Config:
        orm_mode = True
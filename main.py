from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return {'data': {
        "name": "John Doe",
    }}


class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    tags: Optional[list] = []



@app.post("/blog")
def create_blog(blog: Blog):
    return {'data': {
        "title": blog.title,
        "content": blog.content,
    }}



@app.get("/blog/{id}/comments")
def comments(id: int, limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published and limit > 0:
        return {'data': {
            "post_id": id,
            "comments": [
                {"id": 1, "content": "Great post!"},
                {"id": 2, "content": "Thanks for sharing!"}
            ]
        }}
    else:
        return {'data': {
            "post_id": id,
            "comments": []
        }}



@app.get("/blog/{id}")
def get_blog(id: int):
    return {'data': {
        "post_id": id,
        "title": "My First Blog Post",
        "content": "This is the content of the blog post."
    }}

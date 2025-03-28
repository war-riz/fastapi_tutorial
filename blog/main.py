from fastapi import FastAPI
from . import schemas
from . import models
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/blog")
def create_blog(blog: schemas.Blog):
    return {
        "title": blog.title,
        "content": blog.content
    }
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    
    # Check if a blog with the same title already exists
    existing_blog = db.query(models.Blog).filter(models.Blog.title == blog.title).first()
    if existing_blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blog with this title already exists"
        )

    # Now, create the blog
    db_blog = models.Blog(title=blog.title, content=blog.content)

    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)

    return {"data": db_blog}



@app.delete("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_blog(id: int, db: Session = Depends(get_db)):
    deleted_rows = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    
    if deleted_rows == 0:  # If no rows were deleted, blog does not exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db.commit()
    return {"message": "Blog deleted successfully"}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db_blog.title = blog.title
    db_blog.content = blog.content

    db.commit()
    db.refresh(db_blog)

    return {"data": db_blog}



@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"data": blogs}



@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        return {"data": blog}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "Blog not found"}
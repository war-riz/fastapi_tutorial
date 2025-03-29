from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db


router = APIRouter(
    tags=["Blogs"]
)


@router.get("/blogs", response_model=List[schemas.ShowBlog], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blogs found"
        )
    return blogs



@router.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    
    # Check if a blog with the same title already exists
    existing_blog = db.query(models.Blog).filter(models.Blog.title == blog.title).first()
    if existing_blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blog with this title already exists"
        )

    # Now, create the blog
    db_blog = models.Blog(title=blog.title, content=blog.content, user_id=blog.user_id)

    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)

    return db_blog



@router.delete("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_blog(id: int, db: Session = Depends(get_db)):
    deleted_rows = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    
    if deleted_rows == 0:  # If no rows were deleted, blog does not exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db.commit()
    return {"message": "Blog deleted successfully"}



@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
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




@router.get("/blog/{id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        return blog
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "Blog not found"}
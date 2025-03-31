from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session, joinedload
from .. import schemas, models
from ..database import get_db
from ..ouath2 import get_current_user
from collections import defaultdict


router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.get("s", status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).options(joinedload(models.Blog.user)).all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blogs found"
        )
    
    user_blog_map = defaultdict(list)
    for blog in blogs:
        user_blog_map[blog.user.username].append(schemas.ShowBlogBase(
            title=blog.title,
            content=blog.content
        ))
    
    unique_users = []
    for username, user_blogs in user_blog_map.items():
        user = next((blog.user for blog in blogs if blog.user.username == username), None)
        if user:
            unique_users.append(schemas.ShowUser(
                username=user.username,
                email=user.email,
                blogs=user_blogs
            ))

    return {"users": unique_users, "current_user": current_user.username}  # ✅ Custom response



@router.post("", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    
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

    return {"data": db_blog, "current_user": current_user.username}  # ✅ Custom response



@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    deleted_rows = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    
    if deleted_rows == 0:  # If no rows were deleted, blog does not exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db.commit()
    return {"message": "Blog deleted successfully", "current_user": current_user.username}



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
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

    return {"data": db_blog, "current_user": current_user.username}




@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def get_blog(id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
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
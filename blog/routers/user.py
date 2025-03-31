from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..hashing import Hash


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    
    db_user = models.User(username=user.username, email=user.email, password=Hash.get_hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
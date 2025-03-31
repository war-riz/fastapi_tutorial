from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..hashing import Hash
from ..jwt_token import create_access_token


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


@router.post('', status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not Hash.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    access_token = create_access_token(
        data={"sub": db_user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


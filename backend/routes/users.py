from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
import models
from crud.users_crud import create_user, authenticate_user, create_token, get_user_by_username, get_user_by_email
from database import get_db

router = APIRouter()


@router.post("/register", response_model=schemas.UserCreateResponse)
def register_user(user: schemas.UserCreateRequest, db: AsyncSession = Depends(get_db)):
    existing_user = get_user_by_username(db=db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )
    existing_user = get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this e-mail already registered."
        )
    create_user(db=db, user=user)
    return {"success": True}


@router.post("/login", response_model=schemas.LoginUserResponse)
def login_user(login_user: schemas.LoginUserRequest, db: AsyncSession = Depends(get_db)):
    user = authenticate_user(db, login_user.username, login_user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = db.query(models.Token).filter(models.Token.user_id == user.id).first()
    if not token:
        token = create_token(db=db, user_id=user.id)
        return {"token": token}
    return {"token": token.token}

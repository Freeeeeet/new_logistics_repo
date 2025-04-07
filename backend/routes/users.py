from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import schemas
import models
from crud.users_crud import create_user, authenticate_user, create_token, get_user_by_username, get_user_by_email
from database import get_db

router = APIRouter()


@router.post("/register", response_model=schemas.UserCreateResponse)
async def register_user(user: schemas.UserCreateRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db=db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )
    existing_user = await get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this e-mail already registered."
        )
    await create_user(db=db, user=user)
    return {"success": True}


@router.post("/login", response_model=schemas.LoginUserResponse)
async def login_user(login_user: schemas.LoginUserRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, login_user.username, login_user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Переписано с async запросом
    result = await db.execute(
        select(models.Token).where(models.Token.user_id == user.id)
    )
    token = result.scalar_one_or_none()

    if not token:
        token_value = await create_token(db=db, user_id=user.id)
        return {"token": token_value}
    return {"token": token.token}
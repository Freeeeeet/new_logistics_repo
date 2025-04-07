from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import models
import schemas
from utils.security import hash_password, verify_password, create_access_token


def create_user(db: Session, user: schemas.UserCreateRequest):
    try:
        password_hash = hash_password(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            password_hash=password_hash
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding user to the database."
        )


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_token(db: Session, user_id: int):
    try:
        access_token = create_access_token()
        db_token = models.Token(
            user_id=user_id,
            token=access_token,
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        print(f"Token for user {user_id} added to database correctly, returning user")
        return access_token
    except Exception as e:
        db.rollback()
        print(f"An error occurred while adding user to DB. {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding user to the database."
        )


def check_auth(db: Session, token: str):
    try:
        user = db.query(models.Token).filter(models.Token.token == token).first()
        return user
    except Exception as e:
        print(f"An error occurred while checking user token: {e}")
        return None




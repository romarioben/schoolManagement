from sqlalchemy.orm import Session
from sqlalchemy import select

from auth_app import models, schemas
from auth_app.auth import hash_password


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.scalar(select(models.User).where(models.User.email == email))


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.scalar(select(models.User).where(models.User.username == username))


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user_in.email,
        username=user_in.username,
        surname=user_in.surname,
        firstname=user_in.firstname,
        phone_number=user_in.phone_number,
        role=user_in.role,
        hashed_password=hash_password(user_in.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return list(db.scalars(select(models.User).offset(skip).limit(limit)))


def authenticate_user(db: Session, email_or_username: str, password: str) -> models.User | None:
    from auth_app.auth import verify_password

    user = get_user_by_email(db, email_or_username) or get_user_by_username(
        db, email_or_username
    )
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import cruds, schemas
from ..core import security
from ..core.config import SessionLocal
from typing import Annotated

from ..services import user_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbDependency = Annotated[Session, Depends(get_db)]

@router.post("/sign-up/", response_model=schemas.UserWithToken)
async def register_user(user: schemas.UserCreate, db: DbDependency):
    db_user = user_service.create_user(db=db, user=user)
    access_token = security.create_access_token(subject=db_user.email)
    return schemas.UserWithToken(id=db_user.id, email=db_user.email, token=access_token)

@router.post("/login/", response_model=schemas.UserWithToken)
async def login(user: schemas.UserLogin, db: DbDependency):
    db_user = cruds.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not cruds.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = security.create_access_token(subject=user.email)

    return schemas.UserWithToken(
        id=db_user.id,
        email=db_user.email,
        token=access_token
    )

@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(db: DbDependency, token: str = Depends(security.oauth2_scheme)):
    email = security.get_email_from_token(token)
    user = cruds.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

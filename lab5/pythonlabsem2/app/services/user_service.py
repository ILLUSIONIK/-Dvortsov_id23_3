from sqlalchemy.orm import Session
from .. import cruds, schemas
from ..services import email_service

def create_user(db: Session, user: schemas.UserCreate):
    db_user = cruds.create_user(db=db, user=user)
    email_service.send_welcome_email(user.email)
    return db_user
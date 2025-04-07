from pydantic import EmailStr
from pydantic import BaseModel, conint

class BrutHashRequest(BaseModel):
    hash: str
    charset: str
    max_length: conint(gt=0, le=8)

class TaskStatusResponse(BaseModel):
    status: str
    progress: int
    result: str | None

class TaskIdResponse(BaseModel):
    task_id: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str


class UserWithToken(BaseModel):
    id: int
    email: EmailStr
    token: str

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):

    id: Optional[int] = None
    username: str
    password: str
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class AuthModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

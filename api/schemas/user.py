from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id_user: Optional[int]=1
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class UserCount(BaseModel):
    total: int
    
    class Config:
        orm_mode = True
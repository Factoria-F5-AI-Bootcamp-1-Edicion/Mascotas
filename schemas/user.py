from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int]=1
    name: str
    email: str
    password: str

class UserCount(BaseModel):
    total: int
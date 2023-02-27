from typing import Optional

from pydantic import BaseModel


class Pet(BaseModel):
    id_pet: Optional[int]=1
    name_animalito: str
    vacunado: bool
    castrado: bool
    edad: int
    enfermedad: str
    
    class Config:
        orm_mode = True

class PetCount(BaseModel):
    total: int
    
    class Config:
        orm_mode = True
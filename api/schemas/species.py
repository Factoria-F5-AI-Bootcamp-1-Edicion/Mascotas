from pydantic import BaseModel
from typing import Optional

class Species(BaseModel):
    id_species: Optional[int]=1
    especies: str
    
    class Config:
        orm_mode = True

class SpeciesCount(BaseModel):
    total: int
    
    class Config:
        orm_mode = True
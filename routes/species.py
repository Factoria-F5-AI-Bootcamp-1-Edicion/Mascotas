from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from config.depy import get_db
from models.pets import Especies
from schemas.species import Species, SpeciesCount

router = APIRouter()
   
####----------------CRUD Funcions on USERS--------------------------#####

@router.get("/",
    response_model=List[Species],
    description="Get a list of all users",
)
async def get_species(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = []
    try:
        result = db.query(Species).offset(skip).limit(limit).all()
    except:
        #En caso de que no se pueda ejecutar la transacción hago rollback de la transacción y lanzo HttpException
        raise HTTPException(status_code=404, detail="Users not found")
    return result


@router.get("/", response_model=SpeciesCount)
async def get_users_count(db: Session = Depends(get_db)):
    result = db.execute(select([func.count()]).select_from(Species))
    return {"total": tuple(result)[0][0]}


@router.get(
    "/{id}",
    response_model=Species,
    description="Get a single user by Id",
)
async def get_Species(id: str, db: Session = Depends(get_db)):
    return db.execute(Species.select().where(Species.c.id_species == id)).first()


@router.post("/",
    response_model=Species,
    description="Create a new specie",
)
async def create_species(species: Species, db: Session = Depends(get_db)):
    print(species.dict())
    #db_user= Species(id_species=user.id_species, **user.dict())
    #user = user.dict()
    db_species = Especies(especies=species.especies)
    db.add(db_species)
    db.commit()
    db.refresh(db_species)
    return db_species


@router.put(
    "/{id}", response_model=Species, description="Update a Species by Id"
)
async def update_user(species: Species, id: int, db: Session = Depends(get_db)):
    db.execute(
        Species.update()
        .values(especies=species.especies)
        .where(species.c.id_species == id)
    )
    db.commit()
    result = db.execute(Species.select().where(Species.c.id_species == id)).first()
    return result


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db.execute(Species.delete().where(Species.c.id_species == id))
    db.commit()
    result = db.execute(Species.select().where(Species.c.id_species == id)).first()
    return result

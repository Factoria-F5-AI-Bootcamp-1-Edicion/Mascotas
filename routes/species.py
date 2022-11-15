from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from config.depy import get_db
from models.pets import Especies
from schemas.species import Species, SpeciesCount

router = APIRouter()
   
####----------------CRUD Functions on SPECIES-------------------------#####

@router.get("/",
    response_model=List[Species],
    description="Get a list of all species",
)
async def get_species(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = []
    try:
        result = db.query(Especies).offset(skip).limit(limit).all()
    except:
        #En caso de que no se pueda ejecutar la transacción hago rollback de la transacción y lanzo HttpException
        raise HTTPException(status_code=404, detail="Species not found")
    return result


@router.get("/count", response_model=SpeciesCount)
async def get_species_count(db: Session = Depends(get_db)):
    result = db.execute(select([func.count()]).select_from(Especies))
    return {"total": tuple(result)[0][0]}


@router.get(
    "/{id}",
    response_model=Species,
    description="Get a single specie by Id",
)
async def get_speciesID(id: str, db: Session = Depends(get_db)):
    return db.execute(Species.select().where(Species.c.id_species == id)).first()


@router.post("/",
    response_model=Species,
    description="Create a new specie",
)
async def create_species(species: Species, db: Session = Depends(get_db)):
    print(species.dict())
    try:
        db_species = Especies(especies=species.especies)
        db.add(db_species)
        db.commit()
        db.refresh(db_species)
    except:
        status_code=status.HTTP_406_NOT_ACCEPTABLE
        detail="406 Not Acceptable"
    return db_species


@router.put(
    "/{id}", response_model=Species, description="Update a Species by Id"
)
async def update_species(species: Species, id: int, db: Session = Depends(get_db)):
    """
    Update an User stored in the database
    """
    update_row = species
    try:
        db_row = db.query(Species).filter(Species.id_species == id).first()
        if db_row:
            db_row.especies = species.especies
            updated_row = db.merge(db_row)        # Usamos merge para modificar los datos de una fila
            print(updated_row)
            db.commit()
    except:
        status_code=status.HTTP_404_NOT_FOUND
        detail="Species not found with the given ID"   
    return update_row


@router.delete("/{id}", status_code=200)
async def delete_species(id: int, db: Session = Depends(get_db)):
    try:
        db_del = db.query(Especies).filter(Especies.id_species == id).first()
        db.delete(db_del)
        db.commit()
    except:
        #Exception code 204 
        raise HTTPException(status_code=HTTP_204_NO_CONTENT)
    return db_del

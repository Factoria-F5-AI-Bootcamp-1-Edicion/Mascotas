from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from config.depy import get_db
from models.pets import Mascotas_especificas
from schemas.pet import Pet, PetCount

router = APIRouter()


####----------------CRUD Functions on PET--------------------------#####
@router.get("/",
    response_model=List[Pet],
    description="Get a list of all pets",
)
async def get_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = []
    try:
        result = db.query(Mascotas_especificas).offset(skip).limit(limit).all()
    except:
        #En caso de que no se pueda ejecutar la transacción hago rollback de la transacción y lanzo HttpException
        raise HTTPException(status_code=404, detail="Pets not found")
    return result


@router.get("/count", response_model=PetCount)
async def get_pets_count(db: Session = Depends(get_db)):
    result = db.execute(select([func.count()]).select_from(Pet))
    return {"total": tuple(result)[0][0]}


@router.get(
    "/{id}",
    response_model=Pet,
    description="Get a single pet by Id",
)
async def get_user(id: str, db: Session = Depends(get_db)):
    return db.query(Mascotas_especificas).filter(Mascotas_especificas.id_user == id).first()


@router.post("/", response_model=Pet, description="Create a new pet", status_code=200)
async def create_pet(pet: Pet, id_species: int, id_user: int, db: Session = Depends(get_db)):
    print(pet.dict())
    db_pet=pet
    try:
        db_pet = Mascotas_especificas(
                name_animalito=pet.name_animalito, 
                vacunado=pet.vacunado, 
                castrado=pet.castrado, 
                edad=pet.edad, 
                enfermedad=pet.enfermedad,
        )
        db.add(db_pet)
        db.commit()
        db.refresh(db_pet)
    except:
        status_code=status.HTTP_406_NOT_ACCEPTABLE
        detail="406 Not Acceptable"
    return db_pet

@router.put(
    "/{id}", response_model=Pet, description="Update a Pet by Id"
)
async def update_pet(pet: Pet, id: int, db: Session = Depends(get_db)):
    """
    Update an Pet stored in the database
    """
    update_row = pet
    try:
        db_row = db.query(Mascotas_especificas).filter(Mascotas_especificas.id_user == id).first()
        if db_row:
            name_animalito=pet.name_animalito, 
            vacunado=pet.vacunado, 
            castrado=pet.castrado, 
            edad=pet.edad, 
            enfermedad=pet.enfermedad,
            updated_row = db.merge(db_row)        # Usamos merge para modificar los datos de una fila
            print(updated_row)
            db.commit()
    except:
        status_code=status.HTTP_404_NOT_FOUND
        detail="Pet not found with the given ID"   
    return update_row



@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_pet(id: int, db: Session = Depends(get_db)):
    try:
        db_del = db.query(Pet).filter(Pet.id_user == id).first()
        db.delete(db_del)
        db.commit()
    except:
        #En caso de que no se pueda ejecutar la transacción lanzo HttpException 204
        raise HTTPException(status_code=HTTP_204_NO_CONTENT)
    return db_del

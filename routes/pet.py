from fastapi import APIRouter, Depends, HTTPException
from models.pets import Mascotas_especificas
from schemas.pet import Pet, PetCount
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from config.depy import get_db

router = APIRouter()


####----------------CRUD Funcions on PET--------------------------#####
@router.get("/",
    response_model=List[Pet],
    description="Get a list of all pets",
)
async def get_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = []
    try:
        result = db.query(Pet).offset(skip).limit(limit).all()
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
    return db.execute(Mascotas_especificas.select().where(Mascotas_especificas.c.id_pet == id)).first()


@router.post("/", response_model=Pet, description="Create a new pet")
async def create_user(pet: Pet, id_species: int, id_user: int, db: Session = Depends(get_db)):
    #print(**user.dict())
    #db_user= Usuario(id_pet=user.id_pet, **user.dict())
    #user = user.dict()
    db_pet = Pet(name_animalito=pet.name_animalito, 
                vacunado=pet.vacunado, 
                castrado=pet.castrado, 
                edad=pet.edad, 
                enfermedad=pet.enfermedad,
                id_species= id_species,
                id_user=id_user
                )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@router.put(
    "/{id}", response_model=Pet, description="Update a Pet by Id"
)
async def update_pet(pet: Pet, id: int, db: Session = Depends(get_db)):
    db.execute(
        Pet.update()
        .values(name_animalito=pet.name_animalito, vacunado=pet.vacunado, castrado=pet.castrado, edad=pet.edad, enfermedad=pet.enfermedad)
        .where(Pet.c.id_pet == id)
    )
    db.commit()
    result = db.execute(Pet.select().where(Pet.c.id_pet == id)).first()
    return result


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db.execute(Pet.delete().where(Pet.c.id_pet == id))
    db.commit()
    result = db.execute(Pet.select().where(Pet.c.id_pet == id)).first()
    return result

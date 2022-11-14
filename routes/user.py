from typing import List

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from config.depy import get_db
from models.pets import Usuario
from schemas.user import User, UserCount

router = APIRouter()

key = Fernet.generate_key()
f = Fernet(key)
    
####----------------CRUD Funcions on USER--------------------------#####

@router.get("/",
    response_model=List[User],
    description="Get a list of all users",
)
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = []
    try:
        result = db.query(Usuario).offset(skip).limit(limit).all()
    except:
        #En caso de que no se pueda ejecutar la transacción lanzo HttpException
        raise HTTPException(status_code=404, detail="Users not found")
    return result


@router.get("/count", response_model=UserCount)
async def get_users_count(db: Session = Depends(get_db)):
    result = db.execute(select([func.count()]).select_from(Usuario))
    return {"total": tuple(result)[0][0]}


@router.get(
    "/{id}",
    response_model=User,
    description="Get a single user by Id",
)
async def get_user(id: str, db: Session = Depends(get_db)):
    return db.execute(Usuario.select().where(Usuario.c.id_user == id)).first()


@router.post("/",
    response_model=User,
    description="Create a new user",
)
async def create_user(user: User, db: Session = Depends(get_db)):
    print(user.dict())
    #db_user= Usuario(id_user=user.id_user, **user.dict())
    #user = user.dict()
    db_user = Usuario(name=user.name, email=user.email, password=f.encrypt(user.password.encode("utf-8")))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
''' 
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = db.execute(users.insert().values(new_user))
    db.commit()
    print(f"primary_key:{result.inserted_primary_key[0]}")
    print(f"id_user:{users.c.id_user}")
    res = db.execute(users.select().where(users.c.id_user == result.inserted_primary_key[0])).first()
    return res
'''


@router.put(
    "/{id}", response_model=User, description="Update a User by Id"
)
async def update_user(user: User, id: int, db: Session = Depends(get_db)):
    db.execute(
        Usuario.update()
        .values(name=user.name, email=user.email, password=user.password)
        .where(Usuario.c.id_user == id)
    )
    db.commit()
    result = db.execute(Usuario.select().where(Usuario.c.id_user == id)).first()
    return result


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db.execute(Usuario.delete().where(Usuario.c.id_user == id))
    db.commit()
    result = db.execute(Usuario.select().where(Usuario.c.id_user == id)).first()
    return result

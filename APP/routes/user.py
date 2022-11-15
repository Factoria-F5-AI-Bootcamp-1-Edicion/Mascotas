from typing import List

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from config.depy import get_db
from models.pets import Usuario
from schemas.user import User, UserCount

key = Fernet.generate_key()
f = Fernet(key)

router = APIRouter()
    
####----------------CRUD Functions on USER--------------------------#####

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
async def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.id_user == id).first()


@router.post("/",
    response_model=User,
    description="Create a new user",
    status_code=200
)
async def create_user(user: User, db: Session = Depends(get_db)):
    print(user.dict())
    #db_user= Usuario(id_user=user.id_user, **user.dict())
    #user = user.dict()
    try:
        db_user = Usuario(name=user.name, email=user.email, password=f.encrypt(user.password.encode("utf-8")))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        status_code=status.HTTP_406_NOT_ACCEPTABLE
        detail="406 Not Acceptable"
    return db_user



@router.put(
    "/{id}", response_model=User, description="Update a User by Id"
)
async def update_user(user: User, id: int, db: Session = Depends(get_db)):
    """
    Update an User stored in the database
    """
    update_row = user
    try:
        db_row = db.query(Usuario).filter(Usuario.id_user == id).first()
        if db_row:
            db_row.name = user.name
            db_row.email = user.email
            db_row.password = f.encrypt(user.password.encode("utf-8"))
            updated_row = db.merge(db_row)        # Usamos merge para modificar los datos de una fila
            print(updated_row)
            db.commit()
    except:
        status_code=status.HTTP_404_NOT_FOUND
        detail="User not found with the given ID"   
    return update_row


@router.delete("/{id}", response_model=User, status_code=200)
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        db_del = db.query(Usuario).filter(Usuario.id_user == id).first()
        db.delete(db_del)
        db.commit()
    except:
        #En caso de que no se pueda ejecutar la transacción lanzo una HttpException 204
        raise HTTPException(status_code=HTTP_204_NO_CONTENT)
    return db_del

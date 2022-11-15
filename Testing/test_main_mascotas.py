import json
from typing import List

import numpy as np
import pytest
import requests
from config.depy import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.testclient import TestClient
from main import app
from models.pets import Usuario
from pytest import fixture, mark
from schemas.user import User, UserCount
from sqlalchemy import MetaData, create_engine, func, select
from starlette.status import HTTP_204_NO_CONTENT

client = TestClient(app)

app = get_db()


lista_usuarios = [
  {
    "id_user": 1,
    "name": "Pepito",
    "email": "pepito@return.com",
    "password": "\\x674141414141426a627239543176676d354838564d647264564a4a6c5347626b484a376b52346d56526142465f5970655036486e61736f50466755754b63534e7053324d3931784a4732684d39516831525a465937677a776e363866386b686b37413d3d"
  },
  {
    "id_user": 2,
    "name": "Pip",
    "email": "pip@ripi.com",
    "password": "\\x674141414141426a6272392d7045684d705a5539435330364a61434359564547584247506130767a7152314941767671466a68446f4b4c436f7257464f444d4549696e327438374d41654e6a556858504768566f52436d576d6768415f6b752d64513d3d"
  },
  {
    "id_user": 3,
    "name": "Mosca",
    "email": "Mosca@ripi.com",
    "password": "\\x674141414141426a62722d5048503972434a73774f784c6b657475754c514b6b787168746141476b384c77546b4e6455317a566362625543614e594e4f4d6f3569654664445a47554c6751786c34776b4e58397075455552644144493335785349413d3d"
  },
  {
    "id_user": 4,
    "name": "DeLunes",
    "email": "deLunes@sopa.com",
    "password": "\\x674141414141426a6366675034774d736f4d4368776f3961694b724b436731494269414d6f327879322d38544762784c48315a424e424f446e546d58765544717a375334685353317a73477476354b35504e78667a6c7a49454241544138307945413d3d"
  },
  {
    "id_user": 8,
    "name": "Koseas",
    "email": "jode@gorde.com",
    "password": "\\x674141414141426a636e31393542456e3755397033753069614f4b5043553244426a6e4872674a413456456d6e526e534a6c2d7774374b434361596b4d577351765945484a3353456c48676b544731494a6133666b4369765359555a6971515330513d3d"
  },
  {
    "id_user": 7,
    "name": "string",
    "email": "string",
    "password": "\\x674141414141426a636f456e65676759495a627a544a574261664558717a3962454d667368476d4c3031484853545a396e3632474a4a564e6d62676147654e6255505050793231555955304b514d786639775461754b78366f42705f6d354f7a71413d3d"
  }
] 

#Obteniendo la lista de usuarios
def test_get_users():
    response = client.get("/users") 
    assert response.status_code == 200
    assert response.json() == lista_usuarios    
    

#Contamos el número de usuarios  
def test_get_users_count():
    response = client.get("/users") 
    assert len(response.json()) == 6
    assert response.status_code == 200 

    
#Comprobamos que id requerido sea como el id dado    
def test_get_user():
    user={
    "id_user": 2,
    "name": "Pip",
    "email": "pip@ripi.com",
    "password": "\\x674141414141426a6272392d7045684d705a5539435330364a61434359564547584247506130767a7152314941767671466a68446f4b4c436f7257464f444d4549696e327438374d41654e6a556858504768566f52436d576d6768415f6b752d64513d3d"
    } 
    response = client.get("/users/2") 
    assert response.status_code == 200
      

 
# def test_create_user():
#     response = client.post("/", 
#     headers={'Content-Type': 'application/x-www-form-urlencoded'},
#     json={"name": "Foo Bar", "email": "The Foo Barters", "password":"pass"},
#     allow_redirects=True)
#     assert response.status_code == 200


def test_update_user():
  user={
  "id_user": 2,
  "name": "Pip",
  "email": "pip@ripi.com",
  "password": "\\x674141414141426a6272392d7045684d705a5539435330364a61434359564547584247506130767a7152314941767671466a68446f4b4c436f7257464f444d4549696e327438374d41654e6a556858504768566f52436d576d6768415f6b752d64513d3d"
  } 
  response = client.get("/users/2") 
  assert response.status_code == 200







from xmlrpc.client import Boolean

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from config.db import Base, engine, meta


class Usuario(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    #pets_from_users = relationship("Mascotas_especificas")

class Mascotas_especificas(Base):
    __tablename__ = "pets"

    id_pet = Column(Integer, primary_key=True, index=True)
    name_animalito = Column(String, unique=True, index=True)
    vacunado = Column(Boolean, default=True)
    castrado = Column(Boolean, default=True)
    edad = Column(Integer, index=True)
    edad = Column(Integer, index=True)
    enfermedad = Column(String, unique=True, index=True)
    #id_species = Column(Integer, ForeignKey("species.id_species"))
    #id_user = Column(Integer, ForeignKey("users.id_user"))

class Especies(Base):
    __tablename__ = "species"

    id_species = Column(Integer, primary_key=True, index=True)
    especies = Column(String, unique=True, index=True)

    #pets_from_species = relationship("Mascotas_especificas")

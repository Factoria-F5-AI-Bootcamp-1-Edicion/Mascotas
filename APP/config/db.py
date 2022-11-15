import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from dotenv import load_dotenv
import os 

load_dotenv()
'''
#Borrar los prints...Cualquier hacker puede ver los archivos logs y de manera tonta sacarte el user y la password
print(os.getenv("USERNAME_DB"))
print(os.getenv("PASSWORD_DB"))
print(os.getenv("HOST"))
print(os.getenv("PORT"))
print(os.getenv("DATABASE"))
'''

DATABASE_URL =(f'postgresql+psycopg2://{os.getenv("USERNAME_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DATABASE")}')

engine = sqlalchemy.create_engine(DATABASE_URL)

meta = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine, MetaData
import psycopg2

from dotenv import load_dotenv
import os 

load_dotenv()

print(os.getenv("USERNAME_DB"))
print(os.getenv("PASSWORD_DB"))
print(os.getenv("HOST"))
print(os.getenv("PORT"))
print(os.getenv("DATABASE"))

engine = create_engine(f'postgresql+psycopg2://{os.getenv("USERNAME_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DATABASE")}')

meta = MetaData()

conn = engine.connect()
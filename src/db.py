from os import getenv
from sqlmodel import SQLModel, create_engine
from orm.author import *
from orm.book import *
from orm.book_author import *
from orm.book_genre import *
from orm.comment import *
from orm.genre import *
from orm.publisher import *
from orm.report import *
from orm.user import *

POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = getenv("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

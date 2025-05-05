from sqlmodel import SQLModel, create_engine, Session

from orm.author import *
from orm.book import *
from orm.book_author import *
from orm.book_genre import *
from orm.comment import *
from orm.genre import *
from orm.publisher import *
from orm.report import *
from orm.token import *
from orm.user import *
from config import *

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

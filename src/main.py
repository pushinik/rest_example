from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from db import create_db_and_tables
from routers.login_router import login_router
from routers.register_router import register_router
from routers.user_router import user_router
from routers.author_router import author_router
from routers.genre_router import genre_router
from routers.publisher_router import publisher_router
from routers.book_router import book_router
from routers.report_router import report_router

app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)
app.include_router(user_router)
app.include_router(author_router)
app.include_router(genre_router)
app.include_router(publisher_router)
app.include_router(book_router)
app.include_router(report_router)

@app.get("/")
async def root():
    return { "message": "Hello World" }

create_db_and_tables()

from fastapi import FastAPI

from db import create_db_and_tables
from routers.login_router import login_router
from routers.register_router import register_router
from routers.user_router import user_router

app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return { "message": "Hello World" }

create_db_and_tables()

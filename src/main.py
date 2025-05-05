from fastapi import FastAPI

from db import create_db_and_tables

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }

create_db_and_tables()

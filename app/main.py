import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()  # <- Загружает .env перед импортом engine

from app.database.engine import create_db_and_tables
import uvicorn
from fastapi import FastAPI
# from fastapi_pagination import add_pagination
from app.routes import users, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.warning('On startup')

    create_db_and_tables()
    yield

    logging.warning('On shutdown')

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(status.router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8003)

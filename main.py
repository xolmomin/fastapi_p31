from contextlib import asynccontextmanager

from fastapi import FastAPI

from admin import setup_admin
from database.base_model import db
from database.fixtures_loader import load_problems_from_json
from routers import router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('project ishga tushdi')
    # await load_problems_from_json(['problems', 'topics'])

    yield
    print('project toxtadi')


app = FastAPI(docs_url='/', lifespan=lifespan, swagger_ui_parameters={"defaultModelsExpandDepth": -1})
app.include_router(router, prefix='/api/v1')

setup_admin(app, db._engine)

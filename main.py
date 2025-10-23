from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers import router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('project ishga tushdi')

    yield
    print('project toxtadi')


app = FastAPI(docs_url='/', lifespan=lifespan)
app.include_router(router, prefix='/api/v1')

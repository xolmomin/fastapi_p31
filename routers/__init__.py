from enum import Enum

from fastapi import APIRouter
from fastapi.params import Query

from routers.problems import problem_router
from routers.users import user_router
from schemas.base_schema import ResponseSchema
from utils.datagen import GenerateDataService

router = APIRouter()

router.include_router(user_router)
router.include_router(problem_router)


class ModelType(str, Enum):
    TOPIC = "topic"
    LANGUAGE = "language"
    EXAMPLE = "example"
    ALL = "all"


@router.get('/faker')
async def generate_data(
        key: ModelType = Query(...),
        number: int = Query(gt=0)
):
    gen = GenerateDataService(key.value, number)
    await gen.generate()
    return ResponseSchema(data='generating ...')

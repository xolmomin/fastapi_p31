from fastapi import APIRouter
from starlette import status

from database import Problem, Topic
from schemas.base_schema import ResponseSchema
from schemas.problems import TopicCreateSchema, TopicReadSchema, ProblemReadSchema

problem_router = APIRouter()


@problem_router.get("/problems", response_model=ResponseSchema[list[ProblemReadSchema]])
async def get_problems():
    problems = await Problem.all()
    return ResponseSchema(data=problems)


@problem_router.get('/tags', response_model=ResponseSchema[list[TopicReadSchema]])
async def get_all_tags():
    tags = await Topic.all()
    return ResponseSchema(data=tags)


@problem_router.post('/tags', status_code=status.HTTP_201_CREATED)
async def create_tags(data: TopicCreateSchema):
    await Topic.create(**data.model_dump(exclude_none=True, exclude_unset=True))
    return {"success": True}

# connection
# session

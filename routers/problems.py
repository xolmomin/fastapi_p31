from fastapi import APIRouter
from starlette import status

from database import Problem, Topic
from schemas.problems import TopicCreateSchema

problem_router = APIRouter()


@problem_router.get("/problems")
async def get_problems():
    problems = await Problem.all()
    return {"message": "all problems", "data": problems}


@problem_router.get('/tags')
async def get_all_tags():
    tags = await Topic.all()
    return {"tags": tags}


@problem_router.post('/tags', status_code=status.HTTP_201_CREATED)
async def create_tags(data: TopicCreateSchema):
    await Topic.create(**data.model_dump(exclude_none=True, exclude_unset=True))
    return {"success": True}

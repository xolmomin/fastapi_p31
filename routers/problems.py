from fastapi import APIRouter
from starlette import status

from database import Tag
from schemas.problems import TagCreateSchema

problem_router = APIRouter()


@problem_router.get("/problems")
async def get_users():
    return {"message": "Problems"}


@problem_router.get('/tags')
async def get_all_tags():
    tags = await Tag.all()
    return {"tags": tags}


@problem_router.post('/tags', status_code=status.HTTP_201_CREATED)
async def create_tags(data: TagCreateSchema):
    await Tag.create(**data.model_dump(exclude_none=True, exclude_unset=True))
    return {"success": True}

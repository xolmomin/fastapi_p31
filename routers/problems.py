from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Body
from starlette import status

from database import Problem, Topic, Submission
from schemas import SubmissionReadSchema, ResponseSchema, TopicCreateSchema, TopicReadSchema, ProblemReadSchema
from utils.checker import check_code

problem_router = APIRouter()


@problem_router.get("/problems", response_model=ResponseSchema[list[ProblemReadSchema]])
async def get_problems():
    problems = await Problem.all()
    return ResponseSchema(data=problems)


@problem_router.get('/tags', response_model=ResponseSchema[list[TopicReadSchema]])
async def get_all_tags():
    tags = await Topic.all()
    return ResponseSchema(data=tags)


@problem_router.get('/submissions', response_model=ResponseSchema[list[SubmissionReadSchema]])
async def get_all_submissions():
    submissions = await Submission.all()
    return ResponseSchema(data=submissions)


@problem_router.post('/tags', status_code=status.HTTP_201_CREATED)
async def create_tags(data: TopicCreateSchema):
    await Topic.create(**data.model_dump(exclude_none=True, exclude_unset=True))
    return {"success": True}


@problem_router.post('/problems/{pk}/submit')
async def submit_problem(pk: int, background_tasks: BackgroundTasks, code: str = Body(..., media_type="text/plain")):
    background_tasks.add_task(check_code, pk, code)
    return {'message': "check submissions"}

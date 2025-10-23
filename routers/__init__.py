from fastapi import APIRouter
from routers.problems import problem_router
from routers.users import user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(problem_router)

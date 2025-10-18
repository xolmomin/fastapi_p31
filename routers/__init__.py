from fastapi import APIRouter

from routers.users import user_router
from routers.problems import problem_router

router = APIRouter()

router.include_router(user_router)
router.include_router(problem_router)

from fastapi import APIRouter

problem_router = APIRouter()


@problem_router.get("/problems")
async def get_users():
    return {"message": "Problems"}

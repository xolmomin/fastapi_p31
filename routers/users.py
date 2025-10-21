from fastapi import APIRouter

from database import Problem, User
from schemas import RegisterSchema

user_router = APIRouter()


@user_router.get("/users")
async def get_users():
    return {"message": "Hello Python"}


@user_router.post("/auth/register", tags=["auth"])
async def register_user(data: RegisterSchema):
    await User.create(**data)
    return {"message": "check your email"}


@user_router.post("/auth/login", tags=["auth"])
async def register_user(data: RegisterSchema):
    await User.create(**data)
    return {"message": "check your email"}

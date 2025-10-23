import re

from fastapi import HTTPException
from starlette import status

from database import Problem, User
from schemas import RegisterSchema, LoginSchema, ProblemCreateSchema


def is_email(value: str) -> bool:
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value) is not None


async def validate_email_and_username(data: RegisterSchema):
    if await User.exists(User.email == data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if await User.exists(User.username == data.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    return data


async def check_username_and_password(data: LoginSchema):
    if is_email(data.login):
        if not await User.exists(User.email == data.login):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found")
    else:
        if not await User.exists(User.username == data.login):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username not found")

    return data


async def check_unique_constraint_to_problem(data: ProblemCreateSchema):
    if await Problem.exists(Problem.name == data.name):
        raise HTTPException(status_code=400, detail="Problem already exists")

    return data

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import Response

from database import User
from schemas import TokenSchema, UserOutSchema, RegisterSchema, LoginSchema
from utils.security import get_current_user, create_access_token, create_refresh_token
from utils.validators import check_username_and_password

user_router = APIRouter()


@user_router.get("/get-me", response_model=UserOutSchema)
async def get_me(user: User = Depends(get_current_user)):
    return user


@user_router.get("/users")
async def get_users():
    return {"message": "Hello Python"}


@user_router.post("/auth/register", tags=["auth"])
async def register_user(data: RegisterSchema):
    await User.create(**data)
    # TODO send email
    return {"message": "check your email"}


@user_router.post("/auth/login", tags=["auth"], response_model=TokenSchema)
async def login_user(response: Response, data: LoginSchema = Depends(check_username_and_password)):
    access_token = create_access_token(data={"sub": data.login})
    refresh_token = create_refresh_token(data={"sub": data.login})
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)

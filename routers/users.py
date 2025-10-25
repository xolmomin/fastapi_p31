from fastapi import APIRouter, Depends
from fastapi.params import Query
from schemas import UserFilterSchema
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from database import User
# from database.base_model import get_session
from schemas import TokenSchema, UserOutSchema, RegisterSchema, LoginSchema
from schemas.base_schema import ResponseSchema
from schemas.users import UserProfileUpdateSchema
from utils.pagination import paginate_filter_sort
from utils.security import get_current_user, create_access_token, create_refresh_token
from utils.validators import check_username_and_password

user_router = APIRouter()


# @user_router.get("/")
# async def list_users(
#         db: AsyncSession = Depends(get_session),
#         page: int = Query(1, ge=1),
#         limit: int = Query(10, ge=1, le=100),
#         search: str | None = None,
#         sort_by: str | None = None,
#         sort_dir: str | None = Query("asc", pattern="^(asc|desc)$"),
#         first_name: str | None = None,
#         last_name: str | None = None,
#         username: str | None = None,
#         email: str | None = None,
# ):
#     filters = {
#         "first_name": first_name,
#         "last_name": last_name,
#         "username": username,
#         "email": email,
#     }
#
#     result = await paginate_filter_sort(
#         db=db,
#         model=User,
#         page=page,
#         limit=limit,
#         search=search,
#         search_fields=["first_name", "last_name", "email", "username"],
#         filters=filters,
#         sort_by=sort_by,
#         sort_dir=sort_dir,
#     )
#
#     return {
#         "count": result["total"],
#         "page": result["page"],
#         "page_size": result["page_size"],
#         "pages": result["pages"],
#         "results": result["items"],
#     }


@user_router.get("/get-me", response_model=UserOutSchema, tags=['users'])
async def get_me(user: User = Depends(get_current_user)):
    return user


@user_router.patch("/profile/update", tags=["users"])
async def update_user_profile(data: UserProfileUpdateSchema, user: User = Depends(get_current_user)):
    await User.update(user.id, **data.model_dump(exclude_none=True))
    return {'message': 'user profile updated'}


@user_router.post("/auth/register", tags=["auth"])
async def register_user(data: RegisterSchema):
    await User.create(**data)
    # TODO send email
    return {"message": "check your email"}


@user_router.post("/auth/login", tags=["auth"])
async def login_user(response: Response, data: LoginSchema = Depends(check_username_and_password)):
    access_token = create_access_token(data={"sub": data.login})
    refresh_token = create_refresh_token(data={"sub": data.login})
    return ResponseSchema(
        data=TokenSchema(access_token=access_token, refresh_token=refresh_token)
    )

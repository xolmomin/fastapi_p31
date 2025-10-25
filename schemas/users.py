from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from utils.security import get_password_hash


class LoginSchema(BaseModel):
    login: EmailStr | str
    password: str = Field(...)


class RegisterSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
    email: EmailStr = Field(...)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        hashed = get_password_hash(self.password)
        self.password = hashed
        self.confirm_password = hashed
        return self


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserOutSchema(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)

    class Config:
        from_attributes = True


class UserFilterSchema(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserProfileUpdateSchema(BaseModel):
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)

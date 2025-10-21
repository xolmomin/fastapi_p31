from pydantic import BaseModel, Field, EmailStr, model_validator

from utils.security import get_password_hash


class LoginSchema(BaseModel):
    password: str = Field(...)


class RegisterSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
    email: EmailStr = Field(...)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')

        self.password = get_password_hash(self.password)
        return self.model_dump(exclude={'confirm_password'})

    # async def async_validate(self): # TODO
    #     errors = []
    #
    #     if await User.exists(User.email == self.email):
    #         errors.append(ErrorWrapper(ValueError("Email already exists"), loc="email"))
    #
    #     if await User.exists(User.username == self.username):
    #         errors.append(ErrorWrapper(ValueError("Username already exists"), loc="username"))

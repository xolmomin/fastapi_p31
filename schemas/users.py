from pydantic import BaseModel, Field, EmailStr, model_validator

from utils.security import get_password_hash


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

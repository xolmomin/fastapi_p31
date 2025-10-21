from pydantic import Field

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DATABASE: str = Field(...)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_HOST: str = Field(...)
    POSTGRES_PORT: int = Field(...)

    JWT_SECRET_KEY: str = Field(...)
    JWT_ALGORITHM: str = Field(...)

    @property
    def postgresql_url(self) -> str:
        return (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}'
        )

    @property
    def async_postgresql_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}'
        )

    class Config:
        env_file = "env/.env"


settings = Settings()

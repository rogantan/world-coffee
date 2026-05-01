from pydantic_settings import BaseSettings
from yarl import URL

class Settings(BaseSettings):

    FASTAPI_API_V1_PATH: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MS_API_URL: str
    MS_LOGIN: str
    MS_PASSWORD: str

    @property
    def database_url(self) -> str:
        # return URL.build(
        #     scheme="postgresql+asyncpg",
        #     host=self.POSTGRES_HOST,
        #     port=self.POSTGRES_PORT,
        #     user=self.POSTGRES_USER,
        #     password=self.POSTGRES_PASSWORD,
        #     path=f"/{self.POSTGRES_DB}",
        # )
        #return f"postgresql+asyncpg://{self.POSTGRES_USER}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def database_url_alembic(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    class Config:
        env_file = ".env"

settings = Settings()
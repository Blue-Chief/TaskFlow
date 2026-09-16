from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:password"
    secret_key: str = "change-me"

    class Config:
        env_file = ".evn"

settings = Settings()
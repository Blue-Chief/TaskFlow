from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/taskflow"
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"

settings = Settings()
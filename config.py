from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    APP_TITLE: str
    UVICORN_HOST: str
    UVICORN_PORT: int
    DATABASE_URL: str
    SECRET: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


app_settings = Settings()

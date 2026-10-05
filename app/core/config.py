from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    STORAGE_PATH: str = "storage/documents"

    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB

    class Config:
        env_file = ".env"

settings = Settings()
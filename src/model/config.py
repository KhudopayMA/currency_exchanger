from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore", env_prefix="DB_")

    __name: str
    __port: int = 5432
    __host: str
    __user: str
    __password: str

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


db_settings = Settings()

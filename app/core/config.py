from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Amazonish Backend"
    env: str = "dev"

    db_host: str = "127.0.0.1"
    db_port: int = 3307
    db_name: str = "ecommerce"
    db_user: str = "root"
    db_password: str = "root"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        # SQLAlchemy URL format for PyMySQL:
        # mysql+pymysql://user:password@host:port/dbname
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

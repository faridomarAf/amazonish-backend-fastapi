from urllib.parse import quote_plus
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
        password = quote_plus(self.db_password)

        return (
            f"mysql+pymysql://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    fernet_key: str
    jwt_secret: str
    jwt_expire_minutes: int = 30
    admin_user: str = "admin"
    admin_password: str = "changeme"
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    collector_secret: str = "changeme"

    model_config = {"env_file": ".env"}

settings = Settings()

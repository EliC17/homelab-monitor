from pydantic_settings import BaseSettings
 
class Settings(BaseSettings):
    database_url: str
    fernet_key: str          # used from Milestone 6 onward, define now
    jwt_secret: str
    jwt_expire_minutes: int = 30
 
    class Config:
        env_file = ".env"
 
settings = Settings()

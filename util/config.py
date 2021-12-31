from pydantic import BaseSettings


# get enviroment variables
class Settings(BaseSettings):
    fastapi_db_hostname: str
    fastapi_db_port: str
    fastapi_db_username: str
    fastapi_db_password: str
    fastapi_db_name: str
    fastapi_secret_key: str
    fastapi_algorithm: str
    fastapi_access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic_settings import BaseSettings


class AppModel(BaseSettings):
    debug: bool = True


settings = AppModel()
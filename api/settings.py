from pydantic import BaseSettings, DirectoryPath
from functools import lru_cache

class Settings(BaseSettings):
    debug: bool = False
    models_path: DirectoryPath = "./models"

@lru_cache
def get_settings():
    return Settings()